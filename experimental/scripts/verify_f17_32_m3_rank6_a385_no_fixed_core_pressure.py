#!/usr/bin/env python3
"""Verify the A=385 no-fixed-core external pair-core pressure lemma."""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from math import ceil, comb
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experimental.scripts.emit_f17_32_hankel_row_descriptor import K, N, P  # noqa: E402


SCHEMA_VERSION = "f17-32-m3-rank6-a385-no-fixed-core-pressure-v1"
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
DIRECTION_RANK_CAP_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-direction-rank-degree-cap/"
    "f17_32_n512_k256_m3_direction_rank_degree_cap.json"
)
PROJECTIVE_BUDGET_SPLIT_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-m4-projective-budget-split/"
    "f17_32_n512_k256_m3_m4_projective_budget_split.json"
)
FIXED_CORE_SYNTHESIS_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-rank6-a385-fixed-core-synthesis/"
    "f17_32_n512_k256_m3_rank6_a385_fixed_core_synthesis.json"
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


def minimum_pair_overlap(universe_size: int, total_incidence: int) -> int:
    """Minimum sum_s binom(m_s,2) over a universe with total multiplicity."""
    quotient, remainder = divmod(total_incidence, universe_size)
    return (universe_size - remainder) * comb(quotient, 2) + remainder * comb(
        quotient + 1, 2
    )


def pressure_row(total_base_roots: int) -> dict[str, int]:
    external_universe = N - (N - AGREEMENT + 1)
    split_locator_degree = N - AGREEMENT
    finite_class_count = FINITE_BUDGET
    pair_count = comb(finite_class_count, 2)
    external_incidence = finite_class_count * split_locator_degree - total_base_roots
    overlap_sum = minimum_pair_overlap(external_universe, external_incidence)
    return {
        "total_base_root_incidences": total_base_roots,
        "external_root_incidence_lower_bound": external_incidence,
        "pairwise_external_overlap_sum_lower_bound": overlap_sum,
        "some_pair_external_common_core_lower_bound": ceil(overlap_sum / pair_count),
    }


