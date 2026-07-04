# W4: Direct-column rewiring

- **DAG node:** `w4_direct_column_rewiring`.
- **Consumer nodes:** `u1_pullback_dichotomy`,
  `u1_beta_band_trade_reduction`, `anchored_nontoral_pte_bound`,
  `active_core_count_bound`.
- **Status:** PROVED consumer-rewiring packet.  The terminal residue estimate
  remains open.
- **Verifier:** `experimental/scripts/verify_w4_direct_column_rewiring.py`.
- **Certificate:**
  `experimental/data/certificates/w4-direct-column-rewiring/w4_direct_column_rewiring.json`.

## Statement

Assume the terminal primitive PTE residue is supplied in the compiler's
row-wise split-pair currency:

```text
R_PTE(row) <= n^3.
```

Here `R_PTE(row)` is the fully stripped row count: cyclic, dihedral,
boundary-zero-sum, W3 dictionary, moment/PTE pullback, and fixed-tail paid
classes have already been removed or charged elsewhere.

Then the two former hard consumers

```text
U1 primitive star/PTE column
B exit 3 primitive moment/PTE residue
```

consume `R_PTE` directly as one compiler column.  They no longer require the
orbit-converted local estimate

```text
A_h^nt <= h n.
```

Consequently, after this rewiring, the L3 target in `active_core_count_bound`

```text
# uncharged split pairs <= n^3 per row
```

is a sufficient terminal rung for those two consumers.

## Proof

The old route mixed two currencies.

First, X-10 anchors the primitive non-toral residue and proves the orbit
conversion

```text
# split pairs <= (n/h) A_h^nt.
```

If the U1 and B reductions insist on closing as local `n^2` theorems before
the compiler sees the residue, then one must prove

```text
A_h^nt <= h n.
```

That is the strict trophy inequality.  The latest toy data falsifies that
strict form at the `q ~ n^2` boundary under the cyclic-only classifier, and
the DAG now treats it as stronger than the campaign needs.

Second, the clean-rate compiler already prices row-wise charged columns.  The
QA.22 and QA.25 certificates compute the remaining exact integer room after
the staircase, tangent, boundary, and existing `16 n^3` reserve columns.  The
W4 verifier checks, row by row, that

```text
n^3 <= B* - repaired_budget_total.
```

It also checks the defensive stronger fact that two such columns fit.  Thus a
single terminal `n^3` split-pair column may be consumed directly.

For U1, the star-PTE normal form says the primitive post-dictionary survivors
are canonical PTE trades.  The X-10 reduction identifies their uncharged
row-wise supply with the anchored non-toral PTE residue after undoing the
anchor/orbit convention.  W4 changes only the place where this supply is
charged: instead of demanding a standalone `n^2` U1 theorem, every primitive
survivor is assigned to `R_PTE(row)`.

For B, the B-WRITEUP packet already proves exits 1 and 2 formally and names
exit 3 as exactly the primitive moment/PTE residue.  Therefore exit 3 is the
same row-wise column as the U1 primitive residue, not a second independent
family.  It is charged to `R_PTE(row)` as well.  The verifier records the two
consumer routes with one common `residue_column_id`; the row arithmetic would
still tolerate accidental two-column accounting, but the proof uses one.

No mathematical estimate is strengthened here.  The gain is purely
bookkeeping: the proof stack now consumes the terminal residue in the same
row-wise currency in which the compiler has exact budget room.

## Tail Currency

W4 does not accept a core-only estimate followed by an unpaid polynomial tail
multiplier.  A future terminal proof must deliver one of:

```text
1. a final post-strip row-wise split-pair bound R_PTE(row) <= n^3; or
2. a core bound plus separate paid-tail columns already priced by W3/QA-style
   certificates.
```

If neither is available, the remaining gap is:

```text
w4_tail_currency_residue
```

This caveat is the direct-column version of the old defect/tails warning in
`x10_consumer_tolerance_ladder.md`.

## Consequences

The h=3 cubic cap now meets the terminal L3 consumer requirement:

```text
h=3 anchored active pairs < n^3.
```

This does not close `active_core_count_bound`, because `h >= 4` remains open.
It does remove the artificial requirement that the final estimate be linear
in anchored currency.

The remaining terminal problem is therefore sharpened to:

```text
For h >= 4, prove the fully stripped row-wise primitive PTE residue is <= n^3,
or prove the stronger high-q vanishing form.
```

## Verification

Run:

```bash
python3 experimental/scripts/verify_w4_direct_column_rewiring.py
```

To refresh the certificate:

```bash
python3 experimental/scripts/verify_w4_direct_column_rewiring.py --write-certificate
```

Current replay: **31 PASS, 0 FAIL**.
