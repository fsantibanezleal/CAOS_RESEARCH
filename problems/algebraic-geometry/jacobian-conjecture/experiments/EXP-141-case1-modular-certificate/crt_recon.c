/* EXP-141: Chinese remaindering and rational reconstruction of the cofactor coordinates.
 *
 * Usage: crt_recon <work_dir> <k> <out_file|->
 *   <work_dir>/primes.txt   kept primes, one per line, in the order they were kept
 *   <work_dir>/res/<p>.bin  M little-endian uint32 residues (coordinate order fixed by keys.json)
 * Uses the first k primes for CRT (FLINT fmpz_comb, non-negative representative) and fmpq_reconstruct_fmpz on every coordinate, then
 * checks each reconstructed value modulo the next three kept primes (held out). Prints a summary line:
 *   RECON k=<k> M=<M> ok=<n reconstructed and agreeing> fail_recon=<n> fail_check=<n> maxbits=<num+den bits>
 * When every coordinate passes and out_file is not "-", writes "num/den" per coordinate, one per line.
 * Exit status 0 when every coordinate passes, 1 otherwise, 2 on usage or input errors.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <flint/flint.h>
#include <flint/fmpz.h>
#include <flint/fmpq.h>
#include <flint/ulong_extras.h>

static long file_words(const char *path) {
    FILE *f = fopen(path, "rb");
    if (!f) return -1;
    fseek(f, 0, SEEK_END);
    long n = ftell(f) / 4;
    fclose(f);
    return n;
}

/* 1 when the rational q equals the stored residue modulo each held-out prime primes[k..kk-1]. */
static int held_out_agrees(const fmpq_t q, const ulong *r, const ulong *primes, long k, long kk) {
    for (long j = k; j < kk; j++) {
        ulong p = primes[j];
        ulong num = fmpz_fdiv_ui(fmpq_numref(q), p);
        ulong den = fmpz_fdiv_ui(fmpq_denref(q), p);
        if (den == 0) return 0;
        ulong val = n_mulmod2_preinv(num, n_invmod(den, p), p, n_preinvert_limb(p));
        if (val != r[j]) return 0;
    }
    return 1;
}

static int read_u32(const char *path, unsigned int *buf, long m) {
    FILE *f = fopen(path, "rb");
    if (!f) return 0;
    long got = (long) fread(buf, 4, (size_t) m, f);
    fclose(f);
    return got == m;
}

