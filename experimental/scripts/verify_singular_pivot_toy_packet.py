#!/usr/bin/env python3
"""Verify a nonzero singular-bucket affine pivot toy packet.

The toy is intentionally small, but it exercises the v9 singular-pivot shape:
the regular overdetermined bucket is genuinely singular because every maximal
Hankel minor vanishes, while the exact support-image map closes the finite
affine contribution after splitting by noncontainment pivots B_h != 0.
"""

from __future__ import annotations

import argparse
from itertools import combinations
import importlib.util
import json
from hashlib import sha256
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
P = 17
N = 10
K = 4
AGREEMENT = 8
J = N - AGREEMENT
T = AGREEMENT - K
SIZE = J + 1
DOMAIN = list(range(1, 11))
U = [10, 8, 14, 5, 9, 15]
V = [2, 5, 13, 1, 12, 3]
SLOPE = 12
ELIMINANT = [5, 1]  # Z + 5 has root 12 over F_17.

CERTIFICATE_REF = (
    "experimental/data/certificates/singular-pivot-toy/"
    "f17_n10_k4_a8_singular_pivot_certificate.json"
)
PACKET_REF = (
    "experimental/data/certificates/singular-pivot-toy/"
    "f17_n10_k4_a8_singular_pivot_packet.json"
)
SCHEMA_CHECKER = ROOT / "scripts/check_aperiodic_eliminant_packet.py"
SCHEMA = ROOT / "scripts/aperiodic_eliminant_schema.json"


def mod(value: int) -> int:
    return value % P


