#!/usr/bin/env python3
"""Verify the subgroup inverse-Fourier section for RS syndromes.

For a multiplicative subgroup H of order n, the RS dual weights are

    lambda_x = x / n.

Hence every syndrome vector s_0,...,s_{r-1}, r <= n, has the explicit section

    y_s(x) = sum_m s_m x^(-m-1),

because Syn(y_s)_a = n^{-1} sum_m s_m sum_{x in H} x^(a-m) = s_a.

This verifier records the theorem and replays it on a small prime-field row and
on the pinned F_17^32 M3 fixed top-window packet.
"""

from __future__ import annotations

import argparse
import json
from hashlib import sha256
from pathlib import Path
import sys
from typing import Any, Protocol


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from experimental.scripts.emit_f17_32_hankel_row_descriptor import (  # noqa: E402
    Field,
    MODULUS,
    P,
)


SCHEMA_VERSION = "subgroup-syndrome-section-v1"
ROW_DESCRIPTOR_REF = (
    "experimental/data/certificates/hankel-f17-32-row-descriptor/"
    "f17_32_n512_k256_hankel_row_descriptor.json"
)
FIXED_INPUT_REF = (
    "experimental/data/hankel-regular-minor-inputs/"
    "f17_32_n512_k256_a421_426_fixed_prefix92_input.json"
)
LINE_VALUE_LIFT_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-line-value-lift/"
    "f17_32_n512_k256_a421_426_fixed_prefix92_line_values.json"
)
OUTPUT_PATH = REPO_ROOT / (
    "experimental/data/certificates/subgroup-syndrome-section/"
    "subgroup_syndrome_section_certificate.json"
)


class FieldOps(Protocol):
    size: int
    zero: Any
    one: Any

    def normalize(self, value: Any) -> Any: ...
    def encode(self, value: Any) -> int: ...
    def decode(self, value: int) -> Any: ...
    def add(self, left: Any, right: Any) -> Any: ...
    def mul(self, left: Any, right: Any) -> Any: ...
    def pow(self, value: Any, exponent: int) -> Any: ...


class PrimeField:
    def __init__(self, prime: int):
        self.p = prime
        self.size = prime
        self.zero = 0
        self.one = 1

    def normalize(self, value: Any) -> int:
        return int(value) % self.p

    def encode(self, value: Any) -> int:
        return self.normalize(value)

    def decode(self, value: int) -> int:
        if value < 0 or value >= self.p:
            raise ValueError("encoded prime-field element outside field range")
        return value

    def add(self, left: Any, right: Any) -> int:
        return (self.normalize(left) + self.normalize(right)) % self.p

    def mul(self, left: Any, right: Any) -> int:
        return (self.normalize(left) * self.normalize(right)) % self.p

    def pow(self, value: Any, exponent: int) -> int:
        return pow(self.normalize(value), exponent, self.p)


class ExtensionField:
    def __init__(self, field: Field):
        self.field = field
        self.size = field.size
        self.zero = field.zero
        self.one = field.one

    def normalize(self, value: Any) -> tuple[int, ...]:
        return self.field.normalize(value)

    def encode(self, value: Any) -> int:
        return self.field.encode(value)

    def decode(self, value: int) -> tuple[int, ...]:
        return self.field.decode(value)

    def add(self, left: Any, right: Any) -> tuple[int, ...]:
        a = self.normalize(left)
        b = self.normalize(right)
        return tuple((a[index] + b[index]) % self.field.p for index in range(self.field.degree))

    def mul(self, left: Any, right: Any) -> tuple[int, ...]:
        return self.field.mul(left, right)

    def pow(self, value: Any, exponent: int) -> tuple[int, ...]:
        return self.field.pow(value, exponent)


def render(value: dict[str, Any]) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def load_json(ref: str | Path) -> dict[str, Any]:
    path = Path(ref)
    if not path.is_absolute():
        path = REPO_ROOT / path
    return json.loads(path.read_text(encoding="utf-8"))


