/* geng PRUNE hook for EXP-001: discard a partial graph that already has a nonadjacent pair (u, v) with
 * deg(u) + deg(v) > maxn - 1.
 *
 * Soundness: geng extends a graph by adding vertices; edges among existing vertices never change and degrees
 * only grow, so the pair stays nonadjacent with degree sum > maxn - 1 in every completion, and no completion is
 * maximal non-Hamiltonian (Bondy-Chvatal: such a pair could be added without changing Hamiltonicity).
 * Compile: gcc -O3 -o geng_mnh -DMAXN=WORDSIZE -DWORDSIZE=32 -DPRUNE=prune_degsum geng.c prune_degsum.c gtools.o
 *          nauty1.o nautil1.o naugraph1.o schreier.o naurng.o
 */
#include "gtools.h"

int prune_degsum(graph *g, int n, int maxn) {
    int deg[MAXN];
    for (int i = 0; i < n; i++) deg[i] = POPCOUNT(g[i]);
    for (int i = 0; i < n; i++)
        for (int j = i + 1; j < n; j++)
            if (!ISELEMENT(g + i, j) && deg[i] + deg[j] > maxn - 1) return 1;
    return 0;
}
