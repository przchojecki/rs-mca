#!/usr/bin/env python3
"""Verify the A=385 pair-core Cauchy-moment normal form."""

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


SCHEMA_VERSION = "f17-32-m3-rank6-a385-pair-core-cauchy-moment-v1"
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
RANK_TEST_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-rank6-a385-pair-core-rank-test/"
    "f17_32_n512_k256_m3_rank6_a385_pair_core_rank_test.json"
)
LOW_DEGREE_TRANSFER_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-rank6-boundary-low-degree-transfer/"
    "f17_32_n512_k256_m3_rank6_boundary_low_degree_transfer.json"
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
    rank_test = load_json(RANK_TEST_REF)
    transfer = load_json(LOW_DEGREE_TRANSFER_REF)

    require(descriptor["row"]["n"] == N, "descriptor n mismatch")
    require(descriptor["row"]["k"] == K, "descriptor k mismatch")
    require(descriptor["row"]["field_order"] == Q_LINE, "descriptor q mismatch")
    require(
        rank_test["schema_version"] == "f17-32-m3-rank6-a385-pair-core-rank-test-v1",
        "pair-core rank-test schema mismatch",
    )
    require(
        transfer["schema_version"] == "f17-32-m3-rank6-boundary-low-degree-transfer-v1",
        "low-degree transfer schema mismatch",
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
    q_dimension = h_value
    pair_core_min = rank_test["summary"]["pair_core_min"]
    rank_threshold = rank_test["summary"][
        "external_evaluation_rank_threshold_for_pair_line"
    ]

    require(j_value == 127, "A385 j changed")
    require(t_value == 129, "A385 t changed")
    require(m_value == 128, "A385 m changed")
    require(h_value == 5, "A385 boundary defect changed")
    require(q_dimension == 5, "A385 Q dimension changed")
    require(
        transfer_record["boundary_defect_h"] == h_value,
        "transfer record h mismatch",
    )
    require(pair_core_min == 24, "pair-core minimum changed")
    require(rank_threshold == 3, "rank threshold changed")

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT",
        "object": "A=385 pair-core external-evaluation Cauchy-moment normal form",
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
            "a385_pair_core_rank_test": {
                "ref": RANK_TEST_REF,
                "sha256": sha256_file(RANK_TEST_REF),
            },
            "rank6_boundary_low_degree_transfer": {
                "ref": LOW_DEGREE_TRANSFER_REF,
                "sha256": sha256_file(LOW_DEGREE_TRANSFER_REF),
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
            "Q_vector_dimension": q_dimension,
            "pair_core_min": pair_core_min,
            "rank_threshold": rank_threshold,
        },
        "notation": {
            "base_support": "X, |X|=m=128",
            "external_core": "E subset H\\X",
            "base_weight": "W_x = Omega_x/a_x, nonzero on X",
            "base_polynomial": "P_X(T)=prod_{x in X}(T-x)",
            "Q_basis": "1,T,T^2,T^3,T^4",
        },
        "normal_form": {
            "base_interpolation": (
                "For Q(T)=sum_{r=0}^4 q_r T^r, L_Q is the unique degree-<128 "
                "polynomial satisfying L_Q(x)=W_x Q(x) for x in X."
            ),
            "lagrange_formula": (
                "For s outside X, L_Q(s)=sum_{x in X} W_x Q(x) "
                "P_X(s)/((s-x)P_X'(x))."
            ),
            "raw_external_row": (
                "In the monomial Q-basis, ev_s has coordinates "
                "c_r(s)=P_X(s) sum_{x in X} W_x x^r/((s-x)P_X'(x)), "
                "0<=r<=4."
            ),
            "reduced_cauchy_moment_row": (
                "Since P_X(s) is nonzero for s in H\\X, row rank is unchanged "
                "after dividing by P_X(s).  The reduced row is "
                "d_r(s)=sum_{x in X} W_x x^r/((s-x)P_X'(x))."
            ),
            "matrix_factorization": (
                "For row set E and columns r=0..4, the reduced matrix is "
                "D_E = C_{E,X} diag(W_x/P_X'(x)) V_X, where "
                "C_{s,x}=1/(s-x) and V_{x,r}=x^r."
            ),
            "rank_condition": (
                "The pair-core rank-test condition rank M_E<=3 is equivalent "
                "to rank D_E<=3, hence to vanishing of every 4 x 4 minor of D_E."
            ),
            "cauchy_binet_minor": (
                "For rows S={s_1,...,s_4} subset E and columns "
                "R={r_1<...<r_4} subset {0,1,2,3,4}, det D_{S,R} equals the "
                "sum over T subset X, |T|=4, of det(1/(s_i-x))_{s_i in S,x in T} "
                "det(x^r)_{x in T,r in R} prod_{x in T} W_x/P_X'(x)."
            ),
        },
        "consequence_for_pair_core_frontier": {
            "pressure_forced_core_size": pair_core_min,
            "matrix_size_at_forced_core": [pair_core_min, q_dimension],
            "required_rank": "<=3",
            "required_minor_vanishing": "all 4 x 4 minors of the reduced Cauchy-moment matrix D_E vanish",
            "next_target": (
                "Prove that no 24-point external set E and nonzero base weights "
                "W_x compatible with the remaining gates can make D_E rank<=3, "
                "or classify such rank-deficient Cauchy-moment packets as paid."
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
            "Q_vector_dimension": q_dimension,
            "pair_core_min": pair_core_min,
            "rank_threshold": rank_threshold,
            "raw_row_factor_removed": "P_X(s)",
            "reduced_matrix_factorization_available": True,
            "cauchy_binet_minor_formula_available": True,
        },
        "checks": [
            "A=385 dimensions give a five-dimensional Q-space",
            "base interpolation gives the displayed Lagrange formula for L_Q(s)",
            "external points have P_X(s) nonzero, so raw and reduced row ranks agree",
            "reduced rows factor as Cauchy matrix times diagonal weights times Vandermonde moments",
            "rank<=3 is equivalent to vanishing of every 4x4 reduced Cauchy-moment minor",
            "Cauchy-Binet expands every 4x4 minor as a weighted sum over four base nodes",
        ],
        "nonclaims": [
            "does not close the no-fixed-core A=385 frontier",
            "does not prove that rank<=3 Cauchy-moment cores of size 24 are impossible",
            "does not prove that rank<=3 Cauchy-moment cores of size 24 are paid",
            "does not specialize the arbitrary nonzero base weights W_x",
            "does not produce a split-locator witness from the matrix rank condition",
            "does not classify overlapping-support rank-6 pencils",
            "does not produce a row-level M3 safe-side bound",
        ],
    }


def check_certificate(path: Path, certificate: dict[str, Any]) -> None:
    expected = render(certificate)
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"A=385 pair-core Cauchy-moment mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    summary = certificate["summary"]
    print("F_17^32 M3 rank-6 A=385 pair-core Cauchy-moment normal form")
    print(
        "Qdim={Q_vector_dimension}; e>={pair_core_min}; rank<={rank_threshold}".format(
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
