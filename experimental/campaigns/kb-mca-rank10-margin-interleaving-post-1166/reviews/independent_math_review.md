# Independent mathematics review: rank-ten margin/interleaving packet

Reviewer: isolated adversarial reviewer (`direction_exception_adversary`)

Review date: 2026-08-13

Reviewed clean-restack base: `b67078c7c0254ce9e54e5748634de5133fae98ef`

Reviewed canonical payload:
`642641809784eba3e4323f331bc28cc3d09192a287bd2708752a179080896f53`

## Verdict

**GREEN.**  The mathematical mechanism, exact rank-ten arithmetic, source
statement, and certificate packet pass independent review.  The repaired
interleaving proof dispatches the trivial `mu=1` case before using
`q^(mu-2)`, and the deployed rank-ten proposition explicitly binds the sextic
line field required by the sub-square guard.  The current source also passes a
clean LaTeX replay.

## Statement audited

The implication chain is:

1. the sub-square-root common-support interleaving collapse;
2. the high/low support-margin split for one actual gauged MCA family;
3. the reversible rank-ten gauge from error rank `a=10` to explanation-flat
   dimension `s=9`;
4. the exact KoalaBear specialization at `T=667`, including the disjoint `2w`
   near-rational add-back;
5. the claimed method wall at error rank eleven.

Primary artifacts read:

- `experimental/grande_finale.tex`, especially
  `thm:subsquare-interleaving-collapse`,
  `thm:mca-margin-interleaving-split`, and
  `prop:kb-affine-error-rank-ten-payment`;
- `experimental/notes/thresholds/kb_mca_rank10_margin_interleaving_split_v1.md`;
- `experimental/scripts/verify_kb_mca_rank10_margin_interleaving_v1.py`;
- `experimental/scripts/verify_kb_mca_rank10_margin_interleaving_v1.sage`;
- `experimental/data/certificates/kb-mca-rank10-margin-interleaving-v1/README.md`;
- the predecessor support-local transversality theorem, error-rank gauge,
  ordinary affine-span list compiler, and intrinsic `2w` near-stratum theorem.

## Mathematical audit

### 1. Sub-square-root interleaving collapse

The projection-collision argument is correct for `mu>=2`.  For every linear
projection

```text
Phi_alpha(c_1,...,c_mu)=c_1+sum_(i=2)^mu alpha_i c_i,
```

the image is an ordinary list at the identical common-support agreement
threshold.  Cauchy--Schwarz gives the printed lower collision count, while a
fixed distinct tuple pair collides for at most `q^(mu-2)` projections.  Double
counting yields

```text
L_mu <= floor(L(q-1)/(q-L)).
```

When `L^2<q`, the rational upper bound lies strictly below `L+1`; integrality
and diagonal embedding give `L_mu=L`.

The repaired proof begins by observing that `mu=1` is the definition of `L`
and assumes `mu>=2` before invoking `q^(mu-2)`.  Thus the boundary case is now
closed without changing the statement.

### 2. High-margin part

Passing from the complete explanation flat `c_0+C'` to the affine span of the
high-margin subfamily can only shrink its direction space.  Minimizing the
support mismatch over that smaller space cannot lower any margin.  The
support-transverse theorem therefore gives `H_j(T)` for every positive
subfamily rank `j<=s`.

At rank zero, every explanation is the same word.  Each record supplies at
least `T` incident coordinates with nonzero line direction, and one coordinate
determines at most one finite slope.  The incidence cap `floor(n/T)` is valid.

### 3. Low-margin pair reconstruction

For a minimizing `b_gamma in C'`, the definition

```text
a_gamma=h_gamma-gamma b_gamma
```

places `a_gamma` in `c_0+C'` and gives simultaneous agreement of
`(a_gamma,b_gamma)` with the identical received pair `(r_0,r_1)` on at least
`A=m-T+1` coordinates.  Translating the first component by `c_0` puts the
pairs in the two-fold interleaving of the linear code `C'`.

The ordinary affine-span compiler bounds every projected ordinary list by

```text
M_s(T)=floor(binomial(n-K+s,s)/binomial(w-T+1+s,s)).
```

The sub-square-root theorem therefore bounds the number of distinct pairs by
`M_s(T)` under the declared field guard.

For a fixed pair `(a,b)`, its intrinsic common core has size at least `A`.
Pair noncontainment supplies an actual exception coordinate, and

```text
gamma=-(r_0(x)-a(x))/(r_1(x)-b(x))
```

shows that one chosen exception coordinate cannot own two distinct slopes.
Thus the factor `n-A` is correct in distinct affine-slope units.  Duplicate
pair labels are deduplicated before applying this multiplicity; multiple
slopes owned by the same pair are intentionally allowed.

### 4. Gauge and original-record preservation

