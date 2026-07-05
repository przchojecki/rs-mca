# L1: key lemma `E_3 <= ell-2` refuted; frontier vacancy half refuted at `ell in {11,13,17,23}`

**Type: first-class NEGATIVE result (self-correction of our own integrated note).**
Per `agents.md` ("a negative result is still a resolution if it identifies the new
obstruction floor and updates the certificate logic") this note supersedes two
load-bearing claims of the integrated note
`experimental/notes/l1/l1_prime_ell_frontier_corrected.md`:

- its **KEY LEMMA (§3)** `E_3 <= ell-2` (equivalently `delta <= K`, `E_3 + dim U <= ell`), and
- the **lower/VACANCY half (§4)** of `m*(ell) = (ell+3)/2` (`top-m < 2ell` for all `m <= (ell+1)/2`),

which are **REFUTED**. Everything the integrated note labels PROVED or UNCONDITIONAL
(the toolkit of §2, the witnesses of §5, the `ceil(2ell/3)` refutation of §0) **SURVIVES**;
see §4. **Ground rule honored:** this note does *not* edit the integrated note or its
verifier `experimental/scripts/verify_l1_prime_ell_frontier_corrected.py`; that verifier
still exits 0 on every gate and its tamper self-test still catches every flip (re-run
below, independently, twice) — the refutation lives *outside* the region its bounded
gate-iv sweep explores. Filed at
`experimental/notes/l1/l1_prime_ell_key_lemma_refuted.md`. Companion zero-arg verifier:
`experimental/scripts/verify_l1_key_lemma_refuted.py` (stdlib, deterministic, exit 0
iff all gates pass; `--tamper-selftest` flips one datum per gate and confirms each
then fails). Companion constructor: `experimental/scripts/l1_bigfiber_e3_search.py`
(the plant-big-fibers-then-exact-solve search that finds these counterexamples from
scratch — by default it independently re-derives fresh violations at `ell=11,p=67`
and `ell=13,p=79`, not merely replays the stored coefficients below).

Notation is inherited from the integrated note. `ell` odd prime, `ell | p-1`,
`n = (p-1)/ell` cosets, `Gamma(X) = sum_{r=1}^{ell-1} gamma_r X^r` constant-free mixed;
per coset `mu_b` = max fiber (level-set) size; spectrum = the `mu_b` sorted descending;
`E_3 := sum_b (mu_b - 2)_+`; `top-m` = sum of the `m` largest `mu_b`; listing threshold
`top-m >= 2ell` at onset `m = t+1`. All arithmetic exact over `F_p`, stdlib only.

**Status legend:** COUNTEREXAMPLE (refuted, explicit object) / AUDIT (root cause,
independently observed) / EXPERIMENTAL (well-supported, not proved) / SURVIVES (unchanged).

---

## 0. Headline

1. **COUNTEREXAMPLE — the KEY LEMMA `E_3 <= ell-2` is FALSE** at `ell in {11,13,17,19,23}`,
   by six explicit, from-scratch-verified mixed `Gamma` on the non-collinear `K >= 3` chart
   (§1). Observed maxima: **`E_3 = ell-1`** at `ell in {11,13,17}` and **`E_3 = ell`** at
   `ell = 23` (`p = 139`) — so even the fallback `E_3 <= ell-1` is violated at `ell = 23`.

2. **COUNTEREXAMPLE — the frontier VACANCY half is FALSE at every tested `ell >= 11`**
   (`ell in {11,13,17,23}`). At each, an explicit `E_3 = ell-1` config lists a full
   `lambda`-free primitive-mixed minimal kernel codeword at `m = (ell+1)/2 < m*(ell) = (ell+3)/2`,
   passing **all 16 gates** of the integrated verifier's own `run_witness_chain` (§2): `ell=13,
   p=313 m=7`; `ell=11, p=331 m=6` (replicated across 11 distinct `Gamma` at `p in {199,331}`);
   `ell=17, p=409 m=9` (the note's own full-witness prime); and `ell=23, m=12` cross-prime
   replicated at `p=599` and `p=691` (large `n`; the expensive `L5_minimal` gate confirmed
   offline this session, the other 15 gates live). Hence **`m*(ell) <= (ell+1)/2`** at
   `ell in {11,13,17,23}` — one stratum below the claimed onset. `ell = 7` is **unaffected**
   (Theorem R keeps `m*(7) = 5 = (ell+3)/2`; its `(ell+1)/2 = 4` band is a *proved* vacancy).

3. **What this does NOT touch (§4):** the reduction-chain identities (they hold *on* the
   counterexamples — the chain is internally correct, only its endpoint `delta <= K` is false),
   the pairwise cap, the collinear/`det-M`/`L9` no-gos, Theorem R (the `ell = 7` band), the §5
   upper-half witnesses (they list at `(ell+3)/2`, hence certify `m* <= (ell+3)/2` — an existence
   fact that more listings *below* only strengthen), and the refutation of `ceil(2ell/3)` (the
   true onset is even *lower*, so it is refuted a fortiori).

The KEY LEMMA was the integrated note's "single OPEN core." **It is not open; it is false.**
All proof routes aimed at it (`V`-sum, residue-bridge `Psi`, `c`-Veronese extension of L9) were
attacking a false statement.

---

## 1. COUNTEREXAMPLE — `E_3 <= ell-2` refuted (`ell in {11,13,17,19,23}`)

Each `Gamma` below is a valid constant-free mixed polynomial (`deg <= ell-1`) whose spectrum,
`E_3`, and `top-m` are recomputed here **from scratch** (grouping `F_p^*` by `x^ell`, no import
of any inherited script; reproducer §7). `K` = number of cosets carrying the extremal fiber
(the spread), `delta` = rank drop `dim(D cap Z)` of that fiber config; both from the input
reconstruction, where the reduction identities were verified (§4).

| `ell` | `p`  | `n` | spectrum (head)                     | `E_3` | `ell-2` | `ell-1` | `K` | `delta` | reading |
|------:|-----:|----:|:------------------------------------|:-----:|:-------:|:-------:|:---:|:-------:|:--------|
| 11 | 67  | 6  | `[8,3,3,3,3,2]`                       | **10** | 9  | 10 | 6 | 7 = `K+1` | `E_3 = ell-1` |
| 11 | 199 | 18 | `[7,4,3,3,3,1,...]`                   | **10** | 9  | 10 | 5 | 6 = `K+1` | `E_3 = ell-1`, large `n` |
| 13 | 79  | 6  | `[6,6,6,2,2,1]`                       | **12** | 11 | 12 | 5 | 6 = `K+1` | `E_3 = ell-1` |
| 13 | 313 | 24 | `[8,5,3,3,3,2,2,2,2,2]`               | **12** | 11 | 12 | 10| 11 = `K+1`| `E_3 = ell-1`; note's own prime; **`m=7` lister (§2)** |
| 17 | 103 | 6  | `[10,7,3,3,3,2]`                      | **16** | 15 | 16 | 6 | 7 = `K+1` | `E_3 = ell-1` |
| 19 | 191 | 10 | `[11,8,4,3,2,2,1,...]`                | **18** | 17 | 18 | 10| 11 = `K+1`| `E_3 = ell-1`; `m=10` listing OPEN |
| 23 | 139 | 6  | `[13,10,4,3,3,2]`                     | **23** | 21 | 22 | 6 | 8 = `K+2` | **`E_3 = ell`**: fallback `E_3 <= ell-1` ALSO violated |

Explicit `Gamma` (coefficients of `X^1 .. X^{ell-1}`), verbatim from the refutation input:

```
ell=11 p=67 : [43,44,38,44,17,18,42,44,65,1]
ell=11 p=199: [21,144,71,171,42,10,12,115,173,1]
ell=13 p=79 : [23,71,3,40,40,2,46,40,67,69,71,1]
ell=13 p=313: [185,42,295,307,71,257,218,32,90,290,279,1]
ell=17 p=103: [27,7,1,74,35,11,86,96,66,44,7,96,5,48,72,1]
ell=19 p=191: [16,44,177,106,79,157,14,155,11,181,151,28,126,22,142,23,1,1]
ell=23 p=139: [60,80,118,60,48,137,123,101,89,94,15,23,21,88,134,5,48,8,124,42,77,1]
```

**Independently reconfirmed here (from-scratch, no inherited imports):** every spectrum head
and `E_3` value in the table reproduces **exactly**; `E_3 > ell-2` at all six; `E_3 > ell-1`
at `ell = 23`. The **pairwise cap survives on every counterexample** — the top-two `mu`'s sum
to `11, 11, 12, 13, 17, 23`, each `<= ell`, several at equality — so the counterexamples break
only the *aggregate* `E_3 <= ell-2`, never the pairwise bound (consistent with §4: what is
false is the leap from the pairwise/collinear sub-lemmas to `delta <= K`).

> **STATUS: COUNTEREXAMPLE.** `E_3 <= ell-2` refuted at `ell in {11,13,17,19,23}`;
> `E_3 <= ell-1` additionally refuted at `ell = 23`. At `ell = 19` (row added
> post-panel from the H19 hunt, PI-verified from scratch) the `m = 10` LISTING
> question remains OPEN: p = 191 has `n = 10 < 2m-1 = 19` (too small to list),
> and every larger-`n` prime swept stayed at `E_3 <= ell-2` within the search
> budget — a budget cap, not evidence of vacancy.

---

## 2. COUNTEREXAMPLE — frontier vacancy half refuted at `ell in {11,13,17,23}`

The integrated note's lower half reads: *`top-m < 2ell` for all `m <= (ell+1)/2`* (VACANCY
THEOREM, "rigorous modulo the KEY LEMMA"). It is refuted at **every tested `ell >= 11`** by an
explicit full listing at `m = (ell+1)/2`. We first give the flagship `ell = 13` case in full
detail (with its controls), then tabulate the three further `ell` (§2.2). Take the `p = 313`
counterexample, `E_3 = 12`, full spectrum `[8,5,3,3,3,2,2,2,2,2,1^14]` (`n = 24`):

```
top-6 = 24 < 26          (would-be vacant at m = 6)
top-7 = 26 = 2*13 = 2ell (m = 7 = (ell+1)/2)   <-- vacancy VIOLATED
n = 24 >= t + m = 2m-1 = 13 cosets available   <-- codeword assemblable
```

Running the integrated verifier's own machinery (imported unchanged):
`run_witness_chain(gamma=[185,42,295,307,71,257,218,32,90,290,279,1], p=313, ell=13, m=7)`
returns `lam_free=True`, `full=True`, **all 16 gates True**:

```
L1_topm>=2ell  cosets_distinct  LF_map_zeroconst  LF_rank_m_surjective
LF_c_distinct_nonzero  L3_degP<=m*ell  L3_mixed  L3_petal_full
L4_R>=2ell  L4_agreements>=s  L4_retained==maxfiber  dom_distinct_pts
L5_M_kernel  L5_identity  L5_minimal  L6_primitive_mixed
```

with retained core profile `[8,5,3,3,3,2,2]`, `R = 26 = 2ell`, `deg P <= m*ell = 91`,
minimal primitive-mixed missed core `|M| = 65`. This is a full, `lambda`-free, primitive
mixed **minimal kernel codeword LISTING at `m = 7 = (ell+1)/2`, below the claimed onset
`m* = (ell+3)/2 = 8`**. Therefore **`m*(13) <= 7`**, and the note's `m*(13) = 8` and its
`m <= 7` vacancy are FALSE at `ell = 13`.

**The gates have teeth (controls, all reproduced here):** the *same* config at `m = 6` is
NOT full (`top-6 = 24 < 26`, 13/16 gates); the note's *own* certified `m = 8` witness
`gamma = [254,289,...,133,1]` at `m = 7` is NOT full (its `top-7 = 25 < 26`) but IS full at
`m = 8` (reproducing the note's witness); the concentrated `Gamma = X + ... + X^{12}` at
`m = 7` is NOT full (`top-7 = 18`). The verifier's `--tamper-selftest` still catches every
gate flip. So the all-16-True verdict on the `p = 313` config is a genuine listing, not a
vacuous pass. The single structural difference from the note's witness is `E_3`: `12` vs `11`,
i.e. `top-7 = 26` vs `25`. The note believed `m*(13) = 8` because its search never produced
`E_3 = 12` (so `top-7` was stuck at `<= 25`).

### 2.2 The other three `ell` list at `m = (ell+1)/2` too

The same phenomenon — an `E_3 = ell-1` config whose `top-m` first reaches `2ell` exactly at
`m = (ell+1)/2` — now has an explicit **full `run_witness_chain` listing** at `ell in {11,17,23}`,
each recomputed from scratch here and re-run through the integrated verifier's own 16-gate chain:

| `ell` | `p`  | `n`  | `m=(ell+1)/2` | spectrum (head)              | `E_3` | `top-m` | `top-(m-1)` | `run_witness_chain` |
|------:|-----:|-----:|:-------------:|:-----------------------------|:-----:|:-------:|:-----------:|:--------------------|
| 11 | 331 | 30 | 6  | `[8,3,3,3,3,2,1,...]`            | `10 = ell-1` | `22 = 2ell` | `20 < 22` | **all 16 gates True** |
| 17 | 409 | 24 | 9  | `[9,8,3,3,3,2,2,2,2,2,1,...]`    | `16 = ell-1` | `34 = 2ell` | `32 < 34` | **all 16 gates True** |
| 23 | 599 | 26 | 12 | `[13,10,4,3,2^14,1^8]`          | `22 = ell-1` | `46 = 2ell` | `44 < 46` | **16 gates True** (15 live + `L5_minimal` offline) |
| 23 | 691 | 30 | 12 | `[13,10,3,3,3,2^12,1^13]`       | `22 = ell-1` | `46 = 2ell` | `44 < 46` | **16 gates True** (15 live + `L5_minimal` offline) |

Explicit `Gamma` (coefficients of `X^1 .. X^{ell-1}`), each producing a full, `lambda`-free,
primitive-mixed **minimal kernel codeword listing** at `m = (ell+1)/2` via the integrated
`run_witness_chain(gamma, p, ell, m)`:

```
ell=11 p=331 m=6 : [11,165,196,237,31,40,171,236,246,1]
ell=17 p=409 m=9 : [80,5,360,87,283,89,358,379,216,174,67,329,68,317,398,1]
ell=23 p=599 m=12: [327,192,175,17,298,200,474,496,95,354,502,222,509,213,417,173,98,207,106,381,328,1]
ell=23 p=691 m=12: [524,614,310,539,294,303,425,653,551,564,145,271,332,503,117,545,122,226,30,443,430,1]
```

**Each has teeth (control at `m-1`, reproduced here):** the *same* `Gamma` at `m-1` is NOT full
(`ell=11 top-5 = 20 < 22`; `ell=17 top-8 = 32 < 34`; `ell=23 top-11 = 44 < 46` at both primes),
so `m = (ell+1)/2` is the exact crossing, not an artifact of a laxer `m`. Notes on each:

- **`ell = 11, p = 331` (the note's own extremal `E_3` prime):** the `m = 6` listing is not a
  fluke — it **replicates across 11 distinct `Gamma`** (4 at `p = 199`, 7 at `p = 331`), each
  passing all 16 gates. The mechanism is a single large (size-8) planted fiber alongside one
  size-3 fiber saturating the rank budget `(8-1)+(3-1) = 9 = ell-2`, with the solved `Gamma`
  then *accidentally* carrying enough emergent size-2/3 coincidences to lift `top-6` from a
  naive `15` to exactly `22 = 2ell` — landing precisely on the `L1` boundary.
- **`ell = 17, p = 409` (the note's own full-witness prime):** this is a **different, higher-`E_3`
  config (`E_3 = 16` vs the note's `m=10` witness's `14`) at the identical `p = 409`** — not a
  relabeling of the note's own witness, which does NOT list at `m = 9` (`top-9 = 32 < 34`). The
  more extremal `E_3` is exactly what crosses the `m = 9` threshold.
- **`ell = 23, p in {599, 691}` (large `n`):** cross-prime replicated at two independent primes,
  both with `E_3 = 22 = ell-1` and `top-12 = 46 = 2ell` exactly. All 16 gates pass including the
  expensive `L5_minimal` (`|M| ~ 230`, ~400s/prime) — confirmed this session offline and
  reproducible via `verify_l1_key_lemma_refuted.py --full-min`; the companion verifier's zero-arg
  default runs the 15 fast gates live and trusts the recorded minimality (§7). The `n = 6`,
  `E_3 = ell` config of §1 (`p = 139`) is *not* the large-`n` behaviour: across ~130k
  constructor seeds over 38 primes with `n in [26, 294]`, the max `E_3` found at large `n` was
  `ell-1 = 22`, never `ell` — so the `ell = 23` listing rides `E_3 = ell-1`, exactly like
  `ell in {11,13,17}`.

**Per-`ell` frontier scope (exactly scoped):**

- **`ell = 7`: UNAFFECTED.** The vacancy for `m <= 4 = (ell+1)/2` is **Theorem R**
  (`l1_prime_ell_onset.md`, pair-cap Lemma R + Cauchy-Schwarz, `t=3, m=4`), **unconditional**.
  The KEY LEMMA is load-bearing only for `m in [5, (ell+1)/2]`, an empty window at `ell = 7`.
  `m*(7) = 5 = (ell+3)/2` stands; no `E_3 > ell-2` occurs at `ell = 7` (the verifier's own
  gate-iv sweep tops out at `E_3 = 3`, §3).
- **`ell = 13`: REFUTED** (§2.1). `m*(13) <= 7`.
- **`ell = 11`: REFUTED** (§2.2). `m*(11) <= 6`. The earlier obstruction — no single config had
  BOTH `top-6 >= 22` AND `n >= t+m = 11` cosets (`p = 67` had `top-6 = 22` but `n = 6`; `p = 199`
  had `n = 18` but `top-6 = 21`) — is now cleared at **`p = 331`** (`n = 30`, `top-6 = 22`),
  which lists at `m = 6` and **replicates across 11 distinct `Gamma`** (`p in {199,331}`).
- **`ell = 17`: REFUTED** (§2.2). `m*(17) <= 9`, at the large-`n` prime **`p = 409`** (`n = 24 >=
  t+m = 17`), the note's own full-witness prime, via a higher-`E_3` (`16`) config than its `m=10`
  witness. The earlier `p = 103` (`n = 6`) was merely too small to assemble the codeword.
- **`ell = 23`: REFUTED at large `n`** (§2.2). `m*(23) <= 12`, **cross-prime replicated** at
  `p = 599` (`n = 26`) and `p = 691` (`n = 30`), each `E_3 = 22 = ell-1`, `top-12 = 46 = 2ell`.
  The `p = 139` (`n = 6`) `E_3 = ell` config of §1 was a spectrum-side violation only, and does
  *not* recur at large `n` (max `E_3 = ell-1` there); the listing rides `E_3 = ell-1`.

**Upper-half witnesses SURVIVE.** Each integrated-note witness (`ell in {7,11,13,17}`) lists at
`m = (ell+3)/2`, i.e. certifies `m* <= (ell+3)/2` — an existence statement. Finding listers at
`m = (ell+1)/2 < (ell+3)/2` (for `ell in {11,13,17,23}`) only sharpens the onset bound to
`m* <= (ell+1)/2`; it does **not** invalidate the `(ell+3)/2` witnesses (more listings below an
existing one lower the onset, never remove the existing one). Re-running the integrated verifier
zero-arg confirms all four of its witnesses (`ell=11 p=199/p=331 m=7`, `ell=13 p=313 m=8`,
`ell=17 p=409 m=10`) still pass `run_witness_chain` with `full=True` (§7). What is withdrawn is
only the **complementary VACANCY** (the lower bound `m* >= (ell+3)/2`), now at every tested
`ell >= 11`.

> **STATUS: COUNTEREXAMPLE.** `m*(ell) <= (ell+1)/2` at `ell in {11,13,17,23}`; the VACANCY
> THEOREM (`top-m < 2ell` for `m <= (ell+1)/2`) is FALSE at every tested `ell >= 11`. Withdrawn:
> the LOWER half of `m*(ell) = (ell+3)/2` at `ell in {11,13,17,23}` (all refuted, not merely
> OPEN). UNAFFECTED: `ell = 7` (Theorem R keeps `m*(7) = 5`).

---

## 3. AUDIT — root cause (why every prior search missed this)

The KEY LEMMA was labelled **NUMERIC** ("solve-based beam + random, 0 violations"). That
class of search **systematically undershoots max `E_3`**, because it only ever planted a few
`K in {2,3}` *size-3* fibers and never the *big* fibers that carry the excess.

**Independently observed (this session):** the integrated verifier's own gate-iv sweep, re-run
here, reports `maxE_3 = {7: 3, 11: 5}` — at `ell = 11` its bounded random size-3/`K<=3` sweep
reaches only `E_3 = 5`, far below both the true `ell-1 = 10` (the counterexample) and even the
note's hard-coded `ell-2 = 9` saturation anchor. **Factual statement, no blame:** gate iv
passes with "0 violations" only because its sweep never plants big fibers — it does not sample
the region where the violation lives, so its PASS is a true statement about a set that excludes
the counterexamples. (The saturation to `ell-2` in the integrated note came from two *hard-coded*
witness checks, `p=331 E_3=9` and `p=313 E_3=11`, not from the sweep.)

**The search that finds the violations:** a *big-fiber-plant-then-exact-solve* constructor —
plant one large fiber per coset (sizes descending from `~(ell+1)/2`, kept pairwise-legal), stack
fibers while the exact coincidence-rank stays `<= ell-2`, then read the solved nullspace `Gamma`.
It reaches `E_3 = ell-1` (`ell in {11,13,17}`) and `E_3 = ell` (`ell = 23`). Corroborating the
undershoot diagnosis, the greedy beam lands 1–3 below the true max: `E_3 = 9` at `p = 331`
(matches true max, by luck), but only `10` at `p = 313` (true `12`) and `20` at `p = 139`
(true `23`). So "beam never exceeded `ell-2`" was a **search-depth artifact**, not a bound.

This session's companion constructor, `experimental/scripts/l1_bigfiber_e3_search.py`, is a
clean from-scratch reimplementation of exactly this method (independent of whatever produced
the original six witnesses): by default it re-derives its own, freshly discovered violations
at `ell=11,p=67` and `ell=13,p=79` (different explicit `Gamma` than the ones tabulated in §1,
since the plant order is seeded-random, but the same `E_3 = ell-1` phenomenon), confirming the
method is reproducible and not an artifact of one lucky run. It is demonstrably a *harder*
search at the higher-`K` primes (`p=199`, `p=103`, `p=139`, `p=313` — the last needs a
simultaneous `K=10` coincidence) — consistent with the note's own "solve, don't sample"
methodology remark: these configurations are rare enough that naive sampling of `Gamma`-space
found 0 crossings in 201600 trials.

> **STATUS: AUDIT.** The KEY LEMMA's "0 violations" was an artifact of small-fiber search
> depth; the big-fiber-plant-then-solve constructor exhibits the violations. The integrated
> verifier's gate iv remains internally consistent (it never claims to have searched big
> fibers); it is simply not a witness against the counterexamples.

---

## 4. What SURVIVES (exact)

Everything below holds **on the counterexamples** and is unchanged by this note:

1. **Reduction-chain identities.** `E_3 = rank + delta - K`, `delta = P - ell - K + dim U`,
   `dim U = ell - rank`, `dim B(fs) = dim U`, `dim U = #(Deg(A) cap [0, ell-1])` — all verified
   True on `p = 331, 199, 313, 103, 409, 139`. The chain
   `delta <= K  <=>  E_3 <= ell-2  <=>  dim(V-sum) >= E_3  <=>  sigma <= K`
   is internally **correct**; only its endpoint `delta <= K` is false. Hence the "single OPEN
   core" is not open — it is FALSE.
2. **Pairwise cap** `mu_i + mu_j <= ell` — holds on all six counterexamples (top-two sums
   `11,11,12,13,17,23 <= ell`, independently re-checked here; several tight).
3. **Collinear branch** `P <= ell` (`E_3 <= ell-4`) — untouched.
4. **`det-M` no-go** (`K = 2`: the `2x2` syzygy minor never vanishes, `delta = 0`,
   `E_3 <= ell-4`) — untouched.
5. **L9** `delta <= dim Z - 1` — holds (`p = 79`: `delta = 6 <= dim Z - 1 = 8`).
6. **Theorem R** (odd prime `ell`, `t = 3`, `m = 4`; the `ell = 7` vacancy band) — PROVED,
   untouched (`l1_prime_ell_onset.md`).
7. **The three PROVED sub-cases** of the reduction — generic (`delta = 0`), single-shared-value
   (degree bound), `P = ell+1` — remain true; what is false is only the general leap to
   `delta <= K` on the `K >= 3` non-collinear *affinely-independent* chart (the sole chart the
   note itself flagged OPEN).
8. **Upper-half witnesses** `ell in {7,11,13,17}` — list at `(ell+3)/2`; certify
   `m* <= (ell+3)/2`; verified `full=True` here. SURVIVE.
9. **Refutation of `ceil(2ell/3)`** (integrated note §0.1) — SURVIVES *a fortiori*: the true
   onset is even lower than `(ell+3)/2`, so `m* < ceil(2ell/3)` holds with room to spare.

---

## 5. Corrected picture: NEW KEY LEMMA CANDIDATE `E_3 <= ell` (CONJECTURAL_WITH_FALSIFIER)

With full listings now in hand at `m = (ell+1)/2` for **every tested `ell >= 11`** (§2.2), the
onset is *attained* (not conjectural) at `ell in {11,13,17,23}`: the `(ell+1)/2` upper bound on
`m*` is a certificate. What remains conjectural is only the matching *vacancy* below it — and
that follows cleanly from a single, falsifiable `E_3` ceiling that replaces the refuted `ell-2`.

**Observed-max `E_3` and the attained onset (each listing sits exactly on the bound):**

| `ell` | max `E_3` found                                  | `= `      | `m = (ell+1)/2` listing        | `top-m = 2m + E_3` |
|------:|:-------------------------------------------------|:---------:|:-------------------------------|:-------------------|
| 11 | `10`                                                | `ell - 1` | **ACHIEVED** `p=331` (§2.2)       | `22 = 12 + 10` |
| 13 | `12`                                                | `ell - 1` | **ACHIEVED** `p=313` (§2.1)       | `26 = 14 + 12` |
| 17 | `16`                                                | `ell - 1` | **ACHIEVED** `p=409` (§2.2)       | `34 = 18 + 16` |
| 23 | `22` at large `n` (`= ell = 23` only at `n=6`, `p=139`) | `ell - 1` | **ACHIEVED** `p=599,691` (§2.2) | `46 = 24 + 22` |

The rightmost column is the numerically re-verified identity `top-m = 2m + E_3` **on each of the
five listings** (`ell=13` plus the four of §2.2) — all sit exactly on the bound, hence exactly
on `2ell`. This is the mechanism: `E_3 = ell-1` makes `2m + E_3` first reach `2ell` precisely at
`m = (ell+1)/2`, so that is where the first listing appears.

**The conditional law.** The integrated note proves (§2 toolkit — SURVIVES) the upper bound

> `top-m <= 2m + E_3`   for all `m`.

Suppose `E_3 <= ell`. Then for every `m <= (ell-1)/2`,
`top-m <= 2m + E_3 <= (ell-1) + ell = 2ell - 1 < 2ell`, so the `L1` listing gate `top-m >= 2ell`
fails and there is **no listing at any `m <= (ell-1)/2`**. Hence `m*(ell) >= (ell+1)/2`; combined
with the attained `m = (ell+1)/2` listings (`m*(ell) <= (ell+1)/2`),

> **IF `E_3 <= ell` THEN `m*(ell) = (ell+1)/2` exactly, for every `ell >= 11`.**

(`ell = 7` is the lone exception: there `(ell+1)/2 = 4` is *itself* a proved vacancy by Theorem R,
which pushes the onset to `m*(7) = 5 = (ell+3)/2` — the integrated onset note, unaffected.)

**`E_3 <= ell` is the TIGHT ceiling.** It cannot be strengthened to `E_3 <= ell-1`: the `ell=23,
p=139` config of §1 has `E_3 = 23 = ell` **exactly** (a tight witness). Yet `E_3 = ell` does not
break the law — even at `E_3 = ell`, `2m + E_3 <= 2ell - 1 < 2ell` for `m <= (ell-1)/2`. Only
`E_3 >= ell + 1` would let `top-m` reach `2ell` at `m = (ell-1)/2` or below and drop the onset.

> **NEW KEY LEMMA CANDIDATE** (replacing the refuted `E_3 <= ell-2`): **`E_3 <= ell`.** Under it,
> `m*(ell) = (ell+1)/2` for all `ell >= 11`. Observed to hold, tightly, at every tested
> `ell in {11,13,17,23}` (equality `E_3 = ell` reached at `ell = 23`).
>
> **STATUS: CONJECTURAL_WITH_FALSIFIER.** FALSIFIER: any realizable config with `E_3 >= ell+1`
> (it would admit a listing at some `m <= (ell-1)/2`, dropping `m*` below `(ell+1)/2`). The
> big-fiber-plant-then-exact-solve constructor (`l1_bigfiber_e3_search.py`) is the search tool
> for the falsifier; across ~130k seeds at `ell = 23`, large `n`, the max was `E_3 = ell-1`, with
> the single `E_3 = ell` config (`n = 6`) sitting *on* the inclusive boundary, never over it.

---

## 6. Relevance to `agents.md` steering

This refutation **raises the floor** of the mixed-petal / growing-defect residual
`prob:v13-l1-residuals` (`cap25_v13_experimental.tex`). The withdrawn VACANCY would have
**zeroed** any primitive listing at strata `m <= (ell+1)/2`; with it refuted, the **L1 paid
cell in any adjacent upper ledger must now budget listings at the `m = (ell+1)/2` strata** that
the vacancy would have set to zero (concretely: at `ell = 13`, the `m = 7` primitive-mixed
minimal kernel codeword of §2 is a real occupant that the old accounting omitted). The
listings land in the `L_prim` stratum of `pma_wide_residual` and feed
`petal_mixed_amplification` on the low side.

In the residual-branch taxonomy of the v13 final-resolution spine (`agents.md`: `PAID_BY_THEOREM`
/ `PAID_BY_EXACT_CERTIFICATE` / `CONDITIONAL_ON_NAMED_INPUT` / `CONJECTURAL_WITH_FALSIFIER` /
**`COUNTEREXAMPLE_NEW_FLOOR`**), this event is exactly the **`COUNTEREXAMPLE_NEW_FLOOR`** case:
a claimed-vacant cell is shown occupied by an explicit certificate, so the branch converts from
a would-be zeroed cell to a named obstruction floor. The integrated note's ledger entry
(`m*(11): 8->7`, `m*(13): 10->8`, under `prob:v13-l1-residuals`) must be re-read as **`m*(ell) <=
(ell+1)/2` certified at every tested `ell >= 11`** (`m*(11) <= 6`, `m*(13) <= 7`, `m*(17) <= 9`,
`m*(23) <= 12`), and the low-side budget of `petal_mixed_amplification` must include the
`m = (ell+1)/2` primitive listings at each `ell`, rather than excluding them by vacancy.

> **STATUS: COUNTEREXAMPLE_NEW_FLOOR** (per `agents.md` residual-branch enum) for the L1
> vacancy cell at every tested `ell >= 11` (`ell in {11,13,17,23}`); the amplification low-side
> budget is correspondingly raised.

---

### Concurrent tracks (relationship labels; no dependency taken)

- **Upstream PR #310** (latifkasuli, KB-MCA adjacent-window packet) and **our PR #329**
  (`experimental/notes/frontier-adjacent/frontier_adjacent_v13_rows_v1.md`,
  `experimental/data/certificates/frontier-adjacent/*.packet.json`):
  **affected-downstream** — any `U(a0+1)` L1 cell must not assume sub-`(ell+3)/2`
  vacancy (Sec 2 of this note); both packets already carry the L1 cell as
  OPEN/CONDITIONAL, so no correction is needed, only the fatter-floor awareness.
- **PR #283 (now integrated at upstream 5dbb7e5)** (AllenGrahamHart, `experimental/notes/l1/l1_petal_residue_kernel_reduction.md`
  + four sibling `l1_petal_*` soundness notes): **unaffected-and-awaits** — its lemmas are
  conditional-on-ledger; this note changes the ledger side they await (any
  `petal_squarefree_classification_ledger_payload` must now count the `m=(ell+1)/2` listings).
