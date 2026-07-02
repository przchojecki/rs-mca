#!/usr/bin/env python3
"""Verify the A=385 fixed two-core high-core quotient normal form."""

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


SCHEMA_VERSION = "f17-32-m3-rank6-a385-two-core-high-core-quotient-v1"
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
MOVING_SLOPE_INCIDENCE_REF = (
    "experimental/data/certificates/"
    "hankel-f17-32-m3-rank6-a385-two-core-moving-slope-incidence/"
    "f17_32_n512_k256_m3_rank6_a385_two_core_moving_slope_incidence.json"
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


def quotient_row(
    component_type: str,
    component_dimension: int,
    external_core_threshold: int,
    locator_degree: int,
) -> dict[str, Any]:
    quotient_degree_at_threshold = locator_degree - external_core_threshold
    return {
        "component_type": component_type,
        "component_projective_dimension": component_dimension,
        "external_core_threshold": external_core_threshold,
        "external_core_formula_range": [external_core_threshold, locator_degree - 1],
        "quotient_degree_at_threshold": quotient_degree_at_threshold,
        "quotient_degree_formula": "locator_degree - e_G",
        "quotient_degree_at_largest_positive_dimensional_core": 1,
        "quotient_family_projective_dimension_at_most": component_dimension,
    }


def build_certificate() -> dict[str, Any]:
    descriptor = load_json(ROW_DESCRIPTOR_REF)
    low_degree = load_json(LOW_DEGREE_TRANSFER_REF)
    moving_slope = load_json(MOVING_SLOPE_INCIDENCE_REF)
    split_gate = load_json(NULLPOLY_SPLIT_GATE_REF)

    require(descriptor["row"]["n"] == N, "descriptor n mismatch")
    require(descriptor["row"]["k"] == K, "descriptor k mismatch")
    require(descriptor["row"]["field_order"] == Q_LINE, "descriptor q mismatch")
    require(
        low_degree["schema_version"] == "f17-32-m3-rank6-boundary-low-degree-transfer-v1",
        "low-degree transfer schema mismatch",
    )
    require(AGREEMENT in low_degree["window"]["agreements"], "A=385 not in transfer packet")
    require(
        moving_slope["schema_version"]
        == "f17-32-m3-rank6-a385-two-core-moving-slope-incidence-v1",
        "moving-slope incidence schema mismatch",
    )
    require(
        moving_slope["summary"]["remaining_residual_after_incidence"]
        == "fixed two-core moving-slope high-core line/conic branches",
        "moving-slope incidence dependency does not expose the high-core residual",
    )
    require(
        split_gate["schema_version"] == "f17-32-m3-nullpolynomial-split-locator-gate-v1",
        "split-gate schema mismatch",
    )
    require(split_gate["summary"]["split_locator_gate_available"], "split gate unavailable")
    require(N % P != 0, "X^512-1 is not separable in this characteristic")
    require(FINITE_BUDGET == 6 and PROJECTIVE_BUDGET == 6, "unexpected budget")

    j_value = N - AGREEMENT
    t_value = AGREEMENT - K
    m_value = j_value + 1
    support_size = m_value + RANK
    h_value = support_size - t_value
    residual_vector_dimension = h_value - BASE_CORE_SIZE
    residual_projective_dimension = residual_vector_dimension - 1
    line_threshold = (
        moving_slope["summary"]["line_projective_safe_external_core_max"] + 1
    )
    conic_threshold = (
        moving_slope["summary"]["conic_pair_overlap_projective_safe_external_core_max"] + 1
    )
    require(j_value == 127, "A=385 locator degree changed")
    require(h_value == 5, "A=385 boundary defect should be five")
    require(residual_vector_dimension == 3, "fixed two-core residual dimension changed")
    require(residual_projective_dimension == 2, "fixed two-core residual should be P^2")
    require(line_threshold == 71, "line high-core threshold changed")
    require(conic_threshold == 68, "conic high-core threshold changed")

    transfer_record = next(
        record for record in low_degree["agreement_records"] if record["A"] == AGREEMENT
    )
    require(transfer_record["boundary_defect_h"] == h_value, "transfer h mismatch")
    require(
        transfer_record["finite_root_transfer"]["projective_Q_search_dimension"] == 4,
        "A=385 Q-space should be projective dimension four before core reduction",
    )

    line_row = quotient_row("line", 1, line_threshold, j_value)
    conic_row = quotient_row("irreducible_conic", 2, conic_threshold, j_value)
    require(line_row["quotient_degree_at_threshold"] == 56, "line quotient degree changed")
    require(conic_row["quotient_degree_at_threshold"] == 59, "conic quotient degree changed")

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT",
        "object": "A=385 separated rank-6 fixed two-core high-core quotient normal form",
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
            "a385_two_core_moving_slope_incidence": {
                "ref": MOVING_SLOPE_INCIDENCE_REF,
                "sha256": sha256_file(MOVING_SLOPE_INCIDENCE_REF),
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
            "combined_support_size": support_size,
            "boundary_defect_h": h_value,
            "projective_Q_search_dimension_before_core": 4,
            "forced_base_core_size": BASE_CORE_SIZE,
            "residual_vector_dimension_after_core": residual_vector_dimension,
            "projective_Q_search_dimension_after_core": residual_projective_dimension,
            "split_locator_degree": j_value,
        },
        "setup": {
            "residual_space": (
                "After the fixed two-point base core, write Q=E R with deg R<3; "
                "the residual vector space W has dimension three and projectivizes "
                "to a Q-plane."
            ),
            "root_hyperplanes": (
                "For each external subgroup point s, ev_s(R)=L_{E R}(s) is a "
                "linear functional on W.  The root hyperplane is P(ker ev_s) "
                "when ev_s is nonzero, and all of P(W) when ev_s=0."
            ),
            "forced_external_core": (
                "For a component G, the external forced core is the set of "
                "external s for which G is contained in the root hyperplane."
            ),
        },
        "theorem": {
            "positive_dimensional_core_bound": (
                "A positive-dimensional component cannot have e_G>=j=127.  "
                "Otherwise every nonzero L_{E R} on the component is divisible "
                "by the same degree-j external locator, hence is a scalar "
                "multiple of it; this contradicts injectivity of R -> L_{E R} "
                "on a positive-dimensional projective component."
            ),
            "line_forced_core": (
                "For a line component P(U), a forced external root s is exactly "
                "the condition ev_s|_U=0.  Thus C_E=prod_{s in forced core}(T-s) "
                "divides L_{E R} for every R in U, and the split-locator gate "
                "on the line becomes a quotient-locator pencil on U."
            ),
            "irreducible_conic_forced_core": (
                "If an irreducible conic G is contained in a root hyperplane, "
                "then the hyperplane cannot be a proper projective line; hence "
                "ev_s=0 on all of W.  Therefore an irreducible-conic forced "
                "external core is a global common divisor for every L_{E R} in "
                "the whole residual Q-plane."
            ),
            "quotient_split_gate": (
                "Because C_E is a squarefree divisor of X^512-1, a candidate "
                "L_{E R}=C_E F_R passes the degree-j split-locator divisor gate "
                "only if, after normalization and the exact-degree check, F_R "
                "divides (X^512-1)/C_E and has degree j-e_G.  The quotient "
                "degree is therefore at most j-e_G."
            ),
            "line_high_core_normal_form": (
                "The high-core line residual begins at e_G=71, so it is a "
                "projective-line quotient pencil of degree at most 127-71=56."
            ),
            "conic_high_core_normal_form": (
                "The high-core irreducible-conic residual begins at e_G=68, "
                "so it is a projective-plane quotient family of degree at most "
                "127-68=59."
            ),
        },
        "quotient_normal_forms": {
            "line": line_row,
            "irreducible_conic": conic_row,
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
            "split_locator_degree": j_value,
            "positive_dimensional_external_core_upper_bound": j_value - 1,
            "line_high_core_external_core_min": line_threshold,
            "line_residual_quotient_degree_at_most": (
                line_row["quotient_degree_at_threshold"]
            ),
            "line_quotient_family_projective_dimension_at_most": 1,
            "conic_high_core_external_core_min": conic_threshold,
            "conic_residual_quotient_degree_at_most": (
                conic_row["quotient_degree_at_threshold"]
            ),
            "conic_quotient_family_projective_dimension_at_most": 2,
            "remaining_residual_after_quotient_normal_form": (
                "fixed two-core high-core quotient pencils/families"
            ),
        },
        "checks": [
            "row descriptor and dependency schemas match",
            "A=385 fixed two-core residual has Q-plane P^2 and locator degree 127",
            "moving-slope incidence dependency exposes the high-core line/conic residual",
            "positive-dimensional components have external forced core at most 126",
            "line high-core residual starts at e_G=71 and has quotient degree at most 56",
            "irreducible-conic high-core residual starts at e_G=68 and has quotient degree at most 59",
            "irreducible conic containment in a root hyperplane forces a global common core",
            "quotient divisor gate is against (X^512-1)/C_E",
        ],
        "nonclaims": [
            "does not prove product collapse for A=385 high-core line or conic components",
            "does not claim the high-core quotient pencils or families are empty or paid",
            "does not close the full fixed two-core nonconstant moving-slope branch",
            "does not prove that every A=385 over-budget branch has a fixed two-point base core",
            "does not close moving-core or no-common-core A=385 branches",
            "does not classify overlapping-support rank-6 pencils",
            "does not prove endpoint payment",
            "does not produce a row-level M3 safe-side bound",
        ],
    }


def check_certificate(path: Path, certificate: dict[str, Any]) -> None:
    expected = render(certificate)
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"A=385 two-core high-core quotient mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    summary = certificate["summary"]
    print("F_17^32 M3 rank-6 A=385 fixed two-core high-core quotient")
    print(
        "line quotient degree<={line_residual_quotient_degree_at_most}; conic quotient degree<={conic_residual_quotient_degree_at_most}".format(
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
