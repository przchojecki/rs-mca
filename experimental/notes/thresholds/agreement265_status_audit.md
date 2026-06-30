# Agreement-265 finite-slope status audit

**Status:** PROVED-CONSEQUENCE / AUDIT.

**Agent/model:** AllenGrahamHart / Codex.

**Date:** 2026-06-30.

This note records the finite-slope consequence of the already integrated
finite lower-floor packages for the old agreement-265 upper-bound target in
`towards-prize.md`.

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

Together with the random simple-pole entropy floor in
`experimental/notes/m1/m1_random_simple_pole_entropy_floor.md`, the current
explicit low-agreement mechanism coverage is:

```text
a = 257:     all 17^32 finite slopes are bad,
a = 258:     all 17^32 finite slopes are bad,
a = 259:     at least 17^32 - 68904 finite slopes are bad,
a = 260:     at least 33439260151101646297506087371119470 slopes,
a = 261..263 at least binom(63,32) slopes,
a = 264:     at least binom(64,33) slopes,
a = 265..271 at least binom(31,16) slopes,
a = 272:     at least binom(32,17) slopes,
a = 273..287 at least binom(15,8) slopes,
a = 288:     at least binom(16,9) slopes.
```

Since

```text
floor(17^32 / 2^128) = 6,
```

any row with at least seven finite bad slopes is unsafe for the `2^-128`
finite-slope MCA gate. Thus the agreement-265 upper-bound target is not an
open finite-slope upper theorem in this convention; it is refuted by a proved
lower floor.

There is also a stronger global status statement from the high-agreement
threshold package:

```text
LD_sw(C,506) = 7,
LD_sw(C,507) = 6.
```

By monotonicity, the `a=506` row already makes every `a<=506` unsafe, while
the promoted high-agreement theorem proves every `a>=507` safe. This note does
not reprove that threshold; it uses it to keep the agreement-265 status
ledger aligned with the current roadmap.

## Consequence for the finite row

The integrated low-agreement lower-floor packages give more than six finite
bad slopes at each agreement from `257` through `288`:

```text
LD_sw(C,a) > 6        for 257 <= a <= 288.
```

The first row not covered by these two low-agreement mechanism packages is
`a=289`.  This is a mechanism-coverage boundary only.  It is not the first row
not ruled out for the finite-slope predicate overall, because the
high-agreement threshold package already pins the global finite-slope edge at
`506/507`.

Therefore, if the finite-slope support-wise predicate is the intended object,
the old agreement-265 upper-bound work package should be treated as obsolete.
If a different sampler or predicate was intended, it should be restated
explicitly before any further agreement-265 upper-bound work is attempted.

## Non-claims

This note does not add a new proof of the high-agreement `506/507` threshold,
does not classify all bad finite slopes, does not give a projective slope
count, does not prove a protocol soundness statement, and does not change the
high-agreement threshold package. It is only a status audit for the older
agreement-265 finite-slope upper-bound target.

## Verification

The companion verifier checks the exact integer arithmetic, reuses the
random simple-pole, coset-packet, and high-agreement threshold verifiers.  It
confirms that all agreements `257,...,288` have certified low-agreement
mechanism floors larger than the gate value `6`, and that the high-agreement
package pins the global finite-slope threshold at `506/507`:

```sh
python3 experimental/scripts/verify_agreement265_status_audit.py
```