- **PR #282 (now integrated at upstream 5dbb7e5)** (`experimental/notes/m1/xr_*.md`): **unaffected**
  (M1-aperiodic lane, no shared object).
- **Integrated** `experimental/notes/l1/l1_coset_chart_residue_bridge_v1.md`: **consistent** —
  the Sec 1 counterexamples are new extremal inhabitants of its residue-line branch; its
  classification is untouched.

### Post-filing evidence addendum (2026-07-05, session hunts; AUDIT)

- **`ell = 19` listing question**: a second dedicated hunt (two-fiber-seed
  recipe per the mechanism note, ~944,000 candidate `Gamma` across the 9
  eligible primes with `n >= 19`) found **no** `m = 10` listing and no
  `E_3 >= 18` at any `n >= 19` prime — the question REMAINS OPEN; this is
  a bounded-search null result, not a vacancy proof.
- **New-law falsifier hunt**: a dedicated `E_3 >= ell+1` sweep
  (`ell in {11,13,17,19,23,29}`, ~10,600 exact-solved configs, incl. a
  deep-dive at the `E_3 = ell` record `(23,139)`) found **no**
  counterexample — the Sec 5 candidate law `E_3 <= ell` survives its first
  targeted falsifier pass (evidence, not proof).
- Companion structural note: PR #335 (`experimental/notes/l1/l1_sigma_calculus.md`)
  proves the sigma-calculus lemmas behind Sec 4's identities and pins the
  law's exact sigma-form (`sigma <= K + dimU`).

