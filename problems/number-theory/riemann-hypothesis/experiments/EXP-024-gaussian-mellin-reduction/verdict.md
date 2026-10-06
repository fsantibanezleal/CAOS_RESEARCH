# EXP-024 verdict: confirmed supporting analytic reduction

The exact shifted Gaussian identity, crossed residue and absolute dual
convergence are derived in proof.md. The all-order finite Hermite expansion
has an explicit phase remainder. Repeated nonstationary integration by
parts controls the off-band terms. A finite inverse Gaussian smoothing
construction in compact-window-extension.md extends the reduction to fixed
smooth compact windows, with an o(H) representation error for fixed
1/2<theta<1, 0<nu<1 and shifts O(1/log T). The signed main sum is retained.

The declaration was pushed as 8528b1e6 before controls. The initial analytic
proof and kernel controls were pushed as 440e5d1b. Nine independent symbolic
Gaussian moments, eight pairs of independently enclosed Gaussian/Mellin
integrals and 32 explicit remainder comparisons pass at 192 bits. A full
original zeta moment also agrees with its separately enclosed 32-term
dual series and explicit derivative tail; the wrong residue sign is
rejected. Eight symbolic heat-multiplier derivative checks pass. These
finite controls check normalizations; the uniform conclusions come from
the analytic proofs, not finite agreement. Ruff passes on the final code.

Both setup and lint history are retained. The historical full-moment
receipt binds its captured initial source; the current receipt binds the
cleaned code. There is no unresolved mathematical discrepancy in the
recorded controls. No external referee or independent novelty confirmation
has been obtained.

This closes the representation step for the stated smooth windows,
bounded composite twists and shifts. It does not estimate the resulting
signed divisor/conductor sum, prove an enlarged mollified-moment range or
improve the 0.534 short-window onset. Functional equations, Mellin/Gaussian
transforms and Taylor/heat remainders are classical; worldwide priority is
not claimed. The original gamma-phase obstruction concerned a different
pointwise approximation and is not contradicted.

Disposition: research record supporting RH-F4 / issue #360. Its prospective
manuscript home is short-interval-levinson if the remaining signed moment
theorem is proved coherently. No standalone manuscript or Zenodo deposit
is justified by this classical reduction alone. EXP-020 and EXP-023 remain
independent in-flight certificates. The user's stopping condition is unmet.
