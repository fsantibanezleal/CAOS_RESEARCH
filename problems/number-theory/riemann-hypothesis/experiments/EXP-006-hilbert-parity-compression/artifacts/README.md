# EXP-006 artifact index

The current canonical evidence is generated into `canonical/`:

- `result.json`: exact finite census, directed interval certificate, scalar
  barrier witness, source hashes, and independent interval replay;
- `execution-receipt.json`: clean commit, runtime, budget, and result hash;
- `checkpoint.json`: terminal stage marker; and
- `stdout.txt`: flushed stage log.

`superseded-broad-bracket/` preserves the first passed run. It used the broad
declared root bracket `0.5458<theta<0.5459`. The canonical run uses the tighter
certified bracket `0.545884<theta<0.545885`. No formula, source constant, or
target point changed.

`superseded-weaker-transfer/` preserves the tight-bracket run completed before
the consistency audit recovered the simple-real term in Lamzouri's Hilbert
bound. That run certified `Q(N-O)>=2(N-S)^2`. The amended runner certifies the
strictly stronger `(Q-S)(N-O)>=2(N-S)^2` and a correspondingly larger simple
zero lower bound. The frozen target exponent, analytic inputs, and threshold
equation did not change.

The machine artifacts certify finite arithmetic and exact inequalities. The
universal result depends on `mathematical-proof.md` and `adversarial-audit.md`.
