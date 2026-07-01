#!/usr/bin/env python3
"""Verify the lower-rank zero-u branch is contained, not aperiodic."""

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


SCHEMA_VERSION = "f17-32-m3-lower-rank-contained-v1"
Q_LINE = 17**32
A_MIN = 385
A_MAX = 426
ROW_DESCRIPTOR_REF = (
    "experimental/data/certificates/hankel-f17-32-row-descriptor/"
    "f17_32_n512_k256_hankel_row_descriptor.json"
)
WEIGHT_UNIFORM_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-weight-uniform-canonical-gcd/"
    "f17_32_n512_k256_m3_weight_uniform_canonical_gcd.json"
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


def support_choice_sum(max_rank: int) -> int:
    return sum(comb(N, rank) for rank in range(max_rank + 1))


def agreement_record(agreement: int) -> dict[str, Any]:
    j_value = N - agreement
    t_value = agreement - K
    max_lower_rank = j_value
    forced_zero_count_min = agreement - max_lower_rank
    require(forced_zero_count_min >= K, f"A={agreement}: zero-forcing inequality failed")
    return {
        "A": agreement,
        "j": j_value,
        "t": t_value,
        "regular_minor_size": j_value + 1,
        "lower_support_rank_range": {"min": 0, "max": max_lower_rank},
        "support_choice_count_sum": support_choice_sum(max_lower_rank),
        "weight_choice_formula_by_rank": "(17^32 - 1)^r for rank r>=1; 1 for rank 0",
        "regular_bucket_status": "singular_all_maximal_minors_zero",
        "hankel_rank_bound": "rank H(v) <= r <= j < j+1",
        "agreement_witness": "zero codeword on D\\S gives agreement n-r >= A",
        "noncontainment_filter": {
            "forced_zero_count_min": forced_zero_count_min,
            "zero_forcing_threshold": K,
            "reason": (
                "Any degree-<k codeword agreeing with the line word on an "
                "agreement support W has at least |W\\S| >= A-r >= A-j "
                "zeros outside S; in this window A-j >= k, so the codeword is zero."
            ),
            "contained_support": "W subset D\\S, where both f=0 and g=0 are codeword restrictions",
            "supportwise_noncontained_slope_count": 0,
            "residual_aperiodic_slope_count": 0,
        },
        "paid_or_removed_as": "contained/common-code-line branch",
        "schema_residual_label_if_packetized": "tangent",
    }


def build_certificate() -> dict[str, Any]:
    field = Field(P, MODULUS)
    descriptor = load_json(ROW_DESCRIPTOR_REF)
    weight_uniform = load_json(WEIGHT_UNIFORM_REF)

    require(descriptor["row"]["n"] == N, "descriptor n mismatch")
    require(descriptor["row"]["k"] == K, "descriptor k mismatch")
    require(descriptor["row"]["field"] == "F_17^32", "descriptor field mismatch")
    require(descriptor["row"]["field_order"] == Q_LINE, "descriptor q mismatch")
    require(
        descriptor["m3_regular_window"]["A_min"] == A_MIN
        and descriptor["m3_regular_window"]["A_max"] == A_MAX,
        "descriptor M3 window mismatch",
    )
    require(
        weight_uniform["schema_version"] == "f17-32-m3-weight-uniform-canonical-gcd-v1",
        "unexpected weight-uniform certificate schema",
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
    require(records[0]["noncontainment_filter"]["forced_zero_count_min"] == 258, "bad A=385 gap")
    require(records[-1]["noncontainment_filter"]["forced_zero_count_min"] == 340, "bad A=426 gap")

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT for lower-rank zero-u weighted branches",
        "object": "lower-rank singular bucket classified as contained/common-code-line",
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
            "weight_uniform_formula_certificate": {
                "ref": WEIGHT_UNIFORM_REF,
                "sha256": sha256_file(WEIGHT_UNIFORM_REF),
            },
        },
        "window": {
            "A_min": A_MIN,
            "A_max": A_MAX,
            "agreement_count": len(records),
            "lower_rank_condition": "0 <= r <= j = 512-A",
            "forced_zero_count_min_range": [
                records[0]["noncontainment_filter"]["forced_zero_count_min"],
                records[-1]["noncontainment_filter"]["forced_zero_count_min"],
            ],
            "zero_forcing_threshold": K,
        },
        "branch": {
            "support": "S subset H with rank r <= j",
            "weights": "nonzero weights w_i for x_i in S; rank 0 has no weights",
            "syndrome": "u_m=0, v_m=sum_{x_i in S} w_i x_i^m",
            "regular_singularity": (
                "H(v) has rank at most r, so every (j+1)x(j+1) maximal "
                "regular minor of H(u)+Z H(v)=Z H(v) is the zero polynomial."
            ),
            "contained_filter": (
                "For any slope and any agreement-at-least-A support W with a "
                "degree-<k explaining codeword p, p has at least A-r >= A-j "
                "zeros outside S. Since A-j >= k throughout 385<=A<=426, p=0. "
                "Thus W is contained in D\\S, where both line generators are "
                "zero codeword restrictions."
            ),
            "conclusion": (
                "The lower-rank zero-u singular bucket contributes no "
                "support-wise noncontained aperiodic slopes after the "
                "contained/common-code-line filter."
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
            "regular_bucket_status": "singular_all_maximal_minors_zero",
            "supportwise_noncontained_slope_count_after_filter": 0,
            "residual_aperiodic_slope_count_after_filter": 0,
            "residual_label": "contained/common-code-line",
            "schema_residual_label_if_packetized": "tangent",
        },
        "checks": [
            "all 512 descriptor-domain elements are distinct",
            "rank r<=j makes every (j+1)x(j+1) regular minor vanish",
            "A-j=2A-512 is at least k=256 for every A in 385..426",
            "any degree-<k explaining codeword is forced to be zero",
            "the resulting agreement support is contained/common-code-line, not aperiodic",
        ],
        "nonclaims": [
            "only zero-u weighted power-sum syndromes with support rank r<=j",
            "not rank j+1, which is handled by the weight-uniform gcd certificate",
            "not arbitrary length-256 M3 syndrome pencils",
            "not a quotient or extension ledger",
            "not a worst-case support-wise MCA row bound",
        ],
    }


def check_certificate(path: Path) -> None:
    expected = render(build_certificate())
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"lower-rank contained certificate mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    window = certificate["window"]
    summary = certificate["summary"]
    print("F_17^32 M3 lower-rank zero-u contained branch")
    print(
        "A={A_min}..{A_max}, lower rank={lower_rank_condition}, forced zero count range={forced_zero_count_min_range}".format(
            **window
        )
    )
    print(
        "regular status={regular_bucket_status}, residual aperiodic slopes={residual_aperiodic_slope_count_after_filter}".format(
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
