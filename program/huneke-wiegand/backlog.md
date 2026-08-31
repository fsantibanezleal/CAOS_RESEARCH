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
| HWB-035 | 2 | in progress | interior graded Betti table of the conductor fiber cone | EXP-027--031 complete the second and third homological rows; EXP-033 completes the regularity-three/four strands; EXP-034 gives an exact rank-one class in the remaining row two, but both full lower strands remain open |
| HWB-036 | 1 | done | repository promotion and durable handoff for EXP-026 plus companion v0.02 | PRs #190/#191 passed required checks; payload tree `1fb094d102e1f91a6c9754cca26d7f57666450fb`; CAOS_MANAGE PR #559 promoted the ledger |
| HWB-037 | 1 | done | manuscript and Zenodo update for the first interior Betti strand | v0.14 published and fresh-download verified at `10.5281/zenodo.22013515` |
| HWB-038 | 1 | done | repository promotion and durable handoff for EXP-027 plus v0.14 | PRs #194/#195 passed required checks; tested payload tree `84910601b3a5b406c3725f64a0903d8116ad922f`; CAOS_MANAGE PR #562 promoted the verified publication ledger |
| HWB-039 | 1 | done | manuscript and Zenodo update for the complete second Betti row | v0.15 published and fresh-download verified at `10.5281/zenodo.22016550` |
| HWB-040 | 1 | done | repository promotion and durable handoff for EXP-028 plus v0.15 | PRs #198/#199 passed required checks; payload tree `e35f420f59a5343ea09da15985786ab0b65897d6`; CAOS_MANAGE PR #566 promoted the verified publication ledger |
| HWB-041 | 1 | done | manuscript and Zenodo update for the colon-Koszul degree-five diagonal | 36-page v0.16 passed all claim/build/render/authorship gates, published at DOI `10.5281/zenodo.22029468`, and matched a fresh public download exactly |
| HWB-042 | 1 | in progress | repository promotion and durable handoff for EXP-029 plus v0.16 | research PRs #203/#204 passed and all delivery trees match; scoped CAOS_MANAGE ledger remains deferred while that checkout is occupied by unrelated staged work |
| HWB-043 | 1 | done | cubic-colon idealization and degree-six third strand | EXP-030 proves the canonical idealization, exact multigraded support, and `beta_(3,6)=8p(7p^2-12p+2)/3` over every field |
| HWB-044 | 1 | done | manuscript and Zenodo update for the cubic-colon idealization theorem | 40-page v0.17 passed all claim/build/render/authorship gates, published at DOI `10.5281/zenodo.22030167`, and matched a fresh public download exactly |
| HWB-045 | 2 | done | final third-row entry and integral contraction | EXP-031 proves `beta_(3,7)=0` over every field by zero-vertex Morse matching and a signed unit filler block, completing the third homological row |
| HWB-046 | 1 | in progress | repository promotion and durable handoff for EXP-030 plus v0.17 | research PRs #205/#206 passed and all delivery trees match; scoped CAOS_MANAGE ledger remains deferred while that checkout is occupied by unrelated staged work |
| HWB-047 | 1 | done | manuscript and Zenodo update for the complete third row | 42-page v0.18 passed all claim/build/render/authorship gates, published at DOI `10.5281/zenodo.22030743`, and matched a fresh public download exactly |
| HWB-048 | 1 | in progress | repository promotion and durable handoff for EXP-031 plus v0.18 | research PRs #209/#210 passed and all delivery trees match; scoped CAOS_MANAGE ledger remains deferred while that checkout is occupied |
| HWB-049 | 1 | done | complete cubic-colon quotient graded Betti polynomial | EXP-032 proves every free-module rank and shift from Gorenstein self-duality, the h-vector `(1,2p-2,1)`, and the `8p`-variable Koszul factor over every field; differential matrices are not claimed |
| HWB-050 | 1 | done | manuscript and Zenodo update for the complete cubic-colon Betti polynomial | 43-page v0.19 passed every gate, was published at DOI `10.5281/zenodo.22031481`, became concept-latest, and matched a fresh public download exactly |
| HWB-051 | 1 | done | repository promotion and durable handoff for EXP-032 plus v0.19 | PRs #213/#214 passed required checks and promoted payload tree `c2f9f58488c7a1fa7ccee181a75944f7209b795c` through `develop` and `main`; CAOS_MANAGE remains untouched while occupied |
| HWB-052 | 1 | done | decide the complete cubic mapping cone and its comparison ranks | EXP-033 proves `depth(P_p/Q_p)=1`, `reg(P_p/Q_p)=2`, Tor-vanishing of every cubic comparison map, and complete regularity-three/four strands over every field |
| HWB-053 | 1 | done | manuscript and Zenodo update for the minimal-cone theorem | 45-page v0.20 passed all gates, was published at DOI `10.5281/zenodo.22062161`, became concept-latest, and matched a fresh public download exactly |
| HWB-054 | 1 | done | repository promotion and durable handoff for EXP-033 plus v0.20 | PRs #218/#219 passed required checks and promoted payload tree `f51cb2845d20b4fbf7d43029a71af0392bc3d6d9` through `develop` and `main` |
| HWB-055 | 1 | done | two-layer resolution of the EXP-033 kernel and first lower-strand survival test | EXP-034 proves `beta_(p,(p+2,8p-1+p(p+1)/2))=1` for `K_p`, `A_p`, and `C_p` over every field |
| HWB-056 | 1 | done | manuscript and Zenodo update for the first surviving lower-strand class | 48-page v0.21 passed all gates, was published at DOI `10.5281/zenodo.22135689`, became concept-latest, and matched a fresh public download exactly |
| HWB-057 | 1 | done | repository promotion and durable handoff for EXP-034 plus v0.21 | PRs #222/#223 passed required checks and promoted payload tree `f571fb955560c29489c181a6ce542548619209e0` through `develop` and `main` |
| HWB-058 | 1 | done | classify primitive zero-row incidence summands and test the next consecutive survival family | EXP-035 proves the all-parameter zero-row summand and consecutive `K_p` family; the coordinatewise P3 mechanism fails, while the full `p=4` target is characteristic-dependent |
| HWB-059 | 1 | done | manuscript and Zenodo update for zero-row and characteristic-dependence theorems | 51-page v0.22 passed all gates, was published at DOI `10.5281/zenodo.22177072`, became concept-latest, and matched a fresh public download exactly |
| HWB-060 | 1 | done | repository promotion and durable handoff for EXP-035 plus v0.22 | PRs #226/#227 passed required checks and promoted payload tree `0847e35a7641ab5592afd136f42bcf09ffe514f3` through `develop` and `main` |
| HWB-061 | 1 | in progress | all-parameter anatomy of the EXP-035 factor-two torsion | EXP-036 confirms repeated dependence and two mechanisms through `p=9`, refutes two finite fits, and proves family-wide cubic transfer; still require an infinite theorem for the parity-sensitive connecting quotient |
| HWB-062 | 1 | done | manuscript and Zenodo update for EXP-036 | 53-page v0.23 passed every gate, was published at DOI `10.5281/zenodo.22181972`, became concept-latest, and matched a fresh public download exactly |
| HWB-063 | 1 | done | repository promotion and durable handoff for EXP-036 plus v0.23 | PRs #230/#231 passed required checks and promoted payload tree `8ea3fbd0dfd136a7b91c508a31146be7d88eded1` through `develop` and `main` |
| HWB-064 | 1 | done | derive or refute a quasipolynomial law for the `t=2` connecting-parity defect | EXP-037 exactly refutes the candidate at the first new cell: `e_10=72`, not 73; independent order and `GF(5)` audits pass |
| HWB-065 | 1 | in progress | test whether the first discrepancy is a degree-six relation in the parity-defect module | audited exact `e_11=102` passes; conditional `e_12=138` test is active, while an explicit relation/recurrence proof remains mandatory |
| HWB-066 | 1 | done | decompose the parity-sensitive combined core into recurring signed components | EXP-039 refutes bounded defect-one blocks but exposes exact latent sectors `binom(p-2,3),p-4,p-4,p-5` and their `p=9` support merger |
| HWB-067 | 1 | in progress | localize the first degree-six correction inside the merged signed sector | EXP-040 predicts component partitions `67+5` at `p=10` and conditionally `96+6` at `p=11`, then seeks explicit signed bridge columns |
