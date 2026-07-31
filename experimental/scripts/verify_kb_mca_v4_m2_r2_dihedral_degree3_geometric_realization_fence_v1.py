#!/usr/bin/env python3
"""Verify the KoalaBear degree-three geometric realization fence."""

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
    / "data/certificates/kb-mca-v4-m2-r2-dihedral-degree3-geometric-realization-fence-v1"
    / "kb_mca_v4_m2_r2_dihedral_degree3_geometric_realization_fence_v1.json"
)
DEGREE6_PARENT = {
    "commit": "5bcb2b2bd0158912cb7319ef386ca2523db5436d",
    "certificate_path": "experimental/data/certificates/kb-mca-v4-m2-r2-dihedral-degree6-common-pole-exclusion-v1/kb_mca_v4_m2_r2_dihedral_degree6_common_pole_exclusion_v1.json",
    "certificate_blob_oid": "b6c821cdf89c0e82461ff53216e7a83ac8087ff5",
    "certificate_payload_sha256": "224fbbaf75c0aa830c7fab8e6024a51d3454d7ce3a6260184041983806f1e3fd",
    "imported_terminal": "M2_R2_DIHEDRAL_DEGREE6_COMMON_POLE_EMPTY",
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
    path = DEGREE6_PARENT["certificate_path"]
    require(git_output("rev-parse", f"{DEGREE6_PARENT['commit']}:{path}") == DEGREE6_PARENT["certificate_blob_oid"], "parent blob")
    data = parse_json(git_output("show", f"{DEGREE6_PARENT['commit']}:{path}"), path)
    require(data.get("payload_sha256") == DEGREE6_PARENT["certificate_payload_sha256"], "parent payload")
    require(payload_hash(data) == data.get("payload_sha256"), "parent seal")
    require(data.get("conclusion", {}).get("terminal") == DEGREE6_PARENT["imported_terminal"], "parent terminal")


def h(value: Fraction) -> Fraction:
    return (value * value + 2) / (1 - value * value)


def psi(value: Fraction) -> Fraction:
    return Fraction(2, value * value + 1)


def d3(value: Fraction) -> Fraction:
    return value**3 - 3 * value


def component(t: Fraction, x: Fraction) -> Fraction:
    u = x * x + 1
    return 2 * u * t * t - 2 * x * (x * x + 3) * t + u * u


def exact_replay() -> dict[str, Any]:
    t_values = [Fraction(value) for value in range(-7, 8) if value not in (-1, 1)]
    x_values = [Fraction(value) for value in range(-8, 9) if value not in (-1, 1)]
    checks = 0
    for t in t_values:
        for x in x_values:
            y = h(t)
            z = h(psi(x))
            c = y * y + y * z + z * z - 3
            denominator = (t * t - 1) ** 2 * (x * x - 1) ** 2 * (x * x + 3) ** 2
            require(c == Fraction(9) * component(t, x) * component(t, -x) / denominator, "pullback")
            require(d3(y) - d3(z) == (y - z) * c, "D3 relation")
            checks += 2
    require(len(t_values) > 8 and len(x_values) > 12, "interpolation coverage")

    quartic_checks = 0
    for x in [Fraction(value, 2) for value in range(-11, 12)]:
        u = x * x + 1
        p = u / 2
        s = x * (x * x + 3) / u
        require(9 * (s * s * p * p - 2 * p**3 - 3 * p * p + 1) == 0, "quartic")
        require(4 * x * x * (x * x + 3) ** 2 - 8 * u**3 == -4 * (x * x - 1) ** 2 * (x * x + 2), "discriminant")
        quartic_checks += 2
    require(d3(h(Fraction(0))) == 2, "positive branch")
    require(d3(h(Fraction(2))) == -2, "negative branch")
    return {
        "pullback_and_D3_checks": checks,
        "quartic_and_discriminant_checks": quartic_checks,
        "t_grid_size": len(t_values),
        "x_grid_size": len(x_values),
        "branch_values": [-2, 2],
    }


def build_certificate() -> dict[str, Any]:
    data = {
        "schema": "kb-mca-v4-m2-r2-dihedral-degree3-geometric-realization-fence-v1",
        "parent_degree6_exclusion": DEGREE6_PARENT,
        "specialization": {"a": -1, "b": -1, "d": -1, "ell": "identity", "source_genus": 0},
        "maps": {
            "D3": "y^3-3*y",
            "h": "(t^2+2)/(1-t^2)",
            "psi": "2/(x^2+1)",
            "H": "2*(x^2+1)*t^2-2*x*(x^2+3)*t+(x^2+1)^2",
            "coefficient_quartic": "9*(S^2*P^2-2*P^3-3*P^2+1)",
            "source_discriminant": "-4*(x^2-1)^2*(x^2+2)",
        },
        "complete_source": {
            "outer_poles": "two distinct values outside {-2,2}, each of order five for G",
            "endpoint_poles": 6,
            "source_labels": 12,
            "source_degree": 24,
            "row_divisibility": "H(alpha,x) divides B(x) for every source label alpha",
            "saturation": "sum_alpha div(H(alpha,x))=2*div(B)",
            "star_graph": "two disjoint K_(2,2,2)",
        },
        "exact_replay": exact_replay(),
        "conclusion": {
            "terminal": "M2_R2_DIHEDRAL_DEGREE3_GEOMETRIC_REALIZATION_FENCE",
            "surviving_factor_degrees": [3],
            "next_gate": "fixed active endpoint pencil compatibility or chronology-valid recurrent owner",
        },
        "nonclaims": [
            "no fixed KoalaBear endpoint-record realization",
            "no owner or payment",
            "no m2 type, K3, KoalaBear, endpoint, or Prize close",
        ],
    }
    data["payload_sha256"] = payload_hash(data)
    return data


def verify_certificate(data: dict[str, Any], verify_parents: bool) -> None:
    require(data.get("schema") == "kb-mca-v4-m2-r2-dihedral-degree3-geometric-realization-fence-v1", "schema")
    require(data.get("payload_sha256") == payload_hash(data), "payload seal")
    require(data.get("parent_degree6_exclusion") == DEGREE6_PARENT, "parent")
    if verify_parents:
        verify_parent()
    expected = build_certificate()
    for key in ("specialization", "maps", "complete_source", "exact_replay", "conclusion", "nonclaims"):
        require(data.get(key) == expected[key], key)


def reseal(data: dict[str, Any]) -> None:
    data["payload_sha256"] = payload_hash(data)


def tamper_selftest(original: dict[str, Any]) -> int:
    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("parent", lambda row: row["parent_degree6_exclusion"].__setitem__("certificate_blob_oid", "0" * 40)),
        ("a", lambda row: row["specialization"].__setitem__("a", 1)),
        ("b", lambda row: row["specialization"].__setitem__("b", 0)),
        ("d", lambda row: row["specialization"].__setitem__("d", 1)),
        ("ell", lambda row: row["specialization"].__setitem__("ell", "unknown")),
        ("genus", lambda row: row["specialization"].__setitem__("source_genus", 1)),
        ("D3", lambda row: row["maps"].__setitem__("D3", "y^3")),
        ("h", lambda row: row["maps"].__setitem__("h", "t")),
        ("psi", lambda row: row["maps"].__setitem__("psi", "x")),
        ("H", lambda row: row["maps"].__setitem__("H", "0")),
        ("quartic", lambda row: row["maps"].__setitem__("coefficient_quartic", "0")),
        ("disc", lambda row: row["maps"].__setitem__("source_discriminant", "square")),
        ("poles", lambda row: row["complete_source"].__setitem__("endpoint_poles", 5)),
        ("labels", lambda row: row["complete_source"].__setitem__("source_labels", 10)),
        ("degree", lambda row: row["complete_source"].__setitem__("source_degree", 20)),
        ("divisibility", lambda row: row["complete_source"].__setitem__("row_divisibility", "unknown")),
        ("saturation", lambda row: row["complete_source"].__setitem__("saturation", "unknown")),
        ("graph", lambda row: row["complete_source"].__setitem__("star_graph", "unknown")),
        ("replay", lambda row: row["exact_replay"].__setitem__("pullback_and_D3_checks", 0)),
        ("terminal", lambda row: row["conclusion"].__setitem__("terminal", "CLOSED")),
        ("survivor", lambda row: row["conclusion"]["surviving_factor_degrees"].clear()),
        ("next", lambda row: row["conclusion"].__setitem__("next_gate", "none")),
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
    print("PASS: residual degree-three abstract geometry is realizable")
    if args.tamper_selftest:
        count = tamper_selftest(data)
        print(f"PASS: {count}/{count} tamper mutations rejected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
