# CAP25 v13 BC L4: interior excess-1 chart discharges to row-sharp Q at depth w+1

Status: `PROVED` (reformulation A1–A4, saturation B1–B2, first-match classification,
Theorem `[interior chart decomposition]`, Corollary `[discharge to depth-(w+1) Q]`, rigidity/collision
ceilings C2–C3, floors as stated) / `EXPERIMENTAL` (heuristic ray/census sizes) / `AUDIT` (fixture
consistency with the integrated #369 ladder and #361 rung audit). Task **B1** (`agents.md` @ `7bd50ca`,
"Finite BC chart-decomposition audit") / `prob:saturated-bc` (`experimental/grande_finale.tex`, resolution
type (b)) / Good-first-PR #3.

**B1 answer (one sentence).** At the first interior profile the residual chart of the planted interior
family `U_{z*}` is neither a moving-root pencil nor a new obstruction — it is `|B|` curve-restricted copies
of the depth-`(w+1)` prefix-fiber problem, so it is discharged by row-sharp Q (list route) at the same
agreement `m` (the general-line chart at this profile is `§8` OPEN item 3, not claimed here).

Concretely: the excess-1 interior split-pencil ray count decomposes exactly as
`#valid T = Σ_{s∈B} |Fib_{w+1}(θ(s))|` along an explicit polynomial curve `θ`, and
`#rays ≤ #valid T ≤ |B|·max_z |Fib_{w+1}(z)|`. This is resolution type (b) of `prob:saturated-bc`
(the chart is explicitly split; the charge goes to Q), not a higher-dimensional pencil and not an
independent BC obstruction. The only open input is the depth-`(w+1)` max-fiber bound — which is
`prob:row-sharp-q` one dimension down, at the same agreement.

---

## 1. Object and fixture (`AUDIT` / `PROVED`)

