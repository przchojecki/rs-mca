#!/usr/bin/env python3
"""Verify the A=385 large pair-core quotient reduction."""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experimental.scripts.emit_f17_32_hankel_row_descriptor import K, N, P  # noqa: E402


SCHEMA_VERSION = "f17-32-m3-rank6-a385-pair-core-quotient-reduction-v1"
Q_LINE = 17**32
TARGET_BITS = 128
FINITE_BUDGET = Q_LINE // 2**TARGET_BITS
PROJECTIVE_DENOMINATOR = Q_LINE + 1
PROJECTIVE_BUDGET = PROJECTIVE_DENOMINATOR // 2**TARGET_BITS
AGREEMENT = 385
RANK = 6
ROW_DESCRIPTOR_REF = (
    "experimental/data/certificates/hankel-f17-32-row-descriptor/"
    "f17_32_n512_k256_hankel_row_descriptor.json"
)
LOW_DEGREE_TRANSFER_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-rank6-boundary-low-degree-transfer/"
    "f17_32_n512_k256_m3_rank6_boundary_low_degree_transfer.json"
)
NO_FIXED_CORE_PRESSURE_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-rank6-a385-no-fixed-core-pressure/"
    "f17_32_n512_k256_m3_rank6_a385_no_fixed_core_pressure.json"
)
NULLPOLY_SPLIT_GATE_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-nullpolynomial-split-locator-gate/"
    "f17_32_n512_k256_m3_nullpolynomial_split_locator_gate.json"
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


def quotient_row(common_external_core_size: int) -> dict[str, Any]:
    j_value = N - AGREEMENT
    quotient_strict_degree_bound = (j_value + 1) - common_external_core_size
    split_quotient_degree = j_value - common_external_core_size
    return {
        "common_external_core_size": common_external_core_size,
        "ambient_quotient_degree_bound": f"deg R < {quotient_strict_degree_bound}",
        "ambient_quotient_vector_dimension_at_most": max(quotient_strict_degree_bound, 0),
        "split_quotient_degree": split_quotient_degree,
        "remaining_subgroup_size_after_core": N - common_external_core_size,
        "quotient_divisor": "(X^512-1)/C_E",
    }


