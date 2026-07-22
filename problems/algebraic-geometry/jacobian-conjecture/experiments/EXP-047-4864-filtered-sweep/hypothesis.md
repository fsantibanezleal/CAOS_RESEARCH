# EXP-047 - The filtered (48, <= 64) sweep on the F1-family shape (route N2)

- **Question.** JCB-040. EXP-045 made the (48, 64) system small (similarity filter: 111
  unknowns). Run it: the first full-window certificates at the classical case-64 degrees.
- **Motivation (derivation, declared).** By the verified similarity theorem (vdE 10.2.1:
  both degrees > 1, N^0 polygons, origin-centered, ratio deg P : deg Q), any genuine
  Keller partner Q with 2 <= deg Q <= 64 of a degree-48 P has support inside the
  (64/48)-scaled polygon of N^0(P) (the scaled polygons are nested in the ratio). So a
  FILTERED window at N = 64 that comes back inconsistent excludes ALL partners of degree
  <= 64 for that P: a sound full-window certificate, cheap.
- **Falsifiable predictions.**
  1. [MV] (The pure F1 shape) P48 = x + R0(1)^3 (degree 48, the B = 16 family's m = 3
     shape with the swallowed linear vertex): the filtered window at N = 64 is EMPTY:
     no Keller partner of any degree <= 64 exists for this sample.
  2. [MV] (Lower-term samples) Two variants with sampled lower-class terms (an x^2
     filler; an x^2 + x^3 y^4 mix) are likewise EMPTY at filtered N = 64.
  3. [D] (Framing) These degrees are the classical case 64 (Moh's fully-detailed case;
     Heitmann): our certificates are sampled-level machine replications on frontier-
     SHAPED polynomials, not a new truth; the value is the demonstrated cost (seconds to
     minutes per sample at ~100 unknowns) for the beyond-150 territory where the same
     run WOULD be new. Timings recorded.
- **Method.** sympy over QQ; the EXP-045 hull filter; window solves. Caps 570 s per part.
- **Success criterion.** 1-2 verified with timings; 3 recorded: the N2 pipeline is
  validated end to end at the target scale.
- **Failure criterion.** A consistent filtered window (escalate hard: a candidate
  partner at the classical case-64 degrees would contradict Moh/Heitmann or expose a
  filter bug; adjudicate with the unfiltered system before any claim).

Declared 2026-07-22 before the run.
