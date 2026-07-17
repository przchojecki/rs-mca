#!/usr/bin/env python3
"""One-command replay for the dense-shell transfer-shape packet."""

import hashlib
import json
import subprocess
import sys
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve()
REPO_ROOT = SCRIPT_PATH.parents[2]
VERIFY = REPO_ROOT / "experimental/scripts/verify_dense_shell_transfer_shape_arb.py"
CLASS_VERIFY = REPO_ROOT / "experimental/scripts/verify_dense_shell_class_charges.py"
CERT_DIR = (
    REPO_ROOT
    / "experimental/data/certificates/dense-shell-transfer-shape"
)


def run(*arguments):
    command = [sys.executable, *map(str, arguments)]
    print("+", " ".join(command), flush=True)
    subprocess.run(command, cwd=REPO_ROOT, check=True)


def replay_hashes():
    manifest = CERT_DIR / "SHA256SUMS.txt"
    for line in manifest.read_text(encoding="utf-8").splitlines():
        expected, relative = line.split("  ", 1)
        path = REPO_ROOT / relative
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            raise SystemExit(f"artifact hash mismatch: {relative}")
    print("artifact hashes: PASS")


def main():
    run(VERIFY, "--check")
    run(VERIFY, "--tamper-selftest")
    run("-m", "py_compile", VERIFY, CLASS_VERIFY, SCRIPT_PATH)
    run(CLASS_VERIFY, "--deep")
    json.loads((CERT_DIR / "dense_shell_transfer_shape.json").read_text("utf-8"))
    json.loads((CERT_DIR / "consumer_contract.json").read_text("utf-8"))
    replay_hashes()
    print("dense-shell transfer-shape replay: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
