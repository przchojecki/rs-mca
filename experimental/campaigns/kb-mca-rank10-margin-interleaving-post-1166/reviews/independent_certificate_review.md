# Independent certificate review: rank-ten margin/interleaving packet

Reviewer: isolated certificate and exact-arithmetic reviewer

Review date: 2026-08-13

Reviewed clean-restack base:
`b67078c7c0254ce9e54e5748634de5133fae98ef`

Reviewed canonical payload:
`642641809784eba3e4323f331bc28cc3d09192a287bd2708752a179080896f53`

## Statement audited

The packet claims that the KoalaBear post-near affine-error-rank-ten branch
is bounded by

```text
2w + max_(0<=j<=9) H_j(667) + (n-m+666) M_9(667)
= 61,871,313,426,765,543
< 274,980,728,111,395,087,
```

with slack `213,109,414,684,629,544`. It also claims that an exact scan
over every legal integer threshold has first paying threshold `T=16`, unique
rank-ten optimum `T=667`, and first higher-rank method wall
`1,040,506,078,215,897,711` at `T=876` for error rank eleven. The
certificate expressly claims zero active-v4 ledger movement and no
KoalaBear closure.

## Files and sections read

- `experimental/grande_finale.tex`:
  `thm:subsquare-interleaving-collapse`,
  `thm:mca-margin-interleaving-split`, and
  `prop:kb-affine-error-rank-ten-payment`;
- `experimental/notes/thresholds/kb_mca_rank10_margin_interleaving_split_v1.md`;
- `experimental/scripts/verify_kb_mca_rank10_margin_interleaving_v1.py`;
- `experimental/scripts/verify_kb_mca_rank10_margin_interleaving_v1.sage`;
- `experimental/data/certificates/kb-mca-rank10-margin-interleaving-v1/README.md`;
- the canonical manifest with the payload printed above;
- `reviews/independent_math_review.md` for the separate proof-joint review.

Ancestor-chain guidance came from the repository `agents.md` and the
`math-proof-audit` skill. No sibling override was used.

## Dependencies

- **PROVEN/IMPORTED:** support-local transversality and its exact rank-ten
  gauge specialization from the predecessor packet.
- **PROVEN:** the ordinary affine-span list compiler.
- **PROVEN:** the finite-field projection-collision theorem, with the
  `mu=1` case separated before the `q^(mu-2)` count.
- **PROVEN/IMPORTED:** the intrinsic near-rational charge `2w=134944` under
  its printed KoalaBear guards.
- **EXACT CERTIFICATE:** complete threshold scans at explanation ranks
  `9,10,11,12`, the sextic-field guard, and the GF(11) multiplicity fixture.
- **NOT IMPORTED:** no Exa result or external literature theorem is
  load-bearing. The recorded Wolfram calculation is an independent integer
  replay, not a logical dependency.

## Exact optimizer audit

The primary verifier uses exact integers and `Fraction` arithmetic. It scans
every threshold `2<=T<=w`, retaining only thresholds satisfying the strict
guard `M_s(T)^2<p^6`. The reported scan counts are

```text
s=9:  66,662
s=10: 65,810
s=11: 64,482
s=12: 62,597.
```

It orders optima by `(total,T)`, separately records the first paying
threshold, and counts minimizer multiplicity. The replay recovered:

```text
s=9:  T=667,  total=61,871,313,426,765,543
s=10: T=876,  total=1,040,506,078,215,897,711
s=11: T=1146, total=18,020,673,627,684,167,414
s=12: T=1487, total=323,734,765,765,217,100,200.
```

For `s=9`, `T=16` is the first paying threshold and `T=667` is the
unique minimizer. The adjacent totals at `T=666,668` are also certificate
bound, so the uniqueness assertion is not inferred merely from rounded
output. For `s=10`, the minimum exceeds the budget by
`765,525,350,104,502,624`; this is a method wall for the printed formula,
not an impossibility result for error rank eleven.

## Field guard audit

The deployed proposition explicitly binds the line field

```text
|F| = 2130706433^6.
```

At `T=667`, the ordinary cap is `M_9=57,781,140,652`. Both the Python and
Sage replays verify

```text
M_9^2 < 2130706433^6,
M_9^2 >= 2130706433.
```

