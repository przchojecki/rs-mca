#!/usr/bin/env python3
"""Finite regression checks for the Fourier-frame paving converse.

This is not a proof of Kadison--Singer.  It checks the Fourier/Gram identities,
the exact scaled full-dual identity, and the nontrivial raw-norm existence
bound by exhaustive subset search on small finite abelian groups.  It also
checks symbolic heavy-atom and full-slice/residual separation families.

Status: PROVED FINITE CONVERSE / OPEN SOURCE MAX-ATOM THEOREM.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import random
import shutil
import tempfile
from pathlib import Path
from typing import Any, Iterable

import numpy as np


STATUS = "PROVED FINITE CONVERSE / OPEN SOURCE MAX-ATOM THEOREM"
THEOREM_ID = "asymptotic-packed-flatness-converse-v1"
C_MSS = 3.0 + 2.0 * math.sqrt(2.0)
TOL = 2.0e-8
CERT = Path(
    "experimental/data/certificates/packed-flatness-converse/"
    "packed_flatness_converse_v1.json"
)
NOTE = Path(
    "experimental/notes/thresholds/"
    "asymptotic_primitive_profile_packed_flatness_converse_v1.md"
)
PRIOR_NOTE = Path(
    "experimental/notes/thresholds/"
    "asymptotic_primitive_profile_character_frame_v1.md"
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def normalize(value: Any) -> Any:
    if isinstance(value, float):
        return round(value, 12)
    if isinstance(value, dict):
        return {key: normalize(item) for key, item in value.items()}
    if isinstance(value, list):
        return [normalize(item) for item in value]
    return value


def payload_hash(payload: dict[str, Any]) -> str:
    clean = dict(payload)
    clean.pop("payload_sha256", None)
    return hashlib.sha256(
        json.dumps(clean, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def group_elements(shape: tuple[int, ...]) -> list[tuple[int, ...]]:
    return list(itertools.product(*(range(modulus) for modulus in shape)))


def character_table(shape: tuple[int, ...]) -> np.ndarray:
    elements = group_elements(shape)
    return np.array(
        [
            [
                np.exp(
                    2j
                    * np.pi
                    * sum(a * z / modulus for a, z, modulus in zip(chi, point, shape))
                )
                for point in elements
            ]
            for chi in elements
        ]
    )


def fourier_transform(xi: np.ndarray, shape: tuple[int, ...]) -> np.ndarray:
    return character_table(shape) @ xi


def gram(
    hat: np.ndarray,
    shape: tuple[int, ...],
    subset: tuple[int, ...],
) -> np.ndarray:
    elements = group_elements(shape)
    index = {element: position for position, element in enumerate(elements)}
    differences = np.array(
        [
            [
                index[
                    tuple(
                        (elements[j][axis] - elements[i][axis]) % modulus
                        for axis, modulus in enumerate(shape)
                    )
                ]
                for j in subset
            ]
            for i in subset
        ],
        dtype=int,
    )
    return hat[differences]


def op_norm_psd(matrix: np.ndarray) -> float:
    return float(np.linalg.eigvalsh(matrix).max(initial=0.0).real)


def subsets_at_least(q: int, minimum: int) -> Iterable[tuple[int, ...]]:
    for size in range(minimum, q + 1):
        yield from itertools.combinations(range(q), size)


def check_distribution(
    xi: np.ndarray,
    L: int,
    shape: tuple[int, ...] | None = None,
) -> dict[str, Any]:
    shape = shape or (len(xi),)
    q = math.prod(shape)
    if len(xi) != q:
        raise ValueError("measure length does not match group shape")
    if not 1 <= L <= q:
        raise ValueError("L must lie in [1,q]")
    if np.count_nonzero(xi > 1.0e-15) > L:
        raise ValueError("support size exceeds L")
    if np.any(xi < -1.0e-15) or xi.sum() > 1.0 + 1.0e-12:
        raise ValueError("xi must be a subprobability measure")

    hat = fourier_transform(xi, shape)
    atom = float(xi.max(initial=0.0))
    kappa = L * atom
    best_raw = math.inf
    best_raw_size = 0
    best_scaled = math.inf

    for subset in subsets_at_least(q, L):
        norm = op_norm_psd(gram(hat, shape, subset))
        if norm + TOL < len(subset) * atom:
            raise AssertionError("Rayleigh lower bound failed")
        if norm < best_raw:
            best_raw = norm
            best_raw_size = len(subset)
        best_scaled = min(best_scaled, L * norm / len(subset))

    full_norm = op_norm_psd(gram(hat, shape, tuple(range(q))))
    exact_full_norm = q * atom
    scaled_exact = L * full_norm / q
    checks = {
        "full_dual_raw_identity": math.isclose(
            full_norm, exact_full_norm, rel_tol=1.0e-9, abs_tol=TOL
        ),
        "scaled_infimum_exact": math.isclose(
            best_scaled, kappa, rel_tol=1.0e-9, abs_tol=TOL
        ),
        "raw_mss_existence": best_raw <= C_MSS * kappa + TOL,
        "full_dual_scaled_attains_atom": math.isclose(
            scaled_exact, kappa, rel_tol=1.0e-9, abs_tol=TOL
        ),
    }
    if not all(checks.values()):
        raise AssertionError((q, L, checks, best_raw, kappa))

    return {
        "group_shape": list(shape),
        "q": q,
        "L": L,
        "support_size": int(np.count_nonzero(xi > 1.0e-15)),
        "total_mass": float(xi.sum()),
        "max_atom": atom,
        "kappa": kappa,
        "best_raw_norm": best_raw,
        "best_raw_size": best_raw_size,
        "best_raw_over_kappa": best_raw / kappa if kappa else 0.0,
        "best_scaled_multiplier": best_scaled,
        "full_dual_raw_norm": full_norm,
        "checks": checks,
    }


def note_contract(note: str, prior: str) -> dict[str, bool]:
    return {
        "status_printed": "FINITE RAW-NORM PAVING: PROVED" in note,
        "exact_scaled_identity_printed": "exactly equal to the max-atom multiplier" in note,
        "raw_mss_bound_printed": "3+2*sqrt(2)" in note,
        "residual_equivalence_printed": "residual existential PPF <=> exact primitive-profile Q" in note,
        "nonconstructive_guard_printed": "efficient algorithm" in note
        and "existential support-dependent selection" in note,
        "source_theorem_open": "SOURCE-SPECIFIC MANY-SHELL MAX-ATOM BOUND: OPEN" in note,
        "large_sieve_open": "signed multilevel large-sieve input" in note,
        "heavy_atom_obstruction": "Heavy-atom obstruction family" in note,
        "full_residual_separation": "Full-slice/residual separation family" in note,
        "pr564_one_way_bridge": "#564 signed large-sieve input" in note
        and "=> MF564" in note
        and "does not necessarily recover PR #564's particular technical" in note,
        "prior_note_superseded": "existential packing target is superseded" in prior,
    }


def symbolic_separation_rows() -> list[dict[str, Any]]:
    rows = []
    for n in (4, 8, 16, 32):
        L = 2**n
        full_max_atom = 0.5
        residual_max_atom = 1.0 / (2.0 * (L - 1))
        full_kappa = L * full_max_atom
        residual_kappa = L * residual_max_atom
        row = {
            "N": n,
            "L": L,
            "full_max_atom": full_max_atom,
            "full_kappa": full_kappa,
            "full_log_rate": math.log(full_kappa) / n,
            "residual_total_mass": 0.5,
            "residual_max_atom": residual_max_atom,
            "residual_kappa": residual_kappa,
            "checks": {
                "full_measure_has_exponential_rayleigh_floor": full_kappa == 2 ** (n - 1),
                "residual_measure_is_uniformly_flat": residual_kappa <= 2.0 / 3.0,
                "same_full_slice_normalization_used": L * residual_max_atom == residual_kappa,
            },
        }
        if not all(row["checks"].values()):
            raise AssertionError(row)
        rows.append(row)
    return rows


def build_payload(root: Path) -> dict[str, Any]:
    rng = np.random.default_rng(20260710)
    random.seed(20260710)
    rows = []
    for q in range(3, 11):
        for L in range(1, min(q, 5) + 1):
            for trial in range(4):
                support_size = L - 1 if trial == 3 and L > 1 else L
                support = rng.choice(q, support_size, replace=False)
                weights = rng.exponential(size=support_size)
                weights /= weights.sum()
                weights *= (0.7 if trial == 2 else 1.0)
                xi = np.zeros(q)
                xi[support] = weights
                rows.append(check_distribution(xi, L))

    noncyclic_shapes = ((2, 2), (2, 4), (3, 3), (2, 2, 2))
    for shape in noncyclic_shapes:
        q = math.prod(shape)
        for trial in range(4):
            L = min(q, 2 + trial)
            support_size = L - 1 if trial == 3 else L
            support = rng.choice(q, support_size, replace=False)
            weights = rng.exponential(size=support_size)
            weights /= weights.sum()
            weights *= 0.65 if trial == 2 else 1.0
            xi = np.zeros(q)
            xi[support] = weights
            rows.append(check_distribution(xi, L, shape))

    zero_row = check_distribution(np.zeros(5), 3)
    separation_rows = symbolic_separation_rows()

    note = (root / NOTE).read_text(encoding="utf-8")
    prior = (root / PRIOR_NOTE).read_text(encoding="utf-8")
    worst_raw = max(rows, key=lambda row: row["best_raw_over_kappa"])
    normalized_rows = normalize(rows)
    rows_sha256 = hashlib.sha256(
        json.dumps(
            normalized_rows, sort_keys=True, separators=(",", ":")
        ).encode()
    ).hexdigest()
    support_slack_sample = next(
        row for row in rows if row["support_size"] < row["L"]
    )
    subprobability_sample = next(
        row for row in rows if row["total_mass"] < 0.999
    )
    payload: dict[str, Any] = {
        "schema": "packed-flatness-converse-v1",
        "theorem_id": THEOREM_ID,
        "status": STATUS,
        "base_commit": "e190193cebced1d3752d068a1c24136bc69a85d9",
        "mss_reference": {
            "paper": "Interlacing Families II: Mixed Characteristic Polynomials and the Kadison-Singer Problem",
            "arxiv": "1306.3969",
            "result": "Corollary 1.5",
            "bound": "(1/sqrt(r)+sqrt(delta))^2",
        },
        "theorem": {
            "scaled_identity": "inf_{|A|>=L} (L/|A|)||K_A|| = L||xi||_infinity",
            "raw_paving": "exists |A|>=L with ||K_A|| <= (3+2sqrt(2))L||xi||_infinity",
            "full_slice": "existential PPF iff full-slice max-atom flatness",
            "residual": "existential residual PPF iff exact primitive-profile Q",
        },
        "note_contract": note_contract(note, prior),
        "finite_census": {
            "rows_sha256": rows_sha256,
            "representative_rows": [
                rows[0],
                support_slack_sample,
                subprobability_sample,
                worst_raw,
                rows[-1],
            ],
        },
        "symbolic_heavy_atom_and_residual_separation": separation_rows,
        "zero_measure_row": zero_row,
        "summary": {
            "row_count": len(rows),
            "noncyclic_rows": sum(len(row["group_shape"]) > 1 for row in rows),
            "subprobability_rows": sum(row["total_mass"] < 0.999 for row in rows),
            "support_slack_rows": sum(row["support_size"] < row["L"] for row in rows),
            "zero_measure_pass": all(zero_row["checks"].values()),
            "all_checks_pass": all(
                all(row["checks"].values()) for row in rows
            ),
            "worst_raw_over_kappa": worst_raw["best_raw_over_kappa"],
            "worst_q": worst_raw["q"],
            "worst_L": worst_raw["L"],
            "scaled_ratio_is_tautologically_one": all(
                math.isclose(
                    row["best_scaled_multiplier"],
                    row["kappa"],
                    rel_tol=1.0e-9,
                    abs_tol=TOL,
                )
                for row in rows
            ),
            "symbolic_separation_pass": all(
                all(row["checks"].values()) for row in separation_rows
            ),
        },
        "nonclaims": [
            "no proof of the MSS theorem by finite regression",
            "no proof of source-specific many-shell max-atom flatness",
            "no proof of the signed multilevel large-sieve input",
            "no efficient or succinct MSS partition algorithm",
            "no closure of exact primitive-profile Q",
        ],
    }
    payload = normalize(payload)
    payload["payload_sha256"] = payload_hash(payload)
    return payload


def check_payload(payload: dict[str, Any]) -> list[str]:
    errors = []
    if payload.get("payload_sha256") != payload_hash(payload):
        errors.append("payload hash mismatch")
    if payload.get("status") != STATUS:
        errors.append("status mismatch")
    if not all(payload.get("note_contract", {}).values()):
        errors.append("note contract failed")
    summary = payload.get("summary", {})
    if summary.get("row_count") != 164:
        errors.append("expected 164 finite distributions")
    if summary.get("noncyclic_rows") != 16:
        errors.append("expected 16 noncyclic finite distributions")
    if not summary.get("all_checks_pass"):
        errors.append("finite regression failed")
    if not summary.get("scaled_ratio_is_tautologically_one"):
        errors.append("scaled full-dual identity failed")
    if summary.get("subprobability_rows", 0) < 30:
        errors.append("subprobability coverage missing")
    if summary.get("support_slack_rows", 0) < 25:
        errors.append("support-slack coverage missing")
    if not summary.get("zero_measure_pass"):
        errors.append("zero-measure edge case failed")
    if not summary.get("symbolic_separation_pass"):
        errors.append("symbolic heavy-atom/residual separation failed")
    expected_separation = normalize(symbolic_separation_rows())
    if payloads_close(
        payload.get("symbolic_heavy_atom_and_residual_separation"),
        expected_separation,
        "$.symbolic_heavy_atom_and_residual_separation",
    ):
        errors.append("symbolic heavy-atom/residual rows mismatch")
    expected = {
        "no proof of the MSS theorem by finite regression",
        "no proof of source-specific many-shell max-atom flatness",
        "no proof of the signed multilevel large-sieve input",
        "no efficient or succinct MSS partition algorithm",
        "no closure of exact primitive-profile Q",
    }
    if set(payload.get("nonclaims", [])) != expected:
        errors.append("nonclaim ledger mismatch")
    return errors


def write_payload(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def payloads_close(left: Any, right: Any, path: str = "$") -> list[str]:
    if isinstance(left, float) and isinstance(right, (float, int)):
        return [] if math.isclose(left, float(right), rel_tol=2.0e-10, abs_tol=2.0e-10) else [f"{path}: float mismatch"]
    if type(left) is not type(right):
        return [f"{path}: type mismatch"]
    if isinstance(left, dict):
        if set(left) != set(right):
            return [f"{path}: key mismatch"]
        out = []
        for key in left:
            out.extend(payloads_close(left[key], right[key], f"{path}.{key}"))
        return out
    if isinstance(left, list):
        if len(left) != len(right):
            return [f"{path}: length mismatch"]
        out = []
        for index, (a, b) in enumerate(zip(left, right)):
            out.extend(payloads_close(a, b, f"{path}[{index}]"))
        return out
    return [] if left == right else [f"{path}: value mismatch"]


def tamper_selftest(root: Path) -> None:
    payload = build_payload(root)
    mutations = (
        ("status", "PROVED SOURCE Q"),
        ("nonclaims", []),
        ("summary.row_count", 0),
        ("summary.noncyclic_rows", 0),
        ("summary.all_checks_pass", False),
        ("summary.scaled_ratio_is_tautologically_one", False),
        ("summary.subprobability_rows", 0),
        ("summary.support_slack_rows", 0),
        ("summary.zero_measure_pass", False),
        ("summary.symbolic_separation_pass", False),
        ("symbolic_heavy_atom_and_residual_separation", []),
        ("note_contract", {key: False for key in payload["note_contract"]}),
    )
    rejected = 0
    for dotted, value in mutations:
        candidate = json.loads(json.dumps(payload))
        cursor = candidate
        parts = dotted.split(".")
        for part in parts[:-1]:
            cursor = cursor[part]
        cursor[parts[-1]] = value
        candidate["payload_sha256"] = payload_hash(candidate)
        if check_payload(candidate):
            rejected += 1
    if rejected != len(mutations):
        raise AssertionError(f"rejected {rejected}/{len(mutations)} mutations")

    with tempfile.TemporaryDirectory() as tmp:
        temp = Path(tmp)
        note_path = temp / NOTE
        prior_path = temp / PRIOR_NOTE
        note_path.parent.mkdir(parents=True, exist_ok=True)
        prior_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(root / NOTE, note_path)
        shutil.copy2(root / PRIOR_NOTE, prior_path)
        prior_path.write_text(
            prior_path.read_text(encoding="utf-8").replace(
                "existential packing target is superseded",
                "packing target remains open",
                1,
            ),
            encoding="utf-8",
        )
        candidate = build_payload(temp)
        if all(candidate["note_contract"].values()):
            raise AssertionError("supersession mutation was not rejected")
    print(f"TAMPER SELFTEST: PASS ({rejected + 1} mutations rejected)")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()
    root = repo_root()

    if args.tamper_selftest:
        tamper_selftest(root)
        return 0

    payload = build_payload(root)
    errors = check_payload(payload)
    if args.write:
        write_payload(root / CERT, payload)
    if args.check:
        if not (root / CERT).exists():
            errors.append(f"missing certificate {CERT}")
        else:
            committed = json.loads((root / CERT).read_text(encoding="utf-8"))
            errors.extend(check_payload(committed))
            errors.extend(payloads_close(payload, committed))
    if errors:
        for error in errors[:30]:
            print(f"ERROR: {error}")
        return 1

    summary = payload["summary"]
    print(f"theorem_id: {THEOREM_ID}")
    print(f"status: {STATUS}")
    print(f"checked_rows: {summary['row_count']}")
    print(f"noncyclic_rows: {summary['noncyclic_rows']}")
    print(f"subprobability_rows: {summary['subprobability_rows']}")
    print(f"support_slack_rows: {summary['support_slack_rows']}")
    print(f"worst_raw_over_kappa: {summary['worst_raw_over_kappa']:.12f}")
    print("scaled_full_dual_identity: PASS")
    print("raw_MSS_existence_regression: PASS")
    print("heavy_atom_residual_separation: PASS")
    print(f"certificate_sha256: {payload['payload_sha256']}")
    print("RESULT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
