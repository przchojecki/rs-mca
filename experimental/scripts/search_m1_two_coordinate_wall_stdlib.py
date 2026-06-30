#!/usr/bin/env python3
"""Pure-stdlib exact-histogram scan of the M1 two-coordinate Kummer wall.

Stdlib (no numpy/sympy) reimplementation and extension of
`search_m1_remaining_two_coordinate_wall.py`, which requires numpy and was
capped at p <= 500, e <= 24.  The scanned object is the slack-two depth-two M1
two-coordinate character sum

    S_{a,b,0,d} = sum_{u,v != 0, w=-1-u-v != 0, A != 0}
                    chi^a(u) chi^b(v) psi^d(A(u,v)),
    A(u,v) = -(u^2 + v^2 + u v + u + v + 1),

with chi of order e and psi of order h = e * gcd(2, n), n = (p-1)/e.  The
conjectured remaining-wall bound (m1_remaining_two_coordinate_wall_experiment.md,
m1_kummer_weil_import_contract.md) is |S| <= 4p on the ramified-nonreciprocal
asymmetric-nonresonant class C_2^anr.

Key identity used here: S_{a,b,0,d} is exactly the 3D finite Fourier transform of
the joint discrete-log histogram

    Count[dlog(u) mod e][dlog(v) mod e][dlog(A) mod h],

built by a single O(p^2) pass per (p,e).  This is computed with cmath only, and
is faster than the numpy matmul-per-d original, so the scan runs in this
environment AND extends past the published grid.

Validation: the report grid (nonres, p<=500, e<=24) reproduces the published
numpy result exactly (453 cases, 596304 scanned tuples, 0 violations of 4p,
max ratio 3.2173609608); the diagonal n=20, p<=500 grid reproduces the published
max 3.9771715522 at (p=421, e=21).  See `--certificate`.

Script output standard (agents.md): inputs/object/result/proof-cert/theorem-id/
status are all in the JSON certificate; status is EXPERIMENTAL / AUDIT (finite
numerical evidence, not a proof of the 4p bound).
"""
from __future__ import annotations

import argparse
import cmath
import json
import math
import time
from pathlib import Path
from typing import Any, Dict, List

STATUS = "EXPERIMENTAL"
THEOREM_ID = "M1 two-coordinate Kummer wall (m1_remaining_two_coordinate_wall_experiment.md, m1_kummer_weil_import_contract.md (KW_2))"
OBJECT = "M1 slack-two depth-two two-coordinate character sum |S_{a,b,0,d}| vs 4p"


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def prime_factors(m: int) -> List[int]:
    f: List[int] = []
    d = 2
    while d * d <= m:
        if m % d == 0:
            f.append(d)
            while m % d == 0:
                m //= d
        d += 1 if d == 2 else 2
    if m > 1:
        f.append(m)
    return f


def primitive_root(p: int) -> int:
    fs = prime_factors(p - 1)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in fs):
            return g
    raise ValueError(f"no primitive root for {p}")


def dlog_table(p: int) -> List[int]:
    g = primitive_root(p)
    t = [0] * p
    v = 1
    for e in range(p - 1):
        t[v] = e
        v = v * g % p
    return t


def line_monodromies(e: int, h: int, a: int, b: int, d: int):
    lift = h // e
    first = (lift * a) % h
    second = (lift * b) % h
    infinity = (-(first + second + 2 * d)) % h
    return first, second, infinity


def keep_tuple(e: int, h: int, a: int, b: int, d: int, mode: str):
    first, second, infinity = line_monodromies(e, h, a, b, d)
    if infinity == 0:
        return False, None  # infinity_unramified (proved slice)
    if (first + second) % h == 0 or (first + infinity) % h == 0 or (second + infinity) % h == 0:
        return False, None  # projective_reciprocal (proved slice)
    if mode in ("asym", "nonres"):
        if first == second or first == infinity or second == infinity:
            return False, None  # projective equal pair C_2^peq
    if mode == "nonres":
        if any((m + d) % h == 0 for m in (first, second, infinity)):
            return False, None  # line-conic resonant C_2^lc
    return True, (first, second, infinity)


def build_histogram(p: int, e: int, h: int, dlog: List[int]):
    count = [[[0] * h for _ in range(e)] for _ in range(e)]
    dle = [dlog[x] % e for x in range(p)]
    dlh = [dlog[x] % h for x in range(p)]
    for u in range(1, p):
        cu = count[dle[u]]
        uu = (u * u + u) % p
        base = (-1 - u) % p
        for v in range(1, p):
            if (base - v) % p == 0:  # w = -1-u-v = 0
                continue
            A = (-(uu + v * v + u * v + v + 1)) % p
            if A == 0:
                continue
            cu[dle[v]][dlh[A]] += 1
    return count


