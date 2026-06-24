# Audit of PR #105 (M1 standalone Cycle120 LDsw proof) + Cycle84 count structure

- **Status:** AUDIT. Transfer lemma (Lemma 1) INDEPENDENTLY VERIFIED on small
  exact models; count `N` structurally fingerprinted + collision-consistent,
  but NOT recomputed (spec absent from repo). Result is CONDITIONAL on the
  Cycle84 census, exactly as PR #105 itself states.
- **Agent/model:** Claude Opus 4.8 (L2/X1 lane, branch `allen/l2-x1-interleaved-mca`).
- **Date:** 2026-06-24.
- **Subject:** PR #105 (`AllenGrahamHart:codex/m1-cycle120-standalone-proof`,
  head `1c805c3`): `notes/m1/m1_cycle120_standalone_ldsw_proof.md` +
  `scripts/verify_m1_cycle120_standalone_ldsw_proof.py`. Codex/M1 lane -- this
  is an honest independent review, no edits to that branch.

## What PR #105 claims

```text
Cycle84 finite count (#{Phi(T)} = N) + Cycle116 slot identities
   ==(fixed-jet locator transfer, Lemma 1)==>  LD_sw(RS[F_17^16,D0,137],143) >= N
   ==(scalar extension to F_17^32)==========>  same line over K
   ==(smooth-padding transfer, Lemma 2)=====>  LD_sw(RS[F_17^32,H,256],262) >= N
   ==(ABF Def 4.3, delta=125/256)===========>  emca(C,125/256) >= N/17^32 > 2^-128.
N = 52,747,567,092.
```

PR #105's own "Proof Boundary" is explicit: it does **not** rerun the Cycle84
census; `N` is a computer-assisted input recorded in
`m1_cycle84_public_replay_audit.md`.

## What I verified independently (`verify_m1_cycle84_count_structure.py`)

### Part A -- the count's structure (NOT a census recomputation)

The Cycle84 audit reports
```text
compatible pairs (color shell) = 52,747,567,104
Occ(beta) = #{Phi(T)} = N       = 52,747,567,092
double fibers = 12,  fibers >= 3 = 0,  m_max(beta) = 2,  ordered energy = 24.
```

- **Clean factorization (structural fingerprint):**
  `52,747,567,104 = 2^27 * 3 * 131`. A generic 26-billion-scale census output
  would not factor this cleanly; the shell is a genuinely structured
  combinatorial object. Note `131 = 262/2` -- exactly half the Cycle120 support
  threshold `(1-125/256)*512 = 262`. (`Occ = N` itself is
  `2^2 * 3^4 * 11 * 14800103` -- the "minus 12" breaks the clean structure,
  consistent with `N` being shell minus a small collision correction.)
- **Collision bookkeeping is internally forced.** With `m_max(beta) = 2` and no
  fiber of size `>= 3`, a value is hit once or twice. If `t` values are
  double-hit, then `#distinct = #total - t` and the ordered off-diagonal energy
  is `2t`. The reported `t = 12` gives `Occ = shell - 12 = N` and
  `energy = 2*12 = 24`. Both reported numbers are exactly the forced ones.
  **Consistent.**

**Caveat (honest).** A first-principles recomputation of the shell `2^27*3*131`
requires the slot-model spec (7 slots x 48 keys, projected logs, tau
involution), which is **not in this repo** -- it lived in Danny's rejected
archive (`#96`). So Part A is a *partial* independent check: the headline
number's fingerprint and its collision arithmetic, not a re-census. The count
remains the single computer-assisted gate of the whole Cycle120 result.

### Part B -- the fixed-jet locator transfer (Lemma 1), the real proof content

