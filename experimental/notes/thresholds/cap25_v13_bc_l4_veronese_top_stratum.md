# CAP25 v13 BC L4: the z*=0 (Veronese) curve-`M2` top stratum is empty (char 0)

**Status.** `PROVED` (char-0 emptiness theorem, full proof; exact `Z[ζ_n]` corroboration) /
`CONDITIONAL` (char-`p` emptiness at the L4 prime, reduced to a named root-non-concentration input) /
`CONJECTURAL_WITH_FALSIFIER` (that input, with an explicit falsifier + pseudorandom margin) /
`AUDIT` (fixture / `#395` decomposition consistency; recomputed numbers).

**Headline (`PROVED`).** At the L4 fixture with `z*=0` — the planted interior word is the pure
monomial `U=X^{m'}`, so the depth-`(w+1)` prefix curve is the Veronese/diagonal
`Γ={(s,s²,…,s^{w+1})}`, i.e. the **twist-invariant** branch of open PR `#395`'s twist dichotomy —
the **top stratum `e=w+2` of the curve second moment `M2` is EXACTLY EMPTY over characteristic 0**.
The mechanism is a two-step rigidity: the top-stratum members are pairs of degree-`(w+2)` divisors of
`X^n−1` differing by a constant; for `n=2^a` the Lam–Leung structure of vanishing sums of `2`-power
roots of unity forces every such pair to be antipodal-closed, and a parity descent then forces `w+2`
to be a power of `2`. At L4 `w+2 = 4218 = 2·3·19·37` is **not** a power of `2` (and `(w+2)/2 = 2109 =
3·19·37` is odd), so the stratum is empty. This is the **first nontrivial curve-`M2` emptiness theorem** — the
provable half of `#395`'s dichotomy: the leading off-diagonal term of the curve second moment vanishes
identically. In characteristic `p` the stratum is nonempty only through a char-`p` degeneration (`p`
dividing a cyclotomic defect); that residual is a **root-non-concentration / Weil-type input, the exact
analogue of `#382`'s min-`j` pencil freeze**, pinned below with an overwhelming pseudorandom margin.

**Self-containment.** Open PR `#395` (`bc-l4-curve-second-moment`) and its parent `#393`
(`bc-l4-interior-chart-to-q`) are **not integrated into `main`**. Every statement of `#395`/`#393`
used here is restated in §0–§1 and re-derived from scratch by the verifier's toy; there is no file
dependency on either unintegrated note. General references are to `grande_finale.tex` at the base
commit and to integrated notes (`#369`, `#382`).

**Verifier.** `experimental/scripts/verify_bc_l4_veronese_top_stratum.py` (stdlib only; zero-arg
exit-0 = PASS; `--tamper-selftest` = every pin caught; runtime `<60s`, measured `7.8s`).

---

## 0. Object recap (`AUDIT`)

**L4 fixture** (cite the integrated ladder note `cap25_v13_bc_l4_base_floor_ladder.md` (`#369`) and its
certificate `kb_mca_bc_l4_base_floor_ladder_v1.json`; not re-pinned):
```
n=|D|=131072=2^17     K=65537=2^16+1     m=69753 (odd)     w=m−K=4216
p=|B|=2^31−2^24+1=2130706433 (KoalaBear, log2 p=30.988685)   m'=m+1=69754   d1=w+2=4218
D = μ_n ⊆ B^×  (the n-th roots of unity; toy rows use D=μ_n verbatim)
```
Write `ℓ_S(X)=∏_{x∈S}(X−x)`; `a_j(S)` = coefficient of `X^{|S|−j}` in `ℓ_S` (`a_0=1`), so
`a_j=(−1)^j e_j(S)` with `e_j` the elementary symmetric functions and `p_j` the power sums of the roots.
`Φ_{w+1}(T)=(a_1,…,a_{w+1})(T)`, `Fib_{w+1}(z)={T∈\binom{D}{m}:Φ_{w+1}(T)=z}`,
`N_{w+1}(z)=|Fib_{w+1}(z)|`.

**Three-line object.**
1. *Fixture / word.* At `z*=0` the planted interior word is the pure monomial `U=X^{m'}` (the depth-
   `(w+1)` prefix of the received word is null).
