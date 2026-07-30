#!/usr/bin/env python3
"""Verify the KoalaBear m2 r2 dihedral outer-factor reduction."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any, Callable

if not __debug__:
    raise RuntimeError("verifier refuses optimized Python execution")


class VerificationError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


EXPERIMENTAL = Path(__file__).resolve().parents[1]
REPO_ROOT = EXPERIMENTAL.parent
CERTIFICATE = (
    EXPERIMENTAL
    / "data/certificates/kb-mca-v4-m2-r2-dihedral-outer-factor-reduction-v1"
    / "kb_mca_v4_m2_r2_dihedral_outer_factor_reduction_v1.json"
)
M2_PARENT = {
    "commit": "d4063dcd9c56835c3916ef792e263ea720a4d397",
    "certificate_path": "experimental/data/certificates/kb-mca-v4-m2-v4-outer-recurrence-router-v1/kb_mca_v4_m2_v4_outer_recurrence_router_v1.json",
    "certificate_blob_oid": "50d17f218bfa7d3acb211c946db0c025b9a98944",
    "certificate_payload_sha256": "fe8141810501fd7b3762a378210609177185972ec706bf9ac943fa398bd82d39",
    "imported_terminal": "M2_V4_STABILIZERS_OUTER_RECURRENCE_AND_SOURCE_PARITY",
}
GENUS_PARENT = {
    "commit": "f6bc4a2b2a6a5b3bba98f24a520c67ca3373dbbb",
    "certificate_path": "experimental/data/certificates/kb-mca-v4-m2-r2-full-v4-source-genus-drop-v1/kb_mca_v4_m2_r2_full_v4_source_genus_drop_v1.json",
    "certificate_blob_oid": "83e82b826ddfa2f5377e99f439be5f00900507c6",
    "certificate_payload_sha256": "9a2ea090568600356f27f3174aee6d08414217b26dbb8f7922931c64a151122f",
    "imported_terminal": "M2_R2_SOURCE_GENUS_ZERO_OR_ONE",
}
DIVISOR_PARENT = {
    "commit": "a14a05d9ba80068133e93e2fa77d6d1dc8828829",
    "certificate_path": "experimental/data/certificates/kb-mca-v4-degree60-decomposition-source-fiber-adapter-v1/kb_mca_v4_degree60_decomposition_source_fiber_adapter_v1.json",
    "certificate_blob_oid": "911bac3c1c5d1b4cd9822c59939d60e832b7ef23",
    "certificate_payload_sha256": "638190df24415e5609fa9c2f50dde8fd22bd150f60e7bef5cd1496cb22d75b4e",
    "imported_terminal": "PROVED_SOURCE_FIBER_ADAPTER_DEGREE5_DELETION_DEGREE30_REFINEMENT_ROW_OPEN",
}


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def payload_hash(value: dict[str, Any]) -> str:
    unhashed = copy.deepcopy(value)
    unhashed.pop("payload_sha256", None)
    return hashlib.sha256(canonical_json(unhashed).encode()).hexdigest()


def reject_duplicates(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise VerificationError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def parse_json(text: str, label: str) -> dict[str, Any]:
    try:
        value = json.loads(text, object_pairs_hook=reject_duplicates)
    except (json.JSONDecodeError, VerificationError) as error:
        raise VerificationError(f"cannot parse {label}: {error}") from error
    require(isinstance(value, dict), f"{label} is not an object")
    return value


def git_output(*args: str) -> str:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=REPO_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as error:
        raise VerificationError(error.stderr.strip()) from error
    return result.stdout.strip()


def outer_genus_rows() -> list[dict[str, Any]]:
    inputs = [
        (0, {"a": 2, "c": 2, "a*c": 2}),
        (1, {"a": 0, "c": 4, "a*c": 4}),
    ]
    rows = []
    for source_genus, fixed in inputs:
        total = sum(fixed.values())
        numerator = 2 * source_genus - 2 - total
        require(numerator % 4 == 0, "V4 Riemann--Hurwitz divisibility")
        outer_twice_genus_minus_two = numerator // 4
        require((outer_twice_genus_minus_two + 2) % 2 == 0, "outer genus parity")
        outer_genus = (outer_twice_genus_minus_two + 2) // 2
        passport = []
        for inertia, count in fixed.items():
            require(count % 2 == 0, "fixed points must form V4 orbits of size two")
            passport.extend([inertia] * (count // 2))
        rows.append(
            {
                "source_genus": source_genus,
                "fixed_points": fixed,
                "outer_genus": outer_genus,
                "branch_inertia": passport,
            }
        )
    require([row["outer_genus"] for row in rows] == [0, 0], "outer genus rows")
    return rows


def pole_sieve_rows() -> list[dict[str, Any]]:
    rows = []
    for degree in range(2, 31):
        if 30 % degree:
            continue
        if degree == 5:
            profile = {
                "generic_order_five_poles": 1,
                "simple_totally_ramified_poles": 1,
                "endpoint_order_five_poles": 6,
            }
            survives = True
        elif 6 % degree == 0:
            profile = {
                "generic_order_five_poles": 6 // degree,
                "simple_totally_ramified_poles": 0,
                "endpoint_order_five_poles": 6,
            }
            survives = True
        else:
            profile = None
            survives = False
        rows.append({"factor_degree": degree, "survives": survives, "profile": profile})
    require(
        [row["factor_degree"] for row in rows if row["survives"]] == [2, 3, 5, 6],
        "surviving factor degrees",
    )
    return rows


def build_certificate() -> dict[str, Any]:
    data = {
        "schema": "kb-mca-v4-m2-r2-dihedral-outer-factor-reduction-v1",
        "payload_sha256": "",
        "statement": {
            "workboard_item": "K3",
            "row": "KoalaBear MCA at 2^-128",
            "terminal": "M2_R2_DIHEDRAL_FACTOR_DEGREES_2_3_5_6",
            "ledger_movement": 0,
        },
        "parent_m2_router": copy.deepcopy(M2_PARENT),
        "parent_source_genus": copy.deepcopy(GENUS_PARENT),
        "parent_divisor_adapter": copy.deepcopy(DIVISOR_PARENT),
        "input": {
            "inner_degree": 2,
            "outer_degree": 30,
            "outer_component_bidegree": [2, 2],
            "component_stabilizer": "full_V4",
            "endpoint_pole_count": 6,
            "endpoint_pole_order": 5,
        },
        "outer_genus_replay": outer_genus_rows(),
        "dihedral_factor": {
            "projection_degrees": [2, 2],
            "projection_involutions_distinct": True,
            "generated_group": "finite D_n of order 2n",
            "right_factor": "degree-n Dickson/Chebyshev quotient",
            "factor_degree_divides": 30,
            "local_ramification_indices": "1,2,n",
        },
        "pole_sieve_replay": pole_sieve_rows(),
        "conclusion": {
            "outer_component_genus": 0,
            "surviving_factor_degrees": [2, 3, 5, 6],
            "excluded_factor_degrees": [10, 15, 30],
            "factor_degree_deleted_here": False,
            "terminal": "M2_R2_DIHEDRAL_FACTOR_DEGREES_2_3_5_6",
        },
        "nonclaims": [
            "no deletion of factor degree 2, 3, 5, or 6",
            "no deletion or payment of the full-V4 inner-degree-two type",
            "no source-star realization or exclusion",
            "no carrier, received-data, explaining-polynomial, or slope owner",
            "no u2, K3, KoalaBear row, endpoint, or prize closure",
            "no ledger movement",
        ],
    }
    data["payload_sha256"] = payload_hash(data)
    return data


def load_parent(binding: dict[str, Any], label: str) -> dict[str, Any]:
    commit = binding["commit"]
    path = binding["certificate_path"]
    require(
        git_output("rev-parse", f"{commit}:{path}") == binding["certificate_blob_oid"],
        f"{label} blob",
    )
    parent = parse_json(git_output("show", f"{commit}:{path}"), label)
    require(
        payload_hash(parent)
        == parent["payload_sha256"]
        == binding["certificate_payload_sha256"],
        f"{label} payload",
    )
    return parent


def verify_parents() -> None:
    m2 = load_parent(M2_PARENT, "m2 parent")
    require(m2["conclusion"]["terminal"] == M2_PARENT["imported_terminal"], "m2 terminal")
    require(m2["input"]["outer_degree"] == 30, "outer degree")
    require(m2["v4_stabilizer_replay"]["rows"][0] == {"r": 2, "delta": 4, "stabilizer": "V4"}, "full V4 row")

    genus = load_parent(GENUS_PARENT, "genus parent")
    require(genus["conclusion"]["terminal"] == GENUS_PARENT["imported_terminal"], "genus terminal")
    require(genus["conclusion"]["admissible_source_genera"] == [0, 1], "source genera")

    divisor = load_parent(DIVISOR_PARENT, "divisor parent")
    require(divisor["conclusion"]["status"] == DIVISOR_PARENT["imported_terminal"], "divisor terminal")
    degree_two = next(row for row in divisor["profiles"] if row["inner_degree"] == 2)
    require(degree_two["order_five_outer_poles"] == 6, "six outer poles")
    require(degree_two["simple_outer_poles"] == 0, "no simple endpoint poles")


def verify_certificate(data: dict[str, Any], check_git: bool = True) -> None:
    require(payload_hash(data) == data.get("payload_sha256"), "payload hash")
    require(data == build_certificate(), "certificate differs from exact reconstruction")
    if check_git:
        verify_parents()


def reseal(data: dict[str, Any]) -> None:
    data["payload_sha256"] = payload_hash(data)


def tamper_selftest(original: dict[str, Any]) -> int:
    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("m2-parent", lambda row: row["parent_m2_router"].__setitem__("certificate_blob_oid", "0" * 40)),
        ("genus-parent", lambda row: row["parent_source_genus"].__setitem__("certificate_payload_sha256", "0" * 64)),
        ("divisor-parent", lambda row: row["parent_divisor_adapter"].__setitem__("commit", "0" * 40)),
        ("outer-degree", lambda row: row["input"].__setitem__("outer_degree", 60)),
        ("bidegree", lambda row: row["input"]["outer_component_bidegree"].__setitem__(0, 3)),
        ("pole-count", lambda row: row["input"].__setitem__("endpoint_pole_count", 5)),
        ("outer-genus", lambda row: row["outer_genus_replay"][1].__setitem__("outer_genus", 1)),
        ("passport", lambda row: row["outer_genus_replay"][0]["branch_inertia"].pop()),
        ("group", lambda row: row["dihedral_factor"].__setitem__("generated_group", "infinite")),
        ("factor-divides", lambda row: row["dihedral_factor"].__setitem__("factor_degree_divides", 60)),
        ("pole-sieve", lambda row: row["pole_sieve_replay"][0].__setitem__("survives", False)),
        ("survivors", lambda row: row["conclusion"]["surviving_factor_degrees"].append(10)),
        ("delete", lambda row: row["conclusion"].__setitem__("factor_degree_deleted_here", True)),
        ("nonclaim", lambda row: row["nonclaims"].pop()),
    ]
    passed = 0
    for name, mutate in mutations:
        candidate = copy.deepcopy(original)
        mutate(candidate)
        reseal(candidate)
        try:
            verify_certificate(candidate, False)
        except VerificationError:
            passed += 1
        else:
            raise VerificationError(f"tamper survived: {name}")
    bad_hash = copy.deepcopy(original)
    bad_hash["payload_sha256"] = "0" * 64
    try:
        verify_certificate(bad_hash, False)
    except VerificationError:
        passed += 1
    else:
        raise VerificationError("tamper survived: payload")
    try:
        parse_json('{"x":1,"x":2}', "duplicate")
    except VerificationError:
        passed += 1
    else:
        raise VerificationError("duplicate key survived")
    return passed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()
    if not args.write and not args.check and not args.tamper_selftest:
        parser.error("at least one action is required")
    if args.write:
        verify_parents()
        data = build_certificate()
        CERTIFICATE.parent.mkdir(parents=True, exist_ok=True)
        CERTIFICATE.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
        print(f"WROTE: {CERTIFICATE.relative_to(REPO_ROOT)}")
    data = parse_json(CERTIFICATE.read_text(), str(CERTIFICATE))
    verify_certificate(data, True)
    print("PASS: full-V4 m2 r2 outer factor degrees are 2, 3, 5, 6")
    if args.tamper_selftest:
        count = tamper_selftest(data)
        print(f"PASS: {count}/{count} tamper mutations rejected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
