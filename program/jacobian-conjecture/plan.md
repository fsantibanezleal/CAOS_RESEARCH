# Jacobian conjecture - problem plan

Opened 2026-07-20. Area: algebraic-geometry. State: exploring.
Context dossiers: `problems/algebraic-geometry/jacobian-conjecture/context/`.

## Goal

Understand WHY the Jacobian conjecture is false for N >= 3 (Alpöge/Fable counterexample,
2026-07-19), own the generalization (families of counterexamples, invariants, minimality), and
push what transfers to the still-open N = 2 case. Honest deliverables: exactly verified results,
reproducible experiments, sharpened conjectures, and null results where the mathematics says no.

## Phases

| Phase | Content | State |
|---|---|---|
| JC-P0 Foundation | EXP-001 exact validation of the counterexample; context transcription; reference library. | done 2026-07-20 (EXP-001 confirmed) |
| JC-P1 Structure and generalization | Reverse-engineer the map's structure ourselves, exactly: scaling symmetry, z-linearity, invariant-space reduction, fiber identity; then build and verify a GENERAL seed-family constructor (Keller property, fiber degrees, new instances beyond the announced one). | active |
| JC-P2 Geometry of the failure | Exact asymptotic variety (non-properness locus); sheet structure at infinity; real-slice topology; web viz artifacts (GPU sampling). | pending |
| JC-P3 Minimality | Is fiber degree 3 / degree vector (7, 6, 4) minimal? Weighted-ansatz enumeration with symbolic pruning; GPU coefficient search on surviving boxes. | pending |
| JC-P4 Cascade | Push through Bass-Connell-Wright / Druzkowski to explicit cubic forms; verify the consequence chain (Mathieu SU(3), Gaussian moments, Zhao vanishing, Image) from primary sources. | pending |
| JC-P5 The 2D frontier | Formalize the N >= 3 obstruction (weight-vector argument); 2-variable transplant attempts; small-degree 2D Keller searches; properness/asymptotic-variety experiments; deep-research pass on JC(2) primary literature. | active (in parallel with P1, per Felipe's 2026-07-20 directive to focus on generalization + 2D) |
| JC-P6 Consolidate + publish | Wiki, SVGs, web page, manuscript chapter, diffusion. | rolling (manuscript updated per phase) |

## Strategy notes

- The structural claims in circulation (weighted-lift family, seed polynomials, non-properness
  mechanism) come from a secondary web analysis; JC-P1 does NOT cite it as ground truth, it
  re-derives everything independently and exactly. Where our derivation disagrees, ours (with its
  persisted certificate) wins the record.
- If the known hypotheses run dry, the mandate (Felipe, 2026-07-20) is to explore novel
  approaches and keep experimenting: candidate novel directions are kept in
  `program/jacobian-conjecture/backlog.md` and promoted to experiments as slots open.
