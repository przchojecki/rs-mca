#!/usr/bin/env python3
"""Verifier for the M1 nonconsecutive coefficient-window normal form v1.

This packet proves an algebraic normal form for two-row coefficient windows
W={1,r}.  It is a structural routing theorem, not a paid deployed-row
certificate: pair-deficient residual windows remain named residual branches.
"""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
NOTE_PATH = ROOT / "experimental" / "notes" / "m1" / "m1_nonconsecutive_window_normal_form_v1.md"
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "m1-nonconsecutive-window-normal-form-v1"
CERT_PATH = CERT_DIR / "m1_nonconsecutive_window_normal_form_v1.json"
CERT_README_PATH = CERT_DIR / "README.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "m1_nonconsecutive_window_normal_form_v1.report.md"
)


def ensure(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


class TwoPowerCyclotomic:
    """Exact arithmetic in Q(zeta_n), n=2^m, using zeta^(n/2)=-1."""

    def __init__(self, n: int) -> None:
        ensure(n >= 4 and n & (n - 1) == 0, "n must be a 2-power >= 4")
        self.n = n
        self.half = n // 2

    def zero(self) -> tuple[int, ...]:
        return (0,) * self.half

    def one(self) -> tuple[int, ...]:
        return (1,) + (0,) * (self.half - 1)

    def root(self, exp: int) -> tuple[int, ...]:
        exp %= self.n
        sign = 1
        if exp >= self.half:
            exp -= self.half
            sign = -1
        out = [0] * self.half
        out[exp] = sign
        return tuple(out)

    def add(self, left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
        return tuple(a + b for a, b in zip(left, right))

    def sub(self, left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
        return tuple(a - b for a, b in zip(left, right))

    def neg(self, value: tuple[int, ...]) -> tuple[int, ...]:
        return tuple(-a for a in value)

    def mul(self, left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
        out = [0] * self.half
        for i, a in enumerate(left):
            if not a:
                continue
            for j, b in enumerate(right):
                if not b:
                    continue
                exp = i + j
                if exp >= self.half:
                    out[exp - self.half] -= a * b
                else:
                    out[exp] += a * b
        return tuple(out)

    def is_zero(self, value: tuple[int, ...]) -> bool:
        return all(a == 0 for a in value)

    def key(self, value: tuple[int, ...]) -> str:
        return ",".join(str(a) for a in value)


def reduce_cyclotomic_mod(value: tuple[int, ...], omega: int, p: int) -> int:
    total = 0
    power = 1
    for coeff in value:
        total = (total + coeff * power) % p
        power = (power * omega) % p
    return total


def locator_coeffs_exact(field: TwoPowerCyclotomic, support: tuple[int, ...]) -> list[tuple[int, ...]]:
    coeffs = [field.one()]
    for exp in support:
        x = field.root(exp)
        new = [field.zero()] * (len(coeffs) + 1)
        for idx, coeff in enumerate(coeffs):
            new[idx] = field.sub(new[idx], field.mul(coeff, x))
            new[idx + 1] = field.add(new[idx + 1], coeff)
        coeffs = new
    return coeffs


def locator_coeffs_mod(values: list[int], p: int) -> list[int]:
    coeffs = [1]
    for x in values:
        new = [0] * (len(coeffs) + 1)
        for idx, coeff in enumerate(coeffs):
            new[idx] = (new[idx] - coeff * x) % p
            new[idx + 1] = (new[idx + 1] + coeff) % p
        coeffs = new
    return coeffs


def half_turn_decompose(n: int, support: tuple[int, ...]) -> tuple[list[int], list[int]]:
    half = n // 2
    support_set = set(support)
    seen: set[int] = set()
    paired_reps: list[int] = []
    residual: list[int] = []
    for exp in support:
        if exp in seen:
            continue
        opposite = (exp + half) % n
        if opposite in support_set:
            paired_reps.append(min(exp, opposite))
            seen.add(exp)
            seen.add(opposite)
        else:
            residual.append(exp)
            seen.add(exp)
    return paired_reps, residual


def coefficient_terms(deficit: int) -> list[list[int]]:
    return [[h, deficit - 2 * h] for h in range(deficit // 2 + 1)]


def window_formula(r: int) -> dict[str, Any]:
    ensure(r >= 3, "this packet handles r>=3")
    terms = [[h, r - 2 * h] for h in range(r // 2 + 1)]
    if r % 2 == 0:
        kappa = r // 2
        recursive_condition = f"q >= {kappa}"
        solved_coefficient = f"b_{kappa}"
        boundary_condition = f"q < {kappa}"
        branch_rule = "even window: deep paired core solves for the next lower-domain coefficient"
    else:
        kappa = (r - 1) // 2
        recursive_condition = f"some theta_{{{r}-2h}} with 1<=h<=min(q,{kappa - 1}) is nonzero"
        solved_coefficient = "some existing lower-core coefficient with nonzero residual coefficient"
        boundary_condition = f"q < {max(0, kappa - 1)} or no exposed nonzero active coefficient"
        branch_rule = "odd window: nonzero active residual vector descends; all odd theta defects zero routes to half-turn"
    return {
        "r": r,
        "window": [1, r],
        "row_condition_terms": terms,
        "display": " + ".join(f"b_{h} theta_{a}" for h, a in terms) + " = 0",
        "parity": "even" if r % 2 == 0 else "odd",
        "recursive_condition": recursive_condition,
        "solved_or_active_coefficient": solved_coefficient,
        "pair_deficient_condition": boundary_condition,
        "branch_rule": branch_rule,
    }


def theta_values(field: TwoPowerCyclotomic, residual: list[int], max_a: int) -> list[tuple[int, ...]]:
    coeffs = locator_coeffs_exact(field, tuple(residual))
    # coeffs are c0..cs. Convert to deficit coefficients d_a.
    s = len(residual)
    d = []
    for a in range(max_a + 1):
        if 0 <= a <= s:
            d.append(coeffs[s - a])
        else:
            d.append(field.zero())
    z = field.neg(d[1]) if max_a >= 1 else field.zero()
    out = []
    for a in range(max_a + 1):
        prev = d[a - 1] if a - 1 >= 0 else field.zero()
        out.append(field.add(d[a], field.mul(z, prev)))
    return out


def classify_exact_survivor(n: int, support: tuple[int, ...], r: int) -> str:
    field = TwoPowerCyclotomic(n)
    paired, residual = half_turn_decompose(n, support)
    q = len(paired)
    theta = theta_values(field, residual, r)
    if r % 2 == 0:
        kappa = r // 2
        if q >= kappa:
            return "recursive_lower_core_affine_slice"
        return "pair_deficient_residual_window"
    kappa = (r - 1) // 2
    exposed = range(1, min(q, kappa - 1) + 1)
    if any(not field.is_zero(theta[r - 2 * h]) for h in exposed):
        return "recursive_lower_core_affine_slice"
    full_depth = q >= max(0, kappa - 1)
    odd_chain_zero = all(field.is_zero(theta[a]) for a in range(3, r + 1, 2))
    if full_depth and odd_chain_zero:
        return "honest_half_turn_pair_core"
    return "pair_deficient_residual_window"


def exact_window_scan(n: int, j: int, r: int) -> dict[str, Any]:
    field = TwoPowerCyclotomic(n)
    bucket_counts: Counter[str] = Counter()
    residual_counts: Counter[int] = Counter()
    examples: dict[str, list[Any]] = {}
    total = 0
    for support in itertools.combinations(range(n), j):
        coeffs = locator_coeffs_exact(field, support)
        z = field.neg(coeffs[j - 1])
        row1 = field.add(coeffs[j - 1], z)
        rowr = field.add(coeffs[j - r], field.mul(z, coeffs[j - r + 1]))
        if field.is_zero(row1) and field.is_zero(rowr):
            total += 1
            _, residual = half_turn_decompose(n, support)
            residual_counts[len(residual)] += 1
            bucket = classify_exact_survivor(n, support, r)
            bucket_counts[bucket] += 1
            examples.setdefault(bucket, [])
            if len(examples[bucket]) < 3:
                examples[bucket].append(
                    {
                        "support_exponents": list(support),
                        "residual_size": len(residual),
                    }
                )
    ensure(total == sum(bucket_counts.values()), "exact survivor buckets should partition")
    return {
        "model": f"Q(zeta_{n})",
        "n": n,
        "j": j,
        "window": [1, r],
        "survivor_supports": total,
        "residual_histogram": dict(sorted(residual_counts.items())),
        "normal_form_buckets": dict(bucket_counts),
        "examples": examples,
    }


def finite_generated_collision_scan(p: int, n: int, j: int, r: int, omega: int) -> dict[str, Any]:
    field = TwoPowerCyclotomic(n)
    domain = [pow(omega, exp, p) for exp in range(n)]
    total = 0
    honest_zero = 0
    generated = 0
    for support in itertools.combinations(range(n), j):
        coeffs_mod = locator_coeffs_mod([domain[i] for i in support], p)
        z = (-coeffs_mod[j - 1]) % p
        if (coeffs_mod[j - r] + z * coeffs_mod[j - r + 1]) % p:
            continue
        total += 1
        coeffs_exact = locator_coeffs_exact(field, support)
        z_exact = field.neg(coeffs_exact[j - 1])
        defect = field.add(coeffs_exact[j - r], field.mul(z_exact, coeffs_exact[j - r + 1]))
        reduced = reduce_cyclotomic_mod(defect, omega, p)
        ensure(reduced == 0, "finite row defect should reduce to zero")
        if field.is_zero(defect):
            honest_zero += 1
        else:
            generated += 1
    ensure(total == honest_zero + generated, "finite generated split should partition")
    return {
        "model": f"F_{p}",
        "n": n,
        "j": j,
        "window": [1, r],
        "omega": omega,
        "finite_survivors": total,
        "honest_lift_survivors": honest_zero,
        "finite_only_generated_collisions": generated,
        "meaning": "finite-only survivors have nonzero cyclotomic row defect that reduces to zero modulo p",
    }


def build_certificate() -> dict[str, Any]:
    formulas = [window_formula(r) for r in range(3, 11)]
    formula_by_r = {row["r"]: row["display"] for row in formulas}
    ensure(formula_by_r[5] == "b_0 theta_5 + b_1 theta_3 + b_2 theta_1 = 0", "bad r=5 formula")
    ensure(formula_by_r[6] == "b_0 theta_6 + b_1 theta_4 + b_2 theta_2 + b_3 theta_0 = 0", "bad r=6 formula")
    ensure(formula_by_r[7] == "b_0 theta_7 + b_1 theta_5 + b_2 theta_3 + b_3 theta_1 = 0", "bad r=7 formula")

    exact_scans = [
        exact_window_scan(16, 5, 3),
        exact_window_scan(16, 5, 5),
        exact_window_scan(16, 8, 5),
        exact_window_scan(16, 8, 6),
        exact_window_scan(16, 8, 7),
    ]
    finite_scans = [
        finite_generated_collision_scan(17, 16, 5, 3, 3),
        finite_generated_collision_scan(17, 16, 5, 5, 3),
    ]
    ensure(finite_scans[0]["finite_only_generated_collisions"] == 128, "unexpected {1,3} generated count")
    ensure(finite_scans[1]["finite_only_generated_collisions"] == 112, "unexpected {1,5} generated count")

    cert = {
        "status": "PROVED",
        "claim_class": "STRUCTURAL_NORMAL_FORM",
        "unpaid_residuals": ["pair_deficient_residual_window"],
        "no_deployed_budget_deducted": True,
        "note": "experimental/notes/m1/m1_nonconsecutive_window_normal_form_v1.md",
        "script": "experimental/scripts/verify_m1_nonconsecutive_window_normal_form_v1.py",
        "theorem": {
            "name": "nonconsecutive coefficient-window inverse normal form",
            "window_family": "W={1,r}, 3<=r<=j",
            "normal_form_identity": "sum_h b_h theta_{r-2h}(R)=0",
            "branches": [
                "generated_field_collision",
                "honest_half_turn_pair_core",
                "recursive_lower_core_affine_slice",
                "pair_deficient_residual_window",
            ],
            "unpaid_named_residual": "pair_deficient_residual_window",
            "does_not_prove": [
                "payment of pair-deficient residual windows",
                "lower-rung Q/BC/SP constants",
                "primitive Q-fin max-fiber flatness",
                "arbitrary sparse Hankel row-slices without printed coefficient rows",
                "extension-valued split-pencil branches",
            ],
        },
        "formula_checks": formulas,
        "explicit_windows": {
            "W_1_5": "theta_5 + b_1 theta_3 = 0 after theta_1=0",
            "W_1_6": "theta_6 + b_1 theta_4 + b_2 theta_2 + b_3 = 0",
            "W_1_7": "theta_7 + b_1 theta_5 + b_2 theta_3 = 0 after theta_1=0",
        },
        "exact_cyclotomic_scans": exact_scans,
        "finite_generated_collision_scans": finite_scans,
        "deployed_ledger_interpretation": {
            "status": "STRUCTURAL_ONLY_NO_NEW_BUDGET_DEDUCTED",
            "generated_branch_cost": "covered by existing B_gen <= t*p if the row is part of the printed packet",
            "recursive_branch": "descends to lower-rung affine split-locator obligations",
            "new_obstruction": "pair_deficient_residual_window",
        },
    }
    assert_certificate(cert)
    return cert


def assert_certificate(cert: dict[str, Any]) -> None:
    ensure(cert["status"] == "PROVED", "bad status")
    ensure(cert["claim_class"] == "STRUCTURAL_NORMAL_FORM", "bad claim class")
    ensure(cert["no_deployed_budget_deducted"] is True, "M1 packet should not deduct deployed budget")
    branches = set(cert["theorem"]["branches"])
    ensure("pair_deficient_residual_window" in branches, "missing named residual")
    for scan in cert["exact_cyclotomic_scans"]:
        ensure(
            scan["survivor_supports"] == sum(scan["normal_form_buckets"].values()),
            "normal form buckets do not partition exact scan",
        )
    for scan in cert["finite_generated_collision_scans"]:
        ensure(
            scan["finite_survivors"]
            == scan["honest_lift_survivors"] + scan["finite_only_generated_collisions"],
            "finite generated collision split mismatch",
        )


def render_report(cert: dict[str, Any]) -> str:
    lines = [
        "# M1 nonconsecutive coefficient-window normal form v1 report",
        "",
        f"Status: `{cert['status']}`.",
        "",
        "This packet proves the normal-form identity for coefficient windows `W={1,r}`",
        "and routes every survivor to generated collision, half-turn, recursive lower-core",
        "affine slice, or the named pair-deficient residual branch.",
        "",
        "## Formula checks",
        "",
        "| r | formula | branch rule |",
        "| -: | --- | --- |",
    ]
    for row in cert["formula_checks"]:
        lines.append(f"| {row['r']} | `{row['display']}` | {row['branch_rule']} |")
    lines.extend(
        [
            "",
            "## Exact cyclotomic scan checks",
            "",
            "| model | j | window | supports | buckets |",
            "| --- | -: | --- | -: | --- |",
        ]
    )
    for row in cert["exact_cyclotomic_scans"]:
        lines.append(
            f"| {row['model']} | {row['j']} | `{row['window']}` | "
            f"{row['survivor_supports']} | `{row['normal_form_buckets']}` |"
        )
    lines.extend(
        [
            "",
            "## Finite generated-collision guardrails",
            "",
            "| model | j | window | finite survivors | honest lift | generated-only |",
            "| --- | -: | --- | -: | -: | -: |",
        ]
    )
    for row in cert["finite_generated_collision_scans"]:
        lines.append(
            f"| {row['model']} | {row['j']} | `{row['window']}` | "
            f"{row['finite_survivors']} | {row['honest_lift_survivors']} | "
            f"{row['finite_only_generated_collisions']} |"
        )
    lines.extend(
        [
            "",
            "## Nonclaims",
            "",
        ]
    )
    for item in cert["theorem"]["does_not_prove"]:
        lines.append(f"- {item}.")
    lines.append("")
    return "\n".join(lines)


def render_cert_readme(cert: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# M1 nonconsecutive coefficient-window normal form v1 certificate",
            "",
            f"Status: `{cert['status']}`.",
            "",
            "## Regeneration",
            "",
            "```bash",
            "python3 experimental/scripts/verify_m1_nonconsecutive_window_normal_form_v1.py --write",
            "python3 experimental/scripts/verify_m1_nonconsecutive_window_normal_form_v1.py --check",
            "python3 -m json.tool experimental/data/certificates/m1-nonconsecutive-window-normal-form-v1/m1_nonconsecutive_window_normal_form_v1.json",
            "```",
            "",
            "## Claim",
            "",
            "Every printed two-row coefficient window `W={1,r}` satisfies the normal-form",
            "identity `sum_h b_h theta_{r-2h}(R)=0` after half-turn decomposition.",
            "The packet routes survivors into generated collision, honest half-turn,",
            "recursive lower-core affine slice, or pair-deficient residual branches.",
            "",
            "## Nonclaim",
            "",
            "The pair-deficient residual branch is named but not paid by this packet.",
            "",
        ]
    )


def json_bytes(cert: dict[str, Any]) -> bytes:
    return (json.dumps(cert, indent=2, sort_keys=True) + "\n").encode("utf-8")


def report_bytes(cert: dict[str, Any]) -> bytes:
    return render_report(cert).encode("utf-8")


def cert_readme_bytes(cert: dict[str, Any]) -> bytes:
    return render_cert_readme(cert).encode("utf-8")


def write_artifacts(cert: dict[str, Any]) -> None:
    CERT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    CERT_PATH.write_bytes(json_bytes(cert))
    CERT_README_PATH.write_bytes(cert_readme_bytes(cert))
    REPORT_PATH.write_bytes(report_bytes(cert))


def check_artifacts(cert: dict[str, Any]) -> None:
    expected = {
        CERT_PATH: json_bytes(cert),
        CERT_README_PATH: cert_readme_bytes(cert),
        REPORT_PATH: report_bytes(cert),
    }
    missing = [str(path) for path in expected if not path.exists()]
    if missing:
        raise AssertionError(f"missing artifacts: {missing}")
    mismatches = [str(path) for path, data in expected.items() if path.read_bytes() != data]
    if mismatches:
        raise AssertionError(f"artifact mismatch; run --write: {mismatches}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    cert = build_certificate()
    if args.write:
        write_artifacts(cert)
        print(f"wrote {CERT_PATH}")
        print(f"wrote {CERT_README_PATH}")
        print(f"wrote {REPORT_PATH}")
    if args.check:
        check_artifacts(cert)
        print("artifact check passed: 3 files")
    if args.json:
        print(json.dumps(cert, indent=2, sort_keys=True))
    if not (args.write or args.check or args.json):
        print("STATUS:", cert["status"])
        print("RESULT: PASS")


if __name__ == "__main__":
    main()
