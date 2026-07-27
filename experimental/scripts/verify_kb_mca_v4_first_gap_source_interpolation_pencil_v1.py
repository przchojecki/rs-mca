#!/usr/bin/env python3
"""Verify the first-gap KoalaBear source interpolation pencil theorem."""

from __future__ import annotations

import argparse
import copy
import sys
from pathlib import Path
from typing import Any

import verify_kb_mca_v4_c5_twist_frobenius9208_adapter_v1 as active
import verify_m1_kb_rank9_full_histogram_incidence_closure_v1 as legacy

ROOT = Path(__file__).resolve().parents[2]
CERT = (
    ROOT
    / "experimental/data/certificates/"
    "kb-mca-v4-first-gap-source-interpolation-pencil-v1"
)
CERT_PATH = CERT / "certificate.json"
SCHEMA_PATH = (
    ROOT
    / "experimental/data/schemas/"
    "kb_mca_v4_first_gap_source_interpolation_pencil_v1.schema.json"
)

ARCH = active.ARCH
PARTITION_DIGEST = active.partition()["partition_sha256"]

N = legacy.N
K = legacy.K
A_AGREEMENT = legacy.A
J = legacy.J
T = legacy.T
R_FIRST = 67_471
X_FIRST = 1
SOURCE_SIZE = T + R_FIRST + 1
REDUCED_DEGREE = T
COMMON_GCD_DEGREE = K - 1 - REDUCED_DEGREE

SOURCE_PATHS = [
    (
        "experimental/data/certificates/"
        "kb-mca-v4-c5-twist-frobenius9208-adapter-v1/manifest.json"
    ),
    (
        "experimental/data/certificates/"
        "kb-mca-v4-active-full-histogram-replay-v1/certificate.json"
    ),
    (
        "experimental/notes/m1/"
        "m1_kb_rank9_source_rational_owner_splice_v1.md"
    ),
    (
        "experimental/notes/m1/"
        "m1_kb_branch3_rank9_rich_pencil_atlas_v1.md"
    ),
    (
        "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_first_gap_source_interpolation_pencil_v1.md"
    ),
]

Failure = active.Failure
need = active.need
seal = active.seal
dump = active.dump
load = active.load
file_digest = active.file_digest


def source_bindings() -> list[dict[str, str]]:
    bindings = []
    for index, path_text in enumerate(SOURCE_PATHS):
        path = ROOT / path_text
        need(path.is_file(), f"missing source: {path_text}")
        bindings.append(
            {
                "binding_id": (
                    f"SOURCE_{index:02d}_{path.stem.upper().replace('-', '_')}"
                ),
                "hash": file_digest(path),
                "hash_kind": "SHA256",
                "path": path_text,
            }
        )
    return bindings


def poly_trim(poly: list[int]) -> list[int]:
    result = poly[:]
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result


def poly_mul(left: list[int], right: list[int], p: int) -> list[int]:
    result = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] = (result[i + j] + a * b) % p
    return poly_trim(result)


def poly_eval(poly: list[int], x: int, p: int) -> int:
    result = 0
    for coefficient in reversed(poly):
        result = (result * x + coefficient) % p
    return result


def locator(points: list[int], p: int) -> list[int]:
    result = [1]
    for point in points:
        result = poly_mul(result, [(-point) % p, 1], p)
    return result


