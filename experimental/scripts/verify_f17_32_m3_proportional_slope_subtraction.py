#!/usr/bin/env python3
"""Verify the F_17^32 M3 proportional-slope subtraction sidecar.

For a syndrome pencil with u=c*v, the regular Hankel matrix satisfies

    H(u) + Z H(v) = (c+Z) H(v).

Thus any nonzero selected maximal minor is det(H(v))*(Z+c)^(j+1), with the
single finite root Z=-c.  At that slope the full syndrome of the line word is
zero, so the root is paid by the tangent/common-code-line ledger rather than
by a new aperiodic branch.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
from hashlib import sha256
from pathlib import Path
import sys
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from experimental.scripts.emit_f17_32_hankel_row_descriptor import (  # noqa: E402
    Field,
    MODULUS,
    N,
    P,
)


SCHEMA_VERSION = "f17-32-m3-proportional-slope-subtraction-v1"
AGREEMENT = 426
SCALAR = 5
TANGENT_ROOT = 12

INPUT_REF = (
    "experimental/data/hankel-regular-minor-inputs/"
    "f17_32_n512_k256_a426_scalar5_rank_witness_input.json"
)
PACKET_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-proportional-a426/"
    "f17_32_n512_k256_a426_scalar5_packet.json"
)
OUTPUT_PATH = REPO_ROOT / (
    "experimental/data/certificates/hankel-f17-32-m3-proportional-a426/"
    "f17_32_n512_k256_a426_scalar5_subtraction.json"
)
SCHEMA_CHECKER = REPO_ROOT / "scripts/check_aperiodic_eliminant_packet.py"
SCHEMA = REPO_ROOT / "scripts/aperiodic_eliminant_schema.json"


def load_json(ref: str | Path) -> dict[str, Any]:
    path = ref if isinstance(ref, Path) else REPO_ROOT / ref
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(ref: str) -> str:
    return sha256((REPO_ROOT / ref).read_bytes()).hexdigest()


def hash_json(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return sha256(payload).hexdigest()


def render(value: dict[str, Any]) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_schema_checker():
    spec = importlib.util.spec_from_file_location(
        "check_aperiodic_eliminant_packet", SCHEMA_CHECKER
    )
    require(spec is not None and spec.loader is not None, "could not load schema checker")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def encoded_scalar_multiple(field: Field, scalar_encoded: int, values: list[int]) -> list[int]:
    scalar = field.decode(scalar_encoded)
    return [field.encode(field.mul(scalar, field.decode(value))) for value in values]


def check_input(input_data: dict[str, Any]) -> None:
    syndrome = input_data["line_syndrome"]
    require(input_data["certificate_mode"] == "scalar_multiple_roots", "bad mode")
    require(syndrome["scalar_multiple_u_over_v"] == SCALAR, "bad scalar")
    require(syndrome["tangent_root"] == TANGENT_ROOT, "bad tangent root")
    require(syndrome["length"] == N // 2, "unexpected syndrome length")
    field = Field(P, MODULUS)
    expected_u = encoded_scalar_multiple(field, SCALAR, syndrome["v"])
    require(syndrome["u"] == expected_u, "u is not c*v in the pinned field")


def check_packet(packet: dict[str, Any], input_data: dict[str, Any]) -> None:
    checker = load_schema_checker()
    checker.check_path(REPO_ROOT / PACKET_REF, SCHEMA)
    require(packet["extractor"]["certificate_mode"] == "scalar_multiple_roots", "bad packet mode")
    require(packet["extractor"]["input_sha256"] == sha256_file(INPUT_REF), "input hash mismatch")
    require(packet["root_union"] == [TANGENT_ROOT], "root union mismatch")
    require(packet["declared_aperiodic_numerator"] == 1, "numerator mismatch")
    require(
        packet["claim_scope"]["may_be_used_for_threshold_pinning"] is False,
        "proportional packet must stay non-pinning",
    )
    require(packet["exact_agreements"][0]["A"] == AGREEMENT, "agreement mismatch")
    item = packet["exact_agreements"][0]
    require(item["regular_minor_data"]["roots"] == [TANGENT_ROOT], "regular root mismatch")
    require(item["regular_minor"]["degree"] == item["j"] + 1, "degree mismatch")
    require(
        input_data["line_syndrome"]["tangent_root"] == packet["root_union"][0],
        "input tangent root does not match packet root",
    )


def build_certificate() -> dict[str, Any]:
    input_data = load_json(INPUT_REF)
    packet = load_json(PACKET_REF)
    check_input(input_data)
    check_packet(packet, input_data)
    item = packet["exact_agreements"][0]
    residual_roots = sorted(set(packet["root_union"]) - {TANGENT_ROOT})
    require(residual_roots == [], "proportional tangent subtraction left residual roots")
    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT for this synthetic proportional packet",
        "row": packet["row"],
        "scope": {
            "agreement": AGREEMENT,
            "packet_type": "synthetic proportional F_17^32 v9 packet",
            "sampler": packet["sampler"],
            "claim_scope": packet["claim_scope"],
        },
        "source_artifacts": {
            "proportional_input": {
                "ref": INPUT_REF,
                "sha256": sha256_file(INPUT_REF),
                "certificate_mode": input_data["certificate_mode"],
                "scalar_multiple_u_over_v": SCALAR,
                "tangent_root": TANGENT_ROOT,
            },
            "proportional_packet": {
                "ref": PACKET_REF,
                "sha256": sha256_file(PACKET_REF),
                "schema_version": packet["schema_version"],
                "declared_aperiodic_numerator_before_subtraction": packet[
                    "declared_aperiodic_numerator"
                ],
            },
        },
        "proportional_pencil_identity": {
            "syndrome_identity": "Syn(f+z g)=u+zv=(c+z)v",
            "scalar_c": SCALAR,
            "removed_finite_slope": TANGENT_ROOT,
            "root_polynomial_shape": "Delta_A(z)=det(H(v)_R)*(z+c)^(j+1)",
            "input_u_hash": hash_json(input_data["line_syndrome"]["u"]),
            "input_v_hash": hash_json(input_data["line_syndrome"]["v"]),
        },
        "subtraction_rule": {
            "name": "common_code_line_slope",
            "reason": (
                "At z=-c the full stored syndrome vector is zero, so the line "
                "word f+z g lies in the Reed-Solomon code and this regular root "
                "is charged to the tangent/common-code-line ledger."
            ),
            "removed_tangent_roots": [TANGENT_ROOT],
            "removed_quotient_support_roots": [],
            "removed_quotient_image_roots": [],
            "removed_extension_roots": [],
        },
        "per_agreement": [
            {
                "A": item["A"],
                "j": item["j"],
                "t": item["t"],
                "regular_minor_root_union_before_removed_ledgers": packet["root_union"],
                "B_ap_regular_before_removed_ledgers": len(packet["root_union"]),
                "B_tan_common_code_line": 1,
                "overlap_regular_tangent_roots": [TANGENT_ROOT],
                "aperiodic_root_union_after_removed_ledgers": residual_roots,
                "B_ap_after_removed_ledgers": len(residual_roots),
                "claim_status": "synthetic_packet_only",
            }
        ],
        "summary": {
            "regular_root_union_before_removed_ledgers": packet["root_union"],
            "tangent_root_union_removed": [TANGENT_ROOT],
            "aperiodic_root_union_after_removed_ledgers": [],
            "raw_regular_numerator": 1,
            "tangent_numerator_removed": 1,
            "deduped_aperiodic_numerator_after_removed_ledgers": 0,
            "actual_row_status": "not supplied",
            "next_required": (
                "Use the same proportional-root subtraction rule only as a "
                "removed-ledger check inside actual F_17^32 row packets."
            ),
        },
        "nonclaims": [
            "not a worst-case MCA bound",
            "not actual M3 row data",
            "not a full quotient/tangent subtraction table",
            "not a singular-pivot packet",
        ],
    }


def check_certificate(path: Path) -> None:
    expected = render(build_certificate())
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"proportional-slope subtraction mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    summary = certificate["summary"]
    print("F_17^32 M3 proportional-slope subtraction")
    print(f"A={certificate['scope']['agreement']}, c={SCALAR}, root={TANGENT_ROOT}")
    print(
        "roots: regular={regular_root_union_before_removed_ledgers} "
        "removed_tangent={tangent_root_union_removed} "
        "residual={aperiodic_root_union_after_removed_ledgers}".format(**summary)
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", type=Path, help="write deterministic certificate JSON")
    parser.add_argument("--check", type=Path, help="check deterministic certificate JSON")
    parser.add_argument("--json", action="store_true", help="print certificate JSON")
    args = parser.parse_args()

    certificate = build_certificate()
    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(render(certificate), encoding="utf-8")
    if args.check:
        check_certificate(args.check)
    if args.json:
        print(render(certificate), end="")
        return
    print_summary(certificate)


if __name__ == "__main__":
    main()
