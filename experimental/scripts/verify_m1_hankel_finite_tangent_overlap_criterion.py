#!/usr/bin/env python3
"""Verify the finite tangent-overlap criterion for the M3 regular window."""

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


SCHEMA_VERSION = "f17-32-m3-finite-tangent-overlap-criterion-v1"
Q_LINE = 17**32
A_MIN = 385
A_MAX = 426
ROW_DESCRIPTOR_REF = (
    "experimental/data/certificates/hankel-f17-32-row-descriptor/"
    "f17_32_n512_k256_hankel_row_descriptor.json"
)
PROPORTIONAL_REF = (
    "experimental/data/certificates/hankel-proportional-pencil-tangent-lemma/"
    "hankel_proportional_pencil_tangent_lemma_certificate.json"
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


def agreement_record(agreement: int) -> dict[str, Any]:
    j_value = N - agreement
    t_value = agreement - K
    visible_length = t_value + j_value
    return {
        "A": agreement,
        "j": j_value,
        "t": t_value,
        "minor_size": j_value + 1,
        "maximal_row_set_count": comb(t_value, j_value + 1),
        "stored_syndrome_length": N - K,
        "visible_hankel_syndrome_indices": [0, visible_length - 1],
        "visible_hankel_syndrome_length": visible_length,
        "criterion": {
            "finite_tangent_slope_condition": "u + z v = 0 in all 256 stored coordinates",
            "nonzero_v_case": {
                "has_finite_tangent_overlap": "iff u=c v for a scalar c",
                "unique_tangent_slope": "z=-c",
            },
            "non_proportional_case": {
                "has_finite_tangent_overlap": False,
                "tangent_roots_removed_from_finite_root_table": 0,
            },
            "v_zero_u_nonzero_case": {
                "has_finite_tangent_overlap": False,
                "reason": "u+zv=u is never zero",
            },
            "u_zero_v_zero_case": {
                "has_finite_tangent_overlap": "all finite slopes",
                "residual_label": "tangent/common-code-line degenerate codeword line",
                "regular_status": "singular_all_maximal_minors_zero",
            },
        },
        "m4_root_subtraction_rule": {
            "non_proportional_pencil": "remove no finite roots as tangent/common-code-line",
            "proportional_nonzero_v_pencil": "remove the unique root z=-c when it appears",
            "zero_syndrome_line": "remove the whole degenerate codeword-line branch before aperiodic accounting",
        },
    }


def build_certificate() -> dict[str, Any]:
    field = Field(P, MODULUS)
    descriptor = load_json(ROW_DESCRIPTOR_REF)
    proportional = load_json(PROPORTIONAL_REF)

    require(descriptor["row"]["n"] == N, "descriptor n mismatch")
    require(descriptor["row"]["k"] == K, "descriptor k mismatch")
    require(descriptor["row"]["field"] == "F_17^32", "descriptor field mismatch")
    require(descriptor["row"]["field_order"] == Q_LINE, "descriptor q mismatch")
    require(descriptor["row"]["syndrome_length"] == N - K, "syndrome length mismatch")
    require(
        proportional["schema_version"] == "hankel-proportional-pencil-tangent-lemma-v1",
        "unexpected proportional-pencil certificate schema",
    )
    require(
        proportional["window"]["A_min"] == A_MIN
        and proportional["window"]["A_max"] == A_MAX,
        "proportional-pencil window mismatch",
    )

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
        total_row_sets == proportional["window"]["all_row_set_total"],
        "row-set count mismatch",
    )
    for record in records:
        require(
            record["visible_hankel_syndrome_length"] == N - K,
            f"A={record['A']}: visible Hankel syndrome is not the full stored syndrome",
        )

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT",
        "object": "finite tangent-overlap criterion for M3 regular roots",
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
            "proportional_pencil_tangent_lemma": {
                "ref": PROPORTIONAL_REF,
                "sha256": sha256_file(PROPORTIONAL_REF),
            },
        },
        "window": {
            "A_min": A_MIN,
            "A_max": A_MAX,
            "agreement_count": len(records),
            "all_row_set_total": total_row_sets,
        },
        "theorem": {
            "statement": (
                "For any finite slope z, the tangent/common-code-line overlap "
                "condition is exactly u+zv=0 in the full stored syndrome.  In "
                "the M3 window the regular Hankel chart sees all 256 stored "
                "syndrome coordinates, so this condition is equivalent to a "
                "proportional pencil u=(-z)v, except for the degenerate "
                "u=v=0 codeword-line branch."
            ),
            "proof_skeleton": [
                "A finite line point f+zg is a codeword iff its stored syndrome is zero.",
                "The stored syndrome is linear in the slope: Syn(f+zg)=u+zv.",
                "For every A in 385..426, the maximal Hankel entries use indices 0..t+j-1=255.",
                "Thus the visible Hankel relation is the full stored syndrome relation.",
                "If v is nonzero, u+zv=0 has a solution iff all nonzero coordinates give the same scalar u_m/v_m; then z=-c.",
                "If v=0, either u is nonzero and no finite tangent slope exists, or u=0 and the whole line is a degenerate codeword-line branch.",
            ],
            "m4_consequence": (
                "A future non-proportional finite regular root table has zero "
                "tangent/common-code-line overlap.  Tangent subtraction in the "
                "finite regular branch is exhausted by the proportional-pencil "
                "lemma and the degenerate zero-syndrome line."
            ),
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
            "non_proportional_finite_tangent_overlap": 0,
            "proportional_nonzero_v_tangent_roots": 1,
            "zero_syndrome_line_label": "tangent/common-code-line degenerate branch",
        },
        "checks": [
            "t+j=256 for every agreement in the M3 regular window",
            "the row-set totals agree with the proportional-pencil certificate",
            "the proportional certificate supplies the unique paid finite root in the nondegenerate proportional case",
            "the non-proportional case has no finite tangent/common-code-line overlap",
        ],
        "nonclaims": [
            "does not compute arbitrary non-proportional regular root tables",
            "does not classify non-tangent quotient or extension overlap",
            "does not close singular rank-deficient buckets",
            "not a worst-case support-wise MCA row bound",
        ],
    }


def check_certificate(path: Path) -> None:
    expected = render(build_certificate())
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"finite tangent-overlap certificate mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    window = certificate["window"]
    summary = certificate["summary"]
    print("F_17^32 M3 finite tangent-overlap criterion")
    print(
        "A={A_min}..{A_max}, agreements={agreement_count}, row sets={all_row_set_total}".format(
            **window
        )
    )
    print(
        "non-proportional finite tangent overlap={non_proportional_finite_tangent_overlap}".format(
            **summary
        )
    )
    print(
        "proportional nonzero-v tangent roots={proportional_nonzero_v_tangent_roots}".format(
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
