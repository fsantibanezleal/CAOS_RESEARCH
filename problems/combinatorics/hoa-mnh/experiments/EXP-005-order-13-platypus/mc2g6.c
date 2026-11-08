/* EXP-005 (hoa-mnh): convert multicode (GenHypohamiltonian output) on stdin to graph6 lines on stdout.
 * Multicode: byte n; then for x = 1..n-1 the neighbours of x with larger labels followed by 0 (the list of n is
 * omitted). Valid for n <= 62 (one-byte labels, one-byte graph6 order). */
#include <stdio.h>
#include <string.h>

int main(void) {
    int n;
    static int adj[64][64];
    while ((n = getchar()) != EOF) {
        if (n < 1 || n > 62) { fprintf(stderr, "unsupported order %d\n", n); return 2; }
        memset(adj, 0, sizeof adj);
        for (int x = 1; x < n; x++) {
            int y;
            while ((y = getchar()) != 0) {
                if (y == EOF || y <= x || y > n) { fprintf(stderr, "bad multicode\n"); return 2; }
                adj[x - 1][y - 1] = adj[y - 1][x - 1] = 1;
            }
        }
        char out[512];
        int pos = 0, bits = 0, val = 0;
        out[pos++] = (char) (n + 63);
        for (int j = 1; j < n; j++)
            for (int i = 0; i < j; i++) {
                val = (val << 1) | adj[i][j];
                if (++bits == 6) { out[pos++] = (char) (val + 63); bits = 0; val = 0; }
            }
        if (bits) { val <<= (6 - bits); out[pos++] = (char) (val + 63); }
        out[pos] = 0;
        puts(out);
    }
    return 0;
}
