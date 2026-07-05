# SOV Forced-Root Recursion Algebra

Status: PROVED.

Source DAG node: `sov_forced_root_recursion_algebra`.

## Statement

For every `h` over odd characteristic, the monic degree-`h` square-root
recursion uniquely recovers the degree-`h` polynomial `S` forced by the top
`h+1` coefficients of a monic degree-`2h` locator `L`. The obstruction vector
is exactly the list of coefficients of `S^2 - L` in degrees `1, ..., h-1`.

In the shifted-constant trade model, the recursion returns the midpoint and
all obstruction coordinates vanish.

## Proof

Write

```text
S(X) = X^h + s_{h-1}X^{h-1} + ... + s_0.
```

For `d = 2h-1, 2h-2, ..., h`, the coefficient of `X^d` in `S^2` has the form

```text
2 s_{d-h} + known higher terms.
```

The still-unknown coefficient `s_{d-h}` appears only in the two products with
the leading coefficient of `S`. All other terms use coefficients already
recovered at higher degrees. Since the characteristic is odd, `2` is
invertible, so the equation

```text
[X^d] S^2 = [X^d] L
```

solves uniquely for `s_{d-h}`. Descending from `d = 2h-1` to `d = h` recovers
all coefficients of `S`.

Once `S` is fixed, the obstruction coordinates are definitions:

```text
O_i = [X^i](S^2 - L),     1 <= i <= h-1.
```

For the shifted-constant trade model, take monic degree-`h` polynomials `A`
and `B` with `B - A = delta` constant, set `L = A B`, and set
`S = (A+B)/2`. Then

```text
S^2 - L = ((A+B)^2 - 4AB)/4 = (A-B)^2/4 = delta^2/4,
```

which is constant. Thus every obstruction coordinate in degrees `1, ..., h-1`
vanishes, and the recursion recovers the midpoint.

## Non-Claims

This packet proves the algebraic forced-root recursion and shifted-constant
gate. It does not prove the SOV value-set bound for actual anchored-core
families.

## Replay

Regenerate:

```bash
python3 experimental/scripts/verify_sov_forced_root_recursion_algebra.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_sov_forced_root_recursion_algebra.py \
  --check experimental/data/certificates/sov-forced-root-recursion-algebra/sov_forced_root_recursion_algebra.json
```

The verifier checks note anchors, the deterministic shifted-constant midpoint
cases, and the `O_{h-1}` sensitivity gate used by the next SOV packet.
