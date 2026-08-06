#!/usr/bin/env python3
"""Verify the KoalaBear m2 r2 full-V4 source genus drop."""

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
    / "data/certificates/kb-mca-v4-m2-r2-full-v4-source-genus-drop-v1"
    / "kb_mca_v4_m2_r2_full_v4_source_genus_drop_v1.json"
)
M2_PARENT = {
    "commit": "d4063dcd9c56835c3916ef792e263ea720a4d397",
    "certificate_path": "experimental/data/certificates/kb-mca-v4-m2-v4-outer-recurrence-router-v1/kb_mca_v4_m2_v4_outer_recurrence_router_v1.json",
    "certificate_blob_oid": "50d17f218bfa7d3acb211c946db0c025b9a98944",
    "certificate_payload_sha256": "fe8141810501fd7b3762a378210609177185972ec706bf9ac943fa398bd82d39",
    "imported_terminal": "M2_V4_STABILIZERS_OUTER_RECURRENCE_AND_SOURCE_PARITY",
}
CONIC_PARENT = {
    "commit": "ad109774f7d9bc320e7e0c046ba83471f39d5cd9",
    "certificate_path": "experimental/data/certificates/kb-mca-v4-q6-u2-complete-source-conic-exclusion-v1/kb_mca_v4_q6_u2_complete_source_conic_exclusion_v1.json",
    "certificate_blob_oid": "61afd4534740c5ccabc6196919126c80c361e4c5",
    "certificate_payload_sha256": "30a5d45895957f774ef972118e227fa54522fc27a48ee0e2a99a0d5a012a5451",
    "imported_terminal": "DELETED_BY_COMPLETE_SOURCE_DIVISOR_PROFILE_OBSTRUCTION",
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
            ["git", *args], cwd=REPO_ROOT, check=True, capture_output=True, text=True
        )
    except subprocess.CalledProcessError as error:
        raise VerificationError(error.stderr.strip()) from error
    return result.stdout.strip()


def compose(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(left[right[value]] for value in range(4))


def inverse(value: tuple[int, ...]) -> tuple[int, ...]:
    result = [0] * 4
    for source, target in enumerate(value):
        result[target] = source
    return tuple(result)


def conjugation_replay() -> dict[str, Any]:
    rotation = (1, 2, 3, 0)
    eta = (0, 3, 2, 1)
    a = compose(rotation, rotation)
    eta_a = compose(eta, a)
    require(
        compose(compose(rotation, eta), inverse(rotation)) == eta_a,
        "eta conjugation",
    )
    require(
        compose(compose(rotation, a), inverse(rotation)) == a,
        "a conjugation",
    )
    return {
        "deck_group": "V4=<eta,a>",
        "normalizer_witness": "D8 square action",
        "c_eta_c_inverse": "eta*a",
        "c_a_c_inverse": "a",
    }


def fixed_point_rows() -> list[dict[str, int | bool]]:
    rows = []
    for genus in range(4):
        n_eta = 2 * genus + 2
        n_eta_a = n_eta
        n_a = 2 * genus + 6 - n_eta - n_eta_a
        rows.append(
            {
                "genus": genus,
                "fix_eta": n_eta,
                "fix_a": n_a,
                "fix_eta_a": n_eta_a,
                "admissible": n_a >= 0,
            }
        )
    require(
        [(row["genus"], row["fix_a"]) for row in rows if row["admissible"]]
        == [(0, 2), (1, 0)],
        "admissible genus rows",
    )
    return rows


def build_certificate() -> dict[str, Any]:
    data = {
        "schema": "kb-mca-v4-m2-r2-full-v4-source-genus-drop-v1",
        "payload_sha256": "",
        "statement": {
            "workboard_item": "K3",
            "row": "KoalaBear MCA at 2^-128",
            "terminal": "M2_R2_SOURCE_GENUS_ZERO_OR_ONE",
            "ledger_movement": 0,
        },
        "parent_m2_router": copy.deepcopy(M2_PARENT),
        "parent_conic_exclusion": copy.deepcopy(CONIC_PARENT),
        "input": {
            "inner_degree": 2,
            "outer_subdegree": 2,
            "component_degree": 4,
            "component_stabilizer": "full_V4",
            "source_bidegree": [2, 4],
            "prior_source_genus_upper_bound": 3,
        },
        "source_cover": {
            "degree_over_X": 2,
            "degree_over_W": 4,
            "deck_group_over_W": "V4=<eta,a>",
            "eta_quotient_genus": 0,
            "characteristic_is_tame": True,
        },
        "conjugation_replay": conjugation_replay(),
        "fixed_point_replay": fixed_point_rows(),
        "conclusion": {
            "admissible_source_genera": [0, 1],
            "a_fixed_points_by_genus": {"0": 2, "1": 0},
            "genus_two_and_three_excluded": True,
            "r2_type_deleted": False,
            "terminal": "M2_R2_SOURCE_GENUS_ZERO_OR_ONE",
        },
        "nonclaims": [
            "no deletion of the rational source regime",
            "no deletion of the elliptic source regime",
            "no source-genus lower bound",
            "no outer bidegree-two correspondence classification",
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
    full = m2["v4_stabilizer_replay"]["rows"][0]
    require(full == {"r": 2, "delta": 4, "stabilizer": "V4"}, "full V4 row")
    require(m2["input"]["actual_component_bidegree"] == [4, 4], "component bidegree")

    conic = load_parent(CONIC_PARENT, "conic parent")
    require(conic["conclusion"]["terminal"] == CONIC_PARENT["imported_terminal"], "conic terminal")
    require("u=2 birational-quartic image branch" in conic["conclusion"]["still_open"], "quartic residual")


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
        ("conic-parent", lambda row: row["parent_conic_exclusion"].__setitem__("certificate_payload_sha256", "0" * 64)),
        ("subdegree", lambda row: row["input"].__setitem__("outer_subdegree", 4)),
        ("stabilizer", lambda row: row["input"].__setitem__("component_stabilizer", "C2")),
        ("bidegree", lambda row: row["input"]["source_bidegree"].__setitem__(1, 3)),
        ("cover-degree", lambda row: row["source_cover"].__setitem__("degree_over_W", 2)),
        ("deck-group", lambda row: row["source_cover"].__setitem__("deck_group_over_W", "C4")),
        ("tame", lambda row: row["source_cover"].__setitem__("characteristic_is_tame", False)),
        ("conjugation", lambda row: row["conjugation_replay"].__setitem__("c_eta_c_inverse", "eta")),
        ("fixed-row", lambda row: row["fixed_point_replay"][1].__setitem__("fix_a", 2)),
        ("genera", lambda row: row["conclusion"]["admissible_source_genera"].append(2)),
        ("fixed-map", lambda row: row["conclusion"]["a_fixed_points_by_genus"].__setitem__("1", 2)),
        ("delete", lambda row: row["conclusion"].__setitem__("r2_type_deleted", True)),
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
    print("PASS: full-V4 m2 r2 source genus is zero or one")
    if args.tamper_selftest:
        count = tamper_selftest(data)
        print(f"PASS: {count}/{count} tamper mutations rejected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
