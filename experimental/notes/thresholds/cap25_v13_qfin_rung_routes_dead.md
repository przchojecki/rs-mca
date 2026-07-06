# CAP25 v13 raw: conj:Q rung routes — exact dead margins (KB-MCA)

Status: `ROUTE-CUT` / `EXACT_MARGINS` / `PROVED-LOCAL(H1 as a bound, H2 as a
ceiling)` / `AUDIT`.

**Data:** `experimental/data/certificates/frontier-adjacent/kb_mca_conjq_route_margins_v1.json`.
**Verifier:** `experimental/scripts/verify_conjq_rung_routes_dead.py`
(zero-arg, `--tamper-selftest` supported).

**What this is.** `experimental/notes/thresholds/cap25_v13_qfin_rung_audit.md`
(the integrated `conjQ_rung_audit` packet) reduces the KB-MCA v13 raw safe row
`(1116047, 1116048)` to the subset-primitive `conj:Q` core (`L_0`, depth
`w=67471`) plus a four-rung descent ladder `L_1..L_4` (`row_s =
(n/2^s, m/2^s, floor(w/2^s))`, `s=1..4`), every rung `RESIDUAL`/`BELOW`/
`VACUOUS` against the shared bar `rho_s <= K_raw = 2^22.196861`. That audit
proves the *ladder shape* is correct and cheap; it leaves *bounding* each
`Pi_s` (`s=0..4`) as five open reductions. This note asks the next question:
are there any cheap, generic routes that already close one of those five
bounds? It runs the three cheapest candidates — a distance-only packing
bound (`H1`), the proved head-flatness ceiling (`H2`), and a low-moment
bridge (`grande_finale.tex \label{thm:moment-q}`) — against all five rungs
`L_0..L_4`, with exact printed margins, and finds all three **dead
everywhere**, not merely at the primitive core. It also records **one
strategic correction** to how the integrated rung audit's own frame verdict
should be read (§2): the ladder's rungs do not get closer to the proved
head-depth base cases as they get shallower; head-reach degrades in lockstep
with the required depth, so every rung is equally far from it, and the
shallowest rung (`L_4`) is in fact the *worst* case. This is a correction to
a reading, not to any integer, verdict, or proof already shipped.

This note does **not** prove or refute `conj:Q`
(`grande_finale.tex \label{conj:Q}`), does **not** prove `U(1116048) <= B*`,
and does **not** move the frontier edge. It does not modify
`kb_mca_conjq_rung_audit_v1.json`, its companion note, or any of their
verdicts or integers — the new material ships as sibling files.

---

**Label migration (grande_finale.tex was promoted at upstream e749e9e AFTER
this PR was filed):** the conjecture environments were removed; `conj:Q` ->
the formal open Problem `prob:row-sharp-q`; `conj:BC` -> `prob:saturated-bc`
(now requiring saturated line-ray dedup accounting per
`prop:line-ray-saturation`); `thm:asymptotic` and the `R_Q(n) = e^{o(n)}`
soft form were REMOVED outright, and `thm:q-implies-sp` eliminates SP as an
independent target. `rem:head-does-not-close-q`, `cor:head-q`,
`thm:head-flatness`, `thm:moment-q`, and every §4 reduction this note uses
SURVIVE unchanged. Independent corroboration: the promoted note's own
`prop:proper-q-gap` records ~1.66e6 allowed bits vs the 22.2-bit budget at
the KB rows — the same order this note's H1 margins establish by a
different (anticode) formula. Citations below were written against the
pre-promotion text; apply this mapping.

## 1. H1 — the packing bound, and its exact margin

**Statement.** For every target `z` (primitive or not),
```text
|Phi_w^{-1}(z)| <= C(n, m-w) / C(m, w),
```
which is `grande_finale.tex \label{cor:anticode-cap}`, **already PROVED** in
the manuscript as a corollary of `\label{prop:prefix-rigidity}`. For the
`n = 2k` ladder rows (every `L_s` here has `n_s = 2 k_s`), this collapses
algebraically to the clean form
```text
rho(z) = |Phi_w^{-1}(z)| / avg  <=  p^w / C(k-1, w).            (H1*)
```
`H1` in this note is *not* a new theorem: it is `cor:anticode-cap` /
`prop:prefix-rigidity` specialized to the five-rung ladder, with the exact
margin against the shared bar computed at every rung.

