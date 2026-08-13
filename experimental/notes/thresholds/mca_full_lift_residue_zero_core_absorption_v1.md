# MCA full-lift residue-zero core absorption v1

## Status

PROVED / EXACT FINITE CALIBRATION / SUPPORT PAYMENT.

## Statement and proof mechanism

At Mersenne-31 `e=98232`, suppose the selected family is unsafe. The
residue-zero direction router forces at least `343071` slopes on one affine
codeword line and a total common agreement core of size at least
`67452=m-2`.

The line direction is a nonzero degree-`<6` codeword. Outside the gauged
direction support, every common-core coordinate is one of its at most five
zeros. Thus at least `67447` core coordinates lie inside the direction
support.

For any assigned explanation of outside deficit `h`, ownership supplies at
least `h` inside agreements. If

```text
h>=98232-67447+6=30791,
```

those inside agreements meet the line's inside core in at least six
coordinates. Two top anchors and restriction injectivity put the explanation
on the same affine line, at its actual slope parameter. All such slopes are
therefore charged once by `N-m+1=981129`.

The remaining assigned explanations have deficit at most `30790`, hence
outside agreement at least `36664`. The ordinary punctured Johnson cap is

```text
floor(950350*(36664-5)/(36664^2-950350*5))=26.
```

Using the deliberately crude owner cap `e` on those explanations gives

```text
|Z|<=98232*26+981129=3535161<16777215.
```

This contradicts unsafety, with exact margin `13242054`.

## Consequence and nonclaims

Mersenne-31 full-lift support `e=98232` is safe. The residual interval is
now `98233<=e<=1044241`. This does not pay `e=98233`, close the deployed
row, or provide an adjacent unsafe certificate.

## Replay

```bash
python3 experimental/verify_mca_full_lift_residue_zero_core_absorption_v1.py
python3 -O experimental/verify_mca_full_lift_residue_zero_core_absorption_v1.py
python3 experimental/audit_mca_full_lift_residue_zero_core_absorption_v1.py
```
