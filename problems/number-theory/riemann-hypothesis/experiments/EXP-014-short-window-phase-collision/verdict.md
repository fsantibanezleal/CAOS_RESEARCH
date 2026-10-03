# EXP-014 verdict: confirmed generic phase obstruction

Date: 2026-10-03. Declaration `8db97480` preceded implementation.
**Confirmed**: predictions A-C hold for the exact frozen cases and the
uniform family. The [proof](proof.md) supplies the quantifiers; nine examples
alone would not establish an asymptotic statement.

For T=16 B^(2a), M=B^b, r=B^(a-b), h=M, k=M-1,
m=kr+1 and n=hr+1, we have hm-kn=1 and mn<T/8.
The exact log enclosure is H/(kn+1)<=H log(hm/kn)<=H/(kn),
with scale B^(d-a-b) and multiplicative factor tending to one.
For (a,d)=(50,54), b=5,4,3 gives respectively phase tending to
zero, one, infinity. Thus nu=theta-1/2 is the uniform pointwise
resolution threshold. The derivative scale H/log T is smaller still.

The independent auditor expands the Bezout identity and verifies both
logarithm inequalities by their derivatives. Swapped twists reverse the
signed phase; diagonal and altered-limit controls are rejected by tests.
Canonical replay and proof/code/declaration bindings are checked.
Canonical SHA-256: `fb0f0d4a0d165d524a86285c8bae163297959aa9819a5181e1a89b46e3567c2f`.
Report: [artifacts/audit/audit.json](artifacts/audit/audit.json).

The power twists may have zero Mobius weights. This result controls the
generic twisted lemma only; EXP-015 addresses that caveat separately.
Neither experiment proves a nonzero total off-diagonal contribution.
Research-record: standard phase-resolution obstruction, no new onset,
moment-asymptotic refutation, manuscript or RH conclusion.