def scan_case(p: int, e: int, dlog: List[int], mode: str, diagonal: bool, tol: float) -> Dict[str, Any]:
    n = (p - 1) // e
    h = e * math.gcd(2, n)
    count = build_histogram(p, e, h, dlog)
    ze = [cmath.exp(2j * cmath.pi * t / e) for t in range(e)]
    zh = [cmath.exp(2j * cmath.pi * t / h) for t in range(h)]
    best_abs = -1.0
    best_tuple = (0, 0, 0, 0)
    best_mono = (0, 0, 0)
    scanned = 0
    violations = 0
    viol_examples: List[Dict[str, Any]] = []
    for d in range(1, h):
        bl = [[0j] * e for _ in range(e)]
        for j in range(e):
            cj = count[j]
            blj = bl[j]
            for k in range(e):
                cjk = cj[k]
                s = 0j
                for l in range(h):
                    c = cjk[l]
                    if c:
                        s += c * zh[(d * l) % h]
                blj[k] = s
        cmat = [[0j] * e for _ in range(e)]
        for j in range(e):
            blj = bl[j]
            cj = cmat[j]
            for b in range(1, e):
                s = 0j
                for k in range(e):
                    s += blj[k] * ze[(b * k) % e]
                cj[b] = s
        for a in range(1, e):
            for b in range(1, e):
                if diagonal and b != a:
                    continue
                keep, mono = keep_tuple(e, h, a, b, d, mode)
                if not keep:
                    continue
                s = 0j
                for j in range(e):
                    s += ze[(a * j) % e] * cmat[j][b]
                mag = abs(s)
                scanned += 1
                if mag > 4 * p + tol:
                    violations += 1
                    if len(viol_examples) < 8:
                        viol_examples.append(
                            {"p": p, "e": e, "h": h, "tuple": [a, b, 0, d],
                             "abs": round(mag, 6), "ratio": round(mag / p, 8)}
                        )
                if mag > best_abs:
                    best_abs = mag
                    best_tuple = (a, b, 0, d)
                    best_mono = mono
    return {
        "p": p, "e": e, "n": n, "h": h, "scanned": scanned,
        "best_ratio": round(best_abs / p, 10) if scanned else 0.0,
        "best_abs": round(best_abs, 6) if scanned else 0.0,
        "best_tuple": list(best_tuple),
        "best_mono": list(best_mono) if best_mono else [0, 0, 0],
        "violations": violations, "viol_examples": viol_examples,
    }


def run_grid(p_min: int, p_max: int, e_max: int, mode: str, diagonal_n: int, tol: float) -> List[Dict[str, Any]]:
    cases: List[Dict[str, Any]] = []
    for p in range(max(5, p_min), p_max + 1):
        if not is_prime(p):
            continue
        dlog = dlog_table(p)
        if diagonal_n:
            if (p - 1) % diagonal_n != 0:
                continue
            e = (p - 1) // diagonal_n
            if e < 2:
                continue
            cases.append(scan_case(p, e, dlog, mode, True, tol))
        else:
            for e in range(2, e_max + 1):
                if (p - 1) % e != 0:
                    continue
                cases.append(scan_case(p, e, dlog, mode, False, tol))
    return cases


def summarize(cases: List[Dict[str, Any]]) -> Dict[str, Any]:
    feas = sorted((c for c in cases if c["scanned"]), key=lambda c: c["best_ratio"], reverse=True)
    return {
        "case_count": len(cases),
        "scanned_total": sum(c["scanned"] for c in cases),
        "violation_total": sum(c["violations"] for c in cases),
        "max_ratio": feas[0]["best_ratio"] if feas else 0.0,
        "argmax": {k: feas[0][k] for k in ("p", "e", "h", "best_tuple", "best_mono")} if feas else None,
        "top10": [{k: c[k] for k in ("p", "e", "h", "best_ratio", "best_tuple", "best_mono")} for c in feas[:10]],
        "violation_examples": [ex for c in cases for ex in c["viol_examples"]][:16],
    }


def direct_S(p: int, e: int, h: int, dlog: List[int], a: int, b: int, d: int) -> float:
    """Independent O(p^2) direct evaluation of |S_{a,b,0,d}| / p (cross-check)."""
    ze = 2j * cmath.pi / e
    zh = 2j * cmath.pi / h
    s = 0j
    for u in range(1, p):
        cu = cmath.exp(ze * (a * dlog[u]))
        for v in range(1, p):
            if (-1 - u - v) % p == 0:
                continue
            A = (-(u * u + v * v + u * v + u + v + 1)) % p
            if A == 0:
                continue
            s += cu * cmath.exp(ze * (b * dlog[v])) * cmath.exp(zh * (d * dlog[A]))
    return abs(s) / p


