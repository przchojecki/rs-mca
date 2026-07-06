# CAP25 v13 raw: conj:Q divisor-lattice rung audit at a0+1 (M31-MCA)

Status: `AUDIT` / `EXACT_LEDGER` / `PROVED-LOCAL(identity D)` / `OPEN(reductions)` /
`TIGHT(pessimistic ladder EXCEEDS K_raw -- NOT a refutation)`.

**Data:** `experimental/data/certificates/frontier-adjacent/m31_mca_conjq_rung_audit_v1.json`.
**Verifier:** `experimental/scripts/verify_m31_mca_conjq_rung_audit.py` (zero-arg,
`--tamper-selftest` supported).

**Label migration (grande_finale.tex was promoted at upstream e749e9e AFTER
this PR was filed):** the conjecture environments were removed from the
promoted note; `conj:Q` is superseded by the formal open Problem
`prob:row-sharp-q` (the plain name "Q" is retained there for the residual
safe-side mechanism, so this note's usage remains readable); `conj:BC` ->
`prob:saturated-bc`; `thm:q-implies-sp` eliminates SP as an independent
target. Citations below were written against the pre-promotion text; apply
this mapping when reading them. No number or verdict in this audit is
affected by the promotion.

**Sibling of the KB-MCA rung audit (PR #361, integrated at 0fa9427 as `experimental/notes/thresholds/cap25_v13_qfin_rung_audit.md`); same compiler, M31 constants
(`v2(m_safe)=3 => 3-rung ladder`).** This note executes the same
`grande_finale.tex` Work-Plan paragraph "Rung audit" as the integrated KB audit, for the
Mersenne-31 MCA v13 raw row `(1116023, 1116024)`:

> "Before trying to prove hard equidistribution, run the exact divisor-lattice
> audit at `a_0+1` for all quotient scales. If any periodic rung exceeds the
> budget, the adjacent conjecture is false for a paid reason and the edge must
> move. If every rung is below budget with printed margin, the remaining work
> is genuinely primitive." (`grande_finale.tex`, Work Plan, `\paragraph{Rung
> audit}`)

**Headline (read this before the sections below).** Unlike the KB-MCA
sibling, which found every rung comfortably `BELOW` budget with `7+` bits of
margin to spare (verdict `GREEN`), this audit finds that the **same**
pessimistic same-bar ladder construction **EXCEEDS** the M31 row's tiny
budget (`K_raw=9`) by a factor of `~4.66x` -- `2^2.2216`, the exact-sum
ratio `41.977/9`; the charge ratio `42/9 ~= 4.667` differs in the third
decimal because the charge is the ceil -- (aggregate charge `42` against
budget `9`). This is a genuinely different, honest outcome, not a copy of the
KB result with smaller numbers -- see Sec. 5 and Sec. 7 for the precise,
carefully-hedged statement of what this does and does not establish. In
particular: **this is not a refutation of `conj:Q`, and it does not move the
frontier edge** (Sec. 8). It is a quantitative confirmation, to the integer,
of what `experimental/rs_mca_proximity_prize_status.md` already states in
prose: *"The Mersenne-31 rows, at ≈ 3 bits, demand exact extremality."*

Because `n = 2^21` (the M31 row's own scale `M`, Sec. 1), the divisor lattice
is again the full 2-adic tower `j = 0..21`, so the audit below is complete,
exactly as for KB.

**What this note is not.** It does **not** prove `conj:Q`; it does **not**
prove `U(1116024) <= B*`; it does **not** prove `U(1116024) > B*` either; it
does **not** move the frontier edge `(1116023, 1116024)` in either direction.
It reduces the full-target wall exactly to `conj:Q`'s subset-primitive core
plus an explicit three-rung ladder -- but, unlike KB, that ladder's pessimistic
charge is not budget-negligible here (verdict below). It is also **distinct**
from this packet family's existing `m31_mca_v1.packet.json`
`.rung_margin_audit` block, which is a different object computed at a
different (older, pre-move) pair -- see Sec. 8 below for the reconciliation.

---

## 1. Setup and constants (M31-MCA safe row)

Row/extension/target constants taken from
`experimental/scripts/'towards v13'/cap25_v13_raw_moved_frontier_checks.py`
(the `"Mersenne-31 MCA"` row tuple) and cross-checked exactly against
`experimental/data/certificates/frontier-adjacent/m31_mca_v1.packet.json`'s
own `target.B_star` and `v13_raw_moved_pair` blocks:

```text
p'   = 2^31 - 1 = 2147483647          (Mersenne-31 prime, p' = 3 mod 4)
q    = p'^4                            (QM31 quartic extension)
n    = 2^21 = 2097152,
k    = 2^20 = 1048576,
B*   = floor(q / 2^100) = 16777215     (= 2^24 - 1; 24 bits)

m_unsafe = 1116023,   w_unsafe = m_unsafe - k - 1 = 67446,
m_safe   = 1116024,   w_safe   = m_safe   - k - 1 = 67447.

