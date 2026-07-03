#!/usr/bin/env python3
"""Verify the arithmetic in cyclotomic_root_difference_germ.md."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path

import sympy as sp


REPO = Path(__file__).resolve().parents[2]
OUT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "cyclotomic-root-difference-germ"
    / "cyclotomic_root_difference_germ.json"
)


@dataclass(frozen=True)
class CheckResult:
    name: str
    status: str
    details: list[str]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def phi(n: int) -> int:
    return int(sp.totient(n))


def is_prime_power(n: int) -> tuple[bool, int | None]:
    factors = sp.factorint(n)
    if len(factors) == 1:
        return True, next(iter(factors))
    return False, None


def cyclotomic_one_value(m: int) -> int:
    require(m > 1, "M=1 gives the zero root difference")
    ok, prime = is_prime_power(m)
    return int(prime) if ok else 1


def root_difference_norm_formula(n: int, d: int) -> int:
    d %= n
    require(d != 0, "zero difference has norm zero")
    m = n // math.gcd(n, d)
    return cyclotomic_one_value(m) ** (phi(n) // phi(m))


def root_difference_norm_resultant(n: int, d: int) -> int:
    d %= n
    require(d != 0, "zero difference has norm zero")
    x = sp.Symbol("x")
    cyclo = sp.Poly(sp.cyclotomic_poly(n, x), x, domain=sp.ZZ)
    diff = sp.Poly(x**d - 1, x, domain=sp.ZZ)
    return abs(int(sp.resultant(diff.as_expr(), cyclo.as_expr(), x)))


def template_count(n: int) -> int:
    return n // 2


def canonical_unit_sign_template(d: int, n: int) -> int:
    d %= n
    require(d != 0, "zero difference has no nonzero template")
    return min(d, (-d) % n)


def check_norm_formula() -> tuple[CheckResult, list[dict[str, int | list[int]]]]:
    checked_rows = []
    by_order: dict[int, dict[str, set[int] | int]] = {}
    for n in [8, 9, 10, 12, 16, 18, 24, 32]:
        for d in range(1, n):
            formula = root_difference_norm_formula(n, d)
            resultant = root_difference_norm_resultant(n, d)
            require(formula == resultant, f"norm mismatch N={n}, d={d}")
            m = n // math.gcd(n, d)
            checked_rows.append(
                {
                    "quotient_order": n,
                    "d": d,
                    "root_order_M": m,
                    "phi_N": phi(n),
                    "phi_M": phi(m),
                    "norm_abs": formula,
                }
            )
            if n not in by_order:
                by_order[n] = {
                    "checked_d": 0,
                    "root_orders": set(),
                    "norms": set(),
                    "max_norm_bit_length": 0,
                }
            row = by_order[n]
            row["checked_d"] = int(row["checked_d"]) + 1
            row["root_orders"].add(m)  # type: ignore[union-attr]
            row["norms"].add(formula)  # type: ignore[union-attr]
            row["max_norm_bit_length"] = max(int(row["max_norm_bit_length"]), formula.bit_length())
    summary_rows = []
    for n in sorted(by_order):
        row = by_order[n]
        summary_rows.append(
            {
                "quotient_order": n,
                "checked_d": int(row["checked_d"]),
                "distinct_root_orders": sorted(row["root_orders"]),  # type: ignore[arg-type]
                "distinct_norms": sorted(row["norms"]),  # type: ignore[arg-type]
                "max_norm_bit_length": int(row["max_norm_bit_length"]),
            }
        )
    return (
        CheckResult(
            "root-difference norm formula",
            "PASS",
            [
                "checked exact resultants against Phi_M(1)^(phi(N)/phi(M))",
                "orders checked: 8,9,10,12,16,18,24,32",
                f"rows checked: {len(checked_rows)}",
            ],
        ),
        summary_rows,
    )


def check_unit_sign_templates() -> tuple[CheckResult, list[dict[str, int | list[int]]]]:
    rows: list[dict[str, int | list[int]]] = []
    for n in [8, 16, 32, 64]:
        templates = sorted({canonical_unit_sign_template(d, n) for d in range(1, n)})
        require(len(templates) == template_count(n), "unit/sign template count mismatch")
        require(templates == list(range(1, n // 2 + 1)), "unexpected template representatives")
        rows.append(
            {
                "quotient_order": n,
                "template_count": len(templates),
                "expected_template_count": n // 2,
                "template_prefix": templates[:8],
                "template_last": templates[-1],
            }
        )
    return (
        CheckResult(
            "unit/sign root templates",
            "PASS",
            ["verified floor(N/2) singleton templates for N=8,16,32,64"],
        ),
        rows,
    )


def check_power_two_odd_prime_avoidance() -> tuple[CheckResult, list[dict[str, int | bool]]]:
    rows: list[dict[str, int | bool]] = []
    odd_primes = [3, 5, 17, 257, 65537]
    for n in [8, 16, 32, 64, 128]:
        norms = {root_difference_norm_formula(n, d) for d in range(1, n)}
        require(all(norm > 0 and norm & (norm - 1) == 0 for norm in norms), "2-power norms should be powers of two")
        for p in odd_primes:
            rows.append(
                {
                    "quotient_order": n,
                    "prime": p,
                    "all_root_difference_norms_avoid_prime": all(norm % p != 0 for norm in norms),
                    "distinct_norm_count": len(norms),
                    "max_norm_bit_length": max(norm.bit_length() for norm in norms),
                }
            )
            require(rows[-1]["all_root_difference_norms_avoid_prime"], "odd prime divides a 2-power norm")
    return (
        CheckResult(
            "2-power odd-prime avoidance",
            "PASS",
            ["for N a power of two, all singleton root-difference norms are powers of two"],
        ),
        rows,
    )


def build_result() -> dict:
    norm_check, norm_rows = check_norm_formula()
    template_check, template_rows = check_unit_sign_templates()
    odd_check, odd_rows = check_power_two_odd_prime_avoidance()
    script = Path(__file__).resolve()
    return {
        "status": "PROVED_CYCLOTOMIC_ROOT_DIFFERENCE_GERM",
        "supports": ["generator_economy", "cluster_certificates"],
        "object": "single-root quotient e_1 difference certification primitive",
        "script": str(script.relative_to(REPO)),
        "script_sha256": file_sha256(script),
        "checks": [asdict(c) for c in [norm_check, template_check, odd_check]],
        "norm_formula_summary_rows": norm_rows,
        "unit_sign_template_rows": template_rows,
        "power_two_odd_prime_rows": odd_rows,
        "non_claims": [
            "does not construct ell-sum generator-economy designs",
            "does not prove full value-set lower bounds",
            "does not replace row-specific certificates for non-singleton templates",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true", help="write the JSON certificate")
    parser.add_argument("--check", default=str(OUT), help="certificate path to replay")
    args = parser.parse_args()

    result = build_result()
    if args.emit:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        print(f"wrote {OUT.relative_to(REPO)}")
    else:
        expected = json.loads(Path(args.check).read_text())
        require(expected == result, "certificate does not match verifier output; rerun with --emit")
        print(result["status"])
        for check in result["checks"]:
            print(f"  {check['name']}: {check['status']}")


if __name__ == "__main__":
    main()
