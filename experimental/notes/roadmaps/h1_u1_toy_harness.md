# H1: U1 toy harness for the frozen v1 dictionary

- **DAG node:** `u1_pullback_dichotomy`.
- **Task:** H1.
- **Status:** EVIDENCE / HARNESS PASS.  This is a toy-scale validation of
  `u1_primitive_star_pte_bound (v1)`, not a proof of U1.
- **Verifier:** `experimental/scripts/verify_h1_u1_toy_harness.py`.
- **Certificate:**
  `experimental/data/certificates/h1-u1-toy-harness/h1_u1_toy_harness.json`.

## Harness

For each toy row, the verifier exhaustively enumerates all degree-`A`
locators with roots in `mu_n`, groups them by their top `t` coefficients, and
then, for every base locator in a same-top-`t` class, forms the canonical star
trade

```text
target = common core + P,
base   = common core + Q.
```

It checks the star-PTE normal form directly:

```text
e_r(P) = e_r(Q),      1 <= r <= t.
```

Then it applies the explicit v1 quotient and dihedral pullback filters from
the frozen grammar:

```text
psi = X^M,
psi = X^M + X^-M,
t < M <= floor(log2 n)^2.
```

The H1 pass condition is

```text
max_base survivors_after_v1_strip <= n^2.
```

## Checked Rows

```text
F17/mu8,   A=4,  t=3
F13/mu12,  A=5,  t=3
F13/mu12,  A=6,  t=3
F17/mu16,  A=6,  t=3
F17/mu16,  A=8,  t=3
F97/mu16,  A=8,  t=3
F41/mu20,  A=8,  t=3
F41/mu20,  A=10, t=3
F97/mu24,  A=8,  t=3
```

## Result

All checked rows pass the v1 survivor cap.  The strongest observed post-strip
base has only `10` survivors.

```text
max survivors/base: 10
max raw same-top trades/base: 14
```

The raw same-top list is already below `n^2` in every checked row, before the
v1 strip is applied.  The v1 quotient/dihedral filters still remove many
canonical star trades:

```text
F41/mu20, A=8:   23,030 paid star trades
F41/mu20, A=10:  44,850 paid star trades
F97/mu24, A=8:   68,418 paid star trades
```

The largest locator family found is the `F97/mu24, A=8, t=3` row:

```text
max same-top family size: 15
raw trades/base:          14
survivors/base:           7
n^2 cap:                  576
```

## Interpretation

The harness gives a reproducible scaffold for the U1 compression proof:
same-top families are reduced to canonical star trades, explicit v1-paid
pullbacks are stripped, and survivor counts are measured per base.  At these
toy rows, H1 passes with large slack.

The result does not prove U1.  It says the frozen v1 grammar survives the
checked primitive-star toy harness, and no base produces a post-strip survivor
family close to the `n^2` allowance.

## Verification

Run:

```bash
python3 experimental/scripts/verify_h1_u1_toy_harness.py
```

To refresh the pinned certificate:

```bash
python3 experimental/scripts/verify_h1_u1_toy_harness.py --write-certificate
```
