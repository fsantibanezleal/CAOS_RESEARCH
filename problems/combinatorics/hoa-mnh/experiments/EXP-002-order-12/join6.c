/* EXP-002: read graph6 graphs H on m <= 30 vertices; write K_1 join H (a new vertex m adjacent to all) in graph6. */
#include <stdio.h>
#include <string.h>

int main(void) {
    static char line[512];
    while (fgets(line, sizeof line, stdin)) {
        const unsigned char *p = (const unsigned char *)line;
        if (p[0] < 63 || p[0] == 126) continue;
        int m = p[0] - 63, n = m + 1;
        int adj[32][32];
        memset(adj, 0, sizeof adj);
        p++;
        int bit = 0, val = 0;
        for (int j = 1; j < m; j++)
            for (int i = 0; i < j; i++) {
                if (bit == 0) { val = *p++ - 63; bit = 6; }
                bit--;
                if ((val >> bit) & 1) adj[i][j] = adj[j][i] = 1;
            }
        for (int i = 0; i < m; i++) adj[i][m] = adj[m][i] = 1;
        char out[512];
        int k = 0;
        out[k++] = (char)(n + 63);
        int acc = 0, nb = 0;
        for (int j = 1; j < n; j++)
            for (int i = 0; i < j; i++) {
                acc = (acc << 1) | adj[i][j];
                if (++nb == 6) { out[k++] = (char)(acc + 63); acc = 0; nb = 0; }
            }
        if (nb) { acc <<= (6 - nb); out[k++] = (char)(acc + 63); }
        out[k++] = '\n';
        fwrite(out, 1, k, stdout);
    }
    return 0;
}
