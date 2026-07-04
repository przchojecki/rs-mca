#!/usr/bin/env python3
"""Exact verifier for KoalaBear sextic BCHKS25 JMCA bounds.

This verifier has two layers.

1. ``stated_theorem_4_6_safe_edge_v1`` applies the displayed BCHKS25
   Theorem 4.6 list correlated-agreement bound exactly as stated.
2. ``parametric_list_mca_squeeze_v2`` verifies the arithmetic for the
   parameterized list-MCA bridge lemma stated in
   ``experimental/notes/audits/koalabear_bchks25_parametric_list_mca_lemma_v1.md``.

The first layer is the PR headline. The second layer is deliberately separated:
it is not a consequence of the displayed Theorem 4.6 formula alone.

All numerical checks use integers and Fractions; no floating point arithmetic is
used in any certificate decision.
"""
from __future__ import annotations

import argparse
import difflib
import json
from dataclasses import dataclass
from fractions import Fraction
from math import isqrt
from pathlib import Path
from typing import Any, Dict, Iterable, Mapping, Optional, Tuple

N = 2**21
REPO_DIMENSION_K = 2**20
BCHKS_DEGREE_K = REPO_DIMENSION_K - 1
P_KOALABEAR = 2**31 - 2**24 + 1
EXTENSION_DEGREE = 6
TARGET_BITS = 128
TARGET_DENOMINATOR = 2**TARGET_BITS
Q_LINE = P_KOALABEAR**EXTENSION_DEGREE
BUDGET = (Q_LINE - 1) // TARGET_DENOMINATOR

SAFE_CERT_DIR = Path("experimental/data/certificates/koalabear-bchks25-jmca-safe-edge-v1")
SQUEEZE_CERT_DIR = Path("experimental/data/certificates/koalabear-bchks25-jmca-param-squeeze-v2")
SHARED_CERT_DIR = Path("experimental/data/certificates/koalabear-bchks25-jmca-bounds-v1")
REPORT_PATH = Path("experimental/notes/certificate_scanner/outputs/koalabear_bchks25_jmca_bounds_v1_report.md")

BCHKS25_SOURCE = {
    "title": "On Proximity Gaps for Reed-Solomon Codes",
    "authors": "Eli Ben-Sasson, Dan Carmon, Ulrich Habock, Swastik Kopparty, Shubhangi Saraf",
    "pdf_url": "https://www.math.toronto.edu/swastik/rs-proximity-gaps-2025.pdf",
    "doi": "https://dl.acm.org/doi/10.1145/3798129.3800827",
    "pdf_date": "2025-11-11",
    "accessed": "2026-07-04",
    "pdf_sha256": "4ADDED3E55B83C15FCC8A698FB57E137F5BD83E79EA25CE79382817C1AD26A46",
    "headline_import": "Theorem 4.6, List correlated agreement up to Johnson bound",
    "headline_import_pages": "pp. 27-28",
    "parametric_appendix_dependency": (
        "Section 3.2 improved-bound proof, especially the unnumbered Hensel/useful-factor "
        "step beginning with |S_{x0,R,H}| > 2 D_X D_Y^(R) D_Y^(H) D_Z^(R), and the "
        "Theorem 4.6 paragraph generalizing that all-useful-factor bookkeeping to list correlated agreement."
    ),
    "parametric_appendix_dependency_pages": "Section 3.2, pp. 23-25; Theorem 4.6 proof paragraph, p. 28",
}


