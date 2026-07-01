#!/usr/bin/env python3
"""Emit a concrete F_17^32 M3 rank-witness regular-minor input.

This is a stress input for the Paper D v9 regular-window pipeline.  It uses the
pinned F_17^32 row descriptor and builds a synthetic syndrome pencil at a
selected exact agreement A.  The construction is deliberately simple:

    u_m = 0,
    v_m = sum_i x_i^m,

where x_i are the first j+1 domain elements from the descriptor.  At slope 1 the
prefix Hankel minor is Z^(j+1) times a shifted Vandermonde square, so the
extractor can emit the closed-form synthetic root table {0} from the prefix
row set without determinant interpolation.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from experimental.scripts.emit_f17_32_hankel_row_descriptor import (
    Field,
    K,
    MODULUS,
    N,
    P,
)


DEFAULT_AGREEMENT = 426
ROW_DESCRIPTOR = REPO_ROOT / (
    "experimental/data/certificates/hankel-f17-32-row-descriptor/"
    "f17_32_n512_k256_hankel_row_descriptor.json"
)
OUTPUT_PATH = REPO_ROOT / (
    "experimental/data/hankel-regular-minor-inputs/"
    "f17_32_n512_k256_a426_rank_witness_input.json"
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def render(value: dict[str, Any]) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def power_sum_syndrome(
    field: Field,
    nodes: list[tuple[int, ...]],
    length: int,
) -> list[int]:
    syndrome = []
    powers = [field.one for _ in nodes]
    for exponent in range(length):
        total = field.zero
        if exponent == 0:
            total = field.normalize(len(nodes))
        else:
            for power in powers:
                total = tuple(
                    (total[index] + power[index]) % field.p
                    for index in range(field.degree)
                )
        syndrome.append(field.encode(total))
        powers = [field.mul(power, node) for power, node in zip(powers, nodes)]
    return syndrome


def build_input(
    agreement: int = DEFAULT_AGREEMENT,
    agreement_max: int | None = None,
    witness_prefix_count: int | None = None,
    syndrome_scalar: int = 0,
    minor_gcd_contiguous_limit: int | None = None,
    one_spike_linear: bool = False,
    low_rank_update_count: int | None = None,
) -> dict[str, Any]:
    descriptor = load_json(ROW_DESCRIPTOR)
    field = Field(P, MODULUS)
    low_rank_update = low_rank_update_count is not None
    if low_rank_update_count is not None and low_rank_update_count <= 0:
        raise ValueError("low-rank update count must be positive")
    if one_spike_linear and low_rank_update:
        raise ValueError("choose either one-spike or low-rank update mode")
    if agreement_max is not None and agreement_max < agreement:
        raise ValueError("agreement-max must be at least agreement")
    agreements = list(range(agreement, (agreement_max or agreement) + 1))
    j_value = N - agreement
    t_value = agreement - K
    size = j_value + 1
    prefix_count = witness_prefix_count or size
    if one_spike_linear:
        if agreement_max is not None:
            raise ValueError("one-spike linear input currently supports one agreement")
        if syndrome_scalar:
            raise ValueError("one-spike linear input is not a scalar-multiple mode")
        if minor_gcd_contiguous_limit is not None:
            raise ValueError("one-spike linear input is not a minor-gcd mode")
        prefix_count = size + 1
    if low_rank_update:
        if agreement_max is not None:
            raise ValueError("low-rank update input currently supports one agreement")
        if syndrome_scalar:
            raise ValueError("low-rank update input is not a scalar-multiple mode")
        if minor_gcd_contiguous_limit is not None:
            raise ValueError("low-rank update input is not a minor-gcd mode")
        assert low_rank_update_count is not None
        prefix_count = size + low_rank_update_count
    if prefix_count < size:
        raise ValueError("witness prefix count must cover the largest minor")
    if t_value < size:
        raise ValueError("selected agreement is not regular overdetermined")
    length = t_value + j_value
    if length > N - K:
        raise ValueError("selected agreement needs more syndrome entries than n-k")

    domain_encodings = descriptor["domain"]["domain_encodings"]
    if prefix_count > len(domain_encodings):
        raise ValueError("witness prefix count exceeds the pinned domain size")
    nodes = [field.decode(value) for value in domain_encodings[:prefix_count]]
    if one_spike_linear:
        base_nodes = nodes[:size]
        spike_node = nodes[size]
        u_syndrome = power_sum_syndrome(field, base_nodes, length)
        v_syndrome = power_sum_syndrome(field, [spike_node], length)
        scalar = field.zero
        proportional = False
    elif low_rank_update:
        assert low_rank_update_count is not None
        base_nodes = nodes[:size]
        update_nodes = nodes[size : size + low_rank_update_count]
        u_syndrome = power_sum_syndrome(field, base_nodes, length)
        v_syndrome = power_sum_syndrome(field, update_nodes, length)
        scalar = field.zero
        proportional = False
    else:
        v_syndrome = power_sum_syndrome(field, nodes, length)
        scalar = field.normalize(syndrome_scalar)
        u_syndrome = [
            field.encode(field.mul(scalar, field.decode(value))) for value in v_syndrome
        ]
        proportional = any(value != 0 for value in scalar)
    if minor_gcd_contiguous_limit is not None and proportional:
        raise ValueError("minor-gcd closed form currently requires syndrome-scalar 0")
    if minor_gcd_contiguous_limit is not None and minor_gcd_contiguous_limit <= 0:
        raise ValueError("minor-gcd contiguous limit must be positive")
    if one_spike_linear:
        domain_description = (
            "order-512 subgroup from the pinned F_17^32 row descriptor; "
            "synthetic M3 one-spike syndrome uses the first j+1 elements "
            "and the next descriptor-domain element as spike"
        )
    elif low_rank_update:
        assert low_rank_update_count is not None
        domain_description = (
            "order-512 subgroup from the pinned F_17^32 row descriptor; "
            "synthetic M3 low-rank update syndrome uses the first j+1 "
            f"elements and the next {low_rank_update_count} descriptor-domain "
            "elements as update nodes"
        )
    elif agreement_max is None:
        domain_description = (
            "order-512 subgroup from the pinned F_17^32 row descriptor; "
            "synthetic M3 rank-witness syndrome uses the first j+1 elements"
        )
    else:
        domain_description = (
            "order-512 subgroup from the pinned F_17^32 row descriptor; "
            f"fixed synthetic M3 window syndrome uses the first {prefix_count} elements"
        )
    if one_spike_linear:
        line_description = (
            "synthetic M3 one-spike linear witness: "
            f"u_m=sum_i x_i^m for the first {size} descriptor-domain elements "
            f"and v_m=y^m for descriptor-domain element {size}"
        )
    elif low_rank_update:
        assert low_rank_update_count is not None
        line_description = (
            "synthetic M3 low-rank update witness: "
            f"u_m=sum_i x_i^m for the first {size} descriptor-domain elements "
            f"and v_m=sum_i y_i^m for the next {low_rank_update_count} "
            "descriptor-domain elements"
        )
    elif proportional:
        line_description = (
            f"synthetic M3 proportional witness: u={syndrome_scalar}*v and "
            f"v_m=sum_i x_i^m for the first {prefix_count} descriptor-domain elements"
        )
    elif agreement_max is None:
        line_description = (
            "synthetic M3 rank witness: u=0 and v_m=sum_i x_i^m for "
            "the first j+1 descriptor-domain elements"
        )
    else:
        line_description = (
            "fixed synthetic M3 window witness: u=0 and v_m=sum_i x_i^m for "
            f"the first {prefix_count} descriptor-domain elements"
        )
    line_syndrome = {
        "u": u_syndrome,
        "v": v_syndrome,
        "field_encoding": "base-p low-to-high integer",
        "description": line_description,
        "length": length,
        "witness_slope": 1,
        "witness_node_prefix_count": prefix_count,
        "rank_witness_reason": (
            "one-spike Cauchy-Binet rank-one update makes the prefix "
            "determinant affine in the slope"
            if one_spike_linear
            else (
                "low-rank Cauchy-Binet update makes the prefix determinant "
                "degree-bounded by the update rank"
                if low_rank_update
                else (
                    "u=c*v makes the prefix determinant a nonzero scalar multiple "
                    "of (Z+c)^(j+1)"
                    if proportional
                    else "u=0 makes the prefix determinant a nonzero monomial in the slope"
                )
            )
        ),
    }
    if proportional:
        line_syndrome["scalar_multiple_u_over_v"] = field.encode(scalar)
        line_syndrome["tangent_root"] = field.encode(
            tuple((-coeff) % field.p for coeff in scalar)
        )
    packet = {
        "schema_version": "regular-hankel-minor-extractor-input-v1",
        "row": {
            "n": N,
            "k": K,
            "field": "F_17^32",
            "domain_hash": descriptor["row"]["domain_hash"],
            "domain_description": domain_description,
        },
        "field_model": {
            "kind": "polynomial_basis",
            "p": P,
            "degree": field.degree,
            "modulus": MODULUS,
            "encoding": "base-p low-to-high coefficients",
        },
        "agreement_threshold": agreement,
        "exact_agreements": agreements,
        "sampler": "finite_affine_line",
        "certificate_mode": "minor_gcd_roots"
        if minor_gcd_contiguous_limit is not None
        else (
            "one_spike_linear_roots"
            if one_spike_linear
            else (
                "low_rank_update_bound"
                if low_rank_update
                else (
                    "scalar_multiple_roots"
                    if proportional
                    else "zero_u_monomial_roots"
                )
            )
        ),
        "line_syndrome": line_syndrome,
        "row_set_strategy": (
            {"type": "contiguous", "limit": minor_gcd_contiguous_limit}
            if minor_gcd_contiguous_limit is not None
            else {"type": "prefix"}
        ),
        "emit_split_root_certificate": True,
        "status": "PROVED / AUDIT",
        "nonclaims": [
            "synthetic syndrome pencil only",
            "not a worst-case MCA row bound",
            "not a worst-case row root table over F_17^32",
            "not a quotient/tangent subtraction table",
        ],
    }
    if minor_gcd_contiguous_limit is not None:
        packet["minor_gcd_method"] = "zero_u_monomial"
        packet["claim_scope"] = {
            "row_data": "synthetic_syndrome_pencil",
            "threshold_role": "synthetic_stress",
            "root_status": "closed_form",
            "may_be_used_for_threshold_pinning": False,
            "note": (
                "Closed-form common-gcd replay for a contiguous row-set family; "
                "the unique root is the zero-codeword tangent slope, not an "
                "aperiodic row bound."
            ),
        }
    if proportional:
        packet["claim_scope"] = {
            "row_data": "synthetic_syndrome_pencil",
            "threshold_role": "synthetic_stress",
            "root_status": "closed_form",
            "may_be_used_for_threshold_pinning": False,
            "note": (
                "Proportional-pencil closed-form replay; the unique root is "
                "a tangent/common-code-line slope, not an aperiodic row bound."
            ),
        }
    if one_spike_linear:
        packet["one_spike_linear"] = {
            "base_node_encodings": domain_encodings[:size],
            "spike_encoding": domain_encodings[size],
            "coefficient_formula": "Cauchy-Binet Vandermonde-square rank-one update",
        }
        packet["claim_scope"] = {
            "row_data": "synthetic_syndrome_pencil",
            "threshold_role": "synthetic_stress",
            "root_status": "closed_form",
            "may_be_used_for_threshold_pinning": False,
            "note": (
                "Non-proportional one-spike closed-form replay; this is a "
                "synthetic packet and not an actual-row MCA bound."
            ),
        }
    if low_rank_update:
        assert low_rank_update_count is not None
        packet["low_rank_update"] = {
            "base_node_encodings": domain_encodings[:size],
            "update_node_encodings": domain_encodings[
                size : size + low_rank_update_count
            ],
            "coefficient_formula": "Cauchy-Binet Vandermonde-square low-rank update",
        }
        root_status = (
            "closed_form"
            if low_rank_update_count == 2
            else "degree_bound_only"
        )
        packet["claim_scope"] = {
            "row_data": "synthetic_syndrome_pencil",
            "threshold_role": "synthetic_stress",
            "root_status": root_status,
            "may_be_used_for_threshold_pinning": False,
            "note": (
                "Non-proportional low-rank update closed-form replay; this "
                "emits exact roots when the low-rank polynomial is split and "
                "otherwise remains a degree-bound certificate."
            ),
        }
    return packet


def check_input(
    path: Path,
    agreement: int,
    agreement_max: int | None,
    witness_prefix_count: int | None,
    syndrome_scalar: int,
    minor_gcd_contiguous_limit: int | None,
    one_spike_linear: bool,
    low_rank_update_count: int | None,
) -> None:
    expected = render(
        build_input(
            agreement,
            agreement_max,
            witness_prefix_count,
            syndrome_scalar,
            minor_gcd_contiguous_limit,
            one_spike_linear,
            low_rank_update_count,
        )
    )
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"rank-witness input mismatch: {path}")


def print_summary(packet: dict[str, Any]) -> None:
    row = packet["row"]
    agreements = packet["exact_agreements"]
    agreement = agreements[0]
    j_value = row["n"] - agreement
    t_value = agreement - row["k"]
    print("F_17^32 M3 rank-witness extractor input")
    print(
        "row: {field}, n={n}, k={k}, A={agreement}, j={j}, t={t}".format(
            agreement=agreement,
            j=j_value,
            t=t_value,
            **row,
        )
    )
    if len(agreements) > 1:
        print(f"agreement_window={agreements[0]}..{agreements[-1]}")
    print(
        "syndrome_length={length}, witness_prefix={prefix}, mode={mode}".format(
            length=packet["line_syndrome"]["length"],
            prefix=packet["line_syndrome"]["witness_node_prefix_count"],
            mode=packet["certificate_mode"],
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--agreement", type=int, default=DEFAULT_AGREEMENT)
    parser.add_argument("--agreement-max", type=int)
    parser.add_argument("--witness-prefix-count", type=int)
    parser.add_argument(
        "--syndrome-scalar",
        type=int,
        default=0,
        help="emit the proportional pencil u=c*v; default c=0 keeps zero-u mode",
    )
    parser.add_argument(
        "--minor-gcd-contiguous-limit",
        type=int,
        help=(
            "emit minor_gcd_roots with zero_u_monomial closed form over the "
            "first LIMIT contiguous row sets"
        ),
    )
    parser.add_argument(
        "--one-spike-linear",
        action="store_true",
        help=(
            "emit a non-proportional one-spike linear pencil with "
            "u_m=sum x_i^m and v_m=y^m"
        ),
    )
    parser.add_argument(
        "--low-rank-update-count",
        type=int,
        help=(
            "emit a non-proportional low-rank update pencil with COUNT "
            "descriptor-domain update nodes"
        ),
    )
    parser.add_argument("--write", type=Path, help="write deterministic input JSON")
    parser.add_argument("--check", type=Path, help="check deterministic input JSON")
    parser.add_argument("--json", action="store_true", help="print input JSON")
    args = parser.parse_args()

    packet = build_input(
        args.agreement,
        args.agreement_max,
        args.witness_prefix_count,
        args.syndrome_scalar,
        args.minor_gcd_contiguous_limit,
        args.one_spike_linear,
        args.low_rank_update_count,
    )
    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(render(packet), encoding="utf-8")
    if args.check:
        check_input(
            args.check,
            args.agreement,
            args.agreement_max,
            args.witness_prefix_count,
            args.syndrome_scalar,
            args.minor_gcd_contiguous_limit,
            args.one_spike_linear,
            args.low_rank_update_count,
        )
    if args.json:
        print(render(packet), end="")
        return
    print_summary(packet)


if __name__ == "__main__":
    main()
