#!/usr/bin/env python3
"""Verify the A=385 pair-core external-evaluation rank-test normal form."""

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

from experimental.scripts.emit_f17_32_hankel_row_descriptor import K, N  # noqa: E402


SCHEMA_VERSION = "f17-32-m3-rank6-a385-pair-core-rank-test-v1"
Q_LINE = 17**32
TARGET_BITS = 128
BUDGET = Q_LINE // 2**TARGET_BITS
PROJECTIVE_BUDGET = (Q_LINE + 1) // 2**TARGET_BITS
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
PAIR_CORE_QUOTIENT_REF = (
    "experimental/data/certificates/"
    "hankel-f17-32-m3-rank6-a385-pair-core-quotient-reduction/"
    "f17_32_n512_k256_m3_rank6_a385_pair_core_quotient_reduction.json"
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


def build_certificate() -> dict[str, Any]:
    descriptor = load_json(ROW_DESCRIPTOR_REF)
    transfer = load_json(LOW_DEGREE_TRANSFER_REF)
    quotient = load_json(PAIR_CORE_QUOTIENT_REF)

    require(descriptor["row"]["n"] == N, "descriptor n mismatch")
    require(descriptor["row"]["k"] == K, "descriptor k mismatch")
    require(descriptor["row"]["field_order"] == Q_LINE, "descriptor q mismatch")
    require(
        transfer["schema_version"] == "f17-32-m3-rank6-boundary-low-degree-transfer-v1",
        "low-degree transfer schema mismatch",
    )
    require(
        quotient["schema_version"]
        == "f17-32-m3-rank6-a385-pair-core-quotient-reduction-v1",
        "pair-core quotient schema mismatch",
    )
    require(BUDGET == 6 and PROJECTIVE_BUDGET == 6, "unexpected budget")

    transfer_record = next(
        record for record in transfer["agreement_records"] if record["A"] == AGREEMENT
    )
    j_value = N - AGREEMENT
    t_value = AGREEMENT - K
    m_value = j_value + 1
    support_size = m_value + RANK
    h_value = support_size - t_value
    q_vector_dimension = h_value
    q_projective_dimension = q_vector_dimension - 1
    pair_line_vector_dimension = 2
    annihilator_vector_dimension = q_vector_dimension - pair_line_vector_dimension
    rank_for_pair_line = annihilator_vector_dimension
    pair_core_min = quotient["summary"]["pair_core_min"]

    require(j_value == 127, "A385 j changed")
    require(t_value == 129, "A385 t changed")
    require(m_value == 128, "A385 m changed")
    require(h_value == 5, "A385 boundary defect changed")
    require(
        transfer_record["boundary_defect_h"] == h_value,
        "transfer record h mismatch",
    )
    require(
        transfer_record["finite_root_transfer"]["projective_Q_search_dimension"]
        == q_projective_dimension,
        "A385 Q projective dimension mismatch",
    )
    require(pair_core_min == 24, "pair-core minimum changed")
    require(rank_for_pair_line == 3, "rank threshold changed")

    fixed_two_core_residual_dimension = 3
    fixed_two_core_line_annihilator_dimension = (
        fixed_two_core_residual_dimension - pair_line_vector_dimension
    )
    require(
        fixed_two_core_line_annihilator_dimension == 1,
        "fixed two-core comparison dimension changed",
    )

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT",
        "object": "A=385 separated rank-6 pair-core external-evaluation rank test",
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
            "a385_pair_core_quotient_reduction": {
                "ref": PAIR_CORE_QUOTIENT_REF,
                "sha256": sha256_file(PAIR_CORE_QUOTIENT_REF),
            },
        },
        "agreement": {
            "A": AGREEMENT,
            "j": j_value,
            "t": t_value,
            "m": m_value,
            "direction_rank": RANK,
            "combined_support_size": support_size,
            "boundary_defect_h": h_value,
            "Q_vector_dimension": q_vector_dimension,
            "Q_projective_dimension": q_projective_dimension,
            "pair_line_vector_dimension": pair_line_vector_dimension,
            "pair_line_projective_dimension": 1,
            "pair_core_min": pair_core_min,
        },
        "rank_test": {
            "external_evaluation_functional": (
                "For an external subgroup point s, ev_s is the linear "
                "functional on the degree-<5 Q-space given by ev_s(Q)=L_Q(s)."
            ),
            "matrix": (
                "For E={s_1,...,s_e}, form the e x 5 external-evaluation "
                "matrix M_E whose i-th row is ev_{s_i} in any Q-basis."
            ),
            "necessary_condition": (
                "If a projective Q-line U supplies two finite classes sharing "
                "the external core E, then ev_s vanishes on U for every s in E; "
                "therefore rowspan(M_E) is contained in U^perp and rank(M_E)<=3."
            ),
            "linear_converse": (
                "Conversely, rank(M_E)<=3 gives dim ker(M_E)>=2, hence at least "
                "one projective Q-line whose transferred locators vanish on E.  "
                "This converse only supplies the linear common-core condition."
            ),
            "minor_form": (
                "The rank<=3 condition is equivalent to vanishing of every "
                "4 x 4 minor of M_E."
            ),
            "closure_target": (
                "A no-fixed-core over-budget survivor must therefore exhibit a "
                "24-point external set E with rank(M_E)<=3, plus two distinct "
                "kernel-line points passing the split-locator, quotient-divisor, "
                "and finite noncontainment gates."
            ),
        },
        "comparison_with_fixed_two_core_product_collapse": {
            "fixed_two_core_residual_Q_vector_dimension": fixed_two_core_residual_dimension,
            "line_annihilator_dimension_there": fixed_two_core_line_annihilator_dimension,
            "no_fixed_core_Q_vector_dimension": q_vector_dimension,
            "line_annihilator_dimension_here": annihilator_vector_dimension,
            "why_old_line_collapse_does_not_immediately_apply": (
                "In the fixed two-core residual P^2, a projective line has a "
                "one-dimensional annihilator, so two forced external roots make "
                "two evaluation functionals proportional and trigger the "
                "existing product-collapse dichotomy.  In the no-fixed-core "
                "P^4, a projective line has a three-dimensional annihilator; "
                "even 24 forced roots only imply the rank<=3 matrix condition "
                "unless an additional theorem collapses that rank-three span."
            ),
        },
        "sampler_denominators": {
            "finite_line": {
                "denominator": Q_LINE,
                "denominator_formula": "|F|",
                "budget_floor_denominator_over_2_128": BUDGET,
            },
            "projective_line": {
                "denominator": Q_LINE + 1,
                "denominator_formula": "|P^1(F)| = |F| + 1",
                "budget_floor_denominator_over_2_128": PROJECTIVE_BUDGET,
            },
        },
        "summary": {
            "agreement": AGREEMENT,
            "pair_core_min": pair_core_min,
            "Q_vector_dimension": q_vector_dimension,
            "pair_line_vector_dimension": pair_line_vector_dimension,
            "external_evaluation_rank_threshold_for_pair_line": rank_for_pair_line,
            "rank_test_available": True,
            "all_4_by_4_minors_must_vanish": True,
            "fixed_two_core_product_collapse_not_automatic": True,
        },
        "checks": [
            "A=385 dimensions give a five-dimensional Q-space",
            "a pair of distinct finite classes spans a two-dimensional Q-line",
            "the annihilator of that Q-line has dimension three",
            "common external roots are exactly evaluation rows annihilating the Q-line",
            "a 24-point pair-core survivor must have external-evaluation rank at most three",
            "rank at most three is equivalent to vanishing of all 4x4 external-evaluation minors",
            "fixed two-core line product-collapse has annihilator dimension one, not three",
        ],
        "nonclaims": [
            "does not close the no-fixed-core A=385 frontier",
            "does not prove that rank<=3 external evaluation cores of size 24 are impossible",
            "does not prove that rank<=3 external evaluation cores of size 24 are paid",
            "does not produce a split-locator witness from the linear converse",
            "does not classify overlapping-support rank-6 pencils",
            "does not compute arbitrary A=385 rank-6 root tables",
            "does not produce a row-level M3 safe-side bound",
        ],
    }


def check_certificate(path: Path, certificate: dict[str, Any]) -> None:
    expected = render(certificate)
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"A=385 pair-core rank-test mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    summary = certificate["summary"]
    print("F_17^32 M3 rank-6 A=385 pair-core rank test")
    print(
        "Qdim={Q_vector_dimension}; pair-core rank<={external_evaluation_rank_threshold_for_pair_line}; e>={pair_core_min}".format(
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
