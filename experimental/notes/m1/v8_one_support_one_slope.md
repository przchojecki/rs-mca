# V8 One-Support-One-Slope Ledger

- **Status:** PROVED / linear-pencil ledger.
- **DAG node:** `v8_ledger`.
- **Certificate:** `experimental/data/certificates/v8-ledger/v8_ledger.json`.
- **Verifier:** `python3 experimental/scripts/verify_v8_ledger_packet.py --check experimental/data/certificates/v8-ledger/v8_ledger.json`.

This packet records the one-support-one-slope rule used by the MCA counting
frame.

## Claim

Fix a locator/support and pass to its quotient syndrome coordinates. For a
received pair `(u,v)`, write the fixed-locator obstruction as

```text
A + z B = 0
```

in a finite-dimensional vector space over the line field.

If `B != 0`, there is at most one finite slope `z` solving this vector
equation. If `B = 0`, either there are no finite slopes (`A != 0`) or all
slopes solve it (`A = 0`), the all-slope containment/degenerate case handled
by the noncontainment ledger.

Thus each nondegenerate fixed support/locator contributes at most one finite
slope.

## DAG Use

`counting_frame` consumes this packet to turn the finite divisor set into a
finite slope ledger: after degeneracies are removed, counting locators also
counts slopes.

## Non-Claims

- This packet does not count how many locators occur.
- This packet does not remove the all-slope degeneracy.
- This packet does not classify the locator as paid or unpaid.
- This packet does not edit Papers A-D.
