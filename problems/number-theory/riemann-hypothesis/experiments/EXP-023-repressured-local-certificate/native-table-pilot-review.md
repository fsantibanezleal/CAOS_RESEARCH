# Native hypergeometric pilot: enclosure failure, not a false table

The first declared 512-cell pilot completed no cells. Its retained receipt
identifies cell zero as unresolved after eight bisections; it did not exhaust
its thirty-second budget. The exact-point normalization controls passed.
At x=0, native and archived evaluations both enclose
w=1 and w''=-6.09600709917975583342..., whereas the stored cell lower
bounds are 0.9997858948136449 and -6.097955584526063.
On the smallest attempted interval [0,1/1024000], the native w lower
enclosure is approximately 0.99328 and its second-derivative enclosure
has radius about 0.09. These fail the required comparisons through excess
interval width. They neither refute the stored bounds nor audit them.

The original direct-interval source and its source-bound receipt are preserved.
A separately declared Taylor audit will use native hypergeometric functions
at rational midpoints and analytic whole-cell remainder bounds. It will not
change the frozen worker runtime or its tables. A new successful pilot is
required before a full-table run is admitted.

At 22:20 UTC the revised local cover is still 95/96, and EXP-020 is 94/96.
Neither certificate is complete, and no improved zero-count theorem is claimed.

The separately declared midpoint Taylor pilot then proved both table comparisons
on every closed cell of its 512-cell range in 0.446 seconds, without bisection.
Both increased-bound controls rejected their deliberately false test inputs.
Its linear throughput projection is 45.46 seconds for 52,240 cells, satisfying
the declared 600-second admission gate. One full-table run on one CPU is
therefore admitted; its actual receipt, not this projection, determines success.

That full Taylor run stopped inconclusively at cell 32,031 after 94.46 seconds.
Its receipt certifies only the first 32,031 cells and has all-cells false.
The global squared-kernel second-derivative bound can dominate a very small
kernel value near a zero, even after eight bisections. Preserve this source
and receipt. A kernel-first variant is declared separately before implementation.

The kernel-first variant passed all 512 pilot cells and both increased-bound
controls in 0.455 seconds. Its projected complete-table runtime is 46.38 seconds,
within the declared 600-second admission bound. One full audit is admitted.

The kernel-first full run passed all 52,240 closed cells in both bound tables
in 148.04 seconds, with 116,922 subcell enclosures and maximum bisection
depth three. Its source-bound receipt has all-cells true and no unresolved
cell. Native midpoint jet controls and increased-bound controls passed.
This closes this additional input-audit obligation within Python/FLINT/Arb;
it does not close the separate eight-dimensional cover. The two earlier
inconclusive variants and their original receipts are retained in full.
