# L1 official m=4, h=3 split-pencil emptiness v1

**Status:** PROVED EXHAUSTIVE STRATUM CLOSURE / FOUR OFFICIAL ROWS /
DEPLOYED ROWS UNTOUCHED / L1 OPEN.

An exact finite closure: on every official `m=4` row of the family below, the
`h=3` split-pencil stratum is **empty**. This is a row-exhaustive statement,
not a local reduction — the distinction the workboard M1 entry draws when it
notes that existing one-shell and rooted-shell packets are local reductions
rather than exhaustive row bounds.

## Row dictionary (read this first)

The family is

```text
n = 4(p+1),      p a Mersenne prime,
```

giving exactly four official rows:

| `p` | `p` as `2^e - 1` | `n = 4(p+1)` |
|---|---|---|
| 8191 | `2^13 - 1` | 32768 |
| 131071 | `2^17 - 1` | 524288 |
| 524287 | `2^19 - 1` | 2097152 |
| 2147483647 | `2^31 - 1` | 8589934592 |

**A collision worth naming explicitly.** The third row has `n = 2097152`,
which is also the domain size of the deployed KoalaBear setup. They are
different rows and share nothing but that integer:

```text
deployed:  n = 2097152,  p = 2130706433     4(p+1) = 8522825736 != n
this family at n = 2097152:  p = n/4 - 1 = 524287 != 2130706433
```

The deployed row does not satisfy `n = 4(p+1)` and is **not** in this family.
Nothing in this packet says anything about it. The verifier asserts both
directions of that fence so the claim cannot drift.

## Statement

For every official row `(n,p)` above there is no first-checkpoint split pencil
with exactly three complete degree-`p` fibers. Equivalently the complete
official `m=4, h=3` stratum is empty.

## Proof shape

Stratify by the tangent multiplicity `nu` at the depressed-Weierstrass
stationary point, writing `g(y) = y^3 + ay + b`, `Delta = -4a^3 - 27b^2`, and
`y_0 = -3b/(2a)`.

- `nu > 0` — excluded by the tangent-multiplicity computation; the splits are
  `(nu,eta) in {(1,2),(2,1)}`.
- `nu = 0`, `b = 0` — excluded by the Euler/quotient factorization.
- `nu = 0`, `b != 0` — four auxiliary-fiber sub-cases `h_0..h_3`, each excluded
  by the scalar-equation equivalence below.

Six terminal cases in total, and they are exhaustive.

Three identities carry the local algebra:

```text
(I1)  8a^3 g(y_0)                     = b*Delta
(I2)  4 y_0 Delta                     = -48 a^2 g(y_0)          (kappa_1 = kappa_2)
(I3)  4a^3 ( g(y_0) - y_0(3y_0^2+a) ) = -b*Delta
```

and the `nu = 0`, `b != 0` branch turns on the equivalence

```text
h_0 = kappa_2   <==>   r*Delta + 12 a^2 g(r) = 0.
```

## What the verifier establishes

`experimental/scripts/verify_l1_m4_h3_official_emptiness_v1.py`:

- **(I1)–(I3) as rational-function identities over `Q(a,b)`**, not spot checks.
  Each cleared identity is a polynomial of total degree at most 7; the script
  verifies vanishing on an 11x11 grid of distinct values, which over an
  integral domain forces the polynomial to be identically zero. 363 exact
  `Fraction` checks, no floating point.
- **The `nu=0` nonzero-`b` equivalence replayed modulo each of the four
  official primes** — 1792 checks. (The in-tree verifier for this branch runs
  at `p = 7, 31, 127` only; moving the replay onto the actual official primes
  is a strengthening, done for this export.)
- **The row dictionary and the deployed-row fence**, both directions.
- **The case-exhaustion count**: two positive splits, six terminal cases.
- **Two mutation controls** — perturbing the discriminant normalization
  (`27 -> 26`) and the stationary point (`2a -> 3a`), each of which must break
  an identity.

```text
L1_M4_H3_OFFICIAL_EMPTINESS_PASS identities=363 official_prime_replay=1792
  row_checks=20 case_checks=8 mutations=2
  rows=[8191, 131071, 524287, 2147483647]
  deployed_koalabear=excluded_from_family
```

The stratification argument itself — that the six cases are exhaustive — is
prose, above and in the source packet; the script does not re-derive it. That
boundary is stated deliberately rather than blurred.

## Non-claims

- **Nothing about the deployed rows.** See the fence above.
- Does not classify nonembedded `m=4, h=2`.
- Does not treat the `m=8` or `m=16` strata.
- Does not treat width above `p`.
- Does not close L1, and does not close the mixed-petal amplification consumer,
  which remains open.
- The primitive shift-pair ledger and the two-value classification remain open.
- No asymptotic statement: this is an exact finite closure on four rows.

## Falsifier

A first-checkpoint split pencil with exactly three complete degree-`p` fibers
on any of the four official rows; a failure of (I1)–(I3) as identities; a
counterexample to the scalar-equation equivalence at an official prime; or a
seventh terminal case in the stratification.

## Provenance

Source packet: in-tree node `l1_m4_h3_official_emptiness` with six terminal
suppliers (`cartier_resonance_reduction`, `positive_tangent_multiplicity_
exclusion`, `nu0_zero_b_euler_exclusion`, `nu0_nonzero_b_tangent_exclusion`,
`nu0_h0_auxiliary_fiber_exclusion`, `nu0_h3_tangent_multiplicity_exclusion`),
audited and triple-replayed. The exported verifier is a re-derivation for this
packet, not a copy: it upgrades the identity checks to grid-proofs and moves
the modular replay onto the official primes.

- Verifier: `experimental/scripts/verify_l1_m4_h3_official_emptiness_v1.py`
- Certificate: `experimental/data/certificates/l1-m4-h3-official-emptiness-v1/l1_m4_h3_official_emptiness_v1.json`
