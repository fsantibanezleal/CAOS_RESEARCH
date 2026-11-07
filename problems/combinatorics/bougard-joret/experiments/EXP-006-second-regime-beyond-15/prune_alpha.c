/* geng PRUNE hook for EXP-006: discard a partial graph that already has an independent set of size ALPHA_BOUND+1.
 *
 * Soundness: geng extends a graph only by adding vertices; the graph on the first n vertices is an induced
 * subgraph of every completion, and the independence number of an induced subgraph never exceeds that of the
 * graph. A partial graph with an independent set of size ALPHA_BOUND+1 therefore has no completion with
 * independence number at most ALPHA_BOUND, and the filter would reject every completion anyway.
 * Compile (one binary per bound): gcc -O3 -o geng_a<A> -DMAXN=WORDSIZE -DWORDSIZE=32 -DPRUNE=prune_alpha
 *   -DALPHA_BOUND=<A> geng.c prune_alpha.c gtoolsW.o nautyW1.o nautilW1.o naugraphW1.o schreier.o naurng.o
 */
#include "gtools.h"

static unsigned long am[MAXN];
static int found;

static void search(unsigned long cand, int size, int target) {
    if (found) return;
    if (size >= target) { found = 1; return; }
    if (size + __builtin_popcountl(cand) < target) return;
    int v = __builtin_ctzl(cand);
    search(cand & ~(1UL << v) & ~am[v], size + 1, target);
    search(cand & ~(1UL << v), size, target);
}

int prune_alpha(graph *g, int n, int maxn) {
    int target = ALPHA_BOUND + 1;
    if (n < target) return 0;
    for (int i = 0; i < n; i++) {
        am[i] = 0;
        for (int j = 0; j < n; j++)
            if (ISELEMENT(g + i, j)) am[i] |= 1UL << j;
    }
    found = 0;
    search((n >= 64 ? ~0UL : ((1UL << n) - 1)), 0, target);
    return found;
}
