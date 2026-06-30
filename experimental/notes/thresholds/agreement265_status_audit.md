# Agreement-265 finite-slope status audit

**Status:** PROVED-CONSEQUENCE / AUDIT.

**Agent/model:** AllenGrahamHart / Codex.

**Date:** 2026-06-30.

This note records the finite-slope consequence of the already integrated
coset-packet lower-floor theorem for the old agreement-265 upper-bound target
in `towards-prize.md`.

The target

```text
LD_sw(C,265) <= 6
```

is false under the finite-slope support-wise convention used by the threshold
notes, where

```text
C = RS[F_17^32,H,256],        |H|=512.
```

The coset-packet theorem in
`experimental/notes/m1/m1_coset_packet_finite_slope_floors.md` proves

```text
LD_sw(C,a) >= binom(31,16) = 300540195
```

for every `a=265,...,271`, and also proves

```text
LD_sw(C,288) >= binom(16,9) = 11440.
```

Since

```text
floor(17^32 / 2^128) = 6,
```

any row with at least seven finite bad slopes is unsafe for the `2^-128`
finite-slope MCA gate. Thus the agreement-265 upper-bound target is not an
open finite-slope upper theorem in this convention; it is refuted by a proved
lower floor.

## Consequence for the finite row

The coset-packet lower floor gives more than six finite bad slopes at each
agreement from `265` through `288`. In particular, the current finite-slope
lower-bound evidence pushes the first possible safe agreement edge beyond
`288`:

```text
LD_sw(C,a) > 6        for every a <= 288
```

where the statement for `a<265` follows monotonically from the displayed
`a=265` row, and the statement for `265<=a<=288` is covered directly by the
coset-packet rows.

Therefore, if this finite-slope predicate is the intended object, the next
finite upper-bound target should not be `a=265`. The first agreement not ruled
out by the current coset-packet floor is

```text
a = 289.
```

Equivalently, the next threshold-pinning edge allowed by this lower-floor
package is at least

```text
288 / 289
```

in agreement coordinates.

## Non-claims

This note does not prove

```text
LD_sw(C,289) <= 6.
```

It also does not classify all bad finite slopes, does not give a projective
slope count, does not prove a protocol soundness statement, and does not change
the high-agreement `506/507` threshold package. It is only a status audit for
the older agreement-265 finite-slope upper-bound target.

## Verification

The companion verifier checks the exact integer arithmetic, reuses the
coset-packet certificate verifier, and confirms that all agreements
`265,...,288` have certified lower floors larger than the gate value `6`:

```sh
python3 experimental/scripts/verify_agreement265_status_audit.py
```
