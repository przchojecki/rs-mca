#!/usr/bin/env python3
"""Verify the compact 433-1b cell-11 signed-pair route-cut certificate."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

import sympy as sp

from verify_kb_mca_v4_433_1b_cell11_compact_tower_v1 import (
    CERTIFICATE as TOWER_CERTIFICATE,
    verify as verify_tower_certificate,
)


P = 2_130_706_433
ROOT = Path(__file__).resolve().parents[2]
CERTIFICATE = (
    ROOT / "experimental/data/certificates/"
    "kb-mca-v4-433-1b-cell11-signed-pair-route-cut-v1/raw.json"
)
EXPECTED_RAW_SHA256 = "74c2a601542b12cf236aa60519e486a361fbe3326dca62455e460da6ce710e76"
EXPECTED_RESULTANT_SHA256 = "b9a65d00d6b6de580bb57464cd2c6eb1cf08a8596081fdb339ae547639caf0a3"
EXPECTED_RESIDUAL_SHA256 = "5eef057cab04f0b65e09f17e19df728491bdbee4aef2c8cfc6395ca0b196d6fe"
EXPECTED_WITNESS = {
    "r": 976_487_466,
    "t": 1_814_604_652,
    "b": 1_722_399_428,
    "c": 463_843_441,
    "w0": 58_144_935,
    "w1": 1_833_131_373,
    "N0": 1_242_524_170,
    "D0": 796_444_780,
    "raw_product": 0,
    "raw_square": 0,
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def evaluate(expression: str, values: dict[sp.Symbol, int]) -> int:
    return int(sp.sympify(expression).subs(values)) % P


def form(coefficients: list[int], value: int) -> int:
    return sum(coefficient * pow(value, index, P)
               for index, coefficient in enumerate(coefficients)) % P


def verify_witness(payload: dict) -> None:
    tower_payload = json.loads(TOWER_CERTIFICATE.read_text())
    verify_tower_certificate(tower_payload)
    raw_tower = tower_payload["exact_replay"]
    chart = next(row for row in raw_tower["charts"] if row["c_row"] == 5)
    witness = payload["deployed_fiber_scan"]["witness"]
    require(witness == EXPECTED_WITNESS, "witness values")
    t, r, c, b = sp.symbols("t r c b")
    values = {t: witness["t"], r: witness["r"],
              c: witness["c"], b: witness["b"]}
    for name in ("base", "b_relation", "c_relation"):
        require(evaluate(chart[name]["expression"], values) == 0,
                f"witness tower relation {name}")
    kernel = [evaluate(row["expression"], values)
              for row in raw_tower["kernel"]["kernel"]]
    require((kernel[6] + kernel[7]) % P == 0, "B1 opposition")
    a2, a0, k = kernel[:3], kernel[3:6], kernel[6]
    d0, d1 = form(a2, witness["w0"]), form(a2, witness["w1"])
    n0, n1 = form(a0, witness["w0"]), form(a0, witness["w1"])
    product = (n1*d0 + n0*d1) % P
    square = (
        k*k*witness["w0"]*pow(1-witness["w0"], 2, P)*d1*d1
        - k*k*witness["w1"]*pow(1-witness["w1"], 2, P)*d0*d0
        - 4*n0*d0*d1*d1
    ) % P
    require(n0 == witness["N0"] != 0, "witness N0")
    require(d0 == witness["D0"] != 0, "witness D0")
    require(product == witness["raw_product"] == 0, "signed product")
    require(square == witness["raw_square"] == 0, "signed square")
    guard_values = (
        witness["b"], witness["c"], witness["r"], witness["t"],
        witness["b"]-1, witness["b"]+1,
        witness["c"]-1, witness["c"]+1,
        witness["b"]-witness["c"], witness["b"]+witness["c"],
        witness["r"]**2-1, witness["r"]**2+1,
        witness["t"]**2-1, witness["t"]**2+1,
        witness["t"]**2-witness["r"]**2,
        witness["t"]**2+witness["r"]**2,
    )
    require(all(value % P for value in guard_values), "source guard")
    labels = {1, P-1, witness["r"]**2 % P,
              (-witness["r"]**2) % P, witness["t"]**2 % P}
    require(witness["w0"] not in labels and witness["w1"] not in labels,
            "new labels avoid source labels")
    require(witness["w0"] not in (0, witness["w1"])
            and witness["w1"] != 0, "new-label distinctness")


def verify(payload: dict) -> None:
    require(payload.get("schema") ==
            "kb-mca-v4-433-1b-cell11-signed-pair-guard-raw-v1", "schema")
    require(payload.get("field") == P, "field")
    require(payload.get("cell") == 11, "cell")
    require(payload.get("epsilon") == [-1, -1], "epsilon")
    require(payload.get("pivot") == 1, "pivot")
    require(payload.get("selected_c_row") == 5, "chart")
    require(payload.get("tower_checks") == {
        "base": True, "b_relation": True, "c_relation": True,
    }, "tower checks")
    require(payload.get("b1_opposite") is True, "B1 flag")
    require(payload["resultant"]["degree"] == 16, "resultant degree")
    require(payload["resultant"]["sha256"] == EXPECTED_RESULTANT_SHA256,
            "resultant hash")
    require(payload.get("cross_remainder_zero") is False,
            "false 1a transplant promoted")
    require(payload.get("guard_divisibility") == {
        "D0": 5, "N0": 1, "w0_minus_one": 0,
        "w0_minus_r2": 0, "w0_minus_t2": 1,
        "w0_plus_one": 1, "w0_plus_r2": 0,
    }, "guard divisibility")
    require(payload.get("exact_factorization") ==
            "resultant=N0*D0^5*(w0-t^2)*(w0+1)*Q2",
            "exact factorization statement")
    require(payload.get("exact_factorization_reconstructs") is True,
            "factorization reconstruction")
    require(payload["guard_residual"]["degree"] == 2, "residual degree")
    require(payload["guard_residual"]["sha256"] == EXPECTED_RESIDUAL_SHA256,
            "residual hash")
    require(payload.get("guard_residual_discriminant_norm_square") is True,
            "norm square")
    require(payload.get("guard_residual_discriminant_square") is False,
            "tower discriminant nonsquare")
    scan = payload.get("deployed_fiber_scan", {})
    require(scan.get("seed") == 43311 and scan.get("limit") == 256,
            "scan declaration")
    require(scan.get("attempted_r_values") == 4, "scan stopping index")
    require(scan.get("tower_points") == 5, "tower-point count")
    require(scan.get("residual_roots") == 2, "residual-root count")
    require(scan.get("guarded_residual_roots") == 1,
            "guarded residual-root count")
    verify_witness(payload)


def mutation_tests(payload: dict) -> int:
    mutations = []

    def add(name, mutate):
        value = copy.deepcopy(payload)
        mutate(value)
        mutations.append((name, value))

    add("field", lambda x: x.__setitem__("field", P-2))
    add("cell", lambda x: x.__setitem__("cell", 5))
    add("sign", lambda x: x.__setitem__("epsilon", [1, -1]))
    add("chart", lambda x: x.__setitem__("selected_c_row", 6))
    add("tower", lambda x: x["tower_checks"].__setitem__("base", False))
    add("resultant", lambda x: x["resultant"].__setitem__("sha256", "0"*64))
    add("cross", lambda x: x.__setitem__("cross_remainder_zero", True))
    add("divisor", lambda x: x["guard_divisibility"].__setitem__("D0", 4))
    add("factorization", lambda x: x.__setitem__("exact_factorization_reconstructs", False))
    add("residual", lambda x: x["guard_residual"].__setitem__("degree", 1))
    add("square", lambda x: x.__setitem__("guard_residual_discriminant_square", True))
    add("seed", lambda x: x["deployed_fiber_scan"].__setitem__("seed", 1))
    add("count", lambda x: x["deployed_fiber_scan"].__setitem__("tower_points", 4))
    add("w0", lambda x: x["deployed_fiber_scan"]["witness"].__setitem__("w0", 1))
    add("product", lambda x: x["deployed_fiber_scan"]["witness"].__setitem__("raw_product", 1))
    add("N0", lambda x: x["deployed_fiber_scan"]["witness"].__setitem__("N0", 0))
    for name, value in mutations:
        try:
            verify(value)
        except AssertionError:
            continue
        raise AssertionError(f"mutation survived: {name}")
    return len(mutations)


def main() -> None:
    raw = CERTIFICATE.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == EXPECTED_RAW_SHA256,
            "raw certificate hash")
    payload = json.loads(raw)
    verify(payload)
    count = mutation_tests(payload)
    print(json.dumps({
        "status": "OPEN_GAP",
        "raw_sha256": EXPECTED_RAW_SHA256,
        "mutations_rejected": count,
        "witness": EXPECTED_WITNESS,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
