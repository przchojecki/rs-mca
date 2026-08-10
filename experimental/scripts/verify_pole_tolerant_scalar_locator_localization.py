#!/usr/bin/env python3
"""Replay finite seams for the pole-tolerant scalar-locator theorems.

The universal results are proved in the accompanying note.  This stdlib-only
checker binds the source definition, deployed constants, exact finite-field
fixtures, and explicit failure modes.  It claims no ledger payment.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
import sys
from pathlib import Path
from typing import Iterable, Sequence


CERT_REL = Path(
    "experimental/data/certificates/"
    "pole-tolerant-scalar-locator-localization-v1/certificate.json"
)
SCHEMA = "pole-tolerant-scalar-locator-localization-v1"
EXPECTED_SOURCE_PINS = {
    "experimental/grande_finale.tex": "6b21d6ea937a8a9f85fc7ade6032d73efd4c7222"
}
EXPECTED_THEOREMS = {
    "POLE_TOLERANT_EXCLUSIVE_LOCALIZATION",
    "EXACT_LOCATOR_COMMON_POLE_CANCELLATION",
}
EXPECTED_NONCLAIMS = {
    "NO_ACTIVE_V4_FIRST_MATCH_ADAPTER",
    "NO_CAP25_OR_CA_IMPORT",
    "NO_DEPLOYED_LEDGER_PAYMENT",
    "NO_ENDPOINT_CLOSURE",
    "NO_OFFICIAL_SCORE_MOVEMENT",
    "NO_PRESERVATION_OF_MCA_NONTRIVIALITY_AFTER_CANCELLATION",
}


class VerificationError(RuntimeError):
    pass


CHECKS = 0


def require(condition: bool, message: str) -> None:
    global CHECKS
    CHECKS += 1
    if not condition:
        raise VerificationError(message)


def git_blob_sha(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def verify_manifest(certificate_dir: Path) -> None:
    manifest = certificate_dir / "SHA256SUMS.txt"
    require(manifest.is_file(), "missing SHA256SUMS.txt")
    entries = {}
    for line in manifest.read_text(encoding="utf-8").splitlines():
        digest, relative = line.split("  ", 1)
        entries[relative] = digest
    require(
        set(entries)
        == {
            "README.md",
            "certificate.json",
            "recorded_output.txt",
            "../../../notes/m2/pole_tolerant_scalar_locator_localization.md",
            "../../../scripts/verify_pole_tolerant_scalar_locator_localization.py",
        },
        "manifest members",
    )
    for relative, expected in entries.items():
        path = (certificate_dir / relative).resolve()
        require(path.is_file(), f"missing manifest member: {relative}")
        require(hashlib.sha256(path.read_bytes()).hexdigest() == expected, f"manifest hash: {relative}")


def poly_trim(a: Sequence[int], p: int) -> tuple[int, ...]:
    out = [x % p for x in a]
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return tuple(out or [0])


def poly_add(a: Sequence[int], b: Sequence[int], p: int) -> tuple[int, ...]:
    length = max(len(a), len(b))
    return poly_trim(
        [
            ((a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)) % p
            for i in range(length)
        ],
        p,
    )


def poly_scale(a: Sequence[int], scalar: int, p: int) -> tuple[int, ...]:
    return poly_trim([(scalar * x) % p for x in a], p)


def poly_mul(a: Sequence[int], b: Sequence[int], p: int) -> tuple[int, ...]:
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] = (out[i + j] + x * y) % p
    return poly_trim(out, p)


def poly_eval(a: Sequence[int], x: int, p: int) -> int:
    value = 0
    for coefficient in reversed(a):
        value = (value * x + coefficient) % p
    return value


def poly_degree(a: Sequence[int], p: int) -> int:
    trimmed = poly_trim(a, p)
    return -1 if trimmed == (0,) else len(trimmed) - 1


def poly_from_roots(roots: Iterable[int], p: int) -> tuple[int, ...]:
    out: tuple[int, ...] = (1,)
    for root in roots:
        out = poly_mul(out, ((-root) % p, 1), p)
    return out


def poly_divmod(
    a: Sequence[int], b: Sequence[int], p: int
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    dividend = list(poly_trim(a, p))
    divisor = poly_trim(b, p)
    require(divisor != (0,), "polynomial division by zero")
    if len(dividend) < len(divisor):
        return (0,), poly_trim(dividend, p)
    quotient = [0] * (len(dividend) - len(divisor) + 1)
    inverse = pow(divisor[-1], -1, p)
    while len(dividend) >= len(divisor) and dividend != [0]:
        shift = len(dividend) - len(divisor)
        coefficient = dividend[-1] * inverse % p
        quotient[shift] = coefficient
        for index, value in enumerate(divisor):
            dividend[shift + index] = (
                dividend[shift + index] - coefficient * value
            ) % p
        while len(dividend) > 1 and dividend[-1] == 0:
            dividend.pop()
    return poly_trim(quotient, p), poly_trim(dividend, p)


def poly_exact_div(a: Sequence[int], b: Sequence[int], p: int) -> tuple[int, ...]:
    quotient, remainder = poly_divmod(a, b, p)
    require(remainder == (0,), f"non-exact division: {remainder}")
    return quotient


def values_extend_to_degree_lt(
    xs: Sequence[int], ys: Sequence[int], k: int, p: int
) -> bool:
    matrix = [[pow(x, j, p) for j in range(k)] + [y % p] for x, y in zip(xs, ys)]
    row = 0
    for column in range(k):
        pivot = next(
            (i for i in range(row, len(matrix)) if matrix[i][column] % p),
            None,
        )
        if pivot is None:
            continue
        matrix[row], matrix[pivot] = matrix[pivot], matrix[row]
        inverse = pow(matrix[row][column], -1, p)
        matrix[row] = [(value * inverse) % p for value in matrix[row]]
        for index in range(len(matrix)):
            if index == row or matrix[index][column] % p == 0:
                continue
            factor = matrix[index][column] % p
            matrix[index] = [
                (matrix[index][j] - factor * matrix[row][j]) % p
                for j in range(k + 1)
            ]
        row += 1
    return not any(
        all(value % p == 0 for value in equation[:k])
        and equation[-1] % p != 0
        for equation in matrix
    )


def scalar(example: dict, gamma: int) -> int:
    return (example["c0"] + example["c1"] * gamma) % example["p"]


def coincidence_core(example: dict) -> tuple[int, ...]:
    p = example["p"]
    return tuple(
        x
        for x in example["D"]
        if poly_eval(example["A"], x, p)
        == poly_eval(example["Q"], x, p) * example["r0"][x] % p
        and poly_eval(example["B"], x, p)
        == poly_eval(example["Q"], x, p) * example["r1"][x] % p
    )


def support_is_nontrivial(example: dict, support: Sequence[int]) -> bool:
    p = example["p"]
    k = example["k"]
    r0_ok = values_extend_to_degree_lt(
        support, [example["r0"][x] for x in support], k, p
    )
    r1_ok = values_extend_to_degree_lt(
        support, [example["r1"][x] for x in support], k, p
    )
    return not (r0_ok and r1_ok)


def validate_example(example: dict, *, exact_locators: bool) -> None:
    p = example["p"]
    require(len(set(example["D"])) == len(example["D"]), "distinct domain")
    require(example["Q"] != (0,), "nonzero denominator")
    require((example["c0"] % p, example["c1"] % p) != (0, 0), "nonzero scalar pair")
    slopes = [item["gamma"] % p for item in example["items"]]
    require(len(set(slopes)) == len(slopes), "distinct slopes")
    for item in example["items"]:
        support = tuple(item["S"])
        gamma = item["gamma"] % p
        require(len(support) == example["m"], "exact support size")
        require(set(support).issubset(set(example["D"])), "support in domain")
        require(poly_degree(item["h"], p) < example["k"], "degree bound")
        if exact_locators:
            require(item["lam"] == poly_from_roots(support, p), "exact locator")
        else:
            require(
                all(poly_eval(item["lam"], x, p) == 0 for x in support),
                "locator vanishing",
            )
        left = poly_add(
            poly_mul(example["Q"], item["h"], p),
            poly_scale(item["lam"], scalar(example, gamma), p),
            p,
        )
        right = poly_add(example["A"], poly_scale(example["B"], gamma, p), p)
        require(left == right, "certificate identity")
        require(
            all(
                poly_eval(item["h"], x, p)
                == (example["r0"][x] + gamma * example["r1"][x]) % p
                for x in support
            ),
            "support agreement",
        )
        require(support_is_nontrivial(example, support), "support-wise nontriviality")


def check_localization(example: dict) -> None:
    core = set(coincidence_core(example))
    for x in example["D"]:
        if x not in core:
            require(
                sum(x in item["S"] for item in example["items"]) <= 1,
                "exclusive localization",
            )


def cancel_exact_locators(example: dict) -> None:
    validate_example(example, exact_locators=True)
    p = example["p"]
    core = set(coincidence_core(example))
    poles = tuple(x for x in core if poly_eval(example["Q"], x, p) == 0)
    live = [item for item in example["items"] if scalar(example, item["gamma"]) != 0]
    require(len(example["items"]) - len(live) <= 1, "one zero-scalar slope")
    require(bool(live), "nonempty reduced family")
    for item in live:
        require(set(poles).issubset(set(item["S"])), "common poles lie in support")
    locator = poly_from_roots(poles, p)
    qp = poly_exact_div(example["Q"], locator, p)
    ap = poly_exact_div(example["A"], locator, p)
    bp = poly_exact_div(example["B"], locator, p)
    reduced_domain = tuple(x for x in example["D"] if x not in set(poles))
    for item in live:
        reduced_support = tuple(x for x in item["S"] if x not in set(poles))
        reduced_locator = poly_exact_div(item["lam"], locator, p)
        require(
            reduced_locator == poly_from_roots(reduced_support, p),
            "reduced exact locator",
        )
        left = poly_add(
            poly_mul(qp, item["h"], p),
            poly_scale(reduced_locator, scalar(example, item["gamma"]), p),
            p,
        )
        right = poly_add(ap, poly_scale(bp, item["gamma"], p), p)
        require(left == right, "divided certificate")
    reduced_core = {
        x
        for x in reduced_domain
        if poly_eval(ap, x, p) == poly_eval(qp, x, p) * example["r0"][x] % p
        and poly_eval(bp, x, p) == poly_eval(qp, x, p) * example["r1"][x] % p
    }
    require(reduced_core == core - set(poles), "reduced core equality")
    require(
        all(poly_eval(qp, x, p) != 0 for x in reduced_core),
        "root-free reduced core",
    )


def build_exact_example() -> dict:
    p = 17
    q = poly_from_roots((0, 1), p)
    s0 = (0, 1, 2, 3)
    s1 = (0, 1, 4, 5)
    h0 = poly_scale(poly_from_roots((2, 3), p), -1, p)
    h1 = poly_scale(poly_from_roots((4, 5), p), -1, p)
    return {
        "p": p,
        "D": (0, 1, 2, 3, 4, 5),
        "k": 3,
        "m": 4,
        "r0": {0: 11, 1: 15, 2: 0, 3: 0, 4: 0, 5: 1},
        "r1": {0: 3, 1: 7, 2: 0, 3: 0, 4: 0, 5: 16},
        "Q": q,
        "A": (0,),
        "B": (0,),
        "c0": 1,
        "c1": 0,
        "items": [
            {"gamma": 0, "S": s0, "lam": poly_from_roots(s0, p), "h": h0},
            {"gamma": 1, "S": s1, "lam": poly_from_roots(s1, p), "h": h1},
        ],
    }


def build_zero_scalar_example() -> dict:
    p = 17
    support0 = (2, 3, 4)
    support1 = (0, 1, 2)
    return {
        "p": p,
        "D": (0, 1, 2, 3, 4),
        "k": 2,
        "m": 3,
        "r0": {0: 0, 1: 1, 2: 0, 3: 0, 4: 0},
        "r1": {0: 2, 1: 0, 2: 0, 3: 0, 4: 1},
        "Q": poly_from_roots((0, 1), p),
        "A": (0,),
        "B": (0,),
        "c0": 0,
        "c1": 1,
        "items": [
            {
                "gamma": 0,
                "S": support0,
                "lam": poly_from_roots(support0, p),
                "h": (0,),
            },
            {
                "gamma": 1,
                "S": support1,
                "lam": poly_from_roots(support1, p),
                "h": (2, 16),
            },
        ],
    }


def check_extra_root_failure() -> None:
    p = 17
    support = (0, 1, 2)
    weak_locator = poly_from_roots((0, 1, 2, 3), p)
    require(all(poly_eval(weak_locator, x, p) == 0 for x in support), "weak locator")
    require(weak_locator != poly_from_roots(support, p), "extra root detected")
    require(3 not in support and poly_eval(weak_locator, 3, p) == 0, "false support root")


def polynomial_words(p: int, points: Sequence[int], k: int) -> set[tuple[int, ...]]:
    return {
        tuple(poly_eval(coefficients, x, p) for x in points)
        for coefficients in itertools.product(range(p), repeat=k)
    }


def check_exact_boundary() -> None:
    p = 3
    points = (0, 1, 2)
    code = polynomial_words(p, points, 2)
    maximum = 0
    for r0 in itertools.product(range(p), repeat=len(points)):
        for r1 in itertools.product(range(p), repeat=len(points)):
            simultaneous = r0 in code and r1 in code
            bad = 0
            for gamma in range(p):
                word = tuple((r0[i] + gamma * r1[i]) % p for i in range(len(points)))
                bad += int(word in code and not simultaneous)
            maximum = max(maximum, bad)
    require(maximum == 1, "exact g=m full-support numerator")


def validate_certificate(data: dict, repo_root: Path, *, check_sources: bool) -> None:
    require(data.get("schema") == SCHEMA, "schema")
    require(set(data.get("theorems", [])) == EXPECTED_THEOREMS, "theorem set")
    require(set(data.get("nonclaims", [])) == EXPECTED_NONCLAIMS, "nonclaims")
    require(data.get("source_pins") == EXPECTED_SOURCE_PINS, "source pins")
    require(data["audit"]["verdict"] == "ACCEPT_NARROWED", "audit verdict")
    require(data["author_repair"]["verdict"] == "REPAIR", "repair verdict")
    expected_rows = {
        "koalabear_mca": (2_097_152, 1_048_576, 1_116_048, 274_980_728_111_395_087),
        "mersenne31_mca": (2_097_152, 1_048_576, 1_116_024, 16_777_215),
    }
    for name, expected in expected_rows.items():
        row = data["deployed_rows"][name]
        require(
            (row["n"], row["k"], row["m"], row["budget"]) == expected,
            f"row constants: {name}",
        )
        require(row["n"] >= row["m"] > row["k"], f"row order: {name}")
    if check_sources:
        for relative, expected_sha in EXPECTED_SOURCE_PINS.items():
            path = repo_root / relative
            require(path.is_file(), f"missing source: {relative}")
            require(git_blob_sha(path.read_bytes()) == expected_sha, f"source pin: {relative}")


def load_certificate(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8")
    data = json.loads(raw)
    require(raw == json.dumps(data, indent=2, sort_keys=True) + "\n", "canonical JSON")
    return data


def run_check(repo_root: Path, certificate: Path) -> None:
    data = load_certificate(certificate)
    validate_certificate(data, repo_root, check_sources=True)
    verify_manifest(certificate.parent)
    print("PASS certificate, manifest, source pin, audit scope, and nonclaims")
    for fixture in (build_exact_example(), build_zero_scalar_example()):
        validate_example(fixture, exact_locators=True)
        check_localization(fixture)
        cancel_exact_locators(fixture)
    print("PASS pole-tolerant localization and exact-locator cancellation fixtures")
    check_extra_root_failure()
    check_exact_boundary()
    print("PASS extra-root guard and exhaustive g=m boundary")
    print("PASS deployed constants; no deployed payment claimed")
    print(f"RESULT: PASS ({CHECKS} checks)")


def run_tamper_selftest(repo_root: Path, certificate: Path) -> None:
    pristine = load_certificate(certificate)
    validate_certificate(pristine, repo_root, check_sources=True)
    mutations = [
        ("source pin", ("source_pins", "experimental/grande_finale.tex"), "0" * 40),
        ("theorem set", ("theorems", 0), "NO_THEOREM"),
        ("nonclaim", ("nonclaims", 0), "CLAIMS_PAYMENT"),
        ("M31 agreement", ("deployed_rows", "mersenne31_mca", "m"), 1_116_023),
    ]
    for label, path, replacement in mutations:
        mutated = copy.deepcopy(pristine)
        cursor = mutated
        for key in path[:-1]:
            cursor = cursor[key]
        cursor[path[-1]] = replacement
        try:
            validate_certificate(mutated, repo_root, check_sources=False)
        except VerificationError:
            print(f"PASS tamper rejected: {label}")
        else:
            raise VerificationError(f"tamper accepted: {label}")
    print("RESULT: PASS (4/4 mutations rejected)")


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()
    repo_root = Path(__file__).resolve().parents[2]
    certificate = repo_root / CERT_REL
    try:
        if args.check:
            run_check(repo_root, certificate)
        else:
            run_tamper_selftest(repo_root, certificate)
    except (OSError, KeyError, ValueError, VerificationError, json.JSONDecodeError) as exc:
        print(f"RESULT: FAIL - {exc}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
