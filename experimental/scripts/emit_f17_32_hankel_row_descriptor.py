#!/usr/bin/env python3
"""Emit the canonical F_17^32 Hankel row/domain descriptor for M3.

The regular-window extractor needs more than the prose row label
``RS[F_17^32,H,256]``.  This script pins the polynomial-basis field model, the
order-512 multiplicative subgroup generator, the encoded domain, and the domain
hash future v9 packets should reference.
"""

from __future__ import annotations

import argparse
import json
from hashlib import sha256
from pathlib import Path
import sys
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.check_aperiodic_eliminant_packet import is_irreducible_mod_prime


P = 17
DEGREE = 32
N = 512
K = 256
SUBGROUP_ORDER = 512
TWO128 = 2**128

# Same pinned modulus as experimental/scripts/verify_v1_f17_32_algebra_checker.py,
# converted from high-degree-first to low-degree-first coefficient order.
MODULUS_HIGH_TO_LOW = [
    1,
    14,
    0,
    4,
    4,
    2,
    0,
    2,
    14,
    7,
    5,
    5,
    12,
    6,
    11,
    11,
    7,
    6,
    1,
    12,
    3,
    9,
    3,
    4,
    5,
    9,
    11,
    3,
    13,
    5,
    8,
    7,
    16,
]
MODULUS = list(reversed(MODULUS_HIGH_TO_LOW))


class Field:
    def __init__(self, prime: int, modulus: list[int]):
        self.p = prime
        self.modulus = [coeff % prime for coeff in modulus]
        self.degree = len(modulus) - 1
        self.size = prime**self.degree
        self.zero = (0,) * self.degree
        self.one = (1,) + (0,) * (self.degree - 1)

    def normalize(self, value: Any) -> tuple[int, ...]:
        if isinstance(value, int):
            coeffs = [value % self.p]
        else:
            coeffs = [int(entry) % self.p for entry in value]
        if len(coeffs) > self.degree:
            raise ValueError("too many coefficients")
        coeffs += [0] * (self.degree - len(coeffs))
        return tuple(coeffs)

    def encode(self, value: Any) -> int:
        elem = self.normalize(value)
        total = 0
        place = 1
        for coeff in elem:
            total += coeff * place
            place *= self.p
        return total

    def decode(self, value: int) -> tuple[int, ...]:
        if value < 0 or value >= self.size:
            raise ValueError("encoded element outside field range")
        coeffs = []
        remaining = value
        for _ in range(self.degree):
            coeffs.append(remaining % self.p)
            remaining //= self.p
        return tuple(coeffs)

    def mul(self, left: Any, right: Any) -> tuple[int, ...]:
        a = self.normalize(left)
        b = self.normalize(right)
        coeffs = [0] * (2 * self.degree - 1)
        for i, a_i in enumerate(a):
            for j, b_j in enumerate(b):
                coeffs[i + j] = (coeffs[i + j] + a_i * b_j) % self.p
        for deg in range(len(coeffs) - 1, self.degree - 1, -1):
            lead = coeffs[deg] % self.p
            if not lead:
                continue
            offset = deg - self.degree
            for index, coeff in enumerate(self.modulus):
                coeffs[offset + index] = (
                    coeffs[offset + index] - lead * coeff
                ) % self.p
        return tuple(coeffs[: self.degree])

    def pow(self, value: Any, exponent: int) -> tuple[int, ...]:
        out = self.one
        base = self.normalize(value)
        while exponent:
            if exponent & 1:
                out = self.mul(out, base)
            base = self.mul(base, base)
            exponent >>= 1
        return out