2. *The curve `Γ`.* The interior chart of `#393`/`#395` has the twisted prefix curve
   `θ(s)=(φ_1,…,φ_{w+1})` with `φ_1=s`, `φ_j=z*_j+(s−z*_1)φ_{j−1}`. **At `z*=0`**: `φ_j=s·φ_{j−1}=s^j`,
   so `Γ={θ(s)}={(s,s²,…,s^{w+1}):s∈B}` — the **Veronese curve**, `#395`'s twist-invariant branch (§6):
   the twist `z_j↦ζ^j z_j` maps `Γ` to itself, so the factor-`n` twist-orbit gain is available here.
3. *The top stratum.* The curve second moment is `M2 = Σ_{s∈B} N_{w+1}(θ(s))²`; its top nonzero
   off-diagonal stratum `e=w+2` is the **constant-shift pairs** `A,B=A−c` (`c∈B^×`) — equivalently
   (§1) ordered pairs of degree-`(w+2)` divisors of `X^n−1` differing by a constant. This note is that
   top stratum at `z*=0`.

**Restated `#395` Theorem C1 (curve second moment, `PROVED` in `#395`; used as input).** With
`V={valid T}=Φ_{w+1}^{−1}(Γ)` and the off-diagonal encoding `R=T∩T'`, `P=T∖T'`, `P'=T'∖T`, `e=|P|`,
```
   M2 = Σ_{s∈B} N_{w+1}(θ(s))²
      = S1  +  Σ_{e=w+2}^{min(m,n−m)}  Σ_{R⊆D, |R|=m−e}  sp^Γ_{w+1}(e;R),          (C1)
```
`S1=|V|` the diagonal, and the top nonzero stratum `e=w+2` (`deg(ℓ_P−ℓ_{P'})≤0`) is the constant-shift
pairs subject to the curve constraint. (Verifier gate G3 re-derives (C1)'s top-stratum shape by direct
`M2` enumeration on real `z*=0` fixtures; no dependence on the unintegrated `#395` file.) This note
evaluates the top-stratum cell `e=w+2` exactly, at `z*=0`.

---

## 1. Characterization: the top stratum = constant-shift pairs of divisors of `X^n−1` (`PROVED`)

### 1.1 Valid `T` at `z*=0` = the augmented multiset `M⁺=T⊎{s}` is `(w+1)`-null

