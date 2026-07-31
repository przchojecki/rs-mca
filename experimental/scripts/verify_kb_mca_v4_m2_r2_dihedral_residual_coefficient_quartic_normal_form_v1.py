#!/usr/bin/env python3
"""Verify the residual one-parameter coefficient-quartic normal form."""

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
    / "data/certificates/kb-mca-v4-m2-r2-dihedral-residual-coefficient-quartic-normal-form-v1"
    / "kb_mca_v4_m2_r2_dihedral_residual_coefficient_quartic_normal_form_v1.json"
)
STAR_PARENT = {
    "commit": "06a0dcb152687db4017484b215ed851bae52f1f2",
    "certificate_path": "experimental/data/certificates/kb-mca-v4-m2-r2-dihedral-residual-star-graph-rigidity-v1/kb_mca_v4_m2_r2_dihedral_residual_star_graph_rigidity_v1.json",
    "certificate_blob_oid": "c842c89b0d4978a12d4ede3d12fc040de6d11741",
    "certificate_payload_sha256": "63f6387bba81e51e0a49f409645e9493b3f128f6ab9d119be2dcc64da766b1d4",
    "imported_terminal": "M2_R2_DIHEDRAL_RESIDUAL_STAR_GRAPH_RIGIDITY",
}
GENUS_PARENT = {
    "commit": "f6bc4a2b2a6a5b3bba98f24a520c67ca3373dbbb",
    "certificate_path": "experimental/data/certificates/kb-mca-v4-m2-r2-full-v4-source-genus-drop-v1/kb_mca_v4_m2_r2_full_v4_source_genus_drop_v1.json",
    "certificate_blob_oid": "83e82b826ddfa2f5377e99f439be5f00900507c6",
    "certificate_payload_sha256": "9a2ea090568600356f27f3174aee6d08414217b26dbb8f7922931c64a151122f",
    "imported_terminal": "M2_R2_SOURCE_GENUS_ZERO_OR_ONE",
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


def verify_parent(parent: dict[str, str]) -> None:
    path = parent["certificate_path"]
    require(git_output("rev-parse", f"{parent['commit']}:{path}") == parent["certificate_blob_oid"], f"parent blob: {path}")
    data = parse_json(git_output("show", f"{parent['commit']}:{path}"), path)
    require(data.get("payload_sha256") == parent["certificate_payload_sha256"], f"parent payload: {path}")
    require(payload_hash(data) == data.get("payload_sha256"), f"parent seal: {path}")
    require(data.get("conclusion", {}).get("terminal") == parent["imported_terminal"], f"parent terminal: {path}")


def coefficients(a: int, b: Fraction) -> dict[str, Fraction]:
    return {
        "A": (a - 2) * (a - b * b + 2),
        "B": -(a - 2) * (2 * a - b * b - 2 * b + 4),
        "C": (a - b) ** 2,
        "D": 4 * a * a - a * b * b - 4 * a * b - 4 * a + 16 * b - 16,
        "E": -2 * (a - 2) * (a - b),
        "F": (a - 2) ** 2,
    }


def fraction_row(row: dict[str, Fraction]) -> dict[str, str]:
    return {key: str(value) for key, value in row.items()}


def old_coordinate(new: Fraction, b: Fraction) -> Fraction:
    return (b * new - 2) / (new - 1)


def sibling_old(a: int, x: Fraction, y: Fraction) -> Fraction:
    return x * x + y * y - a * x * y + a * a - 4


def sibling_new(row: dict[str, Fraction], x: Fraction, y: Fraction) -> Fraction:
    sigma = x + y
    pi = x * y
    return row["A"] * pi**2 + row["B"] * sigma * pi + row["C"] * (sigma**2 - 2 * pi) + row["D"] * pi + row["E"] * sigma + row["F"]


def quartic(row: dict[str, Fraction], s_value: Fraction, p_value: Fraction) -> Fraction:
    return (
        row["A"] * p_value**4
        + row["B"] * s_value**2 * p_value**2
        - 2 * row["B"] * p_value**3
        + row["C"] * s_value**4
        - 4 * row["C"] * s_value**2 * p_value
        + (2 * row["C"] + row["D"]) * p_value**2
        + row["E"] * s_value**2
        - 2 * row["E"] * p_value
        + row["F"]
    )


def replay(a: int, b: Fraction) -> dict[str, Any]:
    row = coefficients(a, b)
    for x, y in [(Fraction(0), Fraction(3)), (Fraction(-2), Fraction(4)), (Fraction(5), Fraction(-3))]:
        cleared = (x - 1) ** 2 * (y - 1) ** 2 * sibling_old(a, old_coordinate(x, b), old_coordinate(y, b))
        require(cleared == sibling_new(row, x, y), "target transport")
    for t, u in [(Fraction(2), Fraction(3)), (Fraction(-1), Fraction(4))]:
        require(quartic(row, t + u, t * u) == sibling_new(row, t * t, u * u), "quartic pullback")
    alpha = row["B"] ** 2 - 4 * row["A"] * row["C"]
    beta = 8 * row["C"] ** 2 + 2 * row["B"] * row["E"] - 4 * row["C"] * row["D"]
    gamma = row["E"] ** 2 - 4 * row["C"] * row["F"]
    require(alpha == (a - 2) * (a + 2) * (b - 2) ** 3 * (b + 2), "alpha invariant")
    require(beta == -4 * (a + 2) * (a - b) * (b - 2) ** 3, "beta invariant")
    require(gamma == 0, "aligned branch invariant")
    return {
        "a": a,
        "b": str(b),
        "coefficients": fraction_row(row),
        "alpha": str(alpha),
        "beta": str(beta),
        "gamma": str(gamma),
    }


def build_certificate() -> dict[str, Any]:
    data = {
        "schema": "kb-mca-v4-m2-r2-dihedral-residual-coefficient-quartic-normal-form-v1",
        "parent_star_graph": STAR_PARENT,
        "parent_source_genus": GENUS_PARENT,
        "canonical_quartic": {
            "sibling_equation": "A*pi^2+B*sigma*pi+C*(sigma^2-2*pi)+D*pi+E*sigma+F",
            "substitution": {"sigma": "S^2-2P", "pi": "P^2"},
            "equation": "A*P^4+B*S^2*P^2-2B*P^3+C*S^4-4C*S^2*P+(2C+D)*P^2+E*S^2-2E*P+F",
            "actual_image_degree": 4,
        },
        "dihedral_rows": {"n3": {"n": 3, "a": -1}, "n6": {"n": 6, "a": 1}},
        "branch_gate": {
            "quadratic_pullback_branch_places": 2,
            "Y_branch_values": ["-2", "2"],
            "aligned_h_branch_values": 1,
            "normalization": "aligned value 2; other value b not in {-2,2}",
            "target_map": "m(x)=(x-2)/(x-b)",
        },
        "coefficient_formulas": {
            "A": "(a-2)(a-b^2+2)",
            "B": "-(a-2)(2a-b^2-2b+4)",
            "C": "(a-b)^2",
            "D": "4a^2-a*b^2-4a*b-4a+16b-16",
            "E": "-2(a-2)(a-b)",
            "F": "(a-2)^2",
        },
        "exact_replays": [replay(a, b) for a in (-1, 1) for b in (Fraction(-3), Fraction(-1), Fraction(0), Fraction(1), Fraction(3))],
        "conclusion": {
            "terminal": "M2_R2_DIHEDRAL_RESIDUAL_ONE_PARAMETER_QUARTIC_NORMAL_FORM",
            "surviving_factor_degrees": [3, 6],
            "continuous_parameters_per_degree": 1,
            "profiles_deleted": [],
            "next_gate": "factor exceptional b and impose six-pole/source-locator equations",
        },
        "nonclaims": [
            "no irreducibility or source realization for arbitrary b",
            "no n=3 or n=6 deletion or m2 payment",
            "no K3, KoalaBear, endpoint, or Prize close",
        ],
    }
    data["payload_sha256"] = payload_hash(data)
    return data


def verify_certificate(data: dict[str, Any], verify_parents: bool) -> None:
    require(data.get("schema") == "kb-mca-v4-m2-r2-dihedral-residual-coefficient-quartic-normal-form-v1", "schema")
    require(data.get("payload_sha256") == payload_hash(data), "payload seal")
    require(data.get("parent_star_graph") == STAR_PARENT, "star parent")
    require(data.get("parent_source_genus") == GENUS_PARENT, "genus parent")
    if verify_parents:
        verify_parent(STAR_PARENT)
        verify_parent(GENUS_PARENT)
    expected = build_certificate()
    for key in ("canonical_quartic", "dihedral_rows", "branch_gate", "coefficient_formulas", "exact_replays", "conclusion", "nonclaims"):
        require(data.get(key) == expected[key], key)


def reseal(data: dict[str, Any]) -> None:
    data["payload_sha256"] = payload_hash(data)


def tamper_selftest(original: dict[str, Any]) -> int:
    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("star-parent", lambda row: row["parent_star_graph"].__setitem__("certificate_blob_oid", "0" * 40)),
        ("genus-parent", lambda row: row["parent_source_genus"].__setitem__("certificate_payload_sha256", "0" * 64)),
        ("sigma", lambda row: row["canonical_quartic"]["substitution"].__setitem__("sigma", "S^2+2P")),
        ("pi", lambda row: row["canonical_quartic"]["substitution"].__setitem__("pi", "P")),
        ("equation", lambda row: row["canonical_quartic"].__setitem__("equation", "arbitrary quartic")),
        ("degree", lambda row: row["canonical_quartic"].__setitem__("actual_image_degree", 3)),
        ("a3", lambda row: row["dihedral_rows"]["n3"].__setitem__("a", 1)),
        ("a6", lambda row: row["dihedral_rows"]["n6"].__setitem__("a", -1)),
        ("branch-count", lambda row: row["branch_gate"].__setitem__("quadratic_pullback_branch_places", 4)),
        ("aligned", lambda row: row["branch_gate"].__setitem__("aligned_h_branch_values", 2)),
        ("target", lambda row: row["branch_gate"].__setitem__("target_map", "m(x)=x")),
        ("A", lambda row: row["coefficient_formulas"].__setitem__("A", "0")),
        ("D", lambda row: row["coefficient_formulas"].__setitem__("D", "unknown")),
        ("replay", lambda row: row["exact_replays"].pop()),
        ("replay-coefficient", lambda row: row["exact_replays"][0]["coefficients"].__setitem__("A", "0")),
        ("gamma", lambda row: row["exact_replays"][1].__setitem__("gamma", "1")),
        ("parameters", lambda row: row["conclusion"].__setitem__("continuous_parameters_per_degree", 0)),
        ("survivors", lambda row: row["conclusion"]["surviving_factor_degrees"].append(2)),
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
        verify_parent(STAR_PARENT)
        verify_parent(GENUS_PARENT)
        data = build_certificate()
        CERTIFICATE.parent.mkdir(parents=True, exist_ok=True)
        CERTIFICATE.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
        print(f"WROTE: {CERTIFICATE.relative_to(REPO_ROOT)}")
    data = parse_json(CERTIFICATE.read_text(), str(CERTIFICATE))
    verify_certificate(data, True)
    print("PASS: residual n=3,6 coefficient quartics reduce to Q_(a,b)")
    if args.tamper_selftest:
        count = tamper_selftest(data)
        print(f"PASS: {count}/{count} tamper mutations rejected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
