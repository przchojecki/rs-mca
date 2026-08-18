# KoalaBear quotient-pair plane-218 certificate

This packet verifies a conditional finite split-pencil route cut.  Its exact
source interface is part of `contract.json`; the packet does not claim that
the current rank-eleven route already reaches that interface.
The endpoint extension also verifies an exact router under the additional
hypothesis that the residual direction pencil is pure-power.
The dimension-three extension verifies the rich-plane recurrence sharpening
from common-core floor 407,831 to 452,813 under the same source interface.
It also verifies the exact balanced pair-overlap moment floor `k'=4836`,
including the adjacent deficit/slack pair.  Numerical overlap with the
separate shared-core payment threshold is explicitly not treated as a
source-interface transport.

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
