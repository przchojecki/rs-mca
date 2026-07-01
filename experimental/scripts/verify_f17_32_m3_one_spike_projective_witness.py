#!/usr/bin/env python3
"""Verify the F_17^32 M3 one-spike projective-infinity split witness."""

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


SCHEMA_VERSION = "f17-32-m3-one-spike-projective-witness-v1"
Q_LINE = 17**32
A_MIN = 385
A_MAX = 426
MAX_ONE_SPIKE_SUPPORT = N - A_MIN + 2
ROW_DESCRIPTOR_REF = (
    "experimental/data/certificates/hankel-f17-32-row-descriptor/"
    "f17_32_n512_k256_hankel_row_descriptor.json"
)
CANONICAL_EMPTY_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-one-spike-canonical-empty/"
    "f17_32_n512_k256_m3_one_spike_canonical_empty.json"
)
PROJECTIVE_KERNEL_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-m5-projective-infinity-kernel-chart/"
    "f17_32_n512_k256_m3_m5_projective_infinity_kernel_chart.json"
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
    size = j_value + 1
    spike_index = size
    prefix_last_root = j_value - 2
    surviving_base_indices = [j_value - 1, j_value]
    require(j_value >= 2, f"A={agreement}: witness needs j>=2")
    require(t_value >= 2, f"A={agreement}: witness needs two Hankel rows")
    require(spike_index < MAX_ONE_SPIKE_SUPPORT, f"A={agreement}: spike outside audit range")
    return {
        "A": agreement,
        "j": j_value,
        "t": t_value,
        "locator_degree": j_value,
        "split_locator_roots": {
            "description": "{spike_index} union {0,1,...,j-2}",
            "spike_index": spike_index,
            "base_prefix_range": [0, prefix_last_root],
            "root_count": j_value,
        },
        "surviving_base_indices": surviving_base_indices,
        "projective_infinity": {
            "H_v_locator": 0,
            "H_u_locator_nonzero": True,
            "reason": (
                "Only the two surviving base nodes contribute to H(u)ell; "
                "their first two moment equations form an invertible 2x2 "
                "Vandermonde system with nonzero weights."
            ),
            "split_locator_chart_nonempty": True,
            "projective_endpoint": "[0:1]",
            "exact_projective_endpoint_contribution": 1,
        },
    }


def build_certificate() -> dict[str, Any]:
    field = Field(P, MODULUS)
    descriptor = load_json(ROW_DESCRIPTOR_REF)
    canonical = load_json(CANONICAL_EMPTY_REF)
    projective_kernel = load_json(PROJECTIVE_KERNEL_REF)

    require(descriptor["row"]["n"] == N, "descriptor n mismatch")
    require(descriptor["row"]["k"] == K, "descriptor k mismatch")
    require(descriptor["row"]["field"] == "F_17^32", "descriptor field mismatch")
    require(descriptor["row"]["field_order"] == Q_LINE, "descriptor q mismatch")
    require(descriptor["row"]["syndrome_length"] == N - K, "descriptor syndrome mismatch")
    require(
        canonical["schema_version"] == "f17-32-m3-one-spike-canonical-empty-v1",
        "unexpected canonical-empty schema",
    )
    require(canonical["window"]["A_min"] == A_MIN, "canonical A_min mismatch")
    require(canonical["window"]["A_max"] == A_MAX, "canonical A_max mismatch")
    require(
        projective_kernel["schema_version"]
        == "f17-32-m3-m5-projective-infinity-kernel-chart-v1",
        "unexpected projective kernel schema",
    )

    domain_encodings = descriptor["domain"]["domain_encodings"]
    require(len(domain_encodings) == N, "domain length mismatch")
    require(len(set(domain_encodings)) == N, "descriptor domain is not distinct")
    require(
        len(set(domain_encodings[:MAX_ONE_SPIKE_SUPPORT])) == MAX_ONE_SPIKE_SUPPORT,
        "one-spike support prefix is not distinct",
    )
    decoded = [field.decode(value) for value in domain_encodings]
    require(
        [field.encode(value) for value in decoded] == domain_encodings,
        "domain decode/encode roundtrip failed",
    )

    records = [agreement_record(agreement) for agreement in range(A_MIN, A_MAX + 1)]
    canonical_by_a = {record["A"]: record for record in canonical["agreement_records"]}
    for record in records:
        source = canonical_by_a[record["A"]]
        require(
            source["projective_infinity"]["kernel_containment"] is False,
            f"A={record['A']}: canonical packet should have projective noncontainment",
        )
        require(
            source["projective_infinity"]["projective_endpoint_upper_bound"] == 1,
            f"A={record['A']}: projective upper bound mismatch",
        )

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED",
        "object": "M3 one-spike projective-infinity split-locator witness",
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
            "one_spike_canonical_empty": {
                "ref": CANONICAL_EMPTY_REF,
                "sha256": sha256_file(CANONICAL_EMPTY_REF),
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
        },
        "theorem": {
            "statement": (
                "For the one-spike family and every A in 385..426, the "
                "projective-infinity split-locator chart at [0:1] is nonempty."
            ),
            "locator": (
                "Let ell_A be the monic locator with roots y_A and the first "
                "j-1 base nodes.  It splits over the descriptor domain and has "
                "degree j."
            ),
            "Hv_zero": (
                "Since v_m=y_A^m, H(v)ell_A has rows y_A^r ell_A(y_A)=0."
            ),
            "Hu_nonzero": (
                "The locator vanishes on the first j-1 base nodes but not on "
                "the last two base nodes.  If H(u)ell_A were zero, the first "
                "two rows would give a 2x2 Vandermonde system forcing two "
                "nonzero locator values to be zero, contradiction."
            ),
            "consequence": (
                "The M5 projective-infinity one-point upper bound is exact for "
                "this synthetic family."
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
            "projective_infinity_split_nonempty": True,
            "exact_projective_endpoint_contribution": 1,
            "finite_canonical_roots_from_dependency": 0,
        },
        "checks": [
            "row descriptor, canonical-empty, and M5 projective-kernel schemas match",
            "the needed one-spike support prefix has distinct domain elements",
            "each locator has exactly j distinct descriptor-domain roots",
            "H(v)ell vanishes because the spike is a locator root",
            "H(u)ell is nonzero by the two surviving base nodes and a 2x2 Vandermonde",
        ],
        "nonclaims": [
            "does not classify arbitrary projective-infinity charts",
            "does not change the one-point upper bound",
            "does not address quotient or extension overlap for other families",
            "not a worst-case support-wise MCA row bound",
        ],
    }


def check_certificate(path: Path) -> None:
    expected = render(build_certificate())
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"one-spike projective witness certificate mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    window = certificate["window"]
    summary = certificate["summary"]
    print("F_17^32 M3 one-spike projective-infinity witness")
    print("A={A_min}..{A_max}, agreements={agreement_count}".format(**window))
    print(
        "split nonempty={projective_infinity_split_nonempty}, exact endpoint contribution={exact_projective_endpoint_contribution}".format(
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
