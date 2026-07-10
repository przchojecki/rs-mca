#!/usr/bin/env python3
"""Independent checker for C9 reduction map.

checker route: re-read note for required PR refs and razor; verify chain statuses;
require all_pass and OPEN verdict.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify_c9_reduction_map as gen  # noqa: E402


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args(argv)
    root = gen.repo_root()
    path = root / gen.CERT
    if not path.is_file():
        print("RESULT: FAIL missing cert", file=sys.stderr)
        return 1
    cert = json.loads(path.read_text(encoding="utf-8"))
    note = (root / gen.NOTE).read_text(encoding="utf-8")

    prs = ["#575", "#577", "#579", "#581", "#582"]
    prs_ok = all(p in note for p in prs)
    razor_ok = "near-Sidon" in note and "exp-large" in note and "RAZOR" in note.upper()
    open_ok = cert.get("verdict") == "OPEN" and "OPEN" in note
    chain_ok = len(cert.get("chain", [])) == 7
    statuses = {c["step"]: c["status"] for c in cert.get("chain", [])}
    status_ok = (
        statuses.get(1) == "REDUCED"
        and statuses.get(3) == "PROVED-SPECIAL"
        and statuses.get(4) == "MEASURED-mechanism-fails"
        and statuses.get(6) == "OPEN"
    )

    ok = prs_ok and razor_ok and open_ok and chain_ok and status_ok and cert.get("all_pass")
    print(
        "route: note PR-ref scan + razor phrases + chain status table + OPEN verdict"
    )
    print(f"prs_ok={prs_ok} razor_ok={razor_ok} open_ok={open_ok} chain_ok={chain_ok}")
    print(f"payload_sha256: {cert.get('payload_sha256')}")
    print(f"verdict: {cert.get('verdict')}")
    if ok:
        print("RESULT: PASS")
        return 0
    print("RESULT: FAIL", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
