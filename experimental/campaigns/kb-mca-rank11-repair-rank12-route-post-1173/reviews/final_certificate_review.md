# Final certificate and custody review

Review date: 2026-08-20

Scope: certificate-to-claim matching, exact-source custody, executable replay,
packet inventory, build hygiene, and release wording.  This review does not
duplicate the independent proof-mathematics review.

## Durable pre-seal verdict

**PASS TO FREEZE AND GENERATE THE RELEASE MANIFEST.**

This is deliberately a pre-seal verdict.  It records that the current
unsealed payload is internally consistent and may be frozen; it does not say
that `manifest.json` already exists or has passed.  The final release verdict
requires the no-edit post-seal replay listed below.

The previous certificate failure is repaired.  The packet now:

- replaces the false truncated-margin recurrence with the raw-low theorem;
- withdraws the former rank-twelve descendant and endpoint claims;
- contains the complete shortening/span theorem rather than citing the
  unavailable `460e3c...` adapter;
- binds the exact external PR #1160 near-rational dependency by commit, Git
  blobs, and SHA-256 values;
- includes the final mathematics, certificate, and publication review files
  and the GF(11) regression in its packet inventory;
- checks all load-bearing source labels fail-closed; and
- presents the manifest check as a future release gate, not a completed fact.

## Payload and ancestry

- Working tree:
  `rs-mca-kb-rank11-repair-rank12-route-final`.
- Committed head beneath the live release patch:
  `9c5b536cf55a15e1139a80fac22f0024bf1cff63`.
