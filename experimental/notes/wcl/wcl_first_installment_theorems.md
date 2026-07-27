# WCL register: first installment of closed-cell theorems

- **Status:** PROVED (five finite theorems) / EXPERIMENTAL verifier.
- **Channel:** fulfilment of the already-integrated contributor register
  `experimental/notes/wcl_slot_contributor_requests.md`. That register cites
  the `(2,5)`/`(2,6)` closures **by SHA-pin only**; this installment lands the
  theorems themselves, so the register becomes self-contained while CQ-1..CQ-4
  remain open asks. No new pitch, and no change to any open request.
- **Agent/model:** Claude Fable 5 acting for AllenGrahamHart.
- **Replay:** `python3 experimental/scripts/verify_wcl_first_installment.py`
  (stdlib, exact integers, no network). Estimated CPU time: seconds.

## Scope discipline (read first)

Every theorem below is stated **with its exact window and root order**, because
the failure mode this family invites is using a result proved at one level at a
different level. In the register's notation, cell `(ell, w)` lives at root order
`512*ell` with support window `[0, 256*ell)`.

- The weight-3 and weight-4 ambient exclusions are proved at **`ell = 1`
  only** (order 512, exponents in `[0,256)`). They are used in the shipped
  completeness derivation *only* as the pair `{(1,3), (1,4)}`. At `ell >= 2`
  the Newton short-window floor `w >= 2*ell + 1` already excludes weights 3
  and 4, so no order-1024 or order-2048 version of them is needed, claimed, or
  relied upon anywhere.
- The `(2,5)` and `(2,6)` theorems are proved at **order 1024** directly
  (resultants against `X^512+1`), not lifted from `ell = 1`.

## T1. `(2,5)` norm-gcd exclusion [order 1024]

No reduced signed weight-5 polynomial `P` with support a 5-subset of
`[0, 512)` satisfies `P(omega) = P(omega^3) = 0` for `omega` of exact order
1024 with the associated norm carrying an official-admissible prime divisor
(`q < 2^256`, `v_2(q-1) >= 41`).

```text
orbits 1514 | gcd stack 507 | 168 Pocklington-certified roots
prime graph 282 nodes | max v_2(q-1) = 18 (cap 41) | max gcd 9137 bits
3/3 negative controls
```

## T2. `(2,6)` recursive-norm exclusion [order 1024] (+ split16 counterfixture)

Same predicate at weight 6. Closed by a recursive-norm census.

```text
candidates 404,740 | batches 3163 | 443 primes | prime graph 626 nodes
double-zero survivors 510 | max v_2(q-1) = 18 (cap 41) | 6/6 mutation controls
```

The packet carries the **split16 counterfixture**: an instance at
`v_2 = 16` that is *not* excluded, which pins that the admissibility gate
`v_2(q-1) >= 41` is load-bearing rather than decorative.

## T3. Weight-3 ambient exclusion [`ell = 1`, order 512]

No reduced signed weight-3 polynomial with exponents in `[0,256)` has
`Res(X^256+1, P)` divisible by an official-admissible prime.

```text
254 affine-Galois classes | 11,054,080 supports covered | 14 CRT moduli
439 factor roots | prime graph 1498 nodes | max v_2(q-1) = 18
5/5 negative controls
```

## T4. Weight-4 ambient exclusion [`ell = 1`, order 512]

Same at weight 4, over all `C(256,4)*2^3 = 1,398,341,120` reduced signed
polynomials.

```text
24,979 affine-Galois classes | normalized section 1,014,080 keys | max orbit 516
17 CRT moduli | 88,086 factor records | 44,599 distinct primes
Pocklington graph 154,086 nodes | max v_2(q-1) = 29 (cap 41)
5/5 + 4/4 negative controls (ledger + primes)
```

Exactness mechanism: every resultant is recomputed modulo enough certified
31-bit split primes that their product exceeds `2*4^256`; with
`0 <= Res(X^256+1,P) <= 4^256` the modular equality is then exact.

## T5. Newton short-window exclusion

A reduced vanisher at level dimension `ell` needs weight `w >= 2*ell + 1`.
This is the floor the register's completeness derivation uses to bound the
window from below.

```text
208,373 finite sets | 969 paired hits | 6 residual slots
3 boundary controls | 6/6 negative controls
```

## What this does and does not do

- It makes the register self-contained for its two closed cells and the three
  supporting theorems its completeness derivation names.
- **It closes none of the ten open cells.** `(1,5)`, `(1,6)`, `(2,7)`, `(4,9)`
  and the four extended cells remain exactly as requested.
- Survival sampling is not discharge; nothing here converts a partial sweep
  into a closure.
- It changes no cost estimate and no compute request.

## Register maintenance folded in

Three corrections to `wcl_slot_contributor_requests.md`, all of which reduce
the chance a contributor burns cycles on the wrong thing:

1. **Norm(u) order-1024 scope note (soundness).** The weight-3/4 ambient
   exclusions are `ell = 1` theorems. The register now says so explicitly at
   the point of citation, and records that `ell >= 2` is covered by the Newton
   floor rather than by an order-1024 census. This forecloses the reading in
   which a contributor assumes an order-1024 weight-4 result exists.
2. **gcd benchmark note (cost).** CQ-3's gcd stage is ~60% of its cost at the
   pure-integer reference rate; the GMP/FLINT swap is the named optimisation
   target and is still **unmeasured**. The register now marks that figure as an
   unmeasured projection rather than a measured rate.
3. **CQ-2 stage-0 status (readiness).** The two named repairs — re-shard the
   final aggregation, add an ECM stage for slow-factoring tail norms — are
   listed as the gating items, so CQ-2 is not picked up before they land.
