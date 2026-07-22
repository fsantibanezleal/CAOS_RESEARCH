# EXP-051 - THE HALF-PLANE TOWER LEMMA (route N1, closing the last gap)

- **Question.** Derive the general half-plane construction (EXP-048's mechanism) and
  apply it: all-degree exclusions for proper-power-top shapes, including the frontier
  samples.
- **Motivation (the declared derivation).** Let mu = min{p - q : (p, q) in supp(P)} be
  attained by the total-degree top form T (true for the swallowed-staircase geometry:
  the top corner is the y-most support point). Take H = {rows (i, j) : i <= j} (the
  y-heavy half-plane; it contains the constant row). In the H-restricted window system
  M_H (H-rows, all columns), the tower extension has NO unresolvable cases: (a) T-power
  resonances reduce in-window via T^k = (P - lower)^k (Theorem 6's universal reduction),
  and Lambda_H kills H-parts of in-window images by definition; (b) g^s resonances
  (e not dividing s) have x-heavy sources whose H-part is EMPTY: killed trivially;
  (c) a new column whose T-output falls outside H has ALL outputs outside H (T attains
  the minimal i - j, so its output minimizes i - j among the column's outputs): the
  column is zero in M_H and imposes nothing. HENCE: if M_H has a left-null covector
  with nonzero pairing at ONE window N >= deg P - 1, then P is not a Keller component
  at ANY partner degree. This subsumes Theorem 6 (whose scope needed non-proper-power
  tops) on the mu-attaining-top stratum and closes Theorem 5's proper-power case.
- **Falsifiable predictions.**
  1. [MV] (H-certificates exist, symbolically) At (2,2,2), the H-subsystem has a
     cleared certificate with monomial pairing at every window N = 7..10 over QQ(a,b).
  2. [MV] (Case-c vacuity) On samples, every new column whose T-output lies outside H
     has zero H-part entirely.
  3. [MV] (Frontier application, the payoff) The proper-power-top frontier samples
     P32 = x + R0(1)^2 + x^2 (T = x^8 y^24 attains mu = -16) and a degree-72
     corner-(16,56) sample have H-certificates at one window each: by the lemma, they
     are excluded at ALL partner degrees: the first all-degree exclusions on
     B = 16-flavor frontier shapes.
  4. [D] (The lemma) With 1-3 and the derivation, the HALF-PLANE TOWER LEMMA stands
     [MV/D]; Theorem 5's proper-power case closes; the tower now covers every
     swallowed-staircase shape whose top corner is its y-most support point.
- **Method.** sympy over QQ and QQ(a,b); H-restricted systems; cleared covectors with
  identity verification; caps 570 s per part (windows degrade before capping; recorded).
- **Success criterion.** 1-3 verified; 4 stated with exact scope.
- **Failure criterion.** No H-certificate on a shape whose full window is inconsistent
  (the half-plane carries less than the mechanism claims: scope narrows, recorded); a
  case-c violation (the threshold argument is wrong).

Declared 2026-07-22 before the run.
