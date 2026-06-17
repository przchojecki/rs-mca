# F1 degree-1 residue-line witness certificate

Status: **EXPERIMENTAL / AUDIT**.

This folder contains a small, self-contained certificate for an explicit
genuinely extension-valued **degree-1 residue-line** same-set MCA-bad line,
aimed at the F1 direction in `agents.md`:

> decide whether MCA bounds over a base/generated field `B` lift cleanly to
> extension-valued lines over `F`, or whether genuinely `F`-valued residue
> denominators create new bad slopes.

The toy instance is:

```text
B = F_17
F = F_17^2 = F_17[t] / (t^2 + t + 1)
n = 8
k = 4
errors = 3
```

The residue-line fixture is:

```text
beta = (0, 1) in F \ B
f(x) = 1 / (x - beta)
g(x) = x^4
z* = (0, 1) in F \ B
S = {0, 1, 4, 5, 7}
```

The fixture `canonical-residue-witness.json` records evaluations of `f, g`, the
slope `z*`, an agreement set `S`, and a degree-`<k` codeword `c` such that
`h = f + z* g` agrees with `c` on `S`, while neither `f|S` nor `g|S` lies on a
degree-`<k` codeword. This is a genuine same-set MCA failure with an
extension-valued slope.

The denominator structure is spread across the whole domain: on `D`, where
`x^8 = 1`,

```text
1 / (x - beta) = P_beta(x) / (1 - beta^8),
```

so the residue word is represented by a degree-7 polynomial with genuinely
extension-valued coefficients. This is structurally different from a localized
coordinate perturbation.

Run the verifier:

```bash
python3 experimental/f1-extension-witness/verify_ext_witness.py
```

Expected output:

```text
OK canonical witness
OK F\B bad-slope recount: 51
```

The verifier is intentionally standalone: it uses only the Python standard
library and local finite-field/interpolation code, not the external
`mca-frontier` engine.

## Scope and caveats

This certificate demonstrates **toy-scale existence** of a genuinely
extension-valued degree-1 residue-line same-set MCA-bad line. It does **not**
prove a deployed-parameter cap certificate, nor does it establish universality
across rates, extension degrees, or larger smooth domains.

The source certificate engine and larger 600-trial search live in:

```text
https://github.com/latifkasuli/mca
commit 62c54c017bb2c6ad987c0fab3ef2726697297329
residue-layer commit 73f0beb4d2cda0b5a70599e532fbddbb6fbdd889
```

Next checks:

1. Determine whether the degree-1 residue-line mechanism can be lifted from
   this toy scale to the quantitative Paper D parameter regimes.
2. Search for richer companion directions `g` that reach fixed sub-capacity
   gaps, not only the near-capacity `capacity - 1/n` onset.
3. Repeat controlled sweeps for rates `1/4`, `1/8`, cubic extensions, and
   larger smooth domains with bounded/reproducible scripts.
