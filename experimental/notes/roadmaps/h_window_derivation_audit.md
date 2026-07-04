# h-window derivation audit: which trade sizes enter R_PTE

- **DAG node:** `h_window_derivation` (the loose end the (A) closure
  assembly surfaced).
- **Task:** resolve the missing derivation of the `h <= H_max` cap on
  trade sizes used by `a_closure_assembly.md` (its `H_max = 2 log2 n = 20`,
  re-verified at `(log2 n)^2 = 100`, has no in-repo derivation; canonical
  star-PTE trades can a priori have `h` up to the agreement number `A`).
- **Method:** route (iii) first — the cheap accounting audit of which `h`
  actually reach the `R_PTE` compiler column. Then the large-h companion.
- **Verifier:** `experimental/scripts/verify_c2_gcd_harness.py`
  (sections `TASK1 T1a..T1g`; current run 13/13 PASS).
- **Status:** the audit is **complete and honest**; it produces a
  **negative structural finding** plus one **proved lemma** and a concrete
  **recommendation**. It does NOT by itself close the node — it shows the
  node closes cleanly only via resolution (i) (extend (C1)), and prices
  what (ii) would cost.

## 0. TL;DR

1. The assembly's cap `H_max = 2 log2 n = 20` corresponds to **no banked
   object**. It sits **below every Row-C agreement number** `A` (67, 133,
   261), so it bounds nothing a priori (T1c).
2. The only banked cap in the consumer stack is the **frozen W3 v1 grammar
   window** `t < h <= (log2 n)^2 = 100` (`w3_chargeable_dictionary_grammar.md`
   map-degree ceiling; `b_writeup_band_trade_reduction.md` band convention
   `t+1 < h <= floor(log2 n)^2`; `u2a_window_split.md` dangerous window
   `t < b <= floor(log2 n)^2`). This cap is **definitional (a frozen
   grammar choice), not a derived emptiness/charging theorem**, and it is
   `< A` for rates 1/4 and 1/8 (T1b).
3. So the honest answer is **(b)-flavoured**: no banked step caps the
   consumer at `2 log2 n`, and the grammar cap `(log2 n)^2` does not cover
   `h <= A` at two of three Row-C rows. There is a genuine accounting hole
   at `(log2 n)^2 < h <= A` for rates 1/4, 1/8 (and, under the tighter
   `2h <= A` reading, only for rate 1/4, over `100 < h <= 130`).
4. **Large-h companion — proved part:** `<= n` partners per anchored core
   at **every** `h` (value-set argument; sharpens the task's `<= 2n` and
   generalises the h=3 cubic cap; refines to `<= floor(n/h)` full-fiber
   partners). Verified numerically (T1f).
5. **Large-h companion — open part:** the crude route bounds trades by
   `(active cores) x (n/h)`, and `#cores = C(n,h)` is super-polynomial
   (T1g). Hitting the `n^3` budget needs `active cores <= h n^2`, i.e. the
   **terminal `active_core_count_bound`**. So the crude route does **not**
   close large-h; it reduces to the same terminal difficulty.
6. **Recommendation (primary):** adopt resolution **(i)** — extend the
   (C1) certificates to `h <= A` (equivalently `h <= ceil(A/2)`). A3 + X24
   apply verbatim at every `h` (nothing in their proofs caps `h`), `A` is
   modest (`<= 261` at Row C), and the prize rows have **empty** windows
   (T1d), so no extension is needed there. This makes the window question
   moot. Update `a_closure_assembly.md` to set `H_max := A`, not
   `2 log2 n`.

## 1. Parameter frame (verified: T1a, T1d)

`A = k + t` (banked; `qa22_staircase_budget_column.md` line 10), with
`k = rho * n` the code dimension and `t = A - k` the matched-moment
threshold. For `n = 1024`:

```text
rate   k     t   A = k+t   2 log2 n   (log2 n)^2   floor(A/2)
1/4    256   5   261       20         100          130
1/8    128   5   133       20         100          66
1/16   64    3   67        20         100          33
```

Prize rows (`n = 2^41`, `(log2 n)^2 = 1681`):

```text
rate   k       t          A = k+t
1/4    2^39    2^33 + 1   558345748481
1/8    2^38    2^33 + 1   283467841537
1/16   2^37    2^32 + 1   141733920769
```

All six `A = k + t` identities are re-derived in the verifier, and the
prize `t > 1681` (empty small-block window) is confirmed.

## 2. The chain audited (route iii)

The compiler obligation is the terminal primitive residue `R_PTE(row)`
consumed as one direct `n^3` split-pair column (`w4_direct_column_rewiring.md`).
The trades that flow into it arrive along:

```text
same-top-coefficient locator families      (list objects; L_P, L_Q differ
   (agreement pairs at agreement A)          by a constant on the top t)
      | star-PTE lemma (banked)
      v
canonical minimal PTE trades from a base    (h = exchange size; support 2h;
   deg(L_P - L_Q) = 0                          a priori h up to O(A))
      | B exit 3 / U1 primitive residue (b_writeup), then X-10 orbit
      v
R_PTE(row)  <=  n^3  via W4 direct column
```

