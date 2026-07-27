#!/usr/bin/env python3
"""Verify the KoalaBear reciprocal-kernel plane interval sweep."""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import random
import sys
from pathlib import Path
from typing import Any

import verify_kb_mca_v4_post_second_successor_full_histogram_replay_v1 as replay
import verify_kb_mca_v4_second_successor_upper_intrinsic_plane_descent_v1 as upper

ROOT = Path(__file__).resolve().parents[2]
CERT = (
    ROOT
    / "experimental/data/certificates/"
    "kb-mca-v4-reciprocal-kernel-plane-sweep-v1"
)
CERT_PATH = CERT / "certificate.json"
SCHEMA_PATH = (
    ROOT
    / "experimental/data/schemas/"
    "kb_mca_v4_reciprocal_kernel_plane_sweep_v1.schema.json"
)

ARCH = replay.ARCH
PARTITION_DIGEST = replay.PARTITION_DIGEST
R_MIN = 67_475
R_MAX = 134_942
FIRST_OPEN = 134_943
PAID_COUNT = R_MAX - R_MIN + 1
T = upper.plane.pencil.T
N = upper.plane.pencil.N
P = upper.plane.active.prev.BASE_PRIME
B_REMAINING = replay.B_REMAINING

Failure = replay.Failure
need = replay.need
seal = replay.seal
dump = replay.dump
load = replay.load
file_digest = replay.file_digest
canonical_bytes = replay.canonical_bytes
residue = upper.residue

UPSTREAM_CERTIFICATES = {
    "post_second_successor_histogram": {
        "path": (
            "experimental/data/certificates/"
            "kb-mca-v4-post-second-successor-full-histogram-replay-v1/"
            "certificate.json"
        ),
        "payload_sha256": (
            'b0212943d8dfe070c0d36cc9105c52ca60b5380d47b07eb4c1f9e560ade99fd9'
        ),
    },
    "cubic_relation_endpoint": {
        "path": (
            "experimental/data/certificates/"
            "kb-mca-v4-second-successor-upper-intrinsic-plane-descent-v1/"
            "certificate.json"
        ),
        "payload_sha256": (
            '3e7f870adb5f39d5766ffda0cdc3ee248a8f8e0892099734c442e035ed07c177'
        ),
    },
}

SOURCE_PATHS = [
    (
        "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_second_successor_upper_intrinsic_plane_descent_v1.md"
    ),
    (
        "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_post_second_successor_full_histogram_replay_v1.md"
    ),
    (
        "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_reciprocal_kernel_plane_sweep_v1.md"
    ),
]


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


def upstream_bindings() -> dict[str, dict[str, str]]:
    bindings = {}
    for key, contract in UPSTREAM_CERTIFICATES.items():
        path = ROOT / contract["path"]
        need(path.is_file(), f"missing upstream certificate: {key}")
        payload = load(path)
        need(
            payload.get("payload_sha256") == contract["payload_sha256"],
            f"upstream payload mismatch: {key}",
        )
        bindings[key] = {**contract, "file_sha256": file_digest(path)}
    return bindings


def source_size(r: int) -> int:
    return T + r + 1


def maximum_degree(r: int) -> int:
    return r + 1


def maximum_c(r: int) -> int:
    return 2 * maximum_degree(r) - source_size(r)


def strict_degree_margin(r: int) -> int:
    return maximum_degree(r) - 2 * maximum_c(r)


def direct_cap(r: int) -> int:
    return (P + 1) * (N - source_size(r))


def start_strata() -> list[dict[str, int]]:
    r = R_MIN
    s = source_size(r)
    x_floor = (s + 1) // 2 - r
    e_min = (s + 1) // 2
    rows = []
    for x in range(x_floor, 2):
        for e in range(e_min, r + x + 1):
            h = r + x - e
            c = 2 * e - s
            need(h >= 0 and c >= 0, "negative start stratum")
            need(e > 2 * c, "start stratum outside theorem")
            rows.append(
                {
                    "x": x,
                    "e": e,
                    "extra_gcd_degree": h,
                    "c": c,
                    "source_dimension": c + 2,
                }
            )
    need(len(rows) == 6, "start stratum count")
    return rows


