# SOV H-minus-1 Fiber Fourier Duality

Status: PROVED.

Source DAG node: `sov_hminus1_fiber_fourier_duality`.

## Statement

Fix an official-shape row, an `h in (20,A]`, and one forced-root
higher-coefficient conditioning cell of anchored-core locators. Let

```text
c(L) = [X^{h-1}]L
```

be the `h-1` locator coefficient map from the finite conditioned family
`Omega` to the row field `F`. For every value `a in F`,

```text
|{L in Omega : c(L)=a}|
  <= |Omega|/|F| + |F|^{-1} sum_{xi != 0} |S(xi)|,

S(xi) = sum_{L in Omega} psi(xi c(L)),
```

where `psi` is any nontrivial additive character of `F`.

## Proof

The additive-character orthogonality relation says that, for every `u in F`,

```text
1_{u=0} = |F|^{-1} sum_{xi in F} psi(xi u).
```

Apply this with `u = c(L) - a` and sum over `L in Omega`:

```text
N(a)
 = sum_{L in Omega} 1_{c(L)=a}
 = |F|^{-1} sum_{xi in F} psi(-xi a)
       sum_{L in Omega} psi(xi c(L)).
```

The `xi=0` term is exactly `|Omega|/|F|`. For each nonzero `xi`, multiplication
by `psi(-xi a)` has absolute value one. The triangle inequality gives

```text
N(a) <= |Omega|/|F|
        + |F|^{-1} sum_{xi != 0} |S(xi)|.
```

Thus any project-specific bound on the nontrivial sums `S(xi)` immediately
gives a uniform fiber bound for `[X^{h-1}]L`.

## Non-Claims

This packet proves only the Fourier inversion reduction. It does not bound the
nontrivial sums for the actual anchored-core families; that remains the
content of the SOV character-sum nodes.

## Replay

Regenerate:

```bash
python3 experimental/scripts/verify_sov_hminus1_fiber_fourier_duality.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_sov_hminus1_fiber_fourier_duality.py \
  --check experimental/data/certificates/sov-hminus1-fiber-fourier-duality/sov_hminus1_fiber_fourier_duality.json
```

The verifier checks note anchors and exact Fourier reconstruction on a tiny
prime-field sample.
