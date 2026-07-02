#!/usr/bin/env python3
"""Verify the A=385 fixed two-core slope-free emptiness obstruction."""

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


SCHEMA_VERSION = "f17-32-m3-rank6-a385-two-core-slope-free-empty-v1"
Q_LINE = 17**32
TARGET_BITS = 128
FINITE_BUDGET = Q_LINE // 2**TARGET_BITS
PROJECTIVE_DENOMINATOR = Q_LINE + 1
PROJECTIVE_BUDGET = PROJECTIVE_DENOMINATOR // 2**TARGET_BITS
AGREEMENT = 385
RANK = 6
BASE_CORE_SIZE = 2
ROW_DESCRIPTOR_REF = (
    "experimental/data/certificates/hankel-f17-32-row-descriptor/"
    "f17_32_n512_k256_hankel_row_descriptor.json"
)
LOW_DEGREE_TRANSFER_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-rank6-boundary-low-degree-transfer/"
    "f17_32_n512_k256_m3_rank6_boundary_low_degree_transfer.json"
)
GLOBAL_COMPONENT_REF = (
    "experimental/data/certificates/"
    "hankel-f17-32-m3-rank6-a385-two-core-global-component-slope-dichotomy/"
    "f17_32_n512_k256_m3_rank6_a385_two_core_global_component_slope_dichotomy.json"
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
    low_degree = load_json(LOW_DEGREE_TRANSFER_REF)
    global_component = load_json(GLOBAL_COMPONENT_REF)

    require(descriptor["row"]["n"] == N, "descriptor n mismatch")
    require(descriptor["row"]["k"] == K, "descriptor k mismatch")
    require(descriptor["row"]["field_order"] == Q_LINE, "descriptor q mismatch")
    require(
        low_degree["schema_version"] == "f17-32-m3-rank6-boundary-low-degree-transfer-v1",
        "low-degree transfer schema mismatch",
    )
    require(AGREEMENT in low_degree["window"]["agreements"], "A=385 not in transfer packet")
    require(
        global_component["schema_version"]
        == "f17-32-m3-rank6-a385-two-core-global-component-slope-dichotomy-v1",
        "A385 two-core global-component schema mismatch",
    )
    require(
        "fixed two-core slope-free base locus or global component"
        in global_component["summary"]["remaining_residuals"],
        "slope-free residual is not exposed by dependency",
    )
    require(N % P != 0, "X^512-1 is not separable in this characteristic")
    require(FINITE_BUDGET == 6 and PROJECTIVE_BUDGET == 6, "unexpected budget")

    j_value = N - AGREEMENT
    t_value = AGREEMENT - K
    m_value = j_value + 1
    support_size = m_value + RANK
    h_value = support_size - t_value
    residual_vector_dimension = h_value - BASE_CORE_SIZE
    residual_projective_dimension = residual_vector_dimension - 1
    residual_degree_bound = residual_vector_dimension
    max_roots_for_nonzero_residual = residual_degree_bound - 1
    require(h_value == 5, "A=385 boundary defect should be five")
    require(
        residual_vector_dimension == 3 and residual_projective_dimension == 2,
        "two fixed base roots should leave residual projective plane",
    )
    require(
        RANK > max_roots_for_nonzero_residual,
        "direction nodes should outnumber residual degree root bound",
    )

    transfer_record = next(
        record for record in low_degree["agreement_records"] if record["A"] == AGREEMENT
    )
    require(transfer_record["boundary_defect_h"] == h_value, "transfer h mismatch")
    require(
        transfer_record["finite_root_transfer"]["projective_Q_search_dimension"] == 4,
        "A=385 Q-space should be projective dimension four before core reduction",
    )

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT",
        "object": "A=385 separated rank-6 fixed two-core slope-free emptiness",
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
            "a385_two_core_global_component_slope_dichotomy": {
                "ref": GLOBAL_COMPONENT_REF,
                "sha256": sha256_file(GLOBAL_COMPONENT_REF),
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
            "projective_Q_search_dimension_before_core": 4,
            "forced_base_core_size": BASE_CORE_SIZE,
            "residual_vector_dimension_after_core": residual_vector_dimension,
            "projective_Q_search_dimension_after_core": residual_projective_dimension,
            "residual_degree_bound": f"deg R < {residual_degree_bound}",
            "direction_node_count": RANK,
        },
        "setup": {
            "fixed_two_core_factorization": (
                "After the fixed two-point base core, write Q=E R with E "
                "the product over the two fixed base nodes and deg R<3."
            ),
            "separated_support": (
                "The six direction nodes Y are disjoint from the base support X; "
                "therefore every direction node is disjoint from the fixed core."
            ),
            "direction_numerators": (
                "For each direction node y, the numerator linear form is "
                "N_y(R)=Omega_y E(y) R(y)."
            ),
            "nonzero_scalars": (
                "The barycentric residue Omega_y is nonzero because the support "
                "nodes are distinct, and E(y) is nonzero because y is not in the "
                "fixed base core."
            ),
            "slope_free_condition": (
                "A slope-free point or slope-free component requires "
                "N_y(R)=D_y(R)=0 for every direction node y."
            ),
        },
        "theorem": {
            "pointwise_emptiness": (
                "If [R] is slope-free, then N_y(R)=0 for all six direction nodes. "
                "Since N_y(R) is a nonzero scalar multiple of R(y), the nonzero "
                "polynomial R of degree <3 vanishes at six distinct nodes.  A "
                "nonzero degree-<3 polynomial has at most two roots, so no such "
                "projective residual class [R] exists."
            ),
            "component_emptiness": (
                "Any nonempty slope-free global component over the algebraic "
                "closure contains a point.  Pointwise emptiness therefore rules "
                "out a slope-free component as well as an isolated base-locus "
                "point."
            ),
            "accounting": (
                "The fixed two-core slope-free base-locus/global-component "
                "residual contributes zero finite noncontained slopes and zero "
                "projective endpoint parameters."
            ),
        },
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
            "boundary_defect_h": h_value,
            "forced_base_core_size": BASE_CORE_SIZE,
            "residual_vector_dimension_after_core": residual_vector_dimension,
            "projective_Q_search_dimension_after_core": residual_projective_dimension,
            "residual_degree_strict_bound": residual_degree_bound,
            "direction_node_count": RANK,
            "max_roots_for_nonzero_residual_R": max_roots_for_nonzero_residual,
            "direction_nodes_exceed_root_bound": True,
            "slope_free_base_locus_empty": True,
            "slope_free_global_component_empty": True,
            "finite_noncontained_parameter_contribution": 0,
            "projective_endpoint_parameter_contribution": 0,
            "projective_budget": PROJECTIVE_BUDGET,
            "remaining_residual": "fixed two-core determined nonconstant slope map",
        },
        "checks": [
            "row descriptor and dependency schemas match",
            "A=385 has boundary defect h=5 and residual fixed-core Q-space P^2",
            "global-component packet exposes the fixed two-core slope-free residual",
            "direction support is separated from the fixed two-point base core",
            "Omega_y and E(y) are nonzero for every direction node",
            "slope-free implies R vanishes at all six direction nodes",
            "a nonzero degree-<3 residual polynomial has at most two roots",
            "six direction roots contradict projective nonzero residual R",
        ],
        "nonclaims": [
            "does not close fixed two-core nonconstant moving-slope components",
            "does not prove that every A=385 over-budget branch has a fixed two-point base core",
            "does not close moving-core or no-common-core A=385 branches",
            "does not classify overlapping-support rank-6 pencils",
            "does not prove endpoint payment; the slope-free branch is empty",
            "does not compute arbitrary A=385 rank-6 root tables",
            "does not produce a row-level M3 safe-side bound",
        ],
    }


def check_certificate(path: Path, certificate: dict[str, Any]) -> None:
    expected = render(certificate)
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"A=385 two-core slope-free certificate mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    summary = certificate["summary"]
    print("F_17^32 M3 rank-6 A=385 fixed two-core slope-free")
    print(
        "direction nodes={direction_node_count}, max residual roots={max_roots_for_nonzero_residual_R}, finite contribution={finite_noncontained_parameter_contribution}".format(
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
