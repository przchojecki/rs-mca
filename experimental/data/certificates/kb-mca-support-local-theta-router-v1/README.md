# KoalaBear support-local theta router v1

Stacked on exact PR #1165 head
`b6d30ef4f5ff966665b7672e1780a637509873a4`, this packet sharpens its
global proper-subspace compiler with an exact selected-support margin and a
reversible error-rank gauge.

Its conditional direct KoalaBear result is:

- if a disjoint earlier stratum has size at most `2w=134944`, post-deletion
  affine error rank at most 9 is paid by `110390969172308040`, leaving slack
  `164589758939087047`;
- ranks 10, 11, and 12 either pay or emit an actual selected support with at
  most 12, 387, or 12049 direction exceptions;
- rank at least 13 remains explicit.

PR #1160 supplies the required `2w` deletion on its own stack.  This packet
does not insert either result into the still-open v4 S/A/E chronology and
moves no deployed ledger atom.

Replay:

```bash
# The packet pins PR #1160 as an external dependency.  Fetch its exact head
# explicitly because it is not an ancestor of the PR #1165 stack.
git fetch upstream pull/1160/head:refs/remotes/upstream/pr-1160
python3 experimental/scripts/verify_kb_mca_support_local_theta_router_v1.py --check
python3 -O experimental/scripts/verify_kb_mca_support_local_theta_router_v1.py --check
python3 experimental/scripts/verify_kb_mca_support_local_theta_router_v1.py --tamper-selftest
HOME=/tmp DOT_SAGE=/tmp TMPDIR=/tmp /usr/local/bin/sage experimental/scripts/verify_kb_mca_support_local_theta_router_v1.sage
/Users/scott/math_code/.venv/bin/python experimental/scripts/verify_kb_mca_support_local_theta_router_v1_flint.py
/Users/scott/math_code/scripts/wm.sh -file experimental/scripts/verify_kb_mca_support_local_theta_router_v1.wl | grep -F 'KB_MCA_SUPPORT_LOCAL_THETA_WOLFRAM_PASS'
```

The final pipe is intentional: the cloud wrapper can report a transport or
credit error with status zero, so absence of the exact PASS sentinel must
fail the replay.

Regenerate the canonical manifest only after intentional packet changes:

```bash
python3 experimental/scripts/verify_kb_mca_support_local_theta_router_v1.py --write
```
