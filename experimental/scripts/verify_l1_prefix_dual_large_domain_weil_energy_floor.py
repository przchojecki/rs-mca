#!/usr/bin/env python3
"""Verify the large-domain mixed-Weil energy floor.

The script checks exact finite-field algebra with direct finite sums. It uses
Sage/Arb RealBallField for certified atlas energy comparisons when available,
and otherwise falls back to a widened stdlib interval whose error budget is far
below the packet's atlas margins.
"""

from __future__ import annotations

import argparse
import cmath
import itertools
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


DEFAULT_WSL_DISTRO = os.environ.get("RSMCA_WSL_DISTRO", "Ubuntu")
DEFAULT_WSL_SAGE = os.environ.get("RSMCA_WSL_SAGE", "sage")


def windows_to_wsl_path(path: Path) -> str:
    resolved = path.resolve()
    drive = resolved.drive.rstrip(":").lower()
    if drive:
        suffix = resolved.as_posix()[3:]
        return f"/mnt/{drive}/{suffix}"
    return resolved.as_posix()


def probe_wsl_sage() -> tuple[str, str, str] | None:
    wsl = shutil.which("wsl")
    if wsl is None:
        return None
    distro = DEFAULT_WSL_DISTRO
    sage_path = DEFAULT_WSL_SAGE
    try:
        probe = subprocess.run(
            [wsl, "-d", distro, "--exec", sage_path, "-v"],
            text=True,
            capture_output=True,
            timeout=30,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    combined = f"{probe.stdout}\n{probe.stderr}"
    if probe.returncode == 0 and "SageMath version" in combined:
        return wsl, distro, sage_path
    return None


def primitive_root(p: int) -> int:
    factors = []
    x = p - 1
    q = 2
    while q * q <= x:
        if x % q == 0:
            factors.append(q)
            while x % q == 0:
                x //= q
        q += 1
    if x > 1:
        factors.append(x)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in factors):
            return g
    raise ValueError(f"no primitive root for p={p}")


def log_table(p: int) -> tuple[int, dict[int, int]]:
    g = primitive_root(p)
    logs = {}
    x = 1
    for a in range(p - 1):
        logs[x] = a
        x = (x * g) % p
    return g, logs


