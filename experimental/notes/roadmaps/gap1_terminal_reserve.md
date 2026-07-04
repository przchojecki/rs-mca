# GAP-1 terminal reserve at the corridor: stage-1 arithmetic + the stage-2 conjecture

- **Status:** AUDIT (stage-1 arithmetic, deterministically re-derived by the
  verifier) + **CONJECTURE** (stage 2, stated, NOT proved). Nothing here is
  PROVED beyond the cited inputs.
- **Agent/model:** Claude (Fable 5), L1 lane, branch `allen/prize-dag-delta`.
- **Date:** 2026-07-03.
- **DAG target:** the reserve half of `gap1_product_model` -> `gap1_noneq_mass`
  (the half that PR #212's packet explicitly leaves open).
- **Inputs:** `x1_gap1_tower_product_bound.md` (PR #212; PROVED product
  theorem), `x1_gap1_nonequivariant_periodic_evidence.md` (E6),
  `experimental/notes/x1/x1_quotient_reduction.md` (per-scale reserve caveat),
  `qa3_e14_fm_margin_tables.md` (corridor ZM arithmetic; conventions C1-C4).
- **Verifier:** `experimental/scripts/verify_gap1_terminal_reserve.py`
  (stdlib, deterministic, toy scale; exact-integer sign checks).

## 0. The question

PR #212 proves (Theorems 1-3 there): non-equivariant `K_M`-periodic slope
mass is at most the **product over active characters** of per-character image
sizes, each character confined to one intermediate-field line `alpha^r K`.
It does **not** prove the final `gap1_noneq_mass <= poly(n) * FM` bound.

This note asks the missing question:

```text
Is  product_{r in R} (per-character count)  <=  poly(n) * FM
at the corridor, with the crude per-character count |A_r| <= |K|?
```

Stage 1 answers with exact arithmetic: **no — short by >= 120 bits** even in
the most favorable case. Stage 2 states the sub-estimate that would close the
gap, as a conjecture with pinned quantifiers.

## 1. Pinned notation

All conventions are inherited from `qa3_e14_fm_margin_tables.md` sect. 1:

```text
row      (n, k, q): RS code of dim k evaluated on H_n = <omega> <= F_q^*,
         n | q-1;  B := F_q is the base field of the #212 tower B <= K <= F.
A        agreement; t = A - k; j = n - A.
FM(A)    = C(n,j) * q^(1-t)                        (upper form of Lemma FM1)
target   T(A) := n^3 * FM(A);  ZM(A) := log2 T(A)  (poly budget B = 3, per
         qa3 C3; a larger poly exponent only moves the tables by O(log n))
M        period, M | n, M >= 2; K_M = <zeta>, zeta = omega^(n/M).
R        active character set, R subseteq Z/M, |R| <= M.
K        intermediate field of the tower, alpha^M =: beta in K;
         |K| = q^e, e = [K:B] >= 1.
crude    per-character count := |K|  (the full K-line, #212 Thm 1's
         worst-case bound |A_r| <= |K|); crude product := |K|^|R|.
```

Rows tabulated (qa3 C1, same flags apply):

- **pinned:** `n=512, k=256, q = 17^32` exact (`log2 q = 130.79881`).
  Task pin `t* = 5` is `A = 261 = A*+1` in qa3 Table 1 (qa3's `A* = 260`,
  `t*_qa3 = 4`); `t = 6` (`A = 262 = A_zero`) is also shown. FLAG (qa3 F4):
  this row is a calibration row, tangent-pinned elsewhere.
- **Row C:** `n=1024, k=512` (rate 1/2), `log2 q = 250` **idealized exact**
  (qa3 FLAG C1(b): Row C's actual prime is unpinned). `t = 5` is the
  analogous crossing-window point `A*+1 = 517`; `t = 8` is the corridor
  candidate's safe side `A_quot+1 = 520` (qa3 Table 2).

## 2. Stage 1: the crude per-character count, exact arithmetic

The question reduces to one comparison per row. Crude product
`>= |K|^|R| >= q` (minimum at one active character, `|R| = 1`, on the lowest
tower level, `e = 1`, i.e. `K = B`), versus target `T(A) = n^3 FM(A)`:

```text
shortfall(|R|, e) := log2(crude product) - ZM(A) = |R| * e * log2 q - ZM(A).
```

Verifier-derived table (bits; exact `math.comb` + exact integer sign checks,
`q = 17^32` resp. `2^250` exact; floats only for reporting):

```text
row          A    t  j    log2 C(n,j)  ZM(A)      shortfall  shortfall
                                                  |R|=1,e=1  |R|=M=n,e=1
pinned t=5   261  5  251  507.03       +10.84     +119.96    +66958.2
pinned t=6   262  6  250  506.97       -120.02    +250.82    +67089.0
Row C  t=5   517  5  507  1018.60      +48.60     +201.40    +255951.4
Row C  t=8   520  8  504  1018.49      -701.51    +951.51    +256701.5
```

(`shortfall > 0` means the crude bound is TOO BIG by that many bits, i.e. it
fails to establish `product <= T(A)` by that margin.)

**Stage-1 verdict: INSUFFICIENT.** Even the floor case — a single active
character confined to a single base-field line — overshoots the corridor
target by `log2 q - ZM(A)`:

- pinned corridor point (`t = 5`): **short by 119.96 bits**;
- Row C crossing point (`t = 5`): **short by 201.40 bits**;
- Row C corridor candidate (`t = 8`): short by 951.51 bits.

**Dominating factor:** the line size `|K| >= q` (130.8 resp. 250 bits) against
a target budget `ZM(A)` of at most +49 bits anywhere in the corridor. The
active-character count and the tower level cannot help: they only multiply
the exponent (`|R| * e` lines), so the single-line, base-level case is the
minimum, and it already fails. Exact-integer form (verifier-checked):
`q^t > n^3 * C(n,j)` at all four rows, which is precisely the negation of
"crude product <= T(A)" at `|R| = e = 1`.

So stage 1 does NOT close the estimate; stage 2 is required.

## 3. Why the shortfall is structural (three failed shortcuts)

Three natural half-refinements, checked so the conjecture is stated in the
right form. Each is an arithmetic observation, not a claim of impossibility.

**(a) Fixed-support uniqueness is not the object.** For a FIXED `K_M`-stable
support `S` with `|S| = A > k` and fixed received word `w`, interpolation on
any `k` points of `S` determines the codeword, so at most ONE codeword aligns
and each `|A_r| <= 1`. The corridor mass lives in the **ensemble of supports**
(the `C(n,j)` ledger column): `A_r` collects values over all stable agreement
sets, so per-character counting must price the support ensemble, not one `S`.

**(b) Support-counting alone is also short.** Bounding `|A_r|` by the number
of `K_M`-stable supports, `C(n/M, ~j/M)`, gives at `M = 2`: 251.63 bits
(pinned `t=5`) resp. 507.15 bits (Row C `t=5`) — short of `ZM` by 240.8 resp.
458.6 bits (verifier rows S1-S2). The missing factor is exactly the mean
discount `q^(1-t)`: most stable supports must admit NO aligned codeword, and
the needed estimate has to capture that at the quotient scale.

**(c) Per-leaf FM bounds do not aggregate.** The quotient-row instance behind
character `r` (sect. 4) has parameters `(n/M, ~k/M, A/M)`, hence
`t' = t/M < 1` whenever `M > t` — the leaf sits AT OR BELOW its own
mean-crossing (`x1_quotient_reduction.md`'s "below reserve" caveat), where
`max(1, FM_leaf) >= q^(1 - t/M)` is huge. Multiplying such per-leaf bounds
over `|R| = M` active characters gives a `q^(M-t)` factor against the
parent's `q^(1-t)`: an overshoot of `q^(M-1)`. So NO per-character bound of
the form `|A_r| <= poly * max(1, FM_leaf)` can suffice by itself; the needed
statement is **joint** across the active set.

## 4. Stage 2: the terminal reserve conjecture [CONJECTURE — not proved]

Setting, following #212 exactly: `RS_q(H_n, k)` = polynomials of degree `< k`
evaluated on `H_n`; `Agr(c, w) = {x in H_n : c(x) = w(x)}`; for `K_M`-stable
`S = Agr(c, w)`, the `r`-isotypic component of `c` on `S` interpolates as
`X^r G_r(X^M)`, `G_r` over `B` (#212 Thm 1). Define the **aligned
per-character image** (the `K`-line intersected with the alignment
condition):

```text
A_r(w, A, M, alpha) :=
  { alpha^r * G_r(beta) :
      c in RS_q(H_n, k),
      Agr(c, w) is K_M-stable,  |Agr(c, w)| >= A,
      X^r G_r(X^M) = the r-isotypic part of c on Agr(c, w) }.
```

By #212 Thm 1, `A_r subseteq alpha^r K`; the alignment condition is what cuts
it below the crude `|K|`.

**Conjecture TR (GAP-1 terminal reserve).** *There exists an absolute
constant `B_TR` (independent of `q`, `n`, `k`, `A`, `M`, the tower, `alpha`,
`w`, `R`) such that: for every prime power `q`, every `n | q-1`, every
`k < n`, every agreement `A` with `A >= A*(n,k,q) + 2` (the corridor side of
the qa3 crossing, `A_zero`), every period `M | n` with `M >= 2`, every field
tower `B = F_q <= K <= F`, every `alpha in F^*` with `beta := alpha^M in K`,
every received word `w : H_n -> B`, and every active set `R subseteq Z/M`:*

```text
product_{r in R} |A_r(w, A, M, alpha)|  <=  n^B_TR * max(1, C(n, n-A) * q^(1-(A-k))).
```

Quantifier structure, explicitly: `EXISTS B_TR, FORALL (q, n, k, A, M, tower,
alpha, w, R)` — `B_TR` first, uniform in everything, in particular in `q`
(else the corridor's `q >= 2^128`-scale rows leak) and in `M` (else the
divisor union costs more than poly(n)).

**Multi-scale reading** (via `x1_quotient_reduction.md`): each `A_r` is the
slope image at deep point `beta` of the quotient-row instance
`(H_{n/M}, k_r, q)` with `k_r = ceil((k-r)/M)`, received word = the
`M`-quotient of the `r`-isotypic part of `w`, at quotient agreement
`>= A/M` — a same-rate instance one level down. Conjecture TR says: the
**terminal leaves jointly obey the parent row's corridor budget**, even
though (sect. 3(c)) each leaf separately sits below its own reserve when
`M > t`. Combined with #212's Theorems 2-3 (product bound + tower
recursion), TR implies `gap1_noneq_mass <= n^B_TR * max(1, FM)` at every
corridor point — that implication is bookkeeping over #212's proved
statements, but TR itself is open. This is the same per-scale
reserve/cancellation barrier already isolated in
`x1_quotient_reduction.md`'s caveat, now with the exact object (`A_r`), the
exact inequality, and the exact quantifier order pinned.

**What evidence exists:** the E6 + #212 verifiers (F_13/F_97/F_257 toys,
`F_17(alpha)` tower) confirm the PRODUCT mechanism with no cross-character
amplification, and this note's verifier re-confirms the F_13 shape. None of
them test TR's reserve content at corridor scale. [No corridor-scale
evidence exists yet; a natural next packet is a small-field ensemble census
of `|A_r|` against `max(1, FM_leaf)` vs the parent budget.]

## 5. Non-claims

- Conjecture TR is NOT proved here, and no evidence beyond toy scale is
  claimed for it. Stage 1's verdict is arithmetic about a specific crude
  bound, not a lower bound on `|A_r|` (no counterexample is claimed either).
- Sect. 3's items are arithmetic observations about three candidate bounds,
  not impossibility proofs for refinements of them.
- Nothing here proves or modifies `gap1_noneq_mass`, R2, zone-(b), imgfib,
  or any Paper A-D statement; the DAG JSON is untouched.
- Row C numbers inherit qa3 FLAG C1(b) (idealized `log2 q = 250`; true prime
  unpinned): margins shift by `<= (t-1)*|eps|` bits. The pinned-row `t* = 5`
  convention is the task's pin (`= A*+1` of qa3); qa3's own `t*` is 4.
- The `B = 3` poly budget is conventional (qa3 C3); TR deliberately allows
  any absolute `B_TR`. The stage-1 verdict is insensitive to this: absorbing
  even the smallest shortfall above (119.96 bits at pinned, `log2 n = 9`)
  inside the polynomial would need `B >= 3 + 119.96/9 = 16.3`, and the
  shortfall grows with `q` while `poly(n)` does not — the obstruction is the
  `q`-factor, not the polynomial.

## 6. Verification

```bash
python3 experimental/scripts/verify_gap1_terminal_reserve.py
```

Deterministic, stdlib only. Checks, with PASS/FAIL per row and exit 0 iff
all pass:

1. **Stage-1 table (rows T1-T4):** recomputes `log2 C(n,j)`, `ZM(A)`, and
   both shortfall columns for the four rows of sect. 2; exact-integer sign
   checks (`q^t > n^3 C(n,j)` with `17^32` resp. `2^250` exact); cross-checks
   `ZM` against qa3 Table 1/2 reference values (+10.84, -120.02, +48.60,
   -701.51) to 0.02 bits.
2. **Support-count shortcut (rows S1-S2):** sect. 3(b) numbers.
3. **Aggregation failure (row S3):** sect. 3(c)'s `q^(M-t)` overshoot at
   `M = 8 > t = 5`, pinned row, exact integers.
4. **#212 shape on the E6 F_13 toy (rows F13-M2, F13-M4):** `p = 13`,
   `H_12 = <2>`, `alpha = sqrt(2) in F_169` (so `alpha^M in F_13` for
   `M in {2,4}`), all `K_M`-stable supports, all nonempty active sets:
   per-character images land in the line `alpha^r F_13` (confinement), each
   per-character rank `<= 1`, and combined rank `<=` sum of per-character
   ranks (the #212 Thm 2 rank form). Exact linear algebra mod 13.
