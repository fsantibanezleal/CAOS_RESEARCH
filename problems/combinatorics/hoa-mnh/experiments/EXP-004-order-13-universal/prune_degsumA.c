/* Probe hook (case A at order maxn + 1): discard a partial graph H with a nonadjacent pair whose degree sum
 * exceeds maxn - 2. G = K1 join H is MNH only if every nonadjacent pair of G has degree sum <= |G| - 1, i.e.
 * deg_H(u) + deg_H(v) <= maxn - 2; degrees only grow under geng's vertex additions, so the prune is sound. */
#include "gtools.h"
int prune_degsumA(graph *g, int n, int maxn) {
    int deg[MAXN];
    for (int i = 0; i < n; i++) deg[i] = POPCOUNT(g[i]);
    for (int i = 0; i < n; i++)
        for (int j = i + 1; j < n; j++)
            if (!ISELEMENT(g + i, j) && deg[i] + deg[j] > maxn - 2) return 1;
    return 0;
}
