#!/usr/bin/env python3
"""Replay finite seams for denominator-root puncture trivialization.

The universal results are proved in the accompanying note. This stdlib-only
checker binds their prerequisites, exact row constants, finite-field seams,
non-payment fence, and nonclaims. It claims no exception payment.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
import sys
from math import comb
from pathlib import Path
from typing import Sequence


CERT_REL = Path(
    "experimental/data/certificates/"
    "denominator-root-puncture-trivialization-v1/certificate.json"
)
SCHEMA = "denominator-root-puncture-trivialization-v1"
EXPECTED_SOURCE_PINS = {
    "experimental/grande_finale.tex": "6b21d6ea937a8a9f85fc7ade6032d73efd4c7222",
    "experimental/notes/m2/pole_tolerant_scalar_locator_localization.md": (
        "ba51f8ddac7b6fb84669f9d805fb56f5a9ed0df1"
    ),
}
EXPECTED_THEOREMS = {
    "DENOMINATOR_ROOT_CANCELLATION_DICHOTOMY",
    "PUNCTURE_TRIVIALIZED_SUPPORT_SHADOW_PACKING",
}
EXPECTED_NONCLAIMS = {
    "NO_BOUND_ON_ACTUAL_TRIVIALIZED_CARDINALITY",
    "NO_SPREAD_OR_LARGE_OWNER_ABSORPTION",
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
            "../../../notes/m2/denominator_root_puncture_trivialization.md",
            "../../../scripts/verify_denominator_root_puncture_trivialization.py",
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


def poly_eval(coeffs: Sequence[int], x: int, p: int) -> int:
    value = 0
    for coefficient in reversed(coeffs):
        value = (value * x + coefficient) % p
    return value


def values_extend_to_degree_lt(
    xs: Sequence[int], ys: Sequence[int], k: int, p: int
) -> bool:
    matrix = [[pow(x, j, p) for j in range(k)] + [y % p] for x, y in zip(xs, ys)]
    row = 0
    for column in range(k):
        pivot = next(
            (index for index in range(row, len(matrix)) if matrix[index][column] % p),
            None,
        )
        if pivot is None:
            continue
        matrix[row], matrix[pivot] = matrix[pivot], matrix[row]
        inverse = pow(matrix[row][column], -1, p)
        matrix[row] = [(value * inverse) % p for value in matrix[row]]
        for index in range(len(matrix)):
            if index == row or matrix[index][column] % p == 0:
                continue
            factor = matrix[index][column] % p
            matrix[index] = [
                (matrix[index][j] - factor * matrix[row][j]) % p
                for j in range(k + 1)
            ]
        row += 1
    return not any(
        all(value % p == 0 for value in equation[:k])
        and equation[-1] % p != 0
        for equation in matrix
    )


def check_trivialization_fixture() -> None:
    p = 11
    k = 2
    gamma = 1
    support = (0, 1, 2)
    reduced_support = (1, 2)
    r0 = {0: 10, 1: 0, 2: 0}
    r1 = {0: 1, 1: 0, 2: 0}
    h = (0,)
    q = (0, 1)
    locator = (0, 2, 8, 1)  # X(X-1)(X-2) over F_11.
    a = locator
    b = (0,)

    for x in support:
        require(
            poly_eval(q, x, p) * poly_eval(h, x, p) + poly_eval(locator, x, p)
            == (poly_eval(a, x, p) + gamma * poly_eval(b, x, p)) % p,
            "scalar-locator fixture identity",
        )
        require(
            poly_eval(h, x, p) == (r0[x] + gamma * r1[x]) % p,
            "fixture support agreement",
        )

    require(
        not values_extend_to_degree_lt(support, [r0[x] for x in support], k, p),
        "original r0 is nontrivial",
    )
    require(
        not values_extend_to_degree_lt(support, [r1[x] for x in support], k, p),
        "original r1 is nontrivial",
    )
    for received in (r0, r1):
        require(
            values_extend_to_degree_lt(
                reduced_support, [received[x] for x in reduced_support], k, p
            ),
            "punctured explanation exists",
        )
    u = r0[0]
    v = r1[0]
    require(v != 0, "nonzero pole defect")
    require((u + gamma * v) % p == 0, "pole defect recovers slope")


def check_pair_uniqueness() -> None:
    for p in (3, 5, 7):
        points = (1, 2)
        seen = {}
        for coefficients in itertools.product(range(p), repeat=2):
            values = tuple(poly_eval(coefficients, x, p) for x in points)
            require(values not in seen, f"degree-one interpolation uniqueness p={p}")
            seen[values] = coefficients


def check_slope_recovery() -> None:
    for p in (3, 5, 7):
        for dimension in (1, 2, 3):
            for packed in itertools.product(range(p), repeat=2 * dimension):
                u = packed[:dimension]
                v = packed[dimension:]
                compatible = [
                    gamma
                    for gamma in range(p)
                    if all((a + gamma * b) % p == 0 for a, b in zip(u, v))
                ]
                if any(v):
                    require(len(compatible) <= 1, "nonzero defect has unique slope")
                elif any(u):
                    require(not compatible, "zero direction cannot absorb nonzero offset")
                else:
                    require(compatible == list(range(p)), "zero defect accepts all slopes")


def check_shadow_packing() -> None:
    universe = range(8)
    support_size = 4
    k = 2
    family = []
    for support_tuple in itertools.combinations(universe, support_size):
        support = set(support_tuple)
        if all(len(support & previous) < k for previous in family):
            family.append(support)
    shadows = []
    for support in family:
        shadow = set(itertools.combinations(sorted(support), k))
        require(
            all(shadow.isdisjoint(previous) for previous in shadows),
            "disjoint k-shadows",
        )
        shadows.append(shadow)
    require(len(family) > 1, "nontrivial shadow fixture")
    require(
        len(family) * comb(support_size, k) <= comb(len(tuple(universe)), k),
        "shadow packing inequality",
    )


def validate_certificate(data: dict, repo_root: Path, *, check_sources: bool) -> None:
    require(data.get("schema") == SCHEMA, "schema")
    require(set(data.get("theorems", [])) == EXPECTED_THEOREMS, "theorem set")
    require(set(data.get("nonclaims", [])) == EXPECTED_NONCLAIMS, "nonclaims")
    require(data.get("source_pins") == EXPECTED_SOURCE_PINS, "source pins")
    require(data.get("review_status") == "INDEPENDENT_REVIEW_REQUESTED", "review status")
    expected_rows = {
        "koalabear_mca": (2_097_152, 1_048_576, 1_116_048, 274_980_728_111_395_087),
        "mersenne31_mca": (2_097_152, 1_048_576, 1_116_024, 16_777_215),
    }
    for name, expected in expected_rows.items():
        row = data["deployed_rows"][name]
        actual = (row["n"], row["k"], row["m"], row["budget"])
        require(actual == expected, f"row constants: {name}")
        n, k, m, budget = actual
        require(n >= m > k, f"row order: {name}")
        require(2 * n > 3 * m, f"n/m > 3/2: {name}")
        require(k > 100, f"large k: {name}")
        require(budget < 2**58, f"budget below 2^58: {name}")
        for t in (0, 1, m - k - 1, m - k):
            require(0 <= t <= m - k, f"pole degree endpoint: {name}")
            require(m - t >= k, f"reduced support interpolation: {name}")
    require(3**100 > 2**158, "exact (3/2)^100 > 2^58")
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
    print("PASS certificate, manifest, prerequisite pins, review status, and nonclaims")
    check_trivialization_fixture()
    check_pair_uniqueness()
    check_slope_recovery()
    print("PASS puncture fixture, interpolation uniqueness, and pole-defect slope recovery")
    check_shadow_packing()
    print("PASS shadow disjointness and exact deployed non-payment fence")
    print("PASS no exception payment or endpoint claimed")
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