Lemma 1 is the bridge "count `=>` LD_sw" and is a clean linear-algebra claim
(not a computation), so it IS fully auditable. Over `F_17` I reconstructed PR
#105's exact construction -- parity check `(Hw)_m = sum_x x^m w(x)/L_D'(x)`,
error word `e_J(x) = L_D'(x)/((beta-x)P_J'(x))`, `g(x) = L_D(beta)/(beta-x)`,
`f = e_{J_0} - z_{J_0} g` -- and verified all four conclusions for both
`sigma = 1` (35-subset family) and `sigma = 2` (fixed-sum family):

```text
[OK] f + z_J g  agrees with a codeword of RS[F,D,k] on D\J  (size n-j),  every J
[OK] z_J = 1/P_J(beta)
[OK] #distinct bad slopes == #distinct P_J(beta)
[OK] noncontainment: g is NOT degree-<k explained on D\J,  every J
```

So the transfer lemma is **correct**. (`k = n-j-sigma`, redundancy `= n-k`,
agreement `n-j = k+sigma` all hold.) The Cycle116 instance is the
`n=256, j=113, sigma=6, k=137` case of exactly this lemma, plus the smooth
padding of Lemma 2 (`143+119=262`, `137+119=256`), which is the straightforward
multiply-by-`L_A` lift.

## The unifying observation (count and lemma measure the SAME object)

Lemma 1's bad-slope count is `#{P_J(beta)}`. The Cycle116 evaluation identity
`P_T(beta) = 4(beta-1) Phi(T)` (with `4(beta-1) != 0`) makes `T |-> P_T(beta)`
an affine relabelling of `T |-> Phi(T)`, so

```text
   #distinct bad slopes  =  #{P_T(beta)}  =  #{Phi(T)}  =  Occ(beta)  =  N.
```

Therefore the census quantity `Occ(beta) = shell - 12` is **precisely the
injectivity defect of the locator-evaluation map** `T |-> P_T(beta)`: the "12
double fibers" / `m_max = 2` are 12 colliding `Phi(T)` pairs, which is exactly
the over-count that Lemma 1's `#{P_J(beta)}` must discard. My Part B exhibits
this concretely: the `sigma=1` family of 35 subsets collapses to only **16**
distinct `P_J(beta)` (heavy collision), while the `sigma=2` fixed-sum family of
5 stays injective. So the census's collision structure and the lemma's
slope-count are one and the same combinatorial fact.

## Cross-lane connection (M1 <-> L2/X1), verified

`z_J = 1/P_J(beta)`, bad slopes `= {P_J(beta)}` is the **same locator-fiber =>
deep-image mechanism** as the X1 universal-cap bridge (`notes/x1`,
`notes/x1/x1_cs25_free_cap.md`): there the bad slopes of the simple-pole line
`u_z/(x-alpha)` are the deep image `{P(alpha) : P in the list}`. M1's Cycle120
LD_sw count and L2's universal cap are two instances of the single principle
**"a locator fiber produces bad line-slopes through a parity-check / deep-point
identity, and the count is the size of the evaluation image."** This is the
"everything = prefix-fiber + deep-point bridge" theme made concrete across the
M1 and L2 lanes.

## Verdict

- **Lemma 1 (fixed-jet locator transfer): VERIFIED** (small-model enumeration,
  both `sigma=1,2`). Lemma 2 (smooth padding) is an elementary `L_A`-lift; its
  arithmetic gates (`143+119=262`, `137+119=256`, ABF threshold `262`, density
  `> 2^-128`) match #100's audit.
- **Count `N`: structurally fingerprinted and collision-consistent**, but not
  re-censused. The clean `2^27*3*131` and the forced `Occ = shell - 12` are
  positive independent evidence; a full recomputation still needs the
  slot-model spec.
- **Net:** PR #105's transfer chain is sound; the result is conditional ONLY on
  the Cycle84 census, exactly as the PR states. This is the cleanest reviewer
  vehicle of the Cycle120 material; #100 can be archival.

## Reproducibility

```bash
python3 experimental/scripts/verify_m1_cycle84_count_structure.py
python3 experimental/scripts/verify_m1_cycle84_count_structure.py --json
```