- Exact declared stack parent:
  `2788d5ec3fb4b1d6f9c43a58a86ec2381e5f6804` (PR #1173 head).
- The declared parent is an ancestor, and the 22 committed packet commits
  after it are linear with no merge commit.
- Exact load-bearing source parent PR #1168 commit
  `6a5dcdae1591fc7f044eda6a942bfe178521a48c` is contained in the declared
  parent.

## Current theorem and claim boundary

The current result payload, active source, contract, claim registry, campaign
metadata, threshold note, coordination summaries, and PR wording agree on the
following boundary:

- uniform rank-one cap: `4,070,947`;
- rank-eleven required unsafe load: `248,706,399,341,288,370`;
- available post-near load: `274,980,728,111,260,144`;
- conditional rank-eleven slack: `26,274,328,769,971,774`;
- rank-twelve best single-cutoff requirement:
  `546,519,697,764,383,119` at `T=67,472`;
- rank-twelve single-cutoff shortfall: `271,538,969,653,122,975`.

The result claims rank eleven paid only after the separately pinned #1160
near-rational deletion.  It claims only that the repaired single-threshold
method is insufficient at rank twelve.  It does not claim a rank-twelve
descendant, route, owner, or payment.  Active-v4 ledger movement remains zero,
the complete chronology is not regenerated, and KoalaBear remains open.

The old `8,681,730` descendant and `279,911` endpoint figures occur only in
explicit withdrawal statements or clearly marked superseded-review
provenance.  The prior certificate, mathematics, literature, and Wolfram
files carry supersession/context banners and are not presented as current
release reviews.

## Exact executable replay

The following passed against the current live payload:

1. Primary exact verifier in normal mode:

   ```text
   KB_MCA_RANK11_REPAIR_RANK12_ROUTE_PASS
   rank1_cap=4070947
   rank11_slack=26274328769971774
   rank12_shortfall=271538969653122975
   controls=2234476
   ```

2. Primary verifier under `python3 -O`, with the identical sentinel and
   totals.  Its load-bearing checks use a custom fail-closed `require`
   function and survive optimization.
3. Hostile mutation suite: `8/8` rejected.
4. Independent product/recurrence audit:

   ```text
   KB_MCA_RANK11_REPAIR_RANK12_ROUTE_AUDIT_PASS
   uniform_rank_one=4070947
   rank11_required=248706399341288370
   rank11_slack=26274328769971774
   rank12_method_shortfall=271538969653122975
   ```

5. Sage GF(11) raw-versus-truncated regression:

   ```text
   KB_MCA_GF11_TRUNCATED_MARGIN_COUNTEREXAMPLE_PASS
   post_near_distance=3 raw=4 truncated=3 core=2
   ```

6. `py_compile` for the primary verifier, independent auditor, and manifest
   verifier, with bytecode directed outside the repository.
7. Frontier campaign structural audit with `--require-actionable`: PASS with
   6 ideas, 8 claims, 20 status rows, and 5 dependencies.
8. Both working-tree and complete post-parent `git diff --check`: PASS.

The primary verifier exactly reproduces `result.json`.  Its observed hashes
on this pre-seal payload are:

- raw result SHA-256:
  `89a6700b5c0fe3a7f6c504aa5ccb09716cbea4a9b5a8e03bb017eb081e4aa700`;
- canonical compact-JSON payload SHA-256:
  `f811fe07cfc3e98a9ecd4c74d4771f6d3c5f7380dead781f03e14b86b8c38752`.

## External PR #1160 custody and replay

The exact imported dependency commit
`c5f4ea7a0c78828c901ae5f3428894a8b2e2806b` is present locally.  The three
embedded pins match that commit byte-for-byte:

| artifact | Git blob | SHA-256 |
|---|---|---|
| threshold note | `12bc4a0f06189829a9490928e4855d1aa958f940` | `7e75d67420f4ed37add3b4f6ea3aa45e043a782a6396f328b1e34ce659938989` |
| verifier | `3b4533b53e947466de55262e3577108f125738c0` | `5d284cb0f857f2ff7c0797e911a2047009d6883d54f9d0df0a682627c09b5a35` |
| manifest | `d7442684309e51487a139979332a41c754650609` | `1854bc865a88d148f1a04676dcd566daf8fa7d50d1f16a5c105d9bbee69bae3c` |

The exact #1160 verifier was replayed from an isolated snapshot of that
commit.  It checked the deployed `2w=134944` charge, the actual
`67,472`-slope old-bound falsifier, all `117,649` GF(7) toy syndrome pairs,
the exact toy maximum `2`, and rejected `34` hostile mutations.  Result:
`PASS`.

The dependency remains external rather than ancestral.  The PR wording
correctly says that eventual integration requires both exact #1160 and #1173
dependencies, or a manual integration commit containing their bound
artifacts.

## Packet inventory and manifest semantics

`PACKET_FILES` currently has 29 unique entries.  Every path exists.  After
excluding the deliberately not-yet-generated self-referential
`manifest.json`, that set is exactly the complete tracked-plus-untracked delta
from the declared parent: no missing path, duplicate, or unlisted packet path
was found.

The inventory includes:

- all three final review files;
- `07_review_status.csv`;
- the GF(11) `.sage` source;
- the active TeX source and label-only integration map;
- all campaign, proof, coordination, certificate, and verifier files.

The manifest generator binds the raw and canonical result hashes, exact
claims, parent and superseded-candidate pins, imported #1160 dependency pins,
active-source hash, and path/length/SHA-256 of all 29 enumerated files.

All six load-bearing labels occur exactly once in the active source, and
`build_manifest()` rejects any other count:

- `thm:mca-raw-low-heavy-core-shortening`;
- `thm:mca-uniform-rank-one-weighted-line`;
- `cor:mca-rank-eleven-repaired`;
- `thm:mca-dense-core-pair-type`;
- `prop:mca-rank-twelve-single-threshold-wall`;
- `rem:mca-rank-eleven-repair-scope`.

The source-integration fragment is only a label map and contains no duplicate
theorem body.

## Full source build

The complete `experimental/grande_finale.tex` source compiled successfully
with TeX Live/`latexmk` into an isolated `/tmp` directory.  The build produced
a 125-page PDF, 1,140,196 bytes.  Its log contains no overfull box, undefined
reference, or multiply-defined label warning.  Remaining underfull-box
messages predate and lie outside this packet's substantive source block.

## Exact remaining final-seal procedure

No mathematical or certificate-content repair remains.  The maintainer must
perform the following custody steps in order:

1. Register the final mathematics, certificate, and publication reviews in
   `06_review_registry.csv`, which currently contains only its header.  Update
   the applicable `07_review_status.csv` rows conservatively; do not promote
   the external/specialist axis beyond evidence actually obtained.  Re-run
   the campaign audit and confirm that the final reviews are counted.
2. Remove the generated ignored file
   `controls/gf11_truncated_margin_counterexample.sage.py` and confirm no
   packet-local `__pycache__`, `.pyc`, or generated TeX file remains.
3. Freeze every packet-bound file.  Recompute the delta-versus-`PACKET_FILES`
   comparison, excluding only `manifest.json` itself, and require exact set
   equality.
4. Run the manifest verifier with `--write` once.  Make no packet-bound edit
   afterward.
5. Run the normal manifest verifier and require the exact PASS sentinel, file
   count, and canonical payload hash.
6. Request the promised no-edit independent replay of: primary normal and
   optimized modes, 8/8 mutations, independent audit, Sage GF(11), exact
   #1160 pin/hash/verifier checks, `py_compile`, campaign audit, both diff
   checks, manifest verification, source-label counts, clean generated-file
   scan, and the isolated full TeX build.
7. Only after that replay passes should the packet be committed, pushed, and
   opened as a draft stacked successor.  It must remain draft while #1160 and
   #1173 are unresolved dependencies.

This memo must not be edited after the manifest is generated.  A later
no-edit replay may cite it and the sealed manifest, but changing this file
would correctly invalidate the seal.

**Certificate status: PASS TO SEAL; FINAL SEALED REPLAY PENDING.**
