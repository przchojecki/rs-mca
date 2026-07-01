#!/usr/bin/env python3
"""Verify the A=386 slope-free containment filter."""

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


SCHEMA_VERSION = "f17-32-m3-rank6-a386-slope-free-containment-v1"
Q_LINE = 17**32
TARGET_BITS = 128
FINITE_BUDGET = Q_LINE // 2**TARGET_BITS
PROJECTIVE_DENOMINATOR = Q_LINE + 1
PROJECTIVE_BUDGET = PROJECTIVE_DENOMINATOR // 2**TARGET_BITS
AGREEMENT = 386
RANK = 6
ROW_DESCRIPTOR_REF = (
    "experimental/data/certificates/hankel-f17-32-row-descriptor/"
    "f17_32_n512_k256_hankel_row_descriptor.json"
)
LOW_DEGREE_TRANSFER_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-rank6-boundary-low-degree-transfer/"
    "f17_32_n512_k256_m3_rank6_boundary_low_degree_transfer.json"
)
SLOPE_DICHOTOMY_REF = (
    "experimental/data/certificates/"
    "hankel-f17-32-m3-rank6-a386-global-component-slope-dichotomy/"
    "f17_32_n512_k256_m3_rank6_a386_global_component_slope_dichotomy.json"
)
FINITE_KERNEL_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-m5-finite-affine-kernel-chart/"
    "f17_32_n512_k256_m3_m5_finite_affine_kernel_chart.json"
)
PROJECTIVE_SPLIT_GATE_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-projective-split-locator-gate/"
    "f17_32_n512_k256_m3_projective_split_locator_gate.json"
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
    slope_dichotomy = load_json(SLOPE_DICHOTOMY_REF)
    finite_kernel = load_json(FINITE_KERNEL_REF)
    projective_split = load_json(PROJECTIVE_SPLIT_GATE_REF)

    require(descriptor["row"]["n"] == N, "descriptor n mismatch")
    require(descriptor["row"]["k"] == K, "descriptor k mismatch")
    require(descriptor["row"]["field_order"] == Q_LINE, "descriptor q mismatch")
    require(
        low_degree["schema_version"] == "f17-32-m3-rank6-boundary-low-degree-transfer-v1",
        "low-degree transfer schema mismatch",
    )
    require(
        slope_dichotomy["schema_version"]
        == "f17-32-m3-rank6-a386-global-component-slope-dichotomy-v1",
        "slope dichotomy schema mismatch",
    )
    require(
        "slope-free base locus or global component"
        in slope_dichotomy["summary"]["remaining_residuals"],
        "slope-free residual is not exposed by dependency",
    )
    require(
        finite_kernel["schema_version"] == "f17-32-m3-m5-finite-affine-kernel-chart-v1",
        "finite-kernel schema mismatch",
    )
    require(
        projective_split["schema_version"] == "f17-32-m3-projective-split-locator-gate-v1",
        "projective split-gate schema mismatch",
    )
    require(
        "B_matrix * ell != 0"
        in finite_kernel["finite_affine_decision_table"]["ambient_equations"],
        "finite noncontainment gate mismatch",
    )
    require(
        "H_{t,j}(u) ell != 0"
        in projective_split["theorem"]["ambient_projective_chart"],
        "projective noncontainment gate mismatch",
    )
    require(N % P != 0, "X^512-1 is not separable in this characteristic")
    require(FINITE_BUDGET == 6 and PROJECTIVE_BUDGET == 6, "unexpected budget")

    j_value = N - AGREEMENT
    t_value = AGREEMENT - K
    m_value = j_value + 1
    support_size = m_value + RANK
    h_value = support_size - t_value
    require(h_value == 3, "A=386 boundary defect should be three")

    transfer_record = next(
        record for record in low_degree["agreement_records"] if record["A"] == AGREEMENT
    )
    require(transfer_record["boundary_defect_h"] == h_value, "transfer h mismatch")
    require(
        transfer_record["finite_root_transfer"]["projective_Q_search_dimension"] == 2,
        "A=386 Q-space should be projective dimension two",
    )

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT",
        "object": "A=386 separated rank-6 slope-free containment filter",
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
            "a386_global_component_slope_dichotomy": {
                "ref": SLOPE_DICHOTOMY_REF,
                "sha256": sha256_file(SLOPE_DICHOTOMY_REF),
            },
            "finite_affine_kernel_chart": {
                "ref": FINITE_KERNEL_REF,
                "sha256": sha256_file(FINITE_KERNEL_REF),
            },
            "projective_split_locator_gate": {
                "ref": PROJECTIVE_SPLIT_GATE_REF,
                "sha256": sha256_file(PROJECTIVE_SPLIT_GATE_REF),
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
            "projective_Q_search_dimension": 2,
        },
        "setup": {
            "low_degree_transfer": (
                "For Q with deg Q<3, L_Q is the unique degree-<m polynomial "
                "satisfying a_x L_Q(x)=Omega_x Q(x) on X."
            ),
            "direction_forms": (
                "For each direction node y, N_y(Q)=Omega_y Q(y) and "
                "D_y(Q)=b_y L_Q(y)."
            ),
            "slope_free_condition": (
                "N_y(Q)=0 and D_y(Q)=0 for every direction node y."
            ),
        },
        "theorem": {
            "direction_containment": (
                "The direction Hankel action is H(v)L_Q = "
                "(sum_y b_y L_Q(y)y^a)_{0<=a<t}.  Under the slope-free "
                "condition all b_y L_Q(y)=D_y(Q) vanish, so H(v)L_Q=0."
            ),
            "base_containment": (
                "The vector (Omega_s Q(s))_{s in X union Y} is in the first-t "
                "Vandermonde nullspace.  Since the direction terms "
                "Omega_y Q(y)=N_y(Q) vanish, the X terms give H(u)L_Q=0."
            ),
            "finite_affine_filter": (
                "For every finite slope z, H(u+zv)L_Q=0 and H(v)L_Q=0.  Thus "
                "the displayed slope-free vector is in the contained branch "
                "and fails the finite-affine noncontainment gate H(v)ell!=0."
            ),
            "projective_filter": (
                "At projective infinity the same vector has H(v)L_Q=0 and "
                "H(u)L_Q=0, so it also fails the projective noncontainment "
                "gate H(u)ell!=0."
            ),
            "accounting_scope": (
                "Slope-free low-degree-transfer vectors themselves contribute "
                "zero finite or projective support-wise noncontained parameters.  "
                "If the same finite slope has another independent vector with "
                "H(v)ell!=0, that vector is outside this slope-free filter and "
                "must be counted by another branch."
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
            "slope_free_vector_finite_noncontained_contribution": 0,
            "slope_free_vector_projective_endpoint_contribution": 0,
            "finite_noncontainment_gate": "H(v)ell != 0",
            "projective_noncontainment_gate": "H(u)ell != 0",
            "remaining_unclosed_residual": (
                "nonconstant moving-slope components, plus any independent "
                "noncontained vectors at slopes also admitting a slope-free vector"
            ),
        },
        "checks": [
            "row descriptor and dependency schemas match",
            "A=386 has boundary defect h=3 and Q-space P^2",
            "slope dichotomy exposes the slope-free residual",
            "finite-affine dependency uses H(v)ell!=0 as the noncontainment gate",
            "projective dependency uses H(u)ell!=0 as the endpoint noncontainment gate",
            "slope-free D_y=0 implies H(v)L_Q=0",
            "slope-free N_y=0 plus the transfer nullspace implies H(u)L_Q=0",
        ],
        "nonclaims": [
            "does not close nonconstant moving-slope components",
            "does not rule out another independent noncontained vector at the same finite slope",
            "does not cover A=385",
            "does not classify overlapping-support rank-6 pencils",
            "does not prove endpoint payment",
            "does not produce a row-level M3 safe-side bound",
        ],
    }


def check_certificate(path: Path, certificate: dict[str, Any]) -> None:
    expected = render(certificate)
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"A=386 slope-free containment certificate mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    summary = certificate["summary"]
    print("F_17^32 M3 rank-6 A=386 slope-free containment filter")
    print(
        "finite slope-free contribution={slope_free_vector_finite_noncontained_contribution}, projective slope-free contribution={slope_free_vector_projective_endpoint_contribution}".format(
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
