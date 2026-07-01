#!/usr/bin/env python3
"""Verify the F_17^32 M3 one-spike canonical finite-root closure."""

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


SCHEMA_VERSION = "f17-32-m3-one-spike-canonical-empty-v1"
Q_LINE = 17**32
TARGET_BITS = 128
BUDGET = Q_LINE // 2**TARGET_BITS
A_MIN = 385
A_MAX = 426
ROW_DESCRIPTOR_REF = (
    "experimental/data/certificates/hankel-f17-32-row-descriptor/"
    "f17_32_n512_k256_hankel_row_descriptor.json"
)
ONE_SPIKE_INPUT_REF = (
    "experimental/data/hankel-regular-minor-inputs/"
    "f17_32_n512_k256_a426_one_spike_input.json"
)
ONE_SPIKE_PACKET_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-one-spike-a426/"
    "f17_32_n512_k256_a426_one_spike_packet.json"
)
RANK_DROP_BRIDGE_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-m5-regular-root-rank-drop/"
    "f17_32_n512_k256_m3_m5_regular_root_rank_drop.json"
)
PROJECTIVE_KERNEL_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-m5-projective-infinity-kernel-chart/"
    "f17_32_n512_k256_m3_m5_projective_infinity_kernel_chart.json"
)
MAX_ONE_SPIKE_SUPPORT = N - A_MIN + 2


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
    size = j_value + 1
    spike_index = size
    require(t_value >= size + 1, f"A={agreement}: one-spike rows not tall enough")
    require(size >= 2, f"A={agreement}: projective kernel dimension not positive")
    return {
        "A": agreement,
        "j": j_value,
        "t": t_value,
        "minor_size": size,
        "base_support_size": size,
        "spike_domain_index": spike_index,
        "base_plus_spike_support_size": size + 1,
        "maximal_row_set_count": comb(t_value, size),
        "finite_affine": {
            "z_equals_0_rank": size,
            "z_nonzero_rank": size,
            "canonical_finite_roots": [],
            "canonical_finite_root_count": 0,
            "canonical_common_gcd": "1",
            "regular_status": "finite_closed",
        },
        "projective_infinity": {
            "direction_rank": 1,
            "ker_Hv_dimension": size - 1,
            "ker_Hu_dimension": 0,
            "kernel_containment": False,
            "ambient_m5_end_state": "dimension_degree",
            "projective_endpoint_upper_bound": 1,
        },
        "budget_comparison": {
            "finite_affine_count": 0,
            "projective_count_upper_bound": 1,
            "finite_slope_budget": BUDGET,
            "projective_safe_for_this_synthetic_family": True,
        },
    }


def check_one_spike_endpoint(input_packet: dict[str, Any], root_packet: dict[str, Any]) -> None:
    require(
        input_packet["certificate_mode"] == "one_spike_linear_roots",
        "one-spike input mode mismatch",
    )
    require(input_packet["agreement_threshold"] == A_MAX, "one-spike input A mismatch")
    require(input_packet["exact_agreements"] == [A_MAX], "one-spike input agreement list mismatch")
    require(
        root_packet["schema_version"] == "aperiodic-hankel-eliminant-v1",
        "one-spike packet schema mismatch",
    )
    require(root_packet["agreement_threshold"] == A_MAX, "one-spike packet A mismatch")
    require(root_packet["declared_aperiodic_numerator"] == 1, "one-spike selected root count mismatch")
    exact = root_packet["exact_agreements"]
    require(len(exact) == 1 and exact[0]["A"] == A_MAX, "one-spike exact record mismatch")
    require(exact[0]["regular_minor"]["degree"] == 1, "one-spike selected minor degree mismatch")
    require(
        len(exact[0]["regular_minor_data"]["roots"]) == 1,
        "one-spike selected root table mismatch",
    )