Refs: `experimental/notes/l1/l1_prime_ell_frontier_corrected.md` (superseded vacancy half;
its verifier and `run_witness_chain` reused unmodified) |
`experimental/scripts/verify_l1_prime_ell_frontier_corrected.py` |
`experimental/cap25_v13_experimental.tex` `prob:v13-l1-residuals` |
`experimental/data/prize-dag/prize_dag.json` nodes `pma_wide_residual`, `petal_mixed_amplification`

## 7. Reproducibility and per-claim status ledger

**Integrated verifier unchanged and still green (survivors + machinery intact; independently
re-run twice this session, once per gate-set):**

```
python3 experimental/scripts/verify_l1_prime_ell_frontier_corrected.py
    -> RESULT: ALL GATES PASS  (~80s)      # incl. gate-iv sweep maxE_3={7:3, 11:5}
python3 experimental/scripts/verify_l1_prime_ell_frontier_corrected.py --tamper-selftest
    -> SELF-TEST RESULT: all tampers CAUGHT (~67s)   # every gate, incl. run_witness_chain, has teeth
```

**Self-contained reproducer for §1–§2** (stdlib only; imports the shipped verifier's
`run_witness_chain` but does not edit it — the same checks are codified as gates i/ii/iii/iv/v/vi
of this note's own companion verifier, `experimental/scripts/verify_l1_key_lemma_refuted.py`,
which is the authoritative, `pytest`-free, zero-arg reproduction path):

