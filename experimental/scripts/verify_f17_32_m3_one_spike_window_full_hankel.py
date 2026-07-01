#!/usr/bin/env python3
"""Verify the F_17^32 M3 one-spike full-Hankel window ledger.

This closes a non-proportional rank-one test branch across the whole M3
regular window.  For each agreement A=385..426, set j=n-A and take

    u_m = sum_{x in X} x^m,  |X|=j+1,
    v_m = y^m,

where X is the first j+1 points in the pinned subgroup row and y is the next
point.  The prefix regular minor is affine in the slope.  The unique finite
root is excluded from the full-Hankel witness column by the row-shift-1 minor,
and the projective endpoint is charged to quotient-image by a c=2 witness.
"""

from __future__ import annotations

import argparse
from collections import Counter
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
    field_batch_inverses,
    fpoly_degree,
    fpoly_eval,
    fpoly_gcd,
    hash_json,
)
from experimental.scripts.verify_f17_32_m3_low_rank6_11_shifted_minor_exclusion import (  # noqa: E402
    field_from_descriptor,
)


SCHEMA_VERSION = "f17-32-m3-one-spike-window-full-hankel-v1"
N = 512
K = 256
SYNDROME_LENGTH = N - K
AGREEMENT_MIN = 385
AGREEMENT_MAX = 426
SHIFT = 1
FIBER_SIZE = 2
QUOTIENT_ORDER = N // FIBER_SIZE
BUDGET_NUMERATOR = 6

ROW_DESCRIPTOR_REF = (
    "experimental/data/certificates/hankel-f17-32-row-descriptor/"
    "f17_32_n512_k256_hankel_row_descriptor.json"
)
ONE_SPIKE_TEMPLATE_REF = (
    "experimental/data/certificates/hankel-one-spike-linear-template/"
    "hankel_one_spike_linear_template_certificate.json"
)
ONE_SPIKE_TEMPLATE_NOTE_REF = "experimental/notes/m1/hankel_one_spike_linear_template.md"
SHIFTED_MINOR_CRITERION_REF = (
    "experimental/notes/m1/hankel_shifted_minor_exclusion_criterion.md"
)
ENDPOINT_QUOTIENT_IMAGE_CRITERION_REF = (
    "experimental/notes/m1/hankel_endpoint_quotient_image_criterion.md"
)
ONE_SPIKE_A426_PACKET_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-one-spike-a426/"
    "f17_32_n512_k256_a426_one_spike_packet.json"
)
OUTPUT_PATH = REPO_ROOT / (
    "experimental/data/certificates/"
    "hankel-f17-32-m3-one-spike-window-full-hankel/"
    "f17_32_n512_k256_m3_one_spike_window_full_hankel.json"
)


