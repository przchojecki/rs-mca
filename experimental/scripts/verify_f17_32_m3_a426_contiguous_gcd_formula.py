#!/usr/bin/env python3
"""Verify the A=426 zero-u contiguous-row-set gcd formula."""

from __future__ import annotations

import argparse
import importlib.util
import json
from hashlib import sha256
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experimental.scripts.emit_f17_32_hankel_row_descriptor import (  # noqa: E402
    Field,
    K,
    MODULUS,
    N,
    P,
)


SCHEMA_VERSION = "f17-32-m3-a426-contiguous-gcd-formula-v1"
Q_LINE = 17**32
A = 426
J = N - A
T = A - K
SIZE = J + 1
CONTIGUOUS_COUNT = T - SIZE + 1
ROW_DESCRIPTOR_REF = (
    "experimental/data/certificates/hankel-f17-32-row-descriptor/"
    "f17_32_n512_k256_hankel_row_descriptor.json"
)
A426_INPUT_REF = (
    "experimental/data/hankel-regular-minor-inputs/"
    "f17_32_n512_k256_a426_contiguous_gcd4_input.json"
)
A426_GCD_PACKET_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-contiguous-gcd-a426/"
    "f17_32_n512_k256_a426_contiguous_gcd4_packet.json"
)
PACKET_CHECKER = ROOT / "scripts/check_aperiodic_eliminant_packet.py"
SCHEMA = ROOT / "scripts/aperiodic_eliminant_schema.json"


def load_json(ref: str | Path) -> dict[str, Any]:
    path = ref if isinstance(ref, Path) else ROOT / ref
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(ref: str) -> str:
    return sha256((ROOT / ref).read_bytes()).hexdigest()


