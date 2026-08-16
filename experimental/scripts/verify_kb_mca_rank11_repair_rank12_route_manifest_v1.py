#!/usr/bin/env python3
"""Manifest verifier for the rank-11 repair / rank-12 route packet."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "experimental/data/certificates/kb-mca-rank11-repair-rank12-route-v1/manifest.json"


def main() -> None:
    manifest = json.loads(MANIFEST.read_text())
    assert manifest["schema"] == "kb-mca-rank11-repair-rank12-route-manifest-v1"
    assert manifest["parent"] == "2788d5ec3fb4b1d6f9c43a58a86ec2381e5f6804"
    assert manifest["supersedes_unsubmitted_candidate"] == "d01c546f4dca70e256c18c142873821b3bb48ab5"

    result_path = ROOT / manifest["result"]
    result_bytes = result_path.read_bytes()
    assert hashlib.sha256(result_bytes).hexdigest() == manifest["result_sha256"]
    result = json.loads(result_bytes)
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    assert hashlib.sha256(canonical).hexdigest() == manifest["canonical_payload_sha256"]
    assert manifest["claims"] == result["claims"]

    seen: set[str] = set()
    for item in manifest["files"]:
        path = item["path"]
        assert path not in seen
        seen.add(path)
        data = (ROOT / path).read_bytes()
        assert len(data) == item["bytes"]
        assert hashlib.sha256(data).hexdigest() == item["sha256"]

    print(
        "KB_MCA_RANK11_REPAIR_RANK12_ROUTE_MANIFEST_PASS "
        f"files={len(seen)} payload={manifest['canonical_payload_sha256']}"
    )


if __name__ == "__main__":
    main()
