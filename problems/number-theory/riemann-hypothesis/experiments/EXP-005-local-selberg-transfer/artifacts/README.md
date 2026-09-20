# EXP-005 artifact index

The accepted machine evidence is under [`canonical/`](canonical/):

- [`result.json`](canonical/result.json), SHA-256
  `3f0ca476c0e2fe688e4e4f43fc11861d9491b3066d067e46bf88d1a441c696a5`;
- [`execution-receipt.json`](canonical/execution-receipt.json), which binds the
  clean source commit, declaration, runner, source documents, output and PASS;
- [`run-output.txt`](canonical/run-output.txt), the raw canonical stdout.

The two `superseded-attempt-*` directories retain the failed serialization run
and the passed but nonportable schema. They are historical evidence and are not
the accepted certificate. The proof review and verdict bind only the canonical
result above.
