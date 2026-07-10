#!/usr/bin/env python3
"""Independent checker for tangent-exactness (no generator import).

Recomputes remark calibration integers via integer-only arithmetic, re-runs the
prop:capf-tangent constructive MCA lower witness with a DIFFERENT domain
embedding (reversed indices), re-scans paper labels by fresh line scan, and
re-checks in-range menu rows against the stored cert.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

CERT_REL = Path(
    "experimental/data/certificates/tangent-exactness/tangent_exactness.json"
)
PAPER_REL = Path("experimental/cap25_cap_v13_raw.tex")
LABELS = (
    "rem:capf-tangent-calibration",
    "prop:capf-tangent",
    "def:capf-tangent-cell",
    "thm:capf-staircase",
    "thm:deep-mca",
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def is_constant_on(vec, support):
    if not support:
        return True
    v0 = vec[support[0]]
    return all(vec[i] == v0 for i in support)


def constructive_reversed(q: int, n: int, r: int) -> int:
    """Lower witness with reversed domain indices (different from generator)."""
    # Place T at the high end of the domain
    T = list(range(n - r - 1, n))  # last r+1 points
    assert len(T) == r + 1
    gammas = list(range(r + 1))
    f1 = [0] * n
    f2 = [0] * n
    for i, t in enumerate(T):
        f2[t] = 1
        f1[t] = (-gammas[i]) % q
    A = n - r
    bad = 0
    for gamma in gammas:
        ti = next(t for t in T if f1[t] == (-gamma) % q)
        S = [x for x in range(n) if x == ti or x not in T]
        word = [(f1[i] + gamma * f2[i]) % q for i in range(n)]
        point_ok = all(word[i] == 0 for i in S) and len(S) == A
        joint = is_constant_on(f1, S) and is_constant_on(f2, S)
        if point_ok and not joint:
            bad += 1
    return bad


def check() -> None:
    root = repo_root()
    cert = json.loads((root / CERT_REL).read_text(encoding="utf-8"))
    errors = []

    # Labels
    text = (root / PAPER_REL).read_text(encoding="utf-8")
    for lab in LABELS:
        if lab not in text:
            errors.append(f"missing label {lab}")

    # Calibration integers (independent)
    n, k = 512, 256
    B_star = (17**32) // (2**128)
    R_tan = (n - k) // 3
    a_star = n + 1 - B_star
    cal = cert["calibration_integers"]
    if B_star != 6 or cal["B_star"] != 6:
        errors.append(f"B_star {B_star} vs cert {cal['B_star']}")
    if R_tan != 85 or cal["R_tan"] != 85:
        errors.append(f"R_tan {R_tan}")
    if a_star != 507 or cal["a_star"] != 507:
        errors.append(f"a_star {a_star}")
    if (n - 506 + 1) != 7 or (n - 507 + 1) != 6:
        errors.append("N(506)/N(507)")

    # Menu rows
    for row in cert["menu"]:
        if row["kind"] == "in_range_exhaustive_k1":
            if row["true_max_N"] != row["predicted_N"]:
                errors.append(f"exhaustive mismatch {row}")
            # reversed constructive lower
            got = constructive_reversed(row["q"], row["n"], row["r"])
            if got < row["predicted_N"]:
                errors.append(
                    f"reversed lower {got} < pred {row['predicted_N']} for {row}"
                )
        if row["kind"] == "in_range_lower_only":
            if not row["lower_achieved"]:
                errors.append(f"lower failed {row}")

    if cert["summary"]["verdict"] != "NO ISSUE":
        errors.append("verdict not NO ISSUE")

    if errors:
        print("RESULT: FAIL")
        for e in errors:
            print(" -", e)
        raise SystemExit(1)
    print("RESULT: PASS")
    print("route: reversed-T constructive lower + independent calibration integers")
    print("verdict: NO ISSUE")


def main(argv=None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--check", action="store_true")
    args = p.parse_args(argv)
    if args.check:
        try:
            check()
            return 0
        except SystemExit as e:
            return int(e.code) if e.code is not None else 1
    p.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