def hash_json(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return sha256(payload).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def render(value: dict[str, Any]) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_schema_checker():
    spec = importlib.util.spec_from_file_location(
        "check_aperiodic_eliminant_packet", SCHEMA_CHECKER
    )
    require(spec is not None and spec.loader is not None, "could not load schema checker")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def matrix_at_slope(z: int) -> list[list[int]]:
    return [[mod(U[row + col] + z * V[row + col]) for col in range(SIZE)] for row in range(T)]


def hankel_v() -> list[list[int]]:
    return [[V[row + col] for col in range(SIZE)] for row in range(T)]


def rank_mod(matrix: list[list[int]]) -> int:
    work = [[entry % P for entry in row] for row in matrix]
    rank = 0
    rows = len(work)
    cols = len(work[0])
    for col in range(cols):
        pivot = next((row for row in range(rank, rows) if work[row][col]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        inv = pow(work[rank][col], -1, P)
        work[rank] = [(entry * inv) % P for entry in work[rank]]
        for row in range(rows):
            if row == rank or work[row][col] == 0:
                continue
            factor = work[row][col]
            work[row] = [
                (work[row][entry_col] - factor * work[rank][entry_col]) % P
                for entry_col in range(cols)
            ]
        rank += 1
    return rank


def mat_vec(matrix: list[list[int]], vector: list[int]) -> list[int]:
    return [sum(row[col] * vector[col] for col in range(len(vector))) % P for row in matrix]


def locator_for_pair(pair: tuple[int, int]) -> list[int]:
    x, y = pair
    return [(x * y) % P, (-(x + y)) % P, 1]


def poly_eval(coefficients: list[int], value: int) -> int:
    total = 0
    power = 1
    for coeff in coefficients:
        total = (total + coeff * power) % P
        power = (power * value) % P
    return total


def support_records() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    h_v = hankel_v()
    records: list[dict[str, Any]] = []
    pivot_counts = {f"B_{index}": 0 for index in range(T)}
    contained_count = 0
    projective_infinity_count = 0
    slopes: set[int] = set()
    for pair in combinations(DOMAIN, J):
        locator = locator_for_pair(pair)
        b_vec = mat_vec(h_v, locator)
        a_vec = [(5 * value) % P for value in b_vec]
        if all(value == 0 for value in b_vec):
            if any(value != 0 for value in a_vec):
                projective_infinity_count += 1
                status = "projective_infinity"
            else:
                contained_count += 1
                status = "contained_residual_B_equals_0"
            records.append(
                {
                    "T": list(pair),
                    "locator_coefficients": locator,
                    "A": a_vec,
                    "B": b_vec,
                    "status": status,
                    "slope": None,
                    "pivot": None,
                }
            )
            continue
        pivot_index = next(index for index, value in enumerate(b_vec) if value)
        slope = (-a_vec[pivot_index] * pow(b_vec[pivot_index], -1, P)) % P
        require(slope == SLOPE, f"unexpected slope for T={pair}: {slope}")
        require(
            all((a_vec[index] + slope * b_vec[index]) % P == 0 for index in range(T)),
            f"collinearity failure for T={pair}",
        )
        slopes.add(slope)
        pivot_counts[f"B_{pivot_index}"] += 1
        records.append(
            {
                "T": list(pair),
                "locator_coefficients": locator,
                "A": a_vec,
                "B": b_vec,
                "status": "affine_pivot_eliminant",
                "slope": slope,
                "pivot": f"B_{pivot_index}",
            }
        )
    summary = {
        "support_count": len(records),
        "contained_residual_B_equals_0": contained_count,
        "projective_infinity_count": projective_infinity_count,
        "pivot_counts": pivot_counts,
        "root_union_mod_17": sorted(slopes),
    }
    return records, summary


def build_certificate() -> dict[str, Any]:
    records, summary = support_records()
    ranks = [{"z": z, "rank": rank_mod(matrix_at_slope(z))} for z in range(P)]
    rank_at_nodes = ranks[: SIZE + 1]
    require(rank_mod(hankel_v()) == 2, "H(v) should have rank 2")
    require(all(item["rank"] < SIZE for item in ranks), "regular bucket not singular")
    require(summary["root_union_mod_17"] == [SLOPE], "root union mismatch")
    return {
        "schema_version": "singular-pivot-toy-certificate-v1",
        "status": "PROVED / AUDIT",
        "row": {
            "n": N,
            "k": K,
            "field": "F_17",
            "domain": DOMAIN,
            "domain_description": "first ten nonzero elements of F_17",
            "domain_hash": hash_json(DOMAIN),
        },
        "agreement": {"A": AGREEMENT, "j": J, "t": T, "minor_size": SIZE},
        "syndrome_pencil": {
            "u": U,
            "v": V,
            "relation": "u = 5 v",
            "hankel_v_rank": 2,
            "regular_matrix": "H(u)+Z H(v) = (Z+5) H(v)",
        },
        "regular_bucket_singularity": {
            "rank_at_all_finite_slopes": ranks,
            "rank_at_nodes_certificate": rank_at_nodes,
            "nodes_required_for_singularity_proof": SIZE + 1,
            "reason": (
                "All 3x3 minors have degree at most 3 and vanish at four "
                "distinct slopes, so every maximal regular minor is the zero "
                "polynomial."
            ),
        },
        "support_image_equations": {
            "locator": "ell_T(X)=prod_{x in T}(X-x), coefficients low-to-high",
            "A_T": "H(u) ell_T",
            "B_T": "H(v) ell_T",
            "finite_bad_condition": "A_T + Z B_T = 0 and B_T != 0",
            "contained_residual": "B_T = 0 forces A_T = 0 because u=5v",
        },
        "projective_infinity_chart": {
            "status": "empty",
            "projective_point": "[0:1]",
            "equations": "B_T = 0",
            "inequations": "A_T != 0",
            "reason": (
                "A_T=5B_T, so B_T=0 forces A_T=0 and the infinity chart is empty."
            ),
            "support_count": summary["projective_infinity_count"],
        },
        "pivot_open_cover": ["B_0 != 0", "B_1 != 0", "B_2 != 0", "B_3 != 0"],
        "pivots": {
            "B_0": {
                "status": "eliminant",
                "support_count": summary["pivot_counts"]["B_0"],
                "eliminant_coefficients_mod_17_ascending": ELIMINANT,
                "roots_mod_17": [SLOPE],
                "degree": 1,
            },
            "B_1": {
                "status": "eliminant",
                "support_count": summary["pivot_counts"]["B_1"],
                "eliminant_coefficients_mod_17_ascending": ELIMINANT,
                "roots_mod_17": [SLOPE],
                "degree": 1,
            },
            "B_2": {"status": "empty", "support_count": summary["pivot_counts"]["B_2"]},
            "B_3": {"status": "empty", "support_count": summary["pivot_counts"]["B_3"]},
        },
        "coverage": {
            "split_cosupport_count": summary["support_count"],
            "contained_residual_B_equals_0": summary["contained_residual_B_equals_0"],
            "projective_infinity_count": summary["projective_infinity_count"],
            "pivot_counts": summary["pivot_counts"],
            "root_union_mod_17": summary["root_union_mod_17"],
            "declared_aperiodic_numerator": len(summary["root_union_mod_17"]),
        },
        "support_records": records,
        "nonclaims": [
            "toy row only",
            "not an F_17^32 row-data packet",
            "not a prize-row threshold theorem",
            "not a uniform singular-pivot algorithm",
        ],
    }


def build_packet(certificate: dict[str, Any]) -> dict[str, Any]:
    cert_ref = CERTIFICATE_REF
    return {
        "schema_version": "aperiodic-hankel-eliminant-v1",
        "row": {
            "n": N,
            "k": K,
            "field": "F_17",
            "domain_hash": certificate["row"]["domain_hash"],
            "domain_description": certificate["row"]["domain_description"],
        },
        "agreement_threshold": AGREEMENT,
        "sampler": "projective_line",
        "removed_ledgers": [],
        "exact_agreements": [
            {
                "A": AGREEMENT,
                "j": J,
                "t": T,
                "status": "pivot_atlas",
                "regular_bucket_status": "singular",
                "regular_bucket_ref": f"{cert_ref}#/regular_bucket_singularity",
                "charts": [
                    {
                        "chart_id": "split_cosupports_size_2",
                        "equations_ref": f"{cert_ref}#/support_image_equations",
                        "inequations_ref": f"{cert_ref}#/pivot_open_cover",
                        "coverage_ref": f"{cert_ref}#/coverage",
                        "pivot_records": [
                            {
                                "pivot": "B_0 != 0",
                                "status": "eliminant",
                                "eliminant_ref": f"{cert_ref}#/pivots/B_0",
                                "degree": 1,
                            },
                            {
                                "pivot": "B_1 != 0",
                                "status": "eliminant",
                                "eliminant_ref": f"{cert_ref}#/pivots/B_1",
                                "degree": 1,
                            },
                            {"pivot": "B_2 != 0", "status": "empty"},
                            {"pivot": "B_3 != 0", "status": "empty"},
                        ],
                    },
                    {
                        "chart_id": "projective_infinity",
                        "equations_ref": (
                            f"{cert_ref}#/projective_infinity_chart/equations"
                        ),
                        "inequations_ref": (
                            f"{cert_ref}#/projective_infinity_chart/inequations"
                        ),
                        "coverage_ref": f"{cert_ref}#/projective_infinity_chart",
                        "pivot_records": [
                            {
                                "pivot": "B_T = 0, A_T != 0 at [0:1]",
                                "status": "empty",
                            }
                        ],
                    }
                ],
            }
        ],
        "declared_aperiodic_numerator": 1,
        "root_union_table_ref": f"{cert_ref}#/coverage/root_union_mod_17",
        "status": "PROVED / AUDIT",
        "nonclaims": [
            "toy row only",
            "not an F_17^32 row-data packet",
            "not a prize-row threshold theorem",
            "not a uniform singular-pivot algorithm",
        ],
    }


def validate_certificate(certificate: dict[str, Any]) -> None:
    expected = build_certificate()
    require(certificate == expected, "certificate is not deterministic")
    require(poly_eval(ELIMINANT, SLOPE) == 0, "eliminant does not vanish at root")
    roots = [z for z in range(P) if poly_eval(ELIMINANT, z) == 0]
    require(roots == [SLOPE], "eliminant root table mismatch")


def validate_packet(packet: dict[str, Any], certificate: dict[str, Any]) -> None:
    expected = build_packet(certificate)
    require(packet == expected, "packet is not deterministic")
    checker = load_schema_checker()
    checker.check_path(ROOT / PACKET_REF, SCHEMA)


def check_file(path: Path, expected: dict[str, Any], label: str) -> None:
    actual = path.read_text(encoding="utf-8")
    rendered = render(expected)
    if actual != rendered:
        raise AssertionError(f"{label} mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    coverage = certificate["coverage"]
    print("singular pivot toy packet")
    print("row: F_17, n=10, k=4, A=8")
    print("regular bucket: singular; rank(H(v))=2, rank(H(u)+zH(v))<3 for all z")
    print(
        (
            "pivot supports: B_0={B_0}, B_1={B_1}, B_2={B_2}, B_3={B_3}, "
            "contained={contained}, infinity={infinity}"
        ).format(
            contained=coverage["contained_residual_B_equals_0"],
            infinity=coverage["projective_infinity_count"],
            **coverage["pivot_counts"],
        )
    )
    print(f"root union: {coverage['root_union_mod_17']}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-certificate", type=Path)
    parser.add_argument("--write-packet", type=Path)
    parser.add_argument("--check-certificate", type=Path)
    parser.add_argument("--check-packet", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    certificate = build_certificate()
    packet = build_packet(certificate)
    validate_certificate(certificate)
    if args.write_certificate:
        args.write_certificate.parent.mkdir(parents=True, exist_ok=True)
        args.write_certificate.write_text(render(certificate), encoding="utf-8")
    if args.write_packet:
        args.write_packet.parent.mkdir(parents=True, exist_ok=True)
        args.write_packet.write_text(render(packet), encoding="utf-8")
    if args.check_certificate:
        check_file(args.check_certificate, certificate, "certificate")
    if args.check_packet:
        validate_packet(load_json(args.check_packet), certificate)
        check_file(args.check_packet, packet, "packet")
    if args.json:
        print(render(certificate), end="")
        return
    print_summary(certificate)


if __name__ == "__main__":
    main()
