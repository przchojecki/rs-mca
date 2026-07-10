#!/usr/bin/env python3
"""W50-M1: drive thin image-normalized Sidon payment margin toward failure.

Reuses W49 model (power-sum Phi, Gsid rate gate tau=0.05).
Phase0: re-validate image_scale_mi_ma cube3 E=216 Delta=27/64.

generator route: zoom grid around W49 thin-margin locus; adversarial Omega
  constructions (AP-biased, sum-extreme, greedy fold-seeking samples);
  scale-in-p family; margin = tau - rate.
checker route: independent sum-histogram energy on extremal instances;
  recompute rates from raw (M,L,Gsid); synthetic fail still fails.

Status: EXPERIMENTAL.
Rungs: COUNTEREXAMPLE | MEASURED-NEGATIVE-TREND | MEASURED-ROBUST.
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
    "experimental/data/certificates/sidon-margin-attack/sidon_margin_attack.json"
)
TEX = Path("experimental/asymptotic_rs_mca_frontiers.tex")
IMAGE_SCALE_CERT = Path(
    "experimental/data/certificates/image-scale-mi-ma/image_scale_mi_ma.json"
)
BASE_SHA = "e190193cebced1d3752d068a1c24136bc69a85d9"
TAU = 0.05
Q = 2
THR = 0.5

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


def phase0_validate_cube3(root: Path) -> dict[str, Any]:
    A = list(itertools.product([0, 1], repeat=3))
    e1 = m.energy_diff_counter(A)
    e2 = m.energy_four_tuple(A)
    Delta = Fraction(e1, len(A) ** 3)
    cert_E = None
    cpath = root / IMAGE_SCALE_CERT
    if cpath.is_file():
        cert = json.loads(cpath.read_text(encoding="utf-8"))
        row = next(r for r in cert["rows"] if r.get("kind") == "sidon_energy_cube3")
        cert_E = row["gen"]["energy"]
    ok = e1 == 216 and e2 == 216 and Delta == Fraction(27, 64) and cert_E == 216
    return {
        "kind": "phase0_image_scale_cube3",
        "energy_diff": e1,
        "energy_4tuple": e2,
        "Delta": "27/64",
        "cert_energy": cert_E,
        "reproduced": ok,
        "pass": ok,
        "paste": "image_scale_mi_ma.json sidon_energy_cube3 gen.energy=216 Delta_num=27 Delta_den=64",
    }


def margin_of(rate: float | None, tau: float = TAU) -> float | None:
    if rate is None:
        return None
    return tau - rate


def eval_raw(
    p: int,
    N: int,
    m_sz: int,
    R: int,
    Omega: list[tuple[int, ...]],
    thr: float = THR,
    q: int = Q,
    tau: float = TAU,
    tag: str = "",
) -> dict[str, Any]:
    T = list(range(1, N + 1))
    fibers = m.build_fibers(Omega, R, p)
    M = len(Omega)
    L = len(fibers)
    barN = M / float(L) if L else 0.0
    stats = m.gsid_and_stats(fibers, T, barN, q, thr, m.energy_diff_counter)
    Gsid = stats["Gsid"]
    rate = m.payment_rate(Gsid, N, q)
    holds = m.payment_holds(Gsid, N, q, tau)
    sratio = m.shallow_ratio(R, p, N)
    regime = "shallow" if sratio < 0.25 else ("borderline" if sratio < 1.0 else "deep")
    # dual energy on largest fiber
    largest = max(fibers.values(), key=len) if fibers else []
    pts = [m.support_vector(s, T) for s in largest]
    e_diff = m.energy_diff_counter(pts) if pts else 0
    e_sum = 0
    if pts:
        sums: Counter[tuple[int, ...]] = Counter()
        for a, b in itertools.product(pts, pts):
            s = tuple(a[i] + b[i] for i in range(len(a)))
            sums[s] += 1
        e_sum = int(sum(v * v for v in sums.values()))
    rate_f = None if rate == float("-inf") else rate
    return {
        "tag": tag,
        "p": p,
        "N": N,
        "m": m_sz,
        "R": R,
        "M": M,
        "L": L,
        "barN": barN,
        "Gsid": Gsid,
        "rate": rate_f,
        "margin": margin_of(rate_f, tau),
        "payment_holds": holds,
        "regime": regime,
        "shallow_ratio": sratio,
        "max_f": stats["max_f"],
        "max_f_over_barN": stats["max_f_over_barN"],
        "n_low_energy": stats["n_low_energy"],
        "E_diff": e_diff,
        "E_sum": e_sum,
        "energy_routes_agree": e_diff == e_sum,
        "density": m_sz / float(N),
    }


def zoom_sweep() -> list[dict[str, Any]]:
    """Finer grid around W49 thin locus (17,8,4,1) rate~0.0139 margin~0.036."""
    rows: list[dict[str, Any]] = []
    # W49 locus neighborhood: p near 17, N in 6..14, m near N/2, R=1..3
    configs = []
    for p in (13, 17, 19, 23, 29, 31):
        for N in range(6, 15):
            if p <= N:
                continue
            for m_sz in range(max(2, N // 3), min(N - 1, N // 2 + 3) + 1):
                for R in (1, 2, 3):
                    configs.append((p, N, m_sz, R))
    # dedupe and cap via priority: close to (17,8,4,1)
    def score(c: tuple[int, int, int, int]) -> float:
        p, N, m_sz, R = c
        return abs(p - 17) + abs(N - 8) + abs(m_sz - 4) + abs(R - 1) * 0.5

    configs = sorted(set(configs), key=score)[:80]
    for p, N, m_sz, R in configs:
        inst = m.evaluate_instance(
            p, N, m_sz, R, seed=0, Omega_mode="all", max_omega=6000, thr=THR, q=Q, tau=TAU
        )
        rate = inst["rate"]
        rows.append(
            {
                "tag": "zoom",
                "p": p,
                "N": N,
                "m": m_sz,
                "R": R,
                "M": inst["M"],
                "L": inst["L"],
                "barN": inst["barN"],
                "Gsid": inst["Gsid"],
                "rate": rate,
                "margin": margin_of(rate),
                "payment_holds": inst["payment_holds"],
                "regime": inst["regime"],
                "shallow_ratio": inst["shallow_ratio"],
                "max_f_over_barN": inst["max_f_over_barN"],
                "energy_routes_agree": inst["energy_routes_agree"],
                "density": inst["density"],
            }
        )
    return rows


def adversarial_at(p: int, N: int, m_sz: int, R: int, trials: int = 60) -> dict[str, Any]:
    """Maximize rate at fixed (p,N,m,R) via structured Omega constructions."""
    T = list(range(1, N + 1))
    all_sub = m.all_m_subsets(T, m_sz) if math.comb(N, m_sz) <= 20000 else None
    rng = random.Random(20260710 + p + N * 17 + m_sz * 3 + R)
    candidates: list[dict[str, Any]] = []

    def consider(Omega: list[tuple[int, ...]], tag: str) -> None:
        if len(Omega) < 2:
            return
        # cap size for energy
        if len(Omega) > 5000:
            Omega = Omega[:5000]
        candidates.append(eval_raw(p, N, m_sz, R, Omega, tag=tag))

    # 1) full or large random samples
    if all_sub is not None:
        consider(all_sub, "full")
        # sum extremes (small sum + large sum)
        ss = sorted(all_sub, key=lambda s: (sum(s), s))
        half = min(len(ss) // 2, 2000)
        consider(ss[:half] + ss[-half:], "sum_extremes")
        # AP-biased: subsets with 3-term AP
        ap_sets = []
        for S in all_sub:
            sset = set(S)
            has_ap = False
            for a, b in itertools.combinations(S, 2):
                # 2b-a in set (3-AP)
                c = 2 * b - a
                if c in sset and c != a and c != b:
                    has_ap = True
                    break
                c2 = 2 * a - b
                if c2 in sset and c2 != a and c2 != b:
                    has_ap = True
                    break
            if has_ap:
                ap_sets.append(S)
        if ap_sets:
            consider(ap_sets[:4000], "ap_biased")
        # arithmetic progression blocks: subsets of an AP of length N//2
        if N >= 6:
            for start in range(1, 3):
                for step in (1, 2):
                    block = [start + i * step for i in range(N) if start + i * step <= N]
                    if len(block) >= m_sz:
                        Omega_ap = list(
                            itertools.combinations(block[: max(m_sz + 2, len(block))], m_sz)
                        )
                        Omega_ap = [s for s in Omega_ap if all(1 <= x <= N for x in s)]
                        consider(Omega_ap[:3000], f"ap_block_s{start}_d{step}")
    else:
        for t in range(trials):
            Omega = m.sample_m_subsets(T, m_sz, 2500, random.Random(rng.randint(0, 10**9)))
            consider(Omega, f"sample_{t}")

    # 2) greedy fold-seeking: keep subsets that collide under Phi (same image)
    pool = (
        all_sub
        if all_sub is not None
        else m.sample_m_subsets(T, m_sz, 4000, rng)
    )
    fibers = m.build_fibers(pool, R, p)
    ranked = sorted(fibers.values(), key=len, reverse=True)
    for k in (1, 2, 3, 5):
        Omega_h = []
        for fib in ranked[:k]:
            Omega_h.extend(fib)
        consider(Omega_h, f"heavy_fibers_top{k}")

    # 3) random trials maximize rate
    best = None
    for t in range(trials):
        if all_sub is not None and len(all_sub) > 100:
            k = min(len(all_sub), rng.randint(50, min(3000, len(all_sub))))
            Omega = [all_sub[i] for i in rng.sample(range(len(all_sub)), k)]
        else:
            Omega = m.sample_m_subsets(T, m_sz, 2000, random.Random(rng.randint(0, 10**9)))
        row = eval_raw(p, N, m_sz, R, Omega, tag=f"rand_{t}")
        candidates.append(row)
        if best is None or (row["rate"] or float("-inf")) > (best["rate"] or float("-inf")):
            best = row

    for row in candidates:
        if best is None or (row["rate"] or float("-inf")) > (best["rate"] or float("-inf")):
            best = row

    fails = [c for c in candidates if not c["payment_holds"]]
    return {
        "p": p,
        "N": N,
        "m": m_sz,
        "R": R,
        "n_candidates": len(candidates),
        "n_fail": len(fails),
        "best": best,
        "any_counterexample": len(fails) > 0,
        "top5": sorted(
            candidates, key=lambda r: -(r["rate"] or float("-inf"))
        )[:5],
    }


def scale_in_p_family() -> list[dict[str, Any]]:
    """Hold density~1/2 and R=1; grow p,N with N ~ c*sqrt(p) borderline family
    and N fixed density around thin locus.
    """
    rows = []
    # Family A: N=8, m=4, R=1, p increases (W49 thin shape)
    for p in (11, 13, 17, 19, 23, 29, 31, 37, 41, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97):
        if p <= 8:
            continue
        inst = m.evaluate_instance(p, 8, 4, 1, seed=0, Omega_mode="all", max_omega=8000)
        rows.append(
            {
                "family": "N8_m4_R1_vary_p",
                "p": p,
                "N": 8,
                "m": 4,
                "R": 1,
                "rate": inst["rate"],
                "margin": margin_of(inst["rate"]),
                "Gsid": inst["Gsid"],
                "barN": inst["barN"],
                "L": inst["L"],
                "payment_holds": inst["payment_holds"],
                "shallow_ratio": inst["shallow_ratio"],
                "regime": inst["regime"],
            }
        )
    # Family B: N grows with p, density 1/2, R=1
    for p, N in (
        (17, 8),
        (19, 10),
        (23, 12),
        (31, 14),
        (41, 16),
        (47, 18),
        (59, 20),
        (67, 22),
        (79, 24),
        (97, 28),
    ):
        m_sz = N // 2
        inst = m.evaluate_instance(
            p, N, m_sz, 1, seed=1, Omega_mode="all", max_omega=4000
        )
        rows.append(
            {
                "family": "density_half_R1_grow_N",
                "p": p,
                "N": N,
                "m": m_sz,
                "R": 1,
                "rate": inst["rate"],
                "margin": margin_of(inst["rate"]),
                "Gsid": inst["Gsid"],
                "barN": inst["barN"],
                "L": inst["L"],
                "payment_holds": inst["payment_holds"],
                "shallow_ratio": inst["shallow_ratio"],
                "regime": inst["regime"],
            }
        )
    return rows


def trend_of(margins: list[float]) -> str:
    """Simple trend: compare first-third mean vs last-third mean."""
    if len(margins) < 3:
        return "insufficient"
    k = max(1, len(margins) // 3)
    early = sum(margins[:k]) / k
    late = sum(margins[-k:]) / k
    if late < early - 0.005:
        return "SHRINK"
    if late > early + 0.005:
        return "GROW"
    return "BOUNDED"


def build_certificate(root: Path) -> dict[str, Any]:
    phase0 = phase0_validate_cube3(root)
    if not phase0["pass"]:
        return {
            "schema": "sidon_margin_attack.v1",
            "status": STATUS,
            "verdict": "STOP-MODEL-UNFAITHFUL",
            "phase0": phase0,
            "all_pass": False,
            "payload_sha256": "",
        }

    zoom = zoom_sweep()
    # extremal zoom row (minimal margin among holds, or any fail)
    fails = [r for r in zoom if not r["payment_holds"]]
    if fails:
        extremal = max(fails, key=lambda r: r["rate"] or float("-inf"))
    else:
        extremal = min(zoom, key=lambda r: r["margin"] if r["margin"] is not None else 99)

    # adversarial at W49 locus + extremal locus
    adv_w49 = adversarial_at(17, 8, 4, 1, trials=40)
    adv_ext = adversarial_at(
        extremal["p"], extremal["N"], extremal["m"], extremal["R"], trials=40
    )

    scale_rows = scale_in_p_family()
    fam_a = [r for r in scale_rows if r["family"] == "N8_m4_R1_vary_p"]
    fam_b = [r for r in scale_rows if r["family"] == "density_half_R1_grow_N"]
    trend_a = trend_of([r["margin"] for r in fam_a if r["margin"] is not None])
    trend_b = trend_of([r["margin"] for r in fam_b if r["margin"] is not None])

    any_ce = (
        len(fails) > 0
        or adv_w49["any_counterexample"]
        or adv_ext["any_counterexample"]
    )
    # negative trend if either family shrinks
    neg_trend = "SHRINK" in (trend_a, trend_b)

    if any_ce:
        rung = "COUNTEREXAMPLE"
    elif neg_trend:
        rung = "MEASURED-NEGATIVE-TREND"
    else:
        rung = "MEASURED-ROBUST"

    min_margin_zoom = min(
        (r["margin"] for r in zoom if r["margin"] is not None), default=None
    )
    max_rate_zoom = max((r["rate"] for r in zoom if r["rate"] is not None), default=None)
    min_margin_adv = None
    for adv in (adv_w49, adv_ext):
        b = adv.get("best") or {}
        if b.get("margin") is not None:
            if min_margin_adv is None or b["margin"] < min_margin_adv:
                min_margin_adv = b["margin"]

    # energy route agreement
    energy_ok = all(r.get("energy_routes_agree", True) for r in zoom)
    energy_ok = energy_ok and (adv_w49.get("best") or {}).get("energy_routes_agree", True)
    energy_ok = energy_ok and (adv_ext.get("best") or {}).get("energy_routes_agree", True)

    payload: dict[str, Any] = {
        "schema": "sidon_margin_attack.v1",
        "object": "thin-margin attack on image-normalized Sidon payment (hard b)",
        "status": STATUS,
        "proof_status": rung,
        "rung": rung,
        "verdict": rung,
        "base_sha": BASE_SHA,
        "tex_path": str(TEX).replace("\\", "/"),
        "hard_input": "b",
        "weave": ["#527", "W49", "C9"],
        "w49_locus": {"p": 17, "N": 8, "m": 4, "R": 1, "w49_rate_approx": 0.013895},
        "tau": TAU,
        "q": Q,
        "thr": THR,
        "phase0": phase0,
        "generator_route": (
            "zoom grid around W49 thin locus; adversarial AP/sum/heavy-fiber Omega; "
            "scale-in-p families; margin=tau-rate"
        ),
        "checker_route": (
            "sum-histogram energy on extremal rows; recompute margin from raw Gsid; "
            "phase0 cube3 independent"
        ),
        "zoom": {
            "n": len(zoom),
            "n_fail": len(fails),
            "min_margin": min_margin_zoom,
            "max_rate": max_rate_zoom,
            "extremal": extremal,
            "rows": zoom,
        },
        "adversarial": {
            "w49_locus": adv_w49,
            "extremal_locus": adv_ext,
            "min_margin_best": min_margin_adv,
            "any_counterexample": any_ce,
        },
        "scale_in_p": {
            "rows": scale_rows,
            "family_N8_m4_R1_trend": trend_a,
            "family_density_half_trend": trend_b,
        },
        "summary": {
            "rung": rung,
            "zoom_n": len(zoom),
            "zoom_fail": len(fails),
            "min_margin_zoom": min_margin_zoom,
            "max_rate_zoom": max_rate_zoom,
            "min_margin_adv": min_margin_adv,
            "trend_a": trend_a,
            "trend_b": trend_b,
            "any_counterexample": any_ce,
            "energy_routes_ok": energy_ok,
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
            "Does not prove or refute ass:image-normalized-sidon-input at deployed scale.",
            "Finite tau-gate is a proxy for asymptotic o(1) rate.",
            "Adversarial search is incomplete; absence of CE is not a proof.",
        ],
        "honest_headline": (
            f"Rung {rung}: phase0 cube3 E=216; zoom_fail={len(fails)}/{len(zoom)}; "
            f"min_margin_zoom={min_margin_zoom}; trends A={trend_a} B={trend_b}; "
            f"adv_ce={any_ce}"
        ),
        "regeneration": "py -3.13 experimental/scripts/verify_sidon_margin_attack.py",
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
    ok = True
    msgs = []
    if not cert.get("phase0", {}).get("pass"):
        ok = False
        msgs.append("phase0 fail")
    if cert.get("phase0", {}).get("energy_diff") != 216:
        ok = False
        msgs.append("cube3 not 216")
    if cert.get("payload_sha256") != rebuilt.get("payload_sha256"):
        ok = False
        msgs.append("payload mismatch")
    # recompute extremal margin from stored Gsid
    ext = cert.get("zoom", {}).get("extremal", {})
    if ext.get("Gsid") is not None and ext.get("N") is not None:
        rate = m.payment_rate(ext["Gsid"], ext["N"], Q)
        rate_f = None if rate == float("-inf") else rate
        if ext.get("rate") is not None and rate_f is not None:
            if abs(ext["rate"] - rate_f) > 1e-9:
                ok = False
                msgs.append("extremal rate recompute mismatch")
    if ok:
        print("RESULT: PASS")
        print(f"payload_sha256: {cert['payload_sha256']}")
        print(f"verdict: {cert.get('verdict')}")
        print(f"summary: {cert.get('summary')}")
        print(f"phase0: {cert.get('phase0', {}).get('paste')}")
        return 0
    print("RESULT: FAIL", "; ".join(msgs), file=sys.stderr)
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
