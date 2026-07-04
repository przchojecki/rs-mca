# W4 Direct-Column Rewiring Certificate

This dependency certificate records the `n^3` direct-column arithmetic used by
`a_closure_assembly.md`.

It is consumed by:

```bash
python3 experimental/scripts/verify_a3_good_reduction.py
```

The A3 verifier checks that every row has one available `n^3` direct column
and that the remaining-room values in `w4_direct_column_rewiring.json` are
internally consistent.  The W4 packet itself is a consumer rewiring statement;
it does not prove the terminal primitive-residue estimate.