def interval_sweep() -> dict[str, Any]:
    digest = hashlib.sha256()
    minimum_margin = None
    maximum_cap = 0
    maximum_cap_r = None
    for r in range(R_MIN, R_MAX + 1):
        s = source_size(r)
        e = maximum_degree(r)
        c = maximum_c(r)
        margin = strict_degree_margin(r)
        cap = direct_cap(r)
        need(s == r + 67_473, "source-size affine law")
        need(c == r - 67_471, "maximum-c affine law")
        need(margin == 134_943 - r, "strict-margin affine law")
        need(margin > 0, "nonpositive degree margin in paid interval")
        need(cap < B_REMAINING, "direct cap exceeds reserve")
        digest.update(canonical_bytes([r, s, e, c, margin, cap]))
        minimum_margin = (
            margin if minimum_margin is None else min(minimum_margin, margin)
        )
        if cap > maximum_cap:
            maximum_cap = cap
            maximum_cap_r = r

    need(PAID_COUNT == 67_468, "paid interval count")
    need(minimum_margin == 1, "minimum strict margin")
    need(maximum_cap_r == R_MIN, "maximum cap endpoint")
    need(maximum_cap == 4_180_880_687_620_536, "maximum direct cap")
    need(
        B_REMAINING - maximum_cap == 266_599_332_272_955_344,
        "minimum reserve margin",
    )

    boundary = {
        "r": FIRST_OPEN,
        "source_size": source_size(FIRST_OPEN),
        "maximum_degree": maximum_degree(FIRST_OPEN),
        "maximum_c": maximum_c(FIRST_OPEN),
        "strict_degree_margin": strict_degree_margin(FIRST_OPEN),
        "double_source_degree": 2 * source_size(FIRST_OPEN),
        "three_minor_degree": 3 * maximum_degree(FIRST_OPEN),
        "relation_product_degree": (
            maximum_degree(FIRST_OPEN) + maximum_c(FIRST_OPEN)
        ),
    }
    need(boundary["strict_degree_margin"] == 0, "first-open margin")
    need(
        boundary["double_source_degree"]
        == boundary["three_minor_degree"],
        "first-open determinant equality",
    )
    need(
        boundary["relation_product_degree"] == boundary["source_size"],
        "first-open no-wrap equality",
    )

    return {
        "r_min": R_MIN,
        "r_max": R_MAX,
        "paid_count": PAID_COUNT,
        "scan_sha256": digest.hexdigest(),
        "minimum_strict_degree_margin": minimum_margin,
        "maximum_direct_cap": maximum_cap,
        "maximum_direct_cap_r": maximum_cap_r,
        "minimum_reserve_margin": B_REMAINING - maximum_cap,
        "start_strata": start_strata(),
        "last_paid": {
            "r": R_MAX,
            "source_size": source_size(R_MAX),
            "maximum_degree": maximum_degree(R_MAX),
            "maximum_c": maximum_c(R_MAX),
            "strict_degree_margin": strict_degree_margin(R_MAX),
            "carrier_size": N - source_size(R_MAX),
            "direct_cap": direct_cap(R_MAX),
        },
        "first_open": boundary,
    }


def add_poly(left: list[int], right: list[int], prime: int) -> list[int]:
    length = max(len(left), len(right))
    return residue.trim(
        [
            (
                (left[index] if index < len(left) else 0)
                + (right[index] if index < len(right) else 0)
            )
            % prime
            for index in range(length)
        ]
    )


def sub_poly(left: list[int], right: list[int], prime: int) -> list[int]:
    return add_poly(
        left, [(-coefficient) % prime for coefficient in right], prime
    )


def matrix_syzygies(
    matrix: list[tuple[list[int], list[int]]],
    relation_degree: int,
    prime: int,
) -> list[list[int]]:
    row_count = len(matrix)
    product_degree = max(
        len(entry) - 1 for row in matrix for entry in row
    ) + relation_degree
    equations = []
    for column in range(2):
        for degree in range(product_degree + 1):
            equation = []
            for row in range(row_count):
                polynomial = matrix[row][column]
                for power in range(relation_degree + 1):
                    index = degree - power
                    equation.append(
                        polynomial[index]
                        if 0 <= index < len(polynomial)
                        else 0
                    )
            equations.append(equation)
    return residue.nullspace(equations, prime)


def evaluate_relation(
    relation: list[int],
    row_count: int,
    degree: int,
    point: int,
    prime: int,
) -> list[int]:
    return [
        sum(
            relation[row * (degree + 1) + power]
            * pow(point, power, prime)
            for power in range(degree + 1)
        )
        % prime
        for row in range(row_count)
    ]


