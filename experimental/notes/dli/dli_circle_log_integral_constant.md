# DLI Circle Log-Integral Constant

Status: PROVED.

Source DAG node: `dli_circle_log_integral_constant`.

## Statement

The exact circle constant in DLI is

```text
int_0^1 log |cos(2 pi x)|^2 dx = -2 log 2.
```

## Proof

Use the classical integral

```text
int_0^{pi/2} log(cos u) du = -(pi/2) log 2.
```

By periodicity and symmetry,

```text
int_0^1 log |cos(2 pi x)| dx
  = (1 / 2pi) int_0^{2pi} log |cos u| du
  = (1 / 2pi) * 4 * int_0^{pi/2} log(cos u) du
  = -log 2.
```

Therefore

```text
int_0^1 log |cos(2 pi x)|^2 dx
  = 2 int_0^1 log |cos(2 pi x)| dx
  = -2 log 2.
```

## Non-Claims

This packet proves only the scalar circle integral. It does not prove
equidistribution of any DLI sequence or any peak-mass estimate.

## Replay

Regenerate:

```bash
python3 experimental/scripts/verify_dli_circle_log_integral_constant.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_dli_circle_log_integral_constant.py \
  --check experimental/data/certificates/dli-circle-log-integral-constant/dli_circle_log_integral_constant.json
```

The verifier checks note anchors and a high-resolution midpoint-rule numerical
sanity check away from the logarithmic singularities.
