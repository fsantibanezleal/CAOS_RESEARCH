# EXP-027 verdict

Status: **CONFIRMED**.

For every integer `p>=4` and every field,

```text
beta_(2,4)=8p,
beta_(3,4)=p(5p-1)(500p^2-440p+47)/2.
```

The `8p` second syzygies are multiplicity-free in the offset grading and occur exactly at

```text
{3p+a : a in G_p and a>=6p}.
```

The result is characteristic-independent. The proof combines:

1. a direct identification of offset Koszul strands with relative squarefree-divisor chains;
2. an integral lexicographic matching giving at most one class at each predicted offset and none
   elsewhere;
3. the exact colon
   `(Q_p:f_p)_1=span{X_a : a>=6p}`, whose minimal mapping-cone classes give the matching lower
   bound; and
4. the Hilbert-numerator coefficient in degree four for the adjacent `beta_(3,4)` formula.

All declared gates pass: mandatory smoke, 297-parameter campaign, full explicit offset profiles
at `p=4,5,6`, two-characteristic check at `p=4`, six-query all-parameter symbolic certificate,
independent reconstruction audit, premise hashes, and adversarial controls.

This is a relevant new result: it is the first exact interior strand of the presentation-ring
resolution and introduces a reusable relative-homology method. It is not a full Betti table. The
main conductor-fiber manuscript should receive a v0.14 update; a separate manuscript is not yet
justified.