def saturated_kernel_regression() -> dict[str, Any]:
    prime = 29
    e = 9
    profiles = []
    for c in range(1, 5):
        need(e > 2 * c, "synthetic strict degree condition")
        s = 2 * e - c
        left_locator = residue.locator(range(s // 2), prime)
        right_locator = residue.locator(range(s // 2, s), prime)
        left_margin = e - (len(left_locator) - 1)
        right_margin = e - (len(right_locator) - 1)
        source_locator = residue.mul(left_locator, right_locator, prime)
        for b in range(3, c + 3):
            rng = random.Random(10_000 * c + 100 * b)
            matrix = []
            for _ in range(b):
                left_factor = [
                    rng.randrange(prime) for _ in range(left_margin + 1)
                ]
                right_factor = [
                    rng.randrange(prime) for _ in range(right_margin + 1)
                ]
                if not any(left_factor):
                    left_factor[0] = 1
                if not any(right_factor):
                    right_factor[0] = 1
                matrix.append(
                    (
                        residue.mul(left_locator, left_factor, prime),
                        residue.mul(right_locator, right_factor, prime),
                    )
                )

            nonzero_quotients = 0
            maximum_quotient_degree = -1
            for first, second in itertools.combinations(range(b), 2):
                minor = sub_poly(
                    residue.mul(
                        matrix[first][0], matrix[second][1], prime
                    ),
                    residue.mul(
                        matrix[second][0], matrix[first][1], prime
                    ),
                    prime,
                )
                quotient, remainder = residue.divmod_poly(
                    minor, source_locator, prime
                )
                need(remainder == [0], "minor lacks source locator")
                if quotient != [0]:
                    nonzero_quotients += 1
                    maximum_quotient_degree = max(
                        maximum_quotient_degree, len(quotient) - 1
                    )
            need(nonzero_quotients > 0, "synthetic matrix rank below two")
            need(
                maximum_quotient_degree <= c,
                "synthetic quotient exceeds c",
            )

            relations = matrix_syzygies(matrix, c, prime)
            need(relations, "missing synthetic relation space")
            pointwise_ranks = [
                residue.rank(
                    [
                        evaluate_relation(
                            relation, b, c, point, prime
                        )
                        for relation in relations
                    ],
                    prime,
                )
                for point in range(prime)
            ]
            need(
                min(pointwise_ranks) >= b - 2,
                "synthetic relation rank drop",
            )
            profiles.append(
                {
                    "c": c,
                    "base_span": b,
                    "source_size": s,
                    "left_factor_margin": left_margin,
                    "right_factor_margin": right_margin,
                    "relation_space_dimension": len(relations),
                    "minimum_pointwise_rank": min(pointwise_ranks),
                    "maximum_pointwise_rank": max(pointwise_ranks),
                    "maximum_minor_quotient_degree": (
                        maximum_quotient_degree
                    ),
                }
            )
    need(len(profiles) == 10, "synthetic profile count")
    return {
        "prime": prime,
        "degree": e,
        "profile_count": len(profiles),
        "profiles": profiles,
    }


def expected_certificate() -> dict[str, Any]:
    return seal(
        {
            "architecture_id": ARCH,
            "partition_sha256": PARTITION_DIGEST,
            "counted_object": (
                "SCALAR-UNPAID FULL-OUTSIDE COEFFICIENT-RANK-TWO "
                "SLOPES AT FIXED SLACK"
            ),
            "active_ledger": {
                "U_paid": upper.plane.active.PAID,
                "B_remaining": B_REMAINING,
                "additional_charge": 0,
            },
            "theorem": {
                "source_constraints_independent": True,
                "source_dimension_is_c_plus_two": True,
                "extra_gcd_normalization_preserves_selected_slope": True,
                "reciprocal_dimension_two_emits_c5_owner": True,
                "reciprocal_product_matrix_rank_two": True,
                "minor_quotient_degree_at_most_c": True,
                "saturated_kernel_rank_is_base_span_minus_two": True,
                "saturated_kernel_row_degree_sum_at_most_c": True,
                "saturated_kernel_pointwise_full_rank": True,
                "relation_products_do_not_wrap_when_e_gt_2c": True,
                "moving_root_pair_span_at_most_two": True,
                "direct_cap_is_p_plus_one_times_carrier": True,
                "paid_interval": [R_MIN, R_MAX],
                "first_open_slack": FIRST_OPEN,
            },
            "interval_sweep": interval_sweep(),
            "regressions": {
                "endpoint_cubic_relation": (
                    upper.proper_span_guardrail()
                ),
                "synthetic_saturated_kernel": saturated_kernel_regression(),
            },
            "source_bindings": source_bindings(),
            "upstream_certificates": upstream_bindings(),
            "status": (
                "PROVED_RECIPROCAL_KERNEL_PLANE_SWEEP_"
                "PAID_67475_TO_134942_ZERO_CHARGE_"
                "FIRST_OPEN_134943"
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
        "title": "KoalaBear reciprocal-kernel plane sweep",
        "type": "object",
    }


def check_sources() -> None:
    note = (
        ROOT
        / "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_reciprocal_kernel_plane_sweep_v1.md"
    ).read_text(encoding="utf-8")
    for anchor in [
        "PROVED ZERO-CHARGE PAYMENT ON R=67475..134942",
        "Reciprocal-kernel plane theorem",
        "\\dim_FW_e=2(e+1)-s=c+2",
        "Saturated relation kernel",
        "\\sum_i\\delta_i\\le c",
        "67{,}475\\le r\\le134{,}942",
        "e-2c",
        "2s=3e_{\\max}",
        "# PROVED",
    ]:
        need(anchor in note, f"missing note anchor: {anchor}")


def validate(cert: dict[str, Any], schema: dict[str, Any]) -> None:
    need(cert == expected_certificate(), "certificate differs from exact replay")
    need(schema == expected_schema(), "schema differs from exact replay")
    need(cert["active_ledger"]["additional_charge"] == 0, "zero charge")
    need(
        cert["theorem"]["paid_interval"] == [R_MIN, R_MAX],
        "paid interval",
    )
    need(
        cert["theorem"]["first_open_slack"] == FIRST_OPEN,
        "first open slack",
    )
    need(
        cert["interval_sweep"]["minimum_strict_degree_margin"] == 1,
        "strict endpoint margin",
    )
    check_sources()


def emit() -> None:
    CERT.mkdir(parents=True, exist_ok=True)
    dump(CERT_PATH, expected_certificate())
    dump(SCHEMA_PATH, expected_schema())


def tamper_selftest() -> None:
    cert = expected_certificate()
    schema = expected_schema()
    validate(cert, schema)
    mutations = [
        lambda d: d["active_ledger"].__setitem__("additional_charge", 1),
        lambda d: d["theorem"].__setitem__(
            "source_constraints_independent", False
        ),
        lambda d: d["theorem"].__setitem__(
            "extra_gcd_normalization_preserves_selected_slope", False
        ),
        lambda d: d["theorem"].__setitem__(
            "reciprocal_product_matrix_rank_two", False
        ),
        lambda d: d["theorem"].__setitem__(
            "saturated_kernel_pointwise_full_rank", False
        ),
        lambda d: d["theorem"].__setitem__(
            "relation_products_do_not_wrap_when_e_gt_2c", False
        ),
        lambda d: d["theorem"].__setitem__(
            "paid_interval", [R_MIN, R_MAX + 1]
        ),
        lambda d: d["theorem"].__setitem__(
            "first_open_slack", FIRST_OPEN + 1
        ),
        lambda d: d["interval_sweep"].__setitem__(
            "minimum_strict_degree_margin", 0
        ),
        lambda d: d["interval_sweep"]["first_open"].__setitem__(
            "strict_degree_margin", 1
        ),
        lambda d: d["regressions"]["synthetic_saturated_kernel"].__setitem__(
            "profile_count", 9
        ),
        lambda d: d["upstream_certificates"][
            "post_second_successor_histogram"
        ].__setitem__("payload_sha256", "0" * 64),
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
            sweep = cert["interval_sweep"]
            print(f"architecture: {ARCH}")
            print(f"partition_sha256: {PARTITION_DIGEST}")
            print(f"paid_interval: {[R_MIN, R_MAX]}")
            print(f"paid_count: {PAID_COUNT}")
            print(f"first_open_slack: {FIRST_OPEN}")
            print(f"maximum_direct_cap: {sweep['maximum_direct_cap']}")
            print(f"scan_sha256: {sweep['scan_sha256']}")
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
