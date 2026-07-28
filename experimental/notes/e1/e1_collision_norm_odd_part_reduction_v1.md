# E1 collision norm criterion: the A3 odd-part reduction applies here too

**Status:** PROVED REDUCTION (TRANSFERRED, NOT NEW) / STRICTLY SHARPENS THE
PRACTICAL TEST / CLOSES NOTHING / FIRST-BAND TARGET OPEN.

**The reduction is already in this repository.** `a3_good_reduction_lemma.md`
uses it twice — `D_pt(n,h)` is defined as an *odd part*, and the good-reduction
argument turns on "`p` coprime to `delta_0` and to the odd part of the constant
`m`; the 2-power part is a unit". This note claims no novelty for the idea. It
observes only that `e1_collision_norm_criterion.md` does not apply it, and that
applying it there is what makes the bottom of the `N=256` first band closable
at all.

## The statement

The E1 criterion fixes a prime `p == 1 mod N` and asks whether `p` divides

```text
N_{B,B'} = Res(Phi_N(X), Delta_{B,B'}(X)).
```

That hypothesis already forces `p` **odd**. So writing

```text
R = 2^mu * R_odd,        R_odd odd,
```

divisibility by `p` cannot see the 2-part:

```text
p | R   <==>   p | R_odd.
```

Consequently the practical exclusion test — "`R < 2^250` implies no
pair-feasible row prime divides `R`" — may be run on `R_odd` in place of `R`.
It is **never weaker**, and **strictly stronger whenever `mu > 0`**.

That is the whole content. It is two lines, and it is the same two lines as in
A3, applied to a different family of norms.

## Why it is worth writing down: it decides a level

On one `N=256` first-band census at the level where the band bottoms out —
2,994 retained full-conductor vectors, 895 distinct norms:

```text
whole norms  R      at or above 2^250 :  6
odd parts    R_odd  at or above 2^250 :  0
largest 2-adic valuation observed     : 34
```

Six norms fail the whole-norm test. **Zero** fail the odd-part test. Without
the reduction that level does not close; with it, it does. The largest observed
valuation is 34, so on individual vectors the reduction can recover up to 34
bits — though at the binding maximiser it recovers only one, which was exactly
enough.

## The margin, which is the part worth your attention

At that level the binding value is the largest odd part, and it is **250 bits**:

```text
2^250 / max(R_odd) = 1.1152        (about 0.157 bits of headroom)
```

The criterion clears the threshold there by roughly **12%**. That is a
calibration datum about your criterion, not about our census: at the bottom of
this band, the exact-norm route is within an eighth of a bit of having nothing
left to say.

A single certified full-conductor witness at the same level makes the point
concrete:

```text
R       = 2 * R_odd,   249 bits
R_odd   = 248 bits, PRIME, and congruent to 1 mod 256
```

`R_odd` therefore satisfies this lane's row congruence `p == 1 mod N` with
`N = 256` — it is the right shape to be a row prime — and is excluded purely by
size, sitting a factor of about 5 below `2^250`.

## What the verifier establishes

`experimental/scripts/verify_e1_collision_norm_odd_part_v1.py`, exact integer
arithmetic throughout:

- the reduction itself over all odd primes below 400 with a seeded sweep of
  `(mu, R_odd)` — 924 checks;
- monotonicity (the odd-part test is never weaker) plus strictness witnesses —
  4,000 checks;
- internal consistency of the reported extremal data: `R_odd` odd, `R_odd | R`,
  the valuation and both bit lengths;
- the margin, pinned as an integer ratio so it cannot drift unnoticed;
- the witness: valuation, bit lengths, primality, and residue mod 256;
- two mutation controls, including that the reduction genuinely needs `p` odd.

```text
E1_COLLISION_NORM_ODD_PART_PASS reduction_checks=924 monotone_checks=4000
  census_norms_over=6 census_odd_over=0 max_valuation=34
  margin=2^250/max_odd=1115/1000 witness_factor_below=5 mutations=2
```

**Scope boundary, stated rather than blurred:** this script does **not** re-run
the census. The census figures are verified for internal consistency and
arithmetic, not for provenance.

## Non-claims

- **No novelty for the reduction.** It is A3's, cited above.
- Nothing is closed by this note — no variance level, no profile, no row, no
  prize terminal.
- The census that motivates it is not exported here; only its extremal data.
- Nothing is claimed for folded profile `(4,2,0)`, the later swap bands, or any
  `N != 256`.
- The witness is a full-conductor vector with a prime odd-part norm; it is
  **not** a collision, and not a counterexample to anything.
- No claim that the odd-part test suffices anywhere it has not been run.

## Falsifier

A prime `p == 1 mod N` dividing some `R` but not `R_odd`; a reported odd part
that is not the odd part of its norm; a recount making the margin at that level
larger than `1.1152`; or a demonstration that the E1 criterion does not in fact
require `p == 1 mod N`.