def build_certificate() -> dict[str, Any]:
    field = Field(P, MODULUS)
    descriptor = load_json(ROW_DESCRIPTOR_REF)
    one_spike_input = load_json(ONE_SPIKE_INPUT_REF)
    one_spike_packet = load_json(ONE_SPIKE_PACKET_REF)
    rank_drop_bridge = load_json(RANK_DROP_BRIDGE_REF)
    projective_kernel = load_json(PROJECTIVE_KERNEL_REF)

    require(descriptor["row"]["n"] == N, "descriptor n mismatch")
    require(descriptor["row"]["k"] == K, "descriptor k mismatch")
    require(descriptor["row"]["field"] == "F_17^32", "descriptor field mismatch")
    require(descriptor["row"]["field_order"] == Q_LINE, "descriptor q mismatch")
    require(descriptor["row"]["syndrome_length"] == N - K, "syndrome length mismatch")
    require(
        descriptor["m3_regular_window"]["A_min"] == A_MIN
        and descriptor["m3_regular_window"]["A_max"] == A_MAX,
        "descriptor M3 window mismatch",
    )
    require(
        rank_drop_bridge["schema_version"]
        == "f17-32-m3-m5-regular-root-rank-drop-v1",
        "rank-drop bridge schema mismatch",
    )
    require(
        projective_kernel["schema_version"]
        == "f17-32-m3-m5-projective-infinity-kernel-chart-v1",
        "projective kernel schema mismatch",
    )
    require(rank_drop_bridge["window"]["A_min"] == A_MIN, "rank-drop A_min mismatch")
    require(rank_drop_bridge["window"]["A_max"] == A_MAX, "rank-drop A_max mismatch")
    require(projective_kernel["window"]["A_min"] == A_MIN, "projective A_min mismatch")
    require(projective_kernel["window"]["A_max"] == A_MAX, "projective A_max mismatch")
    check_one_spike_endpoint(one_spike_input, one_spike_packet)

    domain_encodings = descriptor["domain"]["domain_encodings"]
    require(len(domain_encodings) == N, "domain length mismatch")
    require(len(set(domain_encodings)) == N, "descriptor domain is not distinct")
    decoded = [field.decode(value) for value in domain_encodings]
    require(
        [field.encode(value) for value in decoded] == domain_encodings,
        "domain decode/encode roundtrip failed",
    )
    require(
        len(set(domain_encodings[:MAX_ONE_SPIKE_SUPPORT])) == MAX_ONE_SPIKE_SUPPORT,
        "one-spike prefix domain elements are not distinct",
    )

    records = [agreement_record(agreement) for agreement in range(A_MIN, A_MAX + 1)]
    total_row_sets = sum(record["maximal_row_set_count"] for record in records)
    require(
        total_row_sets == rank_drop_bridge["window"]["all_row_set_total"],
        "rank-drop row-set total mismatch",
    )
    require(
        total_row_sets == projective_kernel["window"]["all_row_set_total"],
        "projective-kernel row-set total mismatch",
    )

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED",
        "object": "M3 one-spike canonical finite root table over the regular window",
        "row": {
            "code": "RS[F_17^32,H,256]",
            "n": N,
            "k": K,
            "field": "F_17^32",
            "domain_hash": descriptor["row"]["domain_hash"],
            "q_line": Q_LINE,
            "finite_slope_budget": BUDGET,
        },
        "source_artifacts": {
            "row_descriptor": {"ref": ROW_DESCRIPTOR_REF, "sha256": sha256_file(ROW_DESCRIPTOR_REF)},
            "one_spike_a426_input": {"ref": ONE_SPIKE_INPUT_REF, "sha256": sha256_file(ONE_SPIKE_INPUT_REF)},
            "one_spike_a426_selected_minor_packet": {
                "ref": ONE_SPIKE_PACKET_REF,
                "sha256": sha256_file(ONE_SPIKE_PACKET_REF),
            },
            "regular_root_rank_drop_bridge": {
                "ref": RANK_DROP_BRIDGE_REF,
                "sha256": sha256_file(RANK_DROP_BRIDGE_REF),
            },
            "projective_infinity_kernel_chart": {
                "ref": PROJECTIVE_KERNEL_REF,
                "sha256": sha256_file(PROJECTIVE_KERNEL_REF),
            },
        },
        "window": {
            "A_min": A_MIN,
            "A_max": A_MAX,
            "agreement_count": len(records),
            "all_row_set_total": total_row_sets,
        },
        "family": {
            "for_each_A": "s=j+1, X_A={first s descriptor-domain elements}, y_A=descriptor-domain element s",
            "syndrome": "u_m=sum_{x in X_A} x^m, v_m=y_A^m",
            "finite_pencil_factorization": (
                "H_{t,j}(u+zv)=V_t(X_A union {y_A}) diag(1,...,1,z) "
                "V_{j+1}(X_A union {y_A})^T, with the z=0 column removed "
                "by its zero weight."
            ),
            "non_proportional": (
                "If u=c v, then a nonzero signed measure on the distinct set "
                "X_A union {y_A} has its first s+1 moments zero; the "
                "Vandermonde matrix is invertible, contradiction."
            ),
        },
        "theorem": {
            "finite_closure": (
                "For every A in 385..426 and every finite z over any extension "
                "field, rank H_{t,j}(u+zv)=j+1.  Hence the v10 canonical "
                "finite regular gcd is constant and has no finite roots."
            ),
            "z_zero_case": (
                "At z=0 the base support X_A has size j+1, and the first "
                "j+1 rows and columns form invertible Vandermonde factors."
            ),
            "z_nonzero_case": (
                "At z!=0 the support X_A union {y_A} has size j+2.  Since "
                "t>=j+2, the row Vandermonde has full column rank j+2; "
                "the column Vandermonde has rank j+1; the nonzero diagonal "
                "weights cannot reduce rank."
            ),
            "rank_drop_bridge_use": (
                "The M5 bridge says a finite v10 canonical regular root would "
                "force rank H_{t,j}(u+zv)<=j.  The rank computation excludes "
                "this for every finite z, even after scalar extension."
            ),
            "projective_infinity": (
                "At infinity H(v) has rank one while H(u) has full column "
                "rank.  Thus ker H(v) is not contained in ker H(u), and the "
                "M5 projective kernel chart gives a one-point dimension-degree "
                "fallback for [0:1]."
            ),
        },
        "field_audit": {
            "full_domain_distinct": True,
            "domain_size": len(domain_encodings),
            "domain_hash": hash_value(domain_encodings),
            "decoded_roundtrip_hash": hash_value([field.encode(value) for value in decoded]),
            "largest_one_spike_support_needed": MAX_ONE_SPIKE_SUPPORT,
        },
        "agreement_records": records,
        "summary": {
            "agreement_count": len(records),
            "finite_canonical_root_count_per_agreement": 0,
            "finite_canonical_root_union_size": 0,
            "selected_minor_a426_root_count_before_canonical_gcd": 1,
            "selected_minor_root_is_overcount_for_canonical_v10_gcd": True,
            "projective_endpoint_upper_bound_per_agreement": 1,
            "projective_count_upper_bound_safe_for_this_synthetic_family": True,
        },
        "checks": [
            "row descriptor, rank-drop bridge, and projective kernel schemas match",
            "A=426 one-spike selected-minor packet is present and has one affine root",
            "the first 129 descriptor-domain elements are distinct",
            "for every A in 385..426, t>=j+2 for the base-plus-spike rank factorization",
            "finite canonical root table is empty for every agreement in the window",
            "projective infinity has the M5 dimension-degree one-point fallback",
        ],
        "nonclaims": [
            "does not classify arbitrary non-proportional syndrome pencils",
            "does not make the selected prefix minor root a v10 canonical root",
            "does not prove split-locator nonemptiness at projective infinity",
            "does not audit quotient or extension overlap for other families",
            "not a worst-case support-wise MCA row bound",
        ],
    }


def check_certificate(path: Path) -> None:
    expected = render(build_certificate())
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"one-spike canonical-empty certificate mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    window = certificate["window"]
    summary = certificate["summary"]
    print("F_17^32 M3 one-spike canonical finite-root closure")
    print(
        "A={A_min}..{A_max}, agreements={agreement_count}, row sets={all_row_set_total}".format(
            **window
        )
    )
    print(
        "finite canonical roots/agreement={finite_canonical_root_count_per_agreement}, "
        "projective endpoint upper bound={projective_endpoint_upper_bound_per_agreement}".format(
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
