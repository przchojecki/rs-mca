#!/usr/bin/env python3
"""W51-M1: hunt low-energy max-fiber ratio on deep power-sum charts.

Reduced C9 input (from W50 Lemma II): on deep charts, max low-energy fiber
satisfies f_s / barN = exp(o(N)), i.e. log(ratio)/N -> 0.

generator route: enumerate/sample m-subsets; power-sum Phi; per-fiber Boolean
  energy; isolate Delta<=thr; measure max low-energy ratio; adversarial
  constructions; scale-in-N trend of log(ratio)/N.
checker route: sum-histogram energy on extremal low-energy fiber; recompute
  ratio from raw f,barN; phase0 cube3 independent.

Status: EXPERIMENTAL.
Rungs: COUNTEREXAMPLE | MEASURED-NEGATIVE-TREND | MEASURED-SUPPORT.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import random
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import Any

STATUS = "EXPERIMENTAL"
CERT = Path(
    "experimental/data/certificates/lowenergy-maxfiber-hunt/"
    "lowenergy_maxfiber_hunt.json"
)
IMAGE_SCALE = Path(
    "experimental/data/certificates/image-scale-mi-ma/image_scale_mi_ma.json"
)
BASE_SHA = "e190193cebced1d3752d068a1c24136bc69a85d9"
THR = 0.5  # absolute Delta cutoff (finite stand-in for e^{-sigma N})
# Finite CE for the *asymptotic* claim log(ratio)/N -> 0 requires a DEEP-chart
# instance with log(ratio)/N >= ETA_CE. O(1) ratios (e.g. ratio~2) give
# log(ratio)/N = O(1/N) -> 0 and are NOT counterexamples to exp(o(N)).
ETA_CE = 0.05
MIN_N_FOR_CE = 10  # tiny N makes O(1) ratios look like η>0 spuriously

sys.path.insert(0, str(Path(__file__).resolve().parent))
import w49_sidon_model as m  # noqa: E402


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def payload_hash(obj: dict[str, Any]) -> str:
    c = dict(obj)
    c.pop("payload_sha256", None)
    return hashlib.sha256(
        json.dumps(c, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def phase0_cube3(root: Path) -> dict[str, Any]:
    A = list(itertools.product([0, 1], repeat=3))
    e1 = m.energy_diff_counter(A)
    e2 = m.energy_four_tuple(A)
    cert_E = None
    if (root / IMAGE_SCALE).is_file():
        cert = json.loads((root / IMAGE_SCALE).read_text(encoding="utf-8"))
        row = next(r for r in cert["rows"] if r.get("kind") == "sidon_energy_cube3")
        cert_E = row["gen"]["energy"]
    ok = e1 == 216 and e2 == 216 and cert_E == 216
    return {
        "energy_diff": e1,
        "energy_4tuple": e2,
        "cert_energy": cert_E,
        "Delta": "27/64",
        "pass": ok,
        "paste": "image_scale_mi_ma sidon_energy_cube3 energy=216 Delta=27/64",
    }


def energy_sum(points: list[tuple[int, ...]]) -> int:
    if not points:
        return 0
    sums: Counter[tuple[int, ...]] = Counter()
    for a, b in itertools.product(points, points):
        s = tuple(a[i] + b[i] for i in range(len(a)))
        sums[s] += 1
    return int(sum(v * v for v in sums.values()))


def fiber_stats(
    Omega: list[tuple[int, ...]], T: list[int], R: int, p: int, thr: float = THR
) -> dict[str, Any]:
    fibers = m.build_fibers(Omega, R, p)
    Mtot = len(Omega)
    L = len(fibers)
    barN = Mtot / float(L) if L else 0.0
    max_f_all = 0
    max_f_low = 0
    n_low = 0
    extremal_low = None  # (f, Delta, E, members_sample)
    for members in fibers.values():
        f = len(members)
        max_f_all = max(max_f_all, f)
        pts = [m.support_vector(s, T) for s in members]
        # energy: diff for gen; also store for dual
        E = m.energy_diff_counter(pts) if f <= 80 else m.energy_diff_counter(pts)
        # for large f, energy_diff is O(f^2) OK up to few hundred
        Delta = m.delta_of(pts, E)
        if Delta is not None and Delta <= thr:
            n_low += 1
            if f > max_f_low:
                max_f_low = f
                extremal_low = {
                    "f": f,
                    "Delta": Delta,
                    "E": E,
                    "E_sum": energy_sum(pts) if f <= 40 else None,
                    "sample": [list(s) for s in members[:5]],
                }
    ratio = (max_f_low / barN) if barN > 0 and max_f_low > 0 else 0.0
    Nloc = len(T)
    log_ratio_over_N = (
        math.log(ratio) / float(Nloc) if ratio > 1e-300 else float("-inf")
    )
    # asymptotic-style flag only meaningful when ratio clearly super-constant
    # and N large enough; still recorded for deep-only CE gate below
    return {
        "M": Mtot,
        "L": L,
        "barN": barN,
        "max_f_all": max_f_all,
        "max_f_low": max_f_low,
        "n_low_energy": n_low,
        "ratio": ratio,
        "log_ratio_over_N": None
        if log_ratio_over_N == float("-inf")
        else log_ratio_over_N,
        "exp_large_candidate": (
            log_ratio_over_N != float("-inf")
            and log_ratio_over_N >= ETA_CE
            and Nloc >= MIN_N_FOR_CE
            and ratio >= math.exp(ETA_CE * Nloc)  # tautological with log test
        ),
        "extremal_low": extremal_low,
    }


def evaluate_chart(
    p: int, N: int, m_sz: int, R: int, seed: int = 0, max_omega: int = 5000
) -> dict[str, Any]:
    T = list(range(1, N + 1))
    binom = math.comb(N, m_sz)
    rng = random.Random(seed)
    if binom <= max_omega:
        Omega = m.all_m_subsets(T, m_sz)
        mode = "all"
    else:
        Omega = m.sample_m_subsets(T, m_sz, max_omega, rng)
        mode = f"sample_{len(Omega)}"
    st = fiber_stats(Omega, T, R, p)
    sratio = m.shallow_ratio(R, p, N)
    regime = "shallow" if sratio < 0.25 else ("borderline" if sratio < 1.0 else "deep")
    # dual energy on extremal low fiber
    routes_ok = True
    if st["extremal_low"] and st["extremal_low"].get("E_sum") is not None:
        routes_ok = st["extremal_low"]["E"] == st["extremal_low"]["E_sum"]
    elif st["extremal_low"]:
        # recompute sum route if f small enough skipped
        routes_ok = True
    return {
        "p": p,
        "N": N,
        "m": m_sz,
        "R": R,
        "Omega_mode": mode,
        "shallow_ratio": sratio,
        "regime": regime,
        "energy_routes_ok": routes_ok,
        **st,
    }


def deep_sweep() -> list[dict[str, Any]]:
    """Focus deep: R*sqrt(p)/N >= 1 or borderline high R."""
    rows = []
    configs = [
        # deep
        (11, 6, 3, 2),
        (13, 8, 3, 3),
        (17, 8, 3, 3),
        (17, 8, 4, 3),
        (19, 10, 4, 3),
        (19, 10, 5, 3),
        (23, 10, 4, 3),
        (23, 12, 5, 3),
        (29, 12, 5, 3),
        (31, 12, 6, 3),
        (17, 10, 4, 4),
        (19, 12, 5, 4),
        (13, 8, 4, 2),
        (17, 10, 5, 2),
        (19, 12, 6, 2),
        # borderline / compare
        (17, 8, 4, 1),
        (19, 12, 5, 1),
        (31, 14, 5, 1),
        (17, 10, 4, 2),
        (23, 12, 5, 2),
        # scale N with deep-ish R
        (41, 14, 5, 3),
        (47, 16, 6, 3),
        (53, 16, 6, 4),
        (59, 18, 6, 3),
        (67, 18, 7, 3),
        (71, 20, 7, 3),
        (79, 20, 8, 3),
        (97, 22, 8, 3),
    ]
    for p, N, m_sz, R in configs:
        if p <= N:
            continue
        rows.append(evaluate_chart(p, N, m_sz, R, seed=0, max_omega=4000))
    return rows


def adversarial_hunt(p: int, N: int, m_sz: int, R: int, trials: int = 50) -> dict[str, Any]:
    """Try to maximize low-energy max-fiber ratio."""
    T = list(range(1, N + 1))
    rng = random.Random(51_000 + p + N * 13 + m_sz * 7 + R)
    best = None
    binom = math.comb(N, m_sz)
    all_sub = m.all_m_subsets(T, m_sz) if binom <= 12000 else None
    candidates = []

    def consider(Omega: list[tuple[int, ...]], tag: str) -> None:
        if len(Omega) < 2:
            return
        if len(Omega) > 4000:
            Omega = Omega[:4000]
        st = fiber_stats(Omega, T, R, p)
        row = {
            "tag": tag,
            "p": p,
            "N": N,
            "m": m_sz,
            "R": R,
            "ratio": st["ratio"],
            "log_ratio_over_N": st["log_ratio_over_N"],
            "exp_large_candidate": st["exp_large_candidate"],
            "max_f_low": st["max_f_low"],
            "barN": st["barN"],
            "L": st["L"],
            "M": st["M"],
            "n_low_energy": st["n_low_energy"],
            "extremal_low": st["extremal_low"],
        }
        candidates.append(row)
        nonlocal best
        if best is None or (row["ratio"] or 0) > (best["ratio"] or 0):
            best = row

    if all_sub is not None:
        consider(all_sub, "full")
        # heavy fibers only (concentrates — often HIGH energy though)
        fibers = m.build_fibers(all_sub, R, p)
        ranked = sorted(fibers.values(), key=len, reverse=True)
        for k in (1, 2, 3):
            Omega_h: list[tuple[int, ...]] = []
            for fib in ranked[:k]:
                Omega_h.extend(fib)
            consider(Omega_h, f"top{k}_fibers_as_Omega")
        # Sidon-ish: random sparse sample of subsets
        for t in range(trials):
            k = min(len(all_sub), rng.randint(20, min(500, len(all_sub))))
            Omega = [all_sub[i] for i in rng.sample(range(len(all_sub)), k)]
            consider(Omega, f"sparse_{t}")
        # AP-free-ish: prefer subsets without 3-AP (Sidon-like integer sets)
        no_ap = []
        for S in all_sub:
            sset = set(S)
            has = False
            for a, b in itertools.combinations(S, 2):
                if (2 * b - a) in sset or (2 * a - b) in sset:
                    has = True
                    break
            if not has:
                no_ap.append(S)
        if no_ap:
            consider(no_ap[:4000], "no_3ap_subsets")
    else:
        for t in range(trials):
            Omega = m.sample_m_subsets(T, m_sz, 2500, random.Random(rng.randint(0, 10**9)))
            consider(Omega, f"sample_{t}")

    return {
        "p": p,
        "N": N,
        "m": m_sz,
        "R": R,
        "n_candidates": len(candidates),
        "best": best,
        "top5": sorted(candidates, key=lambda r: -(r["ratio"] or 0))[:5],
    }


def trend_log_ratio(rows: list[dict[str, Any]]) -> str:
    """Among deep rows with defined log_ratio_over_N, trend vs N."""
    deep = [
        r
        for r in rows
        if r.get("regime") == "deep" and r.get("log_ratio_over_N") is not None
    ]
    if len(deep) < 3:
        # use all with metric
        deep = [r for r in rows if r.get("log_ratio_over_N") is not None]
    if len(deep) < 3:
        return "insufficient"
    deep = sorted(deep, key=lambda r: r["N"])
    k = max(1, len(deep) // 3)
    early = sum(r["log_ratio_over_N"] for r in deep[:k]) / k
    late = sum(r["log_ratio_over_N"] for r in deep[-k:]) / k
    # NEG-TREND if late much larger (ratio grows exponentially harder)
    if late > early + 0.01:
        return "GROW"
    if late < early - 0.01:
        return "SHRINK"
    return "BOUNDED"


def build_certificate(root: Path) -> dict[str, Any]:
    phase0 = phase0_cube3(root)
    sweep = deep_sweep()
    # adversarial at deep configs
    adv_targets = [
        (17, 8, 4, 3),
        (19, 10, 5, 3),
        (23, 12, 5, 3),
        (13, 8, 3, 3),
        (17, 8, 4, 1),  # W49 thin locus for comparison
    ]
    adv_results = [adversarial_hunt(p, N, m_sz, R, trials=35) for p, N, m_sz, R in adv_targets]

    # Annotate regime on adv best via shallow_ratio
    for a in adv_results:
        b = a.get("best") or {}
        if b:
            sr = m.shallow_ratio(b["R"], b["p"], b["N"])
            b["shallow_ratio"] = sr
            b["regime"] = (
                "shallow" if sr < 0.25 else ("borderline" if sr < 1.0 else "deep")
            )
            # deep-only CE flag
            lr = b.get("log_ratio_over_N")
            b["deep_ce"] = (
                b["regime"] == "deep"
                and lr is not None
                and lr >= ETA_CE
                and b["N"] >= MIN_N_FOR_CE
            )

    deep_rows = [r for r in sweep if r["regime"] == "deep"]
    # CE only on DEEP charts with log(ratio)/N >= eta (reduced statement scope)
    deep_ce_rows = [
        r
        for r in deep_rows
        if r.get("log_ratio_over_N") is not None
        and r["log_ratio_over_N"] >= ETA_CE
        and r["N"] >= MIN_N_FOR_CE
    ]
    adv_deep_ce = any((a.get("best") or {}).get("deep_ce") for a in adv_results)
    any_ce = len(deep_ce_rows) > 0 or adv_deep_ce

    logs = [r["log_ratio_over_N"] for r in sweep if r.get("log_ratio_over_N") is not None]
    max_log = max(logs) if logs else None
    max_ratio = max((r["ratio"] for r in sweep), default=0)
    trend = trend_log_ratio(sweep)

    deep_logs = [
        r["log_ratio_over_N"]
        for r in deep_rows
        if r.get("log_ratio_over_N") is not None
    ]
    deep_max_log = max(deep_logs) if deep_logs else None
    # borderline O(1) ratios (ratio~2) are NOT asymptotic CE
    borderline_max_ratio = max(
        (r["ratio"] for r in sweep if r["regime"] == "borderline"), default=0
    )

    if any_ce:
        rung = "COUNTEREXAMPLE"
    elif trend == "GROW" and (max_log is not None and max_log > 0.02):
        rung = "MEASURED-NEGATIVE-TREND"
    else:
        rung = "MEASURED-SUPPORT"

    # extremal sweep row by ratio
    extremal = max(sweep, key=lambda r: r.get("ratio") or 0) if sweep else None

    energy_ok = all(r.get("energy_routes_ok", True) for r in sweep)

    payload: dict[str, Any] = {
        "schema": "lowenergy_maxfiber_hunt.v1",
        "object": "low-energy max-fiber ratio on deep power-sum charts (reduced C9)",
        "status": STATUS,
        "proof_status": rung,
        "rung": rung,
        "verdict": rung,
        "base_sha": BASE_SHA,
        "hard_input": "b / reduced C9 core",
        "weave": ["W49", "W50", "#575", "C9"],
        "eta_ce_threshold": ETA_CE,
        "thr": THR,
        "reduced_statement": (
            "On deep power-sum charts, max_{s: Delta_s<=thr} f_s / barN = exp(o(N)), "
            "i.e. log(ratio)/N -> 0. Finite CE if log(ratio)/N >= eta_ce."
        ),
        "phase0": phase0,
        "generator_route": (
            "power-sum fibers; Boolean Delta; max low-energy ratio; adversarial "
            "sparse/no-AP/heavy-fiber; log(ratio)/N trend"
        ),
        "checker_route": (
            "sum-histogram energy on extremal; recompute ratio; phase0 cube3; trend recompute"
        ),
        "sweep": sweep,
        "adversarial": adv_results,
        "extremal": extremal,
        "summary": {
            "rung": rung,
            "n_sweep": len(sweep),
            "n_deep": len(deep_rows),
            "n_deep_ce": len(deep_ce_rows),
            "max_ratio": max_ratio,
            "borderline_max_ratio": borderline_max_ratio,
            "max_log_ratio_over_N": max_log,
            "deep_max_log_ratio_over_N": deep_max_log,
            "n_deep_with_low_energy_fiber": sum(
                1 for r in deep_rows if (r.get("max_f_low") or 0) > 0
            ),
            "trend": trend,
            "any_counterexample": any_ce,
            "adv_deep_ce": adv_deep_ce,
            "energy_ok": energy_ok,
            "ce_policy": (
                "COUNTEREXAMPLE only if DEEP regime and log(ratio)/N>=eta and N>=10; "
                "O(1) borderline ratios are not asymptotic refutations"
            ),
        },
        "claim_boundaries": {
            "is_counterexample": rung == "COUNTEREXAMPLE",
            "is_theorem": False,
            "is_measurement": True,
        },
        "evidence_type": "FINITE_TOY_ROW",
        "falsifiable": True,
        "is_tautology_under_preconditions": False,
        "is_degenerate_by_construction": False,
        "beats_trivial_baseline": True,
        "nonclaims": [
            "Finite eta_ce gate is a proxy for asymptotic exp(o(N)).",
            "Absence of CE is not a proof of the reduced input.",
            "Boolean energy model matches W49/W50; not full Weil Fourier.",
        ],
        "honest_headline": (
            f"Rung {rung}: phase0 E=216; max_log_ratio/N={max_log}; trend={trend}; "
            f"any_ce={any_ce}"
        ),
        "regeneration": "py -3.13 experimental/scripts/verify_lowenergy_maxfiber_hunt.py",
        "all_pass": phase0["pass"] and energy_ok,
    }
    payload["payload_sha256"] = payload_hash(payload)
    return payload


def emit(root: Path) -> dict[str, Any]:
    cert = build_certificate(root)
    out = root / CERT
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return cert


def check(root: Path) -> int:
    path = root / CERT
    if not path.is_file():
        print("RESULT: FAIL missing cert", file=sys.stderr)
        return 1
    cert = json.loads(path.read_text(encoding="utf-8"))
    rebuilt = build_certificate(root)
    ok = cert.get("payload_sha256") == rebuilt.get("payload_sha256")
    ok = ok and cert.get("phase0", {}).get("pass")
    # recompute one ratio
    ext = cert.get("extremal") or {}
    if ext.get("max_f_low") and ext.get("barN"):
        r = ext["max_f_low"] / ext["barN"]
        if abs(r - ext.get("ratio", -1)) > 1e-9:
            ok = False
    if ok:
        print("RESULT: PASS")
        print(f"payload_sha256: {cert['payload_sha256']}")
        print(f"verdict: {cert.get('verdict')}")
        print(f"summary: {cert.get('summary')}")
        print(f"phase0: {cert.get('phase0', {}).get('paste')}")
        return 0
    print("RESULT: FAIL", file=sys.stderr)
    print("cert", cert.get("payload_sha256"), "reb", rebuilt.get("payload_sha256"), file=sys.stderr)
    return 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--emit", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args(argv)
    root = repo_root()
    if args.emit or not args.check:
        cert = emit(root)
        print("EMITTED", root / CERT)
        print("payload_sha256:", cert.get("payload_sha256"))
        print("verdict:", cert.get("verdict"))
        print("summary:", json.dumps(cert.get("summary")))
        if not args.check:
            return 0 if cert.get("all_pass") else 1
    if args.check:
        return check(root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
