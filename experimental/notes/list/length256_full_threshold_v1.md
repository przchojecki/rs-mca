```yaml
workboard_item: L
row: RS[F_q,gamma*mu_256,32], rate 1/8, 2^255<=q<2^256; separate q=257^31 family
object: LIST; separately typed MCA corollaries
target_epsilon: 2^-128
agreement: near-cap LIST unsafe 33 / safe 34; tower LIST unsafe 34 / safe 36
B_star: floor(q/2^128), always the original ambient field
direct_statement: exact near-cap all-arity LIST crossing 34; full-threshold MCA and coefficient-field-tower brackets
architecture: DIRECT
atom_or_cell: DIRECT
quantifier: every stated field/coset and every received word or common-support tuple; MCA every received pair
projection_and_unit: distinct codewords/tuples for LIST; distinct finite bad slopes for MCA
claimed_bound: explicit packing uppers and realized cyclic/prefix unsafe witnesses below
status: PROVED
impact: ROW_CLOSURE for the declared near-cap LIST family, not the four-row compiler
falsifier: a failed packing/realized-floor inequality or a near-cap LIST first-safe agreement different from 34
replay: both scripts below; immutable proof/script SHA-256 values in packet.json
```

# Full-threshold length-256 crossings

This is a standalone finite-family contribution to Lane L, independent of
FPC5 source/owner aggregation. It closes a specified family of LIST prize
rows, not the KoalaBear benchmark or the full Prize. The MCA statements
are independent brackets, not an inference that adding one agreement
to a LIST threshold always determines MCA.

## 1. The two field families

Let n=256, k=32, D=gamma H for a multiplicative subgroup H of order
256 in F_q^*, and B=floor(q/2^128). Agreement means at least the stated
integer, so full higher-agreement tails are included. Then:

| Family | LIST | MCA |
| --- | --- | --- |
| 2^255<=q<2^256 | L_r(33)>B>=L_r(34), every arity r | B_C(34)>B>=B_C(36) |
| q=257^31 | L_r(34)>B>=L_r(36), every arity r | B_C(36)>B>=B_C(38) |

Thus the near-cap LIST first-safe agreement is exactly 34. Its largest
safe GRID radius is 222/256=111/128; its REAL safe set is [0,223/256),
with supremum 223/256 not attained. The tower instead has LIST first-safe
agreement in {35,36} and MCA in {37,38}; near-cap MCA is in {35,36}.
The three undecided intermediate agreements are not claimed safe.

The degree-sensitive Johnson agreement is sqrt(n(k-1))=sqrt(7936).
Since 34^2<7936, the near-cap upper is strictly beyond that Johnson
radius, by exactly (sqrt(7936)-34)/256 in normalized radius. It bounds
arbitrary received words, not a selected locator-prefix family.

## 2. Full-threshold packing uppers

For degree-<K RS codewords, including tuples with common agreement,
two distinct explanations cannot agree with the receiver on the same
K coordinates: one nonzero component of their difference has at most
K-1 roots. Counting all K-subsets of each complete agreement set gives

```text
L_r(a) <= floor(binom(n,K)/binom(a,K)), a>=K.       (P1)
```

For MCA we also need the following elementary fact. A word w on h
points that is not degree-<K has at least binom(h-1,K) (K+1)-subsets
on which it is not degree-<K. For K=0 this says a nonzero word has
at least one nonzero coordinate. For h=K+1 it is immediate. Otherwise,
choose a noninterpolating (K+1)-subset and a point x outside it.
Puncturing at x leaves a noninterpolating word, contributing at least
binom(h-2,K) subsets not containing x. Subtract w(x) and divide the
other coordinates by X-x. This shortened word is not degree-<(K-1),
or else w would have been degree-<K. Induction contributes at least
binom(h-2,K-1) subsets containing x. Pascal's identity proves the fact.

