# (C2) GCD-test harness: schema and usage

- **Purpose:** the certification harness that consumes the `W_h` pilot's
  (C1) outputs and discharges the **(C2)** input of the (A) closure
  assembly — the per-row GCD tests `gcd(p, D(n,h)) = 1` of
  `a_closure_assembly.md` section 3.
- **Script:** `experimental/scripts/verify_c2_gcd_harness.py` (pure stdlib).
  It is BOTH the harness and its own verifier.
- **Companions:** `a3_good_reduction_lemma.md` (Theorem A3; the exceptional
  integer `D(n,h)` and its certificate data, sec 3.2), `a_closure_assembly.md`
  ((C1)/(C2) inputs, failure ladder), `h_window_derivation_audit.md` (which
  `h` the row window must cover — recommend `H_max = A`).
- **Status:** harness + self-test **green** (14/14 PASS). The self-test
  reconstructs the A3 toy exceptional set `{7, 17, 97}` at `(n,h) = (16,3)`
  **exactly**, two independent ways.

## Critical-path role

C2 is the row-prime certification side of the A3 bridge.  A3 says that a
clean `gcd(p,D(n,h))` gives characteristic-zero lifting at a fixed cell;
C2 is the machine-checkable harness that consumes the pilot's `D(n,h)`
integers and certifies those GCDs for the official row primes.  Failures are
not proof failures: they route to the A3 closure assembly's recount/charge
ladder.

## 1. What (C2) is

Theorem A3 (proved, `a3_good_reduction_lemma.md`): fix `n = 2^s`, `h >= 2`
and a certificate for `(n,h)` with exceptional integer `D(n,h)` (an odd
positive integer). For a row prime `p` with `q in {p, p^2}` and `n | q-1`,

```text
gcd(p, D(n,h)) = 1   ==>   reduction mod p is a bijection
                            {char-0 anchored (n,h)-candidates}
                            -> {row anchored (n,h)-candidates},
```

which with X24 forces **zero** primitive row trades at that `(n,h)`. So the
whole (C2) obligation per row is: `gcd(p, D(n,h)) = 1` for every window `h`.
A GCD failure is not automatically a trade — `support(D_pt) subset
support(D)` may carry spurious primes — it is a **flag** to be recounted
(the response ladder of `a_closure_assembly.md` section 5).

The harness computes exactly these GCDs and emits a per-row PASS/FAIL
certificate:

```text
PASS(row) = gcd(D(n,h), p) = 1 for all window h  (no window-h exceptional
                                                   divisibility);
FAIL(row) = the list of triples (h, prime, divisor) with gcd > 1.
```

## 2. `q = p` vs `q = p^2` handling (A3 split behaviour)

The divisibility test is the **same integer test** `gcd(D(n,h), p)` in both
cases — `D(n,h)` depends on `(n,h)` only, and the exceptional condition is a
statement about the residue **characteristic** `p` (A3 Lemma 1: the extra
candidate lands in a prime `P` over `p`). What differs is **row existence**:

```text
q_form = "p"   (q = p)   : row exists  iff  n | p - 1     (A3 case f = 1);
q_form = "p2"  (q = p^2) : row exists  iff  n | p^2 - 1   (A3 case f in {1,2}).
```

The harness validates `n | q - 1` per `q_form`, marks invalid rows `SKIP`,
and only GCD-tests valid rows. (A prime whose extra candidate lives in
`F_{p^f}` with `f = ord_n(p) > 2` divides `D` but admits no `q in {p, p^2}`
row, so is correctly excluded — see the `(16,3)` example, section 5.)

## 3. Schemas

### 3.1 D(n,h) certificate — `c2-gcd-certificate/v1` (the (C1) product)

```json
{
  "schema": "c2-gcd-certificate/v1",
  "n": 1024,
  "definition": "D_rur",                     // or "D_pt(ideal-norm)"
  "provenance": "W_h pilot run <id>",
  "entries": [
    {
      "h": 4,
      "D": "<decimal string of the ODD integer D(n,h)>",
      "D_is_odd": true,
      "rur_factors": {                        // OPTIONAL; if present the
        "delta_0": "..",                      //   harness cross-checks
        "delta_i": ["..", ".."],              //   D == oddpart(product)
        "e_j":     ["..", ".."],
        "e_u":     "..",
        "Delta_m": "..",
        "lc_m":    ".."
      }
    }
  ]
}
```

`D(n,h)` is exactly the object of `a3_good_reduction_lemma.md` section 3.2:

```text
D(n,h) = odd part of  delta_0 . prod_i delta_i . prod_j e_j . e_u
                      . Delta_m . lc(m).
```

Supplying `rur_factors` lets the harness re-multiply and confirm the stored
`D` matches — a cheap integrity check on the pilot's arithmetic. The pilot
should emit one `entries[]` element per window `h` (the audit recommends
`h in [t+1, A]`; see `h_window_derivation_audit.md`).

### 3.2 row-prime spec — `c2-row-spec/v1`

```json
{
  "schema": "c2-row-spec/v1",
  "n": 1024,
  "H_max_mode": "agreement_A",   // "grammar_sq" | "two_log2" | "explicit"
  "H_max": 100,                  // only read when H_max_mode == "explicit"
  "rows": [
    { "label": "RowC 1/4",  "p": <prime>, "q_form": "p",  "t": 5, "A": 261 },
    { "label": "RowC 1/16 ext", "p": <prime>, "q_form": "p2", "t": 3, "A": 67 }
  ]
}
```

