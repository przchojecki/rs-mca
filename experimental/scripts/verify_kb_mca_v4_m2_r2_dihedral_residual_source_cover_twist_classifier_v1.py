#!/usr/bin/env python3
"""Verify the residual source-cover twist classifier."""

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
    / "data/certificates/kb-mca-v4-m2-r2-dihedral-residual-source-cover-twist-classifier-v1"
    / "kb_mca_v4_m2_r2_dihedral_residual_source_cover_twist_classifier_v1.json"
)
ATLAS_PARENT = {
    "commit": "4cdfa41a1de1360155e3d350a5fe3ec99e9fe94b",
    "certificate_path": "experimental/data/certificates/kb-mca-v4-m2-r2-dihedral-residual-quartic-singularity-atlas-v1/kb_mca_v4_m2_r2_dihedral_residual_quartic_singularity_atlas_v1.json",
    "certificate_blob_oid": "1355c5acace3f031194abf67b227d657132c12b7",
    "certificate_payload_sha256": "e402c17bf8f4757f5b534f3b1a9da5faebafe6ac60956a4849f27f66202b96de",
    "imported_terminal": "M2_R2_DIHEDRAL_RESIDUAL_QUARTIC_SINGULARITY_ATLAS",
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
    path = ATLAS_PARENT["certificate_path"]
    require(git_output("rev-parse", f"{ATLAS_PARENT['commit']}:{path}") == ATLAS_PARENT["certificate_blob_oid"], "parent blob")
    data = parse_json(git_output("show", f"{ATLAS_PARENT['commit']}:{path}"), path)
    require(data.get("payload_sha256") == ATLAS_PARENT["certificate_payload_sha256"], "parent payload")
    require(payload_hash(data) == data.get("payload_sha256"), "parent seal")
    require(data.get("conclusion", {}).get("terminal") == ATLAS_PARENT["imported_terminal"], "parent terminal")


def q_value_mod_d_relation(a: int, b: Fraction, z: Fraction) -> tuple[Fraction, Fraction]:
    """Return Q_b(z) as c0+c1*d after reducing d^2=a+2."""
    return z * z + b * b + a - 2, -b * z


def square_b_plus_cd_mod_d_relation(a: int, b: Fraction, c: int) -> tuple[Fraction, Fraction]:
    """Return (b+c*d)^2 as c0+c1*d after reducing d^2=a+2."""
    return b * b + c * c * (a + 2), 2 * b * c


def replay(a: int, b: Fraction) -> dict[str, Any]:
    require(a in (-1, 1), "a")
    require(b not in (Fraction(-2), Fraction(2)), "allowed b")
    plus = q_value_mod_d_relation(a, b, Fraction(2))
    minus = q_value_mod_d_relation(a, b, Fraction(-2))
    require(plus == square_b_plus_cd_mod_d_relation(a, b, -1), "Q(2)")
    require(minus == square_b_plus_cd_mod_d_relation(a, b, 1), "Q(-2)")
    discriminant = (a - 2) * (b * b - 4)
    require(discriminant != 0, "Q squarefree")
    return {
        "a": a,
        "b": str(b),
        "d_square": a + 2,
        "Q_at_2_basis_1_d": [str(value) for value in plus],
        "Q_at_minus_2_basis_1_d": [str(value) for value in minus],
        "Q_discriminant": str(discriminant),
    }


def build_certificate() -> dict[str, Any]:
    data = {
        "schema": "kb-mca-v4-m2-r2-dihedral-residual-source-cover-twist-classifier-v1",
        "parent_singularity_atlas": ATLAS_PARENT,
        "square_class": {
            "d_relation": "d^2=a+2",
            "coefficient_cover": "P^2=(Z0-d)^2/Q_b(Z0)",
            "Q_b": "z^2-b*d*z+b^2+d^2-4",
            "endpoint_cover": "W^2=m(ell(Z0))",
            "forced_preimages": "ell^-1({2,b})=roots(Q_b)",
            "Q_at_2": "(b-d)^2",
            "Q_at_minus_2": "(b+d)^2",
        },
        "genus_classifier": {
            "genus_zero": "b^2=a+2",
            "genus_one": "b^2!=a+2",
            "n3_genus_zero": "b^2=1",
            "n6_genus_zero": "b^2=3",
        },
        "exact_replays": [
            replay(-1, Fraction(b))
            for b in [-3, -1, 0, 1, 3]
        ] + [
            replay(1, Fraction(b))
            for b in [-3, -1, 0, 1, 3]
        ],
        "conclusion": {
            "terminal": "M2_R2_DIHEDRAL_RESIDUAL_SOURCE_COVER_TWIST_CLASSIFIER",
            "surviving_factor_degrees": [3, 6],
            "profiles_deleted": [],
            "next_gate": "common degree-30 function plus six-pole/source-locator realization",
        },
        "nonclaims": [
            "no existence in either genus regime",
            "no n=3 or n=6 deletion or m2 payment",
            "no K3, KoalaBear, endpoint, or Prize close",
        ],
    }
    data["payload_sha256"] = payload_hash(data)
    return data


def verify_certificate(data: dict[str, Any], verify_parents: bool) -> None:
    require(data.get("schema") == "kb-mca-v4-m2-r2-dihedral-residual-source-cover-twist-classifier-v1", "schema")
    require(data.get("payload_sha256") == payload_hash(data), "payload seal")
    require(data.get("parent_singularity_atlas") == ATLAS_PARENT, "parent")
    if verify_parents:
        verify_parent()
    expected = build_certificate()
    for key in ("square_class", "genus_classifier", "exact_replays", "conclusion", "nonclaims"):
        require(data.get(key) == expected[key], key)


def reseal(data: dict[str, Any]) -> None:
    data["payload_sha256"] = payload_hash(data)


def tamper_selftest(original: dict[str, Any]) -> int:
    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("parent", lambda row: row["parent_singularity_atlas"].__setitem__("certificate_blob_oid", "0" * 40)),
        ("d", lambda row: row["square_class"].__setitem__("d_relation", "d^2=a-2")),
        ("coefficient-cover", lambda row: row["square_class"].__setitem__("coefficient_cover", "unknown")),
        ("Q", lambda row: row["square_class"].__setitem__("Q_b", "z^2")),
        ("endpoint-cover", lambda row: row["square_class"].__setitem__("endpoint_cover", "W^2=1")),
        ("preimages", lambda row: row["square_class"].__setitem__("forced_preimages", "arbitrary")),
        ("plus", lambda row: row["square_class"].__setitem__("Q_at_2", "0")),
        ("minus", lambda row: row["square_class"].__setitem__("Q_at_minus_2", "0")),
        ("g0", lambda row: row["genus_classifier"].__setitem__("genus_zero", "all b")),
        ("g1", lambda row: row["genus_classifier"].__setitem__("genus_one", "none")),
        ("n3", lambda row: row["genus_classifier"].__setitem__("n3_genus_zero", "b=0")),
        ("n6", lambda row: row["genus_classifier"].__setitem__("n6_genus_zero", "b=0")),
        ("replay", lambda row: row["exact_replays"].pop()),
        ("replay-Q", lambda row: row["exact_replays"][0].__setitem__("Q_at_2", "0")),
        ("replay-disc", lambda row: row["exact_replays"][1].__setitem__("Q_discriminant", "0")),
        ("survivors", lambda row: row["conclusion"]["surviving_factor_degrees"].append(2)),
        ("delete", lambda row: row["conclusion"]["profiles_deleted"].append(3)),
        ("next", lambda row: row["conclusion"].__setitem__("next_gate", "closed")),
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
    print("PASS: residual source-cover twist and genus regimes are exact")
    if args.tamper_selftest:
        count = tamper_selftest(data)
        print(f"PASS: {count}/{count} tamper mutations rejected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
