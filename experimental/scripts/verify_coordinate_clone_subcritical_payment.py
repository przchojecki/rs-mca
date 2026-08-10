#!/usr/bin/env python3
"""Replay finite seams for the coordinate-clone subcritical payment."""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
import sys
from pathlib import Path


CERT_REL = Path(
    "experimental/data/certificates/"
    "coordinate-clone-subcritical-payment-v1/certificate.json"
)
SCHEMA = "coordinate-clone-subcritical-payment-v1"
EXPECTED_SOURCE_PINS = {
    "experimental/grande_finale.tex": "6b21d6ea937a8a9f85fc7ade6032d73efd4c7222"
}
EXPECTED_THEOREMS = {"COORDINATE_CLONE_SUBCRITICAL_CLASS_PAYMENT"}
EXPECTED_NONCLAIMS = {
    "NO_IDENTICALLY_ZERO_OR_FIXED_COMPONENT_PAYMENT",
    "NO_LARGE_CLONE_COMPONENT_PAYMENT",
    "NO_CROSS_CELL_ALLOCATION",
    "NO_COMPLETE_EXCEPTION_ROUTING",
    "NO_ADJACENT_ROW_CLOSURE",
    "NO_OFFICIAL_SCORE_MOVEMENT",
}


class VerificationError(RuntimeError):
    pass


CHECKS = 0


def require(condition: bool, message: str) -> None:
    global CHECKS
    CHECKS += 1
    if not condition:
        raise VerificationError(message)


