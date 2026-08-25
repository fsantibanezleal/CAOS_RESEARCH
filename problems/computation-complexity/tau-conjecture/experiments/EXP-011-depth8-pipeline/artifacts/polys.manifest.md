# polys.pkl manifest

sha256: 563c2717a84e17d4449bd6bfa774821ce04e95b0259d858b58f715d96dbec640
size: 69.38 MB
content: interned poly table (2,161,049 entries) + first_seen depths through 7
location: artifacts/polys.pkl locally during EXP-011; relocates to E:/_Datos/caos-research/tau-conjecture/EXP-011/ after scan8 completes (D6 rule)

## Correction, 2026-08-25 (adversarial validation pass)

The entry count above read 2,161,169; the file contains 2,161,049. The sha256
and the size both match the file exactly, so the ASSET did not drift: the
manifest's content line was mistranscribed when it was written. Verified by
hashing the file (563c2717...640, matches) and then loading it and counting.

Worth noting for anyone relying on manifests: a correct hash does not certify
the prose next to it. The hash proves the bytes; the description beside it is
unverified text unless something checks it against the bytes.
