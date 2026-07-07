# CAP25 v13 raw: row-sharp Q p^{w/2} concentration floor — second-moment routes dead per-stratum; crux = signed-e_m inverse (KB-MCA a=1116048)

Status: `PROVED` (the floor lemma §1 — scope: every bound factoring through the
second moment `Σ_z X²`, i.e. `r=2` / Cauchy–Schwarz / Fourier-Plancherel) /
`EXACT_MARGINS` (route map §3) / `OPEN` (routes (i)/(ii)/(iv): all reduce to the
named crux §7) / `AUDIT`+`ANALYSIS` (framing §7, weave §8).

**Verifier:** `experimental/scripts/verify_q_pw2_concentration_floor.py`
(zero-arg, stdlib-only, ~14 s, `RESULT: PASS (all 66 checks)`; exact big-int
ledger + Legendre-comb, every route margin, the r-floor reconciliation, exact
toy enumeration incl. Parseval and the #397 histogram anchor, and tamper
self-tests). Cross-validated against
`experimental/notes/thresholds/kb_mca_1116048_first_match_ledger_v1.md` and PR
#397's certs.

**What this is / is not.** This does **not** prove `U(1116048) <= B*`, the KB-MCA
first-safe agreement, or the row-sharp Q-prefix atom. It ships one proved
obstruction — closing every second-moment (`r=2` / Cauchy–Schwarz /
Fourier-Plancherel) route for the target, global or per-stratum — plus an
exact-margins route map (anticode separately dead for its own reason;
defect/exchange reduced to the open certificate) and the precise name of the one
input that could still close the atom. Every claim carries a label.

## 0. Deployed row and validated ledger `EXACT-COMPUTATION`

Deployed KoalaBear-MCA adjacent row (grande_finale.tex `def:q-row-atom`):

```
p = 2130706433 = 2^31-2^24+1    n = 2^21 = 2097152    k = 2^20 = 1048576
a = 1116048    j = m = 981104 (support size)    t = 67472    w = 67471
B* = 274980728111395087
```

Reproduced exactly from scratch (exact big-int C(n,j) via Legendre prime powers,
divided by the exact p^w; `lgamma`-log2 matches the exact big-int `log2 C(n,j)`
to `2.56e-9` bits):

```
avg_floor    = 57198030365          avg = C(n,j)/p^w = 2^35.735246
K_raw        = 4807520
K_rem        = 4805007              (= 2^22.196107)
target_floor = 274836936291722953
t*p          = 143763024447376
```

**Actionable target** (sufficient for the atom; `R_prim <= N_w` pointwise, so
bounding the full `N_w` suffices). PR #397's certificate is the **additive
stratum bound** `|R_prim(z)| <= |G_gen_support(z)| + |D_full_rank_prim(z)| +
|E_ret(z)|` (its cert form; an additive bound, not asserted here as a proven
partition), with `|E_ret(z)| <= binom(16,7) = 11440` imported-PROVED —
`~2^13.5` below target — so `G_gen_support` and `D_full_rank_prim` carry the
work:

```
max_z N_w(z) <= K_rem * avg = 2^57.931354   (= target_floor above).
```

`N_w(z) = |Fib_w(z)|` is the prefix fiber count (grande_finale.tex
`prop:second-moment`).

---

## 1. HEADLINE: the uniform p^{w/2} concentration floor `PROVED`

> **Obstruction (proved, elementary).** Let `X(z) >= 0` be any per-target count on
> `F_p^w` (a support-stratum fiber function). Every bound produced from the second
> moment `sum_z X(z)^2` — i.e. every `r=2` moment / Cauchy–Schwarz /
> Fourier-Plancherel (`L²`) argument, **global or per-stratum, before or after
> first-match deletion** — satisfies
> ```
> [any r=2 bound on max_z X]  >=  sqrt( sum_z X(z)^2 )  >=  (sum_z X(z)) / p^{w/2}.
> ```

