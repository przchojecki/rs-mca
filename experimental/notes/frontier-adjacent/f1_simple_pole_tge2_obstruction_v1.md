# F1 simple-pole obstruction at `t >= 2`

Status: PROVED for the named simple-pole pencil / AUDIT.

This note explains the slack split in
`experimental/data/certificates/frontier-adjacent/f1_full_orbit_scan_v1.json`
for the specific pencil

```text
f_beta(x) = 1/(x - beta),     g(x) = x^k.
```

The scanner finds growth at toy slack `t=1`, but zero full-orbit bad slopes at
`t>=2` for the same pencil.  The zero branch is not a finite-field accident:
it follows from an elementary degree/root-count obstruction.

## Replay

```bash
python3 experimental/scripts/verify_f1_simple_pole_tge2_obstruction.py --check \
  experimental/data/certificates/frontier-adjacent/f1_simple_pole_tge2_obstruction_v1.json
```

The verifier freezes the algebraic proof skeleton and cross-checks it against
the current F1 scanner artifact.  When present, it also reads
`f1_effective_slack_translation_v1.json` and records that the deployed
adjacent rows land in `t>=2`.

## Statement

Let `F` be any field containing the domain values, let `S` be a support with
`beta notin S`, let `k>=1`, and let `t>=2` with `|S|=k+t`.  There is no slope
`gamma` and no polynomial `P` of degree `< k` such that

```text
P(x) = 1/(x-beta) + gamma*x^k       for every x in S.
```

## Proof

Assume such `P` and `gamma` exist.  Multiply out the pole and define

```text
R(X) = (X-beta)P(X) - gamma*(X-beta)*X^k - 1.
```

Then `R` vanishes on every point of `S`.  Since `deg(P)<k`, the degree of `R`
is at most `k+1`; the only possible `X^(k+1)` term is `-gamma*X^(k+1)`.

But `|S|=k+t>=k+2`, so `R` has more roots than its degree bound.  Hence `R`
is the zero polynomial.  The coefficient of `X^(k+1)` then forces
`gamma=0`.  With `gamma=0`,

```text
R(X) = (X-beta)P(X) - 1.
```

Evaluating the polynomial identity `R=0` at `X=beta` gives `-1=0`, impossible
in a field.  This contradiction proves the claim.

## Interpretation

The toy `t=1` branch is sharp: the same degree/root-count argument is exactly
one root short of contradiction.  At `t>=2`, the simple-pole pencil cannot
produce any bad slope on a support of size `k+t`.

Combined with `f1_effective_slack_translation_v1.json`, this says the current
deployed adjacent rows sit in the direct `t>=2` analogue, not in the growing
toy `t=1` branch.

## Non-claims

- This does **not** prove `paid_extension(a)` is safe.
- This does **not** classify all genuinely `F`-valued received pairs.
- This does **not** rule out `t>=2` growth for a different `F`-valued pencil.
- This does **not** close the frontier-adjacent extension cell.
- This does **not** resolve Q/BC/SP residuals in CAP25 v13.

## Next step

The useful falsification search is now narrower: find a genuinely `F`-valued
pair **other than** the simple-pole pencil whose `t>=2` constraints still leave
a growing full-orbit `K=F` slope set, or begin a proof-level classification of
which pencil shapes reduce to the same degree/root obstruction.
