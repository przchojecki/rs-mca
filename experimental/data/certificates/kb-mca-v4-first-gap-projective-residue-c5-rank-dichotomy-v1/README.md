# KoalaBear first-gap projective residue C5/rank dichotomy

This packet verifies the exact source-bound dichotomy at the first open
full-outside KoalaBear slack:

```text
one base-rational projective residue point, with global 2e exchange
or
a canonical reciprocal multiplier kernel of dimension at least three.
```

If a base-defined residue line has reciprocal kernel dimension two, the
translated source pair has a base-valued basis. The active pair-global C5
owner therefore removes the incoming residual. The rank-excess alternative
has an exact reciprocal rational normal form. For reciprocal dimension `r`,
the ratio is represented by coprime polynomials of degree
`d = e - r + 1`; every locator pair is therefore either an exact
low-degree root swap of size at most `d` or has exchange at least
`e + r - 1`.

Both rank excess and the resulting root-swap/large-exchange alternatives are
precursors only. This packet does not assign either alternative a slope
payment and makes no ledger movement.

Replay:

```bash
python3 experimental/scripts/verify_kb_mca_v4_first_gap_projective_residue_c5_rank_dichotomy_v1.py --check
python3 experimental/scripts/verify_kb_mca_v4_first_gap_projective_residue_c5_rank_dichotomy_v1.py --tamper-selftest
```

The finite controls exhaust all projective lines of
`P^2(F_9)` relative to `P^2(F_3)`, distinguish reciprocal kernel dimensions
two and three over `F_17`, and replay the reciprocal kernel on the 36 exact
source controls from the first-gap residue packet. They also exhaust 1,540
locator pairs at `(p,e,j)=(23,3,4)` and 21,945 locator pairs at
`(31,4,5)`, checking the rational normal form and every predicted exact
root swap.