int main(int argc, char **argv) {
    if (argc != 4) { fprintf(stderr, "usage: crt_recon <work_dir> <k> <out_file|->\n"); return 2; }
    const char *dir = argv[1];
    long k = atol(argv[2]);
    char path[4096];
    snprintf(path, sizeof path, "%s/primes.txt", dir);
    FILE *pf = fopen(path, "r");
    if (!pf) { fprintf(stderr, "cannot open %s\n", path); return 2; }
    long cap = 1024, np = 0;
    ulong *primes = malloc(sizeof(ulong) * cap);
    unsigned long long x;
    while (fscanf(pf, "%llu", &x) == 1) {
        if (np == cap) { cap *= 2; primes = realloc(primes, sizeof(ulong) * cap); }
        primes[np++] = (ulong) x;
    }
    fclose(pf);
    if (k < 1 || k + 3 > np) { fprintf(stderr, "need k >= 1 and k + 3 <= %ld primes\n", np); return 2; }
    snprintf(path, sizeof path, "%s/res/%lu.bin", dir, primes[0]);
    long M = file_words(path);
    if (M <= 0) { fprintf(stderr, "cannot size %s\n", path); return 2; }

    /* residues[c * (k + 3) + j] = coordinate c modulo prime j */
    long kk = k + 3;
    ulong *res = malloc(sizeof(ulong) * (size_t) M * (size_t) kk);
    unsigned int *buf = malloc(sizeof(unsigned int) * (size_t) M);
    if (!res || !buf) { fprintf(stderr, "out of memory\n"); return 2; }
    for (long j = 0; j < kk; j++) {
        snprintf(path, sizeof path, "%s/res/%lu.bin", dir, primes[j]);
        if (file_words(path) != M || !read_u32(path, buf, M)) { fprintf(stderr, "bad residue file %s\n", path); return 2; }
        for (long c = 0; c < M; c++) res[c * kk + j] = buf[c];
    }
    free(buf);

    fmpz_comb_t comb;
    fmpz_comb_temp_t temp;
    fmpz_comb_init(comb, primes, k);
    fmpz_comb_temp_init(temp, comb);
    fmpz_t a, m;
    fmpq_t q;
    fmpz_init(a); fmpz_init(m); fmpq_init(q);
    fmpz_one(m);
    for (long j = 0; j < k; j++) fmpz_mul_ui(m, m, primes[j]);

    FILE *out = NULL;
    char **vals = NULL;
    if (strcmp(argv[3], "-") != 0) vals = calloc((size_t) M, sizeof(char *));
    long ok = 0, frec = 0, fchk = 0;
    flint_bitcnt_t maxbits = 0;
    char *done = calloc((size_t) M, 1);
    fmpz_t D;                       /* lcm of the denominators of the coordinates validated in the first pass */
    fmpz_init(D);
    fmpz_one(D);
    for (long c = 0; c < M; c++) {
        fmpz_multi_CRT_ui(a, res + c * kk, comb, temp, 0);   /* 0 <= a < m, as reconstruction requires */
        if (!fmpq_reconstruct_fmpz(q, a, m)) { frec++; continue; }
        if (!held_out_agrees(q, res + c * kk, primes, k, kk)) { fchk++; continue; }
        ok++;
        done[c] = 1;
        fmpz_lcm(D, D, fmpq_denref(q));
        flint_bitcnt_t b = fmpz_bits(fmpq_numref(q)) + fmpz_bits(fmpq_denref(q));
        if (b > maxbits) maxbits = b;
        if (vals) vals[c] = fmpq_get_str(NULL, 10, q);
    }
    /* Second pass (common denominator): for a coordinate whose rational reconstruction failed, try n / D with
     * n = D a mod m in the symmetric range, accepted only when n is far below m (at least 64 bits of margin)
     * and the value agrees modulo the held-out primes. The exact identity check stays the proof. */
    long lifted = 0;
    if (ok > 0 && ok < M) {
        fmpz_t bnum, half;
        fmpz_init(bnum); fmpz_init(half);
        fmpz_fdiv_q_2exp(half, m, 1);
        for (long c = 0; c < M; c++) {
            if (done[c]) continue;
            fmpz_multi_CRT_ui(a, res + c * kk, comb, temp, 0);
            fmpz_mul(bnum, a, D);
            fmpz_mod(bnum, bnum, m);
            if (fmpz_cmp(bnum, half) > 0) fmpz_sub(bnum, bnum, m);
            if (fmpz_bits(bnum) + fmpz_bits(D) + 64 > fmpz_bits(m)) continue;
            fmpq_set_fmpz_frac(q, bnum, D);
            if (!held_out_agrees(q, res + c * kk, primes, k, kk)) continue;
            lifted++;
            done[c] = 1;
            flint_bitcnt_t b = fmpz_bits(fmpq_numref(q)) + fmpz_bits(fmpq_denref(q));
            if (b > maxbits) maxbits = b;
            if (vals) vals[c] = fmpq_get_str(NULL, 10, q);
        }
        fmpz_clear(bnum); fmpz_clear(half);
    }
    printf("RECON k=%ld M=%ld ok=%ld fail_recon=%ld fail_check=%ld maxbits=%lu denlift=%ld Dbits=%lu\n", k, M,
           ok + lifted, frec, fchk, (unsigned long) maxbits, lifted, (unsigned long) fmpz_bits(D));
    int all = (ok + lifted == M);
    free(done);
    fmpz_clear(D);
    if (vals && all) {
        out = fopen(argv[3], "w");
        if (!out) { fprintf(stderr, "cannot write %s\n", argv[3]); return 2; }
        for (long c = 0; c < M; c++) { fputs(vals[c], out); fputc('\n', out); }
        fclose(out);
    }
    if (vals) { for (long c = 0; c < M; c++) if (vals[c]) flint_free(vals[c]); free(vals); }
    fmpz_clear(a); fmpz_clear(m); fmpq_clear(q);
    fmpz_comb_temp_clear(temp);
    fmpz_comb_clear(comb);
    free(res); free(primes);
    return all ? 0 : 1;
}
