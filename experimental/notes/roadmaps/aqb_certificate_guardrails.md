# AQB Certificate Guardrails

Status: PROVED certificate-interface guardrails; the AQB family payload remains
open.

This note vendors the proved leaves around the smooth-RS prize DAG's averaged
quotient-box (AQB) route.  It does not claim the `c=2` AQB family exists.
Instead, it pins the finite arithmetic and the certificate semantics that any
future AQB manifest must satisfy.

Replay:

```bash
python3 experimental/scripts/verify_aqb_certificate_guardrails.py
```

## Constants

The AQB interface is keyed to

```text
sigma* = 8,592,912,738
N      = 2^40
d      = 4,296,456,369
m      = 2^39 + d
Q      <= 256
```

The finite deficit is

```text
B_I(Q) = d Q - 40 - log2 binom(N,m).
```

Since `d > 0`, this is maximized at `Q = 256`.  Robbins-Stirling bounds give
the certified interval

```text
B_I(256) =
429645546.773407953684577335517...  +/- < 1e-24 bits.
```

Therefore a certified shared AQB gain of

```text
429,645,547 bits
```

clears the deficit by more than `0.226` bits.  The same calculation gives the
unamplified equality threshold

```text
Qcrit = 255.900000020976959686266378250...
```

which explains why the route is a generated-field normalization issue, not a
challenge-field bookkeeping shortcut.

## Average-To-Member Transfer

For any finite nonempty AQB family, if the family-average contribution after
certified shared entropy gain exceeds the MCA/list trigger, then at least one
member exceeds the trigger.  This is just the finite averaging principle:

```text
average(values) > T  =>  exists member with value > T.
```

The replay enumerates small rational test families as a sanity check of the
strict-inequality convention.

## Certificate Schema

A `c=2` AQB family certificate at `sigma*` must provide:

- a nonempty finite member set;
- a map from every member into the same `c=2` quotient-box geometry;
- shared quotient/fiber data;
- reusable box-charge data; and
- a transfer witness from every member to the list/MCA witness consumed by the
  averaging argument.

If those fields verify, the certificate supplies the averaged-family predicate.

## Entropy Ledger Rule

An AQB entropy ledger is accepted only when it supplies certified lower bounds
for positive shared-family entropy terms and certified upper bounds for every
charged box, overlap, multiplicity, and quotient/fiber normalization cost.

The monotone rule is:

```text
sum positive_lower_bounds - sum cost_upper_bounds >= 429,645,547
  => true net shared entropy gain >= 429,645,547.
```

The replay checks the ledger acceptance logic, missing-field rejection, and a
coupled manifest whose ledger is keyed to the same members and quotient cell as
the family certificate.

## Nonclaim

This packet does not supply the actual coupled AQB manifest.  A future manifest
must still provide the concrete member parametrization, shared quotient/fiber
data, reusable charge data, transfer maps, and exact or interval-certified
ledger entries clearing the `429,645,547`-bit threshold.

For the current frontiers-paper program, AQB is therefore best treated as a
certificate grammar and finite-arithmetic guardrail: it makes the conditional
input checkable if a candidate averaged quotient-box family is proposed.