def render(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def load_json(ref: str) -> dict[str, Any]:
    return json.loads((REPO_ROOT / ref).read_text(encoding="utf-8"))


def file_sha256(ref: str) -> str:
    return sha256((REPO_ROOT / ref).read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def field_product(
    values: list[tuple[int, ...]],
    field: PolynomialBasisField,
) -> tuple[int, ...]:
    out = field.one
    for value in values:
        out = field.mul(out, value)
    return out


def prefix_data_by_size(
    domain: list[tuple[int, ...]],
    max_size: int,
    field: PolynomialBasisField,
) -> dict[int, dict[str, Any]]:
    """Build prefix Vandermonde/denominator data for the first max_size nodes."""

    data = {}
    base_nodes: list[tuple[int, ...]] = []
    denominators: list[tuple[int, ...]] = []
    base_vandermonde_square = field.one
    base_product = field.one
    for size in range(1, max_size + 1):
        new_node = domain[size - 1]
        new_denominator = field.one
        for old_node in base_nodes:
            new_denominator = field.mul(
                new_denominator,
                field.sub(new_node, old_node),
            )
        for index, old_node in enumerate(base_nodes):
            denominators[index] = field.mul(
                denominators[index],
                field.sub(old_node, new_node),
            )
        denominators.append(new_denominator)
        base_nodes.append(new_node)
        base_vandermonde_square = field.mul(
            base_vandermonde_square,
            field.mul(new_denominator, new_denominator),
        )
        base_product = field.mul(base_product, new_node)

        spike = domain[size]
        spike_differences = [field.sub(spike, base) for base in base_nodes]
        data[size] = {
            "base_vandermonde_square": base_vandermonde_square,
            "base_product": base_product,
            "denominators": denominators.copy(),
            "spike": spike,
            "spike_difference_product": field_product(spike_differences, field),
        }
    return data


def one_spike_prefix_and_shift_coefficients(
    prefix_data: dict[str, Any],
    base_nodes: list[tuple[int, ...]],
    base_node_inverses: list[tuple[int, ...]],
    field: PolynomialBasisField,
) -> tuple[list[tuple[int, ...]], list[tuple[int, ...]]]:
    """Return first and row-shift-1 one-spike minor polynomials."""

    spike = prefix_data["spike"]
    spike_differences = [field.sub(spike, base) for base in base_nodes]
    inverse_inputs = [
        field.mul(difference, denominator)
        for difference, denominator in zip(
            spike_differences,
            prefix_data["denominators"],
        )
    ]
    inverses = field_batch_inverses(inverse_inputs, field)
    product_all = prefix_data["spike_difference_product"]

    shift0_multiplier = field.zero
    shift1_multiplier = field.zero
    for index, inverse in enumerate(inverses):
        lagrange_value = field.mul(product_all, inverse)
        lagrange_square = field.mul(lagrange_value, lagrange_value)
        shift0_multiplier = field.add(shift0_multiplier, lagrange_square)
        shift1_multiplier = field.add(
            shift1_multiplier,
            field.mul(lagrange_square, field.mul(spike, base_node_inverses[index])),
        )

    first_c0 = prefix_data["base_vandermonde_square"]
    shifted_c0 = field.mul(first_c0, prefix_data["base_product"])
    return (
        [first_c0, field.mul(first_c0, shift0_multiplier)],
        [shifted_c0, field.mul(shifted_c0, shift1_multiplier)],
    )


def quotient_remainder_support_avoiding_spike(
    agreement: int,
    spike_exponent: int,
) -> dict[str, Any]:
    hit_residue = spike_exponent % QUOTIENT_ORDER
    safe_residues = [
        residue for residue in range(QUOTIENT_ORDER) if residue != hit_residue
    ]
    full_fiber_count = agreement // FIBER_SIZE
    remainder_size = agreement % FIBER_SIZE
    require(
        len(safe_residues) >= full_fiber_count + remainder_size,
        "not enough c=2 fibers avoiding the spike",
    )

    support: set[int] = set()
    full_fiber_residues = safe_residues[:full_fiber_count]
    for residue in full_fiber_residues:
        support.add(residue)
        support.add(residue + QUOTIENT_ORDER)
    remainder_exponents = []
    if remainder_size:
        residue = safe_residues[full_fiber_count]
        support.add(residue)
        remainder_exponents = [residue]

    require(len(support) == agreement, "quotient support size mismatch")
    require(spike_exponent not in support, "quotient support hits spike")
    return {
        "fiber_size": FIBER_SIZE,
        "quotient_order": QUOTIENT_ORDER,
        "support_size": agreement,
        "full_fiber_count": full_fiber_count,
        "remainder_size": remainder_size,
        "full_fiber_residue_range": [
            full_fiber_residues[0],
            full_fiber_residues[-1],
        ],
        "full_fiber_residue_count": len(full_fiber_residues),
        "remainder_exponents": remainder_exponents,
        "hit_spike_residue": hit_residue,
        "support_avoids_spike": True,
        "co_support_size": N - agreement,
        "co_support_contains_spike": True,
        "support_exponent_hash": hash_json(sorted(support)),
    }


def encoded_coefficients(
    polynomial: list[tuple[int, ...]],
    field: PolynomialBasisField,
) -> list[int]:
    return [field.encode(coeff) for coeff in polynomial]


def build_records(
    domain: list[tuple[int, ...]],
    field: PolynomialBasisField,
) -> list[dict[str, Any]]:
    records = []
    max_size = N - AGREEMENT_MIN + 1
    prefix_data = prefix_data_by_size(domain, max_size, field)
    domain_inverses = field_batch_inverses(domain[:max_size], field)
    for agreement in range(AGREEMENT_MIN, AGREEMENT_MAX + 1):
        j = N - agreement
        t = agreement - K
        size = j + 1
        base_nodes = domain[:size]
        base_node_inverses = domain_inverses[:size]
        spike = prefix_data[size]["spike"]
        spike_exponent = size

        first_minor, shifted_minor = one_spike_prefix_and_shift_coefficients(
            prefix_data[size],
            base_nodes,
            base_node_inverses,
            field,
        )
        require(not field.is_zero(first_minor[0]), f"A={agreement}: zero C0")
        require(not field.is_zero(first_minor[1]), f"A={agreement}: zero C1")
        root = field.neg(field.div(first_minor[0], first_minor[1]))
        require(
            field.is_zero(fpoly_eval(first_minor, root, field)),
            f"A={agreement}: root does not kill first minor",
        )
        shifted_value = fpoly_eval(shifted_minor, root, field)
        require(
            not field.is_zero(shifted_value),
            f"A={agreement}: shifted minor also vanishes at root",
        )
        common_gcd = fpoly_gcd(first_minor, shifted_minor, field)
        common_gcd_degree = fpoly_degree(common_gcd, field)
        require(common_gcd_degree == 0, f"A={agreement}: common gcd")

        quotient_support = quotient_remainder_support_avoiding_spike(
            agreement,
            spike_exponent,
        )
        require(quotient_support["co_support_size"] == j, "co-support size")
        endpoint_support_size = N - 1
        endpoint_noncontainment_columns = size + 1
        quotient_image_union_bound = size + j
        require(endpoint_support_size >= agreement, "endpoint misses threshold")
        require(
            endpoint_noncontainment_columns <= SYNDROME_LENGTH,
            "endpoint Vandermonde columns too large",
        )
        require(
            quotient_image_union_bound <= SYNDROME_LENGTH,
            "quotient-image Vandermonde union too large",
        )

        records.append(
            {
                "A": agreement,
                "j": j,
                "t": t,
                "minor_size": size,
                "base_node_range": [0, size - 1],
                "spike_exponent": spike_exponent,
                "spike_encoding": field.encode(spike),
                "regular_minor_degree": 1,
                "regular_minor_coefficients_ascending": encoded_coefficients(
                    first_minor,
                    field,
                ),
                "finite_root": field.encode(root),
                "shifted_minor_row_shift": SHIFT,
                "shifted_minor_coefficients_ascending": encoded_coefficients(
                    shifted_minor,
                    field,
                ),
                "shifted_minor_value_at_root": field.encode(shifted_value),
                "common_gcd_degree": common_gcd_degree,
                "finite_regular_root_count": 1,
                "finite_regular_roots_excluded_by_shifted_minor": 1,
                "finite_full_hankel_witness_upper": 0,
                "projective_endpoint_contribution": 1,
                "projective_endpoint_support_size": endpoint_support_size,
                "endpoint_noncontainment_vandermonde_columns": (
                    endpoint_noncontainment_columns
                ),
                "endpoint_quotient_image_witness": 1,
                "endpoint_quotient_image_support": quotient_support,
                "quotient_image_vandermonde_union_bound": (
                    quotient_image_union_bound
                ),
                "regular_projective_upper": 2,
                "full_hankel_projective_upper_before_endpoint_image": 1,
                "aperiodic_full_hankel_projective_upper": 0,
                "within_regular_projective_budget": True,
                "within_full_hankel_projective_budget": True,
                "within_aperiodic_full_hankel_budget": True,
            }
        )
    return records


def summarize(records: list[dict[str, Any]]) -> dict[str, Any]:
    common_gcd_histogram = Counter(
        record["common_gcd_degree"] for record in records
    )
    root_hash = hash_json([record["finite_root"] for record in records])
    return {
        "record_count": len(records),
        "agreement_range": [AGREEMENT_MIN, AGREEMENT_MAX],
        "finite_regular_root_count_sum": sum(
            record["finite_regular_root_count"] for record in records
        ),
        "finite_regular_roots_excluded_by_shifted_minor_sum": sum(
            record["finite_regular_roots_excluded_by_shifted_minor"]
            for record in records
        ),
        "finite_full_hankel_witness_upper_sum": sum(
            record["finite_full_hankel_witness_upper"] for record in records
        ),
        "projective_endpoint_contribution_sum": sum(
            record["projective_endpoint_contribution"] for record in records
        ),
        "endpoint_quotient_image_witness_sum": sum(
            record["endpoint_quotient_image_witness"] for record in records
        ),
        "regular_projective_upper_sum": sum(
            record["regular_projective_upper"] for record in records
        ),
        "max_regular_projective_upper_per_record": max(
            record["regular_projective_upper"] for record in records
        ),
        "full_hankel_projective_upper_before_endpoint_image_sum": sum(
            record["full_hankel_projective_upper_before_endpoint_image"]
            for record in records
        ),
        "max_full_hankel_projective_upper_before_endpoint_image_per_record": max(
            record["full_hankel_projective_upper_before_endpoint_image"]
            for record in records
        ),
        "aperiodic_full_hankel_projective_upper_sum": sum(
            record["aperiodic_full_hankel_projective_upper"] for record in records
        ),
        "max_aperiodic_full_hankel_projective_upper_per_record": max(
            record["aperiodic_full_hankel_projective_upper"] for record in records
        ),
        "common_gcd_degree_histogram": {
            str(key): value for key, value in sorted(common_gcd_histogram.items())
        },
        "finite_root_hash": root_hash,
        "first_finite_root": records[0]["finite_root"],
        "last_finite_root": records[-1]["finite_root"],
        "minimum_endpoint_support_size": min(
            record["projective_endpoint_support_size"] for record in records
        ),
        "maximum_endpoint_noncontainment_vandermonde_columns": max(
            record["endpoint_noncontainment_vandermonde_columns"]
            for record in records
        ),
        "maximum_quotient_image_vandermonde_union_bound": max(
            record["quotient_image_vandermonde_union_bound"]
            for record in records
        ),
        "projective_budget_numerator": BUDGET_NUMERATOR,
        "all_finite_roots_excluded_by_shifted_minor": all(
            record["finite_regular_roots_excluded_by_shifted_minor"] == 1
            for record in records
        ),
        "all_projective_endpoints_have_quotient_image_witness": all(
            record["endpoint_quotient_image_witness"] == 1 for record in records
        ),
        "all_records_within_regular_projective_budget": all(
            record["within_regular_projective_budget"] for record in records
        ),
        "all_records_within_full_hankel_projective_budget": all(
            record["within_full_hankel_projective_budget"] for record in records
        ),
        "all_records_within_aperiodic_full_hankel_budget": all(
            record["within_aperiodic_full_hankel_budget"] for record in records
        ),
    }


def source_record(name: str, ref: str, data: dict[str, Any] | None = None) -> dict[str, Any]:
    record = {
        "name": name,
        "ref": ref,
        "sha256": file_sha256(ref),
    }
    if data is not None:
        record["schema_version"] = data.get("schema_version")
        record["status"] = data.get("status")
    return record


def validate_sources(
    descriptor: dict[str, Any],
    template: dict[str, Any],
    a426_packet: dict[str, Any],
) -> None:
    require(
        descriptor["schema_version"] == "f17-32-hankel-row-descriptor-v1",
        "row descriptor schema",
    )
    require(
        descriptor["row"]["n"] == N
        and descriptor["row"]["k"] == K
        and len(descriptor["domain"]["domain_encodings"]) == N,
        "row descriptor shape",
    )
    require(
        template["schema_version"] == "m1-hankel-one-spike-linear-template-v1",
        "one-spike template schema",
    )
    require(template["status"] == "PROVED / AUDIT", "one-spike template status")
    require(
        a426_packet["schema_version"] == "aperiodic-hankel-eliminant-v1"
        and a426_packet["agreement_threshold"] == AGREEMENT_MAX
        and a426_packet["declared_aperiodic_numerator"] == 1
        and a426_packet["exact_agreements"][0]["regular_minor"]["degree"] == 1,
        "A=426 one-spike packet cross-check",
    )


def build_certificate() -> dict[str, Any]:
    descriptor = load_json(ROW_DESCRIPTOR_REF)
    template = load_json(ONE_SPIKE_TEMPLATE_REF)
    a426_packet = load_json(ONE_SPIKE_A426_PACKET_REF)
    validate_sources(descriptor, template, a426_packet)
    field = field_from_descriptor(descriptor)
    domain = [field.decode(value) for value in descriptor["domain"]["domain_encodings"]]
    records = build_records(domain, field)
    aggregate = summarize(records)
    require(aggregate["record_count"] == 42, "record count")
    require(aggregate["finite_regular_root_count_sum"] == 42, "finite roots")
    require(
        aggregate["finite_regular_roots_excluded_by_shifted_minor_sum"] == 42,
        "shifted-minor cleared roots",
    )
    require(aggregate["finite_full_hankel_witness_upper_sum"] == 0, "finite full")
    require(
        aggregate["max_aperiodic_full_hankel_projective_upper_per_record"] == 0,
        "aperiodic residual max",
    )
    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT",
        "row": {
            "n": N,
            "k": K,
            "field": descriptor["row"]["field"],
            "domain_hash": descriptor["row"]["domain_hash"],
            "domain_description": (
                "order-512 subgroup from the pinned F_17^32 row descriptor"
            ),
        },
        "agreement_range": [AGREEMENT_MIN, AGREEMENT_MAX],
        "construction": {
            "branch": "non_proportional_one_spike",
            "base_nodes": "first j+1 descriptor-domain points",
            "spike": "descriptor-domain point j+1",
            "u_m": "sum_{x in X} x^m",
            "v_m": "y^m",
            "regular_minor_shape": "C0(A)+Z*C1(A)",
            "shifted_minor_test": "row-shift-1 square minor",
            "projective_endpoint": "[0:1]",
        },
        "source_artifacts": [
            source_record("row_descriptor", ROW_DESCRIPTOR_REF, descriptor),
            source_record("one_spike_template", ONE_SPIKE_TEMPLATE_REF, template),
            source_record("one_spike_template_note", ONE_SPIKE_TEMPLATE_NOTE_REF),
            source_record(
                "shifted_minor_exclusion_criterion",
                SHIFTED_MINOR_CRITERION_REF,
            ),
            source_record(
                "endpoint_quotient_image_criterion",
                ENDPOINT_QUOTIENT_IMAGE_CRITERION_REF,
            ),
            source_record("one_spike_a426_packet", ONE_SPIKE_A426_PACKET_REF, a426_packet),
        ],
        "method": {
            "finite_regular_root": (
                "Cauchy-Binet rank-one update gives one finite first-minor root "
                "in every agreement row"
            ),
            "finite_full_hankel_column": (
                "the row-shift-1 minor is nonzero at that root, so the root is "
                "not an actual full-Hankel exact-support witness"
            ),
            "endpoint_column": (
                "the projective endpoint support D\\{y} is noncontained by "
                "Vandermonde independence"
            ),
            "endpoint_quotient_image": (
                "a c=2 quotient-remainder support of size A avoiding y gives "
                "a quotient-image witness for the endpoint"
            ),
        },
        "aggregate": aggregate,
        "deterministic_records": {
            "storage": "compressed; verifier rebuilds all 42 agreement rows",
            "record_count": len(records),
            "record_sha256": hash_json(records),
            "first_record": records[0],
            "last_record": records[-1],
        },
        "claim": (
            "For the non-proportional one-spike M3 branch over the pinned "
            "F_17^32 row and every A=385..426, the unique finite regular "
            "first-minor root is excluded by the shifted minor, and the only "
            "remaining projective full-Hankel contribution is the endpoint, "
            "which is charged to quotient-image.  The aperiodic full-Hankel "
            "projective residual upper bound is zero in every checked row."
        ),
        "nonclaims": [
            "synthetic one-spike branch only, not arbitrary M3 row data",
            "not a finite-root quotient-image/support audit; finite roots are removed by shifted-minor exclusion",
            "does not replace affine/projective/curve pivot charts for arbitrary singular buckets",
            "not a worst-case MCA threshold theorem",
        ],
    }


def check_certificate(certificate: dict[str, Any], path: Path) -> None:
    actual = path.read_text(encoding="utf-8")
    expected = render(certificate)
    if actual != expected:
        raise AssertionError(f"one-spike full-Hankel certificate mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    aggregate = certificate["aggregate"]
    print("F_17^32 M3 one-spike window full-Hankel ledger")
    print(f"status: {certificate['status']}")
    print(
        "records={records}, finite_roots={finite}, full_max={full}, aperiodic_max={aper}".format(
            records=aggregate["record_count"],
            finite=aggregate["finite_regular_root_count_sum"],
            full=aggregate[
                "max_full_hankel_projective_upper_before_endpoint_image_per_record"
            ],
            aper=aggregate[
                "max_aperiodic_full_hankel_projective_upper_per_record"
            ],
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", type=Path, help="write deterministic certificate")
    parser.add_argument("--check", type=Path, help="check deterministic certificate")
    parser.add_argument("--json", action="store_true", help="print certificate JSON")
    args = parser.parse_args()

    certificate = build_certificate()
    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(render(certificate), encoding="utf-8")
    if args.check:
        check_certificate(certificate, args.check)
    if args.json:
        print(render(certificate), end="")
        return
    print_summary(certificate)


if __name__ == "__main__":
    main()
