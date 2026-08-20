# Huneke-Wiegand extensions - backlog

| id | priority | status | item | gate |
|---|---:|---|---|---|
| HWB-001 | 0 | done | EXP-001 independent Singular/4ti2 reproduction | P1-P6 confirmed; failed toolchain attempts preserved |
| HWB-002 | 0 | done | exact `End_R(I)` value semigroup and Gorenstein test | P1-P6 plus exact Dey--Lyle dependency map confirmed |
| HWB-003 | 1 | done | SAT model calibration at `(181,14)` | P1-P6, extracted model and all controls independently checked |
| HWB-004 | 1 | done | reproduce published `F<69` frontier | EXP-004: 48,954 trees, 1,503,391 gaps, 1,156 accepted DRAT proofs |
| HWB-005 | 1 | done | extend minimal Frobenius frontier | EXP-005 proves least Frobenius 181 with 56 checked lower proofs and exact model |
| HWB-006 | 1 | done | additive-basis/Kunz block family search | EXP-006 Route K opens extraction; EXP-009 proves an infinite family for every `p>=4` |
| HWB-007 | 2 | in progress | surviving-variants matrix | EXP-011 closes the endomorphism/reflexivity row; other positive hypotheses remain to test |
| HWB-008 | 2 | pending | formal certificate/proof packaging | small trusted checker; assess Lean only after theorem stabilizes |
| HWB-009 | 0 | done | manuscript and Zenodo | v0.08 published and verified at `10.5281/zenodo.21908490`; all earlier versions remain frozen |
| HWB-010 | 1 | done | classify rigid pairs at `F=181` | EXP-007: unique normalized pair, support/fixed terminal proofs and fresh audit pass |
| HWB-011 | 2 | in progress | classify the EXP-009 family and nearby Kunz faces | EXP-011 closes uniform endomorphism anatomy; broader Kunz-face classification remains open |
| HWB-012 | 1 | done | uniform endomorphism overring of the EXP-009 family | EXP-011 proves the exact formula, invariants, nonsymmetry, and Ext/Tor escape |
| HWB-013 | 1 | done | pseudo-Frobenius set and reduced type of the endomorphism family | EXP-012 proves the exact `10p` type, maximal reduced type, and non-almost-Gorenstein boundary |
| HWB-014 | 1 | done | exact trace/conductor ideal across the explicit family | EXP-013 proves the common conductor formula and balanced defects `length(R/T)=length(E/R)=p+1` after preserving one smoke correction |
| HWB-015 | 1 | done | conductor stability and exact first defect | EXP-014 proves nonstability; EXP-015 preserves a refuted tail; EXP-016 proves `length(T^2/t^(4s)T)=14p` |
| HWB-016 | 1 | done | conductor reduction sequence and Hilbert data | EXP-017 proves reduction number four, quotient lengths `23p-1,14p,2p,1,0`, and `(e0,e1)=(24p,39p)` |
| HWB-017 | 1 | done | conductor tangent cone | EXP-018 proves depth zero, a unique Valabrega--Valla defect of length `p`, and the exact positive Hilbert numerator |
| HWB-018 | 1 | done | torsion/Buchsbaum anatomy of the tangent cone | EXP-019 proves `H^0=k^p` in degree zero, full maximal-ideal annihilation, Buchsbaumness, and invariant `p` |
| HWB-019 | 1 | done | manuscript and Zenodo update for Buchsbaum theorem | v0.09 published and fresh-download verified at `10.5281/zenodo.21908785` |
| HWB-020 | 1 | done | exact Noether-normalization module and graded Betti data | EXP-020 proves the complete cyclic decomposition, minimal resolution, regularity four, and section identity `25p=e0+I` |
| HWB-021 | 1 | done | manuscript and Zenodo update for module theorem | v0.10 published and fresh-download verified at `10.5281/zenodo.21909127` |
| HWB-022 | 1 | done | conductor fiber cone and canonical Cohen--Macaulayization | EXP-021 proves the exact square, natural quotient, type `10p+1`, and nonlevel behavior |
| HWB-023 | 2 | done | defining ideal of the conductor fiber cone | EXP-023 proves the full presentation by `50p^2-17p` quadrics plus the single cubic `X_0^2X_(3p)-X_p^3`; relation type three and non-Koszulness follow |
| HWB-024 | 1 | done | manuscript and Zenodo update for the fiber-cone theorem | v0.11 published and fresh-download verified at `10.5281/zenodo.21909961` |
| HWB-025 | 1 | done | manuscript and Zenodo update for the defining-ideal theorem | v0.12 published and fresh-download verified at `10.5281/zenodo.21988601` |
| HWB-026 | 1 | done | repository promotion and immutable handoff for EXP-022/023 plus v0.12 | PRs #176/#177 passed required checks; remote `develop`/`main` share tree `5469624bab95a087aaef37630ea9c2a27c656054` |
| HWB-027 | 1 | done | extremal presentation-ring Betti data | EXP-024 proves exact projective dimension, regularity, first linear syzygies, last row, penultimate edge, and canonical degrees |
| HWB-028 | 1 | done | manuscript and Zenodo update for homological edge theorem | v0.13 published and fresh-download verified at `10.5281/zenodo.21995498` |
| HWB-029 | 2 | done | explicit quadratic or Groebner basis | EXP-026 proves the complete reduced grevlex basis and flat monomial degeneration |
| HWB-030 | 1 | done | repository promotion and immutable handoff for EXP-024 plus v0.13 | PRs #182--#185 passed required checks; final remote handoff tree is `b70a3990583057a92e591c34d5f9e9c101185e8c` |
| HWB-031 | 1 | done | curvilinear parametrization and primary decomposition of the conductor fiber cone | EXP-025 proves the truncated model, exact radical, primaryness, sharp nilpotence, curvilinear geometry, and differential fingerprint |
| HWB-032 | 1 | done | companion manuscript and Zenodo record for the curvilinear theorem | v0.01 published and fresh-download verified at `10.5281/zenodo.21997378` |
| HWB-033 | 1 | done | repository promotion and durable handoff for EXP-025 publication round | PRs #186/#187 passed required checks; tested payload tree `53e5e61ffeeb5816497e3e477921bc94c4a5f91d`; CAOS_MANAGE PR #557 promoted the ledger |
| HWB-034 | 1 | done | manuscript and Zenodo update for the explicit Groebner theorem | v0.02 published and fresh-download verified at `10.5281/zenodo.22002907` |
| HWB-035 | 2 | in progress | interior graded Betti table of the conductor fiber cone | EXP-027/028 complete the entire second row; EXP-029 confirms the colon-Koszul degree-five diagonal; `beta_(3,6)` and the remaining interior table stay open |
| HWB-036 | 1 | done | repository promotion and durable handoff for EXP-026 plus companion v0.02 | PRs #190/#191 passed required checks; payload tree `1fb094d102e1f91a6c9754cca26d7f57666450fb`; CAOS_MANAGE PR #559 promoted the ledger |
| HWB-037 | 1 | done | manuscript and Zenodo update for the first interior Betti strand | v0.14 published and fresh-download verified at `10.5281/zenodo.22013515` |
| HWB-038 | 1 | done | repository promotion and durable handoff for EXP-027 plus v0.14 | PRs #194/#195 passed required checks; tested payload tree `84910601b3a5b406c3725f64a0903d8116ad922f`; CAOS_MANAGE PR #562 promoted the verified publication ledger |
| HWB-039 | 1 | done | manuscript and Zenodo update for the complete second Betti row | v0.15 published and fresh-download verified at `10.5281/zenodo.22016550` |
| HWB-040 | 1 | done | repository promotion and durable handoff for EXP-028 plus v0.15 | PRs #198/#199 passed required checks; payload tree `e35f420f59a5343ea09da15985786ab0b65897d6`; CAOS_MANAGE PR #566 promoted the verified publication ledger |
| HWB-041 | 1 | in progress | manuscript and Zenodo update for the colon-Koszul degree-five diagonal | EXP-029 crosses the existing-manuscript trigger; expand to v0.16, render every page, publish a new concept version, and verify a fresh public download |
| HWB-042 | 1 | pending | repository promotion and durable handoff for EXP-029 plus v0.16 | promote the tested research payload through work-to-`develop` and `develop`-to-`main` PRs, then promote the scoped management ledger |
