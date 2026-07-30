#!/usr/bin/env python3
"""Verify the order-two source-subfield and coefficient compiler packet."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any, Callable

if not __debug__:
    raise RuntimeError("verifier refuses optimized Python execution")


class VerificationError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


EXPERIMENTAL = Path(__file__).resolve().parents[1]
REPO_ROOT = EXPERIMENTAL.parent
CERTIFICATE = (
    EXPERIMENTAL
    / "data/certificates/kb-mca-v4-m2-r4-order2-source-subfield-coefficient-compilers-v1"
    / "kb_mca_v4_m2_r4_order2_source_subfield_coefficient_compilers_v1.json"
)
PARENT = {
    "commit": "77b0971ebb443efd8487ee3809cd988ba183d00c",
    "note_path": "experimental/notes/frontier-adjacent/kb_mca_v4_m2_r4_order2_source_facet_interpolation_v1.md",
    "note_blob_oid": "a74eb30e46d8941c1cc4c598b2fdff6a3daad657",
    "verifier_path": "experimental/scripts/verify_kb_mca_v4_m2_r4_order2_source_facet_interpolation_v1.py",
    "verifier_blob_oid": "8c1fd1318b180f27a3114a3a3beedd7e2ed3efbd",
    "certificate_path": "experimental/data/certificates/kb-mca-v4-m2-r4-order2-source-facet-interpolation-v1/kb_mca_v4_m2_r4_order2_source_facet_interpolation_v1.json",
    "certificate_blob_oid": "c0f6f9496e4bf43b60358133372ce47bc9b5c8dd",
    "certificate_payload_sha256": "96c47c813c41f4b268b9826ed4866e14d44c5a8187487266a3de6f550cbbf6b6",
    "terminal": "M2_R4_ORDER_TWO_SOURCE_FACET_AND_DIAGONAL_INTERPOLATION_INTERFACES",
}


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def payload_hash(value: dict[str, Any]) -> str:
    unhashed = copy.deepcopy(value)
    unhashed.pop("payload_sha256", None)
    return hashlib.sha256(canonical_json(unhashed).encode()).hexdigest()


def reject_duplicates(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise VerificationError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def parse_json(text: str, label: str) -> dict[str, Any]:
    try:
        value = json.loads(text, object_pairs_hook=reject_duplicates)
    except (json.JSONDecodeError, VerificationError) as error:
        raise VerificationError(f"cannot parse {label}: {error}") from error
    require(isinstance(value, dict), f"{label} is not an object")
    return value


def git_output(*args: str) -> str:
    try:
        result = subprocess.run(
            ["git", *args], cwd=REPO_ROOT, check=True, capture_output=True, text=True
        )
    except subprocess.CalledProcessError as error:
        raise VerificationError(error.stderr.strip()) from error
    return result.stdout.strip()


def load_parent() -> dict[str, Any]:
    for path_key, blob_key in (
        ("note_path", "note_blob_oid"),
        ("verifier_path", "verifier_blob_oid"),
        ("certificate_path", "certificate_blob_oid"),
    ):
        require(
            git_output("rev-parse", f"{PARENT['commit']}:{PARENT[path_key]}")
            == PARENT[blob_key],
            f"parent blob {PARENT[path_key]}",
        )
    data = parse_json(
        git_output("show", f"{PARENT['commit']}:{PARENT['certificate_path']}"),
        PARENT["certificate_path"],
    )
    require(data.get("payload_sha256") == PARENT["certificate_payload_sha256"],
            "parent payload")
    require(payload_hash(data) == data.get("payload_sha256"), "parent seal")
    require(data["conclusion"]["terminal"] == PARENT["terminal"], "parent terminal")
    require(data["conclusion"]["order_two_type_deleted"] is False, "parent scope")
    return data


def orbit_dimensions(rows: int, columns: int) -> tuple[int, int]:
    fixed = sum(
        (i, j) == (rows - 1 - i, columns - 1 - j)
        for i in range(rows)
        for j in range(columns)
    )
    total = rows * columns
    return ((total + fixed) // 2, (total - fixed) // 2)


def subfield_replay() -> dict[str, Any]:
    u_dims = orbit_dimensions(3, 3)
    v_dims = orbit_dimensions(3, 2)
    source_dims = [u_dims[0] + v_dims[0], u_dims[1] + v_dims[1]]
    passports = []
    for genus in range(4):
        fixed_eta = 2 * genus + 2
        fixed_mu = 2 * genus + 6 - 2 * fixed_eta
        if fixed_mu >= 0:
            passports.append({
                "genus": genus,
                "fixed_eta": fixed_eta,
                "fixed_eta_prime": fixed_eta,
                "fixed_mu": fixed_mu,
                "branch_orbits": [fixed_eta // 2, fixed_eta // 2, fixed_mu // 2],
            })
    require(source_dims == [8, 7], "source dimensions")
    require(passports == [
        {"genus": 0, "fixed_eta": 2, "fixed_eta_prime": 2,
         "fixed_mu": 2, "branch_orbits": [1, 1, 1]},
        {"genus": 1, "fixed_eta": 4, "fixed_eta_prime": 4,
         "fixed_mu": 0, "branch_orbits": [2, 2, 0]},
    ], "low-genus passports")
    return {
        "source_line_coordinates": {
            "b": "-X", "s": "1/X", "psi": "X^2", "tau": "1/Z"
        },
        "U_eigenspace_dimensions": list(u_dims),
        "V_eigenspace_dimensions": list(v_dims),
        "source_eigenspace_dimensions": source_dims,
        "biquadratic_passports": passports,
    }


def coordinate_replay() -> dict[str, Any]:
    monomials = [(i, j) for i in range(3) for j in range(5)]
    positive = [(i, j) for i, j in monomials if (i + j) % 2 == 0]
    negative = [(i, j) for i, j in monomials if (i + j) % 2 == 1]
    plus_even = [(i, j) for i in (0, 2) for j in range(3)]
    plus_odd = [(1, j) for j in range(2)]
    minus_even = [(1, j) for j in range(3)]
    minus_odd = [(i, j) for i in (0, 2) for j in range(2)]
    require((len(positive), len(negative)) == (8, 7), "coordinate dimensions")
    require((len(plus_even) + len(plus_odd),
             len(minus_even) + len(minus_odd)) == (8, 7),
            "coordinate even-odd forms")
    return {
        "coordinates": {"tau": "-T", "b": "-X", "psi": "X^2"},
        "source_eigenspace_dimensions": [len(positive), len(negative)],
        "positive_form": "A_2(W)T^2+A_0(W)+XT B_1(W)",
        "negative_form": "T A_1(W)+X(B_2(W)T^2+B_0(W))",
        "deck_odd_part_required_nonzero": True,
        "endpoint_norm": "G=U^2-WV^2",
        "endpoint_even_in_T": True,
    }


def poly_mul(left: list[int], right: list[int]) -> list[int]:
    out = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            out[i + j] += a * b
    return out


def poly_eval(poly: list[int], value: int) -> int:
    return sum(coefficient * value**degree for degree, coefficient in enumerate(poly))


def resolvent_replay() -> dict[str, Any]:
    rows = []
    for roots in ((1, 2, 4, 8), (-3, 2, 5, 11), (2, 7, 13, 19)):
        quartic = [1]
        for root in roots:
            quartic = poly_mul(quartic, [-root, 1])
        d, c, b, a, leading = quartic
        require(leading == 1, "monic quartic")
        resolvent = [4 * b * d - a * a * d - c * c, a * c - 4 * d, -b, 1]
        pair_roots = [
            roots[0] * roots[1] + roots[2] * roots[3],
            roots[0] * roots[2] + roots[1] * roots[3],
            roots[0] * roots[3] + roots[1] * roots[2],
        ]
        require(len(set(pair_roots)) == 3, "distinct resolvent roots")
        require(all(poly_eval(resolvent, value) == 0 for value in pair_roots),
                "resolvent formula")
        rows.append({"quartic": quartic, "resolvent": resolvent,
                     "resolvent_roots": pair_roots})
    return {
        "formula": "Y^3-bY^2+(ac-4d)Y+(4bd-a^2d-c^2)",
        "rows": rows,
        "rows_sha256": hashlib.sha256(canonical_json(rows).encode()).hexdigest(),
    }


def inverse(value: int, prime: int) -> int:
    return pow(value % prime, prime - 2, prime)


def source_interpolation_replay() -> dict[str, Any]:
    prime = 101
    labels = list(range(12))
    weights = []
    for i, value in enumerate(labels):
        denominator = 1
        for j, other in enumerate(labels):
            if i != j:
                denominator = denominator * (value - other) % prime
        weights.append(inverse(denominator, prime))
    parity = [
        [weights[i] * pow(labels[i], degree, prime) % prime for i in range(12)]
        for degree in range(9)
    ]
    coefficients = [
        [(13 * a + 17 * b + 7 * a * b + 5) % prime for a in range(3)]
        for b in range(5)
    ]
    scales = [(19 * i + 3) % prime or 1 for i in labels]
    rows = [
        [
            sum(coefficients[b][a] * pow(value, a, prime) for a in range(3))
            * inverse(scales[i], prime) % prime
            for b in range(5)
        ]
        for i, value in enumerate(labels)
    ]
    matrix = [
        [check[i] * rows[i][b] % prime for i in range(12)]
        for b in range(5)
        for check in parity
    ]
    residual = [sum(row[i] * scales[i] for i in range(12)) % prime
                for row in matrix]
    require(len(matrix) == 45 and all(len(row) == 12 for row in matrix),
            "source matrix dimensions")
    require(residual == [0] * 45 and all(scales), "source full-support kernel")
    return {
        "field": prime,
        "parity_rows": 9,
        "quartic_coefficients": 5,
        "matrix_rows": 45,
        "matrix_columns": 12,
        "kernel_full_support": True,
        "kernel_residual": residual,
        "matrix_sha256": hashlib.sha256(canonical_json(matrix).encode()).hexdigest(),
    }


def expected_certificate() -> dict[str, Any]:
    data = {
        "schema": "kb-mca-v4-m2-r4-order2-source-subfield-coefficient-compilers-v1",
        "parent": PARENT,
        "source_subfield_dichotomy": {
            "exhaustive_branches": ["source_line_lift", "biquadratic_W_cover"],
            "individual_star_transport_only_in_source_line_branch": True,
            "function_field_V4_is_ambient_stabilizer_V4": False,
            "replay": subfield_replay(),
        },
        "coordinate_coefficient_normal_form": coordinate_replay(),
        "branch_coefficient_compiler": {
            "source_line_norm": "G=U^2-WV^2",
            "endpoint_reciprocal_sign": "+1",
            "biquadratic_test": "monic quartic cubic resolvent splits completely over K(W)",
            "replay": resolvent_replay(),
        },
        "source_row_interpolation": {
            "equivalence": "full-support kernel iff unique bidegree-at-most-(2,4) source interpolant",
            "complete_source_product": "product_i q_i is proportional to B^2",
            "complete_source_resultant": "Res_T(A,H) is proportional to B^2",
            "replay": source_interpolation_replay(),
        },
        "conclusion": {
            "order_two_type_deleted": False,
            "coordinate_orientation_deleted": False,
            "diagonal_orientation_deleted": False,
            "k3_status": "OPEN",
            "koalabear_row_status": "OPEN",
            "terminal": "M2_R4_ORDER_TWO_SOURCE_SUBFIELD_AND_COEFFICIENT_COMPILERS",
        },
        "nonclaims": [
            "no universal source-row kernel, reciprocal-norm, or split-resolvent failure",
            "no exact-degree, irreducibility, or outer-factor conclusion for a passing interpolant",
            "no deletion of an order-two subgroup or the trivial m2 type",
            "no carrier, data, explaining-polynomial, slope owner, or payment",
            "no K3, KoalaBear row, endpoint, or Prize close",
        ],
    }
    data["payload_sha256"] = payload_hash(data)
    return data


def verify_data(data: dict[str, Any]) -> None:
    require(payload_hash(data) == data.get("payload_sha256"), "certificate seal")
    require(data == expected_certificate(), "certificate content")


def tamper_selftest(data: dict[str, Any]) -> int:
    mutations: list[Callable[[dict[str, Any]], None]] = [
        lambda x: x["source_subfield_dichotomy"].__setitem__("exhaustive_branches", ["source_line_lift"]),
        lambda x: x["source_subfield_dichotomy"].__setitem__("individual_star_transport_only_in_source_line_branch", False),
        lambda x: x["source_subfield_dichotomy"].__setitem__("function_field_V4_is_ambient_stabilizer_V4", True),
        lambda x: x["source_subfield_dichotomy"]["replay"].__setitem__("source_eigenspace_dimensions", [9, 6]),
        lambda x: x["source_subfield_dichotomy"]["replay"]["biquadratic_passports"][0].__setitem__("fixed_mu", 0),
        lambda x: x["coordinate_coefficient_normal_form"].__setitem__("source_eigenspace_dimensions", [9, 6]),
        lambda x: x["coordinate_coefficient_normal_form"].__setitem__("deck_odd_part_required_nonzero", False),
        lambda x: x["coordinate_coefficient_normal_form"].__setitem__("endpoint_even_in_T", False),
        lambda x: x["branch_coefficient_compiler"].__setitem__("endpoint_reciprocal_sign", "-1"),
        lambda x: x["branch_coefficient_compiler"].__setitem__("source_line_norm", "G=U^2+WV^2"),
        lambda x: x["branch_coefficient_compiler"]["replay"].__setitem__("rows_sha256", "0" * 64),
        lambda x: x["source_row_interpolation"]["replay"].__setitem__("matrix_rows", 44),
        lambda x: x["source_row_interpolation"]["replay"].__setitem__("kernel_full_support", False),
        lambda x: x["source_row_interpolation"].__setitem__("complete_source_product", "product_i q_i is B^3"),
        lambda x: x["conclusion"].__setitem__("order_two_type_deleted", True),
        lambda x: x["conclusion"].__setitem__("k3_status", "CLOSED"),
        lambda x: x["parent"].__setitem__("certificate_payload_sha256", "0" * 64),
        lambda x: x.__setitem__("payload_sha256", "0" * 64),
    ]
    rejected = 0
    for mutation in mutations:
        hostile = copy.deepcopy(data)
        mutation(hostile)
        try:
            verify_data(hostile)
        except VerificationError:
            rejected += 1
    require(rejected == len(mutations), "tamper self-test")
    return rejected


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()

    load_parent()
    expected = expected_certificate()
    if args.write:
        CERTIFICATE.parent.mkdir(parents=True, exist_ok=True)
        CERTIFICATE.write_text(json.dumps(expected, indent=2, sort_keys=True) + "\n")
    if args.check or not args.write:
        require(CERTIFICATE.is_file(), "missing certificate")
        data = parse_json(CERTIFICATE.read_text(), str(CERTIFICATE))
        verify_data(data)
    else:
        data = expected
    rejected = tamper_selftest(data) if args.tamper_selftest else 0
    print(
        "KB_MCA_V4_M2_R4_ORDER2_SOURCE_SUBFIELD_COEFFICIENT_COMPILERS_PASS "
        f"coordinate_dims={data['coordinate_coefficient_normal_form']['source_eigenspace_dimensions']} "
        f"diagonal_dims={data['source_subfield_dichotomy']['replay']['source_eigenspace_dimensions']} "
        f"source_matrix={data['source_row_interpolation']['replay']['matrix_rows']}x"
        f"{data['source_row_interpolation']['replay']['matrix_columns']} "
        f"tamper_rejected={rejected}"
    )


if __name__ == "__main__":
    main()
