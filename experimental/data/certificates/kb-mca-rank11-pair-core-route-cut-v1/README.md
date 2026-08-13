# KoalaBear rank-eleven pair/core route-cut certificate

Exact dependency: PR #1167 head
`491ccdf53d54846f5a013b808960645275c64ed3`.

This certificate binds the nonuniform support-margin theorem, the exact
fixed-pair concentration terminals, and the two core-deficiency method
ceilings.  It explicitly records that rank eleven is unpaid and that active
v4 ledger movement is zero.

Replay from the repository root:

```bash
python3 experimental/scripts/verify_kb_mca_rank11_pair_core_route_cut_v1.py
python3 -O experimental/scripts/verify_kb_mca_rank11_pair_core_route_cut_v1.py
python3 experimental/scripts/verify_kb_mca_rank11_pair_core_route_cut_v1.py --tamper-selftest
HOME=/tmp /usr/local/bin/sage experimental/scripts/verify_kb_mca_rank11_pair_core_route_cut_v1.sage
python3 /Users/scott/.codex/skills/pursue-frontier-math/scripts/audit_campaign.py \
  experimental/campaigns/kb-mca-rank11-pair-core-post-1167 --require-actionable
```

The source document must also compile:

```bash
python3 /Users/scott/.codex/plugins/cache/openai-bundled/latex/0.2.4/scripts/compile_latex.py \
  experimental/grande_finale.tex --compiler texlive \
  --output-directory /tmp/kb-rank11-pair-core-tex --json
```

The canonical manifest is generated only after packet files freeze:

```bash
python3 experimental/scripts/verify_kb_mca_rank11_pair_core_route_cut_v1.py --write
```

The GF(11) Sage control proves sharp fixed-pair parallelism.  The smaller
GF(7) campaign control independently falsifies distinct-neighbor promotion
at the smallest legal local parameters.  Neither toy is asserted to realize
KoalaBear affine error rank eleven.

The campaign's `scratch/scan_weighted_pair_core.py` is preserved as a
superseded discovery artifact.  It uses the weaker bipartite endpoint
factor-two normalization and is deliberately excluded from the packet.  The
release Python verifier is authoritative.  The campaign experiment is an
unsealed duplicate replay retained for research provenance.