**Proof sketch.** Distinct `M, M'` in one fiber share the first `w` power
sums, hence (Newton, `p > w`) the first `w` top locator coefficients;
`prop:prefix-rigidity` gives `|M \ M'| = |M' \ M| >= w+1`, so
`|M cap M'| <= k = m-w-1`. No `(k+1)`-subset lies in two fiber members
(Johnson/Fisher/Deza–Frankl packing: count pairs `(R, M)` with `R subset M`,
`|R| = m-w`), giving `|Phi_w^{-1}(z)| <= C(n, k+1)/C(m, k+1) = C(n,m-w)/C(m,w)`;
the `n = 2k` binomial algebra collapses this to `(H1*)`. Toy-verified exactly
(verifier gate ii, exhaustive enumeration on 5 toy rows): rigidity holds,
packing holds, and on the one `n = 2k` toy row the underlying identity
`C(k-1,w)*C(n,m-w) == C(n,m)*C(m,w)` holds **exactly** (integer equality),
confirming `(H1*)` is an algebraic identity, not an approximation.

**THE MARGIN.** Big-int exact recompute of `log2(rho_bound)` at all five
rows, against the ladder bar `log2(K_raw) = 22.196861429`:

| rung | `w` | `k-1` | `log2(p^w)` | `log2 C(k-1,w)` | `log2(rho_bound)` | over the bar by |
|---|---:|---:|---:|---:|---:|---:|
| `L_0` | 67471 | 1048575 | 2090837.545 | 361181.146 | **1729656.399** | **1729634.202** |
| `L_1` | 33735 | 524287 | 1045403.278 | 180584.444 | 864818.833 | 864796.637 |
| `L_2` | 16867 | 262143 | 522686.145 | 90286.344 | 432399.801 | 432377.604 |
| `L_3` | 8433 | 131071 | 261327.578 | 45137.544 | 216190.034 | 216167.838 |
| `L_4` | 4216 | 65535 | 130648.295 | 22563.393 | **108084.901** | **108062.704** |

At `L_4`, `log2(rho_bound) = 108,085` bits against the `22.197`-bit bar — over
by `108,063` bits. At `L_0`, the core itself is over by `1.73` million bits.

**The exact breaking point.** Per unit depth, the bound yields
`log2 C(k-1,w) / w ~ 5.35` bits (pure combinatorial entropy: `(k/w) H(w/k)`
with `H(w/k) ~ 0.344`; the per-depth rate is flat across all rungs,
25.636-25.637 bits of deficit),
against `avg`'s `log2 p = 30.99` bits/depth — a deficit of `~25.64` bits/depth
at every rung (`25.636` at `L_0`, `25.637` at `L_4`; flat across the entire
ladder to three decimal places, not shrinking as the rungs get shallower).
This is **structural, not slack**: extremal
constant-weight codes of distance `2(w+1)` genuinely have `~2^{k H(w/k)}`
words; the arithmetic constraint "power sums live in `F_p`" is invisible to
Hamming geometry — `H1` never sees the field size `p`. Consequences:

- **Singleton / Johnson / RCW / Delsarte-with-distance-only** are all
  `<= H1`, hence all **DEAD**.
- **Plotkin** is inapplicable: it needs `d/n ~ 1/2`; here
  `d/n = 2(w+1)/n ~ 0.064` at every rung.
- **Primitivity gives no rescue**: `cor:anticode-cap` already holds for
  every `z` (primitive or not), and the `~10^5`–`10^6`-bit gap dwarfs any
  conceivable primitive discount.

**Verdict: the cheapest structural route is provably `~10^5` bits (`L_4`) to
`~10^6` bits (`L_0`) too weak, at every rung.**

---

## 2. H2 — the head-flatness ceiling, and its ladder degradation

**Statement.** `grande_finale.tex \label{thm:head-flatness}` at `ell=0` (no
planted points) is nonvacuous exactly for
```text
w <= w_head(n,m) := floor( (n-m) / ceil(sqrt p) ).
```
`H2` here is `thm:head-flatness` specialized per rung, solved exactly for
`w_head`, not a new theorem. Two independent derivations agree at all five
rows: the closed form above, and an exact per-`w` search of the theorem's own
nonvacuity inequality (error term `<` main term). At the deployed `L_0` row
this gives `w_head = 21` **exactly**, matching
`\label{cor:head-q}`'s proved `w<=21` at the deployed row to the integer.

**The per-character Weil barrier.** `thm:head-flatness` pays one `sqrt(p)`
loss per active power-sum direction (Weil's bound for a nonconstant additive
character sum); this is exactly why it reaches only `w<=21` at the deployed
row while the row needs `w~67471`
(`grande_finale.tex \label{rem:head-does-not-close-q}`: "the next Q target is
therefore not a uniform per-character bound"; composite Fourier directions
are quotient-scale by `\label{prop:composite-descend}`, and primitive
character maxima face the usual Parseval square-root barrier).

