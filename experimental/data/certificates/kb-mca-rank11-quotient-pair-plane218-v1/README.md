# KoalaBear quotient-pair plane-218 certificate

This packet verifies a conditional finite split-pencil route cut.  Its exact
source interface is part of `contract.json`; the packet does not claim that
the current rank-eleven route already reaches that interface.
The endpoint extension also verifies an exact router under the additional
hypothesis that the residual direction pencil is pure-power.

Replay from the repository root:

```bash
python3 experimental/scripts/verify_kb_mca_rank11_quotient_pair_plane218_v1.py
python3 -O experimental/scripts/verify_kb_mca_rank11_quotient_pair_plane218_v1.py
python3 experimental/scripts/verify_kb_mca_rank11_quotient_pair_plane218_v1.py --tamper-selftest
python3 experimental/scripts/verify_kb_mca_rank11_quotient_pair_plane218_v1_independent.py
python3 -O experimental/scripts/verify_kb_mca_rank11_quotient_pair_plane218_v1_independent.py
```

Optional source replay checks the frozen proof-node trees and source files:

```bash
python3 experimental/scripts/verify_kb_mca_rank11_quotient_pair_plane218_v1.py \
  --source-root /path/to/rs-mca-prize-dag
```

No Sage, CAS, external binary, network call, or large computation is used.
