# EXP-056: uniform low-source formula

[proof.md](proof.md) proves `M_p s_p=b_p^A+b_p^B+gamma_p` for every `p>=8` by collecting
all signed faces. Both `s_p` and `gamma_p` have `p-1` terms. [verdict.md](verdict.md) separates
this uniform identity from the open torsion question.

From the repository root:

```powershell
.venv/Scripts/python.exe problems/commutative-algebra/huneke-wiegand/experiments/EXP-056-uniform-low-source/run.py
```

The runner compares two independent boundary implementations, the frozen EXP-052 formula,
saved training sources, and sign-corruption controls. Use `--output` for a temporary rerun;
`--maximum` must lie in `8..100`. Compact artifacts contain all parameter hashes and checks.
