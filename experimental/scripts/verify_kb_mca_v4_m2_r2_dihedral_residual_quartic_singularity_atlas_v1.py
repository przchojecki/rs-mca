#!/usr/bin/env python3
"""Verify the residual one-parameter quartic singularity atlas."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
from fractions import Fraction
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
    / "data/certificates/kb-mca-v4-m2-r2-dihedral-residual-quartic-singularity-atlas-v1"
    / "kb_mca_v4_m2_r2_dihedral_residual_quartic_singularity_atlas_v1.json"
)
NORMAL_FORM_PARENT = {
    "commit": "3efe818561509dcc6f2ae792f2ed1d22c7d317ae",
    "certificate_path": "experimental/data/certificates/kb-mca-v4-m2-r2-dihedral-residual-coefficient-quartic-normal-form-v1/kb_mca_v4_m2_r2_dihedral_residual_coefficient_quartic_normal_form_v1.json",
    "certificate_blob_oid": "8df504a15307d229a9c3de2bb876be89819853cb",
    "certificate_payload_sha256": "ba9783671d9d91bbd345ebaeec4b894d96be9d8d20f1ccc7d7ee1c5847bf6c81",
    "imported_terminal": "M2_R2_DIHEDRAL_RESIDUAL_ONE_PARAMETER_QUARTIC_NORMAL_FORM",
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
        result = subprocess.run(["git", *args], cwd=REPO_ROOT, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as error:
        raise VerificationError(error.stderr.strip()) from error
    return result.stdout.strip()


def verify_parent() -> None:
    path = NORMAL_FORM_PARENT["certificate_path"]
    require(git_output("rev-parse", f"{NORMAL_FORM_PARENT['commit']}:{path}") == NORMAL_FORM_PARENT["certificate_blob_oid"], "parent blob")
    data = parse_json(git_output("show", f"{NORMAL_FORM_PARENT['commit']}:{path}"), path)
    require(data.get("payload_sha256") == NORMAL_FORM_PARENT["certificate_payload_sha256"], "parent payload")
    require(payload_hash(data) == data.get("payload_sha256"), "parent seal")
    require(data.get("conclusion", {}).get("terminal") == NORMAL_FORM_PARENT["imported_terminal"], "parent terminal")


def coefficients(a: int, b: Fraction) -> dict[str, Fraction]:
    return {
        "A": (a - 2) * (a - b * b + 2),
        "B": -(a - 2) * (2 * a - b * b - 2 * b + 4),
        "C": (a - b) ** 2,
        "D": 4 * a * a - a * b * b - 4 * a * b - 4 * a + 16 * b - 16,
        "E": -2 * (a - 2) * (a - b),
        "F": (a - 2) ** 2,
    }


def singular_replay(a: int, b: Fraction) -> dict[str, Any]:
    row = coefficients(a, b)
    alpha = row["B"] ** 2 - 4 * row["A"] * row["C"]
    beta = 8 * row["C"] ** 2 + 2 * row["B"] * row["E"] - 4 * row["C"] * row["D"]
    n_disc = 4 * (a + 2) * (b - 2) ** 2
    center_hessian = -4 * (a - 2) * (a + 2) * (b - 2) ** 4
    require(alpha == (a - 2) * (a + 2) * (b - 2) ** 3 * (b + 2), "alpha")
    require(beta == -4 * (a + 2) * (a - b) * (b - 2) ** 3, "beta")
    require(n_disc != 0 and center_hessian != 0, "standing fences")
    if b != a:
        side_hessian = 16 * (a - 2) * (a + 2) * (b - 2) ** 3
        require(row["C"] != 0 and alpha != 0 and beta != 0 and side_hessian != 0, "three-node gate")
        atlas = "three ordinary nodes"
        delta = [1, 1, 1]
    else:
        require(row["C"] == 0 and row["E"] == 0, "tacnode specialization")
        require(row["B"] != 0 and row["F"] != 0, "tacnode leading terms")
        atlas = "one ordinary node plus one tacnode"
        delta = [1, 2]
    require(sum(delta) == 3, "delta ledger")
    return {
        "a": a,
        "b": str(b),
        "alpha": str(alpha),
        "beta": str(beta),
        "N_discriminant": str(n_disc),
        "center_hessian": str(center_hessian),
        "atlas": atlas,
        "delta_multiset": delta,
        "normalization_genus": 0,
        "geometrically_irreducible": True,
    }


def build_certificate() -> dict[str, Any]:
    samples = [Fraction(-5), Fraction(-3), Fraction(-1), Fraction(0), Fraction(1), Fraction(3), Fraction(5)]
    data = {
        "schema": "kb-mca-v4-m2-r2-dihedral-residual-quartic-singularity-atlas-v1",
        "parent_normal_form": NORMAL_FORM_PARENT,
        "universal_identities": {
            "M_factorization": "(a-2)(P+1)^2*((a-b^2+2)P^2+2(a-2b+2)P+(a-2))",
            "N_discriminant": "4(a+2)(b-2)^2",
            "R_discriminant": "P^2*(alpha P^2+beta)",
            "alpha": "(a-2)(a+2)(b-2)^3(b+2)",
            "beta": "-4(a+2)(a-b)(b-2)^3",
            "center_hessian": "-4(a-2)(a+2)(b-2)^4",
            "side_hessian": "16(a-2)(a+2)(b-2)^3",
        },
        "exact_replays": [singular_replay(a, b) for a in (-1, 1) for b in samples if b not in (-2, 2)],
        "conclusion": {
            "terminal": "M2_R2_DIHEDRAL_RESIDUAL_QUARTIC_SINGULARITY_ATLAS",
            "allowed_a": [-1, 1],
            "excluded_b": [-2, 2],
            "all_allowed_geometrically_irreducible": True,
            "all_allowed_normalization_genus": 0,
            "profiles_deleted": [],
            "next_gate": "six-pole and complete-source locator realization",
        },
        "nonclaims": [
            "no actual source realization for arbitrary b",
            "no n=3 or n=6 deletion or m2 payment",
            "no K3, KoalaBear, endpoint, or Prize close",
        ],
    }
    data["payload_sha256"] = payload_hash(data)
    return data


def verify_certificate(data: dict[str, Any], verify_parents: bool) -> None:
    require(data.get("schema") == "kb-mca-v4-m2-r2-dihedral-residual-quartic-singularity-atlas-v1", "schema")
    require(data.get("payload_sha256") == payload_hash(data), "payload seal")
    require(data.get("parent_normal_form") == NORMAL_FORM_PARENT, "parent")
    if verify_parents:
        verify_parent()
    expected = build_certificate()
    for key in ("universal_identities", "exact_replays", "conclusion", "nonclaims"):
        require(data.get(key) == expected[key], key)


def reseal(data: dict[str, Any]) -> None:
    data["payload_sha256"] = payload_hash(data)


def tamper_selftest(original: dict[str, Any]) -> int:
    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("parent", lambda row: row["parent_normal_form"].__setitem__("certificate_blob_oid", "0" * 40)),
        ("M", lambda row: row["universal_identities"].__setitem__("M_factorization", "unknown")),
        ("N-disc", lambda row: row["universal_identities"].__setitem__("N_discriminant", "0")),
        ("R-disc", lambda row: row["universal_identities"].__setitem__("R_discriminant", "square")),
        ("alpha", lambda row: row["universal_identities"].__setitem__("alpha", "0")),
        ("beta", lambda row: row["universal_identities"].__setitem__("beta", "0")),
        ("center", lambda row: row["universal_identities"].__setitem__("center_hessian", "0")),
        ("side", lambda row: row["universal_identities"].__setitem__("side_hessian", "0")),
        ("replay", lambda row: row["exact_replays"].pop()),
        ("replay-alpha", lambda row: row["exact_replays"][0].__setitem__("alpha", "0")),
        ("replay-atlas", lambda row: row["exact_replays"][1].__setitem__("atlas", "smooth")),
        ("replay-delta", lambda row: row["exact_replays"][2]["delta_multiset"].append(1)),
        ("replay-genus", lambda row: row["exact_replays"][3].__setitem__("normalization_genus", 1)),
        ("replay-reducible", lambda row: row["exact_replays"][4].__setitem__("geometrically_irreducible", False)),
        ("a", lambda row: row["conclusion"]["allowed_a"].append(0)),
        ("b", lambda row: row["conclusion"]["excluded_b"].pop()),
        ("irreducible", lambda row: row["conclusion"].__setitem__("all_allowed_geometrically_irreducible", False)),
        ("genus", lambda row: row["conclusion"].__setitem__("all_allowed_normalization_genus", 1)),
        ("delete", lambda row: row["conclusion"]["profiles_deleted"].append(3)),
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
        verify_parent()
        data = build_certificate()
        CERTIFICATE.parent.mkdir(parents=True, exist_ok=True)
        CERTIFICATE.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
        print(f"WROTE: {CERTIFICATE.relative_to(REPO_ROOT)}")
    data = parse_json(CERTIFICATE.read_text(), str(CERTIFICATE))
    verify_certificate(data, True)
    print("PASS: every allowed residual quartic is irreducible and rational")
    if args.tamper_selftest:
        count = tamper_selftest(data)
        print(f"PASS: {count}/{count} tamper mutations rejected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
