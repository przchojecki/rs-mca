```yaml
workboard_item: L
row: "(F_q0,D,k=2^40,n=2^41,rho=1/2), q_0=6597069766657=3*2^41+1, D a multiplicative coset of size 2^41"
object: LIST
target_epsilon: "not applicable; exact finite-family ordinary list bracket"
agreement: 1116691496959
B_star: "n/a"
direct_statement: "For the declared q_0 and every multiplicative coset D of size 2^41, one received word has at least L_1 = ceil(C(2^41,2^40+2^34-1)/(2^41*q_0^(2^34-2))) distinct codewords of C=RS[F_q0,D,2^40] agreeing with it in exactly 1116691496959 positions, with 1466604010422 <= bits(L_1) <= 1467447159516. This is the zero-remainder boundary s=0 of the integrated cyclic quotient-rotation theorem, whose proof runs unchanged there with partial-fibre locator 1 and no deleted quotient point. Separately, there exists a family of 1116691496959-subsets of a 2199023255552-element set with pairwise intersections at most 2^40-1 and cardinality at least P_pair = ceil(C(n,a)/V_pair), where V_pair = sum_{j=0}^{2^34-1} C(a,j)C(n-a,j) and bits(P_pair) >= 1923364445404; hence no theorem whose only hypotheses are agreement-set cardinality a and pairwise intersection at most k-1 can prove a universal upper bound below P_pair. The predecessor census of 33 legal dyadic scales remains true under its strict 0<s<c contract; the boundary scale is added outside that contract and the census is not amended."
architecture: DIRECT
partition_digest: "n/a (DIRECT)"
atom_or_cell: DIRECT
quantifier: "The lower construction is existential over one received word and holds for every multiplicative coset D of size 2^41 over the declared q_0. The deterministic cap is uniform over every received word. The packing obstruction is an existence statement about abstract a-subset families of an n-element set, not about Reed--Solomon codewords."
projection_and_unit: "distinct ordinary Reed--Solomon codewords in one Hamming ball for the bracket; abstract a-subsets with pairwise intersection at most k-1 for the obstruction. No CA numerator, MCA numerator, support count, ray, or slope."
claimed_bound: "L_1 <= L_max(a) <= U_pack with U_pack = floor(C(2^41,2^40)/C(2^40+2^34-1,2^40)); certified bit bracket 1466604010422 <= bits(L_max(a)) <= 2095944040454, whose endpoint ratio is below 143/100 because 100*2095944040454 < 143*1466604010422; packing-only obstruction bits(P_pair) >= 1923364445404."
status: PROVED
impact: ROUTE_CUT
falsifier: "For the boundary theorem: a legal tuple at s=0 whose every received word has fewer than the displayed count at exact agreement n/2+d*c; a rotated polynomial whose degree->=k part depends on a coefficient outside a_0,...,a_{d-1} and the fixed monic coefficient; a rotated polynomial with a zero on D outside the chosen subset; or two distinct subsets in one prefix fibre giving the same codeword. For the bit interval: failure of any of 2*63^22>65^22, q_0<769*2^33, 2^19*769^46<1024^46, T-2=46*373475417, 2^5*3^12>4^12, ceil((T-1)/22)=780903145, ceil((T-2)/12)=1431655766. For the obstruction: a greedy step deleting more than V_pair candidates, two selected blocks with intersection at least k, or a failure of r! >= (r/3)^r."
replay: "cd experimental/lean/l_zeroremainder_s1 && lake build LZeroremainderS1.Arithmetic LZeroremainderS1.Obstruction LZeroremainderS1 && lake build"
```

# Zero-remainder rate-half list scale: the boundary champion and a packing route cut

## Exact Lane L print block

```text
row:                 (F_q0, D, k = 2^40, n = 2^41, rho = 1/2),
                     q_0 = 6597069766657 = 3*2^41+1, D a multiplicative coset of size 2^41
object:              ordinary LIST, not MCA
radius/agreement:    delta = 1082331758593/2199023255552;
                     integer agreement a = 1116691496959
Johnson comparison:  exact finite-field Johnson agreement a_J = sqrt(2^41*(2^40-1));
                     the agreement is strictly beyond Johnson, with exact squared gap
                     n(k-1) - a^2 = 1170851739846527019909119
bound:               ceil( C(2^41, 2^40+2^34-1) / (2^41 * q_0^(2^34-2)) )
                       <= L_max(a) <=
                     floor( C(2^41, 2^40) / C(2^40+2^34-1, 2^40) ),
                     with certified sizes
                     1466604010422 <= bits(L_1) <= 1467447159516 and
                     bits(U_pack) <= 2095944040454
route:               DIRECT_LIST
CA_or_MCA_input:     none; no CA-to-list or MCA-to-list conversion is used,
                     so no radius shift and no intrinsic-radius condition apply
code_shift:          C = RS[F_q0, D, 2^40]; no C^+ = RS(k+1) shift
status:              PROVED
```

