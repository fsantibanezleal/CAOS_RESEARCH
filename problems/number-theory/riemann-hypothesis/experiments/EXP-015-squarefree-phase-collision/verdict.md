# EXP-015 verdict: confirmed support-aware phase obstruction

Date: 2026-10-03. Declaration `12fa7d70` was pushed before implementation.
**Confirmed**: predictions A-C hold. This follow-up resolves the
zero-Mobius-weight caveat of EXP-014 without strengthening its claim about
the signed sum.

## Uniform statement

For every M>=1000000, the interval [ceil(M/2),floor(3M/4)] contains
a pair h,k=h-1 that are both squarefree. An elementary union bound for
prime squares gives a positive count uniformly; it assumes neither
twin primes nor an asymptotic sieve theorem. The rational tail bound is
S=2535919/5336100<12/25. The uniform lower bound used at M=1000000
is 199999/25>0.

For any such pair and r>=2, m=kr+1,n=hr+1 give hm-kn=1,
mn<T/8, T=16(Mr)^2. Both Mobius coefficients and both basic P(x)=x
mollifier coefficients are nonzero. The phase is between
H/(2M^2 r) and 5H/(M^2 r). Hence the same exponent threshold
nu=theta-1/2 holds uniformly on supported twists. See [proof](proof.md).

The finite sieve selects h=500006,k=500005 at M=1000000.
At r=1000000, H=10^16,10^18,10^20 have directed phase enclosures
near 0.0399991,3.99991,399.991. These are controls, not the existence proof.

## Validation and scope

The producer marks square divisors by an exact sieve; the auditor uses
trial square division without importing it. Both expand the identities
and use exact rational bounds. Tests reject squareful changes, diagonal
changes, unsupported coefficient assertions, altered prime tails and
the overstrong comparison constant 1/3 (the valid bound is 1/5).
The 20 focused tests, including all three byte-replay/binding controls,
pass. Canonical SHA-256: `871de5a7719bec0a077e1bda88729000d3988e20cee2940f3ef3dd6d55aa3ef8`.
Report: [artifacts/audit/audit.json](artifacts/audit/audit.json).

Research-record: an elementary support-aware strengthening of a proof
mechanism obstruction. No claim that the signed sum cannot cancel, that
the moment formula is false, or that RH or a new onset follows. This
supporting lemma is routed with the short-interval-Levinson research
record; no independent paper or Zenodo deposit is justified.
