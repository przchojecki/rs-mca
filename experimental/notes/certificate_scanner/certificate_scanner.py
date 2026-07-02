#!/usr/bin/env python3
"""Proximity certificate scanner for RS reserve ledgers.

This scanner makes the A/B/C/D + experiments ledgers numerically usable.
It is intentionally conservative: each reported item carries a status
(PROVED / CONDITIONAL / UNKNOWN) and a theorem source tag.

Inputs are JSON.  Outputs are JSON and optional Markdown.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

LN2 = math.log(2.0)


def parse_int(x: Any) -> int:
    """Parse integers, decimal strings, or simple powers like '2^192'/'17^32'."""
    if isinstance(x, int):
        return x
    if isinstance(x, float) and x.is_integer():
        return int(x)
    if not isinstance(x, str):
        raise TypeError(f"cannot parse integer from {x!r}")
    s = x.strip().replace(" ", "")
    if "^" in s:
        base, exp = s.split("^", 1)
        return int(base) ** int(exp)
    if "**" in s:
        base, exp = s.split("**", 1)
        return int(base) ** int(exp)
    return int(s, 10)


def log2_int(x: int) -> float:
    if x <= 0:
        return float("-inf")
    # Exact high-bit plus mantissa for stable huge-int logs.
    b = x.bit_length()
    if b <= 53:
        return math.log2(x)
    shift = b - 53
    mant = x >> shift
    return math.log2(mant) + shift


def log2_add(logx: float, logy: float) -> float:
    if logx == float("-inf"):
        return logy
    if logy == float("-inf"):
        return logx
    if logx < logy:
        logx, logy = logy, logx
    return logx + math.log2(1.0 + 2.0 ** (logy - logx))


def log2_binom(n: int, k: int) -> float:
    if k < 0 or k > n:
        return float("-inf")
    k = min(k, n - k)
    if k == 0:
        return 0.0
    if n <= 200_000:
        return log2_int(math.comb(n, k))
    return (math.lgamma(n + 1.0) - math.lgamma(k + 1.0) - math.lgamma(n - k + 1.0)) / LN2


def divisors(n: int) -> List[int]:
    out = []
    r = math.isqrt(n)
    for d in range(1, r + 1):
        if n % d == 0:
            out.append(d)
            if d * d != n:
                out.append(n // d)
    return sorted(out)


def floor_budget(q: int, lam: int) -> int:
    return q // (1 << lam)


def is_integral_power(base: int, value: int) -> bool:
    if base <= 1 or value <= 0:
        return base == value
    acc = 1
    while acc < value:
        acc *= base
    return acc == value


def prob_le_target_integer(numer: int, denom: int, lam: int) -> bool:
    if numer < 0:
        return False
    return numer * (1 << lam) <= denom


def prob_gt_target_integer(numer: int, denom: int, lam: int) -> bool:
    return numer * (1 << lam) > denom


def frac_le_target(terms: List[Tuple[int, int]], lam: int) -> bool:
    s = Fraction(0, 1)
    for num, den in terms:
        s += Fraction(num, den)
    return s <= Fraction(1, 1 << lam)


def frac_gt_target(terms: List[Tuple[int, int]], lam: int) -> bool:
    s = Fraction(0, 1)
    for num, den in terms:
        s += Fraction(num, den)
    return s > Fraction(1, 1 << lam)


def h2(x: float) -> float:
    if x <= 0.0 or x >= 1.0:
        return 0.0 if x in (0.0, 1.0) else float("nan")
    return -x * math.log2(x) - (1.0 - x) * math.log2(1.0 - x)


def solve_tau_star(rho: float, qgen: int) -> Optional[float]:
    """Solve tau log2(q)=H2(rho+tau), tau in [0, 1-rho]."""
    logq = log2_int(qgen)
    hi = max(0.0, 1.0 - rho)
    if hi <= 0:
        return None
    def f(t: float) -> float:
        return t * logq - h2(rho + t)
    # f(0)=-H(rho)<0 for rho in (0,1); f(hi)=hi log q >=0.
    lo = 0.0
    if f(hi) < 0:
        return None
    for _ in range(90):
        mid = (lo + hi) / 2.0
        if f(mid) >= 0:
            hi = mid
        else:
            lo = mid
    return hi


@dataclass(frozen=True)
class Row:
    n: int
    k: int
    q_gen: int
    q_line: int
    q_chal: int
    q_base: int
    rate: Fraction


def load_config(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text())


def row_from_config(cfg: Dict[str, Any]) -> Row:
    row = cfg["row"]
    n = parse_int(row["n"])
    k = parse_int(row["k"])
    fields = cfg.get("fields", {})
    q_gen = parse_int(fields.get("q_gen", fields.get("q_line", row.get("q", 0))))
    q_line = parse_int(fields.get("q_line", fields.get("q_chal", q_gen)))
    q_chal = parse_int(fields.get("q_chal", q_line))
    q_base = parse_int(fields.get("q_base", q_gen))
    return Row(n=n, k=k, q_gen=q_gen, q_line=q_line, q_chal=q_chal, q_base=q_base, rate=Fraction(k, n))


def agreement_values(cfg: Dict[str, Any], row: Row) -> List[int]:
    if "scan" not in cfg:
        a = cfg.get("agreement", {}).get("a", row.k + cfg.get("agreement", {}).get("sigma", 1))
        return [parse_int(a)]
    scan = cfg["scan"]
    vals: List[int] = []
    if "a_values" in scan:
        vals.extend(parse_int(x) for x in scan["a_values"])
    if "sigma_values" in scan:
        vals.extend(row.k + parse_int(x) for x in scan["sigma_values"])
    if "r_values" in scan:
        vals.extend(row.n - parse_int(x) for x in scan["r_values"])
    if "a_start" in scan and "a_end" in scan:
        start = parse_int(scan["a_start"])
        end = parse_int(scan["a_end"])
        step = parse_int(scan.get("step", 1))
        max_points = int(scan.get("max_points", 2000))
        if end < start:
            start, end = end, start
        if (end - start) // step + 1 > max_points:
            raise ValueError(f"scan range too large; set max_points or increase step")
        vals.extend(range(start, end + 1, step))
    # Useful automatic thresholds.
    if scan.get("include_thresholds", True):
        B_line = floor_budget(row.q_line, int(cfg.get("security", {}).get("lambda", 128)))
        for r in [0, 1, B_line - 3, B_line - 2, B_line - 1, B_line, B_line + 1,
                  (row.n - row.k) // 3, (row.n - row.k) // 2, row.n - row.k - 1]:
            if 0 <= r <= row.n:
                vals.append(row.n - r)
    vals = sorted({a for a in vals if 0 <= a <= row.n})
    return vals


def entropy_ledger(row: Row, a: int) -> Dict[str, Any]:
    sigma = a - row.k
    log_binom = log2_binom(row.n, a)
    lhs = sigma * log2_int(row.q_gen)
    margin = lhs - log_binom
    tau = solve_tau_star(float(row.rate), row.q_gen)
    return {
        "source": "Paper B / Paper C generated-field entropy ledger",
        "status": "PROVED necessary floor / certificate check",
        "sigma": sigma,
        "log2_binom_n_a": log_binom,
        "sigma_log2_q_gen": lhs,
        "entropy_margin_bits": margin,
        "passes_nonnegative_margin": margin >= 0,
        "tau_star_asymptotic": tau,
        "eta": sigma / row.n,
        "eta_minus_tau_star": None if tau is None else sigma / row.n - tau,
    }


def quotient_profile(row: Row, a: int) -> Dict[str, Any]:
    sigma = a - row.k
    g = math.gcd(row.n, row.k)
    active = []
    best = float("-inf")
    for M in divisors(g):
        if M <= 1:
            continue
        if not (1 <= sigma < M):
            continue
        if row.k % M != 0 or row.n % M != 0:
            continue
        kk = row.k // M
        nn = row.n // M
        if kk <= nn - 1:
            val = log2_binom(nn - 1, kk)
            active.append({"M": M, "n_over_M": nn, "k_over_M": kk, "log2_floor": val})
            best = max(best, val)
    active.sort(key=lambda x: x["log2_floor"], reverse=True)
    return {
        "source": "Paper B / Paper C quotient-core profile",
        "status": "PROVED lower-floor profile for exact divisibility; remainder variants not included",
        "sigma": sigma,
        "gcd_n_k": g,
        "Qprof_log2": None if best == float("-inf") else best,
        "active_divisors": active[:50],
        "num_active_divisors": len(active),
    }


def tangent_and_high_agreement(row: Row, a: int, lam: int, curve_degrees: List[int]) -> Dict[str, Any]:
    n, k, q = row.n, row.k, row.q_line
    r = n - a
    R = n - k
    out: Dict[str, Any] = {
        "source": "experiments.tex high-agreement tangent/adjacent ledgers",
        "r": r,
        "R_redundancy": R,
        "R_line_exact": R // 3,
        "R_list_unique": R // 2,
    }
    if k + 1 <= a <= n:
        tang = r + 1
        out["tangent_mca_lower"] = {
            "numerator": tang,
            "denominator": q,
            "unsafe_at_target": prob_gt_target_integer(tang, q, lam),
            "status": "PROVED lower floor for support-wise finite-slope MCA",
        }
    else:
        out["tangent_mca_lower"] = {"status": "not in subcapacity range"}
    if 0 <= r <= R // 3:
        finite = r + 1
        out["finite_line_exact"] = {
            "numerator": finite,
            "denominator": row.q_line,
            "safe_at_target": prob_le_target_integer(finite, row.q_line, lam),
            "unsafe_at_target": prob_gt_target_integer(finite, row.q_line, lam),
            "status": "PROVED exact: LD_sw = LD_ca = r+1 in high-agreement range",
        }
        out["projective_line_exact"] = {
            "numerator": finite,
            "denominator": row.q_line + 1,
            "safe_at_target": prob_le_target_integer(finite, row.q_line + 1, lam),
            "unsafe_at_target": prob_gt_target_integer(finite, row.q_line + 1, lam),
            "status": "PROVED exact for uniform P^1 slope sampler in high-agreement range",
        }
    else:
        out["finite_line_exact"] = {"status": "UNKNOWN outside r <= floor((n-k)/3)", "condition_r_le": R // 3}
        out["projective_line_exact"] = {"status": "UNKNOWN outside r <= floor((n-k)/3)", "condition_r_le": R // 3}
    if 0 <= r <= R // 2:
        out["interleaved_list_unique"] = {
            "numerator": 1,
            "denominator": row.q_chal,
            "safe_at_target": prob_le_target_integer(1, row.q_chal, lam),
            "status": "PROVED exact list size 1 for every arity mu in high-agreement range",
        }
    else:
        out["interleaved_list_unique"] = {"status": "UNKNOWN outside r <= floor((n-k)/2)", "condition_r_le": R // 2}
    curves = []
    for d in curve_degrees:
        Rd = R // (d + 2)
        item: Dict[str, Any] = {"degree": d, "R_curve_exact": Rd}
        if 0 <= r <= Rd:
            upper = d * (r + 1)
            # Split criterion for multiplicative subgroup if enabled.
            split = False
            split_reason = "not checked"
            if row.q_line > 1 and (row.q_line - 1) % d == 0 and math.gcd(d, row.q_line) == 1:
                # If D is a subgroup of order n, gamma^d is d-split over up to n/gcd(d,n) residual roots.
                if r + 1 <= n // math.gcd(d, n):
                    split = True
                    split_reason = "multiplicative subgroup split criterion: d | q-1 and r+1 <= n/gcd(d,n)"
                else:
                    split_reason = "d | q-1 but residual set too large for subgroup d-th power image"
            else:
                split_reason = "d does not divide q-1 or char divides d"
            lower = upper if split else r + 1
            item.update({
                "upper_numerator": upper,
                "lower_numerator": lower,
                "denominator": row.q_line,
                "split_exact": split,
                "split_reason": split_reason,
                "safe_by_upper": prob_le_target_integer(upper, row.q_line, lam),
                "unsafe_by_lower": prob_gt_target_integer(lower, row.q_line, lam),
                "status": "PROVED exact under split criterion" if split else "PROVED envelope; exactness needs split moving-root hypothesis",
            })
        else:
            item.update({"status": "UNKNOWN outside r <= floor((n-k)/(d+2))"})
        curves.append(item)
    out["curve_ledgers"] = curves
    return out


def paper_d_cap(row: Row, lam: int, eps_target_log2: Optional[float] = None) -> Dict[str, Any]:
    # eps target is 2^-lam by default.
    n, k, q, B = row.n, row.k, row.q_line, row.q_base
    rho = Fraction(k, n)
    field_hypotheses = {
        "q_line_lt_2_256": q < (1 << 256),
        "domain_fits_field": n <= q,
        "q_base_subfield_of_q_line": is_integral_power(B, q),
    }
    field_hypotheses_ok = all(field_hypotheses.values())
    active = []
    checked = 0
    for N in divisors(n):
        if N <= 0:
            continue
        a_div = n // N
        if n % N != 0:
            continue
        if k % a_div != 0:
            continue
        rhoN = k // a_div  # = rho*N integer
        if (N - rhoN) < 3:
            continue
        ell2 = rhoN + 2
        if ell2 < 0 or ell2 > N:
            continue
        checked += 1
        log_lhs = log2_binom(N, ell2)
        # log2 B*(q/k+1)
        log_rhs = log2_int(B) + math.log2(q / k + 1.0)
        hyp = log_lhs >= log_rhs
        if hyp and field_hypotheses_ok:
            delta_num = Fraction(1, 1) - rho - Fraction(2, N)
            gap = Fraction(2, N)
            # error floor = (1/(2k))*(1-n/q). Compare to 2^-lam.
            # exact: 2^lam*(q-n) >? 2kq
            eps_floor_gt_target = (1 << lam) * (q - n) > 2 * k * q
            active.append({
                "status": "PROVED_PAPERD_V8_CAP",
                "N": N,
                "rhoN": rhoN,
                "ell2": ell2,
                "gap_2_over_N": float(gap),
                "gap_fraction": f"{gap.numerator}/{gap.denominator}",
                "delta_cap_fraction": f"{delta_num.numerator}/{delta_num.denominator}",
                "delta_cap_float": float(delta_num),
                "log2_binom_N_ell2": log_lhs,
                "log2_requirement": log_rhs,
                "hyp_margin_bits": log_lhs - log_rhs,
                "field_hypotheses_ok": field_hypotheses_ok,
                "epsilon_floor_gt_target": eps_floor_gt_target,
            })
    active.sort(key=lambda x: x["delta_cap_float"])
    return {
        "source": "Paper D v12 universal cap",
        "status": "PROVED_PAPERD_V8_CAP" if active else "NO_ACTIVE_PAPERD_V8_CAP",
        "q_base": B,
        "q_line": q,
        "field_hypotheses": field_hypotheses,
        "field_hypotheses_ok": field_hypotheses_ok,
        "checked_candidate_divisors": checked,
        "num_active_caps": len(active),
        "strongest_cap_min_delta": active[0] if active else None,
        "closest_to_capacity_cap_max_delta": active[-1] if active else None,
        "active_caps": active[:100],
    }


def corrected_mca_conditional(row: Row, a: int, cfg: Dict[str, Any], qprof: Dict[str, Any], lam: int) -> Dict[str, Any]:
    ass = cfg.get("assumptions", {})
    if not ass.get("enable_corrected_mca_conjecture", False):
        return {"status": "not enabled", "source": "Paper B/C corrected MCA assumption"}
    n = row.n
    rho = float(row.rate)
    # Ratios H/beta from Paper C/Snarks: 1.262, 1.082, 1.024, 1.009 for rates.
    key = Fraction(row.k, row.n)
    h_over_beta = {
        Fraction(1, 2): 1.262,
        Fraction(1, 4): 1.082,
        Fraction(1, 8): 1.024,
        Fraction(1, 16): 1.009,
    }.get(key, None)
    beta_over_h = None if h_over_beta is None else 1.0 / h_over_beta
    A_M = float(ass.get("A_M", 1.0))
    Gamma_M = float(ass.get("Gamma_M", 0.0))
    nu = int(cfg.get("protocol", {}).get("implementation_interleaving_nu", 1))
    qprof_log2 = qprof.get("Qprof_log2")
    log_term1 = A_M * math.log2(n)
    if qprof_log2 is None or beta_over_h is None:
        log_term2 = float("-inf")
    else:
        log_term2 = beta_over_h * qprof_log2 + Gamma_M
    log_num = math.log2(nu) + log2_add(log_term1, log_term2)
    log_prob = log_num - log2_int(row.q_line)
    return {
        "source": "Paper B/C corrected MCA conjectural ledger",
        "status": "CONDITIONAL / ASSUMPTION",
        "nu": nu,
        "A_M": A_M,
        "Gamma_M": Gamma_M,
        "beta_over_H": beta_over_h,
        "log2_numerator_bound": log_num,
        "log2_probability_bound": log_prob,
        "safe_at_target": log_prob <= -lam,
    }


def combined_protocol(row: Row, a: int, cfg: Dict[str, Any], ledgers: Dict[str, Any], lam: int) -> Dict[str, Any]:
    proto = cfg.get("protocol", {})
    terms_upper: List[Tuple[int, int, str]] = []
    terms_lower: List[Tuple[int, int, str]] = []
    unknown = []
    use_line = proto.get("include_line_term", True)
    use_list = proto.get("include_interleaved_list_term", True)
    projective = proto.get("line_sampler", "finite") == "projective"
    if use_line:
        key = "projective_line_exact" if projective else "finite_line_exact"
        item = ledgers["tangent_high_agreement"].get(key, {})
        if "numerator" in item:
            den = item["denominator"]
            terms_upper.append((item["numerator"], den, key))
            terms_lower.append((item["numerator"], den, key))
        elif "tangent_mca_lower" in ledgers["tangent_high_agreement"]:
            t = ledgers["tangent_high_agreement"]["tangent_mca_lower"]
            if "numerator" in t:
                terms_lower.append((t["numerator"], t["denominator"], "tangent_mca_lower"))
            unknown.append(key)
    if use_list:
        item = ledgers["tangent_high_agreement"].get("interleaved_list_unique", {})
        if "numerator" in item:
            terms_upper.append((item["numerator"], item["denominator"], "interleaved_list_unique"))
            terms_lower.append((item["numerator"], item["denominator"], "interleaved_list_unique"))
        else:
            unknown.append("interleaved_list")
    for deg in proto.get("curve_degrees", []):
        found = None
        for c in ledgers["tangent_high_agreement"].get("curve_ledgers", []):
            if c.get("degree") == deg:
                found = c
                break
        if found and "upper_numerator" in found:
            terms_upper.append((found["upper_numerator"], found["denominator"], f"curve_d{deg}_upper"))
            terms_lower.append((found["lower_numerator"], found["denominator"], f"curve_d{deg}_lower"))
        else:
            unknown.append(f"curve_d{deg}")
    upper_pairs = [(n, d) for n, d, _ in terms_upper]
    lower_pairs = [(n, d) for n, d, _ in terms_lower]
    upper_safe = False if unknown else frac_le_target(upper_pairs, lam)
    lower_unsafe = frac_gt_target(lower_pairs, lam) if lower_pairs else False
    if lower_unsafe:
        verdict = "UNSAFE_BY_PROVED_LOWER_BOUND"
    elif not unknown and upper_safe:
        verdict = "SAFE_BY_PROVED_UPPER_BOUND"
    else:
        verdict = "UNKNOWN_OR_CONDITIONAL"
    return {
        "source": "Paper C protocol ledger composition",
        "status": "PROVED only for included theorem-backed terms; conditional on actual protocol consuming these objects",
        "terms_upper": [{"name": name, "numerator": num, "denominator": den} for num, den, name in terms_upper],
        "terms_lower": [{"name": name, "numerator": num, "denominator": den} for num, den, name in terms_lower],
        "unknown_terms": unknown,
        "safe_by_upper": upper_safe,
        "unsafe_by_lower": lower_unsafe,
        "verdict": verdict,
    }


def scan_agreement(row: Row, a: int, cfg: Dict[str, Any], lam: int) -> Dict[str, Any]:
    if not (0 <= a <= row.n):
        raise ValueError(f"agreement a={a} outside [0,n]")
    curve_degrees = [int(d) for d in cfg.get("protocol", {}).get("curve_degrees", cfg.get("curve_degrees", []))]
    ent = entropy_ledger(row, a)
    qprof = quotient_profile(row, a)
    tg = tangent_and_high_agreement(row, a, lam, curve_degrees)
    ledgers = {"entropy": ent, "quotient_profile": qprof, "tangent_high_agreement": tg}
    ledgers["paper_d_cap"] = paper_d_cap(row, lam)
    ledgers["corrected_mca_conditional"] = corrected_mca_conditional(row, a, cfg, qprof, lam)
    combined = combined_protocol(row, a, cfg, ledgers, lam)
    r = row.n - a
    sigma = a - row.k
    return {
        "a": a,
        "sigma": sigma,
        "r": r,
        "delta_fraction": f"{r}/{row.n}",
        "delta_float": r / row.n,
        "eta_fraction": f"{sigma}/{row.n}",
        "eta_float": sigma / row.n,
        "ledgers": ledgers,
        "combined_protocol": combined,
    }


def make_report(cfg: Dict[str, Any]) -> Dict[str, Any]:
    row = row_from_config(cfg)
    lam = int(cfg.get("security", {}).get("lambda", 128))
    vals = agreement_values(cfg, row)
    scans = [scan_agreement(row, a, cfg, lam) for a in vals]
    return {
        "scanner_version": "0.1",
        "security_lambda": lam,
        "row": {
            "n": row.n,
            "k": row.k,
            "rho": f"{row.rate.numerator}/{row.rate.denominator}",
            "q_gen": row.q_gen,
            "q_line": row.q_line,
            "q_chal": row.q_chal,
            "q_base": row.q_base,
            "budget_q_line": floor_budget(row.q_line, lam),
            "budget_q_chal": floor_budget(row.q_chal, lam),
        },
        "scans": scans,
    }


def md_num(x: Any) -> str:
    if x is None:
        return "—"
    if isinstance(x, float):
        if math.isinf(x):
            return "—"
        return f"{x:.4g}"
    return str(x)


def report_to_markdown(report: Dict[str, Any]) -> str:
    row = report["row"]
    out = []
    out.append("# Proximity certificate scan")
    out.append("")
    out.append(f"- Security target: `2^-{report['security_lambda']}`")
    out.append(f"- Row: `n={row['n']}`, `k={row['k']}`, `rho={row['rho']}`")
    out.append(f"- Fields: `q_gen={row['q_gen']}`, `q_line={row['q_line']}`, `q_chal={row['q_chal']}`, `q_base={row['q_base']}`")
    out.append(f"- Budgets: `floor(q_line/2^lambda)={row['budget_q_line']}`, `floor(q_chal/2^lambda)={row['budget_q_chal']}`")
    out.append("")
    out.append("## Agreement scans")
    out.append("")
    out.append("| a | sigma | r | entropy margin bits | Qprof bits | line exact | list unique | combined verdict |")
    out.append("|---:|---:|---:|---:|---:|---|---|---|")
    for s in report["scans"]:
        led = s["ledgers"]
        ent = led["entropy"]["entropy_margin_bits"]
        qp = led["quotient_profile"].get("Qprof_log2")
        line = led["tangent_high_agreement"].get("finite_line_exact", {})
        listu = led["tangent_high_agreement"].get("interleaved_list_unique", {})
        out.append("| {a} | {sigma} | {r} | {ent:.3f} | {qp} | {line} | {lst} | {verdict} |".format(
            a=s["a"], sigma=s["sigma"], r=s["r"], ent=ent,
            qp="—" if qp is None else f"{qp:.3f}",
            line=line.get("status", "—").split(":")[0],
            lst=listu.get("status", "—").split(":")[0],
            verdict=s["combined_protocol"]["verdict"],
        ))
    out.append("")
    # Paper D summary once
    if report["scans"]:
        cap = report["scans"][0]["ledgers"]["paper_d_cap"]
        out.append("## Paper D universal cap scan")
        out.append("")
        out.append(f"- Status: {cap['status']}")
        out.append(f"- Active caps: {cap['num_active_caps']}")
        if cap["strongest_cap_min_delta"]:
            c = cap["strongest_cap_min_delta"]
            out.append(f"- Strongest active cap: `N={c['N']}`, gap `{c['gap_fraction']}`, delta cap `{c['delta_cap_fraction']}`, margin `{c['hyp_margin_bits']:.3f}` bits")
        else:
            out.append("- No active Paper D cap found under the configured base/line fields and divisor hypotheses.")
        out.append("")
    out.append("## Notes")
    out.append("")
    out.append("- `SAFE_BY_PROVED_UPPER_BOUND` means all included protocol terms have theorem-backed upper numerators below the target.")
    out.append("- `UNSAFE_BY_PROVED_LOWER_BOUND` means theorem-backed lower numerators already exceed the target.")
    out.append("- `UNKNOWN_OR_CONDITIONAL` means at least one consumed term is outside a proved range, or only a conditional Paper B/C assumption is enabled.")
    out.append("- The scanner does not prove extension-line MCA, arbitrary-word locator local limits, or aperiodic Hankel-pencil packing; it flags those gaps.")
    return "\n".join(out) + "\n"


def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser(description="Scan RS proximity reserve certificates.")
    p.add_argument("config", type=Path, help="input JSON config")
    p.add_argument("--json-out", type=Path, default=None)
    p.add_argument("--md-out", type=Path, default=None)
    p.add_argument("--pretty", action="store_true")
    args = p.parse_args(argv)
    cfg = load_config(args.config)
    report = make_report(cfg)
    text = json.dumps(report, indent=2 if args.pretty else None, sort_keys=True)
    if args.json_out:
        args.json_out.write_text(text + "\n")
    else:
        print(text)
    if args.md_out:
        args.md_out.write_text(report_to_markdown(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
