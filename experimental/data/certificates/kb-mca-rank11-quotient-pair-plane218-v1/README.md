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
When the source family is additionally the complete retained quotient-type
population carrying 255,011,043 records, the packet verifies `q<=3170`, an
80,446-record dense type, and the saturated `q=3170` endpoint.
That endpoint is further reduced to 339--358 rich planes, at least 217
saturated lines, and a global bank of 41,746--47,836 projective directions
with aggregate root saturation above 87.26 percent.
After charging at most 310 residual common-gcd roots, the primitive
three-space is further routed by projective image degree: image degree two
is exactly `span(A^2,AB,B^2)` for one rational map of degree 1,021--2,490,
while image degree at least three forces 597--633 distinct full evaluation
normals.

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