def build_certificate() -> Dict[str, Any]:
    tol = 1e-7
    report = summarize(run_grid(5, 500, 24, "nonres", 0, tol))
    diag = summarize(run_grid(5, 500, 0, "remaining", 20, tol))
    dl601 = dlog_table(601)
    dl197 = dlog_table(197)
    return {
        "status": STATUS,
        "theorem_id": THEOREM_ID,
        "object": OBJECT,
        "method": "3D discrete-log histogram + finite Fourier transform; pure stdlib (cmath); no numpy",
        "conjectured_bound": "|S_{a,b,0,d}| <= 4 p on the ramified-nonreciprocal asymmetric-nonresonant class C_2^anr",
        "report_grid_nonres_p500_e24": {
            "case_count": report["case_count"],
            "scanned_total": report["scanned_total"],
            "violation_total_4p": report["violation_total"],
            "max_ratio": report["max_ratio"],
            "argmax": report["argmax"],
            "reproduces_published_numpy": (
                report["case_count"] == 453
                and report["scanned_total"] == 596304
                and report["violation_total"] == 0
                and report["max_ratio"] == 3.2173609608
            ),
        },
        "diagonal_grid_n20_p500": {
            "max_ratio": diag["max_ratio"],
            "argmax": diag["argmax"],
            "violation_total_4p": diag["violation_total"],
            "reproduces_published_max": diag["max_ratio"] == 3.9771715522,
        },
        "cross_checked_datapoints": {
            "published_max_197_14_6_1_0_17": round(direct_S(197, 14, 28, dl197, 6, 1, 17), 10),
            "extension_max_601_20_4_7_0_1": round(direct_S(601, 20, 40, dl601, 4, 7, 1), 10),
        },
    }


def render(cert: Dict[str, Any]) -> str:
    return json.dumps(cert, indent=2, sort_keys=True) + "\n"


def selftest() -> bool:
    dl = dlog_table(197)
    r = scan_case(197, 14, dl, "nonres", False, 1e-7)
    ok = abs(r["best_ratio"] - 3.2173609608) < 1e-9
    print(f"[selftest] nonres (197,14) best_ratio={r['best_ratio']} (expect 3.2173609608) -> {'OK' if ok else 'FAIL'}")
    dd = direct_S(601, 20, 40, dlog_table(601), 4, 7, 1)
    ok2 = abs(dd - 3.3516589468) < 1e-9
    print(f"[selftest] direct S(601,20,(4,7,0,1))/p={round(dd,10)} (expect 3.3516589468) -> {'OK' if ok2 else 'FAIL'}")
    return ok and ok2


def main() -> int:
    ap = argparse.ArgumentParser(description="M1 two-coordinate Kummer wall stdlib scan.")
    ap.add_argument("--certificate", action="store_true", help="emit the deterministic validation certificate")
    ap.add_argument("--output", type=Path, help="write the certificate JSON to this path")
    ap.add_argument("--check", type=Path, help="compare a stored certificate with a fresh run")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--scan", action="store_true", help="ad-hoc scan with the grid options below")
    ap.add_argument("--p-min", type=int, default=5)
    ap.add_argument("--p-max", type=int, default=500)
    ap.add_argument("--e-max", type=int, default=24)
    ap.add_argument("--mode", choices=("remaining", "asym", "nonres"), default="nonres")
    ap.add_argument("--diagonal-n", type=int, default=0)
    ap.add_argument("--tol", type=float, default=1e-7)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return 0 if selftest() else 1

    if args.check is not None:
        if args.check.read_text(encoding="utf-8") != render(build_certificate()):
            raise SystemExit(f"certificate mismatch: {args.check}")
        print(f"certificate matches: {args.check}")
        return 0

    if args.certificate or args.output is not None:
        cert = build_certificate()
        rendered = render(cert)
        if args.output is not None:
            args.output.write_text(rendered, encoding="utf-8")
        print(rendered, end="")
        ok = (cert["report_grid_nonres_p500_e24"]["reproduces_published_numpy"]
              and cert["diagonal_grid_n20_p500"]["reproduces_published_max"])
        return 0 if ok else 1

    t0 = time.monotonic()
    summ = summarize(run_grid(args.p_min, args.p_max, args.e_max, args.mode, args.diagonal_n, args.tol))
    summ["params"] = {"p_min": args.p_min, "p_max": args.p_max, "e_max": args.e_max,
                      "mode": args.mode, "diagonal_n": args.diagonal_n, "tol": args.tol}
    summ["elapsed_sec"] = round(time.monotonic() - t0, 2)
    if args.json:
        print(json.dumps(summ, indent=2, sort_keys=True))
    else:
        print(f"mode={args.mode} p<= {args.p_max} e<= {args.e_max} diag_n={args.diagonal_n}: "
              f"cases={summ['case_count']} scanned={summ['scanned_total']} "
              f"violations(4p)={summ['violation_total']} max_ratio={summ['max_ratio']} argmax={summ['argmax']}")
        for r in summ["top10"]:
            print(f"  ratio={r['best_ratio']:.8f} p={r['p']} e={r['e']} h={r['h']} "
                  f"tuple={tuple(r['best_tuple'])} lines={tuple(r['best_mono'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
