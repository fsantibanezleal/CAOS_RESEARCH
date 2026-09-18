"""What is the TRUE vanishing order in rho of each row on the merge face?

mergeBC divides the merging row by rho^2. If that row really vanishes to
first order only, the clearing overshoots and leaves a 1/rho divergence,
which is exactly the explicit irho2 branches in the chart and exactly why
the thin box at rho = 0 certifies nothing. The raw matrix has sigma_3 ->
4.4e-3 at the face, so the mathematics is sound and only the chart is
wrong. This measures the order of every row so the clearing can be fixed.
"""
import mpmath as mp

mp.mp.dps = 60

PAIR_OF = [0, 0, 1, 1, 2, 2]
ROWS = [(0, 2), (0, 3), (0, 4), (0, 5), (2, 4), (2, 5)]


def rows_at(rho, tau, wu, wv, mi=1, mj=2):
    o = 1 + tau * tau
    al, be = (1 - tau * tau) / o, 2 * tau / o
    uv = [None] * 3
    uv[3 - mi - mj] = (mp.mpf(1), mp.mpf(0))
    uv[mi] = (wu + rho * al / 2, wv + rho * be / 2)
    uv[mj] = (wu - rho * al / 2, wv - rho * be / 2)
    P = []
    for (u, v) in uv:
        P.append((u, v))
        P.append((-u, v))
    out = []
    for (i, j) in ROWS:
        c = [mp.mpf(0)] * 3
        for k in range(6):
            if k == i or k == j:
                continue
            rik = mp.sqrt((P[i][0] - P[k][0]) ** 2 + (P[i][1] - P[k][1]) ** 2)
            rjk = mp.sqrt((P[j][0] - P[k][0]) ** 2 + (P[j][1] - P[k][1]) ** 2)
            area = ((P[j][0] - P[i][0]) * (P[k][1] - P[i][1])
                    - (P[j][1] - P[i][1]) * (P[k][0] - P[i][0]))
            c[PAIR_OF[k]] += (rik ** -3 - rjk ** -3) * area
        out.append(c)
    return out


tau0, wu0, wv0 = mp.mpf("0.992235"), mp.mpf("0.970750"), mp.mpf("0.993965")
r1, r2 = mp.mpf(2) ** -14, mp.mpf(2) ** -16
A = rows_at(r1, tau0, wu0, wv0)
B = rows_at(r2, tau0, wu0, wv0)

print("order in rho of every entry (from the ratio at rho=2^-14 vs 2^-16)")
print("  a NEGATIVE order means the entry DIVERGES\n")
print("  row            col0        col1(B)     col2(C)")
for n, (i, j) in enumerate(ROWS):
    tag = "MERGE" if (i, j) == (2, 4) else "     "
    cells = []
    for k in range(3):
        a, b = abs(A[n][k]), abs(B[n][k])
        if a == 0 or b == 0:
            cells.append("   zero  ")
            continue
        p = mp.log(a / b) / mp.log(4)
        cells.append(f"  {float(p):+7.3f}")
    print(f"  ({i},{j}) {tag}" + "".join(cells))

print("\nthe merging couple is row (2,4). Its order decides the clearing:")
n = ROWS.index((2, 4))
for k in range(3):
    a, b = abs(A[n][k]), abs(B[n][k])
    p = mp.log(a / b) / mp.log(4)
    print(f"   col{k}: order {float(p):+.4f}   value at 2^-16 = "
          f"{mp.nstr(B[n][k], 8)}")
