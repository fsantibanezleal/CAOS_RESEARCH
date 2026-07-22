# EXP-036 - The annihilation lemma in closed form: sources live in the image

- **Question.** JCB-033, the single derived gap shared by Theorems 2, 3 and 4's tail steps.
  Prove the annihilation lemma in closed form instead of instance by instance.
- **Motivation (the derivation, declared).** The certificate covector Lambda is, by
  construction, left-null on the completion matrix M whose columns are exactly L(m) for the
  ansatz monomials m (L = J(P, .)): so Lambda annihilates the IMAGE of L. Every danger
  source has the form S = P_top^{k-1} J(P_top, m), and the Leibniz identity
  J(f, f^{k-1} g) = f^{k-1} J(f, g) (since J(f, f) = 0) rewrites it as
  S = L_top(P_top^{k-1} m): the source IS an image, with the EXPLICIT preimage
  w = P_top^{k-1} m. Hence Lambda(S) = 0 with no case analysis. Corollary: the truncation
  artifacts observed in EXP-031's first run are explained exactly: Lambda_N annihilates S
  precisely when the preimage w fits inside the window N; a window too small does not
  contain w, so the pairing is not forced to vanish. The lemma is therefore unconditional
  in the full polynomial ring, and Theorems 2-4's tail steps upgrade from [D] to [MV].
- **Falsifiable predictions.**
  1. [MV] (The Leibniz identity) J(f, f^{k-1} g) = f^{k-1} J(f, g) identically for generic
     symbolic f, g and k <= 4.
  2. [MV] (Explicit preimage) For P_top = a x^u y^v over a grid, and every danger monomial
     m with k <= 3: L_top(P_top^{k-1} m) equals the source P_top^{k-1} J(P_top, m) exactly.
  3. [MV] (The window criterion, and the artifact explained) For the (2,2) case:
     Lambda_N(S) = 0 for EVERY source whose preimage has degree <= N, and the sources whose
     pairing was nonzero in EXP-031's first run are exactly those whose preimage exceeded
     that window: the artifact is fully explained by the criterion.
  4. [MV] (Image membership, matrix form) rank([M | S]) = rank(M) for each source vector S
     within a window containing its preimage: the source lies in the column space.
  5. [D -> MV] (The upgrade) With 1-4 the annihilation step is closed in general: the tail
     statements of Theorems 2, 3, 4 become unconditional (no remaining derived gap in the
     perturbation machinery).
- **Method.** sympy over QQ and QQ(a): symbolic identities; explicit preimage construction;
  certificate covectors at several windows; ranks. Caps 570 s.
- **Success criterion.** 1-4 verified; 5 recorded as the upgrade with the proof in the
  verdict.
- **Failure criterion.** A source with no preimage in the ansatz span (the argument has a
  gap: state it), or a nonzero pairing with an in-window preimage (the covector is not
  left-null as believed: instrument error, fix first).

Declared 2026-07-22 before the run.
