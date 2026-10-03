# EXP-024: exact Gaussian reduction with an all-order phase remainder

Declared 2026-10-03 before numerical controls. This is a bounded step within
RH-F4 / issue #360, following EXP-021's complete composite arithmetic layer.
It is not a new research focus, a new moment asymptotic or a zero proportion.

For H>0, T real, h,k positive integers and |Re alpha|, |Re beta|<1/4,
derive an exact absolutely convergent dual series for the whole-real-line
Gaussian-weighted shifted twisted second moment. Retain the residue at
s=1-alpha, all gamma factors and the full cosine phase. Prove the Mellin
transform by Abel regularization and analytic continuation rather than an
unjustified interchange of an infinite oscillatory integral.

Then expand only the nonlinear part of exp(2y/H) inside the exact Gaussian
kernel. For every fixed J>=1 obtain a finite Gaussian/Hermite expression
and an explicit remainder O_J(x^(-Re beta)*(x/H^2)^J), with every constant
shown. On x comparable to T, H=T^theta, theta>1/2, this decreases to every
fixed polynomial order as J grows. It does not provide signed cancellation
after summing the dual arithmetic series. No global error upgrade follows
until the large/small-x tails and full mollifier average are controlled.

Source preflight: Tang 2608.14852 and Bettin 1607.05595 supply related
reciprocity mechanisms; the dossier already retains their hypotheses and
prime/composite limitations. Dutta-Ghoshal-Rajkumar 2408.04247v1 is newly
archived through its PDF/HTML, with its cosine-Mellin proof and closing
kernel/RMT discussion read. Its distributional kernel analogy supplies
no zero-location theorem. Functional equations, Gaussian integration,
Mellin inversion and Taylor remainder mechanisms are classical; no
priority claim is made for them or this representation.

P5: the key scale is x/H^2 after exact transformation, distinct from the
pointwise original gamma-phase scale H^3/T^2 excluded in EXP-014/015.
There is no contradiction: the object and order of integration differ.
The premise dependencies are the classical zeta functional equation,
polynomial vertical-strip growth and exact Gaussian transform. EXP-021
supplies the later composite-character decomposition, not a moment estimate.

PASS requires a complete analytic derivation including residues and
convergence, independent symbolic Hermite controls, and agreement of
separately enclosed Gaussian and Mellin integrals with explicit real-axis
tails. Finite agreement alone cannot prove the identity or uniform bound.
FAIL means an actual sign/normalization/remainder discrepancy; retain it
before correction. Ten minutes CPU controls, one worker, progress per
case; a budget hit retains incomplete controls. No heavy arithmetic sweep.

This supporting result stays in the research record and later belongs to
short-interval-levinson only if a coherent new signed moment theorem is
proved. It does not trigger a standalone manuscript or fulfill the user's
requested stopping condition. EXP-020 and EXP-023 continue independently.