Let `T∈\binom{D}{m}`. Then `T` is **valid** (`Φ_{w+1}(T)∈Γ`) iff `∃s: a_j(T)=s^j` for `j=1,…,w+1`. The
`j=1` equation forces `s=a_1(T)=−p_1(T)`; validity is then `a_j(T)=a_1(T)^j` for `j=2,…,w+1`. Put
`s=a_1(T)` and `M⁺:=T⊎{s}` (`|M⁺|=m'`). The coefficient of `X^{m'−i}` in `ℓ_{M⁺}=(X−s)ℓ_T` is
`a_i(T)−s·a_{i−1}(T)`, which under validity is `s^i−s·s^{i−1}=0` for `i=1,…,w+1`. Hence
```
   ℓ_{M⁺}=(X−s)ℓ_T = X^{m'} + (deg ≤ m−w−1) ≡ U=X^{m'} (mod X^K),   K=m−w,
   ⇔  e_1(M⁺)=…=e_{w+1}(M⁺)=0  ⇔(Newton, w+1<p)  p_1(M⁺)=…=p_{w+1}(M⁺)=0.        (Null)
```
`M⁺` is **`(w+1)`-null**: its first `w+1` power sums (equivalently elementary symmetric functions)
vanish. The degree bookkeeping is `#395`'s identity `m'−(w+2)=K−1`: at `z*=0` the depth-`(w+1)` prefix
rigidity and the augmented-locator threshold `K−1` are the same constraint, with `U=X^{m'}` the pure
monomial. (Verifier gate G1: `valid ⇔ (m+1)-null ⇔ e_j=(−s)^j ⇔ (X−s)ℓ_T≡X^{m'} mod X^K` on all `70`
`m`-subsets of the `n=8,K=2,m=4,w=2` toy.)

**One clean subtlety, pinned.** The valid prefix is **not** that of `(X−s)^{w+1}` (which has
`e_j=\binom{w+1}{j}s^j`). The correct condition is `e_j(T)=(−s)^j`, i.e. `a_j(T)=s^j` — verified on
every `m`-subset in G1, ruling out that misidentification.

### 1.2 The top stratum is the constant-shift pairs (`PROVED`)

By Theorem C1, `M2=Σ_{z∈Γ}N_{w+1}(z)²` counts ordered `(T,T')∈V×V` with equal depth-`(w+1)` prefix.
Off-diagonal pairs are encoded by `R=T∩T'`, `P=T∖T'`, `P'=T'∖T`, `e=|P|=|P'|`; `P,P'` are disjoint by
construction. Equal prefix on `V×V` forces equal `a_1`, hence equal `s`, so subtracting (Null) for
`M⁺=R⊎P⊎{s}` and `M⁺'=R⊎P'⊎{s}` (which share `R` and `s`) gives
```
   p_i(P) = p_i(P')      for i = 1,…,w+1.                                          (SP)
```
By Newton (`w+1<p`), (SP) ⇔ `ℓ_P` and `ℓ_{P'}` agree in coefficients `a_1,…,a_{w+1}`; both are monic of
degree `w+2`, so they differ only in the constant term: `ℓ_P−ℓ_{P'}=c`, and `c≠0` iff `P≠P'` (this
reconfirms the `e=w+2`, `deg≤0` top-stratum shape). Since `P,P'⊆D=μ_n`, **both `ℓ_P` and `ℓ_{P'}=ℓ_P−c`
divide `X^n−1`**; the shift `c=(−1)^{w+2}(∏P−∏P')∈B^×`. A shared root `ζ∈P∩P'` would give
`c=ℓ_P(ζ)−ℓ_{P'}(ζ)=0`, so constant-shift pairs are automatically disjoint — consistent with `P∩P'=∅`.
Folding in the common part `R`,
```
   top stratum = Σ_{(P,P')} #{ R⊆D∖(P∪P') : R⊔P valid },   (P,P') = ordered pairs of
                 degree-(w+2) divisors of X^n−1 with ℓ_P−ℓ_{P'}∈B^×.               (TS)
```
The combinatorial core is `A(μ_n,w+2) := #{(P,P')}`. **If `A=0`, then (TS) is `0` for every `R`
(present or empty) — the entire top stratum vanishes.** So it suffices to prove `A(μ_n,w+2)=0`.

---

## 2. THE THEOREM: char-0 emptiness (`PROVED`)

> **Theorem T4 (Veronese curve-`M2` top stratum, char 0).** For `n=2^a` and `1≤d≤n/2` (disjointness of
> `P,P'` forces `2d≤n`), ordered constant-shift pairs `(P,P')` of `d`-subsets of `μ_n` — disjoint `P,P'`
> with `p_i(P)=p_i(P')` for `i=1,…,d−1`, equivalently `ℓ_P−ℓ_{P'}=c≠0` — exist over characteristic `0`
> **iff `d` is a power of `2`** (and then `P,P'` are cosets of `μ_d`; the `d≤n/2` bound guarantees the
> `n/d≥2` cosets needed for a disjoint pair). In particular the L4 top stratum (`d=w+2`) is **empty**: `A(μ_{2^17},4218)=0`,
> because `w+2=4218` is not a power of `2`.

The proof is two lemmas — antipodal forcing (from Lam–Leung) and parity descent — applied to (SP).

### 2.1 Lemma A (antipodal forcing from Lam–Leung)

> **Lemma A.** Let `n=2^a` and let `P,P'⊆μ_n` be **disjoint** with `p_1(P)=p_1(P')` over a field of
> characteristic `0`. Then `P=−P` and `P'=−P'` (both antipodal-closed).

*Proof.* Since `−1∈μ_{2^a}`, the multiset `M:=P ⊎ (−P')` (where `−P'={−y:y∈P'}⊆μ_n`) satisfies
`Σ_{β∈M}β = p_1(P)−p_1(P') = 0`: a vanishing sum of `2d` roots of unity in `μ_{2^a}`. By Lam–Leung
(for prime-power order `N=p^a` all vanishing sums of `N`-th roots of unity are non-negative integer
combinations of the rotated `Φ_p`-relations; for `p=2` the only relation is the antipodal atom
`η+(−η)=0` — the classical de Bruijn/Rédei case, sharpened by Mann and Conway–Jones), `M` decomposes
into antipodal pairs `{η,−η}`. A necessary and sufficient consequence is `mult_M(β)=mult_M(−β)` for all
`β`. Fix a pair `{β,−β}` and set the four indicators `a=[β∈P]`, `b=[−β∈P]`, `c=[β∈P']`, `d=[−β∈P']`.
Then `mult_M(β)=[β∈P]+[β∈−P']=a+d` and `mult_M(−β)=[−β∈P]+[−β∈−P']=b+c`, so
```
        a + d = b + c,        with  a,b,c,d ∈ {0,1}  and  ¬(a∧c), ¬(b∧d)  (disjointness P∩P'=∅).
```
If `a=1,b=0` then `c−d=1` forces `c=1`, but `a=c=1` violates `¬(a∧c)`; if `a=0,b=1` then `c−d=−1`
forces `d=1`, but `b=d=1` violates `¬(b∧d)`. Hence `a=b`, and then `c=d`. So for every antipodal pair
`β∈P⇔−β∈P` and `β∈P'⇔−β∈P'`, i.e. `P=−P` and `P'=−P'`. ∎

This uses only the `j=1` relation. Two immediate corollaries: (i) any constant-shift pair is
antipodal-closed, so it has **scale ≥2** — there are **no primitive (scale-1) pairs** in char 0; and
(ii) `d=|P|` is **even** (antipodal closure has no fixed point, as `x=−x⇒2x=0⇒x=0∉μ_n`). If `w+2` is
odd, the top stratum is already empty. (At L4 `w+2=4218` is even, so the descent below is needed.)

### 2.2 Lemma B (parity descent) and the theorem

Let `(P,P')` satisfy (SP) with `d=|P|` even; by Lemma A `P=−P`, `P'=−P'`, so `P,P'` are unions of
fibers of the squaring map `σ:μ_{2^a}→μ_{2^{a−1}}`, `x↦x²` (each fiber `{x,−x}`). Put `P̄:=σ(P)`,
`P̄':=σ(P')⊆μ_{2^{a−1}}`, each of size `d/2`.
- **Disjoint.** If `u∈P̄∩P̄'` then `x²=y²=u` for some `x∈P,y∈P'`; `y≠x` (disjointness) forces `y=−x`,
  and `P=−P` gives `−x∈P`, so `−x∈P∩P'` — contradiction. Hence `P̄∩P̄'=∅`.
- **Structure descends fully.** For each `u∈P̄` the two preimages `±x` contribute
  `x^{2j}+(−x)^{2j}=2u^j`, so `p_{2j}(P)=2·p_j(P̄)` and likewise for `P'`. The relations
  `p_{2j}(P)=p_{2j}(P')` for `2j≤d−1` therefore give (dividing by the invertible `2`)
  `p_j(P̄)=p_j(P̄')` for `j=1,…,⌊(d−1)/2⌋=d/2−1`. So `(P̄,P̄')` is again a **constant-shift pair**, of
  size `d/2` in `μ_{2^{a−1}}` — the full `d/2−1` relations, exactly the constant-shift condition one
  level down.

Write `d=w+2=2^k·q`, `q` odd. Iterating Lemma A + Lemma B `k` times reaches disjoint
`P^{(k)},P'^{(k)}⊆μ_{2^{a−k}}` of size `q`, still a constant-shift pair.
- If `q>1` (odd `≥3`): the level-`k` relation `p_1(P^{(k)})=p_1(P'^{(k)})` invokes Lemma A, forcing
  antipodal closure of an **odd-size** set — impossible. **No pair exists ⇒ empty.**
- If `q=1` (`d=2^k`): the descent bottoms at size `1` with **zero** relations (the constant-shift
  condition `p_1..p_{d−1}` is vacuous at `d=1`); any two disjoint singletons `{u},{u'}` work
  (`ℓ_{\{u\}}−ℓ_{\{u'\}}=u'−u≠0`). Climbing back, these are exactly the `μ_{2^k}`-coset pairs —
  **nonempty**.

Hence pairs exist iff `d` is a power of `2`. **At L4**, `d=w+2=4218=2·2109`, `q=2109=3·19·37` odd
`≥3`: after one descent the size is `2109` (odd), Lemma A is impossible, so `A(μ_{2^17},4218)=0` and the
top stratum (TS) is `0`. Since the scale divides `gcd(w+2,n)=gcd(4218,2^17)=2`, the only candidates are
scale-1 (killed directly by Lemma A) and scale-2 (killed by the descent to odd degree `2109`); **both
vanish**. ∎

### 2.3 Corroboration and the twist reading (`EXPERIMENTAL` / `AUDIT`)

- **Exact `Z[ζ_n]` census** (verifier G2, exact-in-`Z[ζ_n]` via `Φ_n`-reduction): for `n∈{8,16}` the
  constant-shift-pair count is nonzero **iff `d` is a power of `2`**, with `A_prim=0` throughout and the
  `j=1` relation forcing antipodal closure on all `1124` disjoint equal-`p_1` pairs (`18` at `n=8`,
  `1106` at `n=16`). The clean "power of `2`" phrasing is specific to `n=2^a`; the exact `Z[ζ_n]` census
  gives `A_prim=0` for **every** tested `n` (e.g. `n∈{10,12,24}`), so the primitive part is empty in
  char 0 in general — only the coset-family (composite) part survives, and only for the divisor structure
  of the given `n`.
- **General-`n=2^a` corollary (`PROVED`).** For every `a`, the Veronese top stratum is empty **unless
  `w+2` is a power of `2`** (`≤2^{a−1}`). L4 is the `a=17` instance.
- **Positive control (verifier G2/G3).** At `d=4=2^2` (a power of `2`) a pair exists explicitly:
  in `μ_8`, `P=μ_4=\{ζ_8^0,ζ_8^2,ζ_8^4,ζ_8^6\}` and `P'=ζ_8·μ_4=\{ζ_8^1,ζ_8^3,ζ_8^5,ζ_8^7\}` give
  `ℓ_P=X^4−1`, `ℓ_{P'}=X^4+1`, `ℓ_P−ℓ_{P'}=−2≠0` with `p_1=p_2=p_3` equal and `P∩P'=∅`. On a genuine
  `M2` toy (`n=8,K=2,m=4,w=2,e_top=4=2^2`) the top stratum is **NONEMPTY** (`2` pairs, each a verified
  constant shift with equal power sums) — the theorem's iff is exercised in both directions.
- **Twist reading (`AUDIT`).** `Γ` is a single `B^×`-torus orbit (`θ(ζs)=ζ·θ(s)`); the squaring
  `D→D_2=μ_{2^{16}}` is the twist-by-`μ_2` quotient, so Lemma B is literally `#395`'s / `prop:composite-
  descend`'s machinery. The factor-`n` twist amplification (real at `z*=0`, since `Γ` is twist-invariant)
  is moot against a zero count.

### 2.4 Exact L4 numbers (`PROVED` count; ceilings `AUDIT` from `#395`; `E[A]` heuristic)

| quantity | value | label |
|---|---:|---|
| top-stratum count (char 0) | **`0`** (exact) | `PROVED` |
| `#395` unconditional top-stratum ceiling `(p−1)C(n,m−w−2)C(n−m+w+2,w+2)` | `2^{153665.47}` | `AUDIT` (`#395`) |
| `M2_equi` (equidistributed target) `C(n,m)²/p^{2w+1}` | `2^{15.289333}` | `AUDIT` (`#395`) |
| char-`p` pseudorandom expected pair count `E[A]∼C(n,w+2)²·p^{−(w+1)}` | `2^{−76898.5}` | heuristic |
| pseudorandom threshold `p_0` (`E[A]∼1`): `log2 p_0 = 2 log2 C(n,w+2)/(w+1)` | `2^{12.753}` | heuristic |
| L4 prime `p` margin above threshold | `+18.24` bits | — |

The theorem replaces the **leading** off-diagonal cell of the depth-`(w+1)` SP ledger — the
`2^{153665.47}` top-stratum constant-shift ceiling, the `prop:top-stratum-quotient-sieve` primitive
residual — by an **exact `0`** (char 0). It does **not** by itself lower the overall `M2` ceiling
(`#395` shows `M2` is dominated by the deep stratum `e*≈32632`); its content is *structural*: the
leading off-diagonal term of curve-`M2` at `z*=0` provably vanishes, and the same rigidity kills its
char-`p` shadow up to a Weil residual (§3).

---

## 3. Char-`p` residual and the `#382` parallel (`CONDITIONAL` / `CONJECTURAL_WITH_FALSIFIER`)

### 3.1 Why char-`p` is a genuine residual

Lemma A is a **characteristic-0** statement (Lam–Leung lives in `Z[ζ_n]⊂C`). Over `F_p` the relation
`p_1(P)=p_1(P')` holds mod `p`, i.e. the lift `δ:=p_1(P)−p_1(P')∈Z[ζ_n]` is a nonzero (by Theorem T4)
element with `p∣δ`; more generally a char-`p` primitive pair forces `p` to divide an explicit but
astronomically large cyclotomic resultant/defect (`≤(2(w+2))^{φ(n)}`). Height bounds cannot certify the
specific L4 prime, and no `poly(n)` Weil bound for "a shifted totally-split cyclotomic polynomial splits
again over one coset" is available. This is the same obstruction `#395` §6 names as `(W,λ)`-Veronese
transversality (its own open core; RC lineage `l1_bounded_excess_structure.md:295`,
`l1_sigma_calculus.md §2A`).

> **Theorem T4 (char-`p`, `CONDITIONAL`).** Over `F_p` the L4 top stratum is empty **iff** `p` divides no
> cyclotomic defect of a non-antipodal degree-`(w+2)` constant-shift configuration; equivalently iff no
> member of the constant pencil `{ℓ_P−c:c∈F_p}` has a *full* fiber (all `w+2` roots) in the single coset
> `D=μ_n` beyond the char-0-forced (coset) ones.

> **Root-non-concentration at the L4 prime (`CONJECTURAL_WITH_FALSIFIER`).** No primitive
> (non-antipodal) pair `P,P'⊆μ_{2^17}` of size `w+2=4218` has `p_i(P)=p_i(P')` for `i=1,…,w+1` over
> `F_p`, `p=2^31−2^24+1`. **Falsifier:** any such pair. Under the pseudorandom ceiling the expected count
> is `E[A]∼2^{−76898.5}`, vanishing with a `+18.24`-bit margin over the `p_0≈2^{12.753}` threshold.
> Small-case cross-check (verifier G3): `p_0∼(e·n/d)²` predicts `210,266,303,473` versus observed max
> **primitive** bad primes `97,97,193,433` for `(n,d)=(16,3),(24,4),(32,5),(24,3)` — every observed bad
> prime is below the predicted threshold. (Above threshold, `A_prim` collapses to `0`; the persistent
> `A_comp` is the char-0 coset family, not a falsifier.)

### 3.2 Same mechanism as `#382`'s min-`j` pencil freeze

`l1_minj_pencil_freeze.md` (`#382`, integrated) relocates its frontier to a **root-non-concentration /
Weil-type statement about an explicit low-degree polynomial family restricted to one coset of `μ_ℓ`**:
its Theorem 2 reduces the frontier to *no member of the degree-`(ℓ−a)` pencil `P−λ·A_drop` (`λ∈F_p`)
concentrates `≥9` roots in one coset* (its `μ_3≤8`, `~10^{−8}` per plant). LANE T4's residual is the
**same shape, one notch more rigid**:

| | `#382` min-`j` pencil freeze | **T4 Veronese top stratum** |
|---|---|---|
| pencil | `P(X)−λ·A_drop(X)`, degree `ℓ−a`, `λ∈F_p` | `ℓ_P(X)−c`, degree `w+2`, `c∈F_p` (constant pencil) |
| coset | one `μ_ℓ`-coset (`ℓ` points) | the coset `D=μ_n` (`n` points) |
| concentration target | a fiber of size `≥9` | a **full** fiber of size `w+2` (the shift *splits*) |
| pseudorandom ceiling | `P(μ_3≥t)∼C(ℓ,t)/p^{t−1}` (`~10^{−8}` at `t=9`) | `E[A]∼C(n,w+2)²/p^{w+1}` (`~2^{−76899}`) |
| char-0 status | freeze is `EXPERIMENTAL` (no proof) | **`PROVED` empty** (Lam–Leung + parity) |

The decisive difference: T4's target ("the shift *splits* over the coset") is rigid enough that char-0
is a **theorem**, not merely a heuristic freeze — a full split makes the defect a genuine *vanishing*
sum of roots of unity, to which Lam–Leung applies. `#382`'s "≥9 of `ℓ`" is a *partial* fiber, outside
Lam–Leung's reach — exactly why `#382` obtains only an experimental freeze while T4 obtains a proof. The
two share the identical residual (Weil non-concentration at the specific prime), with T4's margin
(`2^{−76899}`) dwarfing `#382`'s (`10^{−8}`).

---

## 4. What this does for `#395` (`AUDIT`)

`#395` §6 proves a **twist dichotomy**: the factor-`n` twist-orbit moment gain is available iff `Γ` is
twist-invariant, iff `z*=0` (Veronese) versus `z*≠0` (transversal). This note resolves the **twist-
invariant branch's leading term**:
- **`z*=0` (this note).** The twist-orbit machinery is available, and T4 shows it makes the top
  off-diagonal stratum of curve-`M2` **provably vanish in char 0** — the **first curve-`M2` emptiness theorem**.
  It removes the leading (top-stratum) cell (`2^{153665.47}`) of the `prop:top-stratum-quotient-sieve` ledger at
  this depth, replacing it by exact `0`.
- **Generic `z*≠0` branch — still open.** `Γ` is transversal, the twist gain is unavailable, and the
  sharp curve-`M2` bound needs the `(W,λ)`-Veronese-transversality estimate `#395` §6 flags. Untouched
  here.
- **Full `M2` bound — still open.** T4 zeroes only the top stratum `e=w+2`. The deeper strata
  `e>w+2` (dominated by `e*≈32632`) are **not** bounded beyond `#395`'s unconditional ceilings
  (`Σ_e T_e=2^{261342.87}` (b1) / `2^{153665.47}` (b2)); nothing here lowers the overall `M2`.

---

## 5. Open (tight) and non-claims

**Open.**
1. **Char-`p` emptiness at the L4 prime** — the pinned root-non-concentration / Weil residual (§3);
   proof needs a `poly(n)` non-concentration bound the program does not have.
2. **Deeper strata `e>w+2`** — no bound beyond `#395`'s ceilings; `M2` remains dominated by `e*`.
3. **Generic-`z*` (transversal) curve** — the `(W,λ)`-Veronese-transversality input of `#395` §6.

**Non-claims.** No claim on `M2≤2^{2C}M2_equi`; no `conj:Q`, no row-sharp `Q`; no equidistribution
claim; no resolution of the char-`p` L4 case; nothing about `z*≠0`. Theorem T4(i) is char-0 (or char-`p`
with `p∤defect`); it removes the top stratum only, not the SP-dominant deep stratum. The `E[A]` figure is
a pseudorandom-ceiling heuristic, not a proof.

---

## 6. Verifier

`experimental/scripts/verify_bc_l4_veronese_top_stratum.py` (stdlib; zero-arg exit-0 = PASS;
`--tamper-selftest` = every pin caught; measured `7.8s`).

- **G1 — characterization (a).** On all `70` `m`-subsets of `n=8,K=2,m=4,w=2`:
  `valid ⇔ (m+1)-null ⇔ e_j(T)=(−s)^j ⇔ (X−s)ℓ_T≡X^{m'} mod X^K`. PASS.
- **G2 — char-0 rigidity (Lam–Leung + parity, exact `Z[ζ_n]`).** For `n∈{8,16}`: pairs exist iff `d` is
  a power of `2`; `A_prim=0`; `j=1` forces antipodal closure on all `1124` disjoint equal-`p_1` pairs.
  **Positive control:** the explicit `d=4=2^2` `μ_4`-coset pair (`ℓ_P−ℓ_{P'}=const≠0`, equal power sums,
  disjoint). PASS.
- **G3 — `M2` top stratum on real fixtures (char-`p` degeneration probe).** *Positive control:*
  `n=8,e_top=4=2^2` → top stratum **NONEMPTY** (`2` constant-shift pairs). *Emptiness probe:*
  `n=16,e_top=3` (not a power of `2`) → **present** at the degenerate prime `p=97` (count `32 = A_prim`),
  **empty** at char-0-regime primes `113,193,241`. *Bad-prime cross-check:* `(16,3):97`, `(24,4):97`,
  `(32,5):193`, `(24,3):433` all below the `(e·n/d)²` thresholds `210,266,303,473`. PASS.
- **G4 — exact L4 numbers.** `4218=2·3·19·37`, `(w+2)/2=2109=3·19·37` odd, `gcd(w+2,n)=2`, `w+2` not a
  power of `2`; char-0 top count `0`; `#395` ceiling `2^{153665.47}→0`; `E[A]∼2^{−76898.5}`;
  `p_0∼2^{12.753}`; margin `+18.24` bits. PASS.
- **Tamper coverage:** `--tamper-selftest` perturbs each of the `27` pins in turn; every one flips its
  gate to FAIL (`27/27` caught).

```
python3 experimental/scripts/verify_bc_l4_veronese_top_stratum.py
python3 experimental/scripts/verify_bc_l4_veronese_top_stratum.py --tamper-selftest
```

---

## 7. Relationship to concurrent work

- **open PR `#395`** (`bc-l4-curve-second-moment`, parent, **not integrated**) — this note is the
  provable half of its §6 twist dichotomy: `z*=0 ⇒ Γ=`Veronese`=`one twist orbit, and T4 makes the
  leading off-diagonal term of curve-`M2` **vanish** in char 0. Depends on `#395`'s Theorem C1
  decomposition (restated self-containedly in §0; re-derived by G3). No file dependency.
- **open PR `#393`** (`bc-l4-interior-chart-to-q`, grandparent, **not integrated**) — supplies the
  interior chart `θ(s)` and `S1=Σ_s N_{w+1}(θ(s))` that `#395`/this note take the second moment of;
  restated in §0. No file dependency.
- **`#382`** (`l1_minj_pencil_freeze`, **integrated**) — the mechanism parallel: the identical
  root-non-concentration residual, one notch less rigid; §3.2 makes the parallel exact. T4 supplies the
  char-0 proof `#382`'s freeze lacks.
- **`#369`** (`cap25_v13_bc_l4_base_floor_ladder`, integrated) — the L4 fixture, cited not re-pinned.
- **`#361`** (`cap25_v13_qfin_rung_audit`, integrated) — fixture-consistent rung; no object contact
  here (courtesy).
- **Concurrent lanes T1/T2/T3** — no object or file dependency in either direction.
- **`#389`–`#398`** — no deliverable-file or object contact (courtesy only; the newest
  Q-frontier packets `#397` (row-sharp Q atom reductions, deployed row) and `#398`
  (b2 conj:Q barrier map) work the prefix-atom / character-sum side, not this
  curve-restricted constant-shift stratum).

---

## 8. References (labels at base commit `53bb5df`)

`experimental/grande_finale.tex`: `prop:newton` (551), `prop:prefix-rigidity` (660),
`prop:second-moment` (676), `prop:twist-orbit` (869), `prop:q-orbit-moment` (923),
`prop:composite-descend` (969), `prop:top-stratum-quotient-sieve` (1163), `prop:gamma2-ledger` (1199),
`prop:base-field-floor` (1389), `thm:sp-proper` (1822).

Fixture (cite, don't re-pin): `experimental/notes/thresholds/cap25_v13_bc_l4_base_floor_ladder.md`
(`#369`), `experimental/data/certificates/frontier-adjacent/kb_mca_bc_l4_base_floor_ladder_v1.json`.
Mechanism parallel: `experimental/notes/l1/l1_minj_pencil_freeze.md` (`#382`).
Veronese-transversality lineage: `experimental/notes/l1/l1_bounded_excess_structure.md` (line 295),
`experimental/notes/l1/l1_sigma_calculus.md` (§2A).
Companions (open, unintegrated): `cap25_v13_bc_l4_curve_second_moment.md` (`#395`),
`cap25_v13_bc_l4_interior_chart_to_q.md` (`#393`).
Char-0 engine: Lam–Leung, *On vanishing sums of roots of unity* (Mann; Conway–Jones; de Bruijn/Rédei
for prime-power order).
