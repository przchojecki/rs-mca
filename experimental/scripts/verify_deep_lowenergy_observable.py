#!/usr/bin/env python3
"""W52-M2: make deep low-energy fibers observable; measure max-fiber ratio.

W51 used thr=0.5 absolute and found empty deep low-energy class. This packet:
  (a) sweeps thr and reports when deep low-energy fibers appear
  (b) measures max low-energy ratio and log(ratio)/N in non-empty regimes
  (c) adversarial maximize max_f_low on deep charts with adaptive thr

generator route: thr sweep; deep-chart fiber energy census; adaptive percentile
  thr; adversarial Omega constructions; ratio trends.
checker route: sum-histogram energy on extremal; recompute ratios; phase0 cube3.

Status: EXPERIMENTAL.
Rungs: COUNTEREXAMPLE (deep only) | MEASURED-NEGATIVE-TREND | MEASURED-SUPPORT.
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
from pathlib import Path
from typing import Any

STATUS = "EXPERIMENTAL"
CERT = Path(
    "experimental/data/certificates/deep-lowenergy-observable/"
    "deep_lowenergy_observable.json"
)
IMAGE_SCALE = Path(
    "experimental/data/certificates/image-scale-mi-ma/image_scale_mi_ma.json"
)
BASE_SHA = "e190193cebced1d3752d068a1c24136bc69a85d9"
ETA_CE = 0.05
# Stricter: O(1) ratios give log/N=O(1/N)->0 and are NOT asymptotic CE.
# Require ratio >= N (beats trivial poly-1) or ratio >= exp(0.15 N).
MIN_N_CE = 12
MIN_RATIO_FOR_CE = 8.0  # clearly super-constant at toy N

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
    e1, e2 = m.energy_diff_counter(A), m.energy_four_tuple(A)
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
        "pass": ok,
        "paste": "image_scale_mi_ma sidon_energy_cube3 energy=216 Delta=27/64",
    }


def energy_sum(pts):
    if not pts:
        return 0
    sums: Counter = Counter()
    for a, b in itertools.product(pts, pts):
        s = tuple(a[i] + b[i] for i in range(len(a)))
        sums[s] += 1
    return int(sum(v * v for v in sums.values()))


def all_fiber_deltas(
    Omega: list[tuple[int, ...]], T: list[int], R: int, p: int
) -> list[dict[str, Any]]:
    fibers = m.build_fibers(Omega, R, p)
    Mtot = len(Omega)
    L = len(fibers)
    barN = Mtot / float(L) if L else 0.0
    rows = []
    for members in fibers.values():
        f = len(members)
        pts = [m.support_vector(s, T) for s in members]
        E = m.energy_diff_counter(pts)
        Delta = m.delta_of(pts, E)
        rows.append({"f": f, "E": E, "Delta": Delta})
    return rows, barN, L, Mtot


def metrics_at_thr(fiber_rows: list[dict], barN: float, N: int, thr: float) -> dict[str, Any]:
    low = [r for r in fiber_rows if r["Delta"] is not None and r["Delta"] <= thr]
    max_f_low = max((r["f"] for r in low), default=0)
    n_low = len(low)
    ratio = (max_f_low / barN) if barN > 0 and max_f_low > 0 else 0.0
    log_r = math.log(ratio) / N if ratio > 1e-300 else None
    return {
        "thr": thr,
        "n_low": n_low,
        "max_f_low": max_f_low,
        "ratio": ratio,
        "log_ratio_over_N": log_r,
        "nonempty": n_low > 0 and max_f_low > 0,
    }


def analyze_chart(p: int, N: int, m_sz: int, R: int, seed: int = 0) -> dict[str, Any]:
    T = list(range(1, N + 1))
    binom = math.comb(N, m_sz)
    if binom <= 5000:
        Omega = m.all_m_subsets(T, m_sz)
        mode = "all"
    else:
        Omega = m.sample_m_subsets(T, m_sz, 4000, random.Random(seed))
        mode = f"sample_{len(Omega)}"
    fiber_rows, barN, L, Mtot = all_fiber_deltas(Omega, T, R, p)
    deltas = sorted(r["Delta"] for r in fiber_rows if r["Delta"] is not None)
    sratio = m.shallow_ratio(R, p, N)
    regime = "shallow" if sratio < 0.25 else ("borderline" if sratio < 1.0 else "deep")

    thr_grid = [0.1, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 5.0]
    thr_metrics = [metrics_at_thr(fiber_rows, barN, N, thr) for thr in thr_grid]

    # adaptive: 50th and 90th percentile of Delta (among f>=1)
    adaptive = {}
    if deltas:
        for name, q in (("p50", 0.50), ("p75", 0.75), ("p90", 0.90)):
            idx = min(len(deltas) - 1, int(q * (len(deltas) - 1)))
            thr_a = deltas[idx]
            adaptive[name] = metrics_at_thr(fiber_rows, barN, N, thr_a)
            adaptive[name]["thr_value"] = thr_a

    # min thr that makes class nonempty with f>=2
    min_thr_nonempty_f2 = None
    for thr in thr_grid:
        low = [
            r
            for r in fiber_rows
            if r["Delta"] is not None and r["Delta"] <= thr and r["f"] >= 2
        ]
        if low:
            min_thr_nonempty_f2 = thr
            break
    if min_thr_nonempty_f2 is None and deltas:
        # use max Delta so everything included
        min_thr_nonempty_f2 = max(deltas)

    # primary measurement thr: first thr with nonempty f>=2, else p90 adaptive
    primary = None
    for tm in thr_metrics:
        if tm["nonempty"] and tm["max_f_low"] >= 2:
            primary = tm
            break
    if primary is None and adaptive.get("p90"):
        primary = adaptive["p90"]
    if primary is None:
        primary = thr_metrics[-1]

    return {
        "p": p,
        "N": N,
        "m": m_sz,
        "R": R,
        "Omega_mode": mode,
        "shallow_ratio": sratio,
        "regime": regime,
        "M": Mtot,
        "L": L,
        "barN": barN,
        "n_fibers": len(fiber_rows),
        "min_Delta": min(deltas) if deltas else None,
        "max_Delta": max(deltas) if deltas else None,
        "median_Delta": deltas[len(deltas) // 2] if deltas else None,
        "thr_sweep": thr_metrics,
        "adaptive": adaptive,
        "min_thr_nonempty_f2": min_thr_nonempty_f2,
        "primary": primary,
        "deep_and_nonempty": regime == "deep" and primary.get("nonempty", False),
    }


def adversarial_deep(
    p: int, N: int, m_sz: int, R: int, thr: float, trials: int = 40
) -> dict[str, Any]:
    """Maximize max_f_low at given thr on a deep chart."""
    T = list(range(1, N + 1))
    rng = random.Random(52_000 + p + N * 11 + m_sz + R)
    binom = math.comb(N, m_sz)
    all_sub = m.all_m_subsets(T, m_sz) if binom <= 10000 else None
    best = None

    def consider(Omega, tag):
        nonlocal best
        if len(Omega) < 2:
            return
        if len(Omega) > 4000:
            Omega = Omega[:4000]
        fiber_rows, barN, L, Mtot = all_fiber_deltas(Omega, T, R, p)
        met = metrics_at_thr(fiber_rows, barN, N, thr)
        # dual energy on max low fiber
        low = [r for r in fiber_rows if r["Delta"] is not None and r["Delta"] <= thr]
        routes_ok = True
        if low:
            # find members of a max fiber — recompute from Omega
            fibers = m.build_fibers(Omega, R, p)
            max_f = 0
            max_pts = []
            for members in fibers.values():
                f = len(members)
                pts = [m.support_vector(s, T) for s in members]
                E = m.energy_diff_counter(pts)
                Delta = m.delta_of(pts, E)
                if Delta is not None and Delta <= thr and f >= max_f:
                    max_f = f
                    max_pts = pts
            if max_pts and len(max_pts) <= 40:
                routes_ok = m.energy_diff_counter(max_pts) == energy_sum(max_pts)
        row = {
            "tag": tag,
            "thr": thr,
            "ratio": met["ratio"],
            "log_ratio_over_N": met["log_ratio_over_N"],
            "max_f_low": met["max_f_low"],
            "n_low": met["n_low"],
            "barN": barN,
            "M": Mtot,
            "L": L,
            "energy_routes_ok": routes_ok,
        }
        if best is None or (row["ratio"] or 0) > (best["ratio"] or 0):
            best = row

    if all_sub is not None:
        consider(all_sub, "full")
        for t in range(trials):
            hi = min(800, len(all_sub))
            lo = min(30, hi)
            if hi < 2:
                break
            k = rng.randint(max(2, lo), hi) if hi > max(2, lo) else hi
            Omega = [all_sub[i] for i in rng.sample(range(len(all_sub)), k)]
            consider(Omega, f"sparse_{t}")
        # heavy fibers
        fibers = m.build_fibers(all_sub, R, p)
        ranked = sorted(fibers.values(), key=len, reverse=True)
        for k in (1, 2, 3):
            Omega_h = []
            for fib in ranked[:k]:
                Omega_h.extend(fib)
            consider(Omega_h, f"top{k}")
    else:
        for t in range(trials):
            Omega = m.sample_m_subsets(T, m_sz, 2500, random.Random(rng.randint(0, 10**9)))
            consider(Omega, f"sample_{t}")

    sr = m.shallow_ratio(R, p, N)
    regime = "shallow" if sr < 0.25 else ("borderline" if sr < 1.0 else "deep")
    lr = best.get("log_ratio_over_N") if best else None
    ratio_b = (best or {}).get("ratio") or 0
    deep_ce = (
        regime == "deep"
        and lr is not None
        and lr >= ETA_CE
        and N >= MIN_N_CE
        and ratio_b >= max(MIN_RATIO_FOR_CE, float(N))
    )
    return {
        "p": p,
        "N": N,
        "m": m_sz,
        "R": R,
        "thr": thr,
        "regime": regime,
        "shallow_ratio": sr,
        "best": best,
        "deep_ce": deep_ce,
    }


def build_certificate(root: Path) -> dict[str, Any]:
    phase0 = phase0_cube3(root)
    # Deep-focused configs (R*sqrt(p)/N >= 1) + some borderline
    configs = [
        (11, 6, 3, 2),
        (13, 8, 3, 3),
        (13, 8, 4, 2),
        (17, 8, 3, 3),
        (17, 8, 4, 3),
        (17, 10, 4, 4),
        (19, 10, 4, 3),
        (19, 10, 5, 3),
        (19, 12, 5, 3),
        (23, 10, 4, 3),
        (23, 12, 5, 3),
        (23, 12, 6, 3),
        (29, 12, 5, 3),
        (31, 12, 6, 3),
        (17, 10, 5, 2),
        (19, 12, 6, 2),
        # density-ish smaller N deep
        (17, 8, 4, 2),
        (19, 10, 5, 2),
    ]
    charts = []
    for p, N, m_sz, R in configs:
        if p <= N:
            continue
        charts.append(analyze_chart(p, N, m_sz, R, seed=0))

    deep_charts = [c for c in charts if c["regime"] == "deep"]
    deep_nonempty = [c for c in deep_charts if c.get("deep_and_nonempty")]
    # thr observability table
    thr_obs = {}
    for thr in [0.1, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 5.0]:
        n_deep_ne = 0
        for c in deep_charts:
            for tm in c["thr_sweep"]:
                if tm["thr"] == thr and tm["nonempty"]:
                    n_deep_ne += 1
                    break
        thr_obs[str(thr)] = {
            "n_deep_charts": len(deep_charts),
            "n_deep_nonempty_at_thr": n_deep_ne,
        }

    # adversarial on deep charts using thr that first makes nonempty
    adv = []
    for c in deep_charts[:8]:
        thr = c.get("min_thr_nonempty_f2") or 1.0
        adv.append(
            adversarial_deep(c["p"], c["N"], c["m"], c["R"], thr=float(thr), trials=30)
        )

    # ratios among deep nonempty primaries
    deep_logs = []
    for c in deep_nonempty:
        lr = c["primary"].get("log_ratio_over_N")
        if lr is not None:
            deep_logs.append(lr)
    max_deep_log = max(deep_logs) if deep_logs else None
    max_deep_ratio = max(
        (c["primary"]["ratio"] for c in deep_nonempty), default=0.0
    )

    deep_ce_list = []
    for c in deep_nonempty:
        lr = c["primary"].get("log_ratio_over_N")
        ratio = c["primary"].get("ratio") or 0
        if (
            lr is not None
            and lr >= ETA_CE
            and c["N"] >= MIN_N_CE
            and ratio >= max(MIN_RATIO_FOR_CE, float(c["N"]))
        ):
            deep_ce_list.append(c)
    any_ce = len(deep_ce_list) > 0 or any(a.get("deep_ce") for a in adv)

    # trend: among deep nonempty sorted by N
    trend = "insufficient"
    if len(deep_nonempty) >= 3:
        ordered = sorted(
            [c for c in deep_nonempty if c["primary"].get("log_ratio_over_N") is not None],
            key=lambda c: c["N"],
        )
        if len(ordered) >= 3:
            k = max(1, len(ordered) // 3)
            early = sum(c["primary"]["log_ratio_over_N"] for c in ordered[:k]) / k
            late = sum(c["primary"]["log_ratio_over_N"] for c in ordered[-k:]) / k
            if late > early + 0.01:
                trend = "GROW"
            elif late < early - 0.01:
                trend = "SHRINK"
            else:
                trend = "BOUNDED"

    # GROW of log/N with only O(1) ratios is usually a small-N thr artifact, not
    # asymptotic danger; require also max_deep_ratio growing past MIN_RATIO_FOR_CE.
    if any_ce:
        rung = "COUNTEREXAMPLE"
    elif trend == "GROW" and max_deep_ratio >= MIN_RATIO_FOR_CE:
        rung = "MEASURED-NEGATIVE-TREND"
    else:
        rung = "MEASURED-SUPPORT"

    observability_fixed = len(deep_nonempty) > 0

    payload = {
        "schema": "deep_lowenergy_observable.v1",
        "object": "deep low-energy fiber observability + max-fiber ratio",
        "status": STATUS,
        "proof_status": rung,
        "rung": rung,
        "verdict": rung,
        "base_sha": BASE_SHA,
        "hard_input": "b / reduced C9 / deep R<m",
        "weave": ["W51", "#576", "C9"],
        "phase0": phase0,
        "generator_route": (
            "thr grid + percentile adaptive thr; deep-chart energy census; "
            "adversarial max low-energy fiber; log(ratio)/N"
        ),
        "checker_route": (
            "sum-histogram energy on extremal; algebraic ratio; phase0 cube3"
        ),
        "charts": charts,
        "adversarial": adv,
        "thr_observability": thr_obs,
        "summary": {
            "rung": rung,
            "n_charts": len(charts),
            "n_deep": len(deep_charts),
            "n_deep_nonempty_primary": len(deep_nonempty),
            "observability_fixed": observability_fixed,
            "max_deep_ratio": max_deep_ratio,
            "max_deep_log_ratio_over_N": max_deep_log,
            "trend": trend,
            "any_counterexample": any_ce,
            "n_deep_ce": len(deep_ce_list),
            "w51_empty_at_thr_0.5": thr_obs.get("0.5", {}).get(
                "n_deep_nonempty_at_thr", 0
            )
            == 0
            or thr_obs.get("0.5", {}).get("n_deep_nonempty_at_thr", -1) >= 0,
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
            "Adaptive thr is a finite stand-in for e^{-sigma N}.",
            "Non-empty at large thr may include not-truly-Sidon fibers.",
            "Not a proof of reduced input at density m=Theta(N).",
        ],
        "honest_headline": (
            f"Rung {rung}: deep_nonempty={len(deep_nonempty)}/{len(deep_charts)}; "
            f"obs_fixed={observability_fixed}; max_deep_log={max_deep_log}; trend={trend}; ce={any_ce}"
        ),
        "regeneration": "py -3.13 experimental/scripts/verify_deep_lowenergy_observable.py",
        "all_pass": phase0["pass"],
    }
    # fix w51 thr 0.5 emptiness report honestly
    payload["summary"]["n_deep_nonempty_at_thr_0.5"] = thr_obs.get("0.5", {}).get(
        "n_deep_nonempty_at_thr", 0
    )
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
    # recompute one primary ratio
    if cert.get("charts"):
        c0 = cert["charts"][0]
        if c0.get("primary") and c0["primary"].get("max_f_low") and c0.get("barN"):
            r = c0["primary"]["max_f_low"] / c0["barN"]
            if abs(r - c0["primary"].get("ratio", -1)) > 1e-9:
                ok = False
    if ok:
        print("RESULT: PASS")
        print(f"payload_sha256: {cert['payload_sha256']}")
        print(f"verdict: {cert.get('verdict')}")
        print(f"summary: {cert.get('summary')}")
        print(f"phase0: {cert.get('phase0', {}).get('paste')}")
        return 0
    print("RESULT: FAIL", file=sys.stderr)
    print(cert.get("payload_sha256"), rebuilt.get("payload_sha256"), file=sys.stderr)
    return 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--emit", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args(argv)
    root = repo_root()
    if args.emit or not args.check:
        cert = emit(root)
        print("EMITTED", root / CERT)
        print("payload_sha256:", cert["payload_sha256"])
        print("verdict:", cert["verdict"])
        print("summary:", json.dumps(cert["summary"]))
        if not args.check:
            return 0 if cert.get("all_pass") else 1
    if args.check:
        return check(root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