**Two-line proof.** By Cauchy–Schwarz on the `#{z : X(z)>0} <= p^w` nonzero
targets, `(sum_z X)^2 = (sum_z X·1)^2 <= (sum_z X^2)(#nonzero) <= (sum_z X^2) p^w`,
so `sum_z X^2 >= (sum_z X)^2 / p^w`; and `max_z X <= sqrt(sum_z X^2)` is the
smallest quantity any `r=2` method can output. ∎

Consequence at the deployed row (`verify` §1):

```
(w/2) log2 p                        = 1045418.7723 bits
full-mass r=2 bound  >= avg·p^{w/2}  = 2^1045454.5075
target K_rem·avg                     = 2^57.9314
=> any r=2 bound on a constant-fraction stratum is DEAD by 1,045,396.58 bits,
   INDEPENDENT of how sharp the L^2 ledger (Gamma_2) is.
```

**Scope (exact).** The floor binds precisely the arguments that factor through
`Σ_z X(z)²`: `thm:moment-q` at `r=2`, pointwise Cauchy–Schwarz, and every
Fourier-Plancherel/`L²` argument — global or per-stratum. It does **not** by
itself bind the signed-`e_m` `L¹` triangle route (§7); only that route's
Cauchy–Schwarz-on-the-`c`-sum specialization collapses to route (iii). Within
`L²` it is not escapable by concentration: even if `X` is supported on `nu`
targets, `max_z X >= (sum_z X)/sqrt(nu) >= (sum_z X)/p^{w/2}`.

---

## 2. Full-mass target: every r=2 route is rigorously dead `PROVED`

`sum_z N_w(z) = C(n,m)` **exactly** (every `m`-subset lands in one fiber). By §1
the direct `r=2` bound is `>= C(n,m)/p^{w/2} = 2^1045454.5`, **DEAD by
1,045,396.58 bits with no assumptions.** Since `R_prim <= N_w`, bounding `N_w`
suffices, so the full-mass second-moment route is closed unconditionally.

---

## 3. Route map with exact margins `EXACT-COMPUTATION`

Target line everywhere `2^57.931354`; "gap" `= log2(bound) − 57.931354`; every
numeric row recomputed by `verify` §2.

| route | object (tex label) | log2 bound | gap (bits) | verdict |
|---|---|---:|---:|---|
| (A) anticode fiber cap | `cor:anticode-cap` (PROVED) | 1717535.93 | **1717478.00** | DEAD (separately — p-independent, not a floor instance) |
| (iii/B) 2nd-moment ledger | `thm:sp-proper`+`thm:moment-q` `r=2` | R = 2090837.54 (×K_rem) | **2090815.35** | DEAD (floor) |
| (B′) pointwise Cauchy–Schwarz | `sqrt(C(n,m)+Σ_e T_e)` | 2090873.28 | **2090815.35** | DEAD (floor) |
| intrinsic `r=2` floor | §1, any `L²` ledger | 1045454.51 | **1045396.58** | DEAD (the floor itself) |
| (i) defect-stratified | `prop:prefix-rigidity` + #397 foldings | — | — | OPEN (≡ the crux) |
| (ii) exchange-compression | `prop:mode-null-false` + `prop:q-orbit-moment` | — | — | OPEN (≡ the crux) |
| (iv) signed-`e_m` `L¹` | `prop:fourier-audit` | — | — | OPEN (the crux; not floor-bound, §7) |

Route-specific readings:

- **(A)** `N_w(z) <= C(n,m-w)/C(m,w) = 2^1717535.93`. Dies **separately, for its
  own reason**: the bound contains no `p` at all (pure subset combinatorics), and
  lands 672,081.42 bits above even the abstract §1 floor. Weak precisely because
  `m ≈ n/2`; anticode caps are useful only for `m << n`. Not a floor instance.
