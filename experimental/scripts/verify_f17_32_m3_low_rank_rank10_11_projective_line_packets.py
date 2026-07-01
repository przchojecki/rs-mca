#!/usr/bin/env python3
"""Build M3 rank-10 and rank-11 compact-sweep projective-line packets.

The rank-9..11 sweep stores compact hashes rather than full coefficient
sidecars.  This verifier promotes one maximum-root representative row from
each of ranks 10 and 11 into full v9 packets by recomputing the low-rank
regular minor, checking the stored sweep hashes, splitting the Frobenius gcd,
and adding the projective endpoint.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
import sys
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from experimental.scripts.extract_regular_hankel_minors import (  # noqa: E402
    PolynomialBasisField,
    hash_json,
    render,
)
from experimental.scripts.verify_f17_32_m3_low_rank9_11_slack_sweep import (  # noqa: E402
    frobenius_linear_root_gcd,
    low_rank_coefficients_from_basis_values,
    update_basis_values,
)
from experimental.scripts.verify_f17_32_m3_low_rank_rank6_a426_finite_packet import (  # noqa: E402
    power_sums,
)
from experimental.scripts.verify_f17_32_m3_low_rank_rank7_a393_projective_line_packet import (  # noqa: E402
    split_linear_roots,
)


N = 512
K = 256
SYNDROME_LENGTH = N - K
PROJECTIVE_BUDGET_NUMERATOR = 6

ROW_DESCRIPTOR = REPO_ROOT / (
    "experimental/data/certificates/hankel-f17-32-row-descriptor/"
    "f17_32_n512_k256_hankel_row_descriptor.json"
)
LOW_RANK9_11_SWEEP = REPO_ROOT / (
    "experimental/data/certificates/hankel-f17-32-m3-low-rank9-11-slack-sweep/"
    "f17_32_n512_k256_m3_low_rank9_11_slack_sweep_certificate.json"
)
PROJECTIVE_INFINITY_CERT = REPO_ROOT / (
    "experimental/data/certificates/hankel-f17-32-m3-low-rank2-11-projective-infinity/"
    "f17_32_n512_k256_m3_low_rank2_11_projective_infinity_certificate.json"
)
TANGENT_EXCLUSION = REPO_ROOT / (
    "experimental/data/certificates/hankel-f17-32-m3-low-rank6-11-tangent-exclusion/"
    "f17_32_n512_k256_m3_low_rank6_11_tangent_exclusion_certificate.json"
)
SUBFIELD_EXCLUSION = REPO_ROOT / (
    "experimental/data/certificates/hankel-f17-32-m3-low-rank6-11-subfield-exclusion/"
    "f17_32_n512_k256_m3_low_rank6_11_subfield_exclusion_certificate.json"
)


@dataclass(frozen=True)
class PacketSpec:
    rank: int
    agreement: int

    @property
    def j(self) -> int:
        return N - self.agreement

    @property
    def t(self) -> int:
        return self.agreement - K

    @property
    def minor_size(self) -> int:
        return self.j + 1

    @property
    def schema(self) -> str:
        return (
            f"f17-32-m3-low-rank-rank{self.rank}-a{self.agreement}"
            "-projective-line-v1"
        )

    @property
    def label(self) -> str:
        return f"rank-{self.rank} A={self.agreement}"

    @property
    def path_stem(self) -> str:
        return f"f17_32_n512_k256_a{self.agreement}_rank{self.rank}"

    @property
    def input_path(self) -> Path:
        return REPO_ROOT / (
            "experimental/data/hankel-regular-minor-inputs/"
            f"f17_32_n512_k256_a{self.agreement}_low_rank{self.rank}"
            "_projective_line_input.json"
        )

    @property
    def packet_dir(self) -> Path:
        return REPO_ROOT / (
            "experimental/data/certificates/"
            f"hankel-f17-32-m3-low-rank-rank{self.rank}-a{self.agreement}"
            "-projective-line"
        )

    @property
    def packet_path(self) -> Path:
        return self.packet_dir / f"{self.path_stem}_projective_line_packet.json"


SPECS = [
    PacketSpec(rank=10, agreement=411),
    PacketSpec(rank=11, agreement=391),
]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def file_sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def object_sha256(value: Any) -> str:
    return sha256(render(value).encode("utf-8")).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def field_from_descriptor(descriptor: dict[str, Any]) -> PolynomialBasisField:
    model = descriptor["field_model"]
    return PolynomialBasisField(model["p"], model["modulus"])


def sweep_record(sweep: dict[str, Any], spec: PacketSpec) -> dict[str, Any]:
    records = [
        record
        for record in sweep["records"]
        if record["rank"] == spec.rank and record["A"] == spec.agreement
    ]
    require(len(records) == 1, f"expected one {spec.label} sweep record")
    record = records[0]
    require(
        record["j"] == spec.j and record["t"] == spec.t,
        f"{spec.label} row shape mismatch",
    )
    require(record["root_count"] == 3, f"{spec.label} should have three roots")
    require(record["listed_roots"] is None, f"{spec.label} source should be count-only")
    return record


def validate_sources(
    descriptor: dict[str, Any],
    sweep: dict[str, Any],
    projective_infinity: dict[str, Any],
    spec: PacketSpec,
) -> None:
    require(descriptor["row"]["n"] == N, "row descriptor n mismatch")
    require(descriptor["row"]["k"] == K, "row descriptor k mismatch")
    require(
        sweep["schema_version"] == "f17-32-m3-low-rank9-11-slack-sweep-v1",
        "rank-9..11 sweep schema mismatch",
    )
    require(sweep["agreement_range"] == [385, 426], "rank-9..11 window mismatch")
    rank_summary = sweep["aggregate"]["rank_summaries"][str(spec.rank)]
    require(
        rank_summary["max_finite_roots_per_agreement"] == 3
        and rank_summary["max_projective_regular_roots_per_agreement"] == 4
        and spec.agreement in rank_summary["worst_agreements"],
        f"{spec.label} sweep summary mismatch",
    )
    require(
        projective_infinity["schema_version"]
        == "f17-32-m3-low-rank2-11-projective-infinity-v1",
        "projective-infinity schema mismatch",
    )
    require(
        projective_infinity["aggregate"]["rank_summaries"][str(spec.rank)][
            "endpoint_support_size"
        ]
        == N - spec.rank,
        f"{spec.label} endpoint support mismatch",
    )


def prefix_state(
    field: PolynomialBasisField,
    domain: list[tuple[int, ...]],
    size: int,
) -> tuple[list[tuple[int, ...]], list[tuple[int, ...]], tuple[int, ...]]:
    base_nodes: list[tuple[int, ...]] = []
    denominators: list[tuple[int, ...]] = []
    base_determinant = field.one
    for index in range(size):
        new_node = domain[index]
        new_denominator = field.one
        for old_node in base_nodes:
            new_denominator = field.mul(
                new_denominator, field.sub(new_node, old_node)
            )
        for old_index, old_node in enumerate(base_nodes):
            denominators[old_index] = field.mul(
                denominators[old_index], field.sub(old_node, new_node)
            )
        denominators.append(new_denominator)
        base_nodes.append(new_node)
        base_determinant = field.mul(
            base_determinant, field.mul(new_denominator, new_denominator)
        )
    return base_nodes, denominators, base_determinant


def recompute_row_data(
    descriptor: dict[str, Any],
    record: dict[str, Any],
    spec: PacketSpec,
) -> tuple[list[int], dict[str, Any], list[int]]:
    field = field_from_descriptor(descriptor)
    domain = [
        field.decode(value) for value in descriptor["domain"]["domain_encodings"]
    ]
    base_nodes, denominators, base_determinant = prefix_state(
        field, domain, spec.minor_size
    )
    update_nodes = domain[spec.minor_size : spec.minor_size + spec.rank]
    basis_values = update_basis_values(field, base_nodes, denominators, update_nodes)
    coefficients = low_rank_coefficients_from_basis_values(
        field, basis_values, base_determinant, spec.rank
    )
    encoded_coefficients = [field.encode(coefficient) for coefficient in coefficients]
    require(
        hash_json(encoded_coefficients) == record["coefficient_hash"],
        f"{spec.label} coefficient hash mismatch",
    )

    monic, frobenius_remainder, root_gcd = frobenius_linear_root_gcd(
        coefficients, field
    )
    encoded_monic = [field.encode(coefficient) for coefficient in monic]
    encoded_remainder = [
        field.encode(coefficient) for coefficient in frobenius_remainder
    ]
    encoded_gcd = [field.encode(coefficient) for coefficient in root_gcd]
    compact = record["linear_root_count_certificate"]
    require(
        hash_json(encoded_monic) == compact["monic_delta_hash"],
        f"{spec.label} monic hash mismatch",
    )
    require(
        hash_json(encoded_remainder) == compact["frobenius_remainder_hash"],
        f"{spec.label} Frobenius remainder hash mismatch",
    )
    require(
        hash_json(encoded_gcd) == compact["linear_root_gcd_hash"],
        f"{spec.label} gcd hash mismatch",
    )

    roots = split_linear_roots(root_gcd, field)
    require(len(roots) == record["root_count"], f"{spec.label} split root mismatch")
    require(
        hash_json({"root_count": len(roots), "linear_root_gcd": encoded_gcd})
        == record["root_count_hash"],
        f"{spec.label} root-count hash mismatch",
    )
    for root in roots:
        root_value = field.decode(root)
        total = field.zero
        power = field.one
        for coefficient in root_gcd:
            total = field.add(total, field.mul(coefficient, power))
            power = field.mul(power, root_value)
        require(field.is_zero(total), f"{spec.label} listed root does not satisfy gcd")

    root_count_certificate = {
        "kind": "frobenius_linear_root_gcd",
        "field_encoding": "base-p low-to-high integer",
        "field_order": field.size,
        "polynomial": "Z^q-Z",
        "monic_delta_coefficients_ascending": encoded_monic,
        "frobenius_remainder_coefficients_ascending": encoded_remainder,
        "linear_root_gcd_coefficients_ascending": encoded_gcd,
        "linear_root_count": record["root_count"],
        "listed_roots_status": "listed",
        "reason": (
            "gcd(Delta,Z^q-Z) is the squarefree product of the finite field "
            "linear factors of Delta"
        ),
    }
    return encoded_coefficients, root_count_certificate, roots


def build_input(descriptor: dict[str, Any], spec: PacketSpec) -> dict[str, Any]:
    field = field_from_descriptor(descriptor)
    domain_encodings = descriptor["domain"]["domain_encodings"]
    base_encodings = domain_encodings[: spec.minor_size]
    update_encodings = domain_encodings[spec.minor_size : spec.minor_size + spec.rank]
    base_nodes = [field.decode(value) for value in base_encodings]
    update_nodes = [field.decode(value) for value in update_encodings]
    return {
        "schema_version": "regular-hankel-minor-extractor-input-v1",
        "status": "PROVED / AUDIT",
        "agreement_threshold": spec.agreement,
        "exact_agreements": [spec.agreement],
        "sampler": "projective_line",
        "certificate_mode": "low_rank_update_bound",
        "field_model": {
            "kind": "polynomial_basis",
            "p": descriptor["field_model"]["p"],
            "degree": descriptor["field_model"]["degree"],
            "modulus": descriptor["field_model"]["modulus"],
            "encoding": "base-p low-to-high integer",
        },
        "row": {
            "n": N,
            "k": K,
            "field": descriptor["row"]["field"],
            "domain_hash": descriptor["row"]["domain_hash"],
            "domain_description": (
                "order-512 subgroup from the pinned F_17^32 row descriptor; "
                f"synthetic M3 rank-{spec.rank} low-rank update syndrome uses "
                f"the first {spec.minor_size} elements and the next {spec.rank} "
                "descriptor-domain elements"
            ),
        },
        "claim_scope": {
            "row_data": "synthetic_syndrome_pencil",
            "threshold_role": "synthetic_stress",
            "root_status": "enumerated",
            "may_be_used_for_threshold_pinning": False,
            "note": (
                f"Rank-{spec.rank} low-rank update replay input for the "
                f"A={spec.agreement} projective-line v9 packet; this is not "
                "actual-row data."
            ),
        },
        "row_set_strategy": {"type": "prefix"},
        "line_syndrome": {
            "description": (
                f"synthetic M3 rank-{spec.rank} low-rank update witness: "
                f"u_m=sum_{{x in X}}x^m for the first {spec.minor_size} "
                "descriptor-domain elements and "
                f"v_m=sum_{{y in Y}}y^m for the next {spec.rank} elements"
            ),
            "field_encoding": "base-p low-to-high integer",
            "length": SYNDROME_LENGTH,
            "rank_witness_reason": (
                "low-rank Cauchy-Binet update makes the prefix determinant "
                "degree-bounded by the update rank"
            ),
            "u": power_sums(field, base_nodes, SYNDROME_LENGTH),
            "v": power_sums(field, update_nodes, SYNDROME_LENGTH),
        },
        "low_rank_update": {
            "base_node_count": spec.minor_size,
            "update_rank": spec.rank,
            "base_node_encodings": base_encodings,
            "update_node_encodings": update_encodings,
        },
        "nonclaims": [
            "synthetic syndrome pencil only",
            "not a worst-case or actual-row M3 threshold bound",
            "not a quotient-image subtraction table",
        ],
    }


def build_packet(
    descriptor: dict[str, Any],
    sweep: dict[str, Any],
    projective_infinity: dict[str, Any],
    input_object: dict[str, Any],
    spec: PacketSpec,
) -> dict[str, Any]:
    record = sweep_record(sweep, spec)
    coefficients, root_count_certificate, roots = recompute_row_data(
        descriptor, record, spec
    )
    root_hash = hash_json(roots)
    input_ref = str(spec.input_path.relative_to(REPO_ROOT))
    infinity = record["projective_infinity"]["contribution"]
    return {
        "schema_version": "aperiodic-hankel-eliminant-v1",
        "packet_certificate_schema": spec.schema,
        "status": "PROVED / AUDIT",
        "row": {
            "n": N,
            "k": K,
            "field": descriptor["row"]["field"],
            "domain_hash": descriptor["row"]["domain_hash"],
            "domain_description": (
                "order-512 subgroup from the pinned F_17^32 row descriptor; "
                f"synthetic rank-{spec.rank} low-rank update syndrome at "
                f"A={spec.agreement}"
            ),
        },
        "agreement_threshold": spec.agreement,
        "sampler": "projective_line",
        "sampler_audit": {
            "sampler": "projective_line",
            "slope_field": descriptor["row"]["field"],
            "slope_field_order": descriptor["row"]["field_order"],
            "denominator": descriptor["row"]["field_order"] + 1,
            "denominator_formula": "|P^1(F)| = |F| + 1",
            "field_role": "q_line",
            "extension_denominator_warning": (
                "projective extension-valued line packets are divided by "
                "|P^1(F)|, not by the base field"
            ),
        },
        "claim_scope": {
            "row_data": "synthetic_syndrome_pencil",
            "threshold_role": "synthetic_stress",
            "root_status": "enumerated",
            "may_be_used_for_threshold_pinning": False,
            "note": (
                "Projective-line regular-minor packet for one compact-sweep "
                f"rank-{spec.rank} low-rank row. It is a v9 replay packet, "
                "not an actual-row safe-side threshold certificate."
            ),
        },
        "extractor": {
            "name": "regular-hankel-minor-extractor",
            "method": (
                "compact sweep hash replay, low-rank update regular-minor "
                "replay, deterministic splitting of the Frobenius-gcd finite "
                "root table, and original-top-degree projective infinity audit"
            ),
            "scope": "prime-power syndrome pencils with explicit polynomial-basis model",
            "certificate_mode": "low_rank_update_bound",
            "row_set_strategy": {"type": "prefix"},
            "input_ref": input_ref,
            "input_sha256": object_sha256(input_object),
            "field_model": input_object["field_model"],
        },
        "source_artifacts": {
            "row_descriptor": {
                "ref": str(ROW_DESCRIPTOR.relative_to(REPO_ROOT)),
                "sha256": file_sha256(ROW_DESCRIPTOR),
            },
            "rank9_11_slack_sweep": {
                "ref": str(LOW_RANK9_11_SWEEP.relative_to(REPO_ROOT)),
                "sha256": file_sha256(LOW_RANK9_11_SWEEP),
                "schema_version": sweep["schema_version"],
            },
            "rank2_11_projective_infinity_endpoint": {
                "ref": str(PROJECTIVE_INFINITY_CERT.relative_to(REPO_ROOT)),
                "sha256": file_sha256(PROJECTIVE_INFINITY_CERT),
                "schema_version": projective_infinity["schema_version"],
            },
        },
        "removed_ledgers": [
            {
                "name": "common_code_line_tangent_overlap",
                "numerator": 0,
                "certificate_ref": (
                    str(TANGENT_EXCLUSION.relative_to(REPO_ROOT))
                    + "#/aggregate/common_code_line_tangent_overlap_sum"
                ),
            },
            {
                "name": "proper_subfield_overlap",
                "numerator": 0,
                "certificate_ref": (
                    str(SUBFIELD_EXCLUSION.relative_to(REPO_ROOT))
                    + "#/aggregate/proper_subfield_overlap_sum"
                ),
            },
        ],
        "exact_agreements": [
            {
                "A": spec.agreement,
                "j": spec.j,
                "t": spec.t,
                "status": "regular_minor",
                "regular_minor": {
                    "row_set": list(range(spec.minor_size)),
                    "polynomial_ref": "inline:regular_minor.coefficients_ascending",
                    "degree": record["polynomial_degree"],
                    "root_hash": root_hash,
                },
                "regular_minor_data": {
                    "coefficients_ascending": coefficients,
                    "field_encoding": "base-p low-to-high integer",
                    "field_extension_degree": 32,
                    "p": 17,
                    "roots": roots,
                    "linear_root_count_certificate": root_count_certificate,
                    "root_listing_certificate": {
                        "kind": "deterministic_cantor_zassenhaus_small_degree",
                        "input": "linear_root_gcd_coefficients_ascending",
                        "degree": record["root_count"],
                        "seed_range": [0, 199],
                        "roots": roots,
                    },
                },
                "regular_minor_polynomial_data": {
                    "coefficients_ascending": coefficients,
                    "field_encoding": "base-p low-to-high integer",
                    "field_extension_degree": 32,
                    "p": 17,
                },
                "projective_infinity": {
                    "projective_point": "[0:1]",
                    "status": "nonempty",
                    "top_degree": spec.minor_size,
                    "top_coefficient": 0,
                    "field_encoding": "base-p low-to-high integer",
                    "contribution": infinity,
                    "reason": (
                        "The projective-line regular minor is homogenized to "
                        f"the original degree j+1. Since the rank-{spec.rank} "
                        f"compressed determinant has degree {spec.rank} < "
                        f"j+1={spec.minor_size}, the top coefficient is zero "
                        "and the regular minor does not exclude [0:1]."
                    ),
                    "support_certificate_ref": (
                        str(PROJECTIVE_INFINITY_CERT.relative_to(REPO_ROOT))
                        + "#/deterministic_records"
                    ),
                },
                "extractor_audit": {
                    "certificate_mode": "low_rank_update_bound",
                    "row_set_source": f"low_rank_update_prefix_rank{spec.rank}",
                    "tested_row_sets": 1,
                    "degree_bound": spec.rank,
                    "root_count": len(roots),
                    "field_size": descriptor["row"]["field_order"],
                    "finite_root_count_certificate": "frobenius_linear_root_gcd",
                    "root_listing": "deterministic_small_degree_split",
                    "projective_infinity_contribution": infinity,
                    "projective_regular_root_count": len(roots) + infinity,
                    "projective_budget_numerator": PROJECTIVE_BUDGET_NUMERATOR,
                },
            }
        ],
        "root_union": roots,
        "enumerated_bad_slope_union": [],
        "declared_aperiodic_numerator": len(roots) + infinity,
        "root_union_table_ref": "inline:root_union",
        "finite_affine_numerator": len(roots),
        "projective_infinity_numerator": infinity,
        "projective_line_numerator": len(roots) + infinity,
        "nonclaims": [
            "synthetic syndrome-pencil packet only",
            "regular-minor roots are an upper-bound root table, not proved actual bad slopes",
            "projective infinity is counted as a regular-minor endpoint",
            "not a quotient-image subtraction table",
            "not a worst-case or actual-row M3 threshold bound",
        ],
    }


def build_objects(spec: PacketSpec) -> tuple[dict[str, Any], dict[str, Any]]:
    descriptor = load_json(ROW_DESCRIPTOR)
    sweep = load_json(LOW_RANK9_11_SWEEP)
    projective_infinity = load_json(PROJECTIVE_INFINITY_CERT)
    validate_sources(descriptor, sweep, projective_infinity, spec)
    input_object = build_input(descriptor, spec)
    packet = build_packet(descriptor, sweep, projective_infinity, input_object, spec)
    return input_object, packet


def check_file(path: Path, expected: dict[str, Any], label: str) -> None:
    actual = path.read_text(encoding="utf-8")
    expected_text = render(expected)
    if actual != expected_text:
        raise AssertionError(f"{label} mismatch: {path}")


def print_summary(packets: list[dict[str, Any]]) -> None:
    print("F_17^32 M3 rank-10/11 projective-line compact-sweep packets")
    for packet in packets:
        item = packet["exact_agreements"][0]
        print(
            "rank={rank}, A={agreement}, degree={degree}, "
            "finite_roots={finite}, infinity={infinity}, numerator={num}".format(
                rank=item["extractor_audit"]["degree_bound"],
                agreement=packet["agreement_threshold"],
                degree=item["regular_minor"]["degree"],
                finite=packet["finite_affine_numerator"],
                infinity=packet["projective_infinity_numerator"],
                num=packet["declared_aperiodic_numerator"],
            )
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write inputs and packets")
    parser.add_argument("--check", action="store_true", help="check inputs and packets")
    parser.add_argument("--json", action="store_true", help="print packet JSON list")
    args = parser.parse_args()

    built = [(spec, *build_objects(spec)) for spec in SPECS]
    if args.write:
        for spec, input_object, packet in built:
            spec.input_path.parent.mkdir(parents=True, exist_ok=True)
            spec.packet_dir.mkdir(parents=True, exist_ok=True)
            spec.input_path.write_text(render(input_object), encoding="utf-8")
            spec.packet_path.write_text(render(packet), encoding="utf-8")
    if args.check:
        for spec, input_object, packet in built:
            check_file(spec.input_path, input_object, f"{spec.label} packet input")
            check_file(spec.packet_path, packet, f"{spec.label} projective-line packet")
    packets = [packet for _spec, _input_object, packet in built]
    if args.json:
        print(render(packets), end="")
        return
    print_summary(packets)


if __name__ == "__main__":
    main()
