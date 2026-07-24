#!/usr/bin/env python3
"""Exact replay for the M31 quotient-prefix T64 block-swap witness.

Python is auxiliary replay only.  The proof-validation gate is the stdlib-only
Lean package `experimental/lean/m31_quotient_prefix_flatness/` built by fork CI.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any

P = 2**31 - 1
SCALE_2048 = pow(2, -2047, P)
ACTIVE_ROOTS = [
    434373082, 614288294, 1713110565, 1533195353,
    1984437538, 380812851, 163046109, 1766670796,
]
PARTIAL_27_REPS = [
    27, 37, 91, 101, 155, 165, 219, 229, 283, 293, 347, 357,
    411, 421, 475, 485, 539, 549, 603, 613, 667, 677, 731, 741,
    795, 805, 859, 869, 923, 933, 987,
]
ETA = [
    2144970186, 693846040, 254084710, 1501952290,
    1904231690, 558873387, 1400618348, 1749425225,
    2110682204, 1763030673, 102589073, 1770388691,
    971529856, 948975681, 774218929, 1490251835,
    2095038705, 838625156, 774891784, 644995098,
    888552471, 1685238706, 1330006363, 1053276022,
    1544945819, 100722017, 1420529349, 1803184017,
    1196844108, 324775767, 591689729, 1982980281,
]
SUPPORT_CLASSES = {
    "A": 5,
    "B1": 7,
    "B2": 9,
    "B3": 11,
    "B4": 13,
    "B5": 29,
    "B6": 31,
}
# Upstream steering files are recorded for provenance, not gated.  `agents.md` is
# rewritten by governance commits -- fb6d955 replaced the blob this packet froze --
# so drift there must report, never fail.  The recorded blob stays in the payload.
STEERING_SOURCES = frozenset({"agents.md"})
SOURCE_PINS = {
    "agents.md": "30d8b9f1b4caa3c7504fe3d24fc7ce8da84de434",
    "experimental/grande_finale.tex": "8a5d9791900ca9eed773feba146b92ad296704ce",
    "experimental/notes/thresholds/m31_c2048_partial_occupancy_30carrier_reduction.md":
        "7460c0830ac5d47db9f96e6f74f2a42d89ff8cbb",
    "experimental/notes/thresholds/m31_c2048_fixed_template_interleaved_quotient_route_cut.md":
        "3f69250b63b861963da03759b46d726f3e8754d1",
    "experimental/notes/thresholds/m31_q_rooted_shell_envelope.md":
        "45fd288abd2173d06af3fab244ed20568c991607",
    "experimental/notes/thresholds/m31_c2048_guarded_support_flat_separator.md":
        "8de0d71a7d01070035711fdc33965f7f6ab8c3ce",
    "experimental/notes/thresholds/m31_c2048_vt_multitemplate_global_rank_route_cut.md":
        "63418702fee4da749dd87c76821ab820d104cb09",
    "experimental/notes/thresholds/sidon_effective_image_mi_ma_c9_rowsharp.md":
        "ecfdfc5610f27c53fe40bb4d35692374d8af4d62",
}


def add2(u: tuple[int, int], v: tuple[int, int]) -> tuple[int, int]:
    return ((u[0] + v[0]) % P, (u[1] + v[1]) % P)


def mul2(u: tuple[int, int], v: tuple[int, int]) -> tuple[int, int]:
    return ((u[0] * v[0] - u[1] * v[1]) % P,
            (u[0] * v[1] + u[1] * v[0]) % P)


def pow2(u: tuple[int, int], e: int) -> tuple[int, int]:
    acc = (1, 0)
    base = u
    while e:
        if e & 1:
            acc = mul2(acc, base)
        base = mul2(base, base)
        e >>= 1
    return acc


def chebyshev_pow_two(x: int, exponent_log2: int) -> int:
    y = x % P
    for _ in range(exponent_log2):
        y = (2 * y * y - 1) % P
    return y


def quotient_labels() -> dict[int, int]:
    g = (1717986917, 1288490189)
    return {
        r: (SCALE_2048 * pow2(g, r * 2**19)[0]) % P
        for r in range(1, 2048, 2)
    }


def block_reps(a: int) -> list[int]:
    return [
        r for r in range(1, 2048, 2)
        if r % 64 in {a, 64 - a}
    ]


def poly_mul_linear(poly: list[int], root: int) -> list[int]:
    out = [0] * (len(poly) + 1)
    for i, coefficient in enumerate(poly):
        out[i] = (out[i] - root * coefficient) % P
        out[i + 1] = (out[i + 1] + coefficient) % P
    return out


def locator_for_reps(reps: list[int], labels: dict[int, int]) -> list[int]:
    poly = [1]
    for r in reps:
        poly = poly_mul_linear(poly, labels[r])
    return poly


def locator_prefix(reps: list[int], labels: dict[int, int], depth: int) -> list[int]:
    poly = locator_for_reps(reps, labels)
    assert poly[-1] == 1
    return list(reversed(poly[:-1]))[:depth]


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode()
    return hashlib.sha1(header + data).hexdigest()


def int_list_sha256(values: list[int]) -> str:
    payload = ",".join(str(value) for value in values).encode()
    return hashlib.sha256(payload).hexdigest()


def build_expected(repo_root: Path | None = None) -> dict[str, Any]:
    labels = quotient_labels()
    odd_reps = list(range(1, 2048, 2))
    assert len(labels) == 1024
    assert len(set(labels.values())) == 1024

    g = (1717986917, 1288490189)
    assert mul2(g, (g[0], -g[1])) == (1, 0)
    assert pow2(g, 2**30) == (P - 1, 0)
    assert pow2(g, 2**31) == (1, 0)

    assert all(chebyshev_pow_two(x, 21) == 0 for x in ACTIVE_ROOTS)
    active_fold_labels = [
        (SCALE_2048 * chebyshev_pow_two(x, 11)) % P
        for x in ACTIVE_ROOTS
    ]
    assert active_fold_labels == [labels[1]] * 4 + [labels[3]] * 4

    t64_fibers: list[dict[str, Any]] = []
    for a in range(1, 32, 2):
        reps = block_reps(a)
        values = [labels[r] for r in reps]
        tau = chebyshev_pow_two((2 * labels[a]) % P, 6)
        assert len(reps) == 64
        assert len(set(values)) == 64
        assert all(chebyshev_pow_two((2 * x) % P, 6) == tau for x in values)
        t64_fibers.append({
            "class": a,
            "tau": tau,
            "punctured": a in {1, 3},
            "rep_congruences_mod_64": [a, 64 - a],
            "label_sha256": int_list_sha256(values),
        })

    punctured_reps = [r for r in odd_reps if r not in {1, 3}]
    punctured_labels = [labels[r] for r in punctured_reps]
    assert len(punctured_reps) == 1022
    assert len(set(punctured_labels)) == 1022

    common_reps: list[int] = []
    for a in [15, 17, 19, 21, 23, 25]:
        common_reps.extend(block_reps(a))
    common_reps.extend(PARTIAL_27_REPS)
    common_reps = sorted(common_reps)
    assert len(common_reps) == 415
    assert len(set(common_reps)) == 415
    assert set(common_reps) <= set(punctured_reps)

    supports: dict[str, dict[str, Any]] = {}
    support_reps: dict[str, list[int]] = {}
    prefixes_63 = set()
    for name, moving_class in SUPPORT_CLASSES.items():
        reps = sorted(common_reps + block_reps(moving_class))
        support_reps[name] = reps
        values = [labels[r] for r in reps]
        assert len(reps) == 479
        assert len(set(reps)) == 479
        assert set(reps) <= set(punctured_reps)
        prefix32 = locator_prefix(reps, labels, 32)
        prefix63 = locator_prefix(reps, labels, 63)
        assert prefix32 == ETA
        prefixes_63.add(tuple(prefix63))
        supports[name] = {
            "moving_t64_class": moving_class,
            "size": len(reps),
            "rep_sha256": int_list_sha256(reps),
            "label_sha256": int_list_sha256(values),
        }
    assert len(prefixes_63) == 1

    anchor = set(support_reps["A"])
    for name in [f"B{i}" for i in range(1, 7)]:
        other = set(support_reps[name])
        assert len(anchor - other) == 64
        assert len(anchor & other) == 415

    h64 = math.comb(479, 64) * math.comb(543, 64)
    q = P**32
    four_h64 = 4 * h64
    assert four_h64 < q
    rooted_degree_lower_bound = 6
    violation_lhs_lower_bound = q * (rooted_degree_lower_bound - 3)
    assert violation_lhs_lower_bound > four_h64

    inherited_source_hashes: dict[str, str] = {}
    if repo_root is not None:
        for rel, expected_sha in SOURCE_PINS.items():
            actual = git_blob_sha(repo_root / rel)
            if rel in STEERING_SOURCES:
                if actual != expected_sha:
                    print(
                        f"NOTE steering source drifted: {rel} "
                        f"recorded {expected_sha}, observed {actual}"
                    )
                inherited_source_hashes[rel] = expected_sha
                continue
            assert actual == expected_sha, (
                f"stale source pin for {rel}: expected {expected_sha}, got {actual}"
            )
            inherited_source_hashes[rel] = actual
    else:
        inherited_source_hashes = dict(SOURCE_PINS)

    return {
        "schema": "m31-quotient-prefix-flatness-t64-witness-v1",
        "status": "COUNTEREXAMPLE_NEW_FLOOR",
        "activity": "FALSIFY",
        "base_sha": "c49e45eed71af9c24e3599c2fca3b76e02692be9",
        "branch": "gptpro/m31-quotient-prefix-flatness",
        "workboard_item": "M1",
        "row": "Mersenne-31 list at 2^-100",
        "object": "LIST",
        "target_epsilon": "2^-100",
        "agreement": 1116023,
        "B_star": 16777215,
        "architecture": "DIRECT_PINNED_C2048_U0_V1_QUOTIENT_PROFILE",
        "partition_digest": "N/A; fixed local profile, no row atom banked",
        "atom_or_cell": "Q / fixed-template quotient-prefix family",
        "quantifier": (
            "Existential target eta and anchor A in the pinned punctured quotient "
            "domain, with six explicitly listed same-prefix neighbors."
        ),
        "projection_and_unit": (
            "479-subsets of the 1022-point quotient domain per first-32 locator "
            "coefficient target; no codeword, ray, or slope projection."
        ),
        "direct_statement": (
            "At deficiency e=64 the anchor has d_64(A)>=6 while "
            "floor(4*H_64/p^32)=0, so p^32*(d_64(A)-3)_+>4*H_64."
        ),
        "field": {
            "p": P,
            "p_power_32": q,
            "monic_T2048_scale": SCALE_2048,
            "norm_one_generator": [1717986917, 1288490189],
        },
        "active_profile": {
            "c": 2048,
            "u": 0,
            "v": 1,
            "m_complete": 479,
            "r_err": 137,
            "h": 2,
            "active_four_subset_indices": [0, 1, 4, 5],
            "active_roots": ACTIVE_ROOTS,
            "active_fold_labels": active_fold_labels,
            "punctured_reps": [1, 3],
            "punctured_labels": [labels[1], labels[3]],
            "Q_prime_size": 1022,
        },
        "quotient_parameterization": {
            "formula": (
                "q_r = 2^(-2047) * Re(g^(r*2^19)) mod p, "
                "r odd, 1<=r<=2047"
            ),
            "rep_set": "all odd integers r with 1<=r<=2047",
            "quotient_label_sha256": int_list_sha256(
                [labels[r] for r in odd_reps]
            ),
            "punctured_rep_set": "all odd r in [1,2047] except 1 and 3",
            "punctured_label_sha256": int_list_sha256(punctured_labels),
        },
        "t64_fibers": t64_fibers,
        "witness": {
            "common_full_t64_classes": [15, 17, 19, 21, 23, 25],
            "common_partial_t64_class": 27,
            "common_partial_reps": PARTIAL_27_REPS,
            "common_rep_sha256": int_list_sha256(common_reps),
            "common_label_sha256": int_list_sha256(
                [labels[r] for r in common_reps]
            ),
            "common_size": 415,
            "support_formula": (
                "A=C union C_5; B1=C union C_7; B2=C union C_9; "
                "B3=C union C_11; B4=C union C_13; "
                "B5=C union C_29; B6=C union C_31"
            ),
            "supports": supports,
            "eta_convention": (
                "For V_E(Y)=Y^479+eta_1 Y^478+...+eta_32 Y^447+..., "
                "eta=[eta_1,...,eta_32]."
            ),
            "eta": ETA,
            "matching_nonleading_coefficients": 63,
            "deficiency": 64,
            "listed_neighbor_count": 6,
            "rooted_degree_lower_bound": 6,
        },
        "shell_arithmetic": {
            "H_64": h64,
            "four_H_64": four_h64,
            "floor_four_H_64_over_p32": four_h64 // q,
            "witness_threshold": 4 + four_h64 // q,
            "three_p32": 3 * q,
            "violation_lhs_lower_bound": violation_lhs_lower_bound,
            "strict_margin": violation_lhs_lower_bound - four_h64,
        },
        "recalibration": {
            "coefficient_c": 4,
            "intercepts_refuted_by_witness": [3, 4, 5],
            "minimum_intercept_not_refuted_by_the_six_listed_neighbors": 6,
            "conditional_b6_c4_rooted_shell_total": 14459159,
            "conditional_b6_c4_reserve_below_B_star": 2318056,
            "warning": (
                "(6+4) is only an arithmetically viable successor.  This packet "
                "does not prove its pointwise shell hypothesis, and any actual "
                "d_64(A)>6 could raise the required intercept."
            ),
        },
        "source_blob_pins": inherited_source_hashes,
        "validation": {
            "lean_package": "experimental/lean/m31_quotient_prefix_flatness",
            "python_replay": (
                "python3 experimental/scripts/"
                "verify_m31_quotient_prefix_flatness_t64_witness.py --check"
            ),
            "python_optimized_replay": (
                "python3 -O experimental/scripts/"
                "verify_m31_quotient_prefix_flatness_t64_witness.py --check"
            ),
            "python_mutation": (
                "python3 experimental/scripts/"
                "verify_m31_quotient_prefix_flatness_t64_witness.py "
                "--tamper-selftest"
            ),
        },
        "nonclaims": [
            "No row-global U_Q integer is banked.",
            "No received-word or exact-boundary codeword family is constructed.",
            "No first-match survival after a T64 quotient owner is claimed.",
            "No slope or ray projection is claimed.",
            "No rigidity statement for any e is proved.",
            "No (6+4) or other replacement shell hypothesis is proved.",
            "No adjacent-row certificate or safe agreement is claimed.",
        ],
    }


def canonical_json(data: dict[str, Any]) -> str:
    return json.dumps(data, indent=2, sort_keys=True) + "\n"


def validate(certificate: dict[str, Any], expected: dict[str, Any]) -> None:
    if certificate != expected:
        raise AssertionError("certificate content differs from exact replay")
    shell = certificate["shell_arithmetic"]
    witness = certificate["witness"]
    if witness["rooted_degree_lower_bound"] < shell["witness_threshold"]:
        raise AssertionError("witness misses the required rooted-degree threshold")
    if shell["violation_lhs_lower_bound"] <= shell["four_H_64"]:
        raise AssertionError("claimed strict shell violation does not hold")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--emit", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[2]
    certificate_path = (
        repo_root
        / "experimental/data/certificates/"
          "m31-quotient-prefix-flatness-t64-witness/"
          "m31_quotient_prefix_flatness_t64_witness.json"
    )
    expected = build_expected(repo_root)

    if args.emit:
        certificate_path.parent.mkdir(parents=True, exist_ok=True)
        certificate_path.write_text(canonical_json(expected), encoding="utf-8")
        print(f"wrote {certificate_path}")

    if args.check:
        raw = certificate_path.read_text(encoding="utf-8")
        certificate = json.loads(raw)
        validate(certificate, expected)
        if raw != canonical_json(expected):
            raise AssertionError("certificate is not in canonical JSON form")
        print("M31 quotient-prefix T64 witness: PASS")
        print("d_64(A) >= 6, floor(4 H_64 / p^32) = 0")
        print("terminal = COUNTEREXAMPLE_NEW_FLOOR")

    if args.tamper_selftest:
        tampered = json.loads(canonical_json(expected))
        tampered["witness"]["eta"][0] ^= 1
        try:
            validate(tampered, expected)
        except AssertionError:
            print("tamper self-test: PASS")
        else:
            raise AssertionError("tampered certificate was accepted")

    if not (args.check or args.emit or args.tamper_selftest):
        parser.error("select --check, --emit, or --tamper-selftest")


if __name__ == "__main__":
    main()
