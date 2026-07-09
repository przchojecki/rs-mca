#!/usr/bin/env python3
"""Verifier for the B1 ambient-vs-image normalization bridge audit.

This packet addresses the `FOUND-WEAKER` B1 joint reported by PR #433 for
`experimental/asymptotic_rs_mca.tex`: the asymptotic paper defines primitive
moments using the actual image `L = |im Phi|`, while the cited Fourier-flat Q
theorem in `experimental/grande_finale.tex` is stated at ambient prefix-box
scale.

The verifier does three small, exact things.

1. Enumerates toy smooth-subgroup prefix maps and checks the exact identities

       R_ambient(s) = (A/L) R_image(s)
       Gamma_r^ambient = (A/L)^(r-1) Gamma_r^image,

   where A is the ambient prefix-box size and L is the actual image size.

2. Checks the logical direction for max fibers: an ambient max-fiber bound is
   stronger than an image-normalized max-fiber bound because L <= A.

3. Replays the symbolic single-field obstruction from the integrated fp-span
   note: if the same growing field K contains T and also supplies the ambient
   prefix denominator K^R with R = kappa N, then |Omega| <= 3^N is too small to
   make `log |Omega| - R log |K| = o(N)`.  The frontier reading therefore needs
   either an explicit two-field/base-alphabet convention or an image-scale
   restatement of the C9 Fourier/Sidon payment.

This is an audit packet, not a proof of the asymptotic theorem and not a finite
frontier-adjacent certificate.
"""
from __future__ import annotations

import argparse
import contextlib
import copy
import hashlib
import io
import json
import math
import os
import sys
import tempfile
from collections import defaultdict
from fractions import Fraction
from itertools import combinations


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))
JSON_PATH = os.path.join(
    REPO_ROOT,
    "experimental",
    "data",
    "asymptotic_b1_normalization_bridge.json",
)
NOTE_PATH = os.path.join(
    REPO_ROOT,
    "experimental",
    "notes",
    "audits",
    "asymptotic_b1_normalization_bridge.md",
)

WALL_ID = "ASYMPTOTIC-RS-MCA-B1-NORMALIZATION-BRIDGE"

TOY_ROWS = [
    {"label": "F17x_16_m8_w3", "p": 17, "n": 16, "m": 8, "w": 3},
    {"label": "F17x_16_m8_w4_underfilled", "p": 17, "n": 16, "m": 8, "w": 4},
    {"label": "mu20_F41_m10_w2", "p": 41, "n": 20, "m": 10, "w": 2},
    {"label": "mu24_F97_m12_w2", "p": 97, "n": 24, "m": 12, "w": 2},
]