- **(iii/B)** loose ledger `T_e = C(n,m-e)C(n-m+e,e)C(n-m,e)` (`thm:sp-proper`,
  drops the depth equation): `Σ_e T_e = 2^4181746.56`, peaked at the **bulk**
  `e* = 522117` (NOT the top seam `e = w+1`), giving `Gamma_2 = 2^2090837.54`,
  `R = 2^2090837.54`. The sharper top-stratum term
  `(p-1)C(n,m-w-1)C(n-m+w+1,w+1) = 2^2445389.77` saves 367,422 bits on the `e=w+1`
  term, but that term is `1.74e6` bits **below** the bulk peak, so it is
  irrelevant. `sqrt(C(n,m)+Σ_e T_e) = 2^2090873.28 = C(n,m)` to `0.01` bit — the
  loose ledger is essentially the trivial `max <= total`; the real (still dead)
  second-moment content is the §1 floor. **Ledger-independent: dead by
  1,045,396.58 bits at any sharpness including the perfect `Gamma_2 = 1`; any
  per-stratum `L²` refinement is dead by the same floor (§4).**
- **(i) defect-stratified** `OPEN (≡ the crux: no proved g(delta))`. Proved
  inputs (`prop:prefix-rigidity`; PR #397 folding identities): every prefix
  collision has `e >= w+1 = 67472`; a **nonzero** signed folding defect meeting
  all `33736` odd equations has support `>= 33737`. But `33737 < w+1`, so the
  small-defect impossibility only prunes even/quotient collisions **already
  removed** by first-match quotient deletion (net new pruning of the primitive
  residual: **zero**). No proved upper bound on per-defect multiplicity
  `g(delta)` exists; summing over the `~1.9e6` realizable strata reproduces the
  (dead) second moment. The route produces no candidate bound of its own — it
  **is** the open multiplicity certificate; no independent bit-margin.
- **(ii) exchange-compression** `OPEN (≡ the crux: no monovariant)`.
  `prop:mode-null-false` (max fiber ≠ null `z=0`; toy `N_9(0)=672 < N_9(s)=673`)
  sends any mass-to-null compression at the wrong point;
  `prop:twist-orbit`/`prop:q-orbit-moment` give full **equal-mass** twist orbits
  near the max, so a one-swap has no strict monovariant. A controlled one-swap
  ratio bound is exactly the missing **marked-incidence injection**
  `{0,…,67471} × F_p` (PR #397). Reduces to the same certificate; no candidate
  bound.
- **(iv)** see §7 — the crux; not bound by the §1 floor, and not closable by any
  norm inequality either.

---

## 4. Per-stratum corollary (the case flagged never computed) `PROVED`+`EXPERIMENTAL`

A stratum `X` escapes the §1 floor **only if** its total mass
`sum_z X <= K_rem C(n,m) p^{-w/2} = 2^1045476.7`, a `2^-1045396.58` fraction of
all `C(n,m)` supports (`verify` §1). For `D_full_rank_prim` (the generic
residual: a full-rank primitive support with nonzero signed defect) this is
`EXPERIMENTAL`-ly false — it is the **typical** stratum, `sum_z D ~ C(n,m)`
(§6 toy **analogy** + generic-support heuristic; the toys enumerate the full
`N_w` over `mu_n` and do **not** decompose into #397's named strata, so this is
analogy support, not a stratum-level computation). Moreover a total-mass bound
`sum_z D <= 2^1045477` is a **stronger-in-aggregate** form of the missing
certificate — it is *not* implied by the per-target `<= t*p` ask
(`sum_z D <= p^w · t p = 2^2090884`). Net: "per-stratum after first-match
deletion" is dead by the **same** floor unless `D` is anomalously sparse, which
(EXPERIMENTAL) it is not.

---

## 5. Reconciliation with `prop:q-moment-order-floor` (the r ≥ 94196 convention) `AUDIT`

This is the `r=2` instance of `prop:q-moment-order-floor` (grande_finale.tex
L1988), which prints minimum viable order `r >= 94196` for KB-MCA. The lane's raw
recomputation gives `94198.4`; the difference is a **stated margin-convention
choice**, not an error (`verify` §3, both printed):

| convention | Delta_Q | formula | r |
|---|---:|---|---:|
| tex / #384 / #392 (full-budget) | 22.196862 = `log2(B*/avg_ceil)` (`K_raw` regime; printed 22.1969) | `ceil(w log2 p / Delta_Q)` | **94196** |
| this lane (row-sharp) | 22.196107 = `log2 K_rem` | `w log2 p / Delta_Q` (raw real) | **94198.39** |

The decomposition, with **unrounded** margins throughout: the full-budget raw
value is `w log2 p / 22.196862 = 94195.19`; passing to the row-sharp margin
(`log2 K_rem = 22.196107`, i.e. after reserving `t*p = 143763024447376` for the
non-Q first-match cells) shrinks the denominator by `log2(K_raw/K_rem) =
0.000754` bits and inflates `r` by exactly `+3.20`, to `94198.39`. (The tex's
table evaluates with its printed 4-decimal `Delta_Q = 22.1969`, giving
`94195.02` — a `Delta_Q`-rounding effect of `−0.16` on the raw value; the ceil
of either `94195.02` or `94195.19` is the same `94196`.) Both conventions are
correct under their stated `Delta_Q`; this lane's is the tighter/more
conservative floor because it uses the smaller atom-specific usable margin.
**Either way `r=2` is off from viable by a factor ~47,099**, so the `r=2`
verdict of §1–4 is convention-free.

Provenance: PR #384's integrated `cap25_v13_gammar_order_floor.md` (§3) is where
the `94196` table was first printed and independently reproduced to the digit;
PR #392's `cap25_v13_q_moment_floor_reconciliation.md` (+
`verify_q_moment_order_floor_reconciliation.py`) is the precision/convention
reconciliation packet whose two-convention split this section follows.

---

## 6. Toy anchors (exact enumeration; analogy models) `EXACT-COMPUTATION`

Full enumeration over `D = mu_n = F_p^x` of the **full** `N_w` (analogy models —
they do not decompose into #397's named strata); every cell recomputed by
`verify` §4 (`R = p^w max_z N / C(n,m)`, "r=2 overshoot" `= sqrt(Σ N^2)/max N`,
Parseval of the signed-`e_m` identity, best-triangle
`= (C(n,m)+Σ_{c≠0}|e_m(v_c)|)/p^w / max N`):

| field | n | m | w | true R | r=2 overshoot | p^{w/2} | Parseval relerr | best-triangle |
|------|---|---|---|--------|--------------|---------|-----------------|---------------|
| F_17 | 16 | 8 | 1 | 1.001243 | ×4.118 | 4.123 | 0 | ×1.0000 |
| F_17 | 16 | 8 | 2 | 1.212587 | ×14.03 | 17.0 | 0 | ×1.1136 |
| F_17 | 16 | 8 | 3 | 2.672183 | ×27.98 | 70.09 | 1.6e-16 | ×3.9592 |
| F_23 | 22 | 11 | 1 | 1.000001 | ×4.796 | 4.796 | 0 | ×1.0000 |
| F_23 | 22 | 11 | 2 | 1.024357 | ×22.45 | 23.0 | 0 | ×1.0402 |
| F_13 | 12 | 6 | 1 | 1.012987 | ×3.559 | 3.606 | 0 | ×1.0000 |

Readings:
1. **The atom is almost certainly TRUE:** at deployment-representative `w=1` the
   true ratio `R = 1 + o(1)` (e.g. `1.000001` at F_23), orders of magnitude below
   the allowed `K_rem = 4.8e6`. The gap is a **proof-method** gap, not falsity —
   consistent with our PR #407's independently measured concentration constant
   `κ ≤ 1.221`.
2. The `r=2` overshoot equals `p^{w/2}` to 3 decimals at `w=1` — the §1 floor in
   miniature.
3. Hughes's signed-`e_m` reduction is **exact** (Parseval `≈ 0`) in every case;
   the signed `L¹` falls **below** Cauchy–Schwarz (toy `CS/L1` ×1.00→×1.90→×2.71
   at `p=17`, `w=1,2,3`) but far too slowly; the exact-`L¹` best-triangle bound
   is **exactly tight at `w=1`** (overshoot ×1.0000, vs ×4.12 for `L²` — direct
   toy proof that the `L¹` route is *not* bound by the §1 floor) yet loosens
   with `w`. At `w=1`, `Σ_{c≠0}|e_m(v_c)| = p-1` **exactly** (all nonzero `c`
   give `|e_m| = 1` since `f_c` permutes `mu_n`) — verified L1 = 16 / 22 / 12
   for `p = 17 / 23 / 13` — the single Fourier magnitude behind
   `prop:mode-null-false`.
4. #397 anchor reproduced byte-for-byte: `F_17,n16,m8,w1` top fiber **758**, defect
   histogram `{0:70, 4:480, 6:192, 8:16}` — mass lives at **large** defect
   (`b=4,6`), the small-defect thinness is real but not where the mass is.

---

## 7. What the floor covers — and the crux `ANALYSIS` (framing) / `OPEN` (the named input)

Scoped precisely (`ANALYSIS`):

- **Floor instances (PROVED dead, §1–2, §4):** routes (iii/B) and (B′), and every
  `L²`/Plancherel/per-stratum-second-moment refinement — everything that factors
  through `Σ_z X²`.
- **(A) anticode:** separately and unconditionally dead for its own p-independent
  reason (672,081.42 bits above even the abstract floor) — not a floor instance.
- **(i) defect / (ii) exchange:** produce no candidate bound; both reduce exactly
  to the open certificate — `OPEN ≡ crux`.
- **(iv) signed-`e_m` `L¹`:** **not** proven to inherit the floor — the toy §6
  shows it exactly tight at `w=1` where `L²` overshoots by `p^{1/2}`. But closing
  it needs the **average** `|e_m(v_c)|/C(n,m) <= 2^-2090815.3` over the
  `p^w−1 = 2^2090837.5` nonzero directions — pure cancellation no per-`c`
  estimate reaches; and its only norm-inequality specialization (Cauchy–Schwarz
  on the `c`-sum) is exactly route (iii), floor-dead. So (iv) is the crux, not a
  floor victim.

The exact Fourier identity behind (iv) (grande_finale.tex `prop:fourier-audit`;
Parseval-exact in §6):

```
Rhat(c) = e_m(v_c),  v_c = (exp(2πi f_c(a)/p))_{a in mu_n},  f_c = Σ_{i=1}^w c_i x^i,
max_z N_w(z) <= p^{-w}( C(n,m) + Σ_{c≠0} |e_m(v_c)| ).
```

> **Missing input (max-fiber signed-`e_m` inverse theorem) `OPEN` — THE CRUX.**
> After first-match deletion of the quotient/planted/generated/RIM-rank-drop/BC/SP/
> extension branches, `e_m(v_c)` is **negligible for all but a `poly(n)`-controlled
> set of directions `c`**, so that `Σ_{c≠0} |e_m(v_c)| <= (K_rem-1) C(n,m)`.

This input is:

- the **r-free (max-fiber) analog** of the tex's own open `prob:entropy-inverse-q`
  (grande_finale.tex L823) and its `rem:entropy-inverse-skeleton`; connected to it
  asymptotically by `thm:logmoment-equivalence` but **not** at the finite row,
  where the moment route needs `r >= 94198` (§5) with no `Gamma_r` ledger at such
  `r`;
- on the **signed `e_m` column**, **not** the power-sum `pi_odd` column that PR
  #398's approximate-freeze families refute (they inflate `pi_odd`, not `e_m`), and
  **not** PR #402's `x4b_moment_trade_exclusion` `k`-cap (a different moment
  column) — so neither #398 nor #402 is an obstruction to it;
- **strictly the same content as PR #397's** "primitive full-rank signed-defect
  multiplicity" certificate, viewed on the Fourier side.

This answers the "strengthen moment methods beyond `prop:q-moment-order-floor`"
question in the **negative-with-exact-margins** direction for everything that
factors through the second moment, and names what CAN close the atom.

---

## 8. Weave `AUDIT`

- **PR #397** (`pr-397`; `rowsharp_q_prefix_atom_reductions_v1`): this packet
  consumes its additive stratum bound (`G_gen_support`, `D_full_rank_prim`,
  `E_ret ≤ 11440`) and proved reductions (Newton equivalence, Q1 distance
  `e ≥ w+1`, marked-incidence injection, small signed-defect impossibility). Its
  missing full-rank support certificate **is** the §7 crux, viewed on the Fourier
  side. Our audit comment and avdeev's fix are already on that thread.
- **Hughes** (comment on the PR #397 thread): the signed-`e_m` Fourier reduction of
  §6–7 is **his** observation; this packet independently verifies it
  (Parseval-exact) and sharpens it to the exact `L¹` target — it is recorded as
  the precise open input, not claimed as new.
- **PR #398 / #402**: non-conflation — §7's signed-`e_m` column is disjoint from
  #398's `pi_odd` power-sum column and from #402's `x4b` `k`-cap moment column.
- **PR #384 / #392**: #384's integrated `cap25_v13_gammar_order_floor.md` first
  printed (and proved unconditional) the `94196` order-floor table; #392's
  `cap25_v13_q_moment_floor_reconciliation.md` (+
  `verify_q_moment_order_floor_reconciliation.py`) is the precision/convention
  reconciliation whose two-convention split §5 follows.
- **PR #407** (ours): its measured `κ ≤ 1.221` is consistent with the toy `R ≈ 1`
  of §6 (the atom is almost certainly true; the wall is proof-method).
- **#395** (`bc-l4-curve-second-moment`): the coordination brief carried an
  **unsourced** "route iii died globally ~1e5 bits" figure into this lane; it did
  **not reproduce** — the exact intrinsic `r=2` floor gap at the KB row is
  **1,045,396.58 bits** (§1). #395's own `~1e5`-bit figures are its **L4-row
  (`w=4216`) audit ceilings vs equidistribution** (best: #393 `p`·packing
  `2^103841.23` vs its equidistribution heuristic `S1 = 2^23.14`, a gap of
  ≈103,818 bits; also C1 `2^130686.93`, C2 `2^130693.92`/`2^121743.02`) — a
  **different quantity** (curve-restricted, equidistribution-normalized, different
  row and target), **not an instance of this floor**, and no identification is
  claimed. For context only: `(w/2) log2 p` at `w=4216` is `65,324.15` bits.
- **PR #409** (DannyExperiments, draft, opened 2026-07-07 21:32Z, "Add CAP25 Q
  logmoment mass-aware audit"): a `τ`-mass correction to
  `prop:q-moment-order-floor`'s `Γ_r ≥ 1` Hölder step (the correct floor is
  `τ^r`, `τ = |P|/C(n,m)`, for **pruned primitive-residual** moments) plus a
  route-cut of raw `prob:entropy-inverse-q`. **Non-conflicting** with this
  packet: §1–2 here bound moments of the **full** `N_w` (`τ = 1` by
  construction) and reach `R_prim` only via the pointwise `R_prim ≤ N_w`; and
  the per-stratum floor (§4) already carries the stratum's mass factor
  `sum_z X` explicitly.

### One-line verdict
Every route that bounds `max_z` through the second moment (`r=2` /
Cauchy–Schwarz / Fourier-Plancherel) is DEAD at the deployed row on the intrinsic
`p^{w/2}` concentration floor — 1,045,396.58 bits above `K_rem·avg` for the
full-mass target, rigorously; and per-stratum unless `D_full_rank_prim` carries a
`2^-1045396.58` fraction of all supports (`EXPERIMENTAL`: it does not, §4).
Anticode is separately dead (p-independent); defect and exchange-compression
reduce to the open certificate. The toys show the truth is `R ≈ 1`, so the wall
is the missing signed-`e_m` inverse/sparsity theorem (= PR #397's full-rank
certificate, Fourier side) — the one route not floor-bound, and the named crux.
