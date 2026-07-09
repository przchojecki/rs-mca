# B1 normalization bridge audit

**Data:** `experimental/data/asymptotic_b1_normalization_bridge.json`.
**Verifier:** `experimental/scripts/verify_asymptotic_b1_normalization_bridge.py`.
**Status:** AUDIT.  This does not promote `experimental/asymptotic_rs_mca.tex`
and does not audit the missing C9 moduli manuscript.

## Question

PR #433 flags B1 as a `FOUND-WEAKER` joint in the asymptotic RS-MCA proof note.
The paper's primitive leaf uses the actual image

```text
L = |im Phi|,    Nbar = M/L,
Gamma_r^image = L^-1 sum_s (|F_s| / Nbar)^r,
```

while the cited Grande Fourier-flat theorem is stated at ambient prefix-box
scale:

```text
max_xi |{M : Psi(M)=xi}| <= exp(o(N)) * A^-1 * M
```

with `A = |K|^R` or, in finite prefix toys, `A = p^w`.

The bridge has to say which denominator is intended when the Fourier/Sidon cell
is paid: image scale `L`, ambient scale `A`, or an explicit two-field convention
where the point field and the entropy/base alphabet are separated.

## Exact identities

For any finite prefix map with ambient box size `A`, actual image size `L`, and
fiber counts `F_s`,

```text
R_ambient(s) = (A/L) * R_image(s),
Gamma_r^ambient = (A/L)^(r-1) * Gamma_r^image.
```

The verifier checks these identities exactly on four smooth-subgroup toy rows.
It also checks the easy max-fiber direction:

```text
ambient max-fiber bound M/A  =>  image-normalized bound M/L
```

because `L <= A`.  Thus the B1 gap is **not** that an ambient max-fiber theorem
would be too weak.  The gap is the moment/Fourier payment convention: converting
image moments into ambient moments costs the factor `(A/L)^(r-1)`, and in the
single-field reading `A/L` need not be `exp(o(N))`.

## Toy rows

| row | `A/L` | `log2(A/L)` | `R_image(max)` | `R_ambient(max)` |
|---|---:|---:|---:|---:|
| `F17x_16_m8_w3` | 1.006556 | 0.009427 | 2.654779 | 2.672183 |
| `F17x_16_m8_w4_underfilled` | 6.613429 | 2.725399 | 1.962549 | 12.979176 |
| `mu20_F41_m10_w2` | 1.000000 | 0.000000 | 1.210099 | 1.210099 |
| `mu24_F97_m12_w2` | 1.000000 | 0.000000 | 1.224770 | 1.224770 |

The underfilled row is the useful warning: the same fiber distribution is mild
on image scale but large on ambient scale solely because most ambient prefix
points are not in the image.

## Single-field obstruction

The integrated fp-span note already points at the same problem.  If the same
growing field `K` both contains `T` and supplies the ambient denominator `K^R`,
with `R = kappa N` and `|T| = N`, then `|K| >= N` and `|Omega| <= 3^N` imply

```text
log2 |Omega| - R log2 |K|
    <= N log2 3 - kappa N log2 N
    = -Omega(N log N).
```

That is not an `o(N)` frontier normalization.  The verifier prints the bound for
`kappa=1/4` at `N=100,1000,10000,100000`; the per-`N` deficit tends downward.

## Repair options

This audit leaves three clean ways to repair B1:

1. **Two-field convention.**  Print that the point field grows to contain `T`,
   while the entropy denominator is a separate base alphabet `B` of fixed or
   controlled bit-size.  Then the ambient box in the Q theorem is `|B|^w`, not
   the locator field's `|K|^R`.
2. **Image-scale theorem.**  Restate the C9 Fourier/Sidon payment directly at
   image scale `L = |im Phi|`, avoiding ambient-box transfer.
3. **Explicit bridge hypothesis.**  When using ambient moments, print the needed
   hypothesis `A/L = exp(o(N))` in the frontier window.

The first option appears closest to the intended semantics of Grande's
base-alphabet ledger; the current `asymptotic_rs_mca.tex` text should say it
explicitly before the closed-ledger proof is promoted.

## Nonclaims

- This does not prove the asymptotic RS-MCA theorem.
- This does not address C9's missing moduli manuscript.
- This does not instantiate finite deployed adjacent rows.
- This does not decide which repair option the maintainer should choose.
