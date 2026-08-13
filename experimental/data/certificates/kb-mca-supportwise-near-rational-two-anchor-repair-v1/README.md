# Replay contract

Run from the repository root:

```text
python3 -B experimental/scripts/verify_kb_mca_supportwise_near_rational_two_anchor_repair_v1.py --check --tamper-selftest
python3 -O -B experimental/scripts/verify_kb_mca_supportwise_near_rational_two_anchor_repair_v1.py --check --tamper-selftest
/usr/local/bin/sage experimental/scripts/verify_kb_mca_supportwise_near_rational_two_anchor_repair_v1.sage
~/math_code/.venv/bin/python experimental/scripts/verify_kb_mca_supportwise_near_rational_two_anchor_repair_v1_flint.py
```

The JSON schema is structural preflight only.  The primary verifier checks
pinned source blobs, recursively type-exact nested semantics, exact deployed
arithmetic and counterexample parameters/guards, the literal theorem contract,
packet hashes, and hostile mutations.  It also exhausts the syndrome-normalized
toy row `(q,n,K,m)=(7,6,3,4)`: all `7^6=117649` syndrome pairs and all seven
finite slopes are checked, and the largest near-rational support-wise bad set
has size exactly `2=2w`.

The Sage replay independently reconstructs the toy Reed--Solomon parity-check
geometry and checks the deployed integer guards, together with a literal toy
common-support example.  The FLINT replay checks deployed integers and an exact
degree-eight polynomial illustration of root-count sharpness.  The Wolfram file
is a stateless independent arithmetic and identity sanity replay for
`wolframscript` or the Wolfram cloud.

Passing these checks proves the finite identities and exhaustive toy control.
The general theorem is the argument in the note and repaired TeX source; no
finite computation substitutes for that proof.