avg = binom(n, m_safe) / p'^w_safe,   log2(avg) ~= 20.741147035.
log2(B*) ~= 23.999999914,
log2(B*/avg) ~= 3.258852879,
K_raw = floor(B* p'^w_safe / binom(n, m_safe)) = 9.
```

`K_raw=9` and `budget_bits~=3.259` reproduce, to the shown precision,
`rs_mca_proximity_prize_status.md`'s quoted M31-MCA fail margin ("3.3 bits")
and `m31_mca_v1.packet.json`'s `target.B_star.value = 16777215` and
`v13_raw_moved_pair.fail_margin_bits_a1p = -3.2589` (same quantity, opposite
sign convention) -- three independent sources agreeing to the integer/decimal.

**One further exact fact this audit needs, not stated in any prior note:**
`v2(m_safe) = 3` (`m_safe = 2^3 * 139503`, `139503` odd -- verified directly:
`1116024 / 8 = 139503`, `139503 mod 2 = 1`). This is the hard cap on how many
rungs the descent ladder below can reach (Sec. 3), and it is **one less than
the KB row's cap of 4** (`v2(1116048)=4` there). So the M31 ladder has
**three** nonprimitive rungs (`s=1,2,3`), not four.

**The domain.** Unlike KB (a literal multiplicative coset `alpha*mu_n subset
F_p^*`), the M31-MCA row's domain is the **Chebyshev/circle** construction:
per `m31_mca_v1.packet.json`'s own `row.D` field, *"chi(twin coset) on the
norm-one torus -- NOT a multiplicative subgroup."* Concretely
(`experimental/cap25_cap_v13_raw.tex`, `sec:circle-geometry` and
`thm:fiber-descent`): let `U` be the norm-one torus of `F_{p'^2}/F_{p'}`
(`p' = 3 mod 4`), cyclic of order `p'+1 = 2^31`; the deployed row uses a
standard-position twin coset `mathcal D = gH cup g^{-1}H` of size `2M` with
`M = 2^21` (`ord(g) = 2^23 nmid 2^22 = 2M`, per `cap25_cap_v13_raw.tex`'s own
worked instantiation of this exact row). The `x`-coordinate map
`chi(u) = x` is exactly two-to-one on `mathcal D` (no self-inverse element,
since `g^2 notin H`), landing on `D := chi(mathcal D) subset F_{p'}`,
`|D| = M = n`. For `c | M`, `K_c <= U` is the order-`c` kernel of the
`c`-th power map, and (`lem:cheb-fibers`) the Chebyshev/Dickson-map
`T_c`-fibers in `D` are exactly the `chi`-images of the `K_c`-orbits on
`mathcal D`.

This is **not** a cosmetic restatement: the paper's own general theorems
(`thm:stabilizer-partition`, `thm:fiber-descent`, `cor:periodic-support-count`,
`cap25_cap_v13_raw.tex` L4467-4532) are stated and proved for **exactly two**
parallel cases, "multiplicative" and "Chebyshev," side by side, "with the
divisor lattice of `D` replaced by the dyadic scale lattice of the twin
coset" (L4865) -- and critically, `thm:stabilizer-partition`(i)'s own proof
notes that because the lift `Stilde := chi^{-1}(S) cap mathcal D` of any
`S subset D` is *automatically* inversion-closed by construction, "a union of
complete `T_c`-fibers" is equivalent to `Stilde` being `K_c`-invariant --
i.e. the periodicity/stabilizer bookkeeping is governed by the plain **cyclic**
group `K_M <= U` exactly as KB's is governed by `mu_n <= F_p^*`; the extra
inversion the twin-coset construction carries costs nothing extra (no
dihedral factor-of-two complication). Section 2 below states identity `(D)`
in the same domain-agnostic language Lane C's compiler design note uses (the
identity is domain-2-power generic; only constants change), then maps its
abstract objects onto this Chebyshev-case realization explicitly.

Because the abstract integers `(n, m_safe, w_safe, p', B*)` are all that the
numeric ledger below depends on, **every number in Sec. 4-6 is identical in
form to what a literal multiplicative-coset model would produce** -- the
domain's different geometric realization changes the *proof* of identity
`(D)`'s mechanics (Chebyshev-case character orthogonality via `K_c` rather
than multiplicative-case orthogonality via `mu_c`), not any digit of the
ledger.

The prefix moment map is `Phi_w(M) = (p_1(M), ..., p_w(M))`,
`p_i(M) = sum_{x in M} x^i in F_{p'}` (values land in the base prime field,
since `chi: U -> F_{p'}`), for `m`-subsets `M subset D`. The "twist" action
organizing subsets of `D` by scale is, concretely, `H`'s own right-translation
transported through the bijection `D <-> H` given by `h |-> chi(gh)` (a clean
bijection precisely because `chi` pairs `gh` with `g^{-1}h^{-1}`, never with
itself); the target stabilizer at stratum level is `Stab(z) = K_{gcd(M,I(z))}`,
`I(z) = {i <= w : z_i != 0}` (`gcd(M, empty) = M` for the all-zero target),
exactly paralleling KB's `Stab(z) = mu_{gcd(n,I(z))}`.

---

## 2. The exact image-level descent identity (D)

