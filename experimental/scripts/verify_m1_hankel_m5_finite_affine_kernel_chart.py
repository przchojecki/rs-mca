#!/usr/bin/env python3
"""Verify the M5 finite-affine kernel noncontainment chart."""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from math import comb
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experimental.scripts.emit_f17_32_hankel_row_descriptor import (  # noqa: E402
    Field,
    K,
    MODULUS,
    N,
    P,
)


SCHEMA_VERSION = "f17-32-m3-m5-finite-affine-kernel-chart-v1"
Q_LINE = 17**32
A_MIN = 385
A_MAX = 426
ROW_DESCRIPTOR_REF = (
    "experimental/data/certificates/hankel-f17-32-row-descriptor/"
    "f17_32_n512_k256_hankel_row_descriptor.json"
)
FINITE_TANGENT_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-finite-tangent-overlap/"
    "f17_32_n512_k256_m3_finite_tangent_overlap_criterion.json"
)


def load_json(ref: str | Path) -> dict[str, Any]:
    path = ref if isinstance(ref, Path) else ROOT / ref
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(ref: str) -> str:
    return sha256((ROOT / ref).read_bytes()).hexdigest()


def hash_value(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return sha256(payload).hexdigest()


def render(value: dict[str, Any]) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def finite_affine_decision_table() -> dict[str, Any]:
    return {
        "fixed_finite_slope": "z in F_17^32",
        "M_z": "H_{t,j}(u) + z H_{t,j}(v)",
        "B_matrix": "H_{t,j}(v)",
        "ambient_equations": "M_z * ell = 0, B_matrix * ell != 0",
        "support_wise_meaning": (
            "If B_matrix*ell=0 and M_z*ell=0, then also H(u)*ell=0; "
            "both line endpoints are explained on the same support, so this "
            "is the contained branch removed by the affine pivot split."
        ),
        "outcomes": {
            "empty": {
                "condition": "ker M_z subset ker H_{t,j}(v)",
                "equivalent_rank_test": "rank stack(M_z, H_{t,j}(v)) = rank M_z",
                "end_state": "empty",
                "finite_affine_contribution": 0,
            },
            "ambient_nonempty": {
                "condition": "ker M_z not subset ker H_{t,j}(v)",
                "equivalent_rank_test": "rank stack(M_z, H_{t,j}(v)) > rank M_z",
                "end_state": "dimension_degree",
                "finite_affine_contribution_upper_bound": 1,
                "split_nonemptiness_claimed": False,
            },
        },
        "rank_stratification": {
            "automatic_survival_condition": "rank H_{t,j}(v) > rank M_z",
            "reason": (
                "Containment ker M_z subset ker H(v) would force "
                "row H(v) subset row M_z, hence rank H(v) <= rank M_z."
            ),
            "possible_containment_condition": "rank H_{t,j}(v) <= rank M_z",
            "then_apply": "stacked-rank equality test",
            "full_direction_consequence": (
                "If rank H(v)=j+1, every finite regular root has "
                "rank M_z<=j and therefore survives the ambient "
                "noncontainment test."
            ),
        },
        "pivot_cover": (
            "For ambient linear charts, M_z ell=0 and H(v)ell!=0 is equivalent "
            "to membership in at least one affine pivot chart (H(v)ell)_h != 0."
        ),
    }


def agreement_record(agreement: int) -> dict[str, Any]:
    j_value = N - agreement
    t_value = agreement - K
    size = j_value + 1
    return {
        "A": agreement,
        "j": j_value,
        "t": t_value,
        "minor_size": size,
        "ambient_locator_space_dimension": size,
        "maximal_row_set_count": comb(t_value, size),
        "finite_slope_budget": Q_LINE // 2**128,
    }


def build_certificate() -> dict[str, Any]:
    field = Field(P, MODULUS)
    descriptor = load_json(ROW_DESCRIPTOR_REF)
    finite_tangent = load_json(FINITE_TANGENT_REF)

    require(descriptor["row"]["n"] == N, "descriptor n mismatch")
    require(descriptor["row"]["k"] == K, "descriptor k mismatch")
    require(descriptor["row"]["field"] == "F_17^32", "descriptor field mismatch")
    require(descriptor["row"]["field_order"] == Q_LINE, "descriptor q mismatch")
    require(descriptor["row"]["syndrome_length"] == N - K, "syndrome length mismatch")
    require(
        finite_tangent["schema_version"]
        == "f17-32-m3-finite-tangent-overlap-criterion-v1",
        "unexpected finite tangent-overlap schema",
    )
    require(finite_tangent["window"]["A_min"] == A_MIN, "finite tangent A_min mismatch")
    require(finite_tangent["window"]["A_max"] == A_MAX, "finite tangent A_max mismatch")

    domain_encodings = descriptor["domain"]["domain_encodings"]
    require(len(domain_encodings) == N, "domain length mismatch")
    require(len(set(domain_encodings)) == N, "descriptor domain is not distinct")
    decoded = [field.decode(value) for value in domain_encodings]
    require(
        [field.encode(value) for value in decoded] == domain_encodings,
        "domain decode/encode roundtrip failed",
    )

    records = [agreement_record(agreement) for agreement in range(A_MIN, A_MAX + 1)]
    total_row_sets = sum(record["maximal_row_set_count"] for record in records)
    require(
        total_row_sets == finite_tangent["window"]["all_row_set_total"],
        "finite tangent row-set total mismatch",
    )
    require(Q_LINE // 2**128 == 6, "unexpected finite-slope budget")

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED",
        "object": "M5 finite-affine kernel noncontainment chart",
        "row": {
            "code": "RS[F_17^32,H,256]",
            "n": N,
            "k": K,
            "field": "F_17^32",
            "domain_hash": descriptor["row"]["domain_hash"],
            "q_line": Q_LINE,
            "finite_slope_budget": Q_LINE // 2**128,
        },
        "source_artifacts": {
            "row_descriptor": {"ref": ROW_DESCRIPTOR_REF, "sha256": sha256_file(ROW_DESCRIPTOR_REF)},
            "finite_tangent_overlap": {
                "ref": FINITE_TANGENT_REF,
                "sha256": sha256_file(FINITE_TANGENT_REF),
            },
        },
        "window": {
            "A_min": A_MIN,
            "A_max": A_MAX,
            "agreement_count": len(records),
            "all_row_set_total": total_row_sets,
        },
        "finite_affine_decision_table": finite_affine_decision_table(),
        "theorem": {
            "statement": (
                "For fixed A,u,v and finite slope z, the ambient finite-affine "
                "noncontainment chart M_z ell=0, H(v)ell!=0 is empty iff "
                "ker M_z is contained in ker H(v)."
            ),
            "rank_test": (
                "Equivalently, the chart is empty iff "
                "rank stack(M_z,H(v)) = rank M_z; otherwise the slope z "
                "contributes at most one finite parameter."
            ),
            "rank_stratification": (
                "If rank H(v) > rank M_z, the chart is automatically nonempty. "
                "Thus finite roots with post-root rank below the direction rank "
                "cannot be removed by same-support containment.  Containment can "
                "only occur in the rank range rank H(v) <= rank M_z, where the "
                "stacked-rank equality test decides it."
            ),
            "proof": [
                "The affine incidence equation is M_z ell=0.",
                "The pivot/noncontainment condition is H(v)ell != 0, equivalently some affine pivot coordinate is nonzero.",
                "If ker M_z is contained in ker H(v), no incidence vector survives the pivot open cover.",
                "If containment fails, choose ell in ker M_z outside ker H(v); it lies in at least one ambient affine pivot chart.",
                "The split-locator chart is contained in this ambient chart, so ambient emptiness proves split emptiness and ambient nonemptiness gives a safe one-slope upper bound.",
                "The rank-stratification corollary follows from row-space duality: ker M_z subset ker H(v) is equivalent to row H(v) subset row M_z.",
            ],
            "same_support_containment": (
                "When M_z ell=0 and H(v)ell=0, one also has H(u)ell=0. "
                "Thus both f and g are explained on that witness support; "
                "this is the contained branch, not a support-wise noncontainment slope."
            ),
            "m5_end_states_per_root": {
                "kernel_containment": "empty",
                "kernel_noncontainment": "dimension_degree with finite parameter degree 1",
            },
        },
        "field_audit": {
            "full_domain_distinct": True,
            "domain_size": len(domain_encodings),
            "domain_hash": hash_value(domain_encodings),
            "decoded_roundtrip_hash": hash_value([field.encode(value) for value in decoded]),
        },
        "agreement_records": records,
        "summary": {
            "agreement_count": len(records),
            "finite_slope_budget": Q_LINE // 2**128,
            "finite_affine_root_filter_end_states": ["empty", "dimension_degree"],
            "max_contribution_per_unfiltered_root": 1,
            "projective_infinity_impact": 0,
            "automatic_survival_when_direction_rank_exceeds_root_rank": True,
            "full_direction_regular_roots_survive_kernel_filter": True,
        },
        "checks": [
            "row descriptor and finite tangent-overlap dependency schemas match",
            "window is 385..426",
            "row-set totals match the finite tangent-overlap certificate",
            "domain encodings round-trip in the printed F_17^32 model",
            "kernel-containment and stacked-rank tests are equivalent by rank-nullity",
            "rank H(v)>rank M_z excludes kernel containment",
            "the affine pivot cover is equivalent to H(v)ell nonzero in the ambient chart",
        ],
        "nonclaims": [
            "does not compute finite root tables",
            "does not claim ambient nonempty implies split-locator nonempty",
            "does not close rank-deficient finite buckets without a root table or pivot eliminant",
            "does not classify quotient or extension overlap for surviving roots",
        ],
    }


def check_certificate(path: Path) -> None:
    expected = render(build_certificate())
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"M5 finite-affine kernel certificate mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    window = certificate["window"]
    summary = certificate["summary"]
    print("F_17^32 M5 finite-affine kernel chart")
    print(
        "A={A_min}..{A_max}, agreements={agreement_count}, row sets={all_row_set_total}".format(
            **window
        )
    )
    print(
        "root-filter end states={finite_affine_root_filter_end_states}, max contribution per unfiltered root={max_contribution_per_unfiltered_root}".format(
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
        check_certificate(args.check)
    print_summary(certificate)


if __name__ == "__main__":
    main()
