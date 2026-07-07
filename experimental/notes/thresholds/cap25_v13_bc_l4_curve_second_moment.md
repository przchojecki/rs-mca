# CAP25 v13 BC L4: curve second moment = shift-pair ledger on the curve; residual equidistribution law

Status: `PROVED` (Theorem C1 exact curve-`M2` identity; Cauchy–Schwarz conversion; Theorem C2
twist-equivariance + exact average identity; unconditional L4 ceilings; twist dichotomy) /
`EXPERIMENTAL` (measured curve-sum / residual law at four toy rows) /
`CONJECTURAL_WITH_FALSIFIER` (residual curve equidistribution) /
`AUDIT` (fixture consistency with #369 ladder / #361 rung; numerical replay).

Task: the OPEN input named by **open PR #393** (branch `bc-l4-interior-chart-to-q`,
`agents.md` B1 @ `7bd50ca` / `prob:saturated-bc` resolution type (b)) §8 item 2 —
*"curve equidistribution: whether `Σ_{s∈B}|Fib_{w+1}(θ(s))|` concentrates on heavy prefixes or
avoids them … a named target strictly weaker than full row-sharp Q."* This packet is the
second-moment-along-the-curve analysis of exactly that object.

**Self-containment.** #393's note is not yet integrated into `main`; every statement of #393 used
here is restated in §1 and re-derived from scratch by the verifier's toy (no dependence on
unintegrated files).

Verifier: `experimental/scripts/verify_bc_l4_curve_second_moment.py` (stdlib, zero-arg + `--tamper-selftest`).

---

## 1. Object recap (`AUDIT` / `PROVED`, restated from open PR #393)

