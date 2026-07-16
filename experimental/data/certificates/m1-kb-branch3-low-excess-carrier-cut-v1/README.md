# M1 KoalaBear branch-3 low-excess carrier cut v1

This directory contains the deterministic certificate for a conditional
global-carrier owner inside KoalaBear branch 3 at `A=1,116,048`.

For one retained slope set, select one actual noncontained exact-agreement
witness per slope.  If all selected actual nonzero error supports lie in one
global carrier with excess at most ten over the RS redundancy, the packet
gives a budget-fitting global distinct-slope cap.

The exact boundary is:

```text
B_10 =   78,289,526,705,722,101  fits
B_11 = 1,115,145,741,750,273,207  fails
```

The packet is fail-closed.  It does not supply an exhaustive deployed carrier,
does not charge multiple unrelated carriers by a maximum, and does not change
the current ledger.

Replay:

```bash
python3 experimental/scripts/verify_m1_kb_branch3_low_excess_carrier_cut_v1.py --check
python3 experimental/scripts/verify_m1_kb_branch3_low_excess_carrier_cut_v1.py --tamper-selftest
python3 experimental/scripts/verify_agreement_weighted_transverse_secant.py

python3 experimental/scripts/verify_m1_kb_branch2_rank_deep_owner_v1.py --check
python3 experimental/scripts/verify_m1_kb_branch2_rank_deep_owner_v1.py --tamper-selftest
```

No Sage or elimination replay is required: the new load-bearing computation is
an exact binomial-ratio and source-interface audit over Python big integers.
