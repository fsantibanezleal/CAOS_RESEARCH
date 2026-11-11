/* EXP-012 Gate C harness: read graph6 lines on standard input and print, for each graph, the value that the
 * production PRUNE hook prune_alpha (EXP-006) returns on the whole graph: 1 when it finds an independent set of size
 * ALPHA_BOUND+1, otherwise 0. Built against nauty 2.8.9 with the production flags (MAXN=WORDSIZE=32).
 */
#include "gtools.h"

int prune_alpha(graph *g, int n, int maxn);

int main(void) {
    char *s;
    graph g[MAXN * MAXM];
    while ((s = gtools_getline(stdin)) != NULL) {
        int n = graphsize(s);
        int m = SETWORDSNEEDED(n);
        stringtograph(s, g, m);
        printf("%d\n", prune_alpha(g, n, n));
    }
    return 0;
}