Thus the sub-square-root theorem is used over the actual sextic line field,
and would not be licensed over the prime field alone. The strict inequality
and extension degree are present in the manifest rather than inferred from
the row name.

## Sage fixture and multiplicity semantics

The independent Sage script reconstructs the decisive rank-ten integers and
the GF(11) constant-code star. The fixture has eight distinct slopes, exact
maximal supports consisting of a two-point core plus one private coordinate,
same-support pair noncontainment, and one common low pair. It attains

```text
owners = 8 = n-A.
```

This validates the certificate's multiplicity semantics: `n-A` counts
distinct affine slopes owning one deduplicated pair. It also blocks any
silent replacement by pair labels, supports, distinct neighboring pairs, or
a smaller universal multiplicity.

## Mutation and custody audit

The frozen packet passed:

```text
python3 verify_kb_mca_rank10_margin_interleaving_v1.py
python3 -O verify_kb_mca_rank10_margin_interleaving_v1.py
python3 verify_kb_mca_rank10_margin_interleaving_v1.py --tamper-selftest
sage verify_kb_mca_rank10_margin_interleaving_v1.sage
git diff --check
```

The normal and optimized runs reproduced payload
`642641809784eba3e4323f331bc28cc3d09192a287bd2708752a179080896f53`.
The tamper self-test rejected all `3/3` declared mutations, including a
false KoalaBear-closure flag. The manifest binds the source, note, scripts,
campaign ledgers, literature record, parent commit, row constants, exact
tables, and provenance. Review memos are deliberately outside the hashed
packet, avoiding a self-referential review hash.

The final clean-restack manifest includes the R-004--R-006 registry rows and
binds all 16 declared packet files. An independent SHA-256 replay found no
file mismatch and reproduced the canonical payload exactly. The campaign
actionability audit reports three provisionally verified claims, six passing
reviews, five dependencies, and no errors. The source delta is confined to
the theorem/status additions and this packet; no unrelated mathematical
source is altered.

## Parameter dependence

All numerical conclusions are for the fixed official KoalaBear row

```text
(p,e,n,K,m,w,B*)
=(2130706433,6,2097152,1048576,1116048,67472,
  274980728111395087).
```

The symbolic theorem is finite and uniform in the displayed
`(F,D,K,m,s,T)` parameters subject to `A>K` and `M_s(T)^2<|F|`. There is
no hidden dependence on `T,Y,L,L_barI,lambda,I`, or an asymptotic regime.

## Layer-cake / dyadic summability

Not applicable. The high/low split is a single disjoint finite partition,
not a weighted layer-cake argument.

## Moment / Markov / Chebyshev

Not applicable. The proof uses exact list bounds, projection collisions,
and a direct slope-coordinate injection; it uses no probabilistic moment or
tail optimization.

## Edge cases and notation

- The projection theorem separates `mu=1` before using `q^(mu-2)`.
- The deployed theorem uses `s=9` for explanation-flat dimension and
  `a=10` for error rank; these are not conflated.
- The threshold interval enforces `2<=T<=w`, so `A=m-T+1>K`.
- Empty high or low subfamilies satisfy their respective bounds trivially.
- Pair noncontainment supplies a nonzero denominator in the slope-recovery
  formula.
- Counts remain distinct finite affine slopes on one actual received line.

## Numerical evidence

The KoalaBear arithmetic is an exact official-scale finite computation, not
toy evidence. The GF(11) fixture is toy-scale but is used only as an exact
sharpness/countercontrol for multiplicity. Neither computation proves an
active-v4 owner bridge or the universal four-rate result.

## Verdict

**GREEN - proof obligation appears satisfied with dependencies verified.**

The certificate and independent Sage joints support C-001--C-003 in their
printed scope. The rank-ten direct branch is paid; the active-v4 chronology
and KoalaBear row remain open.

## Remaining risks

1. This theorem supplies no first-match S/A/E owner transport and therefore
   moves no deployed-v4 atom.
2. The rank-eleven number is a sharp minimum only for this exact
   one-threshold formula. New aggregate structure among distinct minimizing
   pairs could still improve it.

## Minimal next action

Publish the scoped rank-ten payment. Mathematically, the next frontier is
correlation among distinct low-margin minimizing pairs at error rank eleven,
not another scalar multiplicity estimate.

**Final status: GREEN.**
