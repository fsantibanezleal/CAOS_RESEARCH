# Uniform filler and bounded-complement coordinates

## 1. A family-wide unit column [D]

For `p>=4`, put `L_p=[1,p] union [3p,4p-2]` and `F_p=L_p minus {2,3p}`. Define

$$c_p=[K,F_p\cup\{7p\};6p],\qquad e_p=[K,F_p;13p].$$

The EXP-036 intervals give

$$6p+[1,p]=[6p+1,7p]\subset H_p,\quad
6p+[3p,4p-2]=[9p,10p-2]\subset H_p.$$

Thus every low face of `c_p` has zero degree-two product. The only surviving face deletes
`7p`, since `6p,7p` are high generators and `13p` lies in degree two. That face occupies
position `|F_p|=2p-3`, hence has sign minus:

$$M_pc_p=-e_p.$$

The grading is exact: `sum(L_p)=4p^2-4p+1`, so the source has exterior size `2p-2`
and total offset `4p^2+6p-1`. More generally, for any `F subset L_p` and `h in H_p`
such that `6p+h` lies in degree two,

$$M_p[K,F\cup\{h\};6p]=(-1)^{|F|}[K,F;6p+h].$$

This is an explicit singleton-pivot family, not a new general homological perturbation theorem.

## 2. Repair of the tested sources [MV]

EXP-054 proves `M_p z_p=2(b_A+b_B)+2(-1)^p e_p` for `p=8,9,10`. Therefore

$$z_p^{\rm corr}=z_p+2(-1)^p c_p,\qquad
M_pz_p^{\rm corr}=2(b_A+b_B).$$

The added coordinate is even, so the mod-two cycle is unchanged. The corrected sources have
supports `126,179,239`; there is still no generic formula for those complete sources.

## 3. The low-complement viewpoint [D]

For an ordered low universe `L` and a selected low subset `F` of size `r`, put
`T_r(e_F)=sgn(F,L minus F)e_(L minus F)`. The shuffle sign counts pairs `x in F`,
`y not in F` with `x>y`. Removing `i in F` changes that count by exactly the number needed for

$$T_{r-1}\iota_i=(-1)^{r-1}(e_i\wedge -)T_r.$$

Hence deletion becomes insertion in a small missing set. This preserves exact orientation;
it is not permission to treat an arbitrary projected row mask as a subcomplex. Coefficient
multiplication and high-variable faces remain part of the differential.

## 4. Fixed-high extraction [MV]

At `p=8,9,10`, the saved `S` terms with high exterior `{6p,10p}` have supports `7,8,9`.
Their complete D boundary is `2(b_A+b_B)`. Their K boundaries have supports `7,8,9` and are
not zero. All these source coefficients are even. Each source omits exactly three low indices,
and `sum(missing)-source_coefficient=6p+2`. EXP-056 extracts and proves the uniform half-source
formula. No full-chain nontriviality or all-parameter torsion follows merely from this slice.

The independent checker passes 456 checks, including 97 parameters for the filler and all
three corrected identities, plus 1,793 complement identities and their sign-reversal controls.