The question the node poses: **does this column count trades at all
`h <= A`, or does a banked step cap `h`?** Three candidate caps live in the
repo; each is examined.

### 2.1 `2 log2 n = 20` — the assembly's cap: NOT banked (T1c)

`a_closure_assembly.md` section 2 states plainly: "I did not locate an
in-repo derivation of the specific `2 log2 n` cap." This audit confirms it:
no grammar, window, or charging note produces `2 log2 n`. Numerically
`20 < 67 <= A` for every Row-C row, so as an a-priori envelope on trade
size it caps **nothing**. (It is plausibly a loose heuristic "first-moment
safe" cutoff — see 3.3 — but heuristics are not derivations.) **Verdict:
discard `2 log2 n` as the consumer cap.**

### 2.2 `(log2 n)^2 = 100` — the grammar window: banked but insufficient (T1b)

This is the real banked object, appearing three times:

- `w3_chargeable_dictionary_grammar.md`: charged families use maps
  `deg(psi) in (t, (log2 n)^2]`; the note **deliberately does NOT charge**
  "maps of degree `> (log2 n)^2`" — an explicit v1 exclusion / falsification
  target, **not** a theorem that such trades are absent.
- `b_writeup_band_trade_reduction.md`: the band-trade object is defined with
  `t+1 < h <= floor(log2 n)^2`; exit 3 (the primitive moment/PTE residue
  routed to `R_PTE`) inherits this ceiling.
- `u2a_window_split.md`: the dangerous small-block window is
  `t < b <= floor(log2 n)^2` (block size `b` = trade half-size `h`).

Two limitations:

1. **It is definitional, not derived.** The `(log2 n)^2` ceiling is a
   *frozen v1 grammar choice* bounding what the dictionary charges. Nothing
   there proves that primitive trades with `h > (log2 n)^2` do not exist or
   are charged elsewhere; the grammar note lists them among its **explicit
   exclusions** and flags them as where "falsification must attack."
2. **It is below `A`.** `(log2 n)^2 = 100 < A` for rates 1/4 (261) and 1/8
   (133). So even accepting the grammar window as the cap, a-priori trades
   with `100 < h <= A` are outside it. Under the tighter reading
   `2h <= A` (support of a minimal `h`-trade is `2h` points; if it sits
   inside the size-`A` agreement set), the ceiling `floor(A/2)` is `130, 66,
   33`, and only **rate 1/4** retains a residual gap `100 < h <= 130`.

### 2.3 `A = k + t` — the a-priori envelope

The star-PTE support lives in the agreement configuration, so the exchange
size is bounded by the agreement number: `h <= A` (or `2h <= A` if the
whole `2h`-support must sit in the agreement set). This is the only
**rigorous** upper envelope on trade size, and it is what the DAG node
names ("`h` up to `A (~67 at Row C)`").

> **HONEST FLAG.** I could not locate the precise star-PTE support-size
> lemma (`h <= A` vs `2h <= A`) as an in-repo statement; both readings are
> carried above. Pinning it is a genuine micro-step: under `2h <= A` the
> residual hole collapses to rate-1/4, `h in (100,130]` (31 sizes); under
> `h <= A` it is rates 1/4 and 1/8, `h in (100,261]` and `(100,133]`.

### 2.4 Route-(iii) verdict

The `R_PTE` column, **as currently specified** (b_writeup exit 3 + W3 v1
grammar window), counts primitive trades only up to `h <= (log2 n)^2`.
Trades with `h > (log2 n)^2` are:

- not charged by the v1 dictionary (explicitly excluded), and
- not in the primitive-residue window,

so at rates 1/4 and 1/8 they are **unaccounted** — neither charged nor
certified zero. This is the accounting hole. The falsifier ("a consumer
trace with `h > 2 log2 n` entering `R_PTE` at super-absorbable weight") is
**not triggered** (I found no trace forcing large-h trades into `R_PTE`),
but it is **not refuted** either (no banked step excludes them). The safe
resolution is to certify those `h`, not to assume them away.

## 3. The large-h companion

### 3.1 PROVED (all `h`): `<= n` partners per anchored core

**Lemma (value-set partner cap).** Let `H = mu_n subset F_q`, let `P` be an
`h`-subset with locator `L_P(X) = prod_{x in P}(X - x)`. If `Q` is an
`h`-subset of `H`, disjoint from `P`, with `e_i(P) = e_i(Q)` for
`1 <= i <= h-1` (a minimal `h`-trade), then

```text
L_Q = L_P - c   for a nonzero constant c,
```

because agreeing on `e_1..e_{h-1}` forces `L_P - L_Q` to be a constant
(only the degree-0 coefficient can differ). Every `y in Q` is a root of
`L_Q`, so `L_P(y) = c`: thus

```text
c in V_P := { L_P(x) : x in H },     |V_P| <= n,
```

and `Q` is exactly the root set of `L_P - c`, so `Q |-> c` is injective.
Hence

```text
# partners of P  <=  |V_P|  <=  n,     at EVERY h.
```

A full-fiber partner needs `|L_P^{-1}(c) cap H| = h`; since
`sum_c |L_P^{-1}(c) cap H| = n`, at most `n/h` values are hit `>= h` times,
so in fact **`# partners <= floor(n/h)`**. QED

This **sharpens** the task's suggested `<= 2n` (the degree-`<= 2n`
polynomial `N_x^n - D^n` of the h=3 cubic cap) to `<= n`, and generalises
the cubic cap to all `h`. Verified in the harness (T1f) over `F_17 ⊃ mu_8`
at `h = 3, 4`: partners per core `<= n = 8` and `Q |-> c` injective.

### 3.2 OPEN (= terminal): active-core count

The trade count is

```text
# minimal h-trades  <=  (# active cores) x floor(n/h),
```

where a core is **active** if it admits `>= 1` partner. The trouble is
`# cores = C(n, h)` (anchored: `C(n-1, h-1)`), which is **super-polynomial**
— `C(1024, 100)` has 141 digits (T1g). To land in the `n^3` split-pair
budget one needs

```text
# active cores  <=  h n^2,
```

i.e. a reduction of `C(n,h)` active cores down to `poly(n)`. **That is
exactly the terminal open node `active_core_count_bound`.** So the crude
"partners x cores" route does not close large-h cheaply; it reduces large-h
emptiness to the same wall the whole campaign is stuck at. The task's
sketched escape (bound active cores by the `h-1` obstruction conditions)
is precisely this terminal reduction, not a shortcut around it.

The x83 dichotomy and A3 do apply at **every** `h` (nothing in their proofs
caps `h`; `x83` denominator control is `2^{4h-2}` for all `h`, X24 forbids
char-0 dyadic trades at all non-2-power `h`), which is what makes
resolution (i) — extend the certificates — the same machinery, and makes
resolution (ii) — a standalone large-h emptiness — as hard as the terminal
problem.

### 3.3 First moment (HEURISTIC, not a proof — T1e)

For `q >= n^2` the naive first moment of primitive `h`-trades is
`~ n^2 / (h!)^2`, which crosses 1 near `h = 7` for `n = 1024`
(`n^2/(h!)^2 = 72.8, 0.041, ...` at `h = 5, 7`). This is why a small cap
"feels" safe — but it is a **heuristic**: the transition is exceptional-prime
driven and **non-monotone** (`campaign_report_01_terminal.md`: nonzero
counts at `q ~ n^{9/4}` between zeros), so the first moment is not a
rigorous emptiness bound. It explains, but does not license, `2 log2 n`.

## 4. Recommendation and node disposition

**Primary (resolution i): extend (C1) to `h <= A` (or `h <= ceil(A/2)`).**
Certify `D(1024, h)` for `h` up to the a-priori envelope at each Row-C
rate (`A = 67, 133, 261`, or `floor(A/2) = 33, 66, 130`). Then the (A)
closure theorem holds for **all** a-priori trade sizes and the window
question is **moot** — there is no `h` left uncovered. Justification:

- A3 + X24 apply verbatim at every `h`; the certificate is the same
  eliminant chain (`a3_good_reduction_lemma.md` sec 3.2), just more `h`.
- `A <= 261` is modest; the parallel `W_h` pilot's feasibility curve prices
  the extra `h` directly (its `D(n,h)` cost curve). The (C2) side is free:
  `verify_c2_gcd_harness.py` already gcd-tests any set of `h` present in the
  certificate against the row primes.
- Prize rows need **no** extension: their windows are empty (`t >> 1681`),
  so the small-window lane is vacuous and large blocks are U2-C's job.

**Concrete edit to bank:** in `a_closure_assembly.md` replace
`H_max = 2 log2 n` by `H_max = A` (Row-C: 261/133/67), citing this audit;
keep the `(log2 n)^2` verification as a *lower* comparison column, and note
explicitly that the W3 v1 grammar cap `(log2 n)^2` does **not** cover
`h <= A` at rates 1/4, 1/8, so the grammar window alone is insufficient.

**Secondary (resolution ii):** a rigorous large-h emptiness lemma is
**not** available cheaply — it is the terminal `active_core_count_bound`.
Do not spend the endgame on it; the proved `<= n` partner cap (3.1) is the
harvestable piece and is now banked here + in the verifier.

**Node status:** `h_window_derivation` should move from `TARGET` to
`RESOLVED-BY-(i)` once the assembly's `H_max` is repointed to `A` and the
pilot's feasibility curve confirms `h <= A` is in budget. The audit output
of this note is the required derivation of the true consumer envelope
(`= A`) plus the honest finding that the two smaller caps (`2 log2 n`,
`(log2 n)^2`) are, respectively, unbanked and insufficient.

## 5. Verification

```bash
python3 experimental/scripts/verify_c2_gcd_harness.py
```

Task-1 sections `T1a..T1g` (parameter identities, cap comparisons, empty
prize windows, the partner-cap lemma, the terminal reduction) plus the
`(16,3)` self-test; current run **13/13 PASS**.
