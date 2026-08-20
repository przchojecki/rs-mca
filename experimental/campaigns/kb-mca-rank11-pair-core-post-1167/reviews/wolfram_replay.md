# Wolfram exact replay

Date: 2026-08-13

The Wolfram plugin independently evaluated the KoalaBear rank-eleven resource,
pair loads, slope floors, deficiency walls, and adjacent budget arithmetic.
It returned

```text
{106618568137036225644,
 {{6486,743449148,114624,8},
  {1795,360132809,200632,4}},
 84494997}
```

The entries are respectively `C_10`; the two tuples
`{tau, fixed-pair weight, forced slope count, maximal compatible deficiency}`;
and the slack obtained if every pair at `tau=6486` has weight at most one
below the forced terminal.  This is an independent arithmetic replay, not a
proof of the source-bound incidence theorem.