```python
import importlib.util
VER = "experimental/scripts/verify_l1_prime_ell_frontier_corrected.py"
s = importlib.util.spec_from_file_location("v", VER); v = importlib.util.module_from_spec(s); s.loader.exec_module(v)

def spectrum(gamma, p, ell):                      # from scratch, group F_p^* by x^ell
    grp = {}
    for x in range(1, p):
        lab = pow(x, ell, p); vv = 0; xr = 1
        for r in range(1, ell):
            xr = xr*x % p; vv = (vv + gamma[r-1]*xr) % p
        grp.setdefault(lab, {}); grp[lab][vv] = grp[lab].get(vv, 0) + 1
    return sorted((max(d.values()) for d in grp.values()), reverse=True)
E3 = lambda sp: sum(mu-2 for mu in sp if mu >= 3)

CE = {(11,67):[43,44,38,44,17,18,42,44,65,1], (11,199):[21,144,71,171,42,10,12,115,173,1],
      (13,79):[23,71,3,40,40,2,46,40,67,69,71,1], (13,313):[185,42,295,307,71,257,218,32,90,290,279,1],
      (17,103):[27,7,1,74,35,11,86,96,66,44,7,96,5,48,72,1],
      (23,139):[60,80,118,60,48,137,123,101,89,94,15,23,21,88,134,5,48,8,124,42,77,1]}
for (ell,p), g in CE.items():
    sp = spectrum(g, p, ell)
    print(ell, p, "E3=", E3(sp), "> ell-2=", ell-2, "  E3>ell-1:", E3(sp) > ell-1)

# frontier: p=313 lists at m=7 (all 16 gates True); NOT full at m=6
for m in (6, 7):
    G, lf, full, tm = v.run_witness_chain(CE[(13,313)], 313, 13, m)
    print("ell=13 p=313 m=%d: top_m=%d full=%s (16 gates: %s)" % (m, tm, full, all(G.values())))

# the four NEW sub-onset listings at m=(ell+1)/2 (top-m = 2m+E3 = 2ell exactly)
NEW = {(11,331,6):[11,165,196,237,31,40,171,236,246,1],
       (17,409,9):[80,5,360,87,283,89,358,379,216,174,67,329,68,317,398,1],
       (23,599,12):[327,192,175,17,298,200,474,496,95,354,502,222,509,213,417,173,98,207,106,381,328,1],
       (23,691,12):[524,614,310,539,294,303,425,653,551,564,145,271,332,503,117,545,122,226,30,443,430,1]}
for (ell,p,m), g in NEW.items():
    sp = spectrum(g,p,ell); e3 = E3(sp)
    # ell=23 minimality is ~400s; use check_minimal=False for a fast 15-gate demo
    G, lf, full, tm = v.run_witness_chain(g, p, ell, m, check_minimal=(ell<23))
    print("ell=%d p=%d m=%d: top_m=%d=2m+E3(%d)=2ell(%d) full/15ok=%s" %
          (ell, p, m, tm, 2*m+e3, 2*ell, all(G.values())))
```

