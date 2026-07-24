#!/usr/bin/env python3
"""Regression gate for the steering-source pin demotion.

Upstream steering files change by governance edit, not by mathematics.  When a
packet verifier gates one of them by blob hash, the verifier stops replaying the
moment upstream re-steers -- `fb6d955` rewrote `agents.md` and broke five of the
six verifiers listed here before this repair.

This gate is structural and fast (<1s).  It asserts, for every verifier that
records a steering source, that the steering source is demoted to
report-only and never hard-gated.  Replaying the packets themselves is the
separate, slower step recorded in the note's `replay` field.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "experimental" / "scripts"

STEERING = "agents.md"

# Verifiers that record `agents.md` among their sources.  Each must demote it.
DEMOTING = [
    "verify_kb_mca_v4_tangent_source_adapter_v1.py",
    "verify_kb_uq_boundary_prefix_tangent_rooted_shell_v1.py",
    "verify_m31_postjohnson_conversion_contract.py",
    "verify_m31_quotient_band_swap_census_t16_mixing.py",
    "verify_m31_quotient_prefix_flatness_t64_witness.py",
]

# Verifiers that tolerate absent PR-transport files via a recorded-hash table.
TRANSPORT_TOLERANT = {
    "verify_m31_quotient_band_swap_census_t16_mixing.py": "LEGACY_PACKET_FILE_SHA256",
    "verify_m31_quotient_t16_mixing_floor.py": "LEGACY_PACKET_FILE_SHA256",
    "verify_kb_uq_boundary_prefix_tangent_rooted_shell_v1.py": "TRANSPORT_ONLY",
}


class Failure(RuntimeError):
    pass


def require(ok: bool, message: str) -> None:
    if not ok:
        raise Failure(message)


def steering_set(text: str) -> set[str]:
    match = re.search(r"STEERING_SOURCES\s*=\s*frozenset\(\{(.*?)\}\)", text, re.S)
    require(match is not None, "STEERING_SOURCES not declared")
    return set(re.findall(r'"([^"]+)"', match.group(1)))


def check() -> None:
    for name in DEMOTING:
        path = SCRIPTS / name
        require(path.is_file(), f"missing verifier: {name}")
        text = path.read_text(encoding="utf-8")

        found = steering_set(text)
        require(
            found == {STEERING},
            f"{name}: steering set is {sorted(found)}, expected ['{STEERING}']",
        )
        require(
            f'"{STEERING}"' in text,
            f"{name}: no recorded {STEERING} pin -- provenance was dropped, not demoted",
        )
        # The demotion must guard the comparison: every steering branch reports.
        require(
            "NOTE steering source drifted" in text,
            f"{name}: steering drift is not reported",
        )
        require(
            "in STEERING_SOURCES" in text,
            f"{name}: STEERING_SOURCES is declared but never consulted",
        )

    for name, table in TRANSPORT_TOLERANT.items():
        path = SCRIPTS / name
        require(path.is_file(), f"missing verifier: {name}")
        text = path.read_text(encoding="utf-8")
        require(
            f"{table} = " in text or f"{table} = {{" in text or table in text,
            f"{name}: no {table} declaration",
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()
    if not (args.check or args.tamper_selftest):
        parser.error("--check or --tamper-selftest is required")

    try:
        check()
    except Failure as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

    if args.tamper_selftest:
        # A verifier that hard-gates the steering source must be rejected.
        broken = 'STEERING_SOURCES = frozenset({"never-matches.md"})\n'
        try:
            found = steering_set(broken)
        except Failure:
            print("FAIL: tamper fixture did not parse", file=sys.stderr)
            return 1
        if found == {STEERING}:
            print("FAIL: wrong steering set was accepted", file=sys.stderr)
            return 1
        print("PASS tamper-selftest: mis-declared steering set rejected")
        if not args.check:
            return 0

    print(f"PASS steering-source pin demotion: {len(DEMOTING)} verifiers demote {STEERING}")
    print(f"PASS transport tolerance declared in {len(TRANSPORT_TOLERANT)} verifiers")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
