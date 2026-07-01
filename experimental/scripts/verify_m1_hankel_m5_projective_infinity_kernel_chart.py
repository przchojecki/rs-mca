#!/usr/bin/env python3
"""Verify the M5 projective-infinity kernel-containment chart."""

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


SCHEMA_VERSION = "f17-32-m3-m5-projective-infinity-kernel-chart-v1"
Q_LINE = 17**32
A_MIN = 385
A_MAX = 426
ROW_DESCRIPTOR_REF = (
    "experimental/data/certificates/hankel-f17-32-row-descriptor/"
    "f17_32_n512_k256_hankel_row_descriptor.json"
)
PROJECTIVE_INFINITY_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-projective-infinity-rank/"
    "f17_32_n512_k256_m3_projective_infinity_rank_criterion.json"
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


def kernel_chart_decision_table() -> dict[str, Any]:
    return {
        "chart": {
            "projective_point": "[0:1]",
            "A_matrix": "H_{t,j}(u)",
            "B_matrix": "H_{t,j}(v)",
            "ambient_equations": "B_matrix * ell = 0, A_matrix * ell != 0",
            "split_chart_relation": (
                "The split-locator infinity chart is contained in this ambient "
                "linear chart."
            ),
        },
        "outcomes": {
            "empty": {
                "condition": "ker H_{t,j}(v) subset ker H_{t,j}(u)",
                "equivalent_rank_test": (
                    "rank stack(H_{t,j}(v), H_{t,j}(u)) = rank H_{t,j}(v)"
                ),
                "end_state": "empty",
                "projective_infinity_contribution": 0,
            },
            "ambient_nonempty": {
                "condition": "ker H_{t,j}(v) not subset ker H_{t,j}(u)",
                "equivalent_rank_test": (
                    "rank stack(H_{t,j}(v), H_{t,j}(u)) > rank H_{t,j}(v)"
                ),
                "end_state": "dimension_degree",
                "dimension_degree_bound": 1,
                "projective_infinity_contribution_upper_bound": 1,
                "split_nonemptiness_claimed": False,
            },
        },
        "specializations": {
            "direction_full_column_rank": {
                "condition": "rank H_{t,j}(v)=j+1",
                "kernel": "0",
                "end_state": "empty",
                "projective_infinity_contribution": 0,
            },
            "proportional_pencil": {
                "condition": "u=c v",
                "kernel_containment": "ker H(v) subset ker H(u)",
                "end_state": "empty",
                "projective_infinity_contribution": 0,
            },
            "zero_direction_syndrome": {
                "condition": "v=0",
                "kernel_containment_empty_test": "H_{t,j}(u)=0",
                "if_nonempty": "the single endpoint is tangent/common-code-line paid by the zero-v endpoint ledger",
            },
        },
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
    }


def build_certificate() -> dict[str, Any]:
    field = Field(P, MODULUS)
    descriptor = load_json(ROW_DESCRIPTOR_REF)
    projective_rank = load_json(PROJECTIVE_INFINITY_REF)

    require(descriptor["row"]["n"] == N, "descriptor n mismatch")
    require(descriptor["row"]["k"] == K, "descriptor k mismatch")
    require(descriptor["row"]["field"] == "F_17^32", "descriptor field mismatch")
    require(descriptor["row"]["field_order"] == Q_LINE, "descriptor q mismatch")
    require(descriptor["row"]["syndrome_length"] == N - K, "syndrome length mismatch")
    require(
        projective_rank["schema_version"]
        == "f17-32-m3-projective-infinity-rank-criterion-v1",
        "unexpected projective-infinity rank schema",
    )
    require(projective_rank["window"]["A_min"] == A_MIN, "projective rank A_min mismatch")
    require(projective_rank["window"]["A_max"] == A_MAX, "projective rank A_max mismatch")

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
        total_row_sets == projective_rank["window"]["all_row_set_total"],
        "projective-rank row-set total mismatch",
    )

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED",
        "object": "M5 ambient projective-infinity kernel-containment chart",
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
            "projective_infinity_rank_criterion": {
                "ref": PROJECTIVE_INFINITY_REF,
                "sha256": sha256_file(PROJECTIVE_INFINITY_REF),
            },
        },
        "window": {
            "A_min": A_MIN,
            "A_max": A_MAX,
            "agreement_count": len(records),
            "all_row_set_total": total_row_sets,
        },
        "kernel_chart_decision_table": kernel_chart_decision_table(),
        "theorem": {
            "statement": (
                "For fixed A,u,v, the ambient linear projective-infinity "
                "chart B ell = 0, A ell != 0 is empty iff "
                "ker H_{t,j}(v) is contained in ker H_{t,j}(u)."
            ),
            "rank_test": (
                "Equivalently, it is empty iff rank stack(H(v),H(u)) = "
                "rank H(v); otherwise the projective parameter contribution "
                "is the single endpoint [0:1]."
            ),
            "proof": [
                "The infinity chart equations are B ell = 0 with A ell nonzero.",
                "If ker B is contained in ker A, no vector satisfying B ell=0 can satisfy A ell !=0.",
                "If ker B is not contained in ker A, choose ell in ker B outside ker A; this gives an ambient chart point.",
                "The split-locator chart is a sublocus of the ambient chart, so ambient emptiness proves split emptiness and ambient nonemptiness gives a safe one-point dimension-degree fallback.",
            ],
            "m5_end_states": {
                "kernel_containment": "empty",
                "kernel_noncontainment": "dimension_degree with projective parameter degree 1",
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
            "projective_infinity_max_extra_parameters": 1,
            "finite_affine_impact": 0,
            "full_rank_direction_end_state": "empty",
            "proportional_pencil_end_state": "empty",
            "rank_deficient_direction_end_states": ["empty", "dimension_degree"],
        },
        "checks": [
            "row descriptor and projective-rank dependency schemas match",
            "window is 385..426",
            "row-set totals match the projective-infinity rank criterion",
            "domain encodings round-trip in the printed F_17^32 model",
            "kernel-containment and stacked-rank tests are equivalent by rank-nullity",
        ],
        "nonclaims": [
            "does not claim ambient nonempty implies split-locator nonempty",
            "does not compute finite affine root tables",
            "does not prove a projective safe-side row bound",
            "does not classify quotient or extension overlap for finite roots",
        ],
    }


def check_certificate(path: Path) -> None:
    expected = render(build_certificate())
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"M5 projective-infinity kernel certificate mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    window = certificate["window"]
    summary = certificate["summary"]
    print("F_17^32 M5 projective-infinity kernel chart")
    print(
        "A={A_min}..{A_max}, agreements={agreement_count}, row sets={all_row_set_total}".format(
            **window
        )
    )
    print(
        "rank-deficient infinity end states={rank_deficient_direction_end_states}, max extra projective parameters={projective_infinity_max_extra_parameters}".format(
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
