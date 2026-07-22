# EXP-031 - The kernel repair: absorption and the annihilation lemma

- **Question.** EXP-030 refuted the injectivity step (L_top has kernels on classes kv,
  visibly spanned by P_top^k) while every empirical prediction held. Repair the proof: (a)
  identify the kernels exactly; (b) test the ANNIHILATION LEMMA: the chain functional kills
  the weight-0 sources J(m, P_top^k) that danger-weight tails inject; (c) certify the danger
  tails directly over QQ(a, b).
- **Motivation.** Kernel absorption: any Q splits as H(P_top) + Q'' (kernel components are
  exactly the H-parts). Then J(P, Q) = J(R, H(P_top)) + J(P, Q''), and the y-class equation
  acquires the source 1 - [J(R, H(P_top))]_{wt 0}. A tail monomial m of weight
  lam = v + 1 - u - kv (the DANGER weights: lam = -1, -3, -5, ... at u = v = 2) feeds that
  source through P_top^k. THEOREM 2 stands iff the obstruction functional annihilates every
  such source. EXP-030's parts C/D/E used mostly safe tails; the danger tails are the
  decisive missing test (though C's (0,3) and (2,5) tails ARE danger cases and still came
  out empty: encouraging, not yet certified).
- **Falsifiable predictions.**
  1. [MV] (Kernel identification) On classes kv (grid (u, v), k <= 3): the kernel of L_top
     is EXACTLY 1-dimensional and its vector matches the monomial coefficients of P_top^k.
  2. [MV] (Annihilation) For u = v = 2 and danger monomials m in {x y^3, x^2 y^5} (k = 1)
     and {y^3, x y^5} (k = 2), and k <= 3 powers: the weight-0 ray component of
     J(m, P_top^k) pairs to ZERO with the pure chain functional at every window tried.
  3. [MV] (Danger certificates) Certificates over QQ(a, b) for P = x + a (xy)^2 + b m with
     m in {x y^3, y^3} at windows <= 10, and the combined tail b x y^3 + c y^3 over
     QQ(a, b, c) at window <= 10: the pairing gcd is a PURE a-power (b, c-free).
  4. [D] (Theorem 2, repaired proof) With 1-3: absorption + annihilation + EXP-030 A
     (coupling) + the pure chain (EXP-029) assemble the proof of: P = x + a x^u y^v + R
     (u >= 2, v >= 1, a != 0, R any polynomial of strictly lower w-weight monomials, degree
     >= 2) is never a Keller component. Machine-shadowed at the tested grids; the general
     annihilation is recorded [D] with its verified instances (not claimed as fully proved
     until derived in closed form).
- **Method.** sympy over QQ(a), QQ(a, b), QQ(a, b, c); the certificate instrument; direct
  functional pairing on the e-ray rows. Caps 570 s.
- **Success criterion.** 1-3 verified; 4 recorded with honest labels.
- **Failure criterion.** A nonzero annihilation pairing or a b-dependent gcd: then the
  danger locus {gcd = 0} is a candidate completion stratum: probe with the checker
  immediately (that would be the discovery branch, not a failure of the record).

Declared 2026-07-22 before the run.
