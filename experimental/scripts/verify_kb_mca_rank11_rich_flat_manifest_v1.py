#!/usr/bin/env python3
"""Verify the rich-flat packet's frozen file hashes and canonical payload."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "experimental/data/certificates/kb-mca-rank11-rich-flat-router-v1/manifest.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    for entry in data["files"]:
        path = ROOT / entry["path"]
        assert path.is_file(), entry["path"]
        assert path.stat().st_size == entry["bytes"], entry["path"]
        assert sha256(path) == entry["sha256"], entry["path"]
    result = ROOT / "experimental/data/certificates/kb-mca-rank11-rich-flat-router-v1/result.json"
    assert sha256(result) == data["result_sha256"]
    payload = {key: value for key, value in data.items() if key != "canonical_payload_sha256"}
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    assert hashlib.sha256(canonical).hexdigest() == data["canonical_payload_sha256"]
    print(
        "KB_MCA_RANK11_RICH_FLAT_MANIFEST_PASS "
        f"files={len(data['files'])} payload={data['canonical_payload_sha256']}"
    )


if __name__ == "__main__":
    main()
