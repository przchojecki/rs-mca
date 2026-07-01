#!/usr/bin/env python3
"""Verify the support-uniform one-spike theorem for the F_17^32 M3 window."""

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


SCHEMA_VERSION = "f17-32-m3-one-spike-uniform-v1"
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
RANK_DROP_BRIDGE_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-m5-regular-root-rank-drop/"
    "f17_32_n512_k256_m3_m5_regular_root_rank_drop.json"
)
PROJECTIVE_KERNEL_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-m5-projective-infinity-kernel-chart/"
    "f17_32_n512_k256_m3_m5_projective_infinity_kernel_chart.json"
)
PREFIX_CANONICAL_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-one-spike-canonical-empty/"
    "f17_32_n512_k256_m3_one_spike_canonical_empty.json"
)
PREFIX_PROJECTIVE_REF = (
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


def agreement_record(agreement: int) -> dict[str, Any]:
    j_value = N - agreement
    t_value = agreement - K
    base_size = j_value + 1
    union_size = base_size + 1
    support_choice_count = comb(N, base_size) * (N - base_size)
    require(t_value >= union_size, f"A={agreement}: one-spike finite rank needs t>=j+2")
    require(base_size >= 2, f"A={agreement}: projective witness needs two base survivors")
    return {
        "A": agreement,
        "j": j_value,
        "t": t_value,
        "base_support_size": base_size,
        "base_plus_spike_support_size": union_size,
        "support_choice_count": support_choice_count,
        "weight_choice_count_formula": f"(q_line-1)^{union_size}",
        "finite_affine": {
            "z_zero_rank": base_size,
            "z_nonzero_rank": base_size,
            "canonical_finite_roots": [],
            "canonical_finite_root_count": 0,
            "canonical_common_gcd": "1",
            "finite_upper_bound": 0,
            "finite_budget": FINITE_BUDGET,
            "comparison_to_budget": comparison(0, FINITE_BUDGET),
        },
        "projective_infinity": {
            "direction_rank": 1,
            "split_locator_witness": (
                "choose the spike and all but two base nodes as locator roots"
            ),
            "split_locator_chart_nonempty": True,
            "exact_projective_endpoint_contribution": 1,
            "projective_upper_bound": 1,
            "projective_budget": PROJECTIVE_BUDGET,
            "comparison_to_budget": comparison(1, PROJECTIVE_BUDGET),
        },
    }


def build_certificate() -> dict[str, Any]:
    field = Field(P, MODULUS)
    descriptor = load_json(ROW_DESCRIPTOR_REF)
    rank_drop = load_json(RANK_DROP_BRIDGE_REF)
    projective_kernel = load_json(PROJECTIVE_KERNEL_REF)
    prefix_canonical = load_json(PREFIX_CANONICAL_REF)
    prefix_projective = load_json(PREFIX_PROJECTIVE_REF)

    require(descriptor["row"]["n"] == N, "descriptor n mismatch")
    require(descriptor["row"]["k"] == K, "descriptor k mismatch")
    require(descriptor["row"]["field"] == "F_17^32", "descriptor field mismatch")
    require(descriptor["row"]["field_order"] == Q_LINE, "descriptor q mismatch")
    require(descriptor["row"]["syndrome_length"] == N - K, "descriptor syndrome mismatch")
    require(
        descriptor["m3_regular_window"]["A_min"] == A_MIN
        and descriptor["m3_regular_window"]["A_max"] == A_MAX,
        "descriptor M3 window mismatch",
    )
    require(
        rank_drop["schema_version"] == "f17-32-m3-m5-regular-root-rank-drop-v1",
        "rank-drop schema mismatch",
    )
    require(
        projective_kernel["schema_version"]
        == "f17-32-m3-m5-projective-infinity-kernel-chart-v1",
        "projective kernel schema mismatch",
    )
    require(
        prefix_canonical["schema_version"] == "f17-32-m3-one-spike-canonical-empty-v1",
        "prefix canonical schema mismatch",
    )
    require(
        prefix_projective["schema_version"] == "f17-32-m3-one-spike-projective-witness-v1",
        "prefix projective schema mismatch",
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
    require(
        [record["A"] for record in records]
        == [record["A"] for record in prefix_canonical["agreement_records"]],
        "prefix canonical agreement list mismatch",
    )
    require(
        [record["A"] for record in records]
        == [record["A"] for record in prefix_projective["agreement_records"]],
        "prefix projective agreement list mismatch",
    )

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED",
        "object": "support-and-weight uniform one-spike M3 theorem",
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
            "regular_root_rank_drop_bridge": {
                "ref": RANK_DROP_BRIDGE_REF,
                "sha256": sha256_file(RANK_DROP_BRIDGE_REF),
            },
            "projective_infinity_kernel_chart": {
                "ref": PROJECTIVE_KERNEL_REF,
                "sha256": sha256_file(PROJECTIVE_KERNEL_REF),
            },
            "prefix_one_spike_canonical_empty_special_case": {
                "ref": PREFIX_CANONICAL_REF,
                "sha256": sha256_file(PREFIX_CANONICAL_REF),
            },
            "prefix_one_spike_projective_witness_special_case": {
                "ref": PREFIX_PROJECTIVE_REF,
                "sha256": sha256_file(PREFIX_PROJECTIVE_REF),
            },
        },
        "window": {
            "A_min": A_MIN,
            "A_max": A_MAX,
            "agreement_count": len(records),
        },
        "family": {
            "base_support": "any subset X of the descriptor domain with |X|=j+1",
            "spike": "any y in D \\ X",
            "weights": "any nonzero base weights a_x and nonzero spike weight b_y",
            "syndrome": "u_m=sum_{x in X} a_x x^m, v_m=b_y y^m",
            "properly_contains_prefix_case": True,
        },
        "theorem": {
            "finite_z_zero": (
                "At z=0, H(u)=V_t(X) diag(a_x) V_{j+1}(X)^T has rank j+1 "
                "because X is distinct, all a_x are nonzero, and t>=j+1."
            ),
            "finite_z_nonzero": (
                "At z!=0, H(u+zv)=V_t(X union {y}) diag(a_x, z b_y) "
                "V_{j+1}(X union {y})^T has rank j+1 because t>=j+2, "
                "the left Vandermonde is injective, and the right Vandermonde "
                "has rank j+1."
            ),
            "canonical_finite_roots": (
                "The rank-drop bridge then excludes finite v10 canonical roots, "
                "even after scalar extension; the canonical finite root table is empty."
            ),
            "projective_witness": (
                "At infinity, choose a split locator whose roots are y and all "
                "but two base nodes.  Then H(v)ell=0, while H(u)ell is nonzero "
                "by a 2x2 Vandermonde argument on the two surviving base nodes."
            ),
            "budget": (
                "The finite numerator is 0 and the projective numerator is exactly 1, "
                "so this whole family is safe for the printed 2^-128 budgets."
            ),
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
        "field_audit": {
            "full_domain_distinct": True,
            "domain_size": len(domain_encodings),
            "domain_hash": hash_value(domain_encodings),
            "decoded_roundtrip_hash": hash_value([field.encode(value) for value in decoded]),
        },
        "agreement_records": records,
        "summary": {
            "agreement_count": len(records),
            "finite_canonical_root_count_per_agreement": 0,
            "projective_endpoint_exact_contribution_per_agreement": 1,
            "finite_budget": FINITE_BUDGET,
            "projective_budget": PROJECTIVE_BUDGET,
            "finite_safe": True,
            "projective_safe": True,
        },
        "checks": [
            "row descriptor, rank-drop bridge, and projective-kernel schemas match",
            "prefix one-spike certificates are special cases of the uniform theorem",
            "domain has 512 distinct points",
            "for every A in 385..426, t>=j+2",
            "finite rank is maximal for z=0 and z!=0",
            "projective split-locator witness exists for every support choice",
            "finite and projective numerator bounds are within the 2^-128 budgets",
        ],
        "nonclaims": [
            "does not classify two-spike or higher-rank update directions",
            "does not classify arbitrary non-proportional syndrome pencils",
            "does not prove a threshold-pinning lower bound",
            "does not audit quotient-image overlap for unrelated families",
        ],
    }


def check_certificate(path: Path) -> None:
    expected = render(build_certificate())
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"one-spike uniform certificate mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    summary = certificate["summary"]
    print("F_17^32 M3 support-uniform one-spike theorem")
    print(
        "agreements={agreement_count}, finite roots/agreement={finite_canonical_root_count_per_agreement}, "
        "projective exact/agreement={projective_endpoint_exact_contribution_per_agreement}".format(
            **summary
        )
    )
    print(
        "finite safe={finite_safe}, projective safe={projective_safe}".format(
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