**THE LADDER DEGRADATION TABLE.**

| rung | `w` needed | `w_head` (exact, both derivations agree) | needed / ceiling |
|---|---:|---:|---:|
| `L_0` | 67471 | **21** | 3212.9x |
| `L_1` | 33735 | 10 | 3373.5x |
| `L_2` | 16867 | 5 | 3373.4x |
| `L_3` | 8433 | 2 | 4216.5x |
| `L_4` | 4216 | **1** | **4216.0x** |

`w_head ~ (n-m)/sqrt(p) ~ k/sqrt(p)`: `n` halves each rung but `sqrt(p)` is
fixed, so `w_head` halves in lockstep with the required depth. The ratio
stays `~3200x`–`4200x` and **never improves** — the shallowest rung is not the
easiest. Worse, the stated consequence is exact at the terminus: the 2-adic
symmetric descent hard-caps at `s=4` (`v2(m_safe)=4`; `L_4`'s `m_4 = 69753` is
**odd**, so it admits no further descent), where head-reach is `w_head=1`
against the needed `w=4216` — **a gap that is exactly `4216x`** at the
terminus (not merely "about"), and it is the worst ratio on the ladder, not
the best.

**This corrects the aspirational reading of the integrated rung audit.**
`cap25_v13_qfin_rung_audit.md` §6 states `L_s` is "a REDUCTION in depth only
(`w_s = w/2^s`, **halving toward the proved head-depth base cases**,
`rem:proved-q-part`), not a weakening of the flatness requirement"; §7
(quoting the Lane C compiler design note) similarly reads the ladder as a
"descent LADDER whose rungs step the depth `w` down by factors of two
**toward** the proved head-depth base cases (`w<=21`)". The table above shows
neither framing holds: the base case itself (`w_head`) halves at the *same
rate* as the required depth, so no rung gets closer to head-reach than any
other — **all rungs are equidistant (`~3200x`–`4200x`) from head-reach; the
base does not scale with the rungs, and the multiscale scaffold does not
connect to the proved head-depth base cases at any rung.** This is a
correction to how the existing ladder should be read (a proof-route
observation), not a change to any integer, verdict, or proved fact already
shipped by that audit — `(D)`, the 22 rung verdicts, and the
conservative-rounding aggregate are all untouched.

---

## 3. Moments at `L_4` — dead, quantified

`grande_finale.tex \label{thm:moment-q}` gives `R <= exp((A+B)/r)`; at the
optimistic case `log2(Gamma_r) ~ 0`, closing a target budget `Delta` needs
moment order `r = ceil(w log2(p) / Delta)`. At `L_4` (`w=4216`,
`log2(p)=30.989`):

```text
r >= 5886   at the shared ladder bar (Delta = log2(K_raw) = 22.197 bits),
r >= 3756   at L_4's own standalone budget (Delta = 34.793 bits).
```

Available depth via `H2` at `L_4` is `w_head = 1`. Even at the most generous
standalone budget, the moment bridge needs `r>=3756` — short by a factor of
`~3750`–`5900` against the provable order. **Dead.**

---

## 4. What remains live (cite-only; no new claims here)

- **the saturated primitive split-pencil line-ray target** (now the formal
  open Problem `prob:saturated-bc`; formerly `conj:BC`,
  the Work-Plan "BC program"). `L_4`'s row is structurally the cleanest
  target for it: `m_4 = 69753` is **odd**, so `v2(m_4)=0` and every member of
  `L_4`'s fiber is subset-primitive — the entire fiber is the `s=0` case, with
  **zero ladder/quotient correction term**. Counting locator factorizations
  `Lambda_M = G*A` with fixed top-`w` coefficients via divisor bounds sees `p`
  directly, exactly where the Weil/Parseval cancellation behind `H2`'s barrier
  does not. This is the Work-Plan's own recommendation ("preferably KoalaBear
  MCA because its `22.2`-bit margin is the most forgiving"); this note adds
  only the observation that `L_4` is the cleanest row within KB-MCA for it.