The predecessor gauge changes the line representative but preserves every
slope, error word, selected support, and same-support containment predicate.
For the inverse-gauge version, if `b_0` is the gauge codeword and `b'_gamma`
is a translated minimizing direction, then

```text
B_gamma=b_0+b'_gamma,
A_gamma=h_gamma-gamma B_gamma
       =h'_gamma-gamma b'_gamma.
```

Hence `A_gamma` and `B_gamma` lie in the asserted affine flats and reconstruct
the identical original explanation `h_gamma=A_gamma+gamma B_gamma`.  No
endpoint label, pair label, or gauge representative is counted as an extra
slope.

### 5. Exact KoalaBear arithmetic

Independent exact replay recovered

```text
(n,K,m,w)       = (2097152,1048576,1116048,67472)
T               = 667
A               = 1115382
M_9(T)          = 57781140652
max_j H_j(T)    = 5143522968716559
(n-A)M_9(T)     = 56727790457914040
2w              = 134944
total           = 61871313426765543
B_* - total     = 213109414684629544
```

The sub-square condition is true over the deployed line field

```text
|F|=2130706433^6,
```

and false over the base field `F_2130706433`.  The abstract theorem states the
right guard, and the repaired deployed proposition now explicitly assumes the
sextic line field rather than relying on “KoalaBear” as an implicit field
convention.

The exact scan also confirms:

- `T=16` is the first paying threshold at `s=9`;
- `T=667` is the unique minimizer at `s=9`;
- at `s=10` (error rank eleven), the minimum is
  `1040506078215897711` at `T=876`, above budget;
- the `s=11` and `s=12` minima are larger.

Thus this theorem closes error rank ten and no higher rank.

## Adversarial sharpness control

The fixed-pair factor cannot be improved from the stated hypotheses.  Over
`RS[F_11,D,1]` with `(n,m,w)=(10,3,2)`, put `(r_0,r_1)=(0,0)` on a
two-coordinate core and put

```text
(r_0,r_1)=(-gamma,1),  gamma=0,...,7,
```

on the eight remaining coordinates.  For each displayed slope, zero is the
unique maximal constant explanation on exactly the core plus its own
coordinate.  The support is pair-noncontained and its word has distance
`7>w` from the constant code, so it survives the near deletion.  All eight
slopes choose the same low pair `(0,0)`, attaining exactly

```text
8=n-A.
```

Therefore the rank-eleven frontier requires aggregate structure among
different minimizing pairs or their common cores.  Another scalar reduction
of the per-pair multiplicity cannot close it.

## Source and certificate findings

The Python verifier passes in normal and optimized modes, rejects all three
declared hostile mutations, and the independent Sage replay passes when Sage
is given a writable temporary home.  The verifier checks both sides of the
field-of-definition guard and the complete exact threshold scan.

The current TeX source compiles cleanly with `latexmk`; the earlier transient
delimiter damage was repaired before this review was finalized.  Re-review
confirmed both requested boundary repairs in the source: `mu=1` is dispatched
before the projection count, and the proposition explicitly assumes
`|F|=2130706433^6`.

After those repairs, the Python verifier passes in normal and optimized modes,
the hostile-mutation replay rejects all `3/3` mutations, the independent Sage
replay passes, and `git diff --check` passes.

## Final clean-restack preservation audit

The final packet was re-read as a clean delta on the exact parent
`b67078c7c0254ce9e54e5748634de5133fae98ef`.  The delta preserves the three
reviewed theorem statements and proofs without mathematical change.  In
particular:

- the `mu=1` boundary dispatch remains before the `q^(mu-2)` collision count;
- both the proposition and certificate bind the actual sextic line field;
- the exact rank-ten total remains `61871313426765543`, with slack
  `213109414684629544`;
- the rank-eleven value remains a method wall for this formula, not an
  impossibility theorem;
- the manifest continues to say `active_v4_ledger_movement=0` and
  `KoalaBear_closed=false`.

The canonical manifest binds the exact parent and the complete packet at
payload `642641809784eba3e4323f331bc28cc3d09192a287bd2708752a179080896f53`.
On the clean restack, normal and optimized Python verification, all `3/3`
hostile mutations, the independent Sage replay, a clean 120-page LaTeX build,
and `git diff --check` all pass.  The external review memos are deliberately
outside the hashed packet, so this preservation note does not perturb that
canonical payload.

## Scope and nonclaims

- This is a direct maximum-over-lines distinct-slope payment conditional on
  the already proved intrinsic `2w` near deletion.
- It moves no active-v4 first-match atom and proves no S/A/E chronology.
- It does not close KoalaBear.
- Error rank eleven remains unpaid by this formula.
- The exact toy is a finite falsifier for a multiplicity improvement, not an
  asymptotic counterexample to MCA.
- Layer-cake/dyadic summability: not applicable.
- Moment/Markov/Chebyshev optimization: not applicable.

**Final status: GREEN.**