def primitive_root(p: int) -> int:
    phi = p - 1
    factors = []
    x = phi
    d = 2
    while d * d <= x:
        if x % d == 0:
            factors.append(d)
            while x % d == 0:
                x //= d
        d += 1
    if x > 1:
        factors.append(x)
    for g in range(2, p):
        if all(pow(g, phi // q, p) != 1 for q in factors):
            return g
    raise RuntimeError(f"no primitive root for p={p}")


def subgroup_domain(p: int, n: int) -> list[int]:
    if (p - 1) % n != 0:
        raise ValueError(f"n={n} must divide p-1={p - 1}")
    g = primitive_root(p)
    h = pow(g, (p - 1) // n, p)
    out = []
    cur = 1
    for _ in range(n):
        out.append(cur)
        cur = (cur * h) % p
    if len(set(out)) != n:
        raise AssertionError("subgroup generator has wrong order")
    return sorted(out)


def prefix_key(support: tuple[int, ...], p: int, w: int) -> tuple[int, ...]:
    key = [0] * w
    for x in support:
        power = 1
        for j in range(w):
            power = (power * x) % p
            key[j] = (key[j] + power) % p
    return tuple(key)


def histogram_for_row(p: int, n: int, m: int, w: int) -> dict[tuple[int, ...], int]:
    domain = subgroup_domain(p, n)
    hist: dict[tuple[int, ...], int] = defaultdict(int)
    for indices in combinations(range(n), m):
        support = tuple(domain[i] for i in indices)
        hist[prefix_key(support, p, w)] += 1
    return dict(hist)


def frac_to_decimal(frac: Fraction, digits: int = 12) -> float:
    return round(frac.numerator / frac.denominator, digits)


def log2_frac(frac: Fraction) -> float:
    return math.log2(frac.numerator) - math.log2(frac.denominator)


def sha256_json(obj) -> str:
    payload = json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def gamma_fraction(hist: dict[tuple[int, ...], int], normalizer_size: int, total: int, r: int) -> Fraction:
    power_sum = sum(count**r for count in hist.values())
    return Fraction((normalizer_size ** (r - 1)) * power_sum, total**r)


def row_audit(row: dict) -> dict:
    p, n, m, w = row["p"], row["n"], row["m"], row["w"]
    hist = histogram_for_row(p, n, m, w)
    total = math.comb(n, m)
    ambient = p**w
    image = len(hist)
    max_count = max(hist.values())
    ambient_over_image = Fraction(ambient, image)
    r_image = Fraction(max_count * image, total)
    r_ambient = Fraction(max_count * ambient, total)
    if r_ambient != ambient_over_image * r_image:
        raise AssertionError("R ambient/image relation failed")

    gamma_checks = {}
    for r in (2, 3, 4):
        g_image = gamma_fraction(hist, image, total, r)
        g_ambient = gamma_fraction(hist, ambient, total, r)
        expected = (ambient_over_image ** (r - 1)) * g_image
        if g_ambient != expected:
            raise AssertionError(f"Gamma relation failed at r={r}")
        gamma_checks[str(r)] = {
            "gamma_image": frac_to_decimal(g_image),
            "gamma_ambient": frac_to_decimal(g_ambient),
            "ambient_over_image_power": frac_to_decimal(ambient_over_image ** (r - 1)),
            "relation_exact": True,
        }

    return {
        "label": row["label"],
        "parameters": row,
        "total_supports": total,
        "ambient_prefix_box_size_A": ambient,
        "actual_image_size_L": image,
        "ambient_over_image_ratio": {
            "numerator": ambient_over_image.numerator,
            "denominator": ambient_over_image.denominator,
            "decimal": frac_to_decimal(ambient_over_image),
            "log2": log2_frac(ambient_over_image),
            "per_N_log2": log2_frac(ambient_over_image) / n,
        },
        "max_fiber": {
            "count": max_count,
            "R_image": frac_to_decimal(r_image),
            "R_ambient": frac_to_decimal(r_ambient),
            "R_relation_exact": True,
        },
        "gamma_relation": gamma_checks,
        "histogram_sha256": sha256_json(sorted(hist.items())),
    }


def single_field_obstruction_table(kappa: Fraction = Fraction(1, 4)) -> list[dict]:
    rows = []
    for n in (100, 1000, 10000, 100000):
        # If |K| >= N and R = kappa N, then
        #   log2 |Omega| - R log2 |K| <= N log2 3 - kappa N log2 N.
        upper_per_n = math.log2(3) - float(kappa) * math.log2(n)
        rows.append(
            {
                "N": n,
                "kappa": f"{kappa.numerator}/{kappa.denominator}",
                "upper_bound_log2_Omega_over_ambient_per_N": upper_per_n,
                "tends_to_minus_infinity": True,
            }
        )
    return rows


def build_packet() -> dict:
    rows = [row_audit(row) for row in TOY_ROWS]
    return {
        "schema": "asymptotic-b1-normalization-bridge/v1",
        "wall_id": WALL_ID,
        "status": "AUDIT",
        "source_gap": "PR #433 B1: image-normalized primitive moments vs ambient Fourier-flat Q",
        "companion_note": "experimental/notes/audits/asymptotic_b1_normalization_bridge.md",
        "companion_verifier": "experimental/scripts/verify_asymptotic_b1_normalization_bridge.py",
        "logic_summary": {
            "max_fiber_direction": "An ambient max-fiber bound M/A implies the image-normalized bound M/L because L <= A.",
            "moment_relation": "Gamma_ambient_r = (A/L)^(r-1) Gamma_image_r exactly.",
            "therefore": "The B1 gap is not the max-fiber implication; it is the denominator convention for moments/Fourier payment and the single-field vs two-field reading of the ambient box.",
        },
        "toy_rows": rows,
        "single_field_obstruction": {
            "statement": "If T is inside the same growing field K and R=kappa*N, then |Omega|<=3^N cannot balance ambient K^R; the offset is -Omega(N log N), not o(N).",
            "table": single_field_obstruction_table(),
        },
        "repair_options": [
            "Print a two-field convention: point field E grows to contain T, while the base alphabet B supplies the entropy denominator.",
            "Restate C9/Fourier-Sidon payment at image scale L=|im Phi| instead of ambient box scale.",
            "Add an explicit bridge hypothesis A/L=exp(o(N)) exactly where ambient moments are converted to image moments.",
        ],
        "nonclaims": [
            "Does not prove the asymptotic RS-MCA theorem.",
            "Does not audit C9's missing moduli manuscript.",
            "Does not instantiate finite deployed adjacent rows.",
            "Does not decide whether the intended convention is the two-field reading or an image-scale theorem.",
        ],
    }


def write_json(path: str, packet: dict) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(packet, fh, indent=2, sort_keys=True)
        fh.write("\n")


def load_json(path: str) -> dict:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def compare_packet(expected: dict, actual: dict) -> list[str]:
    if expected == actual:
        return []
    diffs = []
    expected_rows = {row["label"]: row for row in expected.get("toy_rows", [])}
    actual_rows = {row["label"]: row for row in actual.get("toy_rows", [])}
    if set(expected_rows) != set(actual_rows):
        diffs.append(f"row labels differ: expected={sorted(expected_rows)} actual={sorted(actual_rows)}")
    for label in sorted(set(expected_rows) & set(actual_rows)):
        for path in [
            ("ambient_prefix_box_size_A",),
            ("actual_image_size_L",),
            ("ambient_over_image_ratio", "log2"),
            ("max_fiber", "R_image"),
            ("max_fiber", "R_ambient"),
        ]:
            ev = expected_rows[label]
            av = actual_rows[label]
            for key in path:
                ev = ev[key]
                av = av[key]
            if ev != av:
                diffs.append(f"{label} {'.'.join(path)} expected {ev!r} actual {av!r}")
    if not diffs:
        diffs.append("packet differs outside headline fields")
    return diffs


def check_packet_file(expected: dict, path: str) -> list[str]:
    return compare_packet(expected, load_json(path))


def tamper_selftest(packet: dict) -> None:
    checks = []
    mutated = copy.deepcopy(packet)
    mutated["toy_rows"][0]["actual_image_size_L"] += 1
    checks.append(("image size", mutated))
    mutated = copy.deepcopy(packet)
    mutated["logic_summary"]["max_fiber_direction"] = "wrong direction"
    checks.append(("logic summary", mutated))
    mutated = copy.deepcopy(packet)
    mutated["single_field_obstruction"]["table"][1]["tends_to_minus_infinity"] = False
    checks.append(("single-field table", mutated))
    with tempfile.TemporaryDirectory() as tmpdir:
        for name, mutated_packet in checks:
            path = os.path.join(tmpdir, f"{name.replace(' ', '_')}.json")
            write_json(path, mutated_packet)
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                rc = main(["--json-out", path, "--check"])
            if rc == 0:
                raise AssertionError(f"tamper self-test did not catch {name}")
    print(f"tamper self-test: caught {len(checks)} mutations")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json-out", default=JSON_PATH)
    parser.add_argument("--emit-defaults", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args(argv)

    packet = build_packet()
    if args.tamper_selftest:
        tamper_selftest(packet)
        return 0
    if args.emit_defaults:
        write_json(args.json_out, packet)
        print(f"wrote {os.path.relpath(args.json_out, REPO_ROOT)}")
    if args.check:
        diffs = check_packet_file(packet, args.json_out)
        if diffs:
            print("CHECK FAILED", file=sys.stderr)
            for diff in diffs[:20]:
                print(f"  - {diff}", file=sys.stderr)
            return 1
        print(f"CHECK OK: {os.path.relpath(args.json_out, REPO_ROOT)}")
    if not args.emit_defaults and not args.check:
        print(json.dumps(packet, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
