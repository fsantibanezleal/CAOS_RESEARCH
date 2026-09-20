# EXP-007 artifact index

The canonical evidence is generated into `canonical/`:

- `result.json`: exact spectral and multiplicity censuses, directed rational
  certificate, sensitivity control, pinned source hashes, and independent
  100-digit interval replay;
- `execution-receipt.json`: clean commit, runtime, budget, and result hash;
- `checkpoint.json`: terminal stage marker; and
- `stdout.txt`: flushed stage log.

`failed-attempt-001/` preserves the first canonical attempt. Its exact
certificate passed, but the audit demanded that a 110-digit rational interval
contain a separately rounded 100-digit interval. Three intervals overlapped
without containment at about the last replay digit. The corrected gate checks
nonempty overlap between two independently computed enclosures.

`failed-attempt-002/` preserves the next attempt. It exposed that the historical
EXP-003 pressure parameters at `theta=3/4` lower the coupled-product root even
though their pressure-only bound is much stronger. The declaration made that
case diagnostic, so the corrected gate classifies and records its sign instead
of assuming it is positive.

The final run passed from clean commit
`d63111ffa8a348c51eb4fd06f5a1e70a51211576`. Machine artifacts certify exact
finite arithmetic and numerical enclosures. The universal theorem depends on
`mathematical-proof.md` and `adversarial-audit.md`.

`windows-canonical-v1/` preserves the exact CRLF result bytes cited by
manuscript v0.07. The current canonical run uses fixed LF serialization so its
receipt hash is identical to the immutable Git blob on every platform.