## 1. Frozen row

```text
q_0 = 6597069766657 = 3*2^41+1,
n   = 2^41 = 2199023255552,
k   = 2^40 = 1099511627776,
T   = 2^34 = 17179869184,
a   = k+T-1 = 1116691496959,
C   = RS[F_q0,D,k],   D a multiplicative coset of size n.
```

The object is the ordinary list `L_max(a) = max_u L_u(a)`, the maximum over received
words of the number of distinct degree-`<k` polynomials agreeing with `u` on at
least `a` points of `D`.  The exact closed-ball radius is
`delta = 1082331758593/2199023255552`, and the row is strictly beyond the exact
finite-field Johnson radius with squared gap
`n(k-1) - a^2 = 1170851739846527019909119`.

## 2. The boundary extension, and the exact reason it was missing

The integrated cyclic quotient-rotation theorem assumes a strictly positive
partial-fibre remainder `0 < s < c`.  Its proof extends unchanged to the boundary
`s = 0`: the partial-fibre locator becomes `1`, coefficient-block non-overlap is
vacuous, and no quotient point has to be deleted, so the full quotient is
available.  That admits the previously omitted specialization

```text
c = 1,  N = 2^41,  d = 2^34-1,  m = 2^40+2^34-1,  s = 0,
```

whose exact agreement `n/2 + d*c = k+T-1 = a` is the frozen agreement, and which
gives the ordinary-list lower bound

```text
L_1 = ceil( C(2^41, 2^40+2^34-1) / (2^41 * q_0^(2^34-2)) ) <= L_max(a).
```

The exclusion was contractual, not arithmetical.  Under the predecessor's own
legality predicate the scale `c = 1` fails exactly one conjunct, `0 < s`, while
`c | k`, `1 <= d`, `d <= N/2-1`, `s < c` and the exact-agreement identity all hold
there.  This is mechanized as `strict_contract_excludes_c_one_only_on_positivity`.

## 3. Certified size

The oversized quantity is supplied in closed form with a certified bit-length
interval; no decimal form exists at this scale and none is claimed.  With
`bits(z)` the unique `b` such that `2^(b-1) <= z < 2^b`,

```text
1466604010422 <= bits(L_1) <= 1467447159516.
```

The proof rests on seven exact integer certificates, each mechanized:

```text
2*63^22 > 65^22,
q_0 < 769*2^33,
2^19*769^46 < 1024^46,
T-2 = 46*373475417,
2^5*3^12 > 4^12,
ceil((T-1)/22) = 780903145,
ceil((T-2)/12) = 1431655766.
```

The certified minimum bit length strictly exceeds the predecessor champion's
certified maximum `738734374956`, so this is a change of scale and not a
refinement inside the predecessor interval.

## 4. Full-quotient product flatness

At the boundary the first prefix coordinate is exactly understood.  For a
multiplicative coset `Q` of a cyclic group of order `N` and `1 <= m <= N-1` with
`gcd(m,N) = 1`, every attainable product value has exactly `C(N,m)/N` many
`m`-subsets.  At the frozen specialization `N = 2^41` and `m = 2^40+2^34-1` is
odd, so `gcd(m,N) = 1` and the factor `N = 2^41` in the denominator of `L_1` is
exact rather than a loose pigeonhole.  All remaining looseness lies in the joint
distribution of `a_1(A),...,a_{T-2}(A)` inside one fixed product class.

## 5. New bracket

```text
L_1 <= L_max(a) <= U_pack,
U_pack = floor( C(2^41,2^40) / C(2^40+2^34-1,2^40) ),
1466604010422 <= bits(L_max(a)) <= 2095944040454.
```

The endpoint ratio is below `143/100`, certified by
`100*2095944040454 < 143*1466604010422`.  The predecessor bit gap of roughly
`2.87` was therefore mainly an artefact of omitting the zero-remainder scale, not
a property of the row: at both predecessor endpoints the ratio exceeded `143/100`.

## 6. Packing-only route cut

Put `r = T-1 = a-k`, let `V_pair = sum_{j=0}^{T-1} C(a,j) C(n-a,j)` and
`P_pair = ceil(C(n,a)/V_pair)`.  A greedy selection that repeatedly takes one
remaining `a`-subset and deletes its conflict neighbourhood produces a family of
`a`-subsets with pairwise intersections at most `k-1` and cardinality at least
`P_pair`, and at the frozen integers

```text
bits(P_pair) >= 1923364445404.
```

