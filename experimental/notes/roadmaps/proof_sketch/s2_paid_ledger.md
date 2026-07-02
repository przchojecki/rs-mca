# S2: Paid(A) as one computable function — and the refined threshold bracket

- **Status:** mixed, labelled per node: one PROVABLE-elementary lemma
  (toy-verified exactly), PROVED-cited ledgers, and the quotient-collision
  CONJECTURE zone. All numerics machine-checked.
- **Parent:** `prize_proof_sketch_spine.md` S2 (and feeds S8 / WP-2.4).

## 1. Components of Paid(A) [statuses per component]

For a row `(n, k, q = q_line)` at exact agreement `A` (`t = A-k`, `j = n-A`):

```text
B_tan(A)  <= n - A + 1        PROVED-cited (#147 staircase range); at prize
                              scale n <= 2^41 << B* ~ 2^128: NEVER binds.
                              At small q it is the whole story (506/507).
B_quot(A)                     three zones, SS3 below — the load-bearing term.
B_ext(A)                      lower-side floor PROVED-cited (v10 extension
                              pole, numerator ceil(L(|F|-|B|)/(|F|-|B|+kL)));
                              poly-shaped; safe-side classification = S6.
```

## 2. The first moment is a THEOREM, not a heuristic [PROVABLE + verified]

**Lemma FM1 (exact aperiodic first moment).** For `(u,v)` uniform and
independent, and any exact agreement `A` with `t <= A` (always, since
`A = k + t`):

```text
E[ #aligned locators ]  =  C(n,j) * (1 - q^-t) * q^(1-t).
```

*Route (one page):* for each locator `l`, the syndrome map
`u -> (sum_x u(x) l(x) x^m)_{m=1..t}` is SURJECTIVE (diag(l-values) has rank
`A >= t`, then a Vandermonde row block; machine-checked: all 495 maps of the
F_13 toy have full rank 5), so `(a,b)` is uniform on `F^t x F^t` and
`P[b != 0, a in span(b)] = (1-q^-t) q^(1-t)` exactly; linearity sums it.

*Verification:* F_13 toy (`n=12, k=3, A=8`): exact `E = 0.017333`; empirical
mean over 1500 uniform pairs `= 0.017333` (26 hits vs 26.0 expected).

**Consequence for the sketch's honesty ledger:** the FM engine's mean is
exact. ALL remaining heuristic content sits in exactly two places:

```text
(i)  safe side:   worst-case pairs vs the mean  (R2 / SPI / XR / Conj F);
(ii) unsafe side: locators -> slopes conversion (fiber control, Conj F again).
```

## 3. The quotient term: three zones [PROVED-cited / CONJECTURE]

`prop:qfloor` (Paper B source): at quotient order `N' = n/t'` the canonical
line has `>= Acl(N', rho N'+1) = 2^{beta(rho) N'(1-o(1))}` bad slopes, EXACT
above the norm threshold `p > (2 l')^{N'/2}`, `l' = rho N' + 1`. With
(machine-verified) `beta = 0.7925 / 0.75 / 0.5306 / 0.3343` at the four rates:

```text
zone (a) N' small (norm threshold holds; at log2 q = 256 and rho = 1/2:
         N' <= 80, since (80/2)log2(82) = 254.3 <= 256 < 262.1 at N' = 82):
         mass PROVED-exact = 2^{beta N'} <= 2^63.4  — far below B* = 2^128.
zone (b) 80 < N' < ~512: mass CONJECTURAL, bracketed by
         [DdH floor rho(1-rho)N'^2 ,  2^{beta N'(1-o(1))}] — the collision
         question for e_1-value-sets mod p, WHICH IS prob:perfiber AT
         sigma = 1: "prefix-equal mod p but not in Z[zeta]". Both sides of
         the threshold reduce to the same collision family.
zone (c) the Paper D cap construction proves unsafe at eta = 2^-9 (2^-10)
         regardless of zone-(b) resolution.
```