Expected output: `E_3` = `10,10,12,12,16,23` (all `> ell-2`; `23 > ell-1` at `ell=23`);
`m=6 -> full=False (top_m=24)`, `m=7 -> full=True, all 16 gates True (top_m=26)`; and each NEW
listing has `top_m = 2m+E_3 = 2ell` with all gates True (16 live for `ell in {11,17}`; 15 live
for `ell=23`, its `L5_minimal` confirmed by `verify_l1_key_lemma_refuted.py --full-min`). This
session ran exactly this reproducer (from scratch, before writing any shipped file) and
additionally confirmed: the note's own `p=313` witness is `full=False` at `m=7` (`top_m=25`) and
`full=True` at `m=8` (`top_m=27`); the concentrated `Gamma` is `full=False` at `m=7` (`top_m=18`);
and the `ell=11` `m=6` listing replicates across all 11 constructor `Gamma` (`p in {199,331}`).

**Independent constructor reproduction** (does not replay the table above; re-derives fresh
counterexamples from scratch by search):

```
python3 experimental/scripts/l1_bigfiber_e3_search.py
    -> RESULT: ALL REQUIRED DEFAULT TARGETS CONSTRUCTED  (a few seconds)
       (ell=11,p=67) and (ell=13,p=79), both with E_3 = ell-1, freshly found by
       plant-big-fibers-then-exact-solve, seed-deterministic, not looked up.
```

