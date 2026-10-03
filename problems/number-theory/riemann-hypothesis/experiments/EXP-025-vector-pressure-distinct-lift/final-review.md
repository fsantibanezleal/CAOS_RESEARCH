# Final mathematical and source review

Reviewed 2026-10-03 after both numerical paths completed. This is an internal
proof review, not external peer review or a local Lean rebuild.

## Universal transfer

The block proof needs nonnegative pair weights, each index-span mass at most
two, nonnegative individual pressures, and the local theorem on the full
nonnegative orthant. It never replaces the vector by its minimum component.
The sum B bounds each global gap's charge; averaging complete blocks over
all offsets multiplies that charge by (m-r)/m. The exact count of complete
blocks is max(l-m+1,0). The endpoint subtraction D therefore works even
when l<m. Finite controls supplement, rather than prove, this argument.

Convex trace pinching is applicable to the positive Gram matrix; omitted
singletons have Psi(1)=0. In a block with a large eigenvalue, its clipped
contribution exceeds tau^2>=D and all other contributions and pressures
are nonnegative. Otherwise clipped energy equals raw energy.

For the mixed completion one may avoid any appeal to noncommuting square
monotonicity: diagonalize P and write A<=2cI in that basis. Then
tr(A P)-tr(A^2)/4 <= sum_i[A_ii*p_i-A_ii^2/4]
<=sum_i phi_c(p_i), by scalar completion for A_ii<=2c.
With A=2D0+2D0^(-1/2)C D0^(-1/2), its upper bound follows from
d+tau/d<=max(1+tau,2+tau/2) for d in [1,2]. The remaining Hilbert-Schmidt
estimate is entrywise, so C need not be positive.

The threshold proof uses Q_+Q_-=0 and tr(P Q_+)>=0. Completing squares
on Q_+ costs only c^2 rank(Q_+), with rank at most h+k; minimizing the
Q_- term over positive matrices gives -tr((P-cI)_+^2). The low diagonal
identity is tr(D0^2)=3tr(D0)-2l. Since 2c-3>=0, the mass minima 3h+2k
give exactly 6c-7-c^2 and 4c-2-c^2. No positivity of the complex pair sum
is used. All count definitions and the final denominator agree.

The corrected integrated BGSTB theorem applies to the two fixed functions
R and R'' separately, before multiplying the latter by 1/(4 log(T)^2).
The profile is uniformly positive, admits positive smooth cutoffs, and
converges in L1 and L2. Fixed-block Gram perturbation is uniform in all
real gaps, with the stated Lipschitz estimate. The limit order fixes
m,tau,c first, then takes T to infinity, then removes the cutoff.

## External lemma and normalization

Pinned Solution.lean lines 16838--16848 supply AT7_cert_full by reflection;
lines 17048--17065 identify Fw_W7 with precisely AT7.G and prove cert_AM on
all nonnegative six-gap vectors. The source arrays in aW7 and bW7 equal
those independently parsed from AT7.G. Its delta is 787380/100000000.
The source kernel is the squared normalized Fourier transform of the
thirteen-term profile; its MAM normalization cancels. The two local
window proofs agree and establish the stated lower H.

The source is Samuel Lavery's attempt-013, building on typh's optimized
window/evaluator and Ainta's weighted-point refinement. Its metadata reports
a critical-line score 0.6734302. The archived external attestation and log
report Lean and nanoda checking under propext, Quot.sound and Classical.choice.
They are attributed external evidence. No local formal rebuild, verification
of every imported analytic theorem in Lean, or peer review is asserted.
The numerical distinct-strip consequence is a derived application of this
local theorem and BGSTB/Knausgard's attributed machinery.

## Exact arithmetic and overlap

The predeclared fixed parameters pass both independent calculations. The
native Arb path checks 169 scalar kernel integrals; the standard-library
Fraction path proves the closed window formula with outward rational
enclosures. The latter independently parses the certified functional and
checks 288 list/block cases and 183 pair-count cases, including unequal
pressure values. Every transfer residual is nonnegative.

The result is 30945470743359/36955122080000=0.8373797460706156... .
On October 3, arXiv:2609.33043 still exposes only v1 and its distinct-strip
fraction 16260119298029/19426831050000. Lavery's submission proves a
critical-line consequence, rather than this mixed-multiplicity distinct-strip
application. Searches for distinct zeros with 0.837 or Lavery did not locate
this exact consequence. This limited overlap assessment cannot establish
worldwide novelty. The vector counting and scalar identity are classical;
the attributed new local input enables the improved numerical application.

## Disposition

The implication and exact consequence pass internal review with the stated
external local theorem as a dependency. Route to the same focused companion
as EXP-020; no separate paper for the vector summation or scalar calculation.
The completed EXP-020 certificate provides a separate, locally replayed
stronger-than-prior bound. EXP-023 remains unproved. RH and the short-window
onset remain unchanged. Neither source attribution nor public persistence
establishes expert acceptance or an effective finite height.