- **The multilevel Q max-fiber target** (now the formal open Problem
  `prob:row-sharp-q`). NOTE: the softer `R_Q(n) = e^{o(n)}` form quoted
  below was REMOVED in the promotion — kept here as the pre-promotion
  context this note was written against:
  `conj:Q`'s own statement (`\label{conj:Q}`) records that
  "for the asymptotic frontier it suffices that `R_Q(n)=e^{o(n)}`, or even
  `poly(n)` with logarithmic agreement reserve" — a target that sidesteps the
  finite `2^22.197` bar entirely. `\label{thm:asymptotic}` ("asymptotic
  closure from Q, BC, and SP") is the theorem that cashes this softer form in,
  assuming `Q`, `BC`, `SP` in their `e^{o(n)}` forms uniformly. A
  fourth-moment / large-sieve "few-heavy-fibers" estimate for `Phi_w` at fixed
  rate targets this softer statement, not the finite row bound this note
  closes off. (Label verification: both `\label{conj:Q}` and
  `\label{thm:asymptotic}` exist verbatim in `grande_finale.tex`; the
  `R_Q(n)=e^{o(n)}` clause is part of `conj:Q`'s own statement, and
  `thm:asymptotic` is the downstream closure theorem that consumes it — cited
  together above, not conflated.)

---

## 5. Non-claims

This note does **not** prove any of the following:

```text
conj:Q (grande_finale.tex \label{conj:Q}),
U(1116048) <= B*,
that the frontier edge (1116047, 1116048) moves in either direction,
any bound on L_1, L_2, L_3, L_4, or the conj:Q core (all remain OPEN reductions).
```

It does **not** alter the `GREEN`/`BELOW`/`RESIDUAL`/`VACUOUS` verdicts, the
22-rung table, the descent identity `(D)`, or any integer of
`cap25_v13_qfin_rung_audit.md` / `kb_mca_conjq_rung_audit_v1.json`. The
strategic correction of §2 is about **proof-route selection and how the
existing ladder relates to head-reach** — it is not a correction to that
audit's ledgers, its arithmetic, or its verdicts, all of which stand as
shipped. It does **not** touch `conj:BC` or `conj:SP` beyond citing them as
still-live targets (§4).

---

## 6. Verifier contract

`experimental/scripts/verify_conjq_rung_routes_dead.py` is zero-arg,
stdlib-only, deterministic, and supports `--tamper-selftest`. Four gates:

- **gate i** — H1 packing bound: independently re-derives `K_raw` from raw
  constants (`comb(N,M_SAFE)`, exact big-int, the dominant ~15s cost), then
  recomputes `log2(rho_bound) = w log2(p) - log2 C(k-1,w)` and its margin over
  `log2(K_raw)` at all five ladder rows, diffing against the shipped JSON.
- **gate ii** — H1 toy validation: exhaustive fiber enumeration
  (independent reimplementation) on 5 toy rows, checking rigidity
  (`|M\M'|>=w+1`), the packing bound itself (via exact `Fraction`
  arithmetic), and the exact `n=2k` clean-form identity
  `C(k-1,w)*C(n,m-w) == C(n,m)*C(m,w)`.
- **gate iii** — H2 boundary: recomputes `w_head` two independent ways
  (closed form and exact nonvacuity search) at all five rows, checks they
  agree, checks the degradation table is exactly `(21,10,5,2,1)`, and checks
  the gap ratio never leaves `[3000,4300]`x and is exactly `4216.0`x at `L_4`.
- **gate iv** — moment-order arithmetic at `L_4`: recomputes `r=5886` (ladder
  bar) and `r=3756` (standalone) from `w=4216`, `log2(p)`, and the two
  budgets.

Expected runtime under 60s (dominated by gate i's `comb(N,M_SAFE)`); expected
exit code `0`. A nonzero exit code means a genuine arithmetic mismatch in
this PR, not a judgment about `conj:Q` itself.

---

## Refs

- `experimental/grande_finale.tex` — `\label{conj:Q}`, `\label{cor:anticode-cap}`,
  `\label{prop:prefix-rigidity}`, `\label{thm:head-flatness}`,
  `\label{cor:head-q}`, `\label{rem:head-does-not-close-q}`,
  `\label{prop:composite-descend}`, `\label{thm:moment-q}`,
  `\label{conj:BC}`, `\label{thm:asymptotic}`, and the Work-Plan "BC program"
  paragraph.
- `experimental/notes/thresholds/cap25_v13_qfin_rung_audit.md` — the 5-rung
  ladder, the descent identity `(D)`, the 22-rung table, and the frame
  verdict corrected by §2 above (not otherwise touched).
- `experimental/notes/thresholds/cap25_v13_qfin_primitive_wall_synthesis.md`
  — the rigidity input, the moment barrier, and the wall this note's three
  routes all fail to close.
- `experimental/data/certificates/frontier-adjacent/kb_mca_conjq_rung_audit_v1.json`
  — the sibling packet (not modified by this PR).
- `experimental/data/certificates/frontier-adjacent/kb_mca_conjq_route_margins_v1.json`
  — this note's data.
- `experimental/scripts/verify_conjq_rung_routes_dead.py` — this note's
  verifier (§6).