def ceil_div(a: int, b: int) -> int:
    if b <= 0:
        raise ValueError("positive denominator required")
    return -(-a // b)


def ceil_fraction(x: Fraction) -> int:
    return ceil_div(x.numerator, x.denominator)


def floor_fraction(x: Fraction) -> int:
    return x.numerator // x.denominator


def ceil_sqrt_fraction(num: int, den: int) -> int:
    """Return ceil(sqrt(num / den)) for num >= 0, den > 0."""
    if num < 0 or den <= 0:
        raise ValueError("expected num >= 0 and den > 0")
    candidate = isqrt(num // den)
    while candidate * candidate * den < num:
        candidate += 1
    while candidate > 0 and (candidate - 1) * (candidate - 1) * den >= num:
        candidate -= 1
    return candidate


def fstr(x: Fraction) -> str:
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def stable_json(obj: Mapping[str, Any]) -> str:
    return json.dumps(obj, indent=2, sort_keys=True) + "\n"


def stated_m_for_radius(r: int, rho_num: int, rho_den: int) -> int:
    """Return m=max(ceil(sqrt(rho)/(1-sqrt(rho)-r/N)), 3) exactly.

    Let A=N-r. The candidate m is valid iff

        m * (A/N - sqrt(rho)) >= sqrt(rho),

    equivalently

        m^2 A^2 rho_den >= (m+1)^2 rho_num N^2.
    """
    if not (0 <= r < N):
        raise ValueError("r out of range")
    agreement = N - r
    if agreement * agreement * rho_den <= rho_num * N * N:
        raise ValueError("radius is not below the Johnson radius for this rho")
    m = 3
    while m * m * agreement * agreement * rho_den < (m + 1) * (m + 1) * rho_num * N * N:
        m += 1
    return m


def stated_bound_ceil(r: int, rho_num: int, rho_den: int) -> Tuple[int, int, Fraction]:
    """Return ceil of displayed BCHKS25 Theorem 4.6 bound, m, and X.

    For M=1, t=m+1/2, gamma=r/N,

        N_JMCA = ((2t^5 + 3t gamma rho)/(3 rho^(3/2))) N + t/sqrt(rho)
               = X/sqrt(rho),
        X      = 2t^5 N/(3rho) + t(r+1).

    If rho=a/b, ceil(X/sqrt(rho)) is computed by exact integer squaring.
    """
    m = stated_m_for_radius(r, rho_num, rho_den)
    t = Fraction(2 * m + 1, 2)
    x_pre_sqrt = Fraction(2, 1) * (t**5) * N * rho_den / (3 * rho_num) + t * (r + 1)
    ceil_bound = ceil_sqrt_fraction(
        x_pre_sqrt.numerator * x_pre_sqrt.numerator * rho_den,
        x_pre_sqrt.denominator * x_pre_sqrt.denominator * rho_num,
    )
    return ceil_bound, m, x_pre_sqrt


def stated_result(label: str, status: str, r: int, rho_num: int, rho_den: int) -> Dict[str, Any]:
    ceil_bound, m, x_pre_sqrt = stated_bound_ceil(r, rho_num, rho_den)
    return {
        "label": label,
        "status": status,
        "r": r,
        "A": N - r,
        "delta": f"{r}/{N}",
        "rho": f"{rho_num}/{rho_den}",
        "m": m,
        "X_pre_sqrt": fstr(x_pre_sqrt),
        "ceil_N_JMCA": ceil_bound,
        "budget": BUDGET,
        "ceil_N_JMCA_le_budget": ceil_bound <= BUDGET,
        "ceil_N_JMCA_lt_budget": ceil_bound < BUDGET,
        "budget_minus_ceil_N_JMCA": BUDGET - ceil_bound,
    }


@dataclass(frozen=True)
class ParametricCertificate:
    label: str
    status: str
    theorem_dependency: str
    r: int
    m: int
    U_ceil_DX: int
    V_ceil_DY: int
    W_ceil_DZ: int
    eps_num: int
    eps_den: int


def interpolation_variable_count(U: int, V: int, W: int, k_degree: int = BCHKS_DEGREE_K) -> int:
    total = 0
    for j in range(V):
        i_count = U - k_degree * j
        h_count = W - j
        if i_count <= 0 or h_count <= 0:
            raise ValueError("non-positive monomial count encountered")
        total += i_count * h_count
    return total


def interpolation_equation_count(m: int, W: int, n: int = N) -> int:
    return n * sum((W - s) * (m - s) for s in range(m))


def verify_parametric_certificate(c: ParametricCertificate) -> Dict[str, Any]:
    eps = Fraction(c.eps_num, c.eps_den)
    if not (0 < eps < 1):
        raise AssertionError("expected 0 < epsilon < 1")
    agreement = N - c.r
    U, V, W, m = c.U_ceil_DX, c.V_ceil_DY, c.W_ceil_DZ, c.m

    # Use the lower edge of each ceiling cell. This minimizes R for the fixed
    # integer monomial support while preserving the same U,V,W.
    DX = Fraction(U - 1, 1) + eps
    DY = Fraction(V - 1, 1) + eps
    DZ = Fraction(W - 1, 1) + eps

    assert ceil_fraction(DX) == U
    assert ceil_fraction(DY) == V
    assert ceil_fraction(DZ) == W
    assert V >= m
    assert W >= V
    assert U > BCHKS_DEGREE_K * (V - 1)
    assert W > V - 1

    root_slack = Fraction(m * agreement, 1) - DX
    assert root_slack > 0

    n_vars = interpolation_variable_count(U, V, W)
    n_eqs = interpolation_equation_count(m, W)
    assert n_vars > n_eqs

    R = Fraction(2, 1) * DX * DY * DY * DZ + Fraction(c.r + 1, 1) * DY
    ceil_R = ceil_fraction(R)
    floor_R = floor_fraction(R)
    assert ceil_R < BUDGET

    return {
        "label": c.label,
        "status": c.status,
        "theorem_dependency": c.theorem_dependency,
        "r": c.r,
        "A": agreement,
        "delta": f"{c.r}/{N}",
        "m": m,
        "epsilon": fstr(eps),
        "D_X": fstr(DX),
        "D_Y": fstr(DY),
        "D_Z": fstr(DZ),
        "D_X_integer_plus_epsilon": f"{U - 1} + {fstr(eps)}",
        "D_Y_integer_plus_epsilon": f"{V - 1} + {fstr(eps)}",
        "D_Z_integer_plus_epsilon": f"{W - 1} + {fstr(eps)}",
        "U_ceil_DX": U,
        "V_ceil_DY": V,
        "W_ceil_DZ": W,
        "interpolation_admissibility": {
            "V_ge_m": V >= m,
            "W_ge_V": W >= V,
            "U_gt_k_times_V_minus_1": U > BCHKS_DEGREE_K * (V - 1),
            "W_gt_V_minus_1": W > V - 1,
        },
        "root_agreement_condition": {
            "m_times_A_minus_D_X": fstr(root_slack),
            "D_X_lt_m_times_A": root_slack > 0,
        },
        "interpolation_count": {
            "n_vars": n_vars,
            "n_eqs": n_eqs,
            "n_vars_minus_n_eqs": n_vars - n_eqs,
            "n_vars_gt_n_eqs": n_vars > n_eqs,
        },
        "useful_factor_bound": {
            "formula": "R = 2*D_X*D_Y^2*D_Z + (r+1)*D_Y",
            "R_bound": fstr(R),
            "floor_R_bound": floor_R,
            "ceil_R_bound": ceil_R,
            "ceil_R_bound_lt_budget": ceil_R < BUDGET,
        },
        "budget": BUDGET,
        "budget_minus_ceil_R_bound": BUDGET - ceil_R,
    }


def min_u_for_support(m: int, V: int, W: int) -> int:
    """Minimum U making n_vars > n_eqs for fixed m,V,W."""
    t1 = V * (V - 1) // 2
    t2 = V * (V - 1) * (2 * V - 1) // 6
    s0 = V * W - t1
    s1 = W * t1 - t2
    m1 = m * (m + 1) // 2
    m2 = (m**3 - m) // 6
    n_eqs = N * (W * m1 - m2)
    return (n_eqs + BCHKS_DEGREE_K * s1) // s0 + 1


def best_parametric_integer_cell_for_radius(r: int) -> Optional[Tuple[int, int, int, int, int, int]]:
    """Exhaust the optimized-epsilon integer-ceiling family for one radius.

    For fixed U,V,W,m, the best possible R is approached by taking
    D_X=U-1+epsilon, D_Y=V-1+epsilon, D_Z=W-1+epsilon with epsilon -> 0+.
    The least possible integer ceiling is therefore

        2(U-1)(V-1)^2(W-1) + (r+1)(V-1) + 1.

    The search is finite. If m >= 603, then V >= m, W >= V and
    U > k(V-1) imply the lower bound 2*k*(m-1)^4 >= budget, so no such
    parameter can beat the budget.
    """
    agreement = N - r
    best: Optional[Tuple[int, int, int, int, int, int]] = None
    max_m = 602
    for m in range(1, max_m + 1):
        v_max = (m * agreement - 1) // BCHKS_DEGREE_K + 1
        for V in range(max(m, 2), v_max + 1):
            min_u0 = BCHKS_DEGREE_K * (V - 1) + 1
            rhs = BUDGET - 1 - (r + 1) * (V - 1)
            denom = 2 * (min_u0 - 1) * (V - 1) ** 2
            if rhs <= 0 or denom <= 0:
                continue
            w_max = rhs // denom + 1
            if w_max < V:
                continue
            hi_u = max(min_u_for_support(m, V, w_max), min_u0)
            if hi_u > m * agreement:
                continue
            lo, hi = V, w_max
            while lo < hi:
                mid = (lo + hi) // 2
                mid_u = max(min_u_for_support(m, V, mid), min_u0)
                if mid_u <= m * agreement:
                    hi = mid
                else:
                    lo = mid + 1
            W = lo
            U = max(min_u_for_support(m, V, W), min_u0)
            if U > m * agreement:
                continue
            R_min_ceil = 2 * (U - 1) * (V - 1) ** 2 * (W - 1) + (r + 1) * (V - 1) + 1
            if R_min_ceil < BUDGET:
                item = (R_min_ceil, m, V, W, U, BUDGET - R_min_ceil)
                if best is None or item[0] < best[0]:
                    best = item
    return best


def build_output() -> Dict[str, Any]:
    status_stated = "CONDITIONAL_ON_BCHKS25_THEOREM_4_6_AS_STATED"
    exact_rho = (BCHKS_DEGREE_K, N)
    conservative_half = (1, 2)

    exact_safe = stated_result(
        "koalabear-bchks25-theorem46-displayed-reduced-rho-r604085",
        status_stated,
        604_085,
        *exact_rho,
    )
    exact_next = stated_result(
        "koalabear-bchks25-theorem46-displayed-reduced-rho-r604086-next-grid",
        status_stated,
        604_086,
        *exact_rho,
    )
    half_safe = stated_result(
        "koalabear-bchks25-theorem46-displayed-conservative-rho-half-r604084",
        status_stated,
        604_084,
        *conservative_half,
    )
    half_next = stated_result(
        "koalabear-bchks25-theorem46-displayed-conservative-rho-half-r604085-next-grid",
        status_stated,
        604_085,
        *conservative_half,
    )

    assert exact_safe["m"] == 146 and exact_safe["ceil_N_JMCA_lt_budget"]
    assert exact_next["m"] == 147 and not exact_next["ceil_N_JMCA_le_budget"]
    assert half_safe["m"] == 146 and half_safe["ceil_N_JMCA_lt_budget"]
    assert half_next["m"] == 147 and not half_next["ceil_N_JMCA_le_budget"]

    squeeze = verify_parametric_certificate(
        ParametricCertificate(
            label="koalabear-bchks25-parametric-list-mca-squeeze-v2-r611983",
            status="CONDITIONAL_ON_PARAMETRIC_LIST_MCA_LEMMA_V1",
            theorem_dependency="experimental/notes/audits/koalabear_bchks25_parametric_list_mca_lemma_v1.md",
            r=611_983,
            m=119,
            U_ceil_DX=176_735_111,
            V_ceil_DY=169,
            W_ceil_DZ=27_543,
            eps_num=1,
            eps_den=2**64,
        )
    )

    best_current = best_parametric_integer_cell_for_radius(611_983)
    best_next = best_parametric_integer_cell_for_radius(611_984)
    assert best_current is not None
    assert best_current[1:5] == (119, 169, 27_543, 176_735_111)
    assert best_current[0] == squeeze["useful_factor_bound"]["ceil_R_bound"]
    assert best_next is None

    return {
        "global_parameters": {
            "external_source": BCHKS25_SOURCE,
            "p": P_KOALABEAR,
            "extension_degree": EXTENSION_DEGREE,
            "q_line": Q_LINE,
            "n": N,
            "repo_dimension_K_degree_lt_K": REPO_DIMENSION_K,
            "BCHKS_degree_parameter_k_dimension_k_plus_1": BCHKS_DEGREE_K,
            "target_bits": TARGET_BITS,
            "target_denominator": TARGET_DENOMINATOR,
            "budget_floor((p^6-1)/2^128)": BUDGET,
        },
        "headline": {
            "claim": "Displayed BCHKS25 Theorem 4.6 JMCA safe edge",
            "status": status_stated,
            "safe_delta": f"604085/{N}",
            "safe_A": N - 604_085,
            "non_headline_appendix": "The parametric squeeze is separated and depends on the new bridge lemma in this packet.",
        },
        "stated_theorem_4_6_safe_edge_v1": {
            "status": status_stated,
            "exact_rho_endpoint": exact_safe,
            "exact_rho_next_grid_fails_displayed_bound": exact_next,
            "conservative_rho_half_endpoint": half_safe,
            "conservative_rho_half_next_grid_fails_displayed_bound": half_next,
        },
        "parametric_list_mca_squeeze_v2": {
            **squeeze,
            "optimized_integer_cell_search": {
                "family": "D_X=U-1+epsilon, D_Y=V-1+epsilon, D_Z=W-1+epsilon, epsilon->0+, with theorem admissibility constraints",
                "m_search_upper_bound": 602,
                "r_611983_best_cell": {
                    "ceil_R_bound": best_current[0],
                    "m": best_current[1],
                    "V_ceil_DY": best_current[2],
                    "W_ceil_DZ": best_current[3],
                    "U_ceil_DX": best_current[4],
                    "budget_margin": best_current[5],
                },
                "r_611984_has_no_budget_clearing_cell_in_this_family": best_next is None,
            },
        },
    }


def safe_certificate(output: Mapping[str, Any]) -> Dict[str, Any]:
    return {
        "global_parameters": output["global_parameters"],
        "headline": output["headline"],
        "certificate": output["stated_theorem_4_6_safe_edge_v1"],
    }


def squeeze_certificate(output: Mapping[str, Any]) -> Dict[str, Any]:
    return {
        "global_parameters": output["global_parameters"],
        "certificate": output["parametric_list_mca_squeeze_v2"],
        "non_claim": "This appendix is not a consequence of BCHKS25 Theorem 4.6 as displayed; it depends on the parametric list-MCA bridge lemma added in this packet.",
    }


def render_report(output: Mapping[str, Any]) -> str:
    safe = output["stated_theorem_4_6_safe_edge_v1"]["exact_rho_endpoint"]
    next_safe = output["stated_theorem_4_6_safe_edge_v1"]["exact_rho_next_grid_fails_displayed_bound"]
    half = output["stated_theorem_4_6_safe_edge_v1"]["conservative_rho_half_endpoint"]
    squeeze = output["parametric_list_mca_squeeze_v2"]
    lines = [
        "# KoalaBear BCHKS25 JMCA bounds v1 report",
        "",
        "## External source",
        "",
        f"- {BCHKS25_SOURCE['title']}.",
        f"- PDF: {BCHKS25_SOURCE['pdf_url']}.",
        f"- DOI: {BCHKS25_SOURCE['doi']}.",
        f"- PDF SHA256: `{BCHKS25_SOURCE['pdf_sha256']}`.",
        f"- Headline import: {BCHKS25_SOURCE['headline_import']} ({BCHKS25_SOURCE['headline_import_pages']}).",
        f"- Appendix dependency: {BCHKS25_SOURCE['parametric_appendix_dependency']} ({BCHKS25_SOURCE['parametric_appendix_dependency_pages']}).",
        "",
        "## Headline certificate",
        "",
        "Status: `CONDITIONAL_ON_BCHKS25_THEOREM_4_6_AS_STATED`",
        "",
        f"- Exact reduced-rate endpoint: `r={safe['r']}`, `A={safe['A']}`, `delta={safe['delta']}`.",
        f"- Displayed-Theorem-4.6 bound: `ceil_N_JMCA={safe['ceil_N_JMCA']}`.",
        f"- Budget: `{safe['budget']}`.",
        f"- Margin: `{safe['budget_minus_ceil_N_JMCA']}`.",
        f"- Next grid point under displayed formula: `r={next_safe['r']}`, `m={next_safe['m']}`, `ceil_N_JMCA={next_safe['ceil_N_JMCA']}`, which exceeds budget.",
        "",
        "## Conservative endpoint",
        "",
        f"- With `rho=1/2`: `r={half['r']}`, `A={half['A']}`, `ceil_N_JMCA={half['ceil_N_JMCA']}`.",
        "",
        "## Parametric appendix",
        "",
        "Status: `CONDITIONAL_ON_PARAMETRIC_LIST_MCA_LEMMA_V1`.",
        "",
        f"- Radius: `r={squeeze['r']}`, `A={squeeze['A']}`, `delta={squeeze['delta']}`.",
        f"- Parameters: `m={squeeze['m']}`, `D_X={squeeze['D_X_integer_plus_epsilon']}`, `D_Y={squeeze['D_Y_integer_plus_epsilon']}`, `D_Z={squeeze['D_Z_integer_plus_epsilon']}`.",
        f"- Interpolation slack: `{squeeze['interpolation_count']['n_vars_minus_n_eqs']}`.",
        f"- Root slack: `{squeeze['root_agreement_condition']['m_times_A_minus_D_X']}`.",
        f"- `ceil(R)={squeeze['useful_factor_bound']['ceil_R_bound']}` with margin `{squeeze['budget_minus_ceil_R_bound']}`.",
        f"- Next grid search: `r=611984` has no budget-clearing integer-ceiling cell in the stated optimized family: `{squeeze['optimized_integer_cell_search']['r_611984_has_no_budget_clearing_cell_in_this_family']}`.",
        "",
        "## Non-claims",
        "",
        "The PR headline does not depend on the parametric appendix. The appendix becomes a deployed safe certificate only if reviewers accept the new parametric list-MCA bridge lemma.",
        "",
    ]
    return "\n".join(lines)


def artifact_map(output: Mapping[str, Any]) -> Dict[Path, str]:
    return {
        SAFE_CERT_DIR / "certificate.json": stable_json(safe_certificate(output)),
        SQUEEZE_CERT_DIR / "certificate.json": stable_json(squeeze_certificate(output)),
        SHARED_CERT_DIR / "run_output.json": stable_json(output),
        REPORT_PATH: render_report(output),
    }


def write_artifacts(base_dir: Path, artifacts: Mapping[Path, str]) -> None:
    for rel_path, text in artifacts.items():
        path = base_dir / rel_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")


def check_artifacts(base_dir: Path, artifacts: Mapping[Path, str]) -> None:
    failures = []
    for rel_path, expected in artifacts.items():
        path = base_dir / rel_path
        if not path.exists():
            failures.append((rel_path, "missing", ""))
            continue
        expected_bytes = expected.encode("utf-8")
        actual_bytes = path.read_bytes()
        if actual_bytes != expected_bytes:
            actual = actual_bytes.decode("utf-8", errors="replace")
            diff = "".join(
                difflib.unified_diff(
                    actual.splitlines(keepends=True),
                    expected.splitlines(keepends=True),
                    fromfile=str(rel_path),
                    tofile=str(rel_path) + " (expected)",
                )
            )
            failures.append((rel_path, "mismatch", diff))
    if failures:
        for rel_path, kind, diff in failures:
            print(f"artifact check failed: {rel_path} ({kind})")
            if diff:
                print(diff)
        raise SystemExit(1)
    print(f"artifact check passed: {len(artifacts)} files")


def select_output(output: Mapping[str, Any], safe_edge: bool, squeeze: bool) -> Mapping[str, Any]:
    if safe_edge:
        return safe_certificate(output)
    if squeeze:
        return squeeze_certificate(output)
    return output


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="regenerate committed JSON/report artifacts")
    parser.add_argument("--check", action="store_true", help="byte-compare committed JSON/report artifacts")
    parser.add_argument(
        "--base-dir",
        type=Path,
        default=Path(__file__).resolve().parents[2],
        help="repository root containing experimental/ (default: inferred from script path)",
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--safe-edge", action="store_true", help="print only the displayed-Theorem-4.6 safe-edge certificate")
    mode.add_argument("--squeeze", action="store_true", help="print only the parametric squeeze appendix certificate")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output = build_output()
    artifacts = artifact_map(output)
    if args.write:
        write_artifacts(args.base_dir, artifacts)
    if args.check:
        check_artifacts(args.base_dir, artifacts)
    if (not args.write and not args.check) or args.safe_edge or args.squeeze:
        print(stable_json(select_output(output, args.safe_edge, args.squeeze)), end="")


if __name__ == "__main__":
    main()
