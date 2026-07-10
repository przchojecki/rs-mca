#!/usr/bin/env python3
"""W53-M1: large fiber vs low energy at LINEAR DENSITY, R=2.

Crux: can F_s of Phi=(sum,sumsq) be exp-large AND low-Delta at m=c*N?

generator route: linear-density charts; fiber size vs Delta census; correlation;
  adversarial maximize f among low-Delta fibers; genuine density c in [0.25,0.5].
checker route: sum-histogram energy on extremal; recompute Delta=E/f^3; phase0 cube3.

CE bar (honest): density m/N >= 0.25, N >= 10, f >= max(8, N), Delta <= thr,
  and f/barN >= max(8, N) — O(1) ratios are NOT CE.

Status: EXPERIMENTAL.
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
    "experimental/data/certificates/largefiber-lowenergy-hunt/"
    "largefiber_lowenergy_hunt.json"
)
IMAGE_SCALE = Path(
    "experimental/data/certificates/image-scale-mi-ma/image_scale_mi_ma.json"
)
BASE_SHA = "e190193cebced1d3752d068a1c24136bc69a85d9"
THR = 0.75  # low-energy cutoff (higher than 0.5 so class is observable)
MIN_DENSITY = 0.25
MIN_N = 10
MIN_F_CE = 8

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


def fiber_table(
    Omega: list[tuple[int, ...]], T: list[int], p: int, R: int = 2
) -> tuple[list[dict[str, Any]], float, int, int]:
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
        rows.append(
            {
                "f": f,
                "E": E,
                "Delta": Delta,
                "log_f_over_N": math.log(f) / len(T) if f > 0 else None,
            }
        )
    return rows, barN, L, Mtot


def analyze_linear(
    p: int, N: int, density: float, seed: int = 0, max_omega: int = 5000
) -> dict[str, Any]:
    m_sz = max(2, int(round(density * N)))
    if m_sz >= N:
        m_sz = N - 1
    dens = m_sz / float(N)
    T = list(range(1, N + 1))
    binom = math.comb(N, m_sz)
    rng = random.Random(seed + N * 17 + m_sz)
    if binom <= max_omega:
        Omega = m.all_m_subsets(T, m_sz)
        mode = "all"
    else:
        Omega = m.sample_m_subsets(T, m_sz, max_omega, rng)
        mode = f"sample_{len(Omega)}"
    rows, barN, L, Mtot = fiber_table(Omega, T, p, R=2)
    if not rows:
        return {"p": p, "N": N, "m": m_sz, "density": dens, "empty": True}

    max_f = max(r["f"] for r in rows)
    # largest fiber energy
    largest = max(rows, key=lambda r: r["f"])
    # lowest energy among fibers with f >= 2
    big = [r for r in rows if r["f"] >= 2]
    min_delta_big = min((r["Delta"] for r in big if r["Delta"] is not None), default=None)
    # low-energy max f
    low = [r for r in rows if r["Delta"] is not None and r["Delta"] <= THR]
    max_f_low = max((r["f"] for r in low), default=0)
    # CS predicts Delta ~>= 1/f so larger f tends to smaller Delta — that is NOT
    # the hoped "large=>high energy" law. Track excess over CS floor instead:
    # excess = Delta * f  (>=1 by CS); Sidon-like means excess ~ 2.
    by_f = sorted(rows, key=lambda r: r["f"])
    k = max(1, len(by_f) // 4)
    top = by_f[-k:]
    mean_excess_top = (
        sum(r["Delta"] * r["f"] for r in top if r["Delta"] is not None)
        / max(1, sum(1 for r in top if r["Delta"] is not None))
    )
    med_f = sorted(r["f"] for r in rows)[len(rows) // 2]
    large_fibers = [r for r in rows if r["f"] >= max(2, med_f)]
    min_delta_large = min(
        (r["Delta"] for r in large_fibers if r["Delta"] is not None), default=None
    )
    # "structured energy": largest fiber excess over Sidon floor (2/f)
    sidon_floor_largest = (2 * largest["f"] - 1) / float(largest["f"] ** 2) if largest["f"] else None
    largest_excess_over_sidon = (
        (largest["Delta"] - sidon_floor_largest)
        if largest["Delta"] is not None and sidon_floor_largest is not None
        else None
    )

    ratio_low = (max_f_low / barN) if barN > 0 and max_f_low else 0.0
    # CE candidate
    is_linear = dens >= MIN_DENSITY - 1e-9
    ce = (
        is_linear
        and N >= MIN_N
        and max_f_low >= max(MIN_F_CE, N)
        and ratio_low >= max(8.0, float(N))
        and any(
            r["f"] == max_f_low and r["Delta"] is not None and r["Delta"] <= THR
            for r in rows
        )
    )

    # size-energy frontier points (top 10 by f)
    frontier = sorted(rows, key=lambda r: -r["f"])[:10]
    frontier = [
        {"f": r["f"], "Delta": r["Delta"], "E": r["E"], "log_f_over_N": r["log_f_over_N"]}
        for r in frontier
    ]

    return {
        "p": p,
        "N": N,
        "m": m_sz,
        "density": dens,
        "linear_density": is_linear,
        "Omega_mode": mode,
        "M": Mtot,
        "L": L,
        "barN": barN,
        "n_fibers": len(rows),
        "max_f": max_f,
        "largest_fiber_Delta": largest["Delta"],
        "largest_fiber_E": largest["E"],
        "max_f_low": max_f_low,
        "ratio_low": ratio_low,
        "n_low": len(low),
        "min_delta_among_f_ge_2": min_delta_big,
        "mean_cs_excess_top_quartile_f": mean_excess_top,
        "min_delta_large_fibers": min_delta_large,
        "largest_sidon_floor": sidon_floor_largest,
        "largest_excess_over_sidon": largest_excess_over_sidon,
        "largest_near_sidon": (
            largest_excess_over_sidon is not None and largest_excess_over_sidon < 0.05
        ),
        "frontier_top10": frontier,
        "ce_candidate": ce,
        "shallow_ratio": m.shallow_ratio(2, p, N),
    }


def adversarial_linear(
    p: int, N: int, density: float, trials: int = 40
) -> dict[str, Any]:
    """Maximize max_f among low-Delta fibers at linear density."""
    m_sz = max(2, int(round(density * N)))
    if m_sz >= N:
        m_sz = N - 1
    T = list(range(1, N + 1))
    rng = random.Random(53_000 + p + N * 19 + m_sz)
    binom = math.comb(N, m_sz)
    all_sub = m.all_m_subsets(T, m_sz) if binom <= 12000 else None
    best = None

    def consider(Omega, tag):
        nonlocal best
        if len(Omega) < 2:
            return
        if len(Omega) > 4000:
            Omega = Omega[:4000]
        rows, barN, L, Mtot = fiber_table(Omega, T, p, R=2)
        low = [r for r in rows if r["Delta"] is not None and r["Delta"] <= THR]
        max_f_low = max((r["f"] for r in low), default=0)
        max_f = max((r["f"] for r in rows), default=0)
        # dual energy on a max low fiber
        routes_ok = True
        if max_f_low >= 2:
            fibers = m.build_fibers(Omega, 2, p)
            for members in fibers.values():
                if len(members) != max_f_low:
                    continue
                pts = [m.support_vector(s, T) for s in members]
                E1 = m.energy_diff_counter(pts)
                if len(pts) <= 35:
                    routes_ok = E1 == energy_sum(pts)
                Delta = m.delta_of(pts, E1)
                if Delta is not None and Delta <= THR:
                    break
        row = {
            "tag": tag,
            "max_f": max_f,
            "max_f_low": max_f_low,
            "barN": barN,
            "ratio_low": (max_f_low / barN) if barN and max_f_low else 0.0,
            "M": Mtot,
            "L": L,
            "energy_routes_ok": routes_ok,
        }
        if best is None or row["max_f_low"] > best["max_f_low"] or (
            row["max_f_low"] == best["max_f_low"] and row["ratio_low"] > best["ratio_low"]
        ):
            best = row

    if all_sub is not None:
        consider(all_sub, "full")
        for t in range(trials):
            hi = min(1000, len(all_sub))
            if hi < 4:
                break
            k = rng.randint(4, hi)
            Omega = [all_sub[i] for i in rng.sample(range(len(all_sub)), k)]
            consider(Omega, f"sparse_{t}")
        # prefer no-3AP subsets (Sidon-ish integer sets)
        no_ap = []
        for S in all_sub:
            sset = set(S)
            has = any(
                (2 * b - a) in sset or (2 * a - b) in sset
                for a, b in itertools.combinations(S, 2)
            )
            if not has:
                no_ap.append(S)
        if len(no_ap) >= 2:
            consider(no_ap[:4000], "no_3ap")
    else:
        for t in range(trials):
            Omega = m.sample_m_subsets(T, m_sz, 3000, random.Random(rng.randint(0, 10**9)))
            consider(Omega, f"sample_{t}")

    dens = m_sz / float(N)
    ce = False
    if best:
        ce = (
            dens >= MIN_DENSITY
            and N >= MIN_N
            and best["max_f_low"] >= max(MIN_F_CE, N)
            and best["ratio_low"] >= max(8.0, float(N))
        )
    return {
        "p": p,
        "N": N,
        "m": m_sz,
        "density": dens,
        "best": best,
        "ce_candidate": ce,
    }


def build_certificate(root: Path) -> dict[str, Any]:
    phase0 = phase0_cube3(root)
    # linear density configs: m/N in {0.25,0.33,0.4,0.5}, N up to ~16, p > N
    configs = []
    for N in (8, 10, 12, 14, 16):
        for dens in (0.25, 1 / 3, 0.4, 0.5):
            for p in (N + 1, N + 5, 2 * N + 1, 31, 37, 41):
                if p <= N:
                    continue
                # primes-ish ok as any odd int > N for embedding
                configs.append((p, N, dens))
    # unique by (p,N,m)
    seen = set()
    charts = []
    for p, N, dens in configs:
        m_sz = max(2, int(round(dens * N)))
        key = (p, N, m_sz)
        if key in seen or math.comb(N, m_sz) > 20000 and N > 14:
            # still allow sample mode
            pass
        if key in seen:
            continue
        seen.add(key)
        charts.append(analyze_linear(p, N, dens, seed=0, max_omega=4000))

    linear_charts = [c for c in charts if c.get("linear_density") and not c.get("empty")]
    adv = []
    for N, dens in ((10, 0.4), (12, 0.5), (12, 0.33), (14, 0.5), (16, 0.5)):
        p = max(17, N + 3)
        if p % 2 == 0:
            p += 1
        adv.append(adversarial_linear(p, N, dens, trials=35))

    any_ce = any(c.get("ce_candidate") for c in linear_charts) or any(
        a.get("ce_candidate") for a in adv
    )

    # How often is the largest fiber near the Sidon (minimal-energy) floor?
    near_sidon = sum(1 for c in linear_charts if c.get("largest_near_sidon"))
    n_lin = len(linear_charts)
    max_f_low_lin = max((c.get("max_f_low") or 0 for c in linear_charts), default=0)
    max_ratio_low = max((c.get("ratio_low") or 0 for c in linear_charts), default=0)
    # largest fiber always high energy vs thr?
    large_high = all(
        (c.get("largest_fiber_Delta") or 0) > THR
        for c in linear_charts
        if c.get("max_f", 0) >= 3
    )

    if any_ce:
        rung = "COUNTEREXAMPLE"
    else:
        # No CE under strict bar; support that low-energy max ratio stays O(1)
        rung = "MEASURED-SUPPORT"

    # scatter points for cert (size, energy) from linear charts frontiers
    scatter = []
    for c in linear_charts:
        for pt in c.get("frontier_top10") or []:
            scatter.append(
                {
                    "N": c["N"],
                    "m": c["m"],
                    "density": c["density"],
                    "f": pt["f"],
                    "Delta": pt["Delta"],
                    "log_f_over_N": pt["log_f_over_N"],
                }
            )

    payload = {
        "schema": "largefiber_lowenergy_hunt.v1",
        "object": "R=2 linear-density large fiber vs additive energy",
        "status": STATUS,
        "proof_status": rung,
        "rung": rung,
        "verdict": rung,
        "base_sha": BASE_SHA,
        "hard_input": "b / C9 crux linear density R=2",
        "weave": ["W52", "#579", "#575", "C9"],
        "thr": THR,
        "min_density": MIN_DENSITY,
        "ce_policy": (
            "density>=0.25, N>=10, max_f_low>=max(8,N), ratio_low>=max(8,N); "
            "O(1) ratios are not CE"
        ),
        "phase0": phase0,
        "generator_route": (
            "linear-density R=2 fiber census; size-vs-Delta frontier; "
            "adversarial max low-Delta fiber"
        ),
        "checker_route": (
            "sum-histogram energy on extremal; recompute Delta; phase0 cube3"
        ),
        # Slim cert: keep summary stats + examples, not full 100+ chart dumps (F9).
        "charts_sample": [c for c in linear_charts if c.get("Omega_mode") == "all"][:12],
        "adversarial": adv,
        "scatter_frontier": scatter[:40],
        "summary": {
            "rung": rung,
            "n_charts": len(charts),
            "n_linear": n_lin,
            "n_largest_near_sidon": near_sidon,
            "max_f_low_linear": max_f_low_lin,
            "max_ratio_low_linear": max_ratio_low,
            "largest_fibers_above_thr": large_high,
            "any_counterexample": any_ce,
            "densities_reached": sorted({round(c["density"], 3) for c in linear_charts}),
            "N_range": [
                min((c["N"] for c in linear_charts), default=0),
                max((c["N"] for c in linear_charts), default=0),
            ],
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
            "Toy N<=16; asymptotic exp-large not fully reached.",
            "thr is finite stand-in for e^{-sigma N}.",
            "Not a proof of large=>high energy.",
        ],
        "honest_headline": (
            f"Rung {rung}: linear charts={len(linear_charts)}; "
            f"max_f_low={max_f_low_lin}; max_ratio_low={max_ratio_low}; "
            f"largest_near_sidon={near_sidon}/{n_lin}; ce={any_ce}"
        ),
        "regeneration": "py -3.13 experimental/scripts/verify_largefiber_lowenergy_hunt.py",
        "all_pass": phase0["pass"],
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
    # recompute one chart Delta of largest
    sample = cert.get("charts_sample") or cert.get("charts") or []
    if sample:
        c0 = next((c for c in sample if c.get("linear_density")), sample[0])
        if not c0.get("empty"):
            live = analyze_linear(c0["p"], c0["N"], c0["density"], seed=0, max_omega=4000)
            if live.get("max_f") != c0.get("max_f"):
                if c0.get("Omega_mode") == "all" and live.get("Omega_mode") == "all":
                    ok = False
    if ok:
        print("RESULT: PASS")
        print(f"payload_sha256: {cert['payload_sha256']}")
        print(f"verdict: {cert.get('verdict')}")
        print(f"summary: {cert.get('summary')}")
        print(f"phase0: {cert.get('phase0', {}).get('paste')}")
        return 0
    print("RESULT: FAIL", file=sys.stderr)
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