**Stratification.** Write `v(z) = min_{i in I(z)} v2(i)` (capped at `21`, and
`= 21` for the all-zero target). Stratum `j := {z : v(z) = j}`; `j = 0` is
primitive. (Identical to KB Sec. 2 -- this is pure index arithmetic on `w`,
independent of the domain's geometric realization.)

**Power map / Chebyshev map.** `pi_j : D -> D_j := T_{2^j}(D)`,
`x -> T_{2^j}(x)` (the degree-`2^j` Chebyshev/Dickson map), is exactly
`2^j`-to-1 on `D` (Lane C's abstract "power map" specializes to `x -> x^{2^j}`
in the multiplicative case and to `T_{2^j}` in the Chebyshev case -- both are
literal restrictions of the SAME order-`2^j`-kernel quotient map on the
ambient cyclic group, `mu_n` resp. `K_M <= U`, transported through `chi`).
For any `m`-subset `M`, its fiber-count profile `c_M : D_j -> {0,...,2^j}`
satisfies `sum_y c_M(y) = m`. One Chebyshev-specific caution: unlike the
multiplicative case, the ORDINARY power sums `p_i(M) = sum x^i` do **not**
vanish off multiples of `2^s` for a symmetric `M` (the `T_{2^s}` composition
injects fixed nonzero even-index moments — e.g. `p_2 = 2` for an
`s = 2`-symmetric toy subset). The KB identity `(*)` transfers in the
**Chebyshev basis**, not the monomial basis: for every `i' >= 1`,

```text
sum_{x in M} T_{2^j i'}(x) = 2^j * sum_{y in D_j} c_M(y) T_{i'}(y),      (*_T)
```

the `T`-moments at `T`-indices divisible by `2^j` are exactly the weighted
quotient `T`-moments.

**Subset symmetry.** The subset stabilizer `Stab(M) = mu_{2^s}` (mult. case)
or `K_{2^s}` (Chebyshev case), `s = s(M)`. `M` is scale-`2^s`-symmetric iff
`c_M in {0, 2^s}` (each fiber fully in or out); such `M` are unions of
size-`2^s` fibers, so `2^s | m`, hence **`s(M) <= v2(m_safe) = 3` for every
`m_safe`-subset at this row** -- one less than KB's cap of `4`. Splitting a
fiber by member symmetry level exactly as KB's identity `(E)`:

```text
|Phi_w^{-1}(z)| = sum_{s=0}^{min(v(z),3)} N_s(z),   N_s(z) = #{M in fiber : s(M) = s}.   (E)
```

**Identity (D), and its proof.** A scale-`2^s`-symmetric `M` equals
`pi_s^{-1}(Mbar)` for a unique `Mbar subset D_s`, `|Mbar| = m_safe/2^s`.
In the multiplicative case this uses `sum_{u in mu_{2^s}} u^i = 2^s[2^s|i]`
(KB Sec. 2); in the Chebyshev case the identical mechanism is
`thm:fiber-descent`'s own proof (`cap25_cap_v13_raw.tex` L4525): work over
`F' := F cdot F_{p'^2}`, set `P(u) := p(chi(u))`, a Laurent polynomial; for
`zeta in K_c` and `u in Stilde`, `P(zeta u) = P(u)` on `Stilde`, and since
`|Stilde| = 2|S| >= 2c` exceeds the relevant degree bound, this identity holds
identically -- **only exponents divisible by `c` survive**, and `P` is
*also* automatically inversion-symmetric (because `chi` is), so
`P in F'[u^c + u^{-c}]`; substituting `u^c+u^{-c} = 2 T_c(chi(u))` gives the
same "surviving moments only at multiples of `c`" conclusion as the
multiplicative case's character orthogonality, with **no extra cost** from
the inversion. So, exactly as `(D)` in the KB note:

```text
Nsym_s(z) := #{M in Phi_w^{-1}(z) : M is scale-2^s-symmetric}
           = | (Phi_{w_s}^{D_s})^{-1}( z_down^{(s)} ) |,   row_s = (n/2^s, m_safe/2^s, floor(w_safe/2^s)),
z_down^{(s)} = the reparametrization of the supported targets induced by
               T_{2^s}-composition on the top-w_s locator coefficients        (D)
               (an invertible triangular change of basis; z -> z_down is a
               bijection on the targets the ladder uses).
```

(The multiplicative case's closed form `z_down_{i'} = z_{2^s i'} / 2^s` does
NOT hold here — in the Chebyshev basis the induced map carries affine shift
terms, e.g. `p_2(M) = sum_Mbar y + 2` rather than a pure `/2^s` rescale.
Because the transform is invertible and triangular on the top-`w_s` locator
coefficients, the FIBER PARTITION and hence every count the ledger uses —
`maxPi_s`, `a_s`, the shares — are identical in either basis; the count
identity is exactly what `thm:fiber-descent`'s Chebyshev case proves.)

`(D)` is **PROVED** unconditionally at the paper level (`thm:stabilizer-
partition` + `thm:fiber-descent`, stated and proved for the Chebyshev case
alongside the multiplicative case, `cap25_cap_v13_raw.tex` L4865) and, at the
abstract/generic level Lane C's compiler isolates, verified to the integer
by exhaustive enumeration on toy rows (Sec. 6 below, gate iii of the
verifier) -- the **same four toy rows** the KB audit used (the identity is
domain-2-power generic; only constants change, per
`laneC_compiler_design.md`), run fresh for this packet. Scope stated
plainly: **the four toy rows exercise the multiplicative model only**
(gate iii enumerates `mu_n`-coset domains); they validate the abstract
count pattern of `(D)`/`(E)`, not the circle geometry. For the Chebyshev
realization itself this note rests entirely on the cited TeX theorems
(`thm:stabilizer-partition`, `thm:fiber-descent` Chebyshev case) plus the
basis-independence remark above; a genuine twin-coset toy re-enumeration
is a natural hardening step for a follow-up.

**The correction term** (`sum_{s<j} N_s(z)` for a stratum-`j` target) and
**why naive relaxation fails** (dropping the off-`2^j` vanishing constraints
blows the count up by `p'^{w_safe - w_j}`) are exactly as in the KB note
Sec. 2 -- both are properties of the abstract identity, unaffected by which
row it is instantiated on. The verifier's gate iv reproduces the relaxation
blow-up demonstration on the same toy row (`F17_m9_w2`, `j=1`): true average
`~39.58`, relaxed average `~672.94`, ratio exactly `17^1 = p^{w-w_j}` (using
the toy's own tiny prime, not `p'`).

---

## 3. The 3-rung ladder

Taking `max_z` of `(E)`: `MAXFIBER := max_z |Phi_w^{-1}(z)| <= maxPi_0 +
sum_{s=1}^{3} maxPi_s`, where `maxPi_0` is the subset-**primitive** prefix
fiber (the residual `conj:Q` core, depth `w_0 = 67447`) and `maxPi_s`
(`s=1,2,3`) is the max subset-primitive fiber of the strictly smaller
quotient row `row_s`. The reach stops at `s=3` because `v2(m_safe) = 3` is a
hard cap (Sec. 1) -- **one rung short of KB's reach of `4`.**

**What absorbs strata `j = 4..16, 21`.** For these `j`, `2^j` does **not**
divide `m_safe` (`v2(m_safe)=3`), so no scale-`2^j`-symmetric `m_safe`-subset
exists at all: the entire fiber of any such target is a sum of the *same*
**four** `Pi_s` (`s=0..3`) functions via `(E)`/`(D)` -- no fifth object, no
new proof obligation. (KB's analogous absorbed range was `j=5..16,21`, one
stratum wider, because its cap is `4` not `3`.) The refuted "mode-at-null"
object (`prop:mode-null-false`; the all-zero target is stratum `j=21`) is
again just `sum_{s<=3} N_s(0)`.

**Strata `j = 17..20` are vacuous (PROVED).** The maximum `v2(i)` for
`i <= w_safe = 67447` is `16` (attained only at `i = 65536 = 2^16`; identical
range to KB, since `w_safe` for both rows lies in `[65536, 131071)`), so no
index `i <= w_safe` has `v2(i) >= 17`; these four strata are empty by
construction, not merely small.

---

## 4. The table, j = 0..21

Exact per-rung margin vs. the `K_raw` budget, all 22 scales of the 2-adic
divisor lattice, from an independent from-scratch recompute matching the
shipped `m31_mca_conjq_rung_audit_v1.json` (margins to 9 decimals). Verdict
is one of `RESIDUAL` / `BELOW` / `VACUOUS` / **`EXCEEDS`** -- unlike KB,
**`EXCEEDS` occurs here** (Sec. 5-7 explain exactly what this does and does
not mean).

```text
conj:Q DIVISOR-LATTICE RUNG AUDIT @ a0'+1 = 1116024  (M31-MCA, v13 raw)
wall: CAP25-V13-QFIN-PRIMITIVE-MAX-ORBIT-FLATNESS-M31-MCA-1116024 (an id minted HERE, following the KB naming pattern -- no prior note names an M31 Q-fin wall; the KB id predates its audit in two integrated threshold notes)
K_raw=9 (log2=3.169925001)  budget B*/avg=3.258852879 bits

  j  2^j       n_j      w_j  descend  m_j      log2 a_j       margin_below_Kraw(bits)  pess.share  verdict
  0     1   2097152    67447  trivial  -              -                  0.000000000            9  RESIDUAL (this IS the primitive wall conj:Q; margin=0 by construction)
  1     2   1048576    33723  True    558012   20.959194610           -0.218047575           10  EXCEEDS budget (pessimistic; NOT a proof L_1 is false -- Sec 6/7)
  2     4    524288    16861  True    279006   21.318218138           -0.577071103           13  EXCEEDS budget (pessimistic; NOT a proof L_2 is false -- Sec 6/7)
  3     8    262144     8430  True    139503   21.747729383           -1.006582349           18  EXCEEDS budget (pessimistic; NOT a proof L_3 is false -- Sec 6/7)
  4    16    131072     4215  False   -              -                  -                      0  BELOW budget (no independent mass; covered by s<=3 ladder)
  5    32     65536     2107  False   -              -                  -                      0  BELOW budget (no independent mass; covered by s<=3 ladder)
  6    64     32768     1053  False   -              -                  -                      0  BELOW budget (no independent mass; covered by s<=3 ladder)
  7   128     16384      526  False   -              -                  -                      0  BELOW budget (no independent mass; covered by s<=3 ladder)
  8   256      8192      263  False   -              -                  -                      0  BELOW budget (no independent mass; covered by s<=3 ladder)
  9   512      4096      131  False   -              -                  -                      0  BELOW budget (no independent mass; covered by s<=3 ladder)
 10  1024      2048       65  False   -              -                  -                      0  BELOW budget (no independent mass; covered by s<=3 ladder)
 11  2048      1024       32  False   -              -                  -                      0  BELOW budget (no independent mass; covered by s<=3 ladder)
 12  4096       512       16  False   -              -                  -                      0  BELOW budget (no independent mass; covered by s<=3 ladder)
 13  8192       256        8  False   -              -                  -                      0  BELOW budget (no independent mass; covered by s<=3 ladder)
 14 16384       128        4  False   -              -                  -                      0  BELOW budget (no independent mass; covered by s<=3 ladder)
 15 32768        64        2  False   -              -                  -                      0  BELOW budget (no independent mass; covered by s<=3 ladder)
 16 65536        32        1  False   -              -                  -                      0  BELOW budget (no independent mass; covered by s<=3 ladder)
 17 131072       16        0                          -                  -                      -  VACUOUS (PROVED empty)
 18 262144        8        0                          -                  -                      -  VACUOUS (PROVED empty)
 19 524288        4        0                          -                  -                      -  VACUOUS (PROVED empty)
 20 1048576       2        0                          -                  -                      -  VACUOUS (PROVED empty)
 21 2097152       1        0  False   -              -                  -                      0  BELOW budget (no independent mass; covered by s<=3 ladder)
```

Rungs `j=0` and `j=4..16,21` are `RESIDUAL`/`BELOW` exactly as in KB; strata
`j=17..20` are `VACUOUS` exactly as in KB. **Rungs `j=1,2,3` are `EXCEEDS`**
under the pessimistic same-bar accounting -- this is the row's own genuine
divergence from KB (where the analogous four rungs were comfortably
`BELOW`), not a computational error: it is independently cross-checked below
by exact big-integer cross-multiplication (not merely floating log2), and it
is consistent with -- indeed a precise quantification of -- the tightness
already documented for this row elsewhere in the repo.

---

## 5. Aggregate: residual primitive budget and the rounding policy

The three nonprimitive-rung pessimistic shares (`s=1,2,3`: `10.468426,
13.426358, 18.082313`) are **exact rationals** sharing a common denominator
`binom(n, m_safe)`; their sum, `41.977097`, is not an integer, and -- unlike
KB, where the analogous sum (`35623.86`) was a small fraction of `K_raw`
(`4807520`) -- here the sum **already exceeds** `K_raw = 9` outright, by a
factor of `~4.664`.

**Rounding policy (one sentence, identical wording to KB).** The aggregate
nonprimitive charge is rounded *conservatively* -- `charge :=
ceil(sum_{s=1}^{3} share_s)`, never `floor` -- so that the residual
primitive budget quoted for `conj:Q`'s core is never overstated; here this
still applies, and it makes the reported deficit *worse* (not better), which
is the same conservative direction as KB's use of `ceil`: `charge = 42`
(`ceil` of `41.977097`; the `floor` alternative would be `41` -- which
here coincides with the sum of the per-rung table floors `10+13+18`, two
different quantities that happen to agree at this row -- giving a
*smaller-in-magnitude*, hence less conservative, deficit).

```text
AGGREGATE (conservative rounding policy: charge = ceil, not floor)
  nonprimitive rungs (s=1..3) total pessimistic share (exact float) = 41.977097
  ... floor(share) = 41  (less conservative; NOT adopted)
  ... ceil(share)  = 42  (ADOPTED charge)
  combined margin below K_raw                     = -2.221605485 bits  (i.e. EXCEEDS by 2^2.2216 ~= 4.664x)
  residual "primitive budget" for conj:Q core      = -33   (a NEGATIVE nominal residual; -3.666667 of K_raw)
  charge + residual == K_raw ?                       True   (42 + (-33) = 9, by construction)
  any rung EXCEEDS budget?  YES (j=1,2,3)      all rungs BELOW/RESIDUAL/VACUOUS?  NO
  VERDICT: NOT GREEN -- pessimistic same-bar ladder EXCEEDS K_raw by ~4.66x (NOT a refutation; see Sec 7)
```

**What a negative residual means (and does not mean).** `residual := K_raw -
charge` is a pure bookkeeping identity (`charge + residual == K_raw` holds by
construction regardless of sign, and is checked exactly by the verifier's
gate v). When `residual >= 0` (KB's case), it is a genuine leftover budget
available to the primitive core. When `residual < 0` (this row), it does
**not** mean the primitive core has "negative budget available" in any
operational sense -- `maxPi_0 >= 1` trivially, so the true inequality
`maxPi_0 + sum_s maxPi_s <= K_raw*avg` cannot possibly be certified via this
pessimistic decomposition at all. A negative residual is the ledger's honest
signal that **the decomposition strategy itself is insufficient at this
row's budget scale**, not a claim about any actual fiber size.

**Cross-check against a different, independent metric (informational
only).** The three rungs' own *standalone* slack vs. `B*` (`log2(B*/a_s)`,
computed exactly as KB's informational column, and -- per the explicit
caution repeated from KB Sec. 6 below -- **not** itself the ladder
threshold) is `3.041, 2.682, 2.252` bits for `s=1,2,3`, i.e. **smaller than
the primitive row's own budget (`3.259` bits) at every rung** -- the mirror
image of KB, where every quotient row's standalone slack (`29.5`-`34.8`
bits) comfortably *exceeded* the primitive row's `22.2`-bit budget. Both the
ladder-threshold metric (Sec. 5's main computation) and this informational
metric agree qualitatively: at the M31 row, descending the ladder makes the
quotient rows *harder*, not easier, relative to the primitive row -- the
opposite of KB's pattern.

---

## 6. Minimal lemmas per rung, PROVED / OPEN-REDUCTION

Exactly as KB Sec. 6, one row per nonprimitive rung plus the `s=0` primitive
core, with the same non-negotiable clause: **the ladder threshold is the SAME
flatness bar at every rung, `rho_s <= K_raw`, never a rung-specific standalone
budget** (the caution that produced the "corrected `L_s` framing" in the KB
note applies verbatim here).

| rung | statement (ladder threshold) | standalone slack vs `B*` (bits, informational) | pessimistic share at `rho_s=K_raw` | status |
|---|---|---:|---:|---|
| `(D)` itself (all `s`) | the descent identity of Sec. 2 | -- | -- | **PROVED** (paper-level: `thm:stabilizer-partition`+`thm:fiber-descent`; toy-verified) |
| empty strata `j=17..20` | vacuous, no index `i<=w` has `v2(i)>=17` | -- | -- | **PROVED** (vacuous) |
| `L_1` (`row_1 = (1048576, 558012, 33723)`) | `maxPi_1 <= rho_1 a_1`, `log2 rho_1 <= 3.169925 (= log2 K_raw)` | `3.041` | `10.468` (`>K_raw=9`) | **OPEN-REDUCTION** (pessimistic bound already exceeds `K_raw` alone) |
| `L_2` (`row_2 = (524288, 279006, 16861)`) | `maxPi_2 <= rho_2 a_2`, `log2 rho_2 <= 3.169925 (= log2 K_raw)` | `2.682` | `13.426` (`>K_raw=9`) | **OPEN-REDUCTION** (ditto) |
| `L_3` (`row_3 = (262144, 139503, 8430)`) | `maxPi_3 <= rho_3 a_3`, `log2 rho_3 <= 3.169925 (= log2 K_raw)` | `2.252` | `18.082` (`>K_raw=9`) | **OPEN-REDUCTION** (ditto) |
| `s=0` core (`conj:Q` proper) | `maxPi_0 <= rho_0 avg` at depth `w_0=67447`, domain `n_0=2097152` | `3.2589` (the whole budget) | (residual core) | **OPEN** (head-depth `w<=10-11` **PROVED**, `rem:proved-q-part`) |

Every one of `L_1, L_2, L_3` is individually `OPEN-REDUCTION` in exactly the
same formal sense as KB's `L_1..L_4` -- each is a bona-fide smaller instance
of the same conjecture, at half the depth and domain of the row above it,
and none is disproved by anything in this audit. The difference from KB is
purely quantitative: at KB, `L_1..L_4`'s *own* pessimistic ceiling
(`rho_s = K_raw`) leaves the ladder budget-negligible (`0.741%` of `K_raw`
consumed even in the worst case); here, that same ceiling, applied to all
three rungs *simultaneously*, already overdraws the entire row budget
(`~466%` of `K_raw`). So proving `conj:Q` at the M31 safe row via this
decomposition -- if the decomposition is to certify anything at all -- will
require establishing `L_1, L_2, L_3` at bounds **meaningfully tighter than
the generic `K_raw` bar**, not merely "no less flat than the primitive row
itself" (which sufficed at KB). Trivial-cost consistency of the ladder
itself (that `(E)`/`(D)` correctly charges every nonprimitive stratum to
`L_1..L_3` with no fourth object) is **PROVED** (Sec. 2-3) independently of
this tightness; it is only the *bounding* of `Pi_1, Pi_2, Pi_3` (and of
`Pi_0` itself) that remains open, exactly as at KB.

---

## 7. Frame verdict (honest)

**The compiler still CLEANS the wall's statement and still PROVES the
descent structure; but here it does NOT localize the difficulty to a
comfortably separated primitive core.** Precisely:

1. It replaces the same deferred quotient-descent phrase with the same exact
   finite object: identity `(E)`/`(D)`, now **four** subset-primitive rows
   (`s=0..3`, one fewer than KB's five, since `v2(m_safe)=3` here vs. `4`
   there), and printed per-rung budget shares.
2. Unlike KB, the three nonprimitive strata (`s=1,2,3`) are **not**
   budget-negligible here: even at the identical uniform flatness bar used
   for KB (`rho_s <= K_raw`, "no less flat than the primitive row itself"),
   their pessimistic shares already sum to `41.977` (`ceil 42`) against a
   total budget `K_raw = 9` -- a `~4.66x` overshoot, leaving a **negative**
   nominal residual (`-33`) for the primitive core. The finite certificate's
   ladder, taken pessimistically, does not leave the primitive cell any
   budget at all under this accounting.
3. What the compiler still DOES buy: (a) the exact structural fact that
   nothing beyond these four rows can be the obstruction -- `(E)`/`(D)` is
   unconditionally **PROVED** (at the paper level, for the Chebyshev case
   alongside the multiplicative one) regardless of the row's tightness;
   (b) an honest, quantitative *localization* of exactly where the
   difficulty now lives: **not** purely in the primitive core `s=0` (as at
   KB), but jointly across `{s=0,1,2,3}` together, since the pessimistic
   bound cannot allocate a comfortable separate budget to each rung;
   (c) a precise, checked confirmation of `rs_mca_proximity_prize_status.md`'s
   own qualitative warning that the Mersenne-31 rows "demand exact
   extremality": this audit exhibits *exactly* where that demand bites -- the
   generic/pessimistic same-bar decomposition strategy that suffices at KB
   fails by a factor of `~4.66x` here, so proving `conj:Q` at this row (if
   true) needs genuinely tighter, row-specific quotient flatness bounds for
   `L_1, L_2, L_3` (not merely "as flat as the primitive row"), or a
   fundamentally non-decomposed argument for the row as a whole.

> **Verdict: unlike the KB sibling, the compiler here does NOT reduce the
> wall to a clean "primitive core + negligible ladder" shape.** It proves the
> same descent identity and produces the same kind of finite ledger, but the
> ledger's own arithmetic shows the crude pessimistic ladder EXCEEDS the
> row's tiny budget (`K_raw=9`) by about `4.66x`. This is **not** a
> refutation of `conj:Q`, **not** a proof the frontier moves -- no witness or
> exact `maxPi_s`/`maxPi_0` value has been produced anywhere in this audit;
> `L_1, L_2, L_3`, and the `s=0` core all remain fully **OPEN**. Neither
> branch of `grande_finale`'s Rung-audit paragraph fires cleanly here: not
> the `GREEN` branch (remaining work genuinely primitive -- the ladder is not
> negligible), and not the "exceeds => edge moves" branch either (that branch
> requires an actually **proved** bound to exceed budget, not a pessimistic
> ceiling on an open reduction). The honest third outcome is: **the
> sufficient-condition ladder strategy, applied at the generic bar, is
> inconclusive at this row** -- a materially harder proof-obligation profile
> than KB's, quantified to the integer.

---

## 8. Non-claims

This audit does **not** prove any of the following:

```text
conj:Q (grande_finale.tex \label{conj:Q}),
L_1, L_2, or L_3 (Sec. 6) -- true, false, or at any specific bound,
U(1116024) <= B*,
U(1116024) > B*,
that the frontier edge (1116023, 1116024) moves in either direction.
```

It also does **not** touch `conj:BC` (split-pencil census, `\label{conj:BC}`)
or `conj:SP` (primitive shift-pair control, `\label{conj:SP}`).

**This audit is distinct from the packet family's existing lower-side
audit -- do not conflate them, and note an extra subtlety versus KB.**
`experimental/data/certificates/frontier-adjacent/m31_mca_v1.packet.json`
already carries a `.rung_margin_audit` block -- the periodic **FLOOR** audit
(`Gfloor`/`Gceil`/`Rem`/`Plant` slack profiles vs. the deep-point threshold
`Theta`, across `c = 2^0..2^20`) -- but, unlike this audit, it is computed in
full at the **older, pre-move** pair `(a0=1116021, a0+1=1116022)`
(`agreement_interval.one_step_target`); the packet's `v13_raw_moved_pair`
addendum only spot-checks a *single* rung of the **current** moved pair
`(1116023, 1116024)` (`tight_rung_at_a1p`: profile `Gceil`, `c=2048`,
margin `-0.3938` bits, `TIGHT`, non-firing). That one spot-checked rung
being reported `TIGHT` (not comfortably clear, as KB's analogous spot-check
was: KB's `tight_rung_at_a1p` is `null`) is an independent, *lower-side*
corroboration of the same qualitative fact this audit's *upper-side* ledger
establishes quantitatively: **the M31 moved pair is precarious in a way the
KB moved pair is not.** This audit does **not modify**
`m31_mca_v1.packet.json` -- the new ledger ships as a sibling file,
`m31_mca_conjq_rung_audit_v1.json`, key `conjQ_rung_audit`, exactly mirroring
the KB packet-extension convention.

| | Audit 1 (`m31_mca_v1.packet.json` `.rung_margin_audit`) | This audit (`conjQ_rung_audit`) |
|---|---|---|
| side | lower / periodic FLOOR mass | upper / `conj:Q` max-FIBER |
| pair audited (full) | OLD pre-move pair `(1116021, 1116022)`, all 21 rungs x 4 profiles | CURRENT moved pair `(1116023, 1116024)`, full `j=0..21` |
| pair audited (current moved pair) | single spot-checked rung only (`tight_rung_at_a1p`) | full ledger |
| "exceeds" means | periodic refutation (edge moves) | pessimistic ladder exceeds `K_raw` (Sec. 5/7 -- NOT itself a refutation) |
| verdict | `GREEN` at the old pair; `TIGHT` (non-firing) at the one spot-checked current-pair rung | `NOT GREEN`: pessimistic ladder exceeds `K_raw` by `~4.66x` |

Neither audit exhibits an actual **firing** or **proved-exceeded** bound at
the current moved pair; the adjacent `(1116023, 1116024)` conjecture is
therefore **not falsified** by anything in this repo, and the edge does
**not** (yet, on this evidence) move -- but neither is it "cleanly `GREEN`"
the way the KB row is. It is `TIGHT`/open, consistent across both the
lower-side spot-check and this upper-side full ledger.

---

## 9. Verifier contract

`experimental/scripts/verify_m31_mca_conjq_rung_audit.py` is zero-arg,
stdlib-only, deterministic, and supports `--tamper-selftest`. Five gates,
mirroring the KB verifier exactly:

- **gate i** -- recomputes the entire `j=0..21` table (Sec. 4) from raw
  constants with exact big-integer arithmetic and diffs every field against
  the shipped JSON, **including the `EXCEEDS` verdicts at `j=1,2,3`** (this
  verifier does not assume, the way an incautious port of the KB verifier
  might, that no rung ever exceeds -- it checks the *actual*, signed margin
  and the *actual* verdict category against the shipped data, whichever way
  they come out).
- **gate ii** -- binomial/moment identity spot checks: `w_j = floor(w/2^j)`;
  the divisibility chain `2^s | m_safe` for `s=0..3`; `v2(m_safe) == 3`
  exactly (**not** `4`).
- **gate iii** -- exhaustive toy-validation replay of identity `(D)` on the
  same 4 toy rows as the KB verifier (including the `F_17` witness
  `M={1,2,4,10}`, `z=(0,2)`, and the genuine non-trivial coset row over
  `F_97`), run fresh for this packet -- since the identity is domain-generic,
  reusing KB's toy suite validates the same abstract mechanism.
- **gate iv** -- the relaxation-failure check of Sec. 2, on the same toy row.
- **gate v** -- conservative-rounding consistency: `charge=42`,
  `residual=-33`, `charge + residual == K_raw` (`=9`), and `any rung exceeds
  budget == True` (the opposite of KB's `False`, and exactly what this
  packet's own honest arithmetic requires).

Expected runtime under 90s; expected exit code `0`. A nonzero exit code
means a genuine mismatch, not a judgment about `conj:Q` itself -- this
verifier never gates on whether `conj:Q` is true, only on whether this PR's
own arithmetic is internally consistent and matches its shipped JSON
(whether that arithmetic happens to spell `GREEN` or not).

---

## Refs

- `experimental/notes/thresholds/cap25_v13_qfin_rung_audit.md` -- the KB-MCA
  sibling (PR #361), whose section structure this note mirrors exactly;
  same compiler, different (much tighter) row constants.
- `experimental/cap25_cap_v13_raw.tex` -- `thm:stabilizer-partition`,
  `thm:fiber-descent`, `cor:periodic-support-count`, `lem:cheb-fibers`,
  `lem:torus-fibers`, `sec:circle-geometry`: the paper-level source proving
  the Chebyshev case's parallel treatment to the multiplicative case that
  this note relies on in Sec. 1-2.
- `experimental/grande_finale.tex` -- `conj:Q` (`\label{conj:Q}`), `conj:BC`
  (`\label{conj:BC}`), `conj:SP` (`\label{conj:SP}`), `rem:proved-q-part`,
  `prop:mode-null-false`, and the Work-Plan "Rung audit" paragraph this note
  executes (row-agnostic; shared with the KB sibling).
- `experimental/rs_mca_proximity_prize_status.md` -- row authority for the
  moved v13 raw pair `(1116023, 1116024)` and its `3.3`-bit fail margin;
  the source of the "demand exact extremality" remark this audit confirms
  quantitatively.
- `experimental/scripts/'towards v13'/cap25_v13_raw_moved_frontier_checks.py`
  -- the exact `(p', ext, t, m_unsafe)` row tuple for M31-MCA.
- `experimental/data/certificates/frontier-adjacent/m31_mca_v1.packet.json`
  -- the sibling packet (not modified by this PR); its `.rung_margin_audit`
  is the distinct, older-pair, lower-side periodic-floor audit (Sec. 8).
- `experimental/data/certificates/frontier-adjacent/m31_mca_conjq_rung_audit_v1.json`
  -- this audit's data, key `conjQ_rung_audit`.
- `experimental/scripts/verify_m31_mca_conjq_rung_audit.py` -- this audit's
  verifier (Sec. 9).
