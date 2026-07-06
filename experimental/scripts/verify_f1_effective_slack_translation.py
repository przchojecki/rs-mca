#!/usr/bin/env python3
"""F1 effective-slack translation audit for frontier-adjacent rows.

Proof status: EXPERIMENTAL / AUDIT.

The upstream F1 full-orbit toy scanner has a sharp slack split: the simple
pole pencil grows at toy slack t=1, but vanishes at t>=2 on the tested menu.
This verifier translates the four deployed frontier-adjacent rows into the
same exact variable t=a-k.  It is a scoping guardrail, not an extension-cell
upper theorem.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[2]
FRONTIER_DIR = REPO / "experimental" / "data" / "certificates" / "frontier-adjacent"
ARTIFACT = FRONTIER_DIR / "f1_effective_slack_translation_v1.json"
F1_SCAN = FRONTIER_DIR / "f1_full_orbit_scan_v1.json"

ROW_FILES = {
    "KoalaBear MCA": "kb_mca_v1.packet.json",
    "KoalaBear list": "kb_list_v1.packet.json",
    "M31 MCA": "m31_mca_v1.packet.json",
    "M31 list": "m31_list_v1.packet.json",
}


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def current_pair(packet: dict[str, Any]) -> dict[str, int]:
    moved = packet.get("v14_moved_pair", {})
    if moved:
        new_pair = moved["new_pair"]
        return {
            "unsafe_a": int(new_pair["a0_prime"]),
            "adjacent_open_a": int(new_pair["a0_prime_plus_1"]),
            "source": "v14_moved_pair.new_pair",
        }
    target = packet["agreement_interval"]["one_step_target"]
    return {
        "unsafe_a": int(target["a0"]),
        "adjacent_open_a": int(target["a0_plus_1"]),
        "source": "agreement_interval.one_step_target",
    }


def row_translation(name: str, packet: dict[str, Any]) -> dict[str, Any]:
    row = packet["row"]
    n = int(row["n"])
    k = int(row["k"])
    pair = current_pair(packet)
    unsafe_a = pair["unsafe_a"]
    open_a = pair["adjacent_open_a"]
    return {
        "row": name,
        "packet": ROW_FILES[name],
        "pair_source": pair["source"],
        "n": n,
        "k": k,
        "unsafe_a": unsafe_a,
        "adjacent_open_a": open_a,
        "unsafe_t_equals_a_minus_k": unsafe_a - k,
        "adjacent_open_t_equals_a_minus_k": open_a - k,
        "unsafe_j_equals_n_minus_a": n - unsafe_a,
        "adjacent_open_j_equals_n_minus_a": n - open_a,
        "effective_slack_bucket": "t>=2" if open_a - k >= 2 else "t=1",
    }


def toy_split(scan: dict[str, Any]) -> dict[str, Any]:
    growth = scan["growth_tables"]
    chain_t1 = growth["chain_t1"]["fit"]
    chain_t2 = growth["chain_t2"]["fit"]
    return {
        "source": "frontier-adjacent/f1_full_orbit_scan_v1.json",
        "chain_t1_verdict": chain_t1["verdict"],
        "chain_t1_points": chain_t1["points"],
        "chain_t2_verdict": chain_t2["verdict"],
        "chain_t2_points": chain_t2["points"],
        "overall_verdict_excerpt": scan["overall_verdict"],
    }


def build_certificate() -> dict[str, Any]:
    scan = read_json(F1_SCAN)
    rows = [
        row_translation(name, read_json(FRONTIER_DIR / filename))
        for name, filename in ROW_FILES.items()
    ]
    cert = {
        "schema": "f1-effective-slack-translation-v1",
        "status": "EXPERIMENTAL_AUDIT",
        "target": (
            "Translate deployed frontier-adjacent rows into the F1 toy scanner's "
            "slack variable t=a-k, to identify whether the toy t=1 growth branch "
            "or the toy t>=2 vanishing branch is the direct analogy."
        ),
        "toy_split": toy_split(scan),
        "rows": rows,
        "summary": {
            "all_adjacent_open_rows_have_t_at_least_2": all(
                row["adjacent_open_t_equals_a_minus_k"] >= 2 for row in rows
            ),
            "adjacent_open_t_values": {
                row["row"]: row["adjacent_open_t_equals_a_minus_k"] for row in rows
            },
            "interpretation": (
                "The current deployed adjacent rows are not toy-slack t=1 rows. "
                "Under the direct variable translation t=a-k, they lie deep in "
                "the t>=2 bucket where the upstream simple-pole pencil scan "
                "vanishes on the tested menu.  This does not prove paid_extension "
                "safe; it scopes the t=1 growth falsifier as a corrected-reserve "
                "warning rather than deployed-shape evidence."
            ),
        },
        "non_claims": [
            "does not prove paid_extension(a) is safe",
            "does not classify all genuinely F-valued pairs",
            "does not rule out other extension-cell counterexamples",
            "does not promote the toy scanner to a deployed theorem",
            "does not consume or resolve the open M1/L1/sparse residual cells",
        ],
    }
    validate(cert)
    return cert


def validate(cert: dict[str, Any]) -> None:
    if cert.get("schema") != "f1-effective-slack-translation-v1":
        raise AssertionError("unexpected schema")
    if cert.get("status") != "EXPERIMENTAL_AUDIT":
        raise AssertionError("unexpected status")
    expected_t = {
        "KoalaBear MCA": 67_472,
        "KoalaBear list": 67_471,
        "M31 MCA": 67_448,
        "M31 list": 67_447,
    }
    actual_t = cert["summary"]["adjacent_open_t_values"]
    if actual_t != expected_t:
        raise AssertionError(f"unexpected adjacent t-values: {actual_t}")
    if not cert["summary"]["all_adjacent_open_rows_have_t_at_least_2"]:
        raise AssertionError("adjacent row classified outside t>=2")
    toy = cert["toy_split"]
    if "GROWING" not in toy["chain_t1_verdict"]:
        raise AssertionError("toy t=1 branch no longer records growth")
    if "CONSTANT_ZERO" not in toy["chain_t2_verdict"]:
        raise AssertionError("toy t=2 branch no longer records zero collapse")
    for row in cert["rows"]:
        if row["adjacent_open_a"] != row["unsafe_a"] + 1:
            raise AssertionError(f"non-adjacent pair for {row['row']}")
        if row["adjacent_open_t_equals_a_minus_k"] != row["adjacent_open_a"] - row["k"]:
            raise AssertionError(f"bad t arithmetic for {row['row']}")
        if row["adjacent_open_j_equals_n_minus_a"] != row["n"] - row["adjacent_open_a"]:
            raise AssertionError(f"bad j arithmetic for {row['row']}")


def assert_same(expected: dict[str, Any], actual: dict[str, Any]) -> None:
    if expected != actual:
        raise AssertionError(
            "certificate mismatch\nexpected:\n"
            + json.dumps(expected, indent=2, sort_keys=True)
            + "\nactual:\n"
            + json.dumps(actual, indent=2, sort_keys=True)
        )


def tamper_selftest(cert: dict[str, Any]) -> None:
    bad = json.loads(json.dumps(cert))
    bad["rows"][0]["adjacent_open_t_equals_a_minus_k"] -= 1
    try:
        validate(bad)
    except AssertionError:
        return
    raise AssertionError("tamper selftest failed")


def print_summary(cert: dict[str, Any]) -> None:
    print("f1_effective_slack_translation")
    print(f"  status: {cert['status']}")
    print(f"  interpretation: {cert['summary']['interpretation']}")
    for row in cert["rows"]:
        print(
            f"  {row['row']}: a_open={row['adjacent_open_a']} "
            f"t={row['adjacent_open_t_equals_a_minus_k']} "
            f"j={row['adjacent_open_j_equals_n_minus_a']} "
            f"bucket={row['effective_slack_bucket']}"
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit-defaults", action="store_true")
    parser.add_argument("--check", type=Path)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()

    cert = build_certificate()
    if args.tamper_selftest:
        tamper_selftest(cert)
    if args.emit_defaults:
        ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
        ARTIFACT.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n")
        print(f"wrote {ARTIFACT.relative_to(REPO)}")
    if args.check:
        actual = read_json(args.check)
        validate(actual)
        assert_same(cert, actual)
        print(f"checked {args.check}")
    if args.json:
        print(json.dumps(cert, indent=2, sort_keys=True))
    if not args.emit_defaults and not args.check and not args.json:
        print_summary(cert)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
