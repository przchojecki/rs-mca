---
workboard_item: M1
row: Mersenne-31 list at 2^-100
object: LIST
target_epsilon: 2^-100
agreement: 1116023
B_star: 16777215
direct_statement: "At the exact M31 quotient cardinalities there are two surjective abstract prefix maps on the 479-subsets of a 1022-set into F_p^32 whose raw and falling fiber moments agree through order 990, while their maximum fibers are respectively 16777215 and 16794161. Therefore no argument using only the exact average, full-image size, and histogram moments through order 990 can certify the deployed budget; an RS-realizability input is necessary."
architecture: DIRECT_ABSTRACT_OCCUPANCY_OBSTRUCTION
partition_digest: "N/A; abstract occupancy maps, not an active first-match row atom"
atom_or_cell: Q / depth-32 quotient prefix maximum versus average
quantifier: "Existence of two surjective maps from the exact support universe C([1022],479) to an abstract target set of cardinality p^32; equality of every raw and falling fiber moment through order 990."
projection_and_unit: "479-subsets per depth-32 target. No received word, codeword, explanation, ray, slope, or active first-match projection."
claimed_bound: "The safe map has maximum 16777215; the moment-indistinguishable unsafe map has maximum 16794161, exceeding the budget by 16946. Within the single affine-binomial parity-block construction, order 990 is maximal because every order-991 crossing block already has mass greater than C(1022,479)."
status: PROVED / COUNTEREXAMPLE_TO_HISTOGRAM_MOMENT_ONLY_INFERENCE / ROUTE_CUT / OPEN_RS_PREFIX_REALIZABILITY
impact: ROUTE_CUT / LOCAL_ONLY
falsifier: "Failure of the finite-difference moment identities, a nonpositive fiber, a target-count or total-mass mismatch, a good maximum above budget, a bad maximum at or below budget, or an order-991 affine-binomial crossing block with mass at most C(1022,479)."
replay: "python3 experimental/scripts/verify_m31_flatness_keystone_moment_blind_pair.py --check; python3 -O experimental/scripts/verify_m31_flatness_keystone_moment_blind_pair.py --check; python3 experimental/scripts/verify_m31_flatness_keystone_moment_blind_pair.py --tamper-selftest"
---

# M31 flatness keystone: 990 exact moments do not control the maximum

## Verdict

```text
PROVED_ABSTRACT
COUNTEREXAMPLE_TO_HISTOGRAM_MOMENT_ONLY_INFERENCE
ROUTE_CUT
OPEN_RS_PREFIX_REALIZABILITY
```

At the exact cardinalities of the pinned depth-prefix quotient problem, the
maximum cannot be bounded from the average plus any histogram-moment ledger of
the displayed finite order. Two full-image fiber distributions have the same
total mass and the same raw and distinct-collision moments through the certified
order, but one meets the deployed budget and the other exceeds it.

This is not a Reed--Solomon counterexample. It isolates the missing input:
a successful moment argument must use a theorem restricting which occupancy
histograms are realizable by the locator-prefix map, or must retain
target-labelled phase, kernel, shell, or first-match information that is absent
from an unlabelled moment ledger.

The active consumer labels are `def:primitive-q`, `def:q-row-atom`,
`prop:moment-sandwich`, `thm:moment-q`, and `prob:row-sharp-q` in
`experimental/grande_finale.tex`. The integrated `T_64` and `T_16` witnesses
remain read-only context; this packet does not rebuild them.

## Exact instance

Let
\[
 p=2^{31}-1,\qquad
 \mathcal U=\binom{[1022]}{479},\qquad
 \mathcal T=\mathbb F_p^{32}.
\]
Write
\[
 N=|\mathcal U|=\binom{1022}{479},\qquad
 q=|\mathcal T|=p^{32}.
\]
For a map \(\Phi:\mathcal U\to\mathcal T\), put
\[
 f_\Phi(z)=|\Phi^{-1}(z)|,\qquad
 M_k(\Phi)=\sum_{z\in\mathcal T} f_\Phi(z)^k,
\]
and
\[
 C_k(\Phi)=\sum_{z\in\mathcal T}
       (f_\Phi(z))_{\underline{k}}.
\]
Thus \(M_k\) counts ordered same-target tuples with repetition, while \(C_k\)
counts ordered same-target tuples with distinct supports.

The exact mean is \(N/q\), whose ceiling is the deployed quotient average in the
lane brief.

## Theorem: a full-image moment-blind safe/unsafe pair

There are surjective maps
\[
 \Phi_{\rm safe},\Phi_{\rm bad}:\mathcal U\longrightarrow\mathcal T
\]
such that
\[
 M_k(\Phi_{\rm safe})=M_k(\Phi_{\rm bad})
 \quad\text{and}\quad
 C_k(\Phi_{\rm safe})=C_k(\Phi_{\rm bad})
\]
for every integer \(k\) in the certified range, while
\[
 \max_z f_{\Phi_{\rm safe}}(z)=B^*
 \quad\text{and}\quad
 \max_z f_{\Phi_{\rm bad}}(z)>B^*.
\]

