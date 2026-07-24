# EXP-083 - Verdict: the [125,150] frontier partitioned; only 2 configs are printed-open

**Status: DECIDED (audit). The 24 configs partition into 1 excluded / 5 verify /
2 open / 16 derivation-needed.**

## The partition (artifacts/output-2026-07-24.txt)

- **EXCLUDED, sourced (1):** C13 (GGV2 remark tex ~1053: B0=(8,28),B1=(8,40) ->
  A0'=(8,4) impossible; EXP-082).
- **VERIFY, source reconciliation (5):** C10, C11 (A0=(7,21): GGV2 remark says
  the (7,21) families come from A0'=(2,1) IMPOSSIBLE, but our GGV5-sourced table
  prints A0'=(1,0); the two A0' notions must be reconciled - if GGV2's holds,
  C10/C11 are ALSO excluded); C19, C20 (A0=(6,15): GGV2 excludes B1=(6,18+6k)
  with 18+6k not a multiple of 30 -> (6,3); check C19/C20's B1); C12 (A0=(8,28)
  with A1=(7/4,3), a DIFFERENT chain from C13's; the (8,28) is named but the
  B0/B1 pattern differs - derive).
- **OPEN, printed A0' not excluded (2):** C01 (A0'=(1,0)), C04 (A0'=(2,0)):
  (t,0) is always a possible last lower corner, so these are NOT excluded by
  casos-imposibles and are genuine open family cases (F2 j=1, F24 j=0).
- **DERIVATION-NEEDED (16):** the sporadic configs with UNPRINTED A0'
  (C02,C03,C05-C09,C14-C18,C21-C24): force A0' via the EXP-077 method (GGV1
  Thm 7.6 en-point/q1 + shared-bottom-vertex d0) then test excluded-family
  membership. Several may collapse to excluded (like C13 did).

## Reading

The frontier is MUCH smaller than the naive 24: at most 2 configs (C01, C04)
are confirmed genuine open family cases; 5 need only a source reconciliation
that likely excludes 4-5 of them; 16 need the forcing derivation (cheap per
config, the EXP-077 machine method). This RE-SCOPES the [125,150] program from
'attack 24 unknowns' to 'reconcile 5 + derive 16 A0' forcings, then attack the
few genuine survivors'. The GGV2 remark alone likely clears 5-6 configs we had
treated as open.

## Next (declared)
- EXP-084: reconcile the GGV5-vs-GGV2 A0' notions for C10/C11/C19/C20 (source
  read of GGV5 section 5 family tables vs GGV2's forced last-lower-corner).
- EXP-085: batch the 16 A0' forcings via the EXP-077 method.
