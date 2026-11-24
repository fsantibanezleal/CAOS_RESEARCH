# EXP-002: the closed forms of the character sums on Mat_mu(F_2), against exhaustive counts

Date: 2026-11-24. CPU only, exact integer and rational arithmetic, no randomness. Written before the run; the
enumerated values for mu <= 4 were already known from EXP-001, the closed forms were derived on paper first (note
`context/2026-11-24-hilbert-maps-contract-for-every-mu.md`).

## Question

Do the closed forms of the note agree with exhaustive counts for mu = 2, 3, 4, and do they satisfy the inequality of
the theorem for every mu up to 40?

- H1. p_1(j) = 2^(2 mu - 1)(1 - 2^(-j))/(2^mu - 1)^2 for B of rank j.
- H2. The sum of chi_B over the invertible matrices is (-1)^j 2^(j(j-1)/2 + j(mu-j)) |GL_(mu-j)(F_2)|.
- H3. p_mu(j) = (1 - (-1)^j / prod_{i<j}(2^(mu-i) - 1))/2.
- H4. p_mu(j)/p_1(j) <= 2 - 2^(1-mu), with equality exactly at j = 1, for mu = 2..40 (closed forms only above 4).

## Kill criteria

Any disagreement in H1 to H3 withdraws the corresponding formula of the note. A failure of H4 at some mu withdraws
the theorem.