The L4 fixture is the scale-16 quotient of the KoalaBear-MCA row, pinned by the integrated
ladder note `experimental/notes/thresholds/cap25_v13_bc_l4_base_floor_ladder.md` (#369) and its
certificate `experimental/data/certificates/frontier-adjacent/kb_mca_bc_l4_base_floor_ladder_v1.json`
(cited, not re-pinned):

```
n = |D| = 131072 = 2^17        K = 65537 = 2^16+1   (MCA threshold = k+1)
k = K-1 = 65536                (base RS dimension; pole-line codewords have deg < k)
m = 69753  (odd)               w = m - K = 4216      (row prefix depth on m-subsets)
p = |B| = 2^31 - 2^24 + 1 = 2130706433   (KoalaBear prime, log2 p = 30.988684687)
q = |F| = p^6                  D ⊆ B a multiplicative coset,  Λ_D = ℓ_D = X^n - β,  β ∈ B
boundary profile   d1 = w+1 = 4217   (delegated to conj:Q, excluded from BC)
first BC interior  d1 = w+2 = 4218,   m' = K-1+d1 = 69754 = m+1,   excess e = m'-m = 1
```

**Planted interior word.** `U_{z*}(X) = X^{m'} + Σ_{h=1}^{d1-1} z*_h X^{m'-h}`, `z* ∈ B^{d1-1} = B^{4217}`,
a base-field prefix with no coefficient below `X^K`, evaluated on `D` (the `prop:base-field-floor` witness
family). Pole `α ∈ F∖(D∪B)`, received pole line `f_α = U_{z*}/(X-α)`, `g_α = -1/(X-α)`, line
`U_Z = f_α + Z g_α`. Explaining MCA code `C = RS[F,D,k]`, `k = K-1` (codewords of degree `< k`).

Because `m` is odd and `n = 2^17`, `gcd(m,n) = 1`: the row is 100% subset-primitive (no 2-adic quotient
sub-stratum) and every witness support below is aperiodic (`thm:fiber-to-slope`, final clause).

**No-`B*` fence (`AUDIT`).** L4 is a flatness rung: there is **no `B*` budget** here, and this packet makes
**no** census-vs-budget comparison. The deliverable is the per-line slope/ray structure. Comparing a
support census to `B*` at L4 is a category error (support-census floors are not bad-slope counts and are not
ledger payments — the #369 orientation columns are labelled `orientation_only`); we do not make it.

**Fixture consistency (`AUDIT`, PROVED byte-identical).** The planted stratum recovers the #369 ladder row
`d1=4218` exactly (§3), the interior pigeonhole floor equals the boundary-Q rung `a_4 = 23.139009074` of the
integrated rung audit `cap25_v13_qfin_rung_audit.md` (#361) and the #369 boundary row `23.139009` (§5), and
the planted `m'`-subset density `-8.035617` matches the #369 `d1=4218` prefix-average column.

The `RS[K]`-word census of `U_{z*}` equals, at every pole, the per-line support set of the pole line for the
row's own base MCA code `RS[k]`, `k = K-1` (Lemma A1 + the convention pin §6 + toy2 check 2). This is the
identity that keeps the count one dimension below the MCA row.

---

## 2. Exact reformulation (`PROVED`; Lemmas A1–A4, general `e`, specialised to `e=1`)

Throughout `ℓ_S(X) = Π_{x∈S}(X-x)` is the monic locator, `a_i(T)` is the coefficient of `X^{m-i}` in `ℓ_T`
(so `a_0=1`, `a_1(T) = -Σ_{x∈T}x ∈ B`), and `rt_D(Ψ) = #{x∈D : Ψ(x)=0}` counts **distinct** `D`-roots.
Proofs are the `grande_finale` instances cited; the statements below are what the packet uses.

**Lemma A1 (support+slope ↔ `(T,R)` bijection; prefix condition `(★)`) — `PROVED`.**
For `α ∈ F∖(D∪B)` there is a bijection
```
{ (T,ζ) : T⊆D, |T|=m, (f_α+ζ g_α)|_T explained by some c∈C }
   ⟷  { (T,R) : T⊆D, |T|=m, R monic, deg R = e, deg(U_{z*} - ℓ_T·R) ≤ K-1 }
```
via `ζ = U_{z*}(α) - ℓ_T(α)R(α)` and inversely `R = (U_{z*}-ζ-(X-α)c)/ℓ_T`. The degree condition is
equivalent to the **prefix condition**
```
(★)  the top d1-1 coefficients of ℓ_T·R (those of X^{m'-1},…,X^{m'-(d1-1)}=X^K) equal (z*_1,…,z*_{d1-1}).
```
[Instance of `prop:pole-line` (far clause) + `prop:prefix-witness`. The sole correction to the PI sketch is
the degree bound: `deg(U_{z*}-ℓ_T R) ≤ K-1`, **not** `≤ K`; this `K-1` is forced by the pole-line code being
`RS[F,D,k]` with `k = K-1`. The equation count `d1-1` is unchanged.]

**Lemma A2 (one slope per support) — `PROVED`** (instance of `prop:slope-elimination`).
For fixed `T` there is at most one valid `R` (hence one `ζ`): if `ℓ_T R` and `ℓ_T R'` share prefix `z*` then
`deg ℓ_T(R-R') ≤ m'-(d1-1)-1 = K-1 < m = deg ℓ_T`, forcing `R=R'`. At `e=1` the first prefix equation gives
the unique candidate `r = r(T) := a_1(T) - z*_1`, and `T` is valid iff the remaining `w` equations hold.
`g_α` is never explained on `≥ k+1 = K` points (`prop:pole-line` far clause), so no `T` of size `m ≥ K` is a
common support.

**Lemma A3 (line-rays ↔ valid `Ψ`; `r∈B` at `e=1`) — `PROVED`.**
A **valid `Ψ`** is a monic `Ψ∈F[X]` of degree `m'` with prefix `z*` and `rt_D(Ψ) ≥ m`. Then
`{ line rays (ζ,c) at agreement ≥ m } ⟷ { valid Ψ }` via `Ψ = ℓ_T R`, `ζ = U_{z*}(α)-Ψ(α)`,
`c = (U_{z*}-Ψ-ζ)/(X-α)` with `deg c < k`. At `e=1`, `r = a_1(T)-z*_1 ∈ B` (both terms in `B`), so
`R = X-r ∈ B[X]` and **every valid `Ψ = ℓ_T(X-r) ∈ B[X]` is defined over the base field `B`**.

**Lemma A4 (exact equation bookkeeping) — `PROVED`.**
With `ℓ_T = Σ a_i X^{m-i}` and `R = Σ ρ_l X^{e-l}`, the coefficient of `X^{m'-j}` in `Ψ=ℓ_T R` is
`Σ_{l=0}^{min(j,e)} ρ_l a_{j-l}`. The `d1-1 = w+e` prefix equations split as: `j=1,…,e` solve triangularly
for `R`'s `e` coefficients (fixing `R` as a polynomial in `T`); `j=e+1,…,w+e` are `w` equations on `T`
(reaching `a_{w+e}(T)`). At `e=1`: `a_1-r=z*_1` fixes `r`, and `a_j - r a_{j-1} = z*_j` (`j=2,…,w+1`) are the
**twisted depth-`w` prefix map** on `T`. So `d1-1 = w+1 = 4217` equations: `1` fixes `r`, `w = 4216`
constrain `T`.

**Two-route agreement `B = X-r ≡ R` (`PROVED`).** The independent lattice route (D2) builds the interpolation
module `M_{U_{z*}}` with explicit weak-Popov `B`-basis `g₁=(1,U_{z*})`, `g₂=(S,-T)` from
`X^n-β = U_{z*}S + T`, profile `(d1,d2) = (4218, 61318)`, `d1+d2 = n-K+1 = 65536` (`prop:lattice-split`,
`thm:near-rational(ii)`). Every size-`m` support is a pencil member `A g₁ + B g₂`, and the degree-1 tail
`B = X-r` is forced (`deg A ≤ ω-d1 = 57101 < deg S = 61318`). Cross-multiplying the census identity
`N = Wc` gives `W(U_{z*}-c) = B·Λ_D = B·W ℓ_T`, hence `U_{z*}-c = ℓ_T·B`, i.e. **`B = X-r` is exactly the
route-D1 residual factor `R`**, with `r = a_1(T)-z*_1 ∈ B`. The twisted-fiber route and the lattice route
agree at the structural level; toy2 checks 1 and 2 confirm `Ψ_{closed} = ℓ_T(X-r) = U_{z*}-c` for every valid
`T`, and `r` derived by factoring the independent Lagrange interpolant matches `a_1(T)-z*_1` on all
`8008 + 11440` toy supports (zero mismatches).

---

## 3. Saturation strata and the `M_B(4218)` recovery (`PROVED`; `thm:saturation` instance)

Per valid `Ψ` with ray `(ζ,c)`, the agreement set is exactly `rt_D(Ψ)`, so
`#{ size-m supports of this ray } = C(rt_D(Ψ), m)` (`prop:line-ray-saturation` / `thm:saturation` read one
slope at a time). At `e=1`, `R = X-r`, `r∈B`, giving three strata by the location of `r`:

| stratum | condition | `rt_D(Ψ)` | supports/ray = `C(rt_D(Ψ),m)` |
|---|---|---:|---:|
| **planted** | `r ∈ D∖T` | `m+1 = 69754` | `C(m+1,m) = m+1 = 69754` |
| primitive  | `r ∈ B∖D` | `m` | `1` |
| degenerate | `r ∈ T` (double root) | `m` | `1` |

The planted stratum is the base-field-floor mechanism (`prop:base-field-floor`): planted rays are the
prefix-`z*` `(m+1)`-subsets `M' = T∪{r} ⊆ D`, and `Σ C(m+1,m)` over them recovers the fixture floor
```
M_B(4218) = C(m',m)·⌈C(n,m')/p^{d1-1}⌉ = 69754·1 = 69754      (planted density -8.035617 < 0 ⇒ ⌈·⌉=1),
```
**byte-identical to the #369 ladder row `d1=4218`**. Strata primitive+degenerate are the genuinely interior
rays invisible to the base-field census; `r` ranges over `B` and only the `n/p = 2^{-14}` fraction lands in
`D`, so the primitive stratum carries essentially all rays. This is the concrete `cor:raw-bc-fails` instance:
the raw census inflates planted rays by `m+1`, but the MCA slope count charges each ray once. The exact
per-line identity is
```
Σ_{z∈E} Cen(U_z;m) = (m+1)·(#planted rays) + (#primitive rays) + (#degenerate rays) = Σ_{valid Ψ} C(rt_D(Ψ),m).
```

---

## 4. First-match classification (`PROVED`, load-bearing)

The planted interior pole line, `α∉B`, survives every already-paid ledger cell in `grande_finale`'s
first-match order and lands exactly in the residual `prob:saturated-bc` cell. Each row names the label that
pays (or would pay) the check.

| # | check | verdict | paying label |
|---|---|---|---|
| c.1 | not tangent / common-support | `g_α` explained on no `≥ K` points; pole far from every clause | `prop:pole-line` (far), `prop:exact-tangent-cell`, `thm:gf-mca-from-ca` |
| c.2 | not near-rational | `d1(U_{z*}) = w+2 > w` ⇒ `U_{z*}` not within Hamming `w` of any codeword; `g_α` agrees with none on `≥ K = 65537 < n-2w = 122640` | `thm:near-rational(i)`, `cor:near-rational-line` |
| c.3 | not boundary-Q | `d1 = w+2 = 4218 ≠ w+1 = 4217`; first genuine interior profile, no prefix-fiber double count | `prop:boundary-q` |
| c.4 | not quotient / no firing rung | `m` odd, `n = 2^17` ⇒ `gcd(m,n)=1` ⇒ every support aperiodic; no dyadic rung | `thm:coeff-quotient-extract`, `cor:primitive-coeff-exclusion` |
| c.5 | escapes subfield confinement | the **line** has no `B`-valued scalar multiple: `g_α(x)/g_α(y)=ρ≠1 ⇒ α∈B`, contra `α∉B` | `thm:subfield-confinement`, `prop:rank-one-floor` (scalar-confinement) |
| c.6 | lands in residual cell | survives c.1–c.5 ⇒ the primitive interior split-pencil / saturated line-ray cell | `prob:saturated-bc`; extension is a target not a payment (`prop:extension-cell-target`, `rem:extension-target-nonclaim`) |

**Honest scope on c.5 (important; `PROVED` restricted to the line).** What is proved is the **line-level**
scalar-confinement — no `λ∈F^×` makes `λ g_α` base-valued — which is exactly what makes
`thm:subfield-confinement` not pay the line. This is **not** a per-slope claim: an individual bad slope
`ζ = c(α)` with `c∈B[X]`, `α∉B` need **not** lie in `F∖B` (a base-field polynomial at an
extension point can be base-valued, e.g. an even polynomial at a pole with `α²∈B`). The toy confirms this
distinction: at the even planted word `U = X^{m'}` over the negation-closed `D` (row B, `z*=0`), **all**
rays have base-valued `ζ` (`num_zeta_extension_valued = 0`), whereas the `m`-even non-monomial row A has
every slope value extension-valued (all `21` per-support values; `3` distinct rays). The PROVED extension statement is scalar-confinement of the line; per-slope
membership is `F`-generic but not guaranteed, and the packet does not assert it.

---

## 5. Headline: the interior chart decomposition and its discharge to depth-`(w+1)` Q

### Theorem [interior chart decomposition] — `PROVED`

*Let `U_{z*}` be the planted interior word at the first interior profile (`e=1`, `d1=w+2`), and let*
```
Θ_w(T) := ( a_2 - r a_1, a_3 - r a_2, …, a_{w+1} - r a_w ),   r = a_1(T) - z*_1,
```
*the twisted depth-`w` prefix map `binom(D,m) → B^w`. Define `φ_1(s)=s` and
`φ_j(s) = z*_j + (s - z*_1)φ_{j-1}(s)` for `j=2,…,w+1`, and `θ(s) = (s, φ_2(s),…,φ_{w+1}(s)) ∈ B^{w+1}`.
Then the twisted fiber decomposes as a sum over the base field of standard depth-`(w+1)` prefix fibers along
the explicit polynomial curve `θ`:*
```
#{valid T} = |{ T∈binom(D,m) : Θ_w(T) = (z*_2,…,z*_{w+1}) }| = Σ_{s∈B} |Fib_{w+1}(θ(s))|,
```
*where `Fib_{w+1}(z) = { T∈binom(D,m) : (a_1(T),…,a_{w+1}(T)) = z }` is the ordinary depth-`(w+1)` prefix
fiber of the base MCA code `C = RS[F,D,k]`, `k = K-1`, at agreement `m`.*

*Proof.* By Lemma A2, `#rays ≤ #{valid T}` and each valid `T` is `Θ_w(T) = (z*_2,…,z*_{w+1})`, the `w`
residual equations of Lemma A4 with `r = r(T) = a_1(T)-z*_1` substituted. Partition `{valid T}` by the value
`s = a_1(T) ∈ B`. For fixed `s`, `r = s - z*_1` is fixed, and the `w` equations `a_j - r a_{j-1} = z*_j`
(`j=2,…,w+1`) pin `a_2,…,a_{w+1}` **recursively**: `a_2 = z*_2 + r a_1 = z*_2 + (s-z*_1)s = φ_2(s)`, and
inductively `a_j = z*_j + (s-z*_1)a_{j-1} = z*_j + (s-z*_1)φ_{j-1}(s) = φ_j(s)`. Together with `a_1 = s = φ_1(s)`
this is exactly the depth-`(w+1)` prefix condition `(a_1,…,a_{w+1}) = θ(s)`, i.e. `T∈Fib_{w+1}(θ(s))`.
Conversely every `T∈Fib_{w+1}(θ(s))` has `a_1 = s`, `r = s-z*_1`, and `a_j = φ_j(s)`, so
`a_j - r a_{j-1} = φ_j(s) - (s-z*_1)φ_{j-1}(s) = z*_j`, i.e. `Θ_w(T) = (z*_2,…,z*_{w+1})` and `T` is valid.
Summing the partition over `s∈B` gives the identity. ∎

**Reading.** A depth-`(w+1)` fiber `Fib_{w+1}(z)` is the plain list-decoding fiber of the base MCA code
`C = RS[F,D,k]` itself (`prop:prefix-witness` with `k = m-(w+1)`), at agreement `m`. The MCA row uses the
one-higher threshold `K = k+1` at depth `w = m-K`; the inner object sits at depth `w+1 = m-k` on the base
code. So the excess-1 interior ray count is a `p`-fold, curve-restricted sum of the list-route Q object of
the base code, at the same agreement `m` — row-sharp Q for the "`K-1` row." Heuristically each fiber is
`C(n,m)/p^{w+1}`, and `p·C(n,m)/p^{w+1} = C(n,m)/p^w = 2^{23.14}`: the effective depth is `w`, but the
realized structure is `p` slices of depth `w+1`. The map `Θ_w` reads one coefficient (`a_{w+1}`) beyond the
standard depth-`w` map, so this is **not** an affine reparametrization of a single depth-`w` fiber; it is the
`p`-slice curve-sum.

### Corollary [discharge to row-sharp Q at depth `w+1`] — `PROVED` (reduction)

*For the planted interior family of the Theorem,*
```
#rays  ≤  #{valid T}  =  Σ_{s∈B} |Fib_{w+1}(θ(s))|  ≤  |B| · max_z |Fib_{w+1}(z)|.
```
*Consequently any row-sharp depth-`(w+1)` max-fiber bound — the list route, dimension `k = K-1`, agreement
`m`, i.e. `prob:row-sharp-q` at depth `w+1` —*
```
max_z |Fib_{w+1}(z)| ≤ R_{w+1}·C(n,m)·p^{-(w+1)}
```
*immediately yields `#rays ≤ R_{w+1}·C(n,m)·p^{-w}` for this chart. Therefore the first interior BC chart of
the planted family is discharged by the depth-`(w+1)` row-sharp-Q max-fiber theorem, up to the explicit
factor `|B| = p` and the curve restriction `{θ(s)}` (which can only lower the count). It is resolution
type (b) of `prob:saturated-bc`: an explicitly split chart whose charge goes to Q, not a new obstruction and
not a one-parameter moving-root pencil.*

*Proof.* `#rays ≤ #{valid T}` is Lemma A2 (each ray has ≥1 representative `T`, each valid `T` determines its
ray). The equality is the Theorem. Bounding each of the `|B| = p` curve terms by the global maximum
`max_z |Fib_{w+1}(z)|` gives the middle inequality. Substituting the hypothesised max-fiber bound and
`p·p^{-(w+1)} = p^{-w}` gives the last. The statement is about the planted interior family `U_{z*}`
(`prop:base-field-floor` witness), `α∉B`; it makes no claim about non-planted words or other profiles. ∎

**General `e` (remark, `PROVED`).** For excess `e`, the same argument with `s∈B^e` gives
`#{valid T} = Σ_{s∈B^e} |Fib_{w+e}(θ(s))|`, a sum of `p^e` depth-`(w+e)` fibers over an `e`-dimensional
parametrized curve in `B^{w+e}`; the `e` prefix equations solve triangularly for `R`, the `w` remaining
constrain `T`. Only `e=1` is instantiated numerically here.

---

## 6. Unconditional ceilings and floors (`PROVED` as stated; heuristics `EXPERIMENTAL`)

Ray rigidity (all `e`): if `Ψ≠Ψ'` are valid with representatives `T,T'`, both are monic degree `m'` with
prefix `z*`, so `deg(Ψ-Ψ') ≤ m'-(w+e)-1 = K-1`; vanishing on `T∩T'` forces `|T∩T'| ≤ K-1`, hence
`|T∖T'| ≥ m-(K-1) = w+1` (`prop:prefix-rigidity` / `thm:q-proper` analogue). The collision cap is the same
degree bound: two rays give the same slope iff `(Ψ-Ψ')(α)=0`, at most `K-1` poles per pair.

| quantity | formula | exact `log2` | label |
|---|---|---:|---|
| ray/census heuristic | `C(n,m)/p^w` | `23.139009` (= `a_4`, #361 / #369 boundary) | `EXPERIMENTAL` |
| **pigeonhole floor** `∃z*` | `⌈C(n,m)/p^w⌉` | `23.139009` (ceil differs from `a_4` below print precision) | `PROVED` |
| rigorous ray floor | `≥ #valid T /(m+1)` | `7.05` | `PROVED` |
| conservative slope floor | best pole keeps `≥ ½` | `6.05` | `PROVED` |
| planted per-ray mult. | `C(m+1,m) = m+1` | `69754 = 2^{16.089988}` | `PROVED` |
| planted density | `C(n,m')/p^{d1-1}` | `-8.035617` (⌈·⌉=1) | `AUDIT` |
| base-field floor `M_B(4218)` | `C(m',m)·⌈·⌉` | `69754` | `PROVED` |
| **packing ceiling** (full ball `V_t`, `t=⌊w/2⌋=2108`) | `C(n,m)/V_t` | `103810.24` | `PROVED` |
| packing ceiling (one-term denom.) | `C(n,m)/[C(m,t)C(n-m,t)]` | `103810.24` | `PROVED` |
| anticode ceiling | `C(n,m)/C(n-m+w,w)` | `108108.04` | `PROVED` |
| depth-`(w+1)` reduction+packing | `|B|·C(n,m)/V_{t'}` | `103841.23` | `PROVED` |
| collision cap per pair | `K-1` | `65536` | `PROVED` |
| distinct-slope threshold | `(q-p)/(K-1)+1` | `169.93` | `PROVED` |
| collisions at heuristic `N` | `C(N,2)(K-1)/(q-p)` | `-124.65` (negligible) | `PROVED` |
| gap: packing − heuristic | — | `≈ 103787` bits | `PROVED` |

**Floors.** By pigeonhole over `B^{d1-1}` some `z*` has `#{valid T} ≥ ⌈C(n,m)/p^w⌉ = 2^{23.139009}`
(Theorem numerator, one dimension down). Each `e=1` ray has `≤ m+1` supports, so `#rays ≥ 2^{7.05}`
(rigorous). With the `K-1` collision cap (C3) the best pole keeps `≥ ½` of the rays as distinct slopes
(line-level `α∉B` means the line is not paid by `thm:subfield-confinement`, per c.5): `≥ 2^{6.05}` distinct
MCA-bad finite slopes (rigorous, stated conservatively). These slopes are **generically** `F∖B`-valued, but
per the §4 honest scope the per-slope `F∖B` membership is **not** asserted (the even-word toy row B has zero
extension-valued slopes); the rigorous floor is on the count of distinct MCA-bad slopes, not on how many are
extension-valued. Because the planted stratum has density `2^{-8.04} ≪ 1`, heuristically
`#rays ≈ #{valid T} ≈ 2^{23.14}` (primitive stratum dominates; `EXPERIMENTAL`), with collisions
`≈ 2^{-124.65}` (negligible). The direct `(T,r)`-rigidity ceiling `2^{103810.24}` beats the reduction route
`2^{103841.23}` by `≈ 31 = log2 p` bits (the reduction pays the `|B|` factor); use the direct ceiling for an
unconditional bound.

**Packing-bound correction (`PROVED`; flagged).** The exact Johnson-ball ceiling is `C(n,m)/V_t = 2^{103810.24}`
with `V_t = Σ_{i=0}^{t} C(m,i)C(n-m,i)`, `t=⌊w/2⌋=2108`. Because the terms increase steeply
(`term(t)/term(t-1) ≈ 901`), `V_t` is dominated by its top term (`V_t/C(m,t)C(n-m,t) = 1.00111`), so the
full-ball and one-term denominators coincide at `2^{103810.24}` (they differ only in the 4th decimal:
`103810.2369` vs `103810.2385`). An earlier draft (route-D1 `numbers.py`, and the synthesis brief) quoted
`2^{103799.20}` for the "full ball"; that figure replaces `V_t` by `(t+1)·C(m,t)C(n-m,t)`, which
**over-counts** the ball by a factor `2106×` and therefore under-states the ceiling **below** the true
`C(n,m)/V_t` — it is not a valid upper bound and is dropped. The qualitative conclusion is unchanged: the
gap over the heuristic is `≈ 103787` bits (this is the value the D1 note already used for its gap), the same
qualitative gap as `prop:proper-q-gap`; packing is real but far too weak. Route D1 does not close this gap; it
identifies it with the depth-`(w+1)` Q gap.

---

## 7. Convention pin (`PROVED` at toy scale; `AUDIT`)

The packet's object is the **word census** of `U_{z*}` at dimension `K` (supports `T` with `U_{z*}|_T`
explained by a `deg < K` codeword) — equivalently the pole line for the base code `RS[k]`, `k = K-1`
(quotient degree `< K-1`, total `(ζ,P)`-space dimension `(K-1)+1 = K`, matching the direct `deg < K` test).
This is the object counted at the heuristic `2^{23.14}` (an `EXPERIMENTAL` size, per §6; the convention
identity in this section — which count is the MCA numerator — is what is `PROVED`/`AUDIT`, not the size).

One dimension up, the pole line for `RS[K]` (quotient degree `< K`, the prior-run object) frees the
degree-`K` coefficient — the simple pole absorbs it via `U_{z*}-ℓ_T(X-r) = ζ+(X-α)P` — so it constrains only
`w-1` coefficients of `T` and is **exactly `p×` larger** (depth `w-1`, `2^{54.13}` at L4). Word-census
supports are a subset of line-for-`RS[K]` supports. Pin this to prevent double-counting; it is why naive
"per-line" heuristics disagree by `p`.

Verified exactly:
- **`F_7` instance (`PROVED`).** `B=F_7`, `D=F_7^*` (`n=6`, `K=2`, `m=4`, `w=2`, `m'=5`, `d1=4`): averaging
  exact fiber sizes over all prefixes gives census `= 15/7^2` and pole-for-`RS[K]` `= 15/7`, ratio **exactly
  `p = 7`**, with census supports `⊆` pole supports on every prefix (D2 `toy_check.py`).
- **Rows A/B (`PROVED`).** `line-for-RS[k] == word census` at every tested pole (toy2 check 2:
  row A `Cen = 21`, row B `Cen = 48`, supports and rays equal, `ζ`-formula exact); and
  `word census ⊂ line-for-RS[K]` (toy2 check 10, subset holds at every pole). Toy-scale count **ratios**
  `old/new` are noisy around `p` (row A `5.0`, row B `3.0`, from small heaviest fibers, not the average); the
  exact claim is the **subset property** plus the `F_7` exact-`p` ratio, not a per-row ratio equal to `p`.

At L4 the line-for-`RS[K]` heuristic count is `C(n,m)/p^{w-1} = 2^{54.127694} = p·2^{23.14}` (`EXPERIMENTAL`
size; the exact `p×` ratio to the ray/census count is the `PROVED`/`AUDIT` content). Route-D2 §4c had flagged
`2^{54.13}` as the pole-line slope number; the corrected convention resolves it: the **ray/census** count
(the MCA numerator) is `2^{23.14}` (line-for-`RS[k]`), and `2^{54.13}` is the `RS[K]` line one dimension up,
which the packet does **not** use for the ray count.

---

## 8. What remains OPEN

1. The depth-`(w+1)` max-fiber bound itself, `max_z |Fib_{w+1}(z)| ≤ R_{w+1}C(n,m)p^{-(w+1)}` — this **is**
   `prob:row-sharp-q` one dimension down. Unconditionally only the packing/anticode ceilings
   (`2^{103810.24}` / `2^{108108.04}`) are available, `≈ 103787` bits above the heuristic. The Corollary
   reduces the interior BC chart to this bound; it does not prove it.
2. Curve equidistribution: whether `Σ_{s∈B}|Fib_{w+1}(θ(s))|` concentrates on heavy prefixes or avoids them
   (`Σ` vs `p·max`) is not controlled. Proving the heuristic `#rays ≈ C(n,m)/p^w` needs an
   equidistribution / second-moment input for depth-`(w+1)` fibers restricted to the curve `{θ(s)}` — a named
   target strictly weaker than full row-sharp Q.
3. The general-line (non-planted-word) chart audit at `d1 = 4218`.
4. Deeper interior profiles `d1 > 4218` (`e ≥ 2`): the same reduction shape is expected via the general-`e`
   statement (`Σ over B^e` of depth-`(w+e)` fibers), not yet instantiated.

**Non-claims.** No claim on `U(1116048) ≤ B*`; no `conj:BC`; no full-chart audit; no bad-slope lower bound
beyond the stated `2^{6.05}` floor.

---

## 9. Replay

```sh
python3 experimental/scripts/verify_bc_l4_interior_chart_to_q.py
python3 experimental/scripts/verify_bc_l4_interior_chart_to_q.py --tamper-selftest
```

The verifier is stdlib-only, zero-arg (exit 0 = PASS, `--tamper-selftest` must report all tampers caught),
recomputes every pinned L4 integer exactly with big-int binomials, and re-runs the self-contained toy
enumeration at rows A (`p=97,n=16,K=4,m=6,w=2,d1=4,m'=7`, `z*=[96,1,96]`) and B (`K=5,m=7,m'=8`, `z*=[0,0,0]`)
from scratch (no scratchpad dependence). Runtime `< 5s`.

---

## 10. Relationship to concurrent work

- **#369** (`cap25_v13_bc_l4_base_floor_ladder`, integrated) — consumed: this packet is the slope/ray
  structure on top of the #369 fixture; the planted stratum recovers the #369 `d1=4218` floor `69754`
  byte-identically, and the interior pigeonhole floor equals the #369 boundary row `23.139009`.
- **#361** rung audit (`cap25_v13_qfin_rung_audit`, integrated) — the `a_4 = 23.139009074` boundary-Q rung is
  the cross-consistency target for the pigeonhole floor (verifier gate G1).
- **#383** (`cap25_v13_saturated_bc_budget_fit`) / **#384** (`cap25_v13_gammar_order_floor`), integrated —
  same `prob:saturated-bc` / row-sharp-Q neighbourhood; no object overlap.
- **#389** (Danny, draft, LQ top-seam at RAW row scale) — no deliverable-file or object contact (only the
  shared `agents-log.md` append, as with every packet); courtesy cross-link only, no coordination needed.
- **#392** (separate same-day reconciliation packet) — independent, no dependency in either direction.
- Steering `b33609d` / `7bd50ca` / `ab7721e` (same-day): B1 is "Show that every residual balanced-core
  split-pencil chart … either is already paid or reduces to a primitive one-parameter pencil covered by the
  moving-root theorem" (`agents.md` @ `7bd50ca`); `prob:saturated-bc` v2 asks to "verify that every remaining
  balanced-core split-pencil chart is … (b) a higher-dimensional coefficient family that is explicitly split
  into such pencils, or else assigned to a separate named residual cell with its own slope … bound." This
  packet answers with type (b): explicit split, charge to depth-`(w+1)` Q.

---

## 11. References (line numbers at base commit `ab7721e`)

`experimental/grande_finale.tex`:
`prop:extension-cell-target` (398), `rem:extension-target-nonclaim` (424), `prop:exact-tangent-cell` (477),
`thm:gf-mca-from-ca` (512), `thm:subfield-confinement` (526), `prop:prefix-witness` (563), `prop:pole-line`
(579), `thm:fiber-to-slope` (612), `prop:prefix-rigidity` (660), `cor:anticode-cap` (694),
`thm:coeff-quotient-extract` (1017), `cor:primitive-coeff-exclusion` (1038), `prop:slope-elimination` (1102),
`prop:lattice-split` (1118), `thm:near-rational` (1132), `cor:near-rational-line` (1163), `prop:boundary-q`
(1257), `prop:base-field-floor` (1276), `prop:rank-one-floor` (1305), `prop:rank-one-distinct-slope-floor`
(1328), `thm:q-proper` (1444), `thm:bc-proper` (1478), `thm:bc-moving-root` (1517), `cor:bc-one-pencil`
(1546), `rem:bc-status-after-moving-root` (1567), `def:saturated-rays` (1574), `thm:saturation` (1593),
`cor:raw-bc-fails` (1625), `prop:line-ray-saturation` (1649), `prop:proper-q-gap` (1740), `def:q-row-atom`
(1825), `prop:bc-not-q` (1902), `prob:row-sharp-q` (1959), `prob:saturated-bc` (1973).

`experimental/cap25_cap_v13_raw.tex`:
`prop:capfr1-lattice-census` (7885), `lem:capfr1-autodiv` (7972), `prop:capfr1-detrep` (7992),
`prop:capg-census-floor` (9728), `prob:capg-split-pencil-B` (9842), `prob:capg-active-BC` (9919).

Fixture (cite, don't re-pin): `experimental/notes/thresholds/cap25_v13_bc_l4_base_floor_ladder.md`,
`experimental/data/certificates/frontier-adjacent/kb_mca_bc_l4_base_floor_ladder_v1.json`.
Cross-consistency: `experimental/notes/thresholds/cap25_v13_qfin_rung_audit.md` (`a_4`, line 216).