For a bad finite slope gamma with explanation f on a noncontained
agreement set, v cannot be degree-<k there: otherwise both u and v
would be codewords on that set. A noninterpolating (k+1)-subset extends
to an a-subset within the agreement set. Apply the fact on this a-set.
No such noncontained (k+1)-subset can belong to two slopes: subtracting
the two explanations would make v, and then u, codewords on it.
Consequently

```text
B_C(a) <= floor(binom(n,k+1)/binom(a-1,k)), a>k.    (P2)
```

These upper proofs use only distinct evaluation points. Neither counts
only exact-shell witnesses or uses a scalar LIST-to-MCA safety shortcut.

## 3. A realized cyclic LIST floor over the original field

For any 1<=K<=n-2 put m=K+1 and beta=gamma^n. For each m-subset
S of D, let P_S(X)=sum_(j=0)^m c_j X^j be its monic locator. Reduction
modulo X^n-beta gives

```text
R_S(X)=rem_(X^n-beta)(X^(n-1)P_S)
      =c_0 X^(n-1)+beta*sum_(j=1)^m c_j X^(j-1).
```

Here c_0=(-1)^m product S takes at most n values, in one fixed coset
of H. The leading wrapped term beta X^K is fixed. Thus at least

```text
ceil(binom(n,K+1)/n)                              (C1)
```

locators share their entire degree->=K part U. Each f_S=U-R_S has
degree <K and agrees with U EXACTLY on S, because on D the multiplier
X^(n-1) never vanishes. Different S give distinct codewords. This is
an actual received word over the original field, with no unproved
flatness input. Diagonal repetition preserves the lower count at all
common-support arities.

Use K=32,m=33 for ordinary LIST. Use K=33,m=34 separately for the
shifted list feeding MCA below; it is not an ordinary RS[32] floor.

## 4. Lists give actual pole slopes, with collisions priced

Suppose L distinct degree-<=k polynomials P_i explain W on at least
a>k coordinates. At alpha outside D define

```text
u=W/(X-alpha), v=-1/(X-alpha), gamma_i=P_i(alpha),
f_i=(P_i-P_i(alpha))/(X-alpha), deg f_i<k.
```

The explanations retain their agreements. The direction v cannot agree
with a degree-<k polynomial on more than k points: (X-alpha)g+1 is
nonzero at alpha and has degree at most k. Hence these are genuinely
noncontained witnesses for the original RS[k] pair.

For each pair i!=j, collisions P_i(alpha)=P_j(alpha) occur at at most
k poles. Averaging the number of colliding pairs over q-n poles gives
one pole with C_alpha<=k*binom(L,2)/(q-n). If its value multiplicities
are m_b, Cauchy-Schwarz gives

```text
#{P_i(alpha)} >= L^2/sum_b m_b^2
              = L^2/(L+2 C_alpha)
              >= L(q-n)/(q-n+k(L-1)).              (SP)
```

Alternatively, if k*binom(T,2)<q-n for a chosen T<=L, one pole
avoids every pair collision and gives T distinct original finite slopes.
These are lower/unsafe statements only.

## 5. Near-cap row closure and separate MCA interval

For 2^255<=q<2^256, we have 2^127<=B<=2^128-1. The accompanying
integer certificate checks

```text
floor(binom(256,32)/binom(34,32)) <= 2^127,
ceil(binom(256,33)/256) > 2^128-1,
floor(binom(256,33)/binom(35,32)) <= 2^127.          (N1)
```

The first two comparisons, (P1), and the ACTUAL floor (C1) prove
the exact all-arity LIST crossing. The third and (P2) prove MCA
safety at 36, uniformly over every received pair.

For MCA unsafety at 34, the shifted (C1) list has at least L=2^129
members. The certificate also checks

```text
ceil(binom(256,34)/256) >= L,
2^255-256 > 32(L-1).
```

Thus (SP) gives more than L/2=2^128 distinct bad slopes at a pole,
exceeding every permitted B. This proves the separate MCA interval;
it does not determine agreement 35.