**Authoritative zero-arg gate suite for this note** (six gate classes; gate vi is the four
sub-onset `m = (ell+1)/2` listings of §2.2, verified from-scratch + via the integrated
`run_witness_chain`):

```
python3 experimental/scripts/verify_l1_key_lemma_refuted.py
    -> RESULT: ALL GATES PASS   (~58s; gate vi runs ell=11/17 full-16 live + ell=23 fast-15 live)
python3 experimental/scripts/verify_l1_key_lemma_refuted.py --tamper-selftest
    -> SELF-TEST RESULT: all tampers CAUGHT   (~0.5s; gate vi flips one datum per new witness)
python3 experimental/scripts/verify_l1_key_lemma_refuted.py --full-min
    -> (optional) also runs ell=23 check_minimal=True LIVE (~15 min): all 16 gates True there too
```

**Per-claim status block:**

| # | Claim | Status | Reproduce |
|--:|:------|:-------|:----------|
| 1 | `E_3 <= ell-2` refuted at `ell in {11,13,17,23}`; `E_3 <= ell-1` refuted at `ell=23` | **COUNTEREXAMPLE** | verifier gates i, ii, v; constructor script |
| 2 | Vacancy half refuted at `ell in {11,13,17,23}`: `m*(ell) <= (ell+1)/2` (16-gate `m=(ell+1)/2` listing each) | **COUNTEREXAMPLE** | verifier gate iii (`ell=13`) + gate vi (`ell=11,17,23`, `run_witness_chain` + `m-1` control) |
| 3 | Root cause = small-fiber search undershoot; gate-iv `maxE_3={7:3,11:5}` | **AUDIT** | integrated verifier zero-arg gate-iv line; `l1_bigfiber_e3_search.py` |
| 4 | NEW KEY LEMMA CANDIDATE `E_3 <= ell` (tight at `ell=23`) `=> m*(ell)=(ell+1)/2` for `ell>=11` (attained) | **CONJECTURAL_WITH_FALSIFIER** | §5 derivation (`top-m<=2m+E_3` proved); falsifier `E_3>=ell+1` via constructor |
| 5 | Ledger: `COUNTEREXAMPLE_NEW_FLOOR` for the L1 vacancy cell at `ell in {11,13,17,23}` | **COUNTEREXAMPLE_NEW_FLOOR** | §6 |
| — | Survivors (identities, pairwise cap, no-gos, Theorem R, upper witnesses, `ceil(2ell/3)`) | **SURVIVES** | verifier gate iv (survivor check) + §4 |

Constants are exact throughout; every prime satisfies `ell | p-1`; all fibers are proper
(no full-coset, all points distinct); no floating point anywhere.
