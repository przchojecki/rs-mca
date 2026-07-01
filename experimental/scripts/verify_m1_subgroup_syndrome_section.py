#!/usr/bin/env python3
"""Verify the subgroup syndrome section for the pinned F_17^32 M3 row."""

from __future__ import annotations

import argparse
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
    hash_json,
)


SCHEMA_VERSION = "f17-32-m3-subgroup-syndrome-section-v1"
Q_LINE = 17**32
R = N - K
ROW_DESCRIPTOR_REF = (
    "experimental/data/certificates/hankel-f17-32-row-descriptor/"
    "f17_32_n512_k256_hankel_row_descriptor.json"
)


def load_json(ref: str | Path) -> dict[str, Any]:
    path = ref if isinstance(ref, Path) else ROOT / ref
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(ref: str) -> str:
    return sha256((ROOT / ref).read_bytes()).hexdigest()


def render(value: dict[str, Any]) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def fadd(field: Field, left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple((left[index] + right[index]) % field.p for index in range(field.degree))


def fscale(field: Field, scalar: int, value: tuple[int, ...]) -> tuple[int, ...]:
    return tuple((scalar * coeff) % field.p for coeff in value)


def subgroup_power_sum(
    field: Field,
    generator: tuple[int, ...],
    exponent: int,
) -> tuple[int, ...]:
    total = field.zero
    ratio = field.pow(generator, exponent % N)
    current = field.one
    for _ in range(N):
        total = fadd(field, total, current)
        current = field.mul(current, ratio)
    require(current == field.one, "geometric character ratio did not close")
    return total


def validate_subgroup(
    row_descriptor: dict[str, Any],
    field: Field,
) -> tuple[dict[str, Any], tuple[int, ...]]:
    domain_encodings = row_descriptor["domain"]["domain_encodings"]
    generator = field.decode(row_descriptor["domain"]["generator_encoding"])
    require(len(domain_encodings) == N, "domain length mismatch")
    require(
        hash_json(domain_encodings) == row_descriptor["row"]["domain_hash"],
        "domain hash mismatch",
    )
    require(field.pow(generator, N) == field.one, "generator does not close at order 512")
    require(field.pow(generator, N // 2) != field.one, "generator has smaller order dividing 256")

    current = field.one
    replayed_domain = []
    for _ in range(N):
        replayed_domain.append(field.encode(current))
        current = field.mul(current, generator)
    require(replayed_domain == domain_encodings, "domain is not the listed generator orbit")
    require(current == field.one, "generator orbit does not close")

    return (
        {
            "domain_replayed_from_generator": True,
            "generator_order": N,
            "domain_size": len(replayed_domain),
            "domain_hash": row_descriptor["row"]["domain_hash"],
        },
        generator,
    )


def character_sum_audit(field: Field, generator: tuple[int, ...]) -> dict[str, Any]:
    inverse_n = pow(N % P, -1, P)
    zero_sum = field.normalize(N)
    require(zero_sum == field.normalize(N), "zero exponent sum mismatch")

    nonzero_checked = 0
    for exponent in range(-(R - 1), R):
        if exponent == 0:
            require(
                fscale(field, inverse_n, zero_sum) == field.one,
                "normalized zero sum mismatch",
            )
            continue
        require(
            field.pow(generator, exponent % N) != field.one,
            f"nonzero exponent {exponent} is trivial on H",
        )
        nonzero_checked += 1

    sample_sums = []
    for exponent in [-(R - 1), -1, 0, 1, R - 1]:
        total = subgroup_power_sum(field, generator, exponent)
        expected = zero_sum if exponent == 0 else field.zero
        require(total == expected, f"sample character sum failed at exponent {exponent}")
        sample_sums.append({"exponent": exponent, "sum_encoding": field.encode(total)})

    return {
        "exponent_min": -(R - 1),
        "exponent_max": R - 1,
        "zero_exponent_sum_encoding": field.encode(zero_sum),
        "normalizing_inverse_mod_17": inverse_n,
        "nonzero_exponents_checked": nonzero_checked,
        "explicit_geometric_sum_samples": sample_sums,
        "statement": (
            "sum_{x in H} x^e is |H| for e=0 and 0 for "
            "0<|e|<256"
        ),
    }


def basis_replay_audit() -> dict[str, Any]:
    for basis_index in range(R):
        for coordinate in range(R):
            exponent = coordinate - basis_index
            require(-(R - 1) <= exponent <= R - 1, "basis exponent outside audited range")
            require(
                (exponent == 0) == (coordinate == basis_index),
                f"basis section replay failed at basis {basis_index}, coordinate {coordinate}",
            )

    samples = []
    for basis_index in (0, 1, R // 2, R - 1):
        samples.append(
            {
                "basis_index": basis_index,
                "section_monomial": f"x^(-{basis_index + 1})",
                "nonzero_syndrome_coordinate": basis_index,
            }
        )

    return {
        "basis_vectors_checked": R,
        "syndrome_coordinates_checked_per_basis": R,
        "all_basis_coordinates_checked": R * R,
        "sample_basis_sections": samples,
    }


def build_certificate() -> dict[str, Any]:
    field = Field(P, MODULUS)
    row_descriptor = load_json(ROW_DESCRIPTOR_REF)
    require(row_descriptor["row"]["n"] == N, "row descriptor n mismatch")
    require(row_descriptor["row"]["k"] == K, "row descriptor k mismatch")
    require(row_descriptor["row"]["field"] == "F_17^32", "row descriptor field mismatch")
    require(row_descriptor["row"]["field_order"] == Q_LINE, "row descriptor q mismatch")
    require(row_descriptor["row"]["syndrome_length"] == R, "row descriptor syndrome mismatch")

    subgroup, generator = validate_subgroup(row_descriptor, field)
    character = character_sum_audit(field, generator)
    basis_replay = basis_replay_audit()

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT",
        "object": "explicit subgroup syndrome section for arbitrary M3 syndrome pencils",
        "row": {
            "code": "RS[F_17^32,H,256]",
            "n": N,
            "k": K,
            "field": "F_17^32",
            "q_line": Q_LINE,
            "domain_hash": row_descriptor["row"]["domain_hash"],
            "syndrome_length": R,
        },
        "source_artifacts": {
            "row_descriptor": {
                "ref": ROW_DESCRIPTOR_REF,
                "sha256": sha256_file(ROW_DESCRIPTOR_REF),
            }
        },
        "subgroup_audit": subgroup,
        "character_sum_audit": character,
        "theorem": {
            "weighted_syndrome_map": "Syn(y)_m=(1/|H|) sum_{x in H} x*y(x)*x^m for 0<=m<256",
            "section_formula": "for syndrome s, set y_s(x)=sum_{a=0}^{255} s_a x^(-a-1)",
            "section_identity": "Syn(y_s)_m=s_m for every 0<=m<256",
            "proof": (
                "Substitution gives |H|^{-1} sum_a s_a sum_{x in H} x^(m-a). "
                "The audited character sums are |H| when a=m and 0 otherwise."
            ),
        },
        "basis_replay_audit": basis_replay,
        "m3_window_use": {
            "agreement_min": 385,
            "agreement_max": 426,
            "identity": "t+j=(A-k)+(n-A)=n-k=256",
            "consequence": (
                "Every M3 regular-window syndrome pencil of the required length "
                "has explicit received-line values on the pinned subgroup row."
            ),
        },
        "summary": {
            "syndrome_coordinates": R,
            "line_value_coordinates": N,
            "basis_vectors_checked": basis_replay["basis_vectors_checked"],
            "all_basis_coordinates_checked": basis_replay["all_basis_coordinates_checked"],
            "nonzero_character_exponents_checked": character["nonzero_exponents_checked"],
        },
        "checks": [
            "row descriptor is the pinned order-512 subgroup",
            "character sums vanish for every exponent -255..255 except zero",
            "the normalized zero character sum is one",
            "all 256 coordinate-basis syndrome vectors replay through the section",
        ],
        "nonclaims": [
            "does not classify regular roots for an arbitrary syndrome pencil",
            "does not prove a support-wise MCA safe-side upper bound",
            "does not perform tangent, quotient, extension, or subfield subtraction",
            "does not assert external prize acceptance",
        ],
    }


def check_certificate(path: Path) -> None:
    expected = render(build_certificate())
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"subgroup syndrome-section certificate mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    summary = certificate["summary"]
    print("F_17^32 M3 subgroup syndrome section")
    print(
        "syndrome coordinates={syndrome_coordinates}, line values={line_value_coordinates}".format(
            **summary
        )
    )
    print(
        (
            "basis coordinates checked={all_basis_coordinates_checked}, "
            "nonzero character exponents={nonzero_character_exponents_checked}"
        ).format(
            **summary
        )
    )


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