## 6. Coefficient-field tower: different unsafe endpoints

The prime 257 has no prime divisor <=sqrt(257)<17 (check
2,3,5,7,11,13). Put q=257^31. It satisfies 2^248<q<2^249,
not the near-cap hypothesis. H=F_257^* has order 256. Normalize the
coset by X=gamma Y; this is a degree-preserving code isomorphism
and does not change q or B.

For monic m-subset locators on H, the nonleading coefficients in
degrees m-1,...,K take at most 257^(m-K) values. Pigeonholing this
prefix yields an actual degree-m received polynomial U with at least

```text
ceil(binom(256,m)/257^(m-K))                       (C2)
```

degree-<K explanations, each at EXACT agreement m. Use (K,m)=(32,34)
for ordinary LIST and (33,36) for the separate shifted list. The
certificate verifies that both counts exceed the ORIGINAL budget

```text
B=1499986596337394119150021185100322782.
```

Choosing T=B+1 shifted explanations, the exact inequality
32*binom(T,2)<q-256 provides a collision-free pole. Thus MCA is
unsafe at 36. The safe sides follow independently from

```text
floor(binom(256,32)/binom(36,32)) <= B,
floor(binom(256,33)/binom(37,32)) <= B.
```

This proves all entries in the second row of the table. It leaves
LIST 35 and MCA 37 open. Using the coefficient field in (C2) does
not replace the challenge denominator by 257.

## 7. Replay, provenance, and scope audit

```bash
python3 experimental/scripts/verify_length256_full_threshold_v1.py
python3 experimental/scripts/audit_length256_full_threshold_v1.py
```

All arithmetic is integer-only. The first script uses binomial products;
the second independently uses a Pascal row and validates hostile packet
mutations. The canonical packet freezes proof/script hashes. This is a
complete finite arithmetic check, NOT an exhaustive finite-field search
or a substitute for the analytic witness/upper proofs above.

Main was checked at 93fba1be3f3299b0ba4708d88715377bbb656e45 and
PR #1151 at f7edd54f889c970825c271c626347dc92f878cdb. Main already
contains cyclic-rotation and interpolation methods in its rate-half
large-domain discussion. In `experimental/rs_mca_thresholds.tex`,
`prop:exact-prefix-list`, `thm:collision-aware-pole` and
`cor:exact-good-pole-reservoir` already give (C2), (SP) and pole
separation, respectively; these proofs were reread and are anchors,
not new theorem claims. The old cyclic floor is likewise TAKEN in
the A5 registry. The raced refinements at agreement 1116691496959
and M31/KoalaBear rank frontiers are outside this packet's row.

The new material here is the full-threshold finite consumption, exact
length-256 crossing and separate actual-field tower interval, with
complete self-contained packing and witness proofs. A scoped search
of the current synthesis/threshold/theorem
ledgers found no such length-256/257^31 packet. The open-PR metadata
survey found no matching packet; this is not a line-by-line audit of all
55 PRs. #1176 concerns a different T(509,35,8) covering problem.

The proofs were reconstructed and audited in AllenGrahamHart's Codex
prize worktree. Local consumers are `prize_full_threshold_brackets`,
`rate_half_cyclic_rotated_prefix_floor` and its simple-pole companion.
They are provenance, not required private-repository dependencies of
this self-contained note. Independent external review remains due.

The original FPC5 portion of #1151 remains an architecture bridge. This
packet adds a DIRECT Lane L family closure without proving any FPC5
aggregate, pruned Q atom, four-row compiler entry, KoalaBear adjacent
bound, or complete grand-prize theorem. The other rates/lengths/fields
and the stated undecided MCA/LIST endpoints remain separate work.

## Compute requests

None. Replays use only a 257-entry Pascal row and small integer products.
They ran locally under RAMguard; no Modal or large enumeration is needed.

Audit verdict: NO ISSUE.
