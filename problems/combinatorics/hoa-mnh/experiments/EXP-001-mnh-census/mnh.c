/* EXP-001 exact filter: maximal non-Hamiltonian (MNH) graphs and the residuals of their longest cycles.
 *
 * Reads graph6 lines (3 <= n <= 14) from stdin. For each graph:
 *  1. necessary prune: not complete, and every nonadjacent pair has deg(u) + deg(v) <= n - 1;
 *  2. P[S][v] = bitmask of start vertices of paths covering exactly the vertex set S and ending at v
 *     (dynamic programming over subsets, exact);
 *  3. MNH iff no Hamilton cycle (no v and u in P[V][v] with u ~ v) and every nonadjacent pair u, v has u in P[V][v];
 *  4. for an MNH graph: circumference c = max |S| with a cycle on S (|S| >= 3, u in P[S][v], u ~ v), and for every
 *     such S of size c the residual R = V \ S: complete?, number of components, all components complete?,
 *     connected and not complete?
 * Prints one line per MNH graph:
 *   <graph6> c=<c> sets=<#longest-cycle vertex sets> hoa=<1 if every residual complete>
 *   q2=<1 if every component of every residual complete> q3=<1 if some residual connected and not complete>
 *   maxcomp=<max number of residual components>
 * and "read <N> pruned <M> mnh <K>" on stderr.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define MAXN 14
static int n;
static uint16_t adj[MAXN];
static uint16_t *P; /* P[S * n + v] */

static int parse_g6(const char *s) {
    const unsigned char *p = (const unsigned char *)s;
    if (p[0] < 63 || p[0] == 126) return -1;
    n = p[0] - 63; p++;
    if (n < 3 || n > MAXN) return -1;
    memset(adj, 0, sizeof adj);
    int bit = 0, val = 0;
    for (int j = 1; j < n; j++)
        for (int i = 0; i < j; i++) {
            if (bit == 0) { if (!*p || *p == '\n' || *p == '\r') return -1; val = *p++ - 63; bit = 6; }
            bit--;
            if ((val >> bit) & 1) { adj[i] |= 1u << j; adj[j] |= 1u << i; }
        }
    return 0;
}

static void paths(void) {
    uint32_t full = 1u << n;
    memset(P, 0, sizeof(uint16_t) * full * n);
    for (int v = 0; v < n; v++) P[(1u << v) * n + v] = 1u << v;
    for (uint32_t S = 1; S < full; S++)
        for (int v = 0; v < n; v++) {
            uint16_t st = P[S * n + v];
            if (!st) continue;
            uint16_t ext = adj[v] & ~S;
            while (ext) {
                int w = __builtin_ctz(ext); ext &= ext - 1;
                P[(S | (1u << w)) * n + w] |= st;
            }
        }
}

static int has_cycle(uint32_t S) {
    if (__builtin_popcount(S) < 3) return 0;
    for (int v = 0; v < n; v++)
        if ((S >> v) & 1)
            if (P[S * n + v] & adj[v] & S & ~(1u << v)) return 1;
    return 0;
}

/* components of the induced subgraph on R; returns count, sets *allcomplete */
static int components(uint16_t R, int *allcomplete) {
    int count = 0; *allcomplete = 1;
    uint16_t left = R;
    while (left) {
        uint16_t comp = left & (~left + 1), frontier = comp;
        while (frontier) {
            int v = __builtin_ctz(frontier); frontier &= frontier - 1;
            uint16_t nb = adj[v] & R & ~comp;
            comp |= nb; frontier |= nb;
        }
        uint16_t c = comp;
        while (c) {
            int v = __builtin_ctz(c); c &= c - 1;
            if ((adj[v] & comp) != (comp & ~(1u << v))) { *allcomplete = 0; }
        }
        left &= ~comp;
        count++;
    }
    return count;
}

int main(void) {
    P = malloc(sizeof(uint16_t) * (1u << MAXN) * MAXN);
    static char line[512];
    long long nread = 0, npruned = 0, nmnh = 0;
    while (fgets(line, sizeof line, stdin)) {
        if (parse_g6(line) < 0) continue;
        nread++;
        uint16_t V = (uint16_t)((1u << n) - 1);
        int deg[MAXN], ok = 1, complete = 1;
        for (int v = 0; v < n; v++) deg[v] = __builtin_popcount(adj[v]);
        for (int u = 0; u < n && ok; u++)
            for (int v = u + 1; v < n; v++)
                if (!((adj[u] >> v) & 1)) { complete = 0; if (deg[u] + deg[v] > n - 1) { ok = 0; break; } }
        if (!ok || complete) { npruned++; continue; }
        paths();
        if (has_cycle(V)) continue;
        int mnh = 1;
        for (int u = 0; u < n && mnh; u++)
            for (int v = u + 1; v < n; v++)
                if (!((adj[u] >> v) & 1) && !((P[V * n + v] >> u) & 1)) { mnh = 0; break; }
        if (!mnh) continue;
        nmnh++;
        int c = 0;
        for (uint32_t S = 1; S <= V; S++)
            if (__builtin_popcount(S) > c && has_cycle(S)) c = __builtin_popcount(S);
        int sets = 0, hoa = 1, q2 = 1, q3 = 0, maxcomp = 0;
        for (uint32_t S = 1; S <= V; S++) {
            if (__builtin_popcount(S) != c || !has_cycle(S)) continue;
            sets++;
            uint16_t R = V & ~S;
            int allc, k = components(R, &allc);
            int rcomplete = (k == 1 && allc) || R == 0;
            if (!rcomplete) hoa = 0;
            if (!allc) q2 = 0;
            if (k == 1 && !allc) q3 = 1;
            if (k > maxcomp) maxcomp = k;
        }
        line[strcspn(line, "\r\n")] = 0;
        printf("%s c=%d sets=%d hoa=%d q2=%d q3=%d maxcomp=%d\n", line, c, sets, hoa, q2, q3, maxcomp);
    }
    fprintf(stderr, "read %lld pruned %lld mnh %lld\n", nread, npruned, nmnh);
    return 0;
}