def hash_json(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return sha256(payload).hexdigest()


def sha256_file(ref: str) -> str:
    return sha256((REPO_ROOT / ref).read_bytes()).hexdigest()


def inv(field: FieldOps, value: Any) -> Any:
    value = field.normalize(value)
    if value == field.zero:
        raise ZeroDivisionError("division by zero")
    return field.pow(value, field.size - 2)


def subgroup_weights(field: FieldOps, domain: list[Any]) -> list[Any]:
    inv_order = inv(field, len(domain))
    weights = [field.mul(point, inv_order) for point in domain]
    for point, weight in zip(domain, weights):
        derivative = field.mul(field.normalize(len(domain)), field.pow(point, len(domain) - 1))
        if field.mul(weight, derivative) != field.one:
            raise AssertionError("lambda_x=x/n dual-weight identity failed")
    return weights


def section_values(field: FieldOps, domain: list[Any], syndrome: list[Any]) -> list[Any]:
    values = []
    order = len(domain)
    for point in domain:
        inverse = field.pow(point, order - 1)
        power = inverse
        total = field.zero
        for moment in syndrome:
            total = field.add(total, field.mul(moment, power))
            power = field.mul(power, inverse)
        values.append(total)
    return values


def replay_syndrome(
    field: FieldOps,
    domain: list[Any],
    weights: list[Any],
    values: list[Any],
    length: int,
) -> list[Any]:
    powers = [field.one for _ in domain]
    out = []
    for _ in range(length):
        total = field.zero
        for point_power, weight, value in zip(powers, weights, values):
            total = field.add(total, field.mul(field.mul(weight, point_power), value))
        out.append(total)
        powers = [field.mul(power, point) for power, point in zip(powers, domain)]
    return out


def encoded(field: FieldOps, values: list[Any]) -> list[int]:
    return [field.encode(value) for value in values]


def check_case(field: FieldOps, domain: list[Any], syndrome: list[Any]) -> dict[str, Any]:
    if len(syndrome) > len(domain):
        raise ValueError("section theorem needs syndrome length <= subgroup order")
    weights = subgroup_weights(field, domain)
    values = section_values(field, domain, syndrome)
    replay = replay_syndrome(field, domain, weights, values, len(syndrome))
    return {
        "subgroup_order": len(domain),
        "syndrome_length": len(syndrome),
        "weights_hash": hash_json(encoded(field, weights)),
        "section_values_hash": hash_json(encoded(field, values)),
        "target_syndrome_hash": hash_json(encoded(field, syndrome)),
        "replayed_syndrome_hash": hash_json(encoded(field, replay)),
        "section_replays_syndrome": replay == syndrome,
    }


def prime_case() -> dict[str, Any]:
    field = PrimeField(17)
    domain = list(range(1, 17))
    syndrome = [
        (3 + 5 * index + 2 * index * index + index * index * index) % 17
        for index in range(8)
    ]
    check = check_case(field, domain, syndrome)
    if not check["section_replays_syndrome"]:
        raise AssertionError("prime subgroup section failed")
    return {
        "name": "F17_star_order16",
        "field": "F_17",
        "domain_description": "F_17^*",
        "status": "PASS",
        **check,
    }


def f17_32_case() -> dict[str, Any]:
    descriptor = load_json(ROW_DESCRIPTOR_REF)
    fixed_input = load_json(FIXED_INPUT_REF)
    line_lift = load_json(LINE_VALUE_LIFT_REF)
    field = ExtensionField(Field(P, MODULUS))
    domain = [field.decode(value) for value in descriptor["domain"]["domain_encodings"]]
    u_syndrome = [field.decode(value) for value in fixed_input["line_syndrome"]["u"]]
    v_syndrome = [field.decode(value) for value in fixed_input["line_syndrome"]["v"]]
    u_check = check_case(field, domain, u_syndrome)
    v_check = check_case(field, domain, v_syndrome)
    if not u_check["section_replays_syndrome"] or not v_check["section_replays_syndrome"]:
        raise AssertionError("F17^32 subgroup section failed")
    if u_check["section_values_hash"] != line_lift["line_values"]["f_hash"]:
        raise AssertionError("F17^32 u-section hash disagrees with line-value lift")
    if v_check["section_values_hash"] != line_lift["line_values"]["g_hash"]:
        raise AssertionError("F17^32 v-section hash disagrees with line-value lift")
    return {
        "name": "F17_32_H512_fixed_top_window",
        "field": "F_17^32",
        "domain_hash": descriptor["row"]["domain_hash"],
        "fixed_top_window_input_ref": FIXED_INPUT_REF,
        "fixed_top_window_input_sha256": sha256_file(FIXED_INPUT_REF),
        "line_value_lift_ref": LINE_VALUE_LIFT_REF,
        "line_value_lift_sha256": sha256_file(LINE_VALUE_LIFT_REF),
        "status": "PASS",
        "u_section": u_check,
        "v_section": v_check,
    }


def build_certificate() -> dict[str, Any]:
    cases = [prime_case(), f17_32_case()]
    if any(case["status"] != "PASS" for case in cases):
        raise AssertionError("subgroup syndrome-section case failed")
    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT",
        "theorem": {
            "statement": (
                "For a multiplicative subgroup H of order n and any r <= n, "
                "the weighted Reed-Solomon syndrome map Syn:F^H -> F^r has "
                "the explicit section y_s(x)=sum_{m<r} s_m x^(-m-1)."
            ),
            "dual_weight_formula": "lambda_x = 1 / prod_{y!=x}(x-y) = x/n",
            "section_formula": "y_s(x)=sum_{0<=m<r} s_m x^(-m-1)",
            "orthogonality": "sum_{x in H} x^a is n if a=0 mod n and 0 otherwise",
            "hypotheses": [
                "H is a finite multiplicative subgroup of F^*",
                "r <= |H|",
                "the field characteristic does not divide |H|",
            ],
        },
        "cases": cases,
        "nonclaims": [
            "does not prove a worst-case MCA bound",
            "does not classify quotient, tangent, or extension residuals",
            "does not compute actual-row root tables",
        ],
    }


def check_certificate(path: Path) -> None:
    expected = render(build_certificate())
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"subgroup syndrome-section certificate mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    print("subgroup syndrome-section theorem")
    for case in certificate["cases"]:
        print(f"{case['name']}: {case['status']}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", type=Path, help="write deterministic certificate JSON")
    parser.add_argument("--check", type=Path, help="check deterministic certificate JSON")
    parser.add_argument("--json", action="store_true", help="print certificate JSON")
    args = parser.parse_args()

    certificate = build_certificate()
    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(render(certificate), encoding="utf-8")
    if args.check:
        check_certificate(args.check)
    if args.json:
        print(render(certificate), end="")
        return
    print_summary(certificate)


if __name__ == "__main__":
    main()