**L4 fixture** (cited from the integrated ladder note
`experimental/notes/thresholds/cap25_v13_bc_l4_base_floor_ladder.md` (#369) and its certificate
`experimental/data/certificates/frontier-adjacent/kb_mca_bc_l4_base_floor_ladder_v1.json`, not re-pinned):
```
n=|D|=131072=2^17     K=65537=2^16+1    k=K-1=65536    m=69753 (odd)    w=m-K=4216
p=|B|=2^31-2^24+1=2130706433 (log2 p=30.988684687)     d1=w+2=4218    m'=m+1=69754   excess e=1
D ⊆ B a multiplicative coset (μ_n ⊆ B^×, order n=2^17);  planted interior word U_{z*}, z*∈B^{w+1}.
```

**#393 Theorem [interior chart decomposition] (`PROVED`, restated).** Let `ℓ_T=∏_{x∈T}(X−x)`,
`a_i(T)` = coefficient of `X^{m−i}` (`a_0=1`), `Fib_{w+1}(z)={T∈binom(D,m):(a_1,…,a_{w+1})(T)=z}`,
`N_{w+1}(z)=|Fib_{w+1}(z)|`. With `φ_1(s)=s`, `φ_j(s)=z*_j+(s−z*_1)φ_{j−1}(s)` (`j=2,…,w+1`),
`θ(s)=(s,φ_2(s),…,φ_{w+1}(s))∈B^{w+1}`, and the twisted map
`Θ_w(T)=(a_2−r a_1,…,a_{w+1}−r a_w)`, `r=a_1(T)−z*_1`, the excess-1 interior split-pencil ray
count satisfies
```
      S1 := #{valid T} = #{T : Θ_w(T)=(z*_2,…,z*_{w+1})} = Σ_{s∈B} N_{w+1}(θ(s)),      #rays ≤ S1.
```
So `S1` is a `p`-fold, curve-restricted sum of depth-`(w+1)` prefix fibers of the base code
`RS[F,D,k]`, `k=K−1`, at agreement `m`, along the explicit polynomial **curve** `Γ:={θ(s):s∈B}`
(`p` points; `θ` is a graph over its first coordinate). Heuristically each fiber is `C(n,m)/p^{w+1}`
and `p·C(n,m)/p^{w+1}=C(n,m)/p^w=2^{23.139009}` (`EXPERIMENTAL`, `=` the #361 `a_4` rung / #369
boundary row).

**#393 Corollary [discharge to depth-`(w+1)` Q] (`PROVED`, restated).**
`#rays ≤ S1 = Σ_{s∈B} N_{w+1}(θ(s)) ≤ |B|·max_z N_{w+1}(z)`, so a row-sharp depth-`(w+1)` max-fiber
bound `max_z N_{w+1}(z) ≤ R_{w+1}·C(n,m)·p^{−(w+1)}` yields `#rays ≤ R_{w+1}·C(n,m)·p^{−w}`. This is
resolution type (b) of `prob:saturated-bc`: an explicitly split chart whose charge goes to Q.

**No-`B*` fence (`AUDIT`).** L4 is a flatness rung: no `B*` budget, no census-vs-budget comparison
here. This packet studies the second-moment structure of `S1`; it makes no slope-count-vs-budget claim.

Notation: `F̄_{w+1}=C(n,m)/p^{w+1}` (mean depth-`(w+1)` fiber), `F̄_w=C(n,m)/p^w` (the heuristic `S1`).

---

## 2. Theorem C1 — the exact curve second moment (`PROVED`)

Define the **curve second moment** `M2 := Σ_{s∈B} N_{w+1}(θ(s))²`.

**Fact 0 (`PROVED`, #393 Thm).** `V:={valid T}=Φ_{w+1}^{-1}(Γ)=⊔_{s∈B}Fib_{w+1}(θ(s))`, where
`Φ_{w+1}(T)=(a_1,…,a_{w+1})(T)`; the union is disjoint (distinct `s` give distinct `θ(s)`), so
`S1=Σ_{s∈B}N_{w+1}(θ(s))`.

**Proposition C1-1 (`PROVED`).**
```
      M2 = #{ ordered pairs (T,T')∈V×V : a_1(T)=a_1(T') } = Σ_{z∈Γ} N_{w+1}(z)².
```
*Proof.* By Fact 0 the `p` fibers `Fib_{w+1}(θ(s))` are disjoint with union `V` and `θ(s)↦s` is a
bijection `Γ→B`, giving `Σ_s N_{w+1}(θ(s))²=Σ_{z∈Γ}N_{w+1}(z)²`. For the pair count,
`N_{w+1}(θ(s))²` counts ordered `(T,T')` both in `Fib_{w+1}(θ(s))`, i.e. both valid with
`Φ_{w+1}(T)=Φ_{w+1}(T')=θ(s)`, so `a_1(T)=a_1(T')=s`. Conversely for `(T,T')∈V×V` with
`a_1(T)=a_1(T')=s`, Fact 0 gives `Φ_{w+1}(T)=θ(s)=Φ_{w+1}(T')`. **On `V×V` the value `a_1(T)`
determines the whole depth-`(w+1)` prefix `θ(a_1(T))`, so "`a_1` equal" and "full depth-`(w+1)`
prefix equal" coincide on `V×V`** (they do *not* on all of `binom(D,m)²`). ∎

**Off-diagonal encoding.** Split into diagonal (`T=T'∈V`, contributing `S1`) and off-diagonal
(`T≠T'`). Encode off-diagonal ordered pairs by `R=T∩T'`, `A=ℓ_{T∖T'}`, `B=ℓ_{T'∖T}`, `e=|T∖T'|`
(the `prop:second-moment` / `prop:prefix-rigidity` bijection): `ℓ_T=ℓ_R·A`, `ℓ_{T'}=ℓ_R·B`,
`ℓ_T−ℓ_{T'}=ℓ_R(A−B)`, `deg ℓ_R=m−e`.

**Constraint (i) — `deg(A−B)≤e−w−2` (two agreeing routes, `PROVED`).**
`Φ_{w+1}(T)=Φ_{w+1}(T') ⇔ deg(ℓ_T−ℓ_{T'})≤m−w−2 ⇔ deg(A−B)≤(m−w−2)−(m−e)=e−w−2`. So `A≠B` forces
`e≥w+2` and the **top nonzero stratum is `e=w+2`** (`deg(A−B)≤0`, constant shift). The twisted route
agrees: with equal `a_1`, `r_T=r_{T'}=r`, both augmented locators `Ψ_T=ℓ_T(X−r)`, `Ψ_{T'}=ℓ_{T'}(X−r)`
are monic degree `m'=m+1` with the *same* top `w+1` coefficients `z*`, so `deg(Ψ_T−Ψ_{T'})≤m'−(w+1)−1=K−1`;
since `Ψ_T−Ψ_{T'}=(X−r)ℓ_R(A−B)`, `deg(A−B)≤(K−1)−(m−e+1)=e−w−2`. The identity `m'−(w+2)=K−1` is exactly
why the augmented-locator bound `K−1` and the depth-`(w+1)` prefix rigidity `e−w−2` are the same
constraint. (Verifier gate `offdiag_deg<=e-w-2` PASS by enumeration.)

**Constraint (ii) — the curve constraint** `Φ_{w+1}(ℓ_R·A)∈Γ` (`T` valid); depends on `(R,A)`, not `B`.

Set, for `R⊆D`, `|R|=m−e`,
```
  sp^Γ_{w+1}(e;R) := #{ (A,B) : A,B monic degree-e, split over disjoint root sets in D∖R,
                                deg(A−B) ≤ e−w−2,  Φ_{w+1}(ℓ_R·A) ∈ Γ }.
```

> ### Theorem C1 (exact curve second moment) — `PROVED`
> ```
>   M2 = Σ_{s∈B} N_{w+1}(θ(s))²
>      = S1  +  Σ_{e=w+2}^{min(m,n−m)}  Σ_{R⊆D, |R|=m−e}  sp^Γ_{w+1}(e;R).
> ```
> The top nonzero stratum `e=w+2` is exactly the **constant-shift** pairs `A, B=A−c` (`c∈B^×`,
> since `D⊆B`) split over `D∖R`, subject to the curve constraint `Φ_{w+1}(ℓ_R A)∈Γ`.

*Proof.* Proposition C1-1 writes `M2` as the ordered `V×V` count with equal `a_1`; the reduction
`[both valid]∧[a_1 eq] ⇔ [deg(A−B)≤e−w−2]∧[Φ_{w+1}(ℓ_R A)∈Γ]` (constraints (i)+(ii), with "equal
`a_1`" subsumed by (i) on `V×V`) plus the diagonal `S1` gives the identity; the top-stratum shape is
`deg(A−B)≤0`, `A≠B`, coefficients in `B`. ∎ (Verifier gate `M2_three_way_identity`:
`M2_def==M2_pairs==Σ_Γ N²` on fixed seeds, both rows, PASS.)

**The identification (`PROVED`).** Dropping constraint (ii) gives `sp^Γ_{w+1}(e;R)≤sp_{w+1}(e;D∖R)`,
so
```
  M2 = Σ_{z∈Γ}N_{w+1}(z)²  ≤  Σ_{z∈B^{w+1}}N_{w+1}(z)² = C(n,m) + Σ_{e≥w+2}Σ_R sp_{w+1}(e;D∖R)
                                                        (prop:second-moment at depth w+1).
```
So **curve-`M2` is `prop:second-moment` at depth `w+1`, restricted to prefixes on `Γ`**, with the
exact curve-restricted diagonal `S1≪C(n,m)`. Its off-diagonal `M2−S1` is the depth-`(w+1)` shift-pair
(SP) ledger — the `prop:gamma2-ledger` primitive/quotient object, a `prob:saturated-bc`-type object —
**restricted to `Γ`**; the top stratum `e=w+2` is the constant-shift cell of
`prop:top-stratum-quotient-sieve`, one depth down and curve-restricted.

**`thm:q-implies-sp` consequence (`PROVED`).** At depth `w+1`, any max-fiber bound
`max_z N_{w+1}(z)≤κ·F̄_{w+1}` gives `M2=Σ_{z∈Γ}N²≤κ·F̄_{w+1}·S1≤κ²·C(n,m)²/p^{2w+1}=κ²·M2_equi`. So
**depth-`(w+1)` Q ⇒ the needed `M2` bound with `2^C=κ`**, the same reduction target as #393's Corollary.

**Planted stratum spreads (`PROVED`).** For a prefix-`z*` `(m+1)`-subset `M⁺⊆D`, deleting `ρ∈M⁺`
gives a valid `T=M⁺∖{ρ}` with `a_1(T)=z*_1+ρ` varying with `ρ`; the `m+1` supports land in `m+1`
**distinct** `a_1`-fibers of `Γ`, contributing `≤1` each — so a *single* planted `M⁺` cannot by
itself make any curve fiber heavy. But several prefix-`z*` `(m+1)`-subsets (`N^{(m+1)}(z*)≥2`) can
still pile into the same fiber, and the total planted curve-mass is exactly `(m+1)·N^{(m+1)}(z*)`,
which is *not* a priori small (§7): the toy top offenders `A[1,1,1]`/`B[0,0,0]` are the *heaviest*
curve-sums yet have `residual=0` — entirely planted (`N^{(m+1)}=3`, planted `21` / `48`). So
heaviness *beyond the exact planted census* lives in the primitive stratum (`r∉D`); the planted
census itself is the `prop:base-field-floor` object and can be large (see §7 correction).

---

## 3. Cauchy–Schwarz conversion and the exact `M2` bound it needs (`PROVED` / `CONDITIONAL`)

Cauchy–Schwarz on the `p` curve terms:
```
      S1 = Σ_{s∈B} N_{w+1}(θ(s)) ≤ √( p · Σ_{s∈B} N_{w+1}(θ(s))² ) = √(p·M2).      (CS)
```
(Verifier gate `cauchy_schwarz`: row A `21²≤97·39`, row B `48²≤97·144`, PASS; tight iff the curve
fibers are equal.)

**The needed input.** Squaring, `S1²≤p·M2`, so `S1 ≤ 2^C·C(n,m)/p^w` follows from
```
      ┌──────────────────────────────────────────────────────────────────┐
      │  M2 ≤ 2^{2C}·C(n,m)²/p^{2w+1} = 2^{2C}·M2_equi ,  M2_equi=2^{15.289333}  │
      │  ⇔  log2 M2 ≤ 2C + 15.289333.                                     │
      └──────────────────────────────────────────────────────────────────┘
```
Because `M2_equi=C(n,m)²/p^{2w+1}`, this asks `M2` within a factor `2^{2C}` of its **equidistributed**
value. In particular `C=0` (`M2=M2_equi`, CS tight ⇔ all `N_{w+1}(θ(s))` equal) upgrades #393's
**heuristic** `S1=C(n,m)/p^w=2^{23.139}` to a **theorem**.

**`ℓ²` is strictly weaker than `ℓ^∞` max-fiber (`PROVED`).** #393's Corollary needs
`max_z N_{w+1}(z)≤R_{w+1}F̄_{w+1}` (`ℓ^∞`); Route C1 needs only `Σ_{z∈Γ}N_{w+1}(z)²≤2^{2C}M2_equi`
(`ℓ²`). Max-fiber ⇒ the `M2` bound (§2, `thm:q-implies-sp`) but not conversely: a curve-`M2` bound
tolerates individual fibers above the mean as long as their `ℓ²` mass is controlled, whereas
max-fiber forbids *any* fiber above `κ·F̄_{w+1}`. So C1 is the honest minimal input to make #393's
heuristic a theorem, and it sits strictly inside the max-fiber Q neighborhood.

**Hölder generalization (`CONDITIONAL`).** The `r`-th curve moment `M_r=Σ_s N_{w+1}(θ(s))^r` gives
`S1 ≤ p^{1−1/r}M_r^{1/r}`, and `S1≤2^C·C(n,m)/p^w` needs
`log2 M_r + ((w+1)r−1)log2 p ≤ r·log2 C(n,m) + rC` — the exact curve analogue of `thm:moment-q` one
depth down; `r=2` is (CS).

**Scale disambiguation (`AUDIT`).** These curve moments `M_r` are *finite*-order (`r=2,3`),
depth-`(w+1)`, and **restricted to `Γ`**; they are a different object and scale from the base-commit
`thm:logmoment-equivalence` / `def:primitive-logmoment`, which is *asymptotic* — logarithmic order
`r=r(n)→∞` under `w log|B|/r=o(n)`, on the *full* primitive depth-`w` row (all prefixes, not on a
curve). Our route makes no asymptotic-Q claim; consistently, `rem:finite-moment-order` states fixed
`r=2,3` cannot fit the printed adjacent margins, which is exactly §5's below-trivial curve-CS.

---

## 4. Theorem C2 — twist-equivariance and the exact average identity (`PROVED`)

Twist action of `H=μ_n⊆B^×` (order `n=2^17`, `H=D`-stabilizing) on `B^{w+1}`:
`ζ·z=(ζz_1,ζ²z_2,…,ζ^{w+1}z_{w+1})` (`prop:twist-orbit` at depth `w+1`, `N_{w+1}(ζ·z)=N_{w+1}(z)`).

**Proposition C2-1 (twist-equivariance, `PROVED`).** For all `ζ∈H`, `s∈B`:
`θ_{ζ·z*}(ζs)=ζ·θ_{z*}(s)`. *Proof.* Induction: `φ_{1,ζ·z*}(ζs)=ζs`; and
`φ_{j,ζ·z*}(ζs)=ζ^j z*_j+(ζs−ζz*_1)ζ^{j−1}φ_{j−1,z*}(s)=ζ^j φ_{j,z*}(s)`. The residual equations
`a_j−r a_{j−1}=z*_j` are themselves `H`-equivariant (`a_j↦ζ^j a_j`, `r↦ζr`). ∎ (Verifier gate
`twist_equivariance` over all `ζ∈μ_n`, both rows, PASS.)

**Proposition C2-2 (orbit constancy, `PROVED`).** `S(ζ·z*)=S(z*)` for all `ζ∈H`, where
`S(y)=Σ_{s∈B}N_{w+1}(θ_y(s))`. *Proof.* Substitute `s=ζs̃` and apply C2-1 then
`N_{w+1}(ζ·z)=N_{w+1}(z)`. ∎ (Verifier gate `orbit_constancy`, PASS.) The twist stabilizer is
`s(z*)=gcd(n,A(z*))`, `A(z*)={j:z*_j≠0}`; **a generic planted `z*` at L4 has `z*_1≠0` (index 1 odd),
so `s(z*)=1` and a full primitive orbit of size `n=2^17`** (§6).

> ### THE EXACT AVERAGE IDENTITY — `PROVED`
> The map `(y,s)↦θ_y(s)` is exactly **`p`-to-1** onto `B^{w+1}` (for target `z`: `s=z_1` forced,
> `y_1∈B` free, `y_j=z_j−(z_1−y_1)z_{j−1}` determined). Hence
> ```
>   Σ_{y∈B^{w+1}} S(y) = Σ_{y,s} N_{w+1}(θ_y(s)) = p·Σ_z N_{w+1}(z) = p·C(n,m),
>   ⇒  avg_{y∈B^{w+1}} S(y) = p·C(n,m)/p^{w+1} = C(n,m)/p^w  =  the #393 heuristic.
> ```
> **The heuristic `C(n,m)/p^w` is exactly the average curve sum over planted prefixes.**
> Equidistribution asks whether the *specific* planted `z*` sits near this average.

(Verifier: full-enumeration `Σ_y S(y)=p·C(n,m)` on the mini-row `p=13,D=μ_6,m=4`, `195=13·15`, PASS;
plus `p`-to-1 preimage count and `Σ_z N=C(n,m)` on rows A/B.)

**Theorem C2 (twist-orbit amplification, `PROVED`).** With `M_r=Σ_{y}S(y)^r≤p^r·Σ_z N_{w+1}(z)^r`
(AM–GM + the `p`-to-1 identity) and the primitive orbit `(n/s(z*))·S(z*)^r≤M_r`, for every `r≥2`
```
      S(z*) ≤ ( s(z*)/n · M_r )^{1/r} ≤ p·( s(z*)/n )^{1/r}·( Σ_z N_{w+1}(z)^r )^{1/r},
```
i.e. the curve sum normalized by its heuristic obeys the *same* overhead bound as a single
depth-`(w+1)` fiber normalized by *its* heuristic (`prop:q-orbit-moment`), with the twist orbit the
only gain (factor `n^{1/r}`); curve-averaging is not exploited by this route.

**Composite / quotient audit (`PROVED`).** At L4 `m` is odd and `n=2^17`, so `gcd(m,n)=1`: the row is
100% subset-primitive. For generic `z*` with `z*_1≠0`, `s(z*)=gcd(n,A(z*))=1` is **twist-primitive**;
`prop:composite-descend` gives no composite descent of the curve (a quotient direction needs every
nonzero `z*_j` at even index `j`). Any residual quotient shift-pairs are already inside the joint
`thm:sp-proper` ceiling and only tighten the bound.

---

## 5. Unconditional L4 numbers (`PROVED` ceilings; heuristics `EXPERIMENTAL`)

All logs base 2; recomputed by the verifier (exact big-int anchors + lgamma for the 57102-term SP sum,
pinned inside an exact big-int bracket).

| quantity | formula | log2 | label |
|---|---|---:|---|
| `log2 p` | — | 30.988685 | `AUDIT` |
| `log2 C(n,m)` | exact big-int | 130671.433651 | `PROVED` |
| heuristic `S1` | `C(n,m)/p^w` | **23.139009** | `EXPERIMENTAL` (=#361 `a_4` / #369) |
| **`M2_equi`** (target) | `C(n,m)²/p^{2w+1}=S1²/p` | **15.289333** | derived |
| (b1) unconditional `Σ_e T_e` | `thm:sp-proper` depth `w+1`, `T_e=C(n,m−e)C(n−m+e,e)C(n−m,e)` | **261342.87** | `PROVED` |
| dominant stratum | `e*=32632`, `log2 T_{e*}` | 261335.05 | `PROVED` |
| (b2) top stratum | `(p−1)C(n,m−w−2)C(n−m+w+2,w+2)` | **153665.47** | `PROVED` |
| **C1: `S1` via (b1)+CS** | `√(p·Σ_e T_e)` | **130686.93** | `PROVED` |
| C2: twist-amplified `r=2` | `p·(1/n)^{1/2}(Σ_zN²)^{1/2}` | 130693.92 | `PROVED` |
| C2: twist-amplified `r=3` | `p·(1/n)^{1/3}(Σ_zN³)^{1/3}` | 121743.02 | `PROVED` |
| **#393 `p`·packing** (best) | `|B|·C(n,m)/V_{t'}`, `t'=⌊(w+1)/2⌋=2108` | **103841.23** | `PROVED` |

**Reading (stated plainly).**
- The C1 second-moment route feeds (b1) through Cauchy–Schwarz to prove only `S1≤2^{130686.93}` —
  **below-trivial** (worse than `S1≤C(n,m)=2^{130671.43}`): the unconditional `M2` bound gives no
  nontrivial `S1` bound at all.
- The C2 twist route lands `2^{130693.92}` (`r=2`) / `2^{121743.02}` (`r=3`); the twist orbit shaves
  only `17/r` bits (it is worse than C1's curve-CS at `r=2` by `√(p/n)=2^{6.99}`, since C1 uses the
  `√p` curve-averaging that C2 discards).
- All are **dominated by #393's `p`·packing `2^{103841.23}`**, which stays the best unconditional
  bound on `S1` (#393's direct `(T,r)`-rigidity ceiling `2^{103810.24}` bounds `#rays≤S1` even lower).
- Every unconditional handle throws away the depth equation and/or the curve restriction and lands
  `~10⁵` bits above equidistribution — the **`prop:proper-q-gap` shape**.

---

## 6. Twist dichotomy (`PROVED`) and the missing generic input

The twist-orbit moment gain (factor `n`) is available **iff `Γ` is twist-invariant**, which holds
**iff `z*=0`**:
- `z*=0` (planted monomial `U=X^{m'}`): `φ_j(s)=s^j`, `Γ={(s,s²,…,s^{w+1})}` is the **Veronese /
  diagonal** curve — a single twist orbit `z_j↦ζ^j z_j` (plus `s=0`); `prop:q-orbit-moment` applies
  and the factor-`n` gain is real.
- `z*≠0`: `θ(ζs)≠(ζs,ζ²φ_2(s),…)` in general, so `Γ` is a **transversal** curve and the twist-orbit
  gain is unavailable.

(Verifier gate `twist_equivariance` confirms the invariance direction; the toy dichotomy `z*=0 ⇔ Γ`
twist-invariant is exhibited on rows A/B.) The generic-case (`z*≠0`) sharp curve-`M2` bound needs a
`(W,λ)`-**Veronese-transversality**-type estimate — the same missing-input shape flagged as its own
open core in the integrated bounded-excess/RC lineage
(`experimental/notes/l1/l1_bounded_excess_structure.md:295` — *"an instance of the `(W,λ)`-Veronese
transversality the residual conjecture RC already flags as its own open core"* —,
`experimental/notes/l1/l1_sigma_calculus.md` §2A.2/§2A.3). This transversality of the finite
depth-`(w+1)` curve `Γ` to twist orbits is **not** the base-commit `prop:vandermonde-kills-low-rank`
(linear independence of the *primitive moment-curve columns* `v_y` at `R=Θ(n)` in the asymptotic
entropy-inverse route): a distinct object at a distinct scale; the two must not be conflated.

---

## 7. The measured law (`EXPERIMENTAL`) and the residual-equidistribution conjecture

Exact stdlib enumeration at four toy rows (`measure.py`, results banked in
`scratchpad/laneC_eq/toy/final_summary_ABCE.json`); each row buckets *all* `m`- and `(m+1)`-subsets by
depth-`(w+1)` prefix and evaluates `S(z*)=Σ_s N_{w+1}(θ(s))` and `M2(z*)` on 200 random + 20
heavy-`(m+1)`-derived + the all-zero `z*`. **`Σ`-ratio** `:= S(z*)/(C(n,m)/p^w)`; **planted**
`:= (m+1)·N^{(m+1)}(z*)` (the exact `prop:base-field-floor` term); **residual** `:= S(z*)−planted`;
**residual ratio** `:= residual/(C(n,m)/p^w)`.

| row | `p,n,K,m` | heuristic `C(n,m)/p^w` | max fiber | random-`z*` `Σ`-ratio (mean) | heavy-`z*` `Σ`-ratio (max) | residual ratio (mean / max) | #393 thm | twist |
|---|---|---:|---:|---:|---:|---:|:--:|:--:|
| A | 97,16,4,6 | 0.851100 | 3 | 0.969 | 24.674 | 0.835 / 4.700 | 26/26 | 240/240 |
| B | 97,16,5,7 | 1.215857 | 3 | 1.028 | 39.478 | 0.927 / 4.112 | 25/25 | 240/240 |
| C | 113,16,4,6 | 0.627144 | 3 | 0.957 | 33.485 | 0.851 / 4.784 | 26/26 | 240/240 |
| E | 73,24,8,10 | 368.03 | 16 | 1.0000 | 1.859 | 0.802 / 1.141 | 6/6 | 360/360 |

Row E (`p=73`, `D=μ_24`, `w=2`; the measurer's extra row, `params` verified `w=m−K=2`, `d1=w+2=4`,
`m'=m+1=11`, `24|p−1`) is the **smooth regime** (heuristic `368` ≫ 1, closest to the deployed
`2^{23.14}`); rows A/B/C are the sub-unit-heuristic Poisson regime.

**(i) Random `z*` — the exact average identity, measured.** Random-`z*` `Σ`-ratio means are
`0.969/1.028/0.957` (A/B/C) and `0.9999` at the large-fiber row E (`min 0.821, max 1.212`). This is the
finite-200-sample estimate of the exact statement of §4: `avg_{y}S(y)/heuristic = 1.0` **exactly**
over *all* `y∈B^{w+1}`. *Precise wording (the `0.851/1.216` are not `1.0` and should not be):* the
heuristic `C(n,m)/p^w` **is** `avg_y S(y)`; at toy scale that average is a sub-unit *absolute* mean
occupancy (`0.851, 1.216, 0.627`, `368.03`), **not** a normalized ratio. The number that is exactly
`1.0` is `avg_y[S(y)/heuristic]`; the random-sample means approximate it (and the "overall" means
exceed `1` only because the sample deliberately injects the 20 heaviest prefixes). The exact average
is verified by the `p`-to-1 preimage identity, not by sampling.

**(ii) Heavy `z*` — all concentration is planted.** Heavy-derived `z*` reach `Σ`-ratios up to
`24.7/39.5/33.5` (A/B/C), but the planted/residual split localizes it: the top offenders
`A:z*=[1,1,1]` (`Σ=21`, planted `21`, **residual `0`**), `B/E:z*=[0,0,0]` (`B: Σ=48`, planted `48`,
**residual `0`**) have their entire mass in the base-field-floor stratum. In the smooth row E the top
offender `z*=[0,0,0]` has `Σ=684`, planted `264`, residual `420` — residual **nonzero** but its ratio
is only `420/368=1.14`; the `residual=0` of rows A/B/C is the sub-unit-heuristic artifact (below `1`,
the only way to be heavy is to be entirely planted), while row E shows the real content: the residual
persists but stays `O(1)·`heuristic.

**(iii) Residual ratios stay small.** Across all `z*` (all four rows): residual-ratio mean
`≈0.80–0.93`, **max `4.784` (row C)** — bounded well below the planted spikes.

**(iv) Crosschecks.** #393-Theorem `curve-sum==#valid T` (with independent Lagrange census ground
truth): A `26/26`, B `25/25`, C `26/26`, E `6/6`. Twist-orbit constancy: `240/240` (A/B/C), `360/360`
(E). Prefix-rigidity: `0` violations (A/B/C exhaustive; E fast-mode, skipped).

> ### `CONJECTURAL_WITH_FALSIFIER` — Residual curve equidistribution
> For every planted `z*`, the **residual** (non-planted) curve mass obeys
> ```
>       S(z*) − (m+1)·N^{(m+1)}(z*)  ≤  R_res · C(n,m)/p^w
> ```
> with a small `R_res` (measured `R_res<4.79` across four toy rows, mean residual ratio `≈0.8`).
> **Falsifier:** any `z*` whose residual curve mass `≫` heuristic. The **planted** mass is *not* a
> falsifier — it is the *exact* `prop:base-field-floor` census `(m+1)·N^{(m+1)}(z*)`. **Direction
> caveat (`AUDIT`):** `prop:base-field-floor` bounds this census **from below**
> (`≥(m+1)·⌈C(n,m+1)p^{−(w+1)}⌉ = 69754·1 = 2^{16.089988}` at L4, density `2^{−8.035617}<1 ⇒ ⌈·⌉=1`);
> it is **not** an upper bound. Bounding the planted mass *above* needs a depth-`(w+1)` max-fiber
> (`ℓ^∞`/Q-type) input on `(m+1)`-subsets, `N^{(m+1)}(z*)≤⌈density⌉` — unproven, and *demonstrably
> false* off the sub-unit regime: `(m+1)·⌈density⌉` is violated `3×` in row A (`z*=[1,1,1]`: planted
> `21` vs `7`) and `3.43×` in row E (`z*=[0,0,0]`: `N^{(m+1)}=24`, planted `264` vs `77`). So the
> planted term is exact but **not a priori subdominant**; at L4 its smallness (`2^{16.09}`) is a
> *floor*, not a ceiling, and asserting it is small assumes the very `(m+1)`-max-fiber bound this
> program treats as open.
>
> **Consequence chain.** residual-equidistribution splits `S1 = residual + planted` with
> `residual ≤ R_res·C(n,m)/p^w` (conjecture) and `planted = (m+1)·N^{(m+1)}(z*)` the *exact*
> `prop:base-field-floor` census — itself the raw-BC obstruction (`cor:raw-bc-fails`). Thus the
> conjecture is the `ℓ²`/variance-along-`Γ` statement of §3 (**strictly weaker than depth-`(w+1)`
> row-sharp Q**, not the `ℓ^∞` max-fiber) governing the *primitive* part only; upgrading it to the
> full `S1 ≈ C(n,m)/p^w` additionally requires an `(m+1)`-subset max-fiber bound on the planted
> census, which is *not* supplied here.

---

## 8. Open (tight)

1. **Sharp curve-`M2` / curve-SP bound** `M2≤2^{2C}M2_equi`, `C=O(1)` — the whole remaining content of
   C1; unconditionally only `2^{261343}` (b1) / `2^{153665}` (b2), `~10⁵` bits too weak. Q-shaped
   (`thm:q-implies-sp`, §2) but strictly weaker than max-fiber Q (§3).
2. **Veronese transversality for `z*≠0`** — the generic-curve input of §6 (`(W,λ)`-Veronese
   transversality), recovering a moment gain when `Γ` is not a twist orbit.
3. **The residual-equidistribution conjecture** (§7): proof or falsification at scale.
4. **Non-planted lines and deeper profiles** — deferred to #393 §8 items 3–4.

**Non-claims.** No claim that `M2≤2^{2C}M2_equi`; no `conj:Q`; no `U(1116048)≤B*`; no row-sharp Q. The
unconditional `M2` bounds are audit ceilings, the measured law is `EXPERIMENTAL`, and the residual
conjecture is `CONJECTURAL_WITH_FALSIFIER` — none is a resolution.

---

## 9. Verifier

`experimental/scripts/verify_bc_l4_curve_second_moment.py` (stdlib, zero-arg exit-0 = PASS;
`--tamper-selftest` = every pin caught; runtime `<5s`).

- **G1 (exact L4).** Big-int: `log2 C(n,m)=130671.433651`, `M2_equi=15.289333`, dominant `e*=32632`
  (exact rational ratio-crossing), `log2 T_{e*}=261335.0475`, top-stratum `153665.4719`,
  `p`·packing `103841.2255` (cross-check vs #393), anticode(`w`) `108108.0403`. lgamma:
  `Σ_e T_e=261342.8673` (pinned inside the exact bracket `[T_{e*}, (#terms)T_{e*}]`), CS-through
  `130686.9280`, twist-amplified `130693.9223`/`121743.0234`, heuristic `23.139009`.
- **G2 (self-contained toy, rows A+B + mini-row).** Three-way `M2` identity
  (`def==pairs-on-V==Σ_Γ N²`); off-diagonal `deg(A−B)≤e−w−2` by enumeration; top-stratum constant
  shift; twist-equivariance `θ_{ζz*}(ζs)=ζθ_{z*}(s)` over all `ζ∈μ_n`; orbit constancy of `S`; the
  **exact average identity** `Σ_y S(y)=p·C(n,m)` by full enumeration on `p=13,D=μ_6,m=4` (`195=13·15`)
  plus `p`-to-1 preimage + `Σ_z N=C(n,m)`; Cauchy–Schwarz instances; planted/residual split
  (`residual=0` on the top offenders `A[1,1,1]`, `B[0,0,0]`; nonzero control `B[96,1,96]`);
  #393-Theorem crosscheck (curve-sum `==` `#valid T`) with independent Lagrange census on 2 `z*`/row.
- **G3 (tamper).** Every pinned integer/float perturbed; each flips its gate to FAIL (`34/34` caught).

```
python3 experimental/scripts/verify_bc_l4_curve_second_moment.py
python3 experimental/scripts/verify_bc_l4_curve_second_moment.py --tamper-selftest
```

---

## 10. Relationship to concurrent work

- **open PR #393** (`bc-l4-interior-chart-to-q`, parent, NOT yet integrated into `main`) — this
  packet analyzes the second moment of #393's `S1=Σ_s N_{w+1}(θ(s))`; §1 restates #393's Theorem and
  Corollary self-containedly, and Route C1 answers #393 §8 item 2 (curve equidistribution / second
  moment) with an exact identity, the exact needed constant, and the exact `~10⁵`-bit unconditional
  gap. No file dependency on #393 (which is unintegrated); the verifier re-derives every #393 statement
  it uses.
- **#392** (`thresholds-moment-floor-reconciliation`) / **#394** (`lean-gf-composite-descent`, Lean
  `gcd(e,N)` composite-prefix descent) — same-day sibling packets, same `prob:saturated-bc` /
  row-sharp-Q neighborhood; no object or file dependency in either direction. (#394 formalizes the
  `prop:composite-descend` used in §4's composite audit; courtesy cross-link only.)
- **Grande finale logarithmic-moment route** (`thm:logmoment-equivalence` / `def:primitive-logmoment`,
  integrated into `grande_finale.tex` at base `53bb5df`) — the **asymptotic** (`r→∞`) primitive-Q
  equivalence; complementary to this packet's **finite** fixed-`r` curve second moment (`r=2` (CS) at
  the deployed L4 row, §2–3). That entry itself flags "do not use the asymptotic `e^{o(n)}` statement as
  a certificate" for finite rows; C1/C2 supply exactly the finite-row `ℓ²` curve object one depth down.
  No object or file dependency.
- **#369** (`cap25_v13_bc_l4_base_floor_ladder`, integrated) — the fixture; the planted stratum here is
  its `d1=4218` floor `69754` (§7); heuristic `=` #369 boundary row `23.139009`.
- **#361** rung audit (`cap25_v13_qfin_rung_audit`, integrated) — `a_4=23.139009074` is the
  cross-consistency target (verifier gate `heuristic`).
- **#389** (Danny, draft, LQ top-seam) — no deliverable-file or object contact; courtesy only.
- Steering `b33609d` / `7bd50ca` / `ab7721e` — B1 / `prob:saturated-bc` v2 resolution type (b),
  row-sharp-Q vocabulary; this packet supplies the `ℓ²` / variance-along-`Γ` refinement of the Q input.

---

## 11. References (labels at base commit `53bb5df`)

`experimental/grande_finale.tex`:
`prop:prefix-witness` (563), `prop:pole-line` (579), `prop:prefix-rigidity` (660),
`prop:second-moment` (676), `cor:anticode-cap` (694), `thm:moment-q` (721),
`def:primitive-logmoment` (752), `thm:logmoment-equivalence` (769), `prop:vandermonde-kills-low-rank` (841),
`rem:finite-moment-order` (865), `prop:twist-orbit` (869), `prop:q-orbit-moment` (923),
`prop:composite-descend` (969), `prop:top-stratum-quotient-sieve` (1163), `prop:gamma2-ledger` (1199),
`prop:base-field-floor` (1389), `thm:q-proper` (1557), `thm:saturation` (1706), `cor:raw-bc-fails` (1738),
`prop:line-ray-saturation` (1762), `thm:q-implies-sp` (1784), `thm:sp-proper` (1822),
`prop:proper-q-gap` (1853), `prob:row-sharp-q` (2072), `prob:saturated-bc` (2086).

Fixture (cite, don't re-pin): `experimental/notes/thresholds/cap25_v13_bc_l4_base_floor_ladder.md`,
`experimental/data/certificates/frontier-adjacent/kb_mca_bc_l4_base_floor_ladder_v1.json`.
Veronese-transversality lineage: `experimental/notes/l1/l1_bounded_excess_structure.md` (line 295),
`experimental/notes/l1/l1_sigma_calculus.md` (§2A.2/§2A.3).
Companion (open, unintegrated): `experimental/notes/thresholds/cap25_v13_bc_l4_interior_chart_to_q.md`
(PR #393, branch `bc-l4-interior-chart-to-q`).