def build_certificate() -> dict[str, Any]:
    descriptor = load_json(ROW_DESCRIPTOR_REF)
    transfer = load_json(LOW_DEGREE_TRANSFER_REF)
    pressure = load_json(NO_FIXED_CORE_PRESSURE_REF)
    split_gate = load_json(NULLPOLY_SPLIT_GATE_REF)

    require(descriptor["row"]["n"] == N, "descriptor n mismatch")
    require(descriptor["row"]["k"] == K, "descriptor k mismatch")
    require(descriptor["row"]["field_order"] == Q_LINE, "descriptor q mismatch")
    require(
        transfer["schema_version"] == "f17-32-m3-rank6-boundary-low-degree-transfer-v1",
        "low-degree transfer schema mismatch",
    )
    require(
        pressure["schema_version"] == "f17-32-m3-rank6-a385-no-fixed-core-pressure-v1",
        "no-fixed-core pressure schema mismatch",
    )
    require(
        split_gate["schema_version"] == "f17-32-m3-nullpolynomial-split-locator-gate-v1",
        "split-locator gate schema mismatch",
    )
    require(split_gate["summary"]["split_locator_gate_available"], "split gate unavailable")
    require(N % P != 0, "X^512-1 is not separable in this characteristic")
    require(FINITE_BUDGET == 6 and PROJECTIVE_BUDGET == 6, "unexpected budgets")

    transfer_record = next(
        record for record in transfer["agreement_records"] if record["A"] == AGREEMENT
    )
    j_value = N - AGREEMENT
    t_value = AGREEMENT - K
    m_value = j_value + 1
    h_value = transfer_record["boundary_defect_h"]
    pair_core_min = pressure["summary"]["some_pair_external_common_core_lower_bound"]
    external_universe = N - m_value
    quotient_at_min = quotient_row(pair_core_min)
    quotient_table = [quotient_row(value) for value in [pair_core_min, 64, 96, 122, 127]]

    require(j_value == 127 and t_value == 129 and m_value == 128, "A385 dimensions changed")
    require(h_value == 5, "A385 low-degree defect changed")
    require(external_universe == 384, "A385 external universe changed")
    require(pair_core_min == 24, "pair-core minimum changed")
    require(
        pressure["summary"]["finite_classes_required_for_projective_overbudget"] == 6,
        "pressure packet no longer exposes six finite classes",
    )
    require(
        quotient_at_min["ambient_quotient_vector_dimension_at_most"] == 104,
        "ambient quotient dimension at pair-core minimum changed",
    )
    require(
        quotient_at_min["split_quotient_degree"] == 103,
        "split quotient degree at pair-core minimum changed",
    )

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT",
        "object": "A=385 separated rank-6 large pair-core quotient reduction",
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
            "rank6_boundary_low_degree_transfer": {
                "ref": LOW_DEGREE_TRANSFER_REF,
                "sha256": sha256_file(LOW_DEGREE_TRANSFER_REF),
            },
            "a385_no_fixed_core_pressure": {
                "ref": NO_FIXED_CORE_PRESSURE_REF,
                "sha256": sha256_file(NO_FIXED_CORE_PRESSURE_REF),
            },
            "nullpolynomial_split_locator_gate": {
                "ref": NULLPOLY_SPLIT_GATE_REF,
                "sha256": sha256_file(NULLPOLY_SPLIT_GATE_REF),
            },
        },
        "agreement": {
            "A": AGREEMENT,
            "j": j_value,
            "t": t_value,
            "m": m_value,
            "direction_rank": RANK,
            "boundary_defect_h": h_value,
            "projective_Q_search_dimension": h_value - 1,
            "split_locator_degree": j_value,
            "external_subgroup_size": external_universe,
        },
        "theorem": {
            "statement": (
                "Any separated A=385 rank-6 no-fixed-core over-budget survivor "
                "has a pair of finite classes whose projective Q-line factors "
                "through a common external quotient core of size at least 24."
            ),
            "pair_from_pressure": (
                "The no-fixed-core pressure packet supplies two finite "
                "split-locator classes Q0,Q1 with a common external root set "
                "E of size at least 24."
            ),
            "linearity": (
                "The low-degree transfer map Q -> L_Q is linear.  Therefore if "
                "L_Q0(s)=L_Q1(s)=0 for every s in E, then every Q in the line "
                "<Q0,Q1> satisfies L_Q(s)=0 for every s in E."
            ),
            "quotient_factorization": (
                "Let C_E=prod_{s in E}(T-s).  Since E is external to the base "
                "support, C_E is nonzero on X; since L_Q has degree <128 and "
                "vanishes on E for every Q in the pair line, L_Q=C_E R_Q with "
                "deg R_Q < 128-|E|."
            ),
            "split_quotient_gate": (
                "For the two actual split-locator classes, L_Q is a monic "
                "degree-127 divisor of X^512-1 after normalization.  Hence "
                "R_Q is a degree 127-|E| divisor of (X^512-1)/C_E."
            ),
            "large_core_consequence": (
                "At the guaranteed |E|>=24, the ambient quotient family has "
                "vector dimension at most 104 and the two split quotient "
                "members have degree at most 103."
            ),
            "next_target": (
                "Thus the no-fixed-core frontier reduces to excluding or paying "
                "a projective quotient pencil containing two distinct full-split "
                "degree<=103 quotient members."
            ),
        },
        "quotient_profile_at_min_pair_core": quotient_at_min,
        "quotient_profile_table": quotient_table,
        "sampler_denominators": {
            "finite_line": {
                "denominator": Q_LINE,
                "denominator_formula": "|F|",
                "budget_floor_denominator_over_2_128": FINITE_BUDGET,
            },
            "projective_line": {
                "denominator": PROJECTIVE_DENOMINATOR,
                "denominator_formula": "|P^1(F)| = |F| + 1",
                "budget_floor_denominator_over_2_128": PROJECTIVE_BUDGET,
            },
        },
        "summary": {
            "agreement": AGREEMENT,
            "pressure_packet_consumed": True,
            "pair_core_min": pair_core_min,
            "finite_classes_in_pair": 2,
            "quotient_pencil_projective_dimension": 1,
            "ambient_quotient_vector_dimension_at_pair_core_min": (
                quotient_at_min["ambient_quotient_vector_dimension_at_most"]
            ),
            "split_quotient_degree_at_pair_core_min": quotient_at_min[
                "split_quotient_degree"
            ],
            "large_pair_core_quotient_reduction_available": True,
        },
        "checks": [
            "row descriptor and dependency schemas match",
            "A=385 dimensions are j=127, m=128, h=5",
            "no-fixed-core pressure supplies pair-core size at least 24",
            "Q -> L_Q is linear on the low-degree transfer space",
            "a common external core on two finite classes factors every locator in their Q-line",
            "at pair-core size 24 the ambient quotient degree bound is deg R<104",
            "at pair-core size 24 the two split quotient locators have degree at most 103",
        ],
        "nonclaims": [
            "does not close the no-fixed-core A=385 frontier",
            "does not prove the large pair-core quotient pencil is empty",
            "does not prove the large pair-core quotient pencil is paid",
            "does not classify overlapping-support rank-6 pencils",
            "does not prove the projective endpoint is unpaid",
            "does not compute arbitrary A=385 rank-6 root tables",
            "does not produce a row-level M3 safe-side bound",
        ],
    }


def check_certificate(path: Path, certificate: dict[str, Any]) -> None:
    expected = render(certificate)
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"A=385 pair-core quotient reduction mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    summary = certificate["summary"]
    print("F_17^32 M3 rank-6 A=385 pair-core quotient reduction")
    print(
        "pair core>={pair_core_min}; split quotient degree<={split_quotient_degree_at_pair_core_min}".format(
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
        check_certificate(args.check, certificate)
    print_summary(certificate)


if __name__ == "__main__":
    main()