Hence no theorem whose only hypotheses are `|A| = a` and `|A intersect B| <= k-1`
for distinct members can prove a universal upper bound below `P_pair`.  In exact
position, `1466604010422 < 1923364445404 < 2095944040454`: the obstruction sits
strictly above the certified lower endpoint and strictly below the deterministic
cap, so set packing and pairwise root counting alone cannot close this bracket.
An upper improvement below that scale must use genuinely Reed--Solomon structure
— locator equations, syndrome geometry, or coefficient consistency.

This is a route cut, not a Reed--Solomon lower bound: the family it produces is
abstract and is not claimed to be realized by any received word.

## 7. Relationship to the predecessor packet

The predecessor result is not amended and not retracted.  Its lower bound is a
valid lower bound, and its census of exactly `33` legal dyadic scales with `c = 2`
dominating is a correct census of the single slices satisfying the strict
positive-remainder contract `0 < s < c`.  This packet supersedes the *scale*, not
the *claim*: it adds one boundary scale outside that contract, and what it refutes
is only the reading of the `c = 2` slice as the strongest available
quotient-rotation lower construction once the proof is closed under its natural
`s = 0` boundary.  The unchanged census is mechanized here as
`predecessor_census_unchanged`.

## 8. Formalization, axioms, and replay

The Lean package `experimental/lean/l_zeroremainder_s1` is stdlib-only, with no
Mathlib and no external dependency.  It certifies the frozen row, the legality of
the boundary specialization, the exact single-conjunct reason the strict contract
excluded it, the unchanged predecessor census, the coprimality hypothesis of the
product-flatness law, all seven small-block certificates, every printed exponent
of both bit bounds and of the obstruction, and the exact position of the
obstruction inside the bracket.  It does not formalize finite fields,
Reed--Solomon codes, the rotation construction, the group action, or the greedy
packing argument; those are proved in the accompanying paper and in the cited
integrated source theorem.

Twenty theorems are stated and each is followed by `#print axioms`.  Every
census reports the generated native-decision certificate axiom.  It additionally
reports `propext` for

```text
LZeroremainderS1.zero_remainder_specialization_legal
LZeroremainderS1.strict_contract_excludes_c_one_only_on_positivity
LZeroremainderS1.predecessor_census_unchanged
```

and no additional axiom for the other seventeen.  All twenty theorems are closed
by `native_decide`; none is closed by the ordinary `decide` tactic.  The `decide`
function occurs exactly once, inside the reproduced predecessor legality
predicate, as a Bool-valued evaluation.  No `sorry`, `admit`, custom axiom, or
committed `.lake/` tree is used.

Replay:

```text
cd experimental/lean/l_zeroremainder_s1
lake build LZeroremainderS1.Arithmetic LZeroremainderS1.Obstruction LZeroremainderS1
lake build
```

## 9. Status of each printed quantity

| Quantity | Direction | Status |
| --- | --- | --- |
| frozen row `q_0, n, k, T, a`, radius, Johnson squared gap | frozen / derived | exact, mechanized |
| boundary specialization `c=1, N=2^41, d=T-1, m=a, s=0` | derived | exact, mechanized |
| single-conjunct exclusion of `c=1` under `0<s<c` | derived | exact, mechanized |
| predecessor 33-scale census | unchanged | exact, mechanized |
| `gcd(m,N)=1` product-flatness hypothesis | derived | exact, mechanized |
| seven small-block certificates | enumerated | exact, mechanized |
| `bits(L_1)` interval `1466604010422..1467447159516` | bounded | proved in the paper, exponents mechanized |
| `bits(U_pack) <= 2095944040454` | bounded | carried unchanged from the predecessor |
| endpoint ratio below `143/100` | derived | exact, mechanized |
| `bits(P_pair) >= 1923364445404` | bounded | proved in the paper, exponents mechanized |
| obstruction position inside the bracket | derived | exact, mechanized |
| exact `L_max(a)` | not obtained / open | full prefix fibre and off-construction codewords unclassified |

## 10. What remains open

The exact maximum list size is not obtained, and the bracket remains enormous.
Two faces remain.  On the construction side, no exact or sharply bounded maximum
fibre is known for `A -> (a_1(A),...,a_{T-2}(A))` on a fixed product class; a
lower-side success there would enlarge `L_1`, an upper-side success would show the
boundary construction is near its own optimum.  On the global side, no theorem
here bounds the number of Reed--Solomon agreement sets using algebra beyond the
pairwise root condition and `k`-point interpolation uniqueness, and any such
theorem must exclude the abstract packings counted by `P_pair`.

The full argument, its falsifiers, and its derivation-direction ledger are in
`experimental/papers/zeroremainder_scale.md`.