Consequently, no valid implication whose complete input is only
\[
 (N,q,M_0,M_1,\ldots,M_{990})
\]
or only
\[
 (N,q,C_0,C_1,\ldots,C_{990})
\]
can certify the deployed maximum-fiber inequality on this instance. The same
obstruction applies to any collection of unlabelled fiber statistics that is a
polynomial of degree at most the certified order in each fiber size.

### Proof

Set
\[
 r=990,\qquad m=r+1,\qquad h=16946,\qquad x=675.
\]
For every polynomial \(P\) of degree less than \(m\), the \(m\)-th finite
difference vanishes:
\[
 \sum_{j=0}^{m}(-1)^j\binom mj P(x+jh)=0.
\]
Taking \(P(X)=X^k\) gives
\[
 \sum_{\substack{0\le j\le m\\j\ {\rm even}}}
   \binom mj(x+jh)^k
 =
 \sum_{\substack{0\le j\le m\\j\ {\rm odd}}}
   \binom mj(x+jh)^k
\]
through the asserted order.

Create an even block by using the fiber size \(x+jh\) with multiplicity
\(\binom mj\) for every even \(j\), and an odd block by doing the same for every
odd \(j\). Each block uses
\[
 \sum_{j\ {\rm even}}\binom mj
 =\sum_{j\ {\rm odd}}\binom mj
 =2^{m-1}
\]
target labels. Because \(m\) is odd, the largest even index is \(m-1\) and the
largest odd index is \(m\). Hence the even block has maximum exactly the budget,
whereas the odd block exceeds it by one step.

The two block masses agree because the degree-one identity is included:
\[
 T=2^{m-2}(2x+mh).
\]
There are \(q-2^{m-1}\) target labels left and \(N-T\) supports left. Assign the
same balanced positive filler to both maps: a certified number of the remaining
targets receive the upper filler count and all others receive the lower filler
count. The quotient-remainder identity in the verified integer block gives
total mass exactly \(N\). Every block and filler count is positive, so both maps
are surjective.

The raw moments agree by the finite-difference identity and the identical
filler. Every falling factorial \(X_{\underline{k}}\) is a polynomial of degree
\(k\), so the falling moments agree in the same range. Finally, any positive
integer occupancy vector summing to \(N\) is realized by partitioning the finite
set \(\mathcal U\) into blocks of the specified sizes. This proves the abstract
map statement. \(\square\)

## Sharpness inside the affine-binomial block route

The next order would use finite-difference order \(992\). In a single affine
binomial parity block, write the fiber values as \(x+jh\), with nonnegative
integer \(x\) and positive integer \(h\). To put the odd side at or below the
budget and the even side above it, one must have
\[
 x+991h\le B^*<x+992h.
\]
Each parity side then has mass
\[
 2^{990}(2x+992h).
\]

The minimum possible factor is attained at the certified step and offset.
Indeed, if \(h\) is at least that step, the factor is bounded below directly by
\(992h\). If \(h\) is smaller, the strict crossing forces
\(x\ge B^*-992h+1\), and the resulting affine lower bound is larger. The
minimum block mass already exceeds \(N\), so no nonnegative identical filler
can complete a next-order pair at these exact cardinalities.

Thus the certified order is maximal for this precise one-block
affine-binomial construction. This statement does not exclude a different
Prouhet--Tarry--Escott construction, a combination of several signed blocks, or
an RS-specific moment theorem.

## What failed, and what would revive it

### Failed idea

The attempted closure was to replace pointwise prefix-flatness by a sufficiently
long exact collision-moment ledger, then recover the maximum by a power-mean or
moment inversion. The construction above gives the same full-image
normalization and the same exact collision data through a very high finite
order on both sides of the budget. Therefore the ledger itself contains no
certificate telling the two maxima apart.

### Missing input that would revive the route

Any revival must add information not determined by the unlabelled occupancy
histogram. Examples of genuinely additional hypotheses are:

- a proved characterization of occupancy vectors realizable by the depth-prefix
  locator map on the punctured quotient domain;
- target-labelled Fourier phase or effective-image constraints strong enough to
  forbid the bad occupancy vector;
- a kernel weight-enumerator or shell theorem that is pointwise in the target,
  not merely averaged over targets; or
- an exhaustive first-match theorem showing that every heavy target is deleted
  or paid by a named earlier owner.

Without one of these inputs, increasing a finite moment order within the
certified range cannot establish the maximum-versus-average bound.

## Verified integer block

The verifier parses this block and recomputes every value from the primitive
instance parameters. No floating-point comparison decides a claim.