## 4. The threshold equation and the refined bracket [verified table]

Unsafe when `max(B_quot(A), B_ap(A)) > B*`. Crossings at `log2 q = 256`:

```text
quotient (collision-free): beta/eta = 128  =>  eta_q = beta/128
aperiodic FM:              n H(delta) = 256 t - 128
cap (proved):              eta = 2^-9 (2^-10 at rho = 1/16)

rate    quot crossing   FM crossing    cap        (all: quot < FM < cap ✓)
1/2     0.493809        0.496094       0.498047
1/4     0.744141        0.746811       0.748047
1/8     0.870854        0.872853       0.873047
1/16    0.934888        0.936162       0.936523
```

**Refined prediction R1'.** `delta*` is pinned in
`[1 - rho - beta(rho)/(log2 q - 128), cap]`, and WHICH mechanism decides it
is a zone-(b) question: collision-free quotient mass => the left end;
heavy collisions => the aperiodic FM point; the cap caps it either way.
The corridor widths are 2.17 / 2.00 / 1.12 / 1.67 grid steps of the cap
reserve (`2^-9`, `2^-10` at rho=1/16) per rate [corrected in the turn-13
coherence pass; verified in s8_s9]. Note the pleasing shape:
`delta* = 1 - rho - Theta(1/log q)` in every branch — R1 survives, sharpened.

**Coherence check (pinned row) — with a correction to turn 1.** At `B* = 6`
the tangent term `n - A + 1 > 6` for EVERY `A < 507`, so the pinned row is
unsafe at all lower agreements via tangent alone and the quotient/FM
crossings are moot there: the threshold is tangent-pinned at 506/507 (SS1),
exactly as proved. This exposes a mislabel in spine SS3: the "open
`LD_sw(C,265) <= 6`" prediction CANNOT refer to the raw row (raw
`LD_sw(C,265) >= 248` by the tangent floor); the open A=265 target is the
quotient/tangent-STRIPPED slack instance (the F1 `t=9` object / `Lambda^aper`).
FM correctly predicts that STRIPPED count `~ 0`; the spine's P2 is restated
accordingly (corrected this turn).

## 5. Paid(A) for the assembly compiler [feeds S8 / WP-2.4]

```text
Paid(A | row, profile):
  tan  = (n - A + 1) if staircase-active(A) else tangent-ledger(A)
  quot = sum over active quotient orders N' | n, N' <= n/t:
           zone(a): Acl(N', rho N'+1)              [exact, cited]
           zone(b): interval [DdH(N'), 2^{beta N'}] [conditional cell]
           zone(c): cap witness mass                [cited]
  ext  = extension-pole numerator                    [cited; S6 classifies]
  return tan + quot + ext   (deduped per checker logic, WP-0.4)
```

M4 tables (WP-2.4) should print zone-(b) entries as intervals, never points.

## 6. Forks

```text
F1: zone (b) resolves collision-free (value sets full) -> delta* at the left
    end; the unsafe side needs no new construction, only the collision count;
    prob:perfiber sigma=1 becomes BOTH the safe-side wall and the unsafe-side
    locator — one statement decides the prize corridor.
F2: zone (b) resolves heavily-collided -> delta* at the FM point; the unsafe
    side then needs the averaged fiber-to-slope conversion (Conj F averaged,
    plausibly provable) to convert locator mean into slope existence.
F3: norm-threshold improvements (better cyclotomic norm bounds) push zone (a)
    upward — each improvement moves the PROVED part of the bracket; a
    quantified target for the bottom-up lane: extend prop:qfloor's
    exactness from N' <= 80 toward N' ~ 161 at 2^256.
F4: the o(1) in 2^{beta N'(1-o(1))} matters at the corridor scale ->
    second-order term of Acl needed; flag to Paper B owners before any
    numeric prediction is quoted as sharp.
```
