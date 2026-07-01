#!/usr/bin/env python3
"""Verify the M4 budget table for the F_17^32 M3 one-spike family."""

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

from experimental.scripts.emit_f17_32_hankel_row_descriptor import (  # noqa: E402
    Field,
    K,
    MODULUS,
    N,
    P,
)


SCHEMA_VERSION = "f17-32-m3-one-spike-m4-budget-v1"
Q_LINE = 17**32
PROJECTIVE_DENOMINATOR = Q_LINE + 1
TARGET_BITS = 128
FINITE_BUDGET = Q_LINE // 2**TARGET_BITS
PROJECTIVE_BUDGET = PROJECTIVE_DENOMINATOR // 2**TARGET_BITS
A_MIN = 385
A_MAX = 426
ROW_DESCRIPTOR_REF = (
    "experimental/data/certificates/hankel-f17-32-row-descriptor/"
    "f17_32_n512_k256_hankel_row_descriptor.json"
)
CANONICAL_EMPTY_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-one-spike-canonical-empty/"
    "f17_32_n512_k256_m3_one_spike_canonical_empty.json"
)
PROJECTIVE_WITNESS_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-one-spike-projective-witness/"
    "f17_32_n512_k256_m3_one_spike_projective_witness.json"
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


def comparison(value: int, budget: int) -> str:
    relation = "<=" if value <= budget else ">"
    return f"{value} {relation} {budget}"


def agreement_record(source: dict[str, Any]) -> dict[str, Any]:
    agreement = source["A"]
    finite_count = source["finite_affine"]["canonical_finite_root_count"]
    projective_bound = (
        finite_count + source["projective_infinity"]["projective_endpoint_upper_bound"]
    )
    require(finite_count == 0, f"A={agreement}: finite count should be zero")
    require(projective_bound == 1, f"A={agreement}: projective bound should be one")
    require(projective_bound <= PROJECTIVE_BUDGET, f"A={agreement}: projective budget exceeded")
    require(finite_count <= FINITE_BUDGET, f"A={agreement}: finite budget exceeded")
    return {
        "A": agreement,
        "j": source["j"],
        "t": source["t"],
        "finite_affine_sampler": {
            "denominator": Q_LINE,
            "denominator_formula": "|F|",
            "B_tan": 0,
            "B_quot_support": 0,
            "B_quot_image": 0,
            "B_ap_regular": 0,
            "B_ap_pivot": 0,
            "B_ext": 0,
            "deduped_total_upper_bound": 0,
            "budget": FINITE_BUDGET,
            "comparison_to_budget": comparison(0, FINITE_BUDGET),
            "status": "safe",
        },
        "projective_sampler": {
            "denominator": PROJECTIVE_DENOMINATOR,
            "denominator_formula": "|P^1(F)| = |F| + 1",
            "finite_canonical_roots": 0,
            "projective_infinity_upper_bound": 1,
            "projective_infinity_split_witness_lower_bound": 1,
            "projective_infinity_exact": True,
            "B_tan": 0,
            "B_quot_support": 0,
            "B_quot_image": 0,
            "B_ap_regular_finite": 0,
            "B_ap_projective_infinity": 1,
            "B_ap_regular_projective_total": 1,
            "B_ap_pivot": 0,
            "B_ext": 0,
            "deduped_total_upper_bound": 1,
            "budget": PROJECTIVE_BUDGET,
            "comparison_to_budget": comparison(1, PROJECTIVE_BUDGET),
            "status": "safe",
        },
        "ledger_note": (
            "No finite roots remain after the v10 canonical gcd.  The only "
            "projective contribution is the M5 one-point infinity fallback; "
            "counting it without quotient/tangent subtraction is already safe."
        ),
    }


