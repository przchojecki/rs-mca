# X-10 Consumer Tolerance Ladder

- **DAG node:** `anchored_nontoral_pte_bound`.
- **Task:** consumer tolerance ladder for the X-10 estimate.
- **Status:** arithmetic packet; exact verifier green.
- **Verifier:** `experimental/scripts/verify_x10_consumer_tolerance_ladder.py`.
- **Certificate:**
  `experimental/data/certificates/x10-consumer-tolerance-ladder/x10_consumer_tolerance_ladder.json`.

## Critical-path role

This packet records the tolerance of the conditional prize proof path to the
terminal active-core/PTE estimate.  Before W4, local U1/B consumers forced the
near-linear anchored target `A_h^nt <= h n`.  After W4, the two hard consumers
share one final post-strip row-wise split-pair column, so the clean-rate
compiler can consume the weaker but correctly denominated target

```text
# uncharged split pairs <= n^3 per row.
```

This ladder is therefore metadata for the terminal conjecture: it says which
exponent forms are sufficient for which consumers, and it prevents mixing a
core-only estimate with an unpaid polynomial tail multiplier.

## Normalization

All exponents in this packet use the normalized form

```text
A_h^nt <= h n^alpha.
```

The proved orbit conversion sends this to

```text
# uncharged split pairs <= (n/h) A_h^nt <= n^(alpha+1).
```

Thus the stated X-10 target `A_h^nt <= h n` is `alpha = 1`.
An unnormalized statement such as `A_h^nt <= n polylog n` must be compared
against the allowed `h` envelope; it is target-strength only if the factor
`polylog(n)/h` is controlled over the relevant `h` range.

## Ladder

```text
consumer                         budget consumed          max alpha   n^1.5?   n^(2-delta)?
------------------------------------------------------------------------------------------------
A -> U1 split-pair budget        n^2 split pairs          1           no       only delta >= 1
A -> compiler room only          QA22/QA25 row room       2 safe      yes      yes for delta >= 0
B exit 3                         n^2 band trades          1           no       only delta >= 1
A1 active shadow, local          n^2 active mass          2           yes      yes for delta >= 0
A2 active shadow, local          n^2 depth-active mass    2           yes      yes for delta >= 0
tails/defect wrapper             n^2 after orbit          alpha+lambda <= 1
```

The tails row is the weakest rung.  If the defect/tail wrapper costs a
polynomial factor `n^lambda`, then the X-10 exponent must save the same amount:

```text
alpha + lambda <= 1.
```

In particular, at the exact target `alpha = 1`, no polynomial defect loss is
available; only constant or genuinely subpolynomial losses can be harmless, and
their constants still have to be tracked.

## Exact Row-Room Check

The verifier reads the landed QA.22 and QA.25 certificates and computes the
remaining integer room

```text
B* - repaired_budget_total.
```

For a hypothetical direct compiler column `n^(alpha+1)`, all six rows tolerate
`alpha = 2` exactly.  The limiting rows are the prize rows:

```text
row          min direct compiler alpha_max
prize 1/4    2.0925011911751605
prize 1/8    2.092501191439833
prize 1/16   2.092501191439831
```

So the global arithmetic has room for a much weaker direct compiler column.  In
the pre-W4 proof stack, however, the local U1 and B reductions still needed the
orbit-converted `n^2` bound, hence `alpha <= 1`.

## W4 Addendum

The W4 direct-column packet rewires the two hard consumption points:

```text
U1 primitive star/PTE column
B exit 3 primitive moment/PTE residue
```

Both now consume the same final row-wise post-strip residue column directly in
the compiler.  Therefore the strict anchored target

```text
A_h^nt <= h n
```

is no longer the weakest sufficient campaign target.  The rewired sufficient
form is the L3 terminal rung

```text
# uncharged split pairs <= n^3 per row,
```

provided the bound is delivered in final post-strip split-pair currency.  A
core-only bound with an unpaid polynomial tail multiplier is still not accepted.

## Verdict

Before W4, the weakest sufficient rung for the local U1/B statements was the
near-linear anchored estimate:

```text
A_h^nt <= h n
```

or a version with only losses that are explicitly absorbed in the `h` envelope
and in the exact constants.  After W4, the compiler can instead consume one
direct `n^3` split-pair column, which is the target now recorded in
`active_core_count_bound`.

## Verification

Run:

```bash
python3 experimental/scripts/verify_x10_consumer_tolerance_ladder.py
```

To refresh the certificate:

```bash
python3 experimental/scripts/verify_x10_consumer_tolerance_ladder.py --write-certificate
```

Current replay: **24 PASS, 0 FAIL**.
