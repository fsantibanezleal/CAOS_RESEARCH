# Attempt 006: targeted exact determinant reached its gate

The common-quadratic targeted modular selection found one new basis and no
rank defects. Direct reconstruction of that default basis did not finish
within the declared 300-second gate, so the process was stopped and no exact
section was claimed.

The same determinant computation will not receive a larger budget. The
redirect searches alternative full-rank bases at the identical targeted
points, prioritizing previously reconstructed bases plus the minimum required
row replacements. Candidates are scored by their exact largest SCC before any
determinant reconstruction. Only the minimum-cost exact profile advances.