- `t` and `A` set the row window `[t+1, H_max]`; the harness tests exactly
  the certificate `h`'s inside it. Per the window audit the safe default is
  `H_max_mode = "agreement_A"` (`H_max = A`); `"grammar_sq"` (`(log2 n)^2`)
  and `"two_log2"` (`2 log2 n`) are comparison columns.
- If a row omits `t`, the harness tests **every** `h` in the certificate
  (used by the bare-`(n,h)` `(16,3)` self-test).
- **The official Row-C primes are a class, not fixed integers** in the
  banked data (`n = 1024`, `q in {p,p^2}`, `n | q-1`, `char p >= n^2`; the
  x10/qa22 certificates pin `n` and the budgets but not specific `p`). The
  spec is therefore a parameter: the operator lists the primes actually
  chosen for the submission rows. Any `p` with `p >= n^2` and `n | q-1` is
  admissible; the harness enforces `n | q-1` and is otherwise `p`-agnostic
  (the GCD test needs only the integer `p`).

### 3.3 result — `c2-gcd-result/v1` (emitted)

```json
{
  "schema": "c2-gcd-result/v1",
  "n": 1024,
  "H_max_mode": "agreement_A",
  "rows": [
    { "label": "..", "p": <prime>, "q_form": "p", "q": <prime>,
      "row_valid": true, "window": [6, 261], "h_tested": [6,7,...],
      "verdict": "PASS", "exceptional": [] },
    { "label": "..", "p": <prime>, "q_form": "p2", "q": <p^2>,
      "row_valid": true, "window": [4, 67], "h_tested": [4,...],
      "verdict": "FAIL",
      "exceptional": [ { "h": 5, "prime": <p>, "divisor": <g> } ] }
  ],
  "summary": { "rows_valid_pass": N, "rows_valid_fail": M,
               "exceptional_primes": [ ... ] }
}
```

A `FAIL` row is **data, not an error**: harness mode always exits 0. Each
`(h, prime, divisor)` triple routes to the recount ladder of
`a_closure_assembly.md` section 5 (recount at the bad pair; charge genuine
extras to the `n^3` column; or accept as a real charged trade).

## 4. Usage

Harness (consume pilot (C1) + row spec, emit per-row certificate):

```bash
python3 experimental/scripts/verify_c2_gcd_harness.py \
    --cert    D_1024.json \
    --rowspec rowc_rows.json \
    --out     c2_result.json
```

Verifier / self-test (no args) — runs the `(16,3)` recovery, the Task-1
window-audit arithmetic, and the pinned self-test certificate check,
PASS/FAIL per section, exit 0 iff all pass:

```bash
python3 experimental/scripts/verify_c2_gcd_harness.py
```

## 5. Self-test: the `(16,3)` toy exceptional set `{7, 17, 97}`

The self-test computes the toy `D(16,3)` **directly** (light, `~4 s`):

```text
D_pt(16,3) = odd part of  prod_R  N(a(R)),
   R ranging over the C(15,5) = 3003 anchored 6-subsets of mu_16 (1 in R),
   a(R) = ideal ( O_1^cl(R), O_2^cl(R) ) in Z[zeta_16],
   O_j^cl = 2^{4h-2} O_j        (x83 cleared obstructions, h = 3),
   N(a(R)) = [ Z[zeta_16] : a(R) ]   (exact integer lattice index / HNF).
```

`p | N(a(R))` iff both cleared obstructions of `R` land in a common prime
of `Z[zeta_16]` over `p` — i.e. iff `R` is an extra anchored mod-`p`
candidate — so `supp(D_pt)` is exactly the exceptional-prime set. All 3003
supports are non-candidates (X24: no char-0 `(16,3)` trades, `3` not a
2-power), verified in-line.

The harness then GCD-tests `D_pt(16,3)` against the A3 row lists — `q = p`
for `p ≡ 1 (mod 16)`, `p <= 700`, and `q = p^2` for `p in {7, 23}` — and
recovers the FAIL set **`{7, 17, 97}`** exactly (7 via the `q = 49`
extension row). Confirmed independently and rigorously by:

- **S3** the harness `gcd(D, p)` route;
- **S4** a from-scratch **pointwise** `a(R) subset P` evaluation (ported
  from `verify_a3_good_reduction.py`, uses no `D`, no gcd) — same set;
- **S5** the split-behaviour gate: `D_pt(16,3)`'s small-prime support is
  `{3, 7, 17, 97}`; `3` has `ord_16(3) = 4`, so its extra candidate lives
  only in `F_{3^4}` and admits **no** `q in {p, p^2}` row — correctly
  excluded, while every valid-row divisor is in `{7, 17, 97}`;
- **S6** every reported exceptional prime is a valid row prime.

The `lattice_index` (integer HNF) is unit-tested and was cross-checked
against sympy's Smith normal form (0 mismatches on 60 supports) during
development; the shipped script needs only stdlib.

## 6. Notes for the pilot handoff

- The pilot emits `c2-gcd-certificate/v1` with one `D(1024, h)` per window
  `h`. For the **empty-window prize rows** no certificate is needed (the
  lane is vacuous; `u2a_window_split.md`). For **Row-C rows** the window is
  `[t+1, A]` under the audit's recommendation (`A = 261/133/67`).
- The RUR route (`definition = "D_rur"`) yields a single modest integer per
  `h` (a product of a handful of resultant/discriminant quantities), unlike
  the proof-minimal `D_pt` (a product over `C(n,2h)` supports, feasible only
  at the toy). The harness treats both uniformly: it needs only the integer
  `D` (and, optionally, `rur_factors` to re-verify it).
- (C2) is **reusable**: `D(1024, h)` is row-independent within the Row-C
  class, so the same certificate serves every Row-C prime and every future
  `q` at `n = 1024`; only the per-row GCD is repeated.
