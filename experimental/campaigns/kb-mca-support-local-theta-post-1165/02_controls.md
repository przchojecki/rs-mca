# Control Zoo

| Control ID | Object | Preserved structure | Target behavior | Mechanism behavior | Status |
|---|---|---|---|---|---|
| C-001 | PR #1165 GF(1009) fixture | exact supports, global separation | old compiler fails | 31 > 23 | passed parent |
| C-002 | smooth GF(257) fixture | full multiplicative domain, exact supports | old fails; repaired accepts | 87 > 8 and 87 <= 759 | passed Python/Sage/Wolfram |
| C-003 | endpoint profiles | 10,716 legal small integer rows | closed formula equals profile maximum | exact equality | passed |
| C-004 | Koala theta boundary | exact big integers | theta and theta-1 straddle budget | 1/13/388/12050 | passed |
| C-005 | shortened-code boundary | ranks 1--14 | rank 9 fits, rank 10 fails at theta 1 | exact floors | passed |
| C-006 | M31 stress row | ranks 1--4 | thresholds exact and predecessors fail | 1/16/237/7118 | passed |
| C-007 | gauge inverse | GF(257) exact errors/supports | rank drops one and inverse restores record | exact | passed Sage |
| C-008 | hostile manifest mutations | units, hashes, owners, bounds | every mutation rejected | 32/32 caught | passed |