def build_certificate() -> dict[str, Any]:
    field = Field(P, MODULUS)
    descriptor = load_json(ROW_DESCRIPTOR_REF)
    canonical = load_json(CANONICAL_EMPTY_REF)
    projective_witness = load_json(PROJECTIVE_WITNESS_REF)

    require(descriptor["row"]["n"] == N, "descriptor n mismatch")
    require(descriptor["row"]["k"] == K, "descriptor k mismatch")
    require(descriptor["row"]["field"] == "F_17^32", "descriptor field mismatch")
    require(descriptor["row"]["field_order"] == Q_LINE, "descriptor q mismatch")
    require(descriptor["row"]["syndrome_length"] == N - K, "descriptor syndrome mismatch")
    require(
        canonical["schema_version"] == "f17-32-m3-one-spike-canonical-empty-v1",
        "unexpected one-spike canonical schema",
    )
    require(canonical["window"]["A_min"] == A_MIN, "canonical A_min mismatch")
    require(canonical["window"]["A_max"] == A_MAX, "canonical A_max mismatch")
    require(
        canonical["summary"]["finite_canonical_root_count_per_agreement"] == 0,
        "canonical finite count summary mismatch",
    )
    require(
        canonical["summary"]["projective_endpoint_upper_bound_per_agreement"] == 1,
        "canonical projective endpoint summary mismatch",
    )
    require(
        projective_witness["schema_version"] == "f17-32-m3-one-spike-projective-witness-v1",
        "unexpected one-spike projective witness schema",
    )
    require(projective_witness["window"]["A_min"] == A_MIN, "projective witness A_min mismatch")
    require(projective_witness["window"]["A_max"] == A_MAX, "projective witness A_max mismatch")
    require(
        projective_witness["summary"]["exact_projective_endpoint_contribution"] == 1,
        "projective witness contribution mismatch",
    )

    domain_encodings = descriptor["domain"]["domain_encodings"]
    require(len(domain_encodings) == N, "domain length mismatch")
    require(len(set(domain_encodings)) == N, "descriptor domain is not distinct")
    decoded = [field.decode(value) for value in domain_encodings]
    require(
        [field.encode(value) for value in decoded] == domain_encodings,
        "domain decode/encode roundtrip failed",
    )

    records = [agreement_record(record) for record in canonical["agreement_records"]]
    require([record["A"] for record in records] == list(range(A_MIN, A_MAX + 1)), "A list mismatch")
    witness_by_a = {record["A"]: record for record in projective_witness["agreement_records"]}
    for record in records:
        witness = witness_by_a[record["A"]]
        require(
            witness["projective_infinity"]["exact_projective_endpoint_contribution"] == 1,
            f"A={record['A']}: projective witness contribution mismatch",
        )
        require(
            witness["projective_infinity"]["split_locator_chart_nonempty"] is True,
            f"A={record['A']}: projective witness nonempty mismatch",
        )

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT for this synthetic family",
        "object": "M4 budget table for the M3 one-spike canonical-empty family",
        "row": {
            "code": "RS[F_17^32,H,256]",
            "n": N,
            "k": K,
            "field": "F_17^32",
            "domain_hash": descriptor["row"]["domain_hash"],
        },
        "source_artifacts": {
            "row_descriptor": {"ref": ROW_DESCRIPTOR_REF, "sha256": sha256_file(ROW_DESCRIPTOR_REF)},
            "one_spike_canonical_empty": {
                "ref": CANONICAL_EMPTY_REF,
                "sha256": sha256_file(CANONICAL_EMPTY_REF),
            },
            "one_spike_projective_witness": {
                "ref": PROJECTIVE_WITNESS_REF,
                "sha256": sha256_file(PROJECTIVE_WITNESS_REF),
            },
        },
        "sampler_denominators": {
            "finite_affine_line": {
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
        "window": {
            "A_min": A_MIN,
            "A_max": A_MAX,
            "agreement_count": len(records),
        },
        "theorem": {
            "finite_affine": (
                "The one-spike canonical-empty packet gives zero finite v10 "
                "regular roots at every agreement; hence the finite affine "
                "aperiodic contribution is 0."
            ),
            "projective": (
                "Adding the M5 projective-infinity one-point dimension-degree "
                "fallback gives projective numerator at most 1 at every agreement; "
                "the split-locator witness proves this endpoint is actually present."
            ),
            "budget": (
                "Both finite and projective denominators have 2^-128 budget 6, "
                "so the family is safe with a large margin: 0<=6 finite and 1<=6 projective."
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
            "max_finite_affine_total_upper_bound": 0,
            "max_projective_total_upper_bound": 1,
            "projective_total_lower_bound": 1,
            "projective_total_exact": 1,
            "finite_budget": FINITE_BUDGET,
            "projective_budget": PROJECTIVE_BUDGET,
            "finite_safe": True,
            "projective_safe": True,
            "known_lower_bound": "projective endpoint contribution is exactly 1 for this synthetic family",
        },
        "checks": [
            "row descriptor, one-spike canonical-empty, and projective witness schemas match",
            "finite affine denominator is |F|",
            "projective denominator is |F|+1",
            "finite canonical root count is zero for each agreement",
            "projective endpoint upper bound is one for each agreement",
            "projective endpoint split-locator lower bound is one for each agreement",
            "deduped upper bounds are within the 2^-128 budgets",
        ],
        "nonclaims": [
            "does not prove a lower bound or threshold pinning statement",
            "does not classify arbitrary non-proportional pencils",
            "does not prove split-locator nonemptiness at projective infinity",
            "does not replace quotient/tangent subtraction tables for other families",
        ],
    }


def check_certificate(path: Path) -> None:
    expected = render(build_certificate())
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"one-spike M4 budget certificate mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    summary = certificate["summary"]
    print("F_17^32 M3 one-spike M4 budget table")
    print(
        "agreements={agreement_count}, finite max={max_finite_affine_total_upper_bound}, "
        "projective max={max_projective_total_upper_bound}".format(**summary)
    )
    print(
        "finite budget={finite_budget}, projective budget={projective_budget}".format(
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