<!-- VERIFIED-INTEGERS-BEGIN -->
p=2147483647
depth=32
domain_size=1022
support_size=479
target_bins=41855804344513474996659235398101492226513356497450298740932889847998693318143069882098996132602011303952349637025722282585533160693229396196872386718816372844518146497415885223313922264348563527038409009746582412510577609691239404142296725925022012935690228019787759005225367255740944911962461962241
total_supports=151271865290567282756670209927671126612573718499984279646030908205795367378645973832177793165136706631573210771619584252500710632400169112681192055348722412206290242750426752087291990702755284787532455089499756167113798752793361036534746315185930511714934550247772523231121741961638844402219522161141316000
floor_average=3614119
ceil_average=3614120
average_remainder=7548778587015219130749919959628379493028775703410749273281236177882372060252956051361373258139744248853801817862284966111208715580527547821932900501597833163649332550399893901282650118721755927357603447484993482512633668572475393014382515879345810719047125207442915642880687636317942661096628835321
budget=16777215
moment_order=990
finite_difference_order=991
step=16946
offset=675
bins_per_parity=10463951242053391806136963369726580181263718864311851635192874886429209483641954321222640418122029864527291727710479949464718215680589004332016189037791576956967351342601788071700268169006221818240189631008834448226154239518944108944497601509840881752510934060240763835605888507473266002770708660224
good_max=16777215
bad_max=16794161
bad_excess=16946
block_twice_mean=16794836
block_mass_per_side=87870172511141509313907046666282639492587215538111900534698081043048599443705652772212782654665459780919041045527083116274115109284060355579750722117353668586822861576688421985481122527239889208482896730846944554554375681712692601444485159875564997564406862874278874566865929058649138450454798776120901632
filler_bins=31391853102460083190522272028374912045249637633138447105740014961569483834501115560876355714479981439425057909315242333120814945012640391864856197681024795887550795154814097151613654095342341708798219378737747964284423370172295295197799124415181131183179293959546995169619478748267678909191753302017
filler_mass=63401692779425773442763163261388487119986502961872379111332827162746767934940321059965010510471246850654169726092501136226595523116108757101441333231368743619467381173738330101810868175515395579049558358652811612559423071080668435090261155310365514150527687373493648664255812902989705951764723385020414368
filler_low=2019686
filler_high=2019687
filler_high_multiplicity=6554330577864029997757488074510964443329149521430129199305074343407172100977280887142916031057187532217459236609415149270083309134617477378761770497712523465910692465482056893590309802822573717854487484377565673172270866039513399032916765996035697031873512016178107726347815950606374867925482907706
filler_low_multiplicity=24837522524596053192764783953863947601920488111708317906434940618162311733523834673733439683422793907207598672705827183850731635878022914486094427183312272421640102689332040258023344292519767990943731894360182291112152504132781896164882358419145434151305781943368887443271662797661304041266270394311
next_moment_order=991
next_finite_difference_order=992
next_minimizing_step=16913
next_minimizing_offset=0
next_minimum_twice_mean=16777696
next_minimum_block_mass_per_side=175560992897994223492256905780408165400867570934889495932368956210543802236861682447359809252564307969960084310841208606214404948351355415625250686754599589544603302751364649323413302458063011775001156611418397686666155079760030500861661630861251322415575688338765222441589573188280185121622107605805563904
next_block_exceeds_total_by=24289127607426940735586695852737038788293852434905216286338048004748434858215708615182016087427601338386873539221624353713694315951186302944058631405877177338313060000937897236121311755307726987468701521918641519552356326966669464326915315675320810700641138090992699210467831226641340719402585444664247904
<!-- VERIFIED-INTEGERS-END -->

## Provenance and proof boundary

Context was read at lab base
`d968e1cb9a3a6dbcfba35ecf9f448b4a373a35bb`, synchronized to upstream
`71f64349a8fa8cbf05678a6e9d4e00e8e06d7de5`. The certificate records the Git
blob identifiers of the active Grande Finale, live four-row compiler, integrated
flatness/mixing packets, and prior moment-order audit. They are provenance only:
the theorem here is self-contained and the verifier deliberately does not fail
on steering or contextual-file drift.

The packet proves no statement that either constructed map is the actual
locator-prefix map. It supplies no received word, first-match survivor,
codeword, ray, slope, list-size lower bound, or row-global `U_Q`. It does not
move the M31 LIST endpoint.

## Replay

```bash
python3 experimental/scripts/verify_m31_flatness_keystone_moment_blind_pair.py --check
python3 -O experimental/scripts/verify_m31_flatness_keystone_moment_blind_pair.py --check
python3 experimental/scripts/verify_m31_flatness_keystone_moment_blind_pair.py --tamper-selftest
```

The checker is deterministic, stdlib-only, uses exact integers, directly checks
every finite-difference moment identity in the certified range, validates the
balanced filler and next-order boundary, checks packet hashes, and rejects
semantic mutations. Python is replay; the proof is the finite-difference
argument above.

# OPEN GAP
