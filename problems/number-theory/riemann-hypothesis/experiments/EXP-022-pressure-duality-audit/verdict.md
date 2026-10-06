# EXP-022 verdict: uniform pressure ceiling confirmed; stronger input proposed

Declaration 4b1af0f5 and bounded admission 5c35f3d3 preceded exploration.
The exact-ceiling declaration f9aaf9cf preceded its arithmetic. The 6.34-
second one-process search completed all nine pressures. Its observed
minima are exploratory upper observations, never universal lower bounds.
Two setup failures before mathematical execution are preserved; the
isolated SciPy dependency installation left the shared venv and EXP-020
runtime unchanged. Ruff passes for the new source and both auditors.

Two rational gap configurations yield the exact pressure-family cap

    36988549868669912117331491083904339887470179336382577399511572430992757248
    /44169583944984760631542371660594662647325476621424736315194080095849609375
    = 0.8374212877970697... < 67/80 = 0.8375.

Every admissible finite-block distinct-strip bound using this fixed
packet window and pair weights is strictly below that exact cap, for
every nonnegative pressure. This bounds the counting assembly's output,
not the actual proportion of distinct zeros. The general proof and safe
enclosure direction are in proof.md and ceiling-declaration.md. The
independent auditor recomputes the selected energies with native Arb sinc
at 256 bits, independently of the verifier's derivative/series code;
Fraction arithmetic checks the rising/falling-line envelope and all signs.
The cap is conservative, not a sharp true family optimum or a novelty
claim for convex duality. Other windows, weights and analytic estimates
are outside its scope.

Changing pressure from 1/2500 to 1/1250 offers the proposed input
delta=52231/5000000. The exact admissible block m=562, tau=1203/500,
c=1703/500 would give

    2340938143167/2795532013000 = 0.8373855610599298...

after a complete new universal certificate and the attributed analytic
transfer. This is about 0.00021 above EXP-020's proposed transfer and
passes this declaration's 0.0001 value gate. A separately declared pilot
and full certificate are justified. No such new certificate is supplied
by this search or by EXP-020's partial cover at the old pressure.

RH-F12 closes as a supporting pressure audit. No standalone manuscript
or Zenodo deposit is triggered; the barrier may support a coherent
distinct-zero companion if a stronger lower theorem is subsequently
proved. The user's stopping condition is still unmet; research continues.
