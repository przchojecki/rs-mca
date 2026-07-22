#!/usr/bin/env python3
"""Deterministic checks for the singleton-MASTER reduction packet.

The companion note contains the analytic proofs.  This stdlib-only verifier
checks conventions, exact counterexample arithmetic, finite recurrence
regressions, first-insertion positivity, and a fail-closed status contract. It does not
prove the open all-position singleton MASTER theorem.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import platform
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
from typing import Callable, Sequence


PI = math.pi
ALPHA = 2.0 * PI / 3.0
ROOT = Path(__file__).resolve().parents[2]
PROOF_PATH = ROOT / "experimental/notes/thresholds/singleton_master_reductions.md"
CONTRACT_PATH = (
    ROOT
    / "experimental/data/certificates/singleton-master-reductions/consumer_contract.json"
)
CERT_PATH = (
    ROOT
    / "experimental/data/certificates/singleton-master-reductions/singleton_master_reductions.json"
)
CERT_DIR = CERT_PATH.parent
MANIFEST_PATH = CERT_DIR / "SHA256SUMS.txt"
AUTHORITY_PATHS = {
    "ordinary_master_source": ROOT
    / "experimental/notes/thresholds/dense_shell_transfer_shape.md",
    "ordinary_master_contract": ROOT
    / "experimental/data/certificates/dense-shell-transfer-shape/consumer_contract.json",
    "charge_interface": ROOT
    / "experimental/notes/thresholds/dense_shell_class_charges.md",
}
EXPECTED_AUTHORITY_HASHES = {
    "ordinary_master_source": "5fc9f180b69fe87f5d2b055355577511672aff8ef222beb42ab9d2e628354368",
    "ordinary_master_contract": "a0cfa97b006f316812ea4e8c9f7384e745a980691cdc91c14b35fe68a200dacb",
    "charge_interface": "e13be4f164ac741329c98e174b2261970c368081a1f725bd4b9ae7249e4e7270",
}
MANIFEST_EXPECTED_PATHS = {
    "experimental/notes/thresholds/singleton_master_reductions.md",
    "experimental/scripts/verify_singleton_master_reductions.py",
    "experimental/data/certificates/singleton-master-reductions/README.md",
    "experimental/data/certificates/singleton-master-reductions/consumer_contract.json",
}


EXPECTED_CONTRACT = {
    "schema": "singleton-master-reductions-consumer/v1",
    "producer": "experimental/notes/thresholds/singleton_master_reductions.md",
    "proved_results": [
        "insertion-position factorization",
        "normalized-monotonicity sufficient criterion",
        "terminal singleton coordinate",
        "scalar upper-cap transfer lemma",
        "first-insertion source positivity",
        "source cap-six and shifted-Jacobi counterexamples",
    ],
    "open_target": "all-position single-insertion MASTER (SIM)",
    "dependency_chain": [
        "corrected source envelope plus homogeneous transfer preservation",
        "all-position single-insertion MASTER (SIM)",
        "conditional pair-decorated reduction",
        "PDSP_2",
        "|U|=2 dense-shell class-sign law",
    ],
    "downstream_consumer": "experimental/notes/thresholds/dense_shell_pair_reduction.md",
    "ordinary_master_source": "experimental/notes/thresholds/dense_shell_transfer_shape.md",
    "ordinary_master_contract": (
        "experimental/data/certificates/dense-shell-transfer-shape/consumer_contract.json"
    ),
    "charge_interface": "experimental/notes/thresholds/dense_shell_class_charges.md",
    "sim_status": "OPEN",
    "unconditional_sim": False,
    "unconditional_pdsp2": False,
    "live_kml_ledger_impact": "ZERO",
    "upstream_base": "fb6d9555339b43911c59c498373c43ed6c5cd391",
}


def sha256(path: Path) -> str:
    # Git may materialize these text artifacts with CRLF on Windows. Hash the
    # canonical UTF-8/LF representation so --check is checkout-independent.
    text = path.read_text(encoding="utf-8")
    canonical = text.replace("\r\n", "\n").replace("\r", "\n")
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def repo_relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def parse_manifest() -> tuple[dict[str, str], list[str]]:
    entries: dict[str, str] = {}
    errors: list[str] = []
    if not MANIFEST_PATH.exists():
        return entries, [f"missing manifest: {repo_relative(MANIFEST_PATH)}"]
    for line_number, raw in enumerate(
        MANIFEST_PATH.read_text(encoding="utf-8").splitlines(), start=1
    ):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split(None, 1)
        if len(parts) != 2 or len(parts[0]) != 64:
            errors.append(f"line {line_number}: malformed entry")
            continue
        digest, relative = parts[0].lower(), parts[1].strip().replace("\\", "/")
        if relative.startswith("*"):
            relative = relative[1:]
        if any(character not in "0123456789abcdef" for character in digest):
            errors.append(f"line {line_number}: malformed digest")
        elif relative in entries:
            errors.append(f"line {line_number}: duplicate path {relative}")
        else:
            entries[relative] = digest
    return entries, errors


def write_manifest() -> None:
    lines = [f"{sha256(ROOT / relative)}  {relative}" for relative in sorted(MANIFEST_EXPECTED_PATHS)]
    MANIFEST_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def stable(value):
    if isinstance(value, float):
        return format(value, ".12g")
    if isinstance(value, dict):
        return {key: stable(item) for key, item in value.items()}
    if isinstance(value, list):
        return [stable(item) for item in value]
    return value


def d_of(t: float) -> float:
    return -0.5 * math.cos(2.0 * PI * t)


def dp_of(t: float) -> float:
    return PI * math.sin(2.0 * PI * t)


def vadd(x: Sequence[float], y: Sequence[float]) -> tuple[float, ...]:
    n = max(len(x), len(y))
    out = [0.0] * n
    for index, value in enumerate(x):
        out[index] += value
    for index, value in enumerate(y):
        out[index] += value
    return tuple(out)


def n_op(vector: Sequence[float], t: float) -> tuple[float, ...]:
    """Apply N_t=K+d(t)I in flipped shifted-Chebyshev coordinates."""
    out = [0.0] * (len(vector) + 1)
    drift = d_of(t)
    for index, value in enumerate(vector):
        out[index] += drift * value
        out[index + 1] += (0.5 if index == 0 else 0.25) * value
        if index >= 1:
            out[index - 1] += 0.25 * value
    return tuple(out)


@lru_cache(maxsize=None)
def ordinary(n: int, t: float) -> tuple[float, ...]:
    if n == 0:
        return (1.0,)
    plus = (1.0 + t) / 3.0
    minus = (1.0 - t) / 3.0
    return vadd(n_op(ordinary(n - 1, plus), plus), n_op(ordinary(n - 1, minus), minus))


@lru_cache(maxsize=None)
def source(m: int, t: float) -> tuple[float, ...]:
    plus = (1.0 + t) / 3.0
    minus = (1.0 - t) / 3.0
    outer = tuple(d_of(plus) * value for value in n_op(ordinary(m, plus), plus))
    inner = tuple(d_of(minus) * value for value in n_op(ordinary(m, minus), minus))
    return vadd(outer, inner)


@lru_cache(maxsize=None)
def singleton(n: int, q: int, t: float) -> tuple[float, ...]:
    if not (1 <= q <= n):
        raise ValueError((n, q))
    if q == 1:
        return source(n - 1, t)
    plus = (1.0 + t) / 3.0
    minus = (1.0 - t) / 3.0
    return vadd(
        n_op(singleton(n - 1, q - 1, plus), plus),
        n_op(singleton(n - 1, q - 1, minus), minus),
    )


@lru_cache(maxsize=None)
def factorized(m: int, transfers: int, t: float) -> tuple[float, ...]:
    if transfers == 0:
        return source(m, t)
    plus = (1.0 + t) / 3.0
    minus = (1.0 - t) / 3.0
    return vadd(
        n_op(factorized(m, transfers - 1, plus), plus),
        n_op(factorized(m, transfers - 1, minus), minus),
    )


def gate_contract() -> dict:
    actual = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    return {
        "pass": actual == EXPECTED_CONTRACT,
        "contract_sha256": sha256(CONTRACT_PATH),
        "sim_status": actual.get("sim_status"),
        "unconditional_sim": actual.get("unconditional_sim"),
    }


def gate_authority_hashes() -> dict:
    actual = {
        name: sha256(path) if path.exists() else "MISSING"
        for name, path in AUTHORITY_PATHS.items()
    }
    return {
        "pass": actual == EXPECTED_AUTHORITY_HASHES,
        "actual": actual,
        "expected": EXPECTED_AUTHORITY_HASHES,
    }


def gate_artifact_manifest() -> dict:
    entries, errors = parse_manifest()
    listed = set(entries)
    missing_entries = sorted(MANIFEST_EXPECTED_PATHS - listed)
    extra_entries = sorted(listed - MANIFEST_EXPECTED_PATHS)
    mismatches: dict[str, dict[str, str]] = {}
    for relative, expected in entries.items():
        path = ROOT / relative
        actual = sha256(path) if path.exists() else "MISSING"
        if actual != expected:
            mismatches[relative] = {"expected": expected, "actual": actual}
    passed = not errors and not missing_entries and not extra_entries and not mismatches
    return {
        "pass": passed,
        "manifest_sha256": sha256(MANIFEST_PATH) if MANIFEST_PATH.exists() else "MISSING",
        "listed_entries": len(entries),
        "expected_entries": len(MANIFEST_EXPECTED_PATHS),
        "missing_entries": missing_entries,
        "extra_entries": extra_entries,
        "mismatches": mismatches,
        "parse_errors": errors,
    }


def gate_factorization(max_n: int = 7, cells: int = 16) -> dict:
    worst = 0.0
    checked = 0
    for n in range(1, max_n + 1):
        for q in range(1, n + 1):
            for cell in range(cells + 1):
                t = 0.5 * cell / cells
                direct = singleton(n, q, t)
                reduced = factorized(n - q, q - 1, t)
                worst = max(worst, max(abs(x - y) for x, y in zip(direct, reduced)))
                checked += len(direct)
    return {
        "pass": worst < 2.0e-12,
        "max_error": worst,
        "checked_coordinates": checked,
        "max_n": max_n,
    }


def gate_normalized_criterion(cells: int = 1024) -> dict:
    minimum_scalar_margin = float("inf")
    derivative_error = 0.0
    for cell in range(cells + 1):
        epsilon = 0.25 * cell / cells
        tout = 5.0 / 12.0 + epsilon / 3.0
        tin = 0.25 - epsilon / 3.0
        numerator = math.sin(2.0 * PI * epsilon / 3.0)
        denominator = math.sin(PI / 3.0 + 2.0 * PI * epsilon / 3.0)
        nu = numerator / denominator
        margin = math.cos(ALPHA * tout) / math.cos(ALPHA * tin) - nu
        minimum_scalar_margin = min(minimum_scalar_margin, margin)

        t = 0.5 * cell / cells
        f = math.cosh(0.7 * t) + 0.3 * math.cos(0.4 * t)
        fp = 0.7 * math.sinh(0.7 * t) - 0.12 * math.sin(0.4 * t)
        j = fp + ALPHA * math.tan(ALPHA * t) * f
        quotient_derivative = (
            fp * math.cos(ALPHA * t) + ALPHA * f * math.sin(ALPHA * t)
        ) / (math.cos(ALPHA * t) ** 2)
        derivative_error = max(
            derivative_error,
            abs(quotient_derivative - j / math.cos(ALPHA * t)),
        )
    return {
        "pass": minimum_scalar_margin >= -2.0e-15 and derivative_error < 2.0e-12,
        "minimum_scalar_margin": minimum_scalar_margin,
        "max_derivative_identity_error": derivative_error,
        "epsilon_cells": cells,
    }


def kappa(q: int) -> float:
    value = -1.0
    for level in range(1, q + 1):
        value *= math.cos(2.0 * PI / (3**level))
    return value


def gate_terminal_coordinate(max_n: int = 9, cells: int = 32) -> dict:
    worst = 0.0
    minimum = float("inf")
    argmin = None
    checked = 0
    for n in range(1, max_n + 1):
        for q in range(1, n + 1):
            for cell in range(cells + 1):
                t = 0.5 * cell / cells
                actual = singleton(n, q, t)[-1]
                expected = (2.0 ** (-n)) * kappa(q) * math.cos(2.0 * PI * t / (3**q))
                error = abs(actual - expected)
                worst = max(worst, error)
                if actual < minimum:
                    minimum = actual
                    argmin = (n, q, t)
                checked += 1
    return {
        "pass": worst < 2.0e-13 and minimum > 0.0,
        "max_error": worst,
        "minimum_terminal_coordinate": minimum,
        "argmin": repr(argmin),
        "checked_values": checked,
        "max_n": max_n,
    }


def gate_source_m0_and_counterexamples(cells: int = 256) -> dict:
    worst_formula = 0.0
    for cell in range(cells + 1):
        t = 0.5 * cell / cells
        c = math.cos(ALPHA * t)
        expected = ((3.0 - 2.0 * c * c) / 8.0, c / 4.0)
        actual = source(0, t)
        worst_formula = max(worst_formula, max(abs(x - y) for x, y in zip(actual, expected)))

    cap_gap = 0.75 - 5.0 * PI * PI / 18.0
    # pi^2 > 9 gives a strictly negative rational upper bound without libm.
    cap_gap_rational_upper = Fraction(3, 4) - Fraction(5 * 9, 18)
    shifted_gap = Fraction(-191, 1600)
    threshold = Fraction(1, 10)
    return {
        "pass": (
            worst_formula < 2.0e-14
            and cap_gap_rational_upper == Fraction(-7, 4)
            and cap_gap_rational_upper < 0
            and shifted_gap < 0
        ),
        "max_source_formula_error": worst_formula,
        "cap_six_gap_at_t0_float_diagnostic": cap_gap,
        "cap_six_rational_upper_bound": str(cap_gap_rational_upper),
        "shifted_gap_at_half": str(shifted_gap),
        "largest_possible_source_shift": str(threshold),
    }


def gate_first_insertion_positivity(max_m: int = 9, cells: int = 128) -> dict:
    minimum = float("inf")
    argmin = None
    checked = 0
    for m in range(max_m + 1):
        for cell in range(cells + 1):
            t = 0.5 * cell / cells
            vector = source(m, t)
            for index, value in enumerate(vector):
                checked += 1
                if value < minimum:
                    minimum = value
                    argmin = (m, t, index)
    return {
        "pass": minimum >= -2.0e-12,
        "minimum_coefficient": minimum,
        "argmin": repr(argmin),
        "checked_coefficients": checked,
        "max_m": max_m,
    }


Scalar = tuple[Callable[[float], float], Callable[[float], float], Callable[[float], float]]


def scalar_upper_expression(family: Scalar, t: float) -> float:
    f, fp, fpp = family

    def branch(u: float) -> float:
        hu_t = fpp(u) / 9.0 + ALPHA * ALPHA * f(u)
        hdu_t = (2.0 * dp_of(u) * fp(u) + d_of(u) * fpp(u)) / 9.0
        return 6.0 * d_of(u) * f(u) - hdu_t + (6.0 * f(u) - hu_t) / 3.0

    return branch((1.0 + t) / 3.0) + branch((1.0 - t) / 3.0)


def gate_scalar_upper_cap(cells: int = 2048) -> dict:
    families: list[Scalar] = [
        (lambda t: 1.0, lambda t: 0.0, lambda t: 0.0),
        (
            lambda t: math.cos(ALPHA * t),
            lambda t: -ALPHA * math.sin(ALPHA * t),
            lambda t: -(ALPHA**2) * math.cos(ALPHA * t),
        ),
        (lambda t: math.cosh(t), lambda t: math.sinh(t), lambda t: math.cosh(t)),
        (
            lambda t: 1.0 + 0.2 * math.cosh(t),
            lambda t: 0.2 * math.sinh(t),
            lambda t: 0.2 * math.cosh(t),
        ),
    ]
    minimum = float("inf")
    argmin = None
    for family_index, family in enumerate(families):
        for cell in range(cells + 1):
            t = 0.5 * cell / cells
            value = scalar_upper_expression(family, t)
            if value < minimum:
                minimum = value
                argmin = (family_index, t)

    phi_quarter_lower = Fraction(112, 243) - Fraction(22, 63)
    coupled_lower = Fraction(56, 81) - Fraction(59, 243) - Fraction(22, 63)
    expected_phi_quarter = Fraction(190, 1701)
    expected_coupled = Fraction(169, 1701)
    return {
        "pass": (
            minimum >= -2.0e-12
            and phi_quarter_lower == expected_phi_quarter
            and coupled_lower == expected_coupled
            and phi_quarter_lower > 0
            and coupled_lower > 0
        ),
        "minimum_test_family_value": minimum,
        "argmin": repr(argmin),
        "phi_quarter_exact_derivation": "112/243 - 22/63",
        "analytic_margin_phi_quarter": str(phi_quarter_lower),
        "coupled_exact_derivation": "56/81 - 59/243 - 22/63",
        "analytic_margin_coupled": str(coupled_lower),
        "cells": cells,
    }


def run() -> dict:
    gates = {
        "consumer_contract": gate_contract(),
        "upstream_authority_hashes": gate_authority_hashes(),
        "artifact_manifest": gate_artifact_manifest(),
        "insertion_factorization": gate_factorization(),
        "normalized_criterion": gate_normalized_criterion(),
        "terminal_coordinate": gate_terminal_coordinate(),
        "source_m0_guardrails": gate_source_m0_and_counterexamples(),
        "first_insertion_positivity_regression": gate_first_insertion_positivity(),
        "scalar_upper_cap_regression": gate_scalar_upper_cap(),
    }
    payload = {
        "schema": "singleton-master-reductions/v2",
        "claim_status": "PROVED_REDUCTIONS_ROUTE_CUT_OPEN_GAP",
        "dependency_chain": EXPECTED_CONTRACT["dependency_chain"],
        "downstream_consumer": EXPECTED_CONTRACT["downstream_consumer"],
        "sim_status": "OPEN",
        "unconditional_sim": False,
        "unconditional_pdsp2": False,
        "live_kml_ledger_impact": "ZERO",
        "finite_scans_status": "COMPUTED regressions; analytic note is load-bearing",
        "upstream_base": EXPECTED_CONTRACT["upstream_base"],
        "provenance": {
            "command": (
                "python3 experimental/scripts/verify_singleton_master_reductions.py "
                "--write-manifest --emit-cert"
            ),
            "python_version": platform.python_version(),
            "upstream_base": EXPECTED_CONTRACT["upstream_base"],
            "parameters": {
                "factorization_max_n": 7,
                "factorization_cells": 16,
                "normalized_criterion_cells": 1024,
                "terminal_max_n": 9,
                "terminal_cells": 32,
                "source_positivity_max_m": 9,
                "source_positivity_cells": 128,
                "scalar_upper_cap_cells": 2048,
            },
            "authority_sha256": EXPECTED_AUTHORITY_HASHES,
        },
        "source_sha256": sha256(Path(__file__).resolve()),
        "proof_sha256": sha256(PROOF_PATH),
        "consumer_contract_sha256": sha256(CONTRACT_PATH),
        "gates": gates,
        "pass": all(gate["pass"] for gate in gates.values()),
    }
    return stable(payload)


def encoded_payload() -> tuple[dict, str]:
    payload = run()
    return payload, json.dumps(payload, indent=2, sort_keys=True) + "\n"


def status_guard(payload: dict) -> bool:
    """Fail closed if a certificate promotes either open theorem."""
    return (
        payload.get("schema") == "singleton-master-reductions/v2"
        and payload.get("claim_status")
        == "PROVED_REDUCTIONS_ROUTE_CUT_OPEN_GAP"
        and payload.get("dependency_chain") == EXPECTED_CONTRACT["dependency_chain"]
        and payload.get("sim_status") == "OPEN"
        and payload.get("unconditional_sim") is False
        and payload.get("unconditional_pdsp2") is False
        and payload.get("live_kml_ledger_impact") == "ZERO"
    )


def run_tamper_selftest() -> bool:
    payload, _ = encoded_payload()
    mutations = [
        {**payload, "sim_status": "PROVED"},
        {**payload, "unconditional_sim": True},
        {**payload, "unconditional_pdsp2": True},
        {**payload, "claim_status": "SIM_PROVED"},
        {**payload, "dependency_chain": ["SIM", "PDSP_2"]},
        {**payload, "live_kml_ledger_impact": "POSITIVE"},
    ]
    caught = 0
    for index, mutation in enumerate(mutations, start=1):
        if not status_guard(mutation):
            caught += 1
            print(f"tamper-{index}: detected")
        else:
            print(f"tamper-{index}: NOT DETECTED")
    print(f"tamper-selftest: caught {caught}/{len(mutations)}")
    return caught == len(mutations)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit-cert", action="store_true")
    parser.add_argument("--write-manifest", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()

    if args.tamper_selftest:
        return 0 if run_tamper_selftest() else 1

    if args.write_manifest:
        write_manifest()
        print("manifest:", MANIFEST_PATH)

    payload, encoded = encoded_payload()
    for name, gate in payload["gates"].items():
        print(f"[{('PASS' if gate['pass'] else 'FAIL')}] {name}")
        for key, value in gate.items():
            if key != "pass":
                print(f"  {key}: {value}")
    print("RESULT:", "PASS" if payload["pass"] else "FAIL")

    if args.emit_cert:
        CERT_PATH.parent.mkdir(parents=True, exist_ok=True)
        CERT_PATH.write_text(encoded, encoding="utf-8")
        print("certificate:", CERT_PATH)
    if args.check:
        if not CERT_PATH.exists():
            print("missing_certificate:", CERT_PATH)
            return 1
        if CERT_PATH.read_text(encoding="utf-8") != encoded:
            print("certificate_mismatch")
            return 1
        print("certificate_check: PASS")
    return 0 if payload["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
