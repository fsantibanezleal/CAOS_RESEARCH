# Late primary-source eligibility review

This is a source audit supporting RH-F4, not a new zero theorem or a new
experimental family. Downloads alone do not validate mathematical claims.
The [manifest](source-manifest-20261003-late-review.json) binds the original
PDF/HTML bytes and Lean source ZIP in the external research archive.

## Das--Pujahari: a displayed exponent inconsistency

Primary source: [arXiv:2104.10243v3](https://arxiv.org/abs/2104.10243v3),
Theorems 2--3 and the proof of Theorem 2, printed pages 4--5 and 10--11.
The PDF's page 11 was rendered and visually checked against the HTML and
text extraction. The observed minimum identity is present in the PDF,
rather than introduced by HTML conversion. The journal publication is
listed on the authors' institutional research pages; its full publisher
version was inaccessible, and no corrigendum was located in a limited
title/author/arXiv search. This does not establish that none exists.

The displayed two error powers, without an arbitrarily small epsilon,
are 3-(5/2)a+(7/8)nu and (5/2)(1-a)+(7/4)nu. For both to be below a,
one needs nu<min(4a-24/7,2a-10/7). On 5/7<=a<1 the first is strictly
smaller: their difference is 2a-2. The printed equality choosing the
second branch is therefore arithmetically inconsistent. An exact witness
a=19/20, nu=23/50 satisfies the stated second-branch range, but the first
error exponent exceeds a. An independent rational receipt is retained.

This rejects the displayed derivation as a justification for importing
the entire advertised range. It does not disprove the moment theorem:
another estimate or a correction could repair it. The separate Theorem 3
retains a>1/2+nu and therefore does not itself cross our short-window
length threshold. We will not claim a better onset from this source.

## Qi--Qiao: spectral cancellation requires a family conversion

Primary source: [arXiv:2608.29558v1](https://arxiv.org/abs/2608.29558v1),
Theorem 1, the strategy and Propositions 2--3, and the hybrid large-sieve
setup. The improvement concerns Hecke--Maass spectral coefficients with
n^(it_j), retaining the Eisenstein contribution and its cancellation with
the Kloosterman main term. Its theorem has M>T_s^(4/7), N>T_s^2/M and
N<M^2*T_s^2. These are spectral parameters, not the original zeta height
and interval length. We have not audited all sixteen pages of its proof.

Our present dual expression is a signed composite character/divisor sum.
No identity converting it into the stated spectral family has been proved.
For the naive assignment T_s=T^(1-theta) and N=T^(1+2nu-2theta), near
nu=theta-1/2 the dual length is much smaller than T_s, whereas M<=T_s
forces N>T_s. Thus that assignment cannot directly use Theorem 1.
This is an applicability check, not a general spectral impossibility.
The promising route is to retain the full Eisenstein term through an
actual Kuznetsov conversion; taking absolute values beforehand discards
the cancellation the theorem studies. Its conversion and error bounds
remain open research obligations.

## Cicada Lean port: explicit analytic hypotheses remain

Primary source: [project and trust boundary](https://zeta-zeros.cicada71.net/).
The 91-member archived ZIP passes CRC validation. We inspected
Solution/Basic.lean, ZetaZeros/Defs.lean and docs/TRUST-BOUNDARY.md. Each
of the four zero-counting statements explicitly takes RiemannVonMangoldt
and PairCorrelation as hypotheses. Neither analytic input is proved in
this port. Its finite multiset bounds have a different unconditional scope.
The project attributes its mathematics to Lamzouri and its formalization
to the Axiom upstream; it is not a new stronger proportion method.

We did not run lake build or independently reproduce the claimed axiom
listing. Source inspection of the hypotheses is sufficient to prevent
misreporting an end-to-end unconditional formalization. This port does
not certify the changed-pressure interval computation. Its numerical
dashboard also explicitly excludes rigorous zero completeness and error
bounds; it supplies no additional mathematical evidence for our target.

Archive extraction initially encountered an unavailable pypdf in the
research venv and a Windows console encoding error. Native pdftotext,
rendered PDF review and explicit UTF-8 source extraction resolved these
operational issues. No mathematical claim relies on the failed attempts.

The original source versions remain pinned. No author contact, publication,
new manuscript or research stopping claim follows from this review.
