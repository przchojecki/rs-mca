#!/usr/bin/env python3
"""Verify the Cycle84 projected-log certificate for the normalized slot table.

This nonmutating verifier checks the compact witness fixture
experimental/data/witnesses/m1-cycle84/slot_logs.json. The fixture supplies a
discrete log for each of the 336 normalized slot values. This script verifies
those logs by exponentiation in F_17^16, checks colors/residues, and checks the
tau-pair structure used by the projected duplicate-bin census.

It does not rerun the projected tau-folded duplicate-bin enumeration. Its job is
to certify the additive log model on which that enumeration runs.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Dict, Sequence, Tuple


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[1]
DEFAULT_CERTIFICATE = (
    REPO_ROOT / "experimental" / "data" / "witnesses" / "m1-cycle84" / "slot_logs.json"
)
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import verify_m1_cycle116_slot_identities as slot


N = 17**16 - 1
M = N // 3
EXPECTED_FACTORS = {2: 8, 3: 2, 5: 1, 29: 1, 18913: 1, 41761: 1, 184417: 1}
EXPECTED_MODS = [256, 9, 5, 29, 18913, 41761, 184417]
EXPECTED_GENERATOR = [2, 1]
EXPECTED_KAPPA = 15_337_197_211_725_320_908
EXPECTED_FIXED_ROOTS = [7_668_598_605_862_660_454, 15_778_797_251_807_138_534]


FieldElt = Tuple[int, ...]


def product_from_factors(factors: Dict[int, int]) -> int:
    out = 1
    for prime, exponent in factors.items():
        out *= prime**exponent
    return out


def build_slot_values() -> Dict[Tuple[int, int, int], FieldElt]:
    beta_squared = slot.fmul(slot.BETA, slot.BETA)
    seed_polys = {
        seed: slot.prime_poly_from_roots(
            pow(3, exponent, slot.P) for exponent in exponents
        )
        for seed, exponents in slot.E_SETS.items()
    }
    return {
        (t, seed, shift): slot.normalized_u(
            seed_polys,
            beta_squared,
            t,
            seed,
            shift,
        )
        for t in range(1, 8)
        for seed in (1, 2, 3)
        for shift in range(16)
    }


def row_key(row: Dict[str, Any]) -> Tuple[int, int, int]:
    return int(row["t"]), int(row["i"]), int(row["a"])


def key_index(seed: int, shift: int) -> int:
    return (seed - 1) * 16 + shift


def key_seed_shift(key: int) -> Tuple[int, int]:
    return key // 16 + 1, key % 16


def tau_key(key: int) -> int:
    seed, shift = key_seed_shift(key)
    if seed == 1:
        return 16 + (shift + 6) % 16
    if seed == 2:
        return (shift + 10) % 16
    return 32 + (shift + 8) % 16


def verify_records(data: Dict[str, Any]) -> Dict[str, Any]:
    slot_values = build_slot_values()
    records = data["records"]
    if len(records) != 336:
        raise AssertionError(("bad record count", len(records)))

    seen = set()
    logs_mod_m = [[None for _ in range(48)] for _ in range(7)]
    colors = [[None for _ in range(48)] for _ in range(7)]
    full_logs = [[None for _ in range(48)] for _ in range(7)]

    for row in records:
        t, seed, shift = row_key(row)
        if (t, seed, shift) in seen:
            raise AssertionError(("duplicate row", row))
        seen.add((t, seed, shift))
        if t not in range(1, 8) or seed not in (1, 2, 3) or shift not in range(16):
            raise AssertionError(("bad row key", row))

        log_value = int(row["log"])
        if not 0 <= log_value < N:
            raise AssertionError(("bad log range", row))
        if row["res"] != [log_value % modulus for modulus in EXPECTED_MODS]:
            raise AssertionError(("bad residues", row))

        expected_color = slot.color(seed, shift)
        if int(row["color"]) != expected_color:
            raise AssertionError(("bad color", row))

        value = slot_values[(t, seed, shift)]
        if slot.fpow(slot.BETA, log_value) != value:
            raise AssertionError(("log does not exponentiate", row))

        k = key_index(seed, shift)
        logs_mod_m[t - 1][k] = log_value % M
        full_logs[t - 1][k] = log_value
        colors[t - 1][k] = expected_color

    if len(seen) != 336:
        raise AssertionError("missing rows")
    if any(value is None for row in logs_mod_m for value in row):
        raise AssertionError("incomplete log table")
    if any(value is None for row in colors for value in row):
        raise AssertionError("incomplete color table")

    return {
        "logs_mod_m": logs_mod_m,
        "full_logs": full_logs,
        "colors": colors,
    }


def verify_tau_structure(tables: Dict[str, Any]) -> Dict[str, Any]:
    logs_mod_m = tables["logs_mod_m"]
    colors = tables["colors"]

    slot_constants = []
    half_keys = []
    for t in range(7):
        constants = set()
        for key in range(48):
            tau = tau_key(key)
            if tau_key(tau) != key:
                raise AssertionError(("tau not involutive", key, tau))
            if tau == key:
                raise AssertionError(("tau fixed key", key))
            if (colors[t][key] + colors[t][tau]) % 16 != 8:
                raise AssertionError(("tau color mismatch", t, key, tau))
            constants.add((logs_mod_m[t][key] + logs_mod_m[t][tau]) % M)
            if key < tau:
                half_keys.append((t, key))
        if len(constants) != 1:
            raise AssertionError(("nonconstant tau log sum", t, constants))
        slot_constants.append(constants.pop())

    kappa = sum(slot_constants) % M
    if kappa != EXPECTED_KAPPA:
        raise AssertionError(("bad kappa", kappa))
    for root in EXPECTED_FIXED_ROOTS:
        if (2 * root - kappa) % M != 0:
            raise AssertionError(("bad fixed root", root))

    return {
        "slot_constants": slot_constants,
        "kappa": kappa,
        "fixed_roots": EXPECTED_FIXED_ROOTS,
        "tau_half_domain_size": len(half_keys),
    }


def build_report(certificate_path: Path = DEFAULT_CERTIFICATE) -> Dict[str, Any]:
    raw_bytes = certificate_path.read_bytes()
    data = json.loads(raw_bytes)
    factors = {int(key): int(value) for key, value in data["factors"].items()}
    slot_report = slot.build_report()

    model_checks = {
        "N_matches": int(data["N"]) == N,
        "M_matches": M == 16_220_397_291_888_956_160,
        "factors_match": factors == EXPECTED_FACTORS,
        "factors_multiply_to_N": product_from_factors(factors) == N,
        "mods_match": data["mods"] == EXPECTED_MODS,
        "generator_matches_beta": data["generator"] == EXPECTED_GENERATOR,
        "generator_has_full_order": all(
            slot.fpow(slot.BETA, N // prime) != slot.ONE for prime in EXPECTED_FACTORS
        ),
        "slot_identity_replay_passes": slot_report["status"] == "PASS",
    }
    failed_model = [name for name, value in model_checks.items() if not value]
    if failed_model:
        raise AssertionError(f"failed model checks: {', '.join(failed_model)}")

    tables = verify_records(data)
    tau = verify_tau_structure(tables)

    record_checks = {
        "all_336_logs_exponentiate": True,
        "all_colors_match": True,
        "all_residue_vectors_match": True,
        "tau_pairs_have_constant_slot_sums": True,
        "tau_color_complement_is_8": True,
        "tau_half_domain_size_168": tau["tau_half_domain_size"] == 168,
    }

    return {
        "status": "PASS",
        "proof_status": "AUDIT / FINITE-MODEL-LOG-CERTIFICATE-VERIFIED",
        "theorem_problem_id": "M1 Cycle84 projected log certificate",
        "certificate_path": str(certificate_path.relative_to(REPO_ROOT)),
        "certificate_sha256": hashlib.sha256(raw_bytes).hexdigest(),
        "slot_table_digest": slot_report["slot_table"]["digest_sha256"],
        "model": {
            "N": N,
            "M": M,
            "generator": EXPECTED_GENERATOR,
            "factorization": {str(key): value for key, value in EXPECTED_FACTORS.items()},
        },
        "tau_projection": {
            "slot_constants": tau["slot_constants"],
            "kappa": tau["kappa"],
            "fixed_roots": tau["fixed_roots"],
            "tau_half_domain_size": tau["tau_half_domain_size"],
        },
        "checks": {**model_checks, **record_checks},
        "imports_required": [
            "projected tau-folded duplicate-bin completeness",
            "official ABF source gate verification",
        ],
        "nonmutating": True,
    }


def print_human(report: Dict[str, Any]) -> None:
    model = report["model"]
    tau = report["tau_projection"]

    print("m1_cycle84_projected_log_certificate: PASS")
    print(f"status={report['proof_status']}")
    print(f"theorem_problem_id={report['theorem_problem_id']}")
    print(f"certificate={report['certificate_path']}")
    print(f"certificate_sha256={report['certificate_sha256']}")
    print(f"slot_table_digest={report['slot_table_digest']}")
    print(
        "model="
        f"N={model['N']}, M={model['M']}, generator={model['generator']}"
    )
    print(
        "tau_projection="
        f"kappa={tau['kappa']}, half_domain={tau['tau_half_domain_size']}, "
        f"fixed_roots={tau['fixed_roots']}"
    )
    print("checked=" + ", ".join(report["checks"].keys()))
    print("imports_required=" + "; ".join(report["imports_required"]))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Verify the Cycle84 projected-log certificate."
    )
    parser.add_argument(
        "--certificate",
        type=Path,
        default=DEFAULT_CERTIFICATE,
        help="path to the slot log certificate JSON",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="print the audit report as JSON",
    )
    args = parser.parse_args()

    report = build_report(args.certificate)
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print_human(report)


if __name__ == "__main__":
    main()
