#!/usr/bin/env python3
"""Build and verify the Paper D v9 smoke packet for the settled F_17^32 row.

This is a format/replay test, not a new theorem.  It reads the already
committed high-agreement threshold package, checks the decisive A=506 and
A=507 rows, and emits a v9 eliminant packet in which the known tangent
high-agreement ledger is charged and the residual aperiodic bucket is empty.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
from typing import Any


SOURCE_CERTIFICATE = Path(
    "experimental/data/certificates/high-agreement-threshold-package/"
    "f17_512_high_agreement_threshold_certificate.json"
)
OUTPUT_PACKET = Path(
    "experimental/data/certificates/hankel-smoke-f17-506-507/"
    "f17_32_hankel_smoke_506_507_packet.json"
)
N = 512
K = 256
AGREEMENTS = (506, 507)


def hash_json(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def load_source() -> dict[str, Any]:
    return json.loads(SOURCE_CERTIFICATE.read_text(encoding="utf-8"))


def require_checks(checks: dict[str, Any], label: str) -> None:
    failed = [key for key, value in checks.items() if value is not True]
    if failed:
        raise AssertionError((label, failed))


def source_row_for_agreement(source: dict[str, Any], agreement: int) -> dict[str, Any]:
    replay = source["definition_freeze"]["pure_mca_scanner_replay"]
    require_checks(replay["checks"], "pure_mca_scanner_replay")
    row = replay["threshold_rows"][str(agreement)]
    require_checks(row["checks"], f"threshold_row_{agreement}")
    return row


def ledger_ref(agreement: int) -> str:
    return (
        f"{SOURCE_CERTIFICATE}"
        "#definition_freeze.pure_mca_scanner_replay.threshold_rows."
        f"{agreement}"
    )


def build_packet() -> dict[str, Any]:
    source = load_source()
    source_hash = sha256_file(SOURCE_CERTIFICATE)
    source_row = source["row"]
    proof_input = source["proof_input"]
    affine = source["f17_512_affine"]
    require_checks(affine["checks"], "f17_512_affine")

    if source_row["n"] != N or source_row["k"] != K:
        raise AssertionError(("unexpected row", source_row))
    if affine["last_unsafe_agreement"] != 506:
        raise AssertionError(("unexpected unsafe agreement", affine))
    if affine["first_safe_agreement"] != 507:
        raise AssertionError(("unexpected safe agreement", affine))

    exact_agreements: list[dict[str, Any]] = []
    removed_ledgers: list[dict[str, Any]] = []
    root_numerator_table: list[dict[str, Any]] = []

    for agreement in AGREEMENTS:
        row = source_row_for_agreement(source, agreement)
        j = N - agreement
        t = agreement - K
        numerator = row["finite_line_numerator"]
        expected_numerator = N - agreement + 1
        if row["r"] != j or row["sigma"] != t:
            raise AssertionError(("bad row arithmetic", agreement, row))
        if numerator != expected_numerator:
            raise AssertionError(("bad tangent numerator", agreement, numerator))

        ledger_name = f"tangent_high_agreement_exact_A{agreement}"
        removed_ledgers.append(
            {
                "name": ledger_name,
                "numerator": numerator,
                "certificate_ref": ledger_ref(agreement),
            }
        )
        exact_agreements.append(
            {
                "A": agreement,
                "j": j,
                "t": t,
                "status": "empty",
                "empty_reason": (
                    "smoke packet: exact numerator is charged to the "
                    f"{ledger_name} removed ledger"
                ),
            }
        )
        root_numerator_table.append(
            {
                "A": agreement,
                "j": j,
                "t": t,
                "finite_line_numerator": numerator,
                "tangent_formula": "n-A+1",
                "budget": affine["budget"],
                "safe_at_target": row["safe_at_target"],
                "unsafe_at_target": row["unsafe_at_target"],
                "combined_verdict": row["combined_verdict"],
                "residual_aperiodic_roots_after_removal": 0,
                "removed_ledger": ledger_name,
            }
        )

    return {
        "schema_version": "aperiodic-hankel-eliminant-v1",
        "row": {
            "n": N,
            "k": K,
            "field": "F_17^32",
            "domain_hash": hash_json(
                {
                    "code": source_row["code"],
                    "source_certificate_sha256": source_hash,
                    "domain_description": (
                        "smooth domain H used by the high-agreement threshold "
                        "package; elements are not enumerated in this smoke packet"
                    ),
                }
            ),
            "domain_description": (
                "smooth domain H from the high-agreement threshold package; "
                "this smoke packet references the settled row rather than "
                "re-enumerating H"
            ),
        },
        "agreement_threshold": 506,
        "sampler": "finite_affine_line",
        "removed_ledgers": removed_ledgers,
        "exact_agreements": exact_agreements,
        "declared_aperiodic_numerator": 0,
        "root_union_table_ref": "inline:root_union",
        "root_union": [],
        "root_numerator_table": root_numerator_table,
        "source_certificate": {
            "path": str(SOURCE_CERTIFICATE),
            "sha256": source_hash,
            "proof_input": proof_input,
        },
        "threshold_summary": {
            "unsafe_agreement": 506,
            "unsafe_numerator": affine["unsafe_line_numerator"],
            "safe_agreement": 507,
            "safe_numerator": affine["safe_line_numerator"],
            "budget": affine["budget"],
            "status": affine["compiler_status"],
        },
        "status": "AUDIT",
        "nonclaims": [
            "not a new proof of the high-agreement tangent theorem",
            "not a new prize-row threshold",
            "not a regular-minor computation for the F_17^32 row",
            "not a lower-agreement M1 aperiodic local-limit theorem",
        ],
    }


def render(packet: dict[str, Any]) -> str:
    return json.dumps(packet, indent=2, sort_keys=True) + "\n"


def check_packet(path: Path) -> None:
    expected = render(build_packet())
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"packet mismatch: {path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", type=Path, help="write deterministic packet")
    parser.add_argument("--check", type=Path, help="check deterministic packet")
    parser.add_argument("--json", action="store_true", help="print packet JSON")
    args = parser.parse_args()

    packet = build_packet()
    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(render(packet), encoding="utf-8")
    if args.check:
        check_packet(args.check)
    if args.json:
        print(render(packet), end="")
        return

    print("Paper D v9 F_17^32 Hankel smoke packet")
    for row in packet["root_numerator_table"]:
        print(
            "A={A} j={j} t={t} numerator={finite_line_numerator} "
            "budget={budget} verdict={combined_verdict}".format(**row)
        )
    print("residual aperiodic numerator=0 after removed tangent ledgers")
    print("smoke packet checks passed")


if __name__ == "__main__":
    main()