def subgroup(p: int, n: int) -> tuple[int, ...]:
    if (p - 1) % n:
        raise ValueError("n must divide p-1")
    g = primitive_root(p)
    gen = pow(g, (p - 1) // n, p)
    out = []
    x = 1
    for _ in range(n):
        out.append(x)
        x = (x * gen) % p
    return tuple(sorted(out))


def antipodal_reps(H: tuple[int, ...], p: int) -> tuple[int, ...]:
    remaining = set(H)
    reps = []
    while remaining:
        h = min(remaining)
        reps.append(h)
        remaining.remove(h)
        remaining.remove((-h) % p)
    return tuple(reps)


def q_eval(coeffs: tuple[int, ...], x: int, p: int) -> int:
    return sum(c * pow(x, 2 * idx + 1, p) for idx, c in enumerate(coeffs)) % p


def degree(coeffs: tuple[int, ...]) -> int:
    for idx in range(len(coeffs) - 1, -1, -1):
        if coeffs[idx] % 10**100:
            return 2 * idx + 1
    return -1


def validate_phase(coeffs: tuple[int, ...], p: int, odd: bool = True) -> int:
    D = degree(coeffs)
    if D < 0:
        raise ValueError("q=0 is excluded")
    if D >= p:
        raise ValueError("D>=p requires degree reduction before applying the theorem")
    if not odd:
        raise ValueError("nonodd phases are excluded from the real-sum identity")
    return D


def additive_char(p: int, value: int) -> complex:
    return cmath.exp(2j * math.pi * (value % p) / p)


def multiplicative_char_value(logs: dict[int, int], p: int, n: int, ell: int, x: int) -> complex:
    # H has order n and index m.  Characters trivial on H are indexed by
    # ell=0,...,m-1 and satisfy chi(g^a)=exp(2*pi*i*ell*a/m).
    m = (p - 1) // n
    return cmath.exp(2j * math.pi * ell * logs[x] / m)


def subgroup_sum(coeffs: tuple[int, ...], p: int, n: int, u: int) -> complex:
    return sum(additive_char(p, 2 * u * q_eval(coeffs, h, p)) for h in subgroup(p, n))


def mixed_sum(coeffs: tuple[int, ...], p: int, n: int, u: int, ell: int, logs: dict[int, int]) -> complex:
    total = 0j
    for x in range(1, p):
        total += multiplicative_char_value(logs, p, n, ell, x) * additive_char(
            p,
            2 * u * q_eval(coeffs, x, p),
        )
    return total


def character_decomposition_case(p: int, n: int, coeffs: tuple[int, ...]) -> dict[str, object]:
    D = validate_phase(coeffs, p)
    _, logs = log_table(p)
    m = (p - 1) // n
    sqrt_p = math.sqrt(p)
    rows = []
    ok = True
    for u in range(1, min(p, 8)):
        direct = subgroup_sum(coeffs, p, n, u)
        pieces = [mixed_sum(coeffs, p, n, u, ell, logs) for ell in range(m)]
        expanded = sum(pieces) / m
        expansion_ok = abs(direct - expanded) < 1e-9
        trivial_ok = abs(pieces[0]) <= (D - 1) * sqrt_p + 1 + 1e-9
        mixed_ok = all(abs(value) <= D * sqrt_p + 1e-9 for value in pieces[1:])
        subgroup_bound_ok = abs(direct) <= D * sqrt_p + 1e-9
        ok = ok and expansion_ok and trivial_ok and mixed_ok and subgroup_bound_ok
        rows.append({
            "u": u,
            "direct_abs": abs(direct),
            "expanded_abs": abs(expanded),
            "expansion_error": abs(direct - expanded),
            "trivial_abs": abs(pieces[0]),
            "trivial_bound": (D - 1) * sqrt_p + 1,
            "max_nontrivial_abs": max([abs(value) for value in pieces[1:]] or [0.0]),
            "mixed_bound": D * sqrt_p,
            "subgroup_bound": D * sqrt_p,
            "ok": expansion_ok and trivial_ok and mixed_ok and subgroup_bound_ok,
        })
    return {
        "params": {"p": p, "n": n, "D": D, "coeffs": coeffs},
        "rows": rows,
        "ok": ok,
    }


def energy_direct(coeffs: tuple[int, ...], p: int, n: int, scalar: int) -> float:
    reps = antipodal_reps(subgroup(p, n), p)
    return sum(
        math.sin(2.0 * math.pi * scalar * q_eval(coeffs, h, p) / p) ** 2
        for h in reps
    )


def energy_from_sum(coeffs: tuple[int, ...], p: int, n: int, scalar: int) -> float:
    total = subgroup_sum(coeffs, p, n, scalar).real
    return n / 4.0 - total / 4.0


def energy_identity_case(p: int, n: int, coeffs: tuple[int, ...]) -> dict[str, object]:
    D = validate_phase(coeffs, p)
    rows = []
    ok = True
    for scalar in range(1, min(p, 10)):
        direct = energy_direct(coeffs, p, n, scalar)
        via_sum = energy_from_sum(coeffs, p, n, scalar)
        real_error = abs(subgroup_sum(coeffs, p, n, scalar).imag)
        row_ok = abs(direct - via_sum) < 1e-9 and real_error < 1e-9
        ok = ok and row_ok
        rows.append({
            "scalar": scalar,
            "direct_energy": direct,
            "sum_energy": via_sum,
            "subgroup_sum_imag_abs": real_error,
            "ok": row_ok,
        })
    return {"params": {"p": p, "n": n, "D": D}, "rows": rows, "ok": ok}


def floor_general(D: int, p: int, n: int) -> float:
    return 0.5 - D * math.sqrt(p) / (2.0 * n)


def floor_full_group(D: int, p: int) -> float:
    return 0.5 - ((D - 1) * math.sqrt(p) + 1) / (2.0 * (p - 1))


def threshold_corollary_cases() -> dict[str, object]:
    rows = []
    ok = True
    for p, D in [(257, 7), (65537, 15), (4099, 5)]:
        n_quarter = math.ceil(2 * D * math.sqrt(p))
        n_three_eighths = math.ceil(4 * D * math.sqrt(p))
        rows.append({
            "p": p,
            "D": D,
            "n_for_quarter": n_quarter,
            "floor_at_quarter_threshold": floor_general(D, p, n_quarter),
            "n_for_three_eighths": n_three_eighths,
            "floor_at_three_eighths_threshold": floor_general(D, p, n_three_eighths),
        })
        ok = ok and floor_general(D, p, n_quarter) >= 0.25 - 1e-3
        ok = ok and floor_general(D, p, n_three_eighths) >= 0.375 - 1e-3
    return {"rows": rows, "ok": ok}


def bessel_consequence_case() -> dict[str, object]:
    lam = 0.5
    rows = []
    ok = True
    for p, n, coeffs in [
        (257, 256, (1, 25, 240, 183)),
        (193, 64, (1, 10, 133, 118)),
    ]:
        D = validate_phase(coeffs, p)
        tau = floor_full_group(D, p) if n == p - 1 else floor_general(D, p, n)
        E_star = min(energy_direct(coeffs, p, n, scalar) for scalar in range(1, p))
        N = n // 2
        if tau > 0:
            row_ok = E_star >= tau * N - 1e-8
            bound = math.exp(-lam * tau * N)
            status = "NONTRIVIAL"
        else:
            row_ok = True
            bound = None
            status = "VACUOUS_NOT_FALSE"
        rows.append({
            "p": p,
            "n": n,
            "D": D,
            "tau": tau,
            "status": status,
            "E_star_over_N": E_star / N,
            "bessel_term_bound": bound,
            "ok": row_ok,
        })
        ok = ok and row_ok
    torus_rows = []
    for p, n, support in [
        (17, 16, (1, 3)),
        (31, 30, (1, 3, 5)),
    ]:
        d = (max(support) + 1) // 2
        D = max(support)
        tau = floor_full_group(D, p) if n == p - 1 else floor_general(D, p, n)
        N = n // 2
        denom = (p - 1) ** len(support)
        total = 0.0
        for values in itertools.product(range(1, p), repeat=len(support)):
            coeffs = [0] * d
            for exp, value in zip(support, values):
                coeffs[(exp - 1) // 2] = value
            total += math.exp(-lam * energy_direct(tuple(coeffs), p, n, 1))
        average = total / denom
        bound = math.exp(-lam * tau * N)
        row_ok = tau > 0 and average <= bound + 1e-12
        torus_rows.append({
            "p": p,
            "n": n,
            "support": support,
            "tau": tau,
            "torus_average": average,
            "bound": bound,
            "ok": row_ok,
        })
        ok = ok and row_ok
    return {"lambda": lam, "rows": rows, "torus_average_rows": torus_rows, "ok": ok}


def stdlib_interval_atlas(cases: list[dict[str, object]], error_ratio: float = 1e-8) -> dict[str, object]:
    """Fallback atlas checker when Sage is unavailable.

    The Sage/Arb path is preferred because it gives real-ball enclosures.  This
    fallback keeps the verifier runnable on hosts where WSL/Sage is unavailable:
    it recomputes the same finite sums with Python's libm and widens the
    winning energy ratio by a deliberately conservative absolute error budget.
    The checked atlas margins in this packet are > 4e-2, so the fallback's
    1e-8 ratio budget is not close to the decision boundary.
    """
    rows = []
    for case in cases:
        p = int(case["p"])
        n = int(case["n"])
        coeffs = tuple(int(c) for c in case["coeffs"])
        ratios = [
            energy_direct(coeffs, p, n, u) / (n // 2)
            for u in range(1, p)
        ]
        best_ratio = min(ratios)
        lower_ratio = max(0.0, best_ratio - error_ratio)
        upper_ratio = min(1.0, best_ratio + error_ratio)
        rows.append({
            "label": case["label"],
            "p": p,
            "n": n,
            "N": n // 2,
            "energy_lower": lower_ratio * (n // 2),
            "energy_upper": upper_ratio * (n // 2),
            "energy_ratio_lower": lower_ratio,
            "energy_ratio_upper": upper_ratio,
            "backend": "stdlib-libm-widened",
            "error_ratio_budget": error_ratio,
        })
    return {"bits": None, "backend": "stdlib-libm-widened", "rows": rows}


def sage_certified_atlas(
    cases: list[dict[str, object]],
    bits: int = 160,
    backend: str = "auto",
) -> dict[str, object]:
    if backend not in {"auto", "sage", "stdlib"}:
        raise ValueError("backend must be one of auto, sage, stdlib")
    if backend == "stdlib":
        return stdlib_interval_atlas(cases)
    sage_exe = shutil.which("sage")
    wsl_sage = None
    if sage_exe is None:
        wsl_sage = probe_wsl_sage()
    if sage_exe is None and wsl_sage is None:
        if backend == "sage":
            raise RuntimeError("Sage executable not found on PATH or configured WSL Sage")
        print(
            "warning: atlas backend auto downgraded to stdlib-libm-widened; "
            "Sage executable not found on PATH or configured WSL Sage",
            file=sys.stderr,
        )
        return stdlib_interval_atlas(cases)
    request = {"bits": bits, "cases": cases}
    sage_code = r'''
import json
import sys
from sage.all import RealBallField

inp = json.load(open(sys.argv[1]))
bits = int(inp["bits"])
R = RealBallField(bits)
pi = R.pi()

def primitive_root(p):
    factors = []
    x = p - 1
    q = 2
    while q * q <= x:
        if x % q == 0:
            factors.append(q)
            while x % q == 0:
                x //= q
        q += 1
    if x > 1:
        factors.append(x)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in factors):
            return g
    raise ValueError("no primitive root")

def subgroup(p, n):
    g = primitive_root(p)
    gen = pow(g, (p - 1) // n, p)
    out = []
    x = 1
    for _ in range(n):
        out.append(x)
        x = (x * gen) % p
    return sorted(out)

def reps(H, p):
    remaining = set(H)
    out = []
    while remaining:
        h = min(remaining)
        out.append(h)
        remaining.remove(h)
        remaining.remove((-h) % p)
    return out

def q_eval(coeffs, x, p):
    return sum(int(c) * pow(x, 2*i + 1, p) for i, c in enumerate(coeffs)) % p

rows = []
for case in inp["cases"]:
    p = int(case["p"])
    n = int(case["n"])
    coeffs = [int(c) for c in case["coeffs"]]
    H = subgroup(p, n)
    Rreps = reps(H, p)
    intervals = []
    for u in range(1, p):
        E = R(0)
        for h in Rreps:
            value = (u * q_eval(coeffs, h, p)) % p
            E += (2 * pi * R(value) / R(p)).sin() ** 2
        intervals.append(E)
    best = min(intervals, key=lambda x: x.center())
    rows.append({
        "label": case["label"],
        "p": p,
        "n": n,
        "N": n // 2,
        "energy_lower": float(best.lower()),
        "energy_upper": float(best.upper()),
        "energy_ratio_lower": float((best / R(n // 2)).lower()),
        "energy_ratio_upper": float((best / R(n // 2)).upper()),
    })
json.dump({"bits": bits, "rows": rows}, open(sys.argv[2], "w"), sort_keys=True)
'''
    with tempfile.TemporaryDirectory() as tmp:
        in_path = Path(tmp) / "request.json"
        out_path = Path(tmp) / "response.json"
        code_path = Path(tmp) / "certify_large_domain.py"
        in_path.write_text(json.dumps(request))
        code_path.write_text(sage_code)
        if sage_exe is not None:
            command = [sage_exe, "-python", str(code_path), str(in_path), str(out_path)]
            backend_name = "sage-arb"
        else:
            wsl, distro, sage_path = wsl_sage or ("wsl", DEFAULT_WSL_DISTRO, DEFAULT_WSL_SAGE)
            command = [
                wsl,
                "-d",
                distro,
                "--exec",
                sage_path,
                "-python",
                windows_to_wsl_path(code_path),
                windows_to_wsl_path(in_path),
                windows_to_wsl_path(out_path),
            ]
            backend_name = "sage-arb-wsl"
        completed = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if completed.returncode != 0:
            if backend == "auto":
                print(
                    "warning: atlas backend auto downgraded to stdlib-libm-widened; "
                    "Sage atlas certification command failed",
                    file=sys.stderr,
                )
                return stdlib_interval_atlas(cases)
            raise RuntimeError(
                "Sage atlas certification failed:\n"
                f"STDOUT:\n{completed.stdout}\nSTDERR:\n{completed.stderr}"
            )
        result = json.loads(out_path.read_text())
        result["backend"] = backend_name
        return result


def atlas_regression_case(backend: str = "auto") -> dict[str, object]:
    cases = [
        {"label": "193,64,4", "p": 193, "n": 64, "coeffs": [1, 10, 133, 118]},
        {"label": "257,32,4", "p": 257, "n": 32, "coeffs": [1, 177, 104, 67]},
        {"label": "257,64,4", "p": 257, "n": 64, "coeffs": [1, 96, 55, 162]},
        {"label": "257,128,4", "p": 257, "n": 128, "coeffs": [1, 198, 160, 165]},
        {"label": "257,256,4", "p": 257, "n": 256, "coeffs": [1, 25, 240, 183]},
    ]
    certified = sage_certified_atlas(cases, backend=backend)
    rows = []
    ok = True
    for case, cert in zip(cases, certified["rows"]):
        D = validate_phase(tuple(case["coeffs"]), case["p"])
        floor = floor_full_group(D, case["p"]) if case["n"] == case["p"] - 1 else floor_general(D, case["p"], case["n"])
        status = "NONTRIVIAL" if floor > 0 else "VACUOUS_NOT_FALSE"
        row_ok = status == "VACUOUS_NOT_FALSE" or cert["energy_ratio_lower"] >= floor - 1e-12
        rows.append({
            **cert,
            "D": D,
            "floor": floor,
            "status": status,
            "ok": row_ok,
        })
        ok = ok and row_ok
    return {"certification": certified, "rows": rows, "ok": ok}


def rejection_cases() -> dict[str, object]:
    rows = []
    for label, coeffs, p, odd in [
        ("q=0", (0, 0), 17, True),
        ("D>=p", tuple([0] * 9 + [1]), 17, True),
        ("nonodd", (1,), 17, False),
    ]:
        try:
            validate_phase(coeffs, p, odd=odd)
            rejected = False
        except ValueError as exc:
            rejected = True
            message = str(exc)
        rows.append({"label": label, "rejected": rejected, "message": message if rejected else ""})
    return {"rows": rows, "ok": all(row["rejected"] for row in rows)}


def run_all(atlas_backend: str = "auto") -> dict[str, object]:
    character_cases = [
        character_decomposition_case(17, 16, (1, 3)),
        character_decomposition_case(17, 8, (1, 5)),
        character_decomposition_case(31, 30, (1, 2, 4)),
        character_decomposition_case(41, 20, (1, 7, 3)),
    ]
    energy_cases = [
        energy_identity_case(17, 16, (1, 3)),
        energy_identity_case(17, 8, (1, 5)),
        energy_identity_case(31, 30, (1, 2, 4)),
    ]
    thresholds = threshold_corollary_cases()
    bessel = bessel_consequence_case()
    atlas = atlas_regression_case(atlas_backend)
    rejections = rejection_cases()
    all_ok = (
        all(case["ok"] for case in character_cases)
        and all(case["ok"] for case in energy_cases)
        and thresholds["ok"]
        and bessel["ok"]
        and atlas["ok"]
        and rejections["ok"]
    )
    return {
        "proof_status": "AUDIT / PROVED finite-field identities with an EXPERIMENTAL stdlib fallback when Sage is unavailable",
        "theorem_problem_id": "L1 large-domain mixed-Weil energy floor",
        "reproducibility": {
            "command": "python3 experimental/scripts/verify_l1_prefix_dual_large_domain_weil_energy_floor.py",
            "atlas_backend": atlas_backend,
        },
        "character_decomposition_cases": character_cases,
        "energy_identity_cases": energy_cases,
        "threshold_corollaries": thresholds,
        "bessel_consequence": bessel,
        "atlas_regressions": atlas,
        "rejection_cases": rejections,
        "ALL_CHECKS_OK": all_ok,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument(
        "--atlas-backend",
        choices=("auto", "sage", "stdlib"),
        default="auto",
        help="atlas certification backend; auto uses Sage if available and otherwise a widened stdlib interval",
    )
    args = parser.parse_args()
    result = run_all(args.atlas_backend)
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print("L1 large-domain mixed-Weil energy-floor verifier")
        print(f"proof_status: {result['proof_status']}")
        print(f"theorem_problem_id: {result['theorem_problem_id']}")
        for case in result["character_decomposition_cases"]:
            params = case["params"]
            print(
                "  chars p={p} n={n} D={D}: rows={rows} ok={ok}".format(
                    p=params["p"],
                    n=params["n"],
                    D=params["D"],
                    rows=len(case["rows"]),
                    ok=case["ok"],
                )
            )
        for row in result["atlas_regressions"]["rows"]:
            print(
                "  atlas {label}: floor={floor:.6g} E/N=[{lo:.6g},{hi:.6g}] {status} ok={ok}".format(
                    label=row["label"],
                    floor=row["floor"],
                    lo=row["energy_ratio_lower"],
                    hi=row["energy_ratio_upper"],
                    status=row["status"],
                    ok=row["ok"],
                )
            )
        print(f"  atlas_backend={result['atlas_regressions']['certification'].get('backend')}")
        print(f"  threshold_corollaries_ok={result['threshold_corollaries']['ok']}")
        print(f"  bessel_consequence_ok={result['bessel_consequence']['ok']}")
        print(f"  rejection_cases_ok={result['rejection_cases']['ok']}")
        print(f"ALL_CHECKS_OK={result['ALL_CHECKS_OK']}")
    if not result["ALL_CHECKS_OK"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
