# EXP-057 hypothesis: four-row kernel representative

Declared: 2026-09-04, before computation. Exact integers, CPU only.

## Proposed uniform reduction

EXP-056 defines the explicit chain `gamma_p` with `p-1` K rows. Write

`G_p(a,j;c)=[K,(L_p minus {a,3p,3p+j}) union {6p};10p+c]`.

Let `q_p=[K,(L_p minus {3p,3p+2}) union {6p};10p]`. Its proposed boundary is

$$M_pq_p=\sum_{a=1}^{p-2}(-1)^{a-1}G_p(a,2;a).$$

Consequently, the proposed representative is

$$\eta_p=\gamma_p+M_pq_p=(-1)^p\bigl(
2G_p(p-3,2;p-3)-G_p(p-2,2;p-2)
+2G_p(p-2,1;p-3)-2G_p(p-3,1;p-4)\bigr).$$

- P1: these exact identities hold for every `p>=8`, by a complete symbolic face argument.
- P2: independent multiplication verifies the identities at `p=8,...,100`; the support of
  `eta_p` is exactly four, with a single odd-coefficient row.
- P3: `M_p(s_p-q_p)=b_A+b_B+eta_p`; corrupted coefficients fail the check.

## Premise, source, and invariant preflight

EXP-056 owns `M s=b_A+b_B+gamma` and its complete family-by-family derivation. EXP-036/037
define all offsets and signs. The new invariant is direct cancellation of the long interval
against one K column, before any rank or Smith calculation. The complete primary source pass
and Koszul/Morse limits are recorded in EXP-054--056; no imported theorem supplies this identity.

PASS proves an integral cokernel equivalence to a four-row endpoint representative and a
one-row mod-two representative. It does not prove nonzero class, order two for every parameter,
an injective transfer from the projected relative quotients, or an upper bound. FAIL refutes
the proposed cancellation without weakening EXP-056.

## Budget and scope

One CPU process, 60 seconds, 1 GiB private memory; expected runtime below ten seconds. Flush
and checkpoint each parameter. Stop on exact disagreement, premise mismatch, or budget exhaustion.
No HNF, full-basis enumeration, or original `p=11` source reconstruction. Persist compact
deterministic hashes and counts; test writes go to temporary paths.

The exploration outcome would be a bounded endpoint target for a generic dual obstruction.
It is not the complete quotient normal form or a manuscript trigger by itself.