def hash_value(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return sha256(payload).hexdigest()


def render(value: dict[str, Any]) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def field_add(field: Field, left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple((a_i + b_i) % field.p for a_i, b_i in zip(left, right))


def field_sub(field: Field, left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple((a_i - b_i) % field.p for a_i, b_i in zip(left, right))


def field_product(field: Field, values: list[tuple[int, ...]]) -> tuple[int, ...]:
    out = field.one
    for value in values:
        out = field.mul(out, value)
    return out


def is_zero(field: Field, value: tuple[int, ...]) -> bool:
    return value == field.zero


def load_packet_checker():
    spec = importlib.util.spec_from_file_location(
        "check_aperiodic_eliminant_packet", PACKET_CHECKER
    )
    require(spec is not None and spec.loader is not None, "could not load packet checker")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def power_sum_encodings(
    field: Field,
    nodes: list[tuple[int, ...]],
    length: int,
) -> list[int]:
    powers = [field.one for _ in nodes]
    out = []
    for _ in range(length):
        total = field.zero
        for power in powers:
            total = field_add(field, total, power)
        out.append(field.encode(total))
        powers = [field.mul(power, node) for power, node in zip(powers, nodes)]
    return out


def vandermonde_square(field: Field, nodes: list[tuple[int, ...]]) -> tuple[int, ...]:
    out = field.one
    for left_index, left in enumerate(nodes):
        for right in nodes[left_index + 1 :]:
            diff = field_sub(field, right, left)
            out = field.mul(out, field.mul(diff, diff))
    return out


def leading_coefficients(
    field: Field,
    nodes: list[tuple[int, ...]],
) -> list[tuple[int, ...]]:
    base = vandermonde_square(field, nodes)
    node_product = field_product(field, nodes)
    out = []
    scale = field.one
    for _ in range(CONTIGUOUS_COUNT):
        out.append(field.mul(base, scale))
        scale = field.mul(scale, node_product)
    return out


def validate_packet_against_formula(
    checker: Any,
    packet: dict[str, Any],
    leading_encoded: list[int],
) -> dict[str, Any]:
    checker.check_path(ROOT / A426_GCD_PACKET_REF, SCHEMA)
    require(packet["agreement_threshold"] == A, "packet threshold mismatch")
    require(packet["root_union"] == [0], "packet root union mismatch")
    require(packet["declared_aperiodic_numerator"] == 1, "packet numerator mismatch")
    require(len(packet["exact_agreements"]) == 1, "packet should have one exact agreement")
    item = packet["exact_agreements"][0]
    require(item["A"] == A and item["j"] == J and item["t"] == T, "packet row mismatch")
    gcd = item["regular_minor_gcd"]
    data = item["regular_minor_gcd_data"]
    require(gcd["minor_count"] == 4, "packet should audit four row sets")
    require(data["roots"] == [0], "packet gcd roots mismatch")
    require(data["gcd_coefficients_ascending"] == [0] * SIZE + [1], "packet gcd mismatch")

    for index, record in enumerate(data["minor_polynomials_ascending"]):
        expected_row_set = list(range(index, index + SIZE))
        require(record["row_set"] == expected_row_set, f"packet row set {index} mismatch")
        expected_coefficients = [0] * SIZE + [leading_encoded[index]]
        require(
            record["coefficients"] == expected_coefficients,
            f"packet coefficients {index} mismatch formula",
        )

    return {
        "packet_checked_by_schema_checker": True,
        "packet_minor_count": gcd["minor_count"],
        "packet_row_starts": list(range(gcd["minor_count"])),
        "packet_matches_formula_prefix": True,
    }


def build_certificate() -> dict[str, Any]:
    field = Field(P, MODULUS)
    descriptor = load_json(ROW_DESCRIPTOR_REF)
    input_data = load_json(A426_INPUT_REF)
    packet = load_json(A426_GCD_PACKET_REF)

    require(descriptor["row"]["n"] == N, "descriptor n mismatch")
    require(descriptor["row"]["k"] == K, "descriptor k mismatch")
    require(descriptor["row"]["field"] == "F_17^32", "descriptor field mismatch")
    require(descriptor["row"]["field_order"] == Q_LINE, "descriptor q mismatch")
    require(input_data["agreement_threshold"] == A, "input threshold mismatch")
    require(input_data["exact_agreements"] == [A], "input exact agreement mismatch")
    require(input_data["certificate_mode"] == "minor_gcd_roots", "input mode mismatch")
    require(input_data["minor_gcd_method"] == "zero_u_monomial", "input gcd method mismatch")
    require(
        input_data["row_set_strategy"] == {"type": "contiguous", "limit": 4},
        "input row-set strategy mismatch",
    )

    domain_encodings = descriptor["domain"]["domain_encodings"]
    require(input_data["row"]["domain_hash"] == descriptor["row"]["domain_hash"], "domain hash mismatch")
    nodes = [field.decode(value) for value in domain_encodings[:SIZE]]
    require(len(set(domain_encodings[:SIZE])) == SIZE, "support nodes not distinct")
    require(all(not is_zero(field, node) for node in nodes), "support contains zero")

    u_syndrome = input_data["line_syndrome"]["u"]
    v_syndrome = input_data["line_syndrome"]["v"]
    require(len(u_syndrome) == N - K and len(v_syndrome) == N - K, "syndrome length mismatch")
    require(all(value == 0 for value in u_syndrome), "u syndrome is not zero")
    require(
        power_sum_encodings(field, nodes, N - K) == v_syndrome,
        "v syndrome is not the first-87-node power-sum syndrome",
    )

    vander = vandermonde_square(field, nodes)
    product = field_product(field, nodes)
    leading = leading_coefficients(field, nodes)
    leading_encoded = [field.encode(value) for value in leading]
    require(not is_zero(field, vander), "Vandermonde square vanished")
    require(not is_zero(field, product), "node product vanished")
    require(all(not is_zero(field, value) for value in leading), "some contiguous leading coefficient vanished")

    packet_audit = validate_packet_against_formula(
        load_packet_checker(),
        packet,
        leading_encoded,
    )

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT for the synthetic A=426 zero-u pencil",
        "object": "all-contiguous-row-set common-gcd formula at A=426",
        "row": {
            "code": "RS[F_17^32,H,256]",
            "n": N,
            "k": K,
            "field": "F_17^32",
            "domain_hash": descriptor["row"]["domain_hash"],
            "q_line": Q_LINE,
        },
        "source_artifacts": {
            "row_descriptor": {"ref": ROW_DESCRIPTOR_REF, "sha256": sha256_file(ROW_DESCRIPTOR_REF)},
            "input": {"ref": A426_INPUT_REF, "sha256": sha256_file(A426_INPUT_REF)},
            "bounded_gcd_packet": {
                "ref": A426_GCD_PACKET_REF,
                "sha256": sha256_file(A426_GCD_PACKET_REF),
            },
        },
        "parameters": {
            "A": A,
            "j": J,
            "t": T,
            "minor_size": SIZE,
            "contiguous_row_start_min": 0,
            "contiguous_row_start_max": CONTIGUOUS_COUNT - 1,
            "contiguous_row_set_count": CONTIGUOUS_COUNT,
            "support_node_count": SIZE,
        },
        "formula": {
            "support": "X = first 87 descriptor-domain elements",
            "syndrome": "u_m=0, v_m=sum_{x in X} x^m",
            "row_set": "R_s={s,s+1,...,s+86}",
            "factorization": "det(v_{s+a+b})_{0<=a,b<87} = (prod_{x in X} x)^s * Vandermonde(X)^2",
            "determinant_polynomial": "Delta_s(Z)=c_s Z^87",
            "common_gcd": "gcd_s Delta_s(Z) = Z^87, made monic",
        },
        "field_audit": {
            "support_nodes_distinct": True,
            "support_nodes_nonzero": True,
            "vandermonde_square_encoding": field.encode(vander),
            "support_product_encoding": field.encode(product),
            "leading_coefficients_nonzero": True,
            "leading_coefficients_hash": hash_value(leading_encoded),
            "first_four_leading_coefficients": leading_encoded[:4],
            "last_leading_coefficient": leading_encoded[-1],
        },
        "common_gcd": {
            "coefficients_ascending": [0] * SIZE + [1],
            "degree": SIZE,
            "roots": [0],
            "root_certificate": {
                "kind": "split_linear_factorization",
                "leading_coefficient": 1,
                "field_encoding": "base-p low-to-high integer",
                "factors": [{"root": 0, "multiplicity": SIZE}],
            },
            "raw_aperiodic_numerator_before_subtraction": 1,
            "tangent_paid_roots": [0],
            "residual_aperiodic_numerator_after_tangent": 0,
        },
        "bounded_packet_audit": packet_audit,
        "checks": [
            "input u syndrome is identically zero",
            "input v syndrome matches first-87-node power sums",
            "all 84 contiguous leading coefficients are nonzero",
            "common gcd over the all-contiguous subatlas is monic Z^87",
            "stored bounded gcd packet matches the first four formula rows",
        ],
        "nonclaims": [
            "only the contiguous row-set subatlas at A=426",
            "not the all-maximal-minor canonical gcd over every row set",
            "not a worst-case support-wise MCA row bound",
            "not a singular-bucket classification",
        ],
    }


def check_certificate(path: Path) -> None:
    expected = render(build_certificate())
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"A=426 contiguous-gcd formula certificate mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    params = certificate["parameters"]
    print("F_17^32 M3 A=426 contiguous-gcd formula")
    print(
        "row starts {contiguous_row_start_min}..{contiguous_row_start_max}, count={contiguous_row_set_count}".format(
            **params
        )
    )
    print("common gcd: Z^87, roots={0}, residual after tangent=0")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", type=Path)
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()

    certificate = build_certificate()
    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(render(certificate), encoding="utf-8")
    if args.check:
        check_certificate(args.check)
    print_summary(certificate)


if __name__ == "__main__":
    main()