def hash_json(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return sha256(payload).hexdigest()


def v2(value: int) -> int:
    count = 0
    while value % 2 == 0:
        count += 1
        value //= 2
    return count


def ceil_div(numerator: int, denominator: int) -> int:
    return -(-numerator // denominator)


def find_generator(field: Field) -> tuple[tuple[int, ...], int]:
    exponent = (field.size - 1) // SUBGROUP_ORDER
    for witness in range(2, 10000):
        candidate = field.pow(field.decode(witness), exponent)
        if (
            field.pow(candidate, SUBGROUP_ORDER) == field.one
            and field.pow(candidate, SUBGROUP_ORDER // 2) != field.one
        ):
            return candidate, witness
    raise RuntimeError("failed to find order-512 generator")


def subgroup_encodings(field: Field, generator: tuple[int, ...]) -> list[int]:
    out = []
    current = field.one
    for _ in range(SUBGROUP_ORDER):
        out.append(field.encode(current))
        current = field.mul(current, generator)
    if current != field.one:
        raise AssertionError("subgroup generator failed to close")
    return out


def check(status: bool, name: str, detail: str) -> dict[str, str]:
    return {"status": "PASS" if status else "FAIL", "name": name, "detail": detail}


def build_descriptor() -> dict[str, Any]:
    field = Field(P, MODULUS)
    generator, witness = find_generator(field)
    domain = subgroup_encodings(field, generator)
    domain_hash = hash_json(domain)
    regular_start = ceil_div(N + K + 1, 2)
    tangent_start = N - ((N - K) // 3)
    degree_bound_sum = sum(N - agreement + 1 for agreement in range(regular_start, tangent_start))
    budget = field.size // TWO128

    checks = [
        check(len(MODULUS) == DEGREE + 1 and MODULUS[-1] == 1, "modulus_shape", "monic degree-32 low-to-high modulus"),
        check(is_irreducible_mod_prime(MODULUS, P), "modulus_irreducible", "irreducible over F_17"),
        check(v2(field.size - 1) == 9, "full_2_sylow", "v2(17^32 - 1) = 9"),
        check(field.pow(generator, SUBGROUP_ORDER) == field.one, "generator_closes", "g^512 = 1"),
        check(field.pow(generator, SUBGROUP_ORDER // 2) != field.one, "generator_exact_order", "g^256 != 1"),
        check(len(set(domain)) == SUBGROUP_ORDER, "domain_distinct", "512 distinct encoded elements"),
        check(field.encode(field.zero) not in domain, "domain_excludes_zero", "0 not in H"),
        check(field.encode(field.one) in domain, "domain_contains_one", "1 in H"),
        check(domain_hash == hash_json(domain), "domain_hash_replay", "domain hash matches encoded domain list"),
        check(budget == 6, "security_budget", "floor(17^32 / 2^128) = 6"),
        check(regular_start == 385 and tangent_start == 427, "m3_window", "regular non-tangent window is 385..426"),
        check(degree_bound_sum == 4515, "m3_degree_sum", "regular degree-bound sum over 385..426 is 4515"),
    ]

    return {
        "schema_version": "f17-32-hankel-row-descriptor-v1",
        "status": "AUDIT",
        "row": {
            "field": "F_17^32",
            "field_order": field.size,
            "n": N,
            "k": K,
            "syndrome_length": N - K,
            "domain_hash": domain_hash,
            "domain_description": "order-512 multiplicative subgroup generated by generator_encoding",
        },
        "field_model": {
            "kind": "polynomial_basis",
            "p": P,
            "degree": DEGREE,
            "modulus": MODULUS,
            "encoding": "base-p low-to-high integer",
            "source_ref": "experimental/scripts/verify_v1_f17_32_algebra_checker.py:MODULUS",
        },
        "domain": {
            "type": "multiplicative_subgroup",
            "order": SUBGROUP_ORDER,
            "generator_encoding": field.encode(generator),
            "generator_coefficients_low_to_high": list(generator),
            "generator_witness_integer": witness,
            "domain_encodings": domain,
            "domain_hash_scope": "sha256(json.dumps(domain_encodings, sort_keys=True, separators=(',', ':')))",
        },
        "m3_regular_window": {
            "A_min": regular_start,
            "A_max": tangent_start - 1,
            "regular_start": regular_start,
            "tangent_exact_start": tangent_start,
            "degree_bound_sum": degree_bound_sum,
            "budget_numerator": budget,
            "degree_only_closes_safe_side": degree_bound_sum <= budget,
        },
        "checks": checks,
        "nonclaims": [
            "does not supply syndrome-pencil line data",
            "does not compute regular minors for the 385..426 window",
            "does not prove a safe-side MCA bound",
        ],
    }


def render(descriptor: dict[str, Any]) -> str:
    return json.dumps(descriptor, indent=2, sort_keys=True) + "\n"


def check_descriptor(path: Path) -> None:
    expected = render(build_descriptor())
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"descriptor mismatch: {path}")


def print_summary(descriptor: dict[str, Any]) -> None:
    row = descriptor["row"]
    domain = descriptor["domain"]
    window = descriptor["m3_regular_window"]
    print("F_17^32 Hankel row descriptor")
    print(
        "row: n={n}, k={k}, field={field}, domain_hash={domain_hash}".format(
            **row
        )
    )
    print(
        "field model: p={p}, degree={degree}, modulus_degree={modulus_degree}".format(
            p=descriptor["field_model"]["p"],
            degree=descriptor["field_model"]["degree"],
            modulus_degree=len(descriptor["field_model"]["modulus"]) - 1,
        )
    )
    print(
        "domain: order={order}, generator_encoding={generator_encoding}, witness={generator_witness_integer}".format(
            **domain
        )
    )
    print(
        "M3 window: A={A_min}..{A_max}, degree_sum={degree_bound_sum}, budget={budget_numerator}".format(
            **window
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", type=Path, help="write deterministic descriptor JSON")
    parser.add_argument("--check", type=Path, help="check deterministic descriptor JSON")
    parser.add_argument("--json", action="store_true", help="print descriptor JSON")
    args = parser.parse_args()

    descriptor = build_descriptor()
    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(render(descriptor), encoding="utf-8")
    if args.check:
        check_descriptor(args.check)
    if args.json:
        print(render(descriptor), end="")
        return
    print_summary(descriptor)


if __name__ == "__main__":
    main()