def build_certificate() -> dict[str, Any]:
    descriptor = load_json(ROW_DESCRIPTOR_REF)
    transfer = load_json(LOW_DEGREE_TRANSFER_REF)
    direction_cap = load_json(DIRECTION_RANK_CAP_REF)
    budget_split = load_json(PROJECTIVE_BUDGET_SPLIT_REF)
    fixed_core = load_json(FIXED_CORE_SYNTHESIS_REF)

    require(descriptor["row"]["n"] == N, "descriptor n mismatch")
    require(descriptor["row"]["k"] == K, "descriptor k mismatch")
    require(descriptor["row"]["field_order"] == Q_LINE, "descriptor q mismatch")
    require(
        transfer["schema_version"] == "f17-32-m3-rank6-boundary-low-degree-transfer-v1",
        "low-degree transfer schema mismatch",
    )
    require(AGREEMENT in transfer["window"]["agreements"], "A=385 missing in transfer")
    require(
        direction_cap["schema_version"] == "f17-32-m3-direction-rank-degree-cap-v1",
        "direction-rank cap schema mismatch",
    )
    require(
        budget_split["schema_version"] == "f17-32-m3-m4-projective-budget-split-v1",
        "projective budget split schema mismatch",
    )
    require(
        fixed_core["schema_version"] == "f17-32-m3-rank6-a385-fixed-core-synthesis-v1",
        "fixed-core synthesis schema mismatch",
    )
    require(
        fixed_core["summary"]["fixed_base_core_size_at_least_two_projective_safe"],
        "fixed-core synthesis unavailable",
    )
    require(N % P != 0, "X^512-1 is not separable in this characteristic")
    require(FINITE_BUDGET == 6 and PROJECTIVE_BUDGET == 6, "unexpected budgets")

    transfer_record = next(
        record for record in transfer["agreement_records"] if record["A"] == AGREEMENT
    )
    budget_record = next(
        record for record in budget_split["agreement_records"] if record["A"] == AGREEMENT
    )
    direction_record = next(
        record for record in direction_cap["agreement_records"] if record["A"] == AGREEMENT
    )

    j_value = N - AGREEMENT
    t_value = AGREEMENT - K
    m_value = j_value + 1
    h_value = transfer_record["boundary_defect_h"]
    external_universe = N - m_value
    finite_class_count = FINITE_BUDGET
    finite_pair_count = comb(finite_class_count, 2)
    base_root_cap_per_class = h_value - 1
    max_total_base_roots = finite_class_count * base_root_cap_per_class
    worst_pressure = pressure_row(max_total_base_roots)
    pressure_table = [pressure_row(total) for total in range(max_total_base_roots + 1)]

    require(j_value == 127 and t_value == 129 and m_value == 128, "A385 dimensions changed")
    require(h_value == 5, "A385 low-degree defect changed")
    require(external_universe == 384, "A385 external universe changed")
    require(base_root_cap_per_class == 4, "A385 base-root cap changed")
    require(max_total_base_roots == 24, "A385 six-class base incidence cap changed")
    require(
        direction_record["finite_root_count_cap"]
        == "at most r finite roots before paid-ledger subtraction",
        "direction cap statement changed",
    )
    require(
        budget_record["endpoint_sensitive_direction_rank"] == RANK
        and budget_record["projective_budget"] == PROJECTIVE_BUDGET,
        "projective budget record mismatch",
    )
    require(
        worst_pressure["external_root_incidence_lower_bound"] == 738,
        "external incidence lower bound changed",
    )
    require(
        worst_pressure["pairwise_external_overlap_sum_lower_bound"] == 354,
        "pair-overlap lower bound changed",
    )
    require(
        worst_pressure["some_pair_external_common_core_lower_bound"] == 24,
        "pair-core lower bound changed",
    )

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT",
        "object": (
            "A=385 separated rank-6 no-fixed-core external pair-core pressure"
        ),
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
            "direction_rank_degree_cap": {
                "ref": DIRECTION_RANK_CAP_REF,
                "sha256": sha256_file(DIRECTION_RANK_CAP_REF),
            },
            "m4_projective_budget_split": {
                "ref": PROJECTIVE_BUDGET_SPLIT_REF,
                "sha256": sha256_file(PROJECTIVE_BUDGET_SPLIT_REF),
            },
            "a385_fixed_core_synthesis": {
                "ref": FIXED_CORE_SYNTHESIS_REF,
                "sha256": sha256_file(FIXED_CORE_SYNTHESIS_REF),
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
                "After the A=385 fixed-core synthesis, any remaining separated "
                "rank-6 branch that is projectively over budget must contain "
                "two finite split-locator classes sharing at least 24 external "
                "subgroup roots."
            ),
            "finite_root_saturation": (
                "The direction-rank degree cap gives at most six finite affine "
                "roots in a rank-6 regular bucket.  Since the projective budget "
                "is also six and there is at most one projective endpoint, any "
                "projective over-budget survivor must have exactly six distinct "
                "finite noncontained classes and an unpaid endpoint."
            ),
            "base_root_cap": (
                "At A=385 the low-degree transfer has deg Q<5.  On the base "
                "support, L_Q(x)=0 iff Q(x)=0, so each nonzero finite class has "
                "at most four base-support roots."
            ),
            "external_incidence": (
                "Six degree-127 split locators therefore have at most 24 total "
                "base-root incidences and at least 738 external-root incidences "
                "inside the 384-point external subgroup complement."
            ),
            "pair_core_pressure": (
                "Distributing 738 incidences over 384 external points gives "
                "sum_{i<j}|E_i cap E_j| >= 354.  Since there are 15 pairs of "
                "finite classes, one pair has external intersection at least 24."
            ),
            "contrapositive_use": (
                "A separated A=385 branch with no fixed two-point base core and "
                "with every pair of finite classes sharing at most 23 external "
                "roots is projective-budget safe."
            ),
        },
        "pressure_profile": {
            "finite_classes_required_for_projective_overbudget": finite_class_count,
            "projective_endpoint_must_be_unpaid": True,
            "base_root_cap_per_finite_class": base_root_cap_per_class,
            "max_total_base_root_incidences": max_total_base_roots,
            "external_root_incidence_lower_bound": worst_pressure[
                "external_root_incidence_lower_bound"
            ],
            "external_universe_size": external_universe,
            "pairwise_external_overlap_sum_lower_bound": worst_pressure[
                "pairwise_external_overlap_sum_lower_bound"
            ],
            "finite_class_pair_count": finite_pair_count,
            "some_pair_external_common_core_lower_bound": worst_pressure[
                "some_pair_external_common_core_lower_bound"
            ],
        },
        "base_incidence_pressure_table": pressure_table,
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
            "fixed_core_synthesis_consumed": True,
            "finite_classes_required_for_projective_overbudget": finite_class_count,
            "base_root_cap_per_class": base_root_cap_per_class,
            "max_total_base_roots_across_six_classes": max_total_base_roots,
            "external_root_incidence_lower_bound": worst_pressure[
                "external_root_incidence_lower_bound"
            ],
            "pairwise_external_overlap_sum_lower_bound": worst_pressure[
                "pairwise_external_overlap_sum_lower_bound"
            ],
            "some_pair_external_common_core_lower_bound": worst_pressure[
                "some_pair_external_common_core_lower_bound"
            ],
            "safe_if_all_pair_external_common_cores_at_most": (
                worst_pressure["some_pair_external_common_core_lower_bound"] - 1
            ),
        },
        "checks": [
            "row descriptor and dependency schemas match",
            "A=385 has j=127, m=128, h=5, and 384 external subgroup points",
            "direction-rank cap bounds finite roots by six",
            "projective-budget split makes rank six endpoint-sensitive",
            "fixed-core synthesis removes all fixed base cores of size at least two",
            "low-degree transfer caps base roots at four per finite class",
            "six finite degree-127 split locators require at least 738 external-root incidences",
            "external occupancy forces pairwise overlap sum at least 354",
            "one pair of finite classes must share at least 24 external roots",
        ],
        "nonclaims": [
            "does not close the no-fixed-core A=385 frontier",
            "does not prove existence of a no-fixed-core over-budget witness",
            "does not classify overlapping-support rank-6 pencils",
            "does not prove the projective endpoint is unpaid",
            "does not prove that a large external pair-core is quotient-paid or impossible",
            "does not compute arbitrary A=385 rank-6 root tables",
            "does not produce a row-level M3 safe-side bound",
        ],
    }


def check_certificate(path: Path, certificate: dict[str, Any]) -> None:
    expected = render(certificate)
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"A=385 no-fixed-core pressure mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    summary = certificate["summary"]
    print("F_17^32 M3 rank-6 A=385 no-fixed-core pressure")
    print(
        "external incidences>={external_root_incidence_lower_bound}; pair-core>={some_pair_external_common_core_lower_bound}".format(
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
