# EXP-034 preflight - two-layer kernel and lower Betti strands

Date: 2026-08-27

## Scope

The unresolved object after EXP-033 is the regularity-two quotient

```text
A_p=P_p/Q_p
```

in the exact sequence

```text
0 -> K_p -> A_p -> D_p -> 0,
D_p=P_p/(Q_p:f_p).
```

EXP-032 determines the complete ordinary graded Betti polynomial of `D_p`, and EXP-033 proves
that `K_p` is one-dimensional Cohen--Macaulay with Hilbert series
`(8p z+10p z^2)/(1-z)`. The two lower strands of `A_p`, and therefore the remaining two strands
of `C_p`, are still open. This round does not claim to settle the Huneke--Wiegand conjecture; the
underlying family already consists of counterexamples, and the target is their unresolved
homological structure.

## Reconciled internal evidence

- EXP-030 proof SHA-256:
  `1822095a7d16207b7d04261b7a6645f7ca51b01f490ba9d212a84ab7ca5bc729`.
- EXP-032 proof SHA-256:
  `4dc37605c012b7f6a70ec5d383897c45a34e1dd5d5e4bb32a0582b7a6d651d1c`.
- EXP-033 proof SHA-256:
  `e27cd386ad47da7ad5282e88a095d82f2b1156f76546e934b287e911da2c7b1c`.
- EXP-033 verdict SHA-256:
  `674b2940259465f0a2cba96261a8bb021e103cb3e51db50a8aac4f64c0c5927b`.

The source objects, object names, shifts, and remaining boundary agree across `RESUME.md`,
`state.md`, `plan.md`, `backlog.md`, the experiment registry, and EXP-033. The active work is not
a stale Jacobian-conjecture route and does not touch CAOS_MANAGE.

## External method sweep

The following primary sources were checked for a reusable vanishing or splitting criterion:

1. Francisco, Ha, and Van Tuyl, *Splittings of monomial ideals*, arXiv:0807.2185.
2. Bolognini, *Betti splitting via componentwise linear ideals*, arXiv:1410.6511.
3. Jayanthan, Sivakumar, and Van Tuyl, *Partial Betti splittings of ideals*, arXiv:2412.04195.
4. Eisenbud and Schreyer, *Betti numbers of graded modules and cohomology of vector bundles*,
   arXiv:math/0611081.

Partial Betti splitting gives a useful language for regional Tor-map vanishing, but no cited
result directly decides the family-specific extension `0 -> K_p -> A_p -> D_p -> 0`. The exact
offset incidence of `K_p` is stronger information than its Hilbert series, so EXP-034 prioritizes
that incidence complex before cone inequalities or a raw resolution.

## Redirection decision

The strongest route is to kill the EXP-033 regular element `X_0` and resolve the resulting
two-layer finite-length module. This converts all differentials into explicit signed incidence
maps between offset-labelled exterior powers. A maximal-rank heuristic is retained only as a
control: the first objective is to search for cells with no possible incoming face, because one
such cell gives a characteristic-free integral homology class.

The stronger survival question is multigraded. An explicit class in `Tor(K_p,k)` contributes to
`Tor(A_p,k)` only if it is not hit by the connecting map from `Tor(D_p,k)`. EXP-034 must therefore
compute or exclude the source in the same `(standard degree, offset)`; ordinary Betti counts are
not enough.

## Guardrails

- Declare before implementing or running any EXP-034 campaign.
- Work only on `work/huneke-wiegand/open` in CAOS_RESEARCH.
- Freeze and recheck every premise hash before each canonical run.
- Use exact integer or finite-field arithmetic, deterministic ordering, independent
  reconstruction, and corrupted controls.
- Distinguish a theorem about `K_p` from a theorem about `A_p`; survival through the long exact
  Tor sequence requires separate evidence.
- Treat finite campaigns as implementation validation, never as the all-parameter proof.
- Update the existing manuscript only if a proved class changes the published Betti boundary;
  consider a separate manuscript only for a transferable two-layer-resolution theorem.