def matrix_rank(matrix: list[list[int]], p: int) -> int:
    rows = [[value % p for value in row] for row in matrix]
    if not rows:
        return 0
    row_count = len(rows)
    col_count = len(rows[0])
    pivot_row = 0
    for col in range(col_count):
        pivot = next(
            (row for row in range(pivot_row, row_count) if rows[row][col]),
            None,
        )
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        inverse = pow(rows[pivot_row][col], -1, p)
        rows[pivot_row] = [
            (value * inverse) % p for value in rows[pivot_row]
        ]
        for row in range(row_count):
            if row == pivot_row or not rows[row][col]:
                continue
            scale = rows[row][col]
            rows[row] = [
                (a - scale * b) % p
                for a, b in zip(rows[row], rows[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def interpolation_matrix(
    sigma: list[int],
    epsilon_0: list[int],
    epsilon_1: list[int],
    degree: int,
    p: int,
) -> list[list[int]]:
    rows = []
    for h in sigma:
        e0 = poly_eval(epsilon_0, h, p)
        e1 = poly_eval(epsilon_1, h, p)
        need((e0, e1) != (0, 0), "zero source pair")
        powers = [pow(h, i, p) for i in range(degree + 1)]
        rows.append(
            [(e1 * value) % p for value in powers]
            + [(-e0 * value) % p for value in powers]
        )
    return rows


def in_kernel(
    pair: tuple[list[int], list[int]],
    matrix: list[list[int]],
    degree: int,
    p: int,
) -> bool:
    left, right = pair
    vector = (
        left + [0] * (degree + 1 - len(left))
        + right + [0] * (degree + 1 - len(right))
    )
    return all(
        sum(a * b for a, b in zip(row, vector)) % p == 0
        for row in matrix
    )


def projective_normalize(pair: tuple[int, int], p: int) -> tuple[int, int]:
    left, right = pair[0] % p, pair[1] % p
    need((left, right) != (0, 0), "zero projective point")
    if left:
        inverse = pow(left, -1, p)
        return (1, right * inverse % p)
    return (0, 1)


def toy_control() -> dict[str, Any]:
    p = 17
    degree = 2
    sigma = [0, 1, 2, 3]
    f = locator([0, 1], p)
    g = locator([2, 3], p)
    source_locator = locator(sigma, p)
    matrix = interpolation_matrix(sigma, f, g, degree, p)
    rank = matrix_rank(matrix, p)
    nullity = 2 * (degree + 1) - rank
    pair_0 = (f, [0])
    pair_1 = ([0], g)
    need(in_kernel(pair_0, matrix, degree, p), "toy pair 0")
    need(in_kernel(pair_1, matrix, degree, p), "toy pair 1")
    cross = poly_mul(f, g, p)
    need(cross == source_locator, "toy determinant locator")
    leading_rank = matrix_rank(
        [[f[degree], 0], [0, g[degree]]],
        p,
    )
    need(rank == len(sigma), "toy full row rank")
    need(nullity == 2, "toy nullity")
    need(leading_rank == 2, "toy leading map")

    projective_parameters = [(1, value) for value in range(p)] + [(0, 1)]
    off_source = [x for x in range(p) if x not in sigma]
    image_sizes = []
    for x in off_source:
        fx = poly_eval(f, x, p)
        gx = poly_eval(g, x, p)
        need(fx != 0 and gx != 0, "toy off-source determinant")
        images = {
            projective_normalize(((-u * fx) % p, (v * gx) % p), p)
            for u, v in projective_parameters
        }
        image_sizes.append(len(images))
        need(len(images) == p + 1, "toy projective bijection")

    short_sigma = [0, 1, 2]
    short_matrix = interpolation_matrix(short_sigma, f, g, degree, p)
    short_rank = matrix_rank(short_matrix, p)
    short_nullity = 2 * (degree + 1) - short_rank
    lower_pair = ([0], locator([2], p))
    need(
        in_kernel(lower_pair, short_matrix, degree, p),
        "short-source lower-degree pair",
    )
    need(short_nullity == 3, "short-source nullity")

    return {
        "field_prime": p,
        "degree": degree,
        "source_points": sigma,
        "source_locator_coefficients": source_locator,
        "interpolation_rank": rank,
        "interpolation_nullity": nullity,
        "leading_coefficient_rank": leading_rank,
        "off_source_points_checked": len(off_source),
        "projective_image_sizes": image_sizes,
        "short_source_points": short_sigma,
        "short_source_rank": short_rank,
        "short_source_nullity": short_nullity,
        "threshold_sharp": short_nullity > nullity,
    }


def deployed_arithmetic() -> dict[str, Any]:
    source_rational_limit = (SOURCE_SIZE - 1) // 2
    degree_lower = source_rational_limit + 1
    degree_upper = SOURCE_SIZE + X_FIRST - T - 1
    forced_common_roots = A_AGREEMENT - X_FIRST - SOURCE_SIZE
    ambient_dimension = 2 * (REDUCED_DEGREE + 1)
    constraint_count = SOURCE_SIZE
    need(R_FIRST == T - 1, "first gap identity")
    need(SOURCE_SIZE == 2 * T, "source size")
    need(source_rational_limit == T - 1, "rational limit")
    need(degree_lower == REDUCED_DEGREE, "degree lower")
    need(degree_upper == REDUCED_DEGREE, "degree upper")
    need(
        forced_common_roots == COMMON_GCD_DEGREE,
        "forced common-root degree",
    )
    need(
        COMMON_GCD_DEGREE + REDUCED_DEGREE == K - 1,
        "degree saturation",
    )
    need(ambient_dimension - constraint_count == 2, "nullity floor")
    need(
        SOURCE_SIZE - (REDUCED_DEGREE + 1) == R_FIRST,
        "source RS redundancy",
    )
    need(
        2 * REDUCED_DEGREE - 1 < SOURCE_SIZE,
        "low-degree cross determinant",
    )
    need(
        2 * REDUCED_DEGREE == SOURCE_SIZE,
        "basis cross determinant",
    )
    need(R_FIRST > active.FROBENIUS_DEGREE, "Frobenius predecessor")
    return {
        "n": N,
        "k": K,
        "agreement": A_AGREEMENT,
        "j": J,
        "t": T,
        "r": R_FIRST,
        "x": X_FIRST,
        "source_size": SOURCE_SIZE,
        "source_rational_limit": source_rational_limit,
        "reduced_degree_lower": degree_lower,
        "reduced_degree_upper": degree_upper,
        "reduced_degree": REDUCED_DEGREE,
        "forced_common_root_degree": forced_common_roots,
        "full_gcd_degree": COMMON_GCD_DEGREE,
        "source_kernel_ambient_dimension": ambient_dimension,
        "source_constraint_count": constraint_count,
        "source_kernel_nullity_floor": ambient_dimension - constraint_count,
        "source_rs_redundancy_per_coordinate": (
            SOURCE_SIZE - (REDUCED_DEGREE + 1)
        ),
        "low_degree_cross_determinant_max": 2 * REDUCED_DEGREE - 1,
        "basis_cross_determinant_max": 2 * REDUCED_DEGREE,
        "off_source_domain_size": N - SOURCE_SIZE,
    }


def expected_certificate() -> dict[str, Any]:
    return seal(
        {
            "architecture_id": ARCH,
            "partition_sha256": PARTITION_DIGEST,
            "active_ledger": {
                "U_paid": active.PAID,
                "B_remaining": active.REMAINING,
                "additional_charge": 0,
            },
            "theorem": {
                "pair_global_source_kernel": True,
                "qualifying_reduced_pair_exists": True,
                "source_kernel_dimension": 2,
                "leading_coefficient_map_injective": True,
                "cross_determinant": "NONZERO_SCALAR_TIMES_SOURCE_LOCATOR",
                "off_source_evaluation_isomorphism": True,
                "root_slope_parameter_unique": True,
                "common_zero_set_determines_graph_line": True,
                "selector_independent": True,
                "determinant_mass_paid": False,
            },
            "deployed_arithmetic": deployed_arithmetic(),
            "finite_field_control": toy_control(),
            "source_bindings": source_bindings(),
            "status": (
                "PROVED_FIRST_GAP_SOURCE_INTERPOLATION_PENCIL_"
                "DETERMINANT_PACKING_OPEN_ROW_OPEN"
            ),
        }
    )


def expected_schema() -> dict[str, Any]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "additionalProperties": True,
        "properties": {
            "architecture_id": {"const": ARCH},
            "partition_sha256": {"const": PARTITION_DIGEST},
            "payload_sha256": {"pattern": "^[0-9a-f]{64}$", "type": "string"},
        },
        "required": ["architecture_id", "partition_sha256", "payload_sha256"],
        "title": "KoalaBear first-gap source interpolation pencil",
        "type": "object",
    }


def check_sources() -> None:
    note = (
        ROOT
        / "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_first_gap_source_interpolation_pencil_v1.md"
    ).read_text(encoding="utf-8")
    for anchor in [
        "PROVED SOURCE-BOUND NORMAL FORM",
        "\\boxed{e=t=67{,}472,\\qquad s=2e.}",
        "\\boxed{\\dim_F\\mathcal K_\\Sigma(e)=2.}",
        "R_0S_1-R_1S_0=c_\\Sigma L_\\Sigma",
        "Unique root/slope parameter",
        "common-zero set determines the graph line",
        "67{,}471",
        "# PROVED",
    ]:
        need(anchor in note, f"missing note anchor: {anchor}")


def validate(cert: dict[str, Any], schema: dict[str, Any]) -> None:
    need(cert == expected_certificate(), "certificate differs from exact replay")
    need(schema == expected_schema(), "schema differs from exact replay")
    need(cert["active_ledger"]["additional_charge"] == 0, "zero movement")
    need(
        cert["theorem"]["source_kernel_dimension"] == 2,
        "kernel dimension",
    )
    need(
        cert["theorem"]["determinant_mass_paid"] is False,
        "determinant status",
    )
    check_sources()


def emit() -> None:
    dump(CERT_PATH, expected_certificate())
    dump(SCHEMA_PATH, expected_schema())


def tamper_selftest() -> None:
    cert = expected_certificate()
    schema = expected_schema()
    mutations = [
        lambda d: d["deployed_arithmetic"].__setitem__(
            "reduced_degree", REDUCED_DEGREE + 1
        ),
        lambda d: d["theorem"].__setitem__("source_kernel_dimension", 3),
        lambda d: d["theorem"].__setitem__(
            "cross_determinant", "UNBOUND"
        ),
        lambda d: d["theorem"].__setitem__(
            "off_source_evaluation_isomorphism", False
        ),
        lambda d: d["theorem"].__setitem__(
            "common_zero_set_determines_graph_line", False
        ),
        lambda d: d["deployed_arithmetic"].__setitem__(
            "source_rs_redundancy_per_coordinate", R_FIRST - 1
        ),
        lambda d: d["finite_field_control"].__setitem__(
            "short_source_nullity", 2
        ),
        lambda d: d["active_ledger"].__setitem__("additional_charge", 1),
    ]
    passed = 0
    for mutate in mutations:
        bad = copy.deepcopy(cert)
        mutate(bad)
        try:
            validate(bad, schema)
        except Failure:
            passed += 1
        else:
            raise Failure("tamper accepted")
    need(passed == len(mutations), "tamper count")
    print(f"tamper-selftest: PASS {passed}/{len(mutations)}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()
    try:
        if args.emit:
            emit()
        if args.check:
            cert = load(CERT_PATH)
            schema = load(SCHEMA_PATH)
            validate(cert, schema)
            arithmetic = cert["deployed_arithmetic"]
            control = cert["finite_field_control"]
            print(f"architecture: {ARCH}")
            print(f"partition_sha256: {PARTITION_DIGEST}")
            print(
                "first_gap: "
                f"r={arithmetic['r']} x={arithmetic['x']} "
                f"s={arithmetic['source_size']} "
                f"e={arithmetic['reduced_degree']}"
            )
            print(
                "source_kernel: "
                f"dimension={cert['theorem']['source_kernel_dimension']} "
                f"cross={cert['theorem']['cross_determinant']}"
            )
            print(
                "toy_control: "
                f"nullity={control['interpolation_nullity']} "
                f"short_nullity={control['short_source_nullity']}"
            )
            print(f"payload_sha256: {cert['payload_sha256']}")
            print("check: PASS")
        if args.tamper_selftest:
            tamper_selftest()
        if not (args.emit or args.check or args.tamper_selftest):
            parser.error("choose --emit, --check, or --tamper-selftest")
    except Failure as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
