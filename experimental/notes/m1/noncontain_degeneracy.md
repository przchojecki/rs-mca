# Noncontainment Degeneracy Packet

- **Status:** PROVED / degeneracy identification.
- **DAG node:** `noncontain_degeneracy`.
- **Certificate:** `experimental/data/certificates/noncontain-degeneracy/noncontain_degeneracy.json`.
- **Verifier:** `python3 experimental/scripts/verify_noncontain_degeneracy_packet.py --check experimental/data/certificates/noncontain-degeneracy/noncontain_degeneracy.json`.

This packet records the boundary between finite-slope locator accounting and
the all-slope containment degeneracy.

## Claim

For a fixed locator/support, write the induced pencil obstruction as

```text
A + z B = 0.
```

The all-slope case occurs exactly when

```text
A = 0 and B = 0.
```

In the residue-line language this is the containment/degenerate pencil case:
both endpoints already lie in the same contained kernel, so the fixed locator
does not represent a genuine finite-slope noncontainment event.

Every other case has either no finite slope or at most one finite slope, as
handled by the V8 one-support-one-slope ledger.

## DAG Use

`counting_frame` consumes this packet to remove all-slope containment before
using the one-support-one-slope ledger. It is also a guardrail for extension
and orbit-pole forcing arguments where contained pencils must not be counted
as finite slope events.

## Non-Claims

- This packet does not count noncontained finite slopes.
- This packet does not classify paid quotient, tangent, or extension strata.
- This packet does not prove the Paper B normal form.
- This packet does not edit Papers A-D.
