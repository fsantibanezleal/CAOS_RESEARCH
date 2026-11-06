/* EXP-005 exact filter: read graph6 lines from stdin (n <= 32), keep the graphs with independence number
 * exactly ALPHA and vertex connectivity at least K.
 *
 * Independence number: exact branch and bound on bitsets (maximum independent set = maximum clique of the
 * complement). Connectivity >= K: the graph is connected, has more than K vertices, and stays connected after
 * deleting every vertex set of size 1..K-1 (exhaustive; K <= 5 here). Both are exact; no heuristic.
 *
 * Usage: filter ALPHA K [--print]   prints "read <N> kept <M>" on stderr; with --print the kept graph6 lines
 * go to stdout.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

static int n;
static uint32_t adj[32];

static int parse_g6(const char *s) {
    const unsigned char *p = (const unsigned char *)s;
    if (*p == '>') p += 10; /* optional ">>graph6<<" header */
    if (p[0] < 63 || p[0] == 126) return -1;
    n = p[0] - 63; p++;
    if (n > 32) return -1;
    memset(adj, 0, sizeof adj);
    int bit = 0; int val = 0;
    for (int j = 1; j < n; j++) {
        for (int i = 0; i < j; i++) {
            if (bit == 0) { if (!*p || *p == '\n' || *p == '\r') return -1; val = *p++ - 63; bit = 6; }
            bit--;
            if ((val >> bit) & 1) { adj[i] |= 1u << j; adj[j] |= 1u << i; }
        }
    }
    return 0;
}

/* maximum independent set size within candidate set cand */
static int best;
static void mis(uint32_t cand, int size) {
    if (!cand) { if (size > best) best = size; return; }
    if (size + __builtin_popcount(cand) <= best) return;
    int v = __builtin_ctz(cand);
    /* branch: take v (remove v and its neighbours) */
    mis(cand & ~(1u << v) & ~adj[v], size + 1);
    /* skip v */
    mis(cand & ~(1u << v), size);
}

static int connected_without(uint32_t removed) {
    uint32_t all = (n == 32 ? 0xffffffffu : ((1u << n) - 1)) & ~removed;
    if (!all) return 1;
    uint32_t seen = all & (~all + 1), frontier = seen;
    while (frontier) {
        int v = __builtin_ctz(frontier);
        frontier &= frontier - 1;
        uint32_t nb = adj[v] & all & ~seen;
        seen |= nb; frontier |= nb;
    }
    return seen == all;
}

static int kconnected(int k) {
    if (n <= k) return 0;
    if (!connected_without(0)) return 0;
    /* delete every set of size 1..k-1 */
    int idx[8];
    for (int s = 1; s < k; s++) {
        for (int i = 0; i < s; i++) idx[i] = i;
        while (1) {
            uint32_t rem = 0;
            for (int i = 0; i < s; i++) rem |= 1u << idx[i];
            if (!connected_without(rem)) return 0;
            int i = s - 1;
            while (i >= 0 && idx[i] == n - s + i) i--;
            if (i < 0) break;
            idx[i]++;
            for (int j = i + 1; j < s; j++) idx[j] = idx[j - 1] + 1;
        }
    }
    return 1;
}

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: filter ALPHA K [--print]\n"); return 2; }
    int alpha = atoi(argv[1]), k = atoi(argv[2]);
    int print = argc > 3 && strcmp(argv[3], "--print") == 0;
    static char line[4096];
    long long read = 0, kept = 0;
    while (fgets(line, sizeof line, stdin)) {
        if (parse_g6(line) < 0) continue;
        read++;
        best = 0;
        mis(n == 32 ? 0xffffffffu : ((1u << n) - 1), 0);
        if (best != alpha) continue;
        if (!kconnected(k)) continue;
        kept++;
        if (print) fputs(line, stdout);
    }
    fprintf(stderr, "read %lld kept %lld\n", read, kept);
    return 0;
}
