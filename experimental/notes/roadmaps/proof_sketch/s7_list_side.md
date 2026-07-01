# S7: the list side — grand challenge 2 through the same dictionary

- **Status:** PROVED-cited lower bounds + verified arithmetic + the L1
  CONJECTURE input clearly quarantined. NOT rigorous as a whole.
- **Parent:** `prize_proof_sketch_spine.md` S7. Numerics machine-checked.

## 1. Two different thresholds — do not conflate them [important]

Paper B's dyadic reserve `eta >= max{tau*(rho, q_D), Theta_rho(1/log n)}`
concerns POLYNOMIAL lists. The PRIZE gate is different: it asks where
`|Lambda(C^{==m}, delta)|` crosses `2^-128 |F| ~ 2^128`. At that gate the
`1/log n` scale is irrelevant and both mechanisms land back on `1/log q`:

```text
poly-list threshold:   slack sigma ~ n/log n     (quotient cores, academic)
prize-gate threshold:  slack sigma ~ n H(rho)/log2 q ~ n tau*   (both mechanisms)
```

## 2. The unsafe half at the prize gate is UNCONDITIONAL [PROVED-cited + verified]

`thm:qcore`: quotient cores produce `>= C(n/M - 1, k/M)` codewords at
agreement `k + sigma` whenever `M | k` and `sigma < M` — *independently of
q*, a pure count (no norm threshold, no value-set collisions: codewords are
distinct by construction). Exponent check (verified):
`log2 C(n/M-1, k/M) ~ (n/M) H(rho)` (1017.7 vs 1024 at `n = 2^20, M = 2^10`).
Crossing `2^128` needs a 2-power `M | k` with `sigma < M <= n H(rho)/128`;
dyadic domains supply every scale (verified: plentiful at `n = 2^41`), giving
the crossing window (up to 2-power rounding):

```text
rate    list-unsafe slack window       delta window                MCA corridor (S2)
1/2     [H/256, H/128] = [.0039,.0078]  [0.492188, 0.496094]       [0.493809, 0.498047]
1/4     [.0032, .0063]                  [0.743662, 0.746831]       [0.744141, 0.748047]
1/8     [.0021, .0042]                  [0.870753, 0.872877]       [0.870854, 0.873047]
1/16    [.0013, .0026]                  [0.934865, 0.936182]       [0.934888, 0.936523]
```

**Two consequences.** (i) The list threshold sits FARTHER from capacity
than the MCA corridor: quotient cores hit lists with the FULL binomial
entropy `H(rho)`, while the MCA side is compressed to value sets
(`beta(rho) < H(rho)`, turn 4) — grand challenge 2's safe side binds before
grand challenge 1's. (ii) Unlike MCA's zone-(b) collision uncertainty, the
list-side unsafe half at the gate is UNCONDITIONAL once endpoint
conventions are checked — only the SAFE side of the list challenge is open.

## 3. Interleaved conversion [PROVED-cited (mine) + verified budgets]

The L2 codegree reduction (Theorems A/B/C, on main, L1-free) reduces
`m`-fold interleaved lists to base-list fibers at agreements `a` and
`2a - k`; the deep-point identity gives `BadVec = Deep_alpha^mu`, worst-case
`a`-regular collapse has interleaved list = base list (exponent exactly 1),
and the `K_{m,m}` clique cap `n >= k + m^2(a - k)` bounds amplification
linearly in `n`. Budget at the protocol row (`n = 2^40`, `mu = 2`,
`log2 q - 128 = 128`; re-derived this turn):

```text
interleaved-MCA term <= n^{eB}/q <= 2^-128  <=>  eB <= 128/40:
worst-case exponent (e = 2):   base-list exponent  B <= 1.60
a-regular collapse (e = 1):    B <= 3.20
```

consistent with the R2/SPI/XR poly budget `B <= 3` (turn 2) only in the
a-regular branch — the worst-case branch demands `B <= 1.6`, a genuinely
tighter target; flag: proving a-regularity reductions (or improving `e`)
is worth a full point of exponent. **Standing order 9 applies: the codegree
reduction consumes an L1 bound; it never supplies one.**

## 4. The L1 input — where it stands [CONJECTURE + populated escape]

Target: `#ImgFib_U(a) <= n^B` above the reserve
`eta >= (1 + eps) tau*(rho, q_D)` with the quotient profile budgeted (the
image-fiber object, never raw fibers). The proof program's frontier
(Theorem 21/B11) leaves one escape: full-petal sunflowers with cofactor
excess `d - ell -> infinity`, and that branch is POPULATED (witnesses at
`d - ell = 2, 5`, p = 1009) with the exact-rank shortcut route-cut.
Dictionary to the sketch (turn 4): the sunflower core is a common divisor,
petals are the free part — full-petal extras are points on petal-structured
plane sections of the divisor set, i.e. **the L1 battle is Conjecture F for
its plane family**; FM at `q_gen` predicts poly extras above the reserve
[CONJECTURE]. One collision family, fourth appearance.

## 5. Assembly shape for grand challenge 2, and forks

```text
delta*_list(rho) in [1 - rho - H/128, 1 - rho - H/256]   (unsafe side proved-shape);
safe side = L1 image-fiber bound + codegree conversion + challenge-field
denominator printed; budgets B <= 1.6 / 3.2 as above.
```

```text
F1 (conventions): thm:qcore's agreement k + sigma vs the closed-radius
    grid — same endpoint audit as step 1; route to WP-0.1 before quoting
    the delta windows as prize-facing.
F2 (rounding): the [H/256, H/128] window is a 2-power artifact; exact
    optimization over M | k collapses it — a clean bottom-up lemma
    (compute the exact max over scales; likely lands near H/128).
F3 (L1 fails at reserve): the safe side of BOTH challenges moves; the
    sketch's posture is S9 (determine the new ledger, resolve lower).
F4 (a-regularity): if the a-regular collapse cannot be forced, the
    interleaved budget B <= 1.6 becomes the binding exponent target for
    the whole program — tighter than R2's B <= 3.
```