def git_blob_sha(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def verify_manifest(certificate_dir: Path) -> None:
    manifest = certificate_dir / "SHA256SUMS.txt"
    require(manifest.is_file(), "missing SHA256SUMS.txt")
    entries = {}
    for line in manifest.read_text(encoding="utf-8").splitlines():
        digest, relative = line.split("  ", 1)
        entries[relative] = digest
    require(
        set(entries)
        == {
            "README.md",
            "certificate.json",
            "recorded_output.txt",
            "../../../notes/m2/coordinate_clone_subcritical_payment.md",
            "../../../scripts/verify_coordinate_clone_subcritical_payment.py",
        },
        "manifest members",
    )
    for relative, expected in entries.items():
        path = (certificate_dir / relative).resolve()
        require(path.is_file(), f"missing manifest member: {relative}")
        require(
            hashlib.sha256(path.read_bytes()).hexdigest() == expected,
            f"manifest hash: {relative}",
        )


def curve_value(coeffs, gamma: int, tau: int, p: int) -> int:
    a, b, c, d = coeffs
    return (a + b * gamma + c * tau + d * gamma * tau) % p


def check_bidegree_fixtures() -> None:
    for p in (5, 7, 11):
        clone = (1, 0, 0, 1)  # 1+gamma*tau.
        clone_points = {
            (gamma, tau)
            for gamma, tau in itertools.product(range(p), repeat=2)
            if curve_value(clone, gamma, tau, p) == 0
        }
        require(len(clone_points) == p - 1, f"clone point count p={p}")
        outside_curves = (
            (0, 1, 1, 0),
            (1, 1, 1, 0),
            (2, 1, 0, 1),
            (1, 0, 1, 0),
        )
        for outside in outside_curves:
            intersections = {
                point
                for point in clone_points
                if curve_value(outside, *point, p) == 0
            }
            require(len(intersections) <= 2, f"Bezout seam p={p}")


def check_integer_grid() -> None:
    for n in range(8, 41):
        for m in range(2, n + 1):
            if not (n < 2 * m and n <= 2 * (m - 1)):
                continue
            for c in range(2, m):
                require(c * (m - c + 1) >= n, "concave endpoint inequality")
                require(
                    2 * (n - c) <= 2 * c * (m - c),
                    "per-class 2c bound",
                )


def validate_certificate(data: dict, repo_root: Path, *, check_sources: bool) -> None:
    require(data.get("schema") == SCHEMA, "schema")
    require(set(data.get("theorems", [])) == EXPECTED_THEOREMS, "theorem set")
    require(set(data.get("nonclaims", [])) == EXPECTED_NONCLAIMS, "nonclaims")
    require(data.get("source_pins") == EXPECTED_SOURCE_PINS, "source pins")
    require(data.get("review_status") == "INDEPENDENT_REVIEW_REQUESTED", "review status")
    expected_rows = {
        "koalabear_mca": (2_097_152, 1_116_048, 274_980_728_111_395_087),
        "mersenne31_mca": (2_097_152, 1_116_024, 16_777_215),
    }
    for name, expected in expected_rows.items():
        row = data["deployed_rows"][name]
        actual = (row["n"], row["m"], row["budget"])
        require(actual == expected, f"row constants: {name}")
        n, m, budget = actual
        require(n < 2 * m, f"unique large class: {name}")
        require(n <= 2 * (m - 1), f"2c endpoint: {name}")
        for c in (2, 3, m // 2, m - 2, m - 1):
            require(2 <= c < m, f"test class range: {name}")
            require(c * (m - c + 1) >= n, f"test class inequality: {name}")
            require(
                2 * (n - c) <= 2 * c * (m - c),
                f"test class 2c: {name}",
            )
        require(2 * n == 4_194_304, f"literal 2n: {name}")
        require(2 * n < budget, f"deployed payment: {name}")
    if check_sources:
        for relative, expected_sha in EXPECTED_SOURCE_PINS.items():
            path = repo_root / relative
            require(path.is_file(), f"missing source: {relative}")
            require(git_blob_sha(path.read_bytes()) == expected_sha, f"source pin: {relative}")


def load_certificate(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8")
    data = json.loads(raw)
    require(raw == json.dumps(data, indent=2, sort_keys=True) + "\n", "canonical JSON")
    return data


def run_check(repo_root: Path, certificate: Path) -> None:
    data = load_certificate(certificate)
    validate_certificate(data, repo_root, check_sources=True)
    verify_manifest(certificate.parent)
    print("PASS certificate, manifest, source pin, review status, and nonclaims")
    check_bidegree_fixtures()
    print("PASS affine-chart bidegree intersection fixtures")
    check_integer_grid()
    print("PASS concave endpoint inequality and all-subcritical-class payment")
    print("PASS unique-large-class reduction; no complete exception routing claimed")
    print(f"RESULT: PASS ({CHECKS} checks)")


def run_tamper_selftest(repo_root: Path, certificate: Path) -> None:
    pristine = load_certificate(certificate)
    validate_certificate(pristine, repo_root, check_sources=True)
    mutations = [
        ("source pin", ("source_pins", "experimental/grande_finale.tex"), "0" * 40),
        ("theorem set", ("theorems", 0), "NO_THEOREM"),
        ("nonclaim", ("nonclaims", 0), "CLAIMS_PAYMENT"),
        ("review status", ("review_status",), "AUDITED"),
        ("M31 agreement", ("deployed_rows", "mersenne31_mca", "m"), 1_116_023),
    ]
    for label, path, replacement in mutations:
        mutated = copy.deepcopy(pristine)
        cursor = mutated
        for key in path[:-1]:
            cursor = cursor[key]
        cursor[path[-1]] = replacement
        try:
            validate_certificate(mutated, repo_root, check_sources=False)
        except VerificationError:
            print(f"PASS tamper rejected: {label}")
        else:
            raise VerificationError(f"tamper accepted: {label}")
    print("RESULT: PASS (5/5 mutations rejected)")


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()
    repo_root = Path(__file__).resolve().parents[2]
    certificate = repo_root / CERT_REL
    try:
        if args.check:
            run_check(repo_root, certificate)
        else:
            run_tamper_selftest(repo_root, certificate)
    except (OSError, KeyError, ValueError, VerificationError, json.JSONDecodeError) as exc:
        print(f"RESULT: FAIL - {exc}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
