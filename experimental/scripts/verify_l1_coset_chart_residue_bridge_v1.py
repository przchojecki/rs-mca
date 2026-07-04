#!/usr/bin/env python3
"""Verify the L1 coset-chart residue-line bridge.

The theorem checked here is deliberately narrow:

  * petals are H-cosets T_i = g_i H, with |H| = ell;
  * the core is a union of H-cosets;
  * E is a capped kernel set, ell <= |E| <= (t-1)ell;
  * the classification is quotient-coset or residue-line normal-form data.

The script verifies the finite certificate and emits the generated JSON,
Markdown report, and certificate README.  The proof is the residue-graded CRT
argument plus active-basepoint cancellation in the companion note.  This
script deliberately proves a bridge/normal form, not that the residue-line
family is globally paid or quantitatively small.
"""
from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

ROOT = Path(__file__).resolve().parents[2]
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "l1-coset-chart-residue-bridge-v1"
CERT_PATH = CERT_DIR / "l1_coset_chart_residue_bridge_v1.json"
CERT_README_PATH = CERT_DIR / "README.md"
REPORT_PATH = ROOT / "experimental" / "notes" / "certificate_scanner" / "outputs" / "l1_coset_chart_residue_bridge_v1.report.md"


def inv(x: int, p: int) -> int:
    if x % p == 0:
        raise ZeroDivisionError("zero has no inverse")
    return pow(x % p, p - 2, p)


def trim(poly: Sequence[int]) -> List[int]:
    out = [x for x in poly]
    while out and out[-1] == 0:
        out.pop()
    return out or [0]


def trim_mod(poly: Sequence[int], p: int) -> List[int]:
    out = [x % p for x in poly]
    while out and out[-1] == 0:
        out.pop()
    return out or [0]


def degree(poly: Sequence[int]) -> int:
    t = trim(poly)
    return -1 if t == [0] else len(t) - 1


def poly_add(a: Sequence[int], b: Sequence[int], p: int) -> List[int]:
    n = max(len(a), len(b))
    out = [0] * n
    for i in range(n):
        out[i] = ((a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)) % p
    return trim_mod(out, p)


def poly_mul(a: Sequence[int], b: Sequence[int], p: int) -> List[int]:
    out = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        ai %= p
        if ai:
            for j, bj in enumerate(b):
                out[i + j] = (out[i + j] + ai * bj) % p
    return trim_mod(out, p)


def poly_scale(a: Sequence[int], c: int, p: int) -> List[int]:
    return trim_mod([(c * x) % p for x in a], p)


def poly_div_linear(poly: Sequence[int], root: int, p: int) -> List[int]:
    """Divide ``poly`` by ``X-root`` over F_p.

    The zero polynomial is treated as divisible by every linear factor, which is
    exactly what active-basepoint cancellation needs for a projective pair.
    """
    poly = trim_mod(poly, p)
    if degree(poly) == -1:
        return [0]
    if len(poly) == 1:
        raise ValueError("nonzero constant is not divisible by X-root")
    quotient = [0] * (len(poly) - 1)
    carry = poly[-1] % p
    quotient[-1] = carry
    for i in range(len(poly) - 2, 0, -1):
        carry = (poly[i] + root * carry) % p
        quotient[i - 1] = carry
    remainder = (poly[0] + root * carry) % p
    if remainder != 0:
        raise ValueError("linear factor does not divide polynomial")
    return trim_mod(quotient, p)


def eval_poly(poly: Sequence[int], x: int, p: int) -> int:
    acc = 0
    for coeff in reversed(poly):
        acc = (acc * x + coeff) % p
    return acc


def locator(points: Iterable[int], p: int) -> List[int]:
    out = [1]
    for x in points:
        out = poly_mul(out, [(-x) % p, 1], p)
    return trim_mod(out, p)


def interpolate(xs: Sequence[int], ys: Sequence[int], p: int) -> List[int]:
    if len(xs) != len(ys):
        raise ValueError("xs and ys length mismatch")
    result = [0]
    for i, xi in enumerate(xs):
        basis = [1]
        denom = 1
        for j, xj in enumerate(xs):
            if i == j:
                continue
            basis = poly_mul(basis, [(-xj) % p, 1], p)
            denom = denom * (xi - xj) % p
        result = poly_add(result, poly_scale(basis, ys[i] * inv(denom, p), p), p)
    return trim_mod(result, p)


def multiplicative_order(x: int, p: int) -> int:
    y = x % p
    order = 1
    while y != 1:
        y = y * x % p
        order += 1
    return order


def primitive_root(p: int) -> int:
    for g in range(2, p):
        if multiplicative_order(g, p) == p - 1:
            return g
    raise ValueError(f"no primitive root found for {p}")


def subgroup(p: int, ell: int) -> List[int]:
    g = primitive_root(p)
    h = pow(g, (p - 1) // ell, p)
    return sorted(pow(h, i, p) for i in range(ell))


def cosets_of_H(p: int, ell: int) -> List[List[int]]:
    H = subgroup(p, ell)
    seen = set()
    cosets = []
    for g in range(1, p):
        if g in seen:
            continue
        coset = sorted(g * h % p for h in H)
        seen.update(coset)
        cosets.append(coset)
    return cosets


def decompose_by_residue(poly: Sequence[int], ell: int) -> List[List[int]]:
    blocks: List[List[int]] = []
    for r in range(ell):
        coeffs = []
        j = r
        while j < len(poly):
            coeffs.append(poly[j])
            j += ell
        blocks.append(trim(coeffs or [0]))
    return blocks


def degree_in_x_from_blocks(blocks: Sequence[Sequence[int]], ell: int) -> int:
    out = -1
    for r, block in enumerate(blocks):
        block_degree = degree(block)
        if block_degree >= 0:
            out = max(out, r + ell * block_degree)
    return out


def compose_x_from_blocks(blocks: Sequence[Sequence[int]], ell: int, p: int) -> List[int]:
    out = [0]
    for r, block in enumerate(blocks):
        for j, coeff in enumerate(block):
            if coeff % p == 0:
                continue
            idx = r + ell * j
            if len(out) <= idx:
                out.extend([0] * (idx + 1 - len(out)))
            out[idx] = (out[idx] + coeff) % p
    return trim_mod(out, p)


def cancel_projective_basepoints(
    G: Sequence[int],
    H: Sequence[int],
    labels: Sequence[int],
    scalars: Sequence[int],
    p: int,
) -> Dict[str, object]:
    """Cancel active basepoints and check the ordinary residue-line datum."""
    G_values = [eval_poly(G, a, p) for a in labels]
    H_values = [eval_poly(H, a, p) for a in labels]
    relation_ok = all(H_values[i] == scalars[i] * G_values[i] % p for i in range(len(labels)))
    basepoints = [i for i, (gv, hv) in enumerate(zip(G_values, H_values)) if gv == 0 and hv == 0]
    survivors = [i for i in range(len(labels)) if i not in basepoints]

    G_reduced = trim_mod(G, p)
    H_reduced = trim_mod(H, p)
    for i in basepoints:
        G_reduced = poly_div_linear(G_reduced, labels[i], p)
        H_reduced = poly_div_linear(H_reduced, labels[i], p)

    reduced_G_values = [eval_poly(G_reduced, labels[i], p) for i in survivors]
    reduced_H_values = [eval_poly(H_reduced, labels[i], p) for i in survivors]
    reduced_relation_ok = all(
        reduced_H_values[j] == scalars[i] * reduced_G_values[j] % p
        for j, i in enumerate(survivors)
    )
    active_count = len(survivors)
    reduced_degree_bound = active_count - 2
    denominator_nonzero = all(v != 0 for v in reduced_G_values)
    ordinary_residue_line_datum = (
        relation_ok
        and reduced_relation_ok
        and denominator_nonzero
        and active_count >= 2
        and degree(G_reduced) <= reduced_degree_bound
        and degree(H_reduced) <= reduced_degree_bound
    )
    return {
        "basepoint_positions": basepoints,
        "surviving_positions": survivors,
        "active_count_after_basepoint_cancellation": active_count,
        "reduced_deg_G": degree(G_reduced),
        "reduced_deg_H": degree(H_reduced),
        "reduced_degree_bound_active_minus_2": reduced_degree_bound,
        "denominator_nonzero_on_survivors": denominator_nonzero,
        "reduced_relation_ok_on_survivors": reduced_relation_ok,
        "ordinary_residue_line_datum_after_cancellation": ordinary_residue_line_datum,
        "reduced_G_values_on_survivors": reduced_G_values,
        "reduced_H_values_on_survivors": reduced_H_values,
    }


def all_subsets(points: Sequence[int], min_size: int, max_size: int) -> Iterable[Tuple[int, ...]]:
    for size in range(min_size, max_size + 1):
        for subset in itertools.combinations(points, size):
            yield subset


class CosetCase:
    def __init__(self, p: int, ell: int, t: int, m: int, scalars: Sequence[int]):
        self.p = p
        self.ell = ell
        self.t = t
        self.m = m
        self.scalars = [x % p for x in scalars]
        if len(self.scalars) != t:
            raise ValueError("scalar count must equal t")
        if any(x == 0 for x in self.scalars):
            raise ValueError("the residue bridge assumes nonzero scalars")
        cosets = cosets_of_H(p, ell)
        if t + m > len(cosets):
            raise ValueError("not enough cosets")
        self.petals = cosets[:t]
        self.core_cosets = cosets[t : t + m]
        self.core = [x for coset in self.core_cosets for x in coset]
        self.labels = [pow(coset[0], ell, p) for coset in self.petals]
        self.cap = (t - 1) * ell

    def is_union_of_core_cosets(self, E: Iterable[int]) -> bool:
        E_set = set(E)
        for coset in self.core_cosets:
            count = sum(1 for x in coset if x in E_set)
            if count not in (0, len(coset)):
                return False
        return True

    def analyze_subset(self, E_tuple: Tuple[int, ...]) -> Dict[str, object]:
        p, ell = self.p, self.ell
        F_E = locator(E_tuple, p)
        f_blocks = decompose_by_residue(F_E, ell)
        # Fast coset CRT: residue blocks interpolate independently on the
        # quotient labels a_i=g_i^ell.  This is equivalent to the full-petal
        # degree-<t*ell CRT representative but much faster.
        w_blocks = [
            interpolate(
                self.labels,
                [self.scalars[i] * eval_poly(f_r, self.labels[i], p) % p for i in range(self.t)],
                p,
            )
            for f_r in f_blocks
        ]
        deg_W_E = degree_in_x_from_blocks(w_blocks, ell)
        is_kernel = self.ell <= len(E_tuple) <= self.cap and deg_W_E <= len(E_tuple)
        quotient_by_blocks = all(degree(f_blocks[r]) == -1 for r in range(1, ell))
        quotient_by_cosets = self.is_union_of_core_cosets(E_tuple)
        residue_certificate = None
        if is_kernel and not quotient_by_blocks:
            for r in range(1, ell):
                f_r = f_blocks[r]
                if degree(f_r) == -1:
                    continue
                w_r = w_blocks[r]
                f_values = [eval_poly(f_r, a, p) for a in self.labels]
                w_values = [eval_poly(w_r, a, p) for a in self.labels]
                relation_ok = all(
                    w_values[i] == self.scalars[i] * f_values[i] % p
                    for i in range(self.t)
                )
                bridge = cancel_projective_basepoints(f_r, w_r, self.labels, self.scalars, p)
                residue_certificate = {
                    "r": r,
                    "deg_G": degree(f_r),
                    "deg_H": degree(w_r),
                    "degree_bound_t_minus_2": self.t - 2,
                    "relation_ok": relation_ok,
                    "G_not_zero_on_all_active_labels": any(v != 0 for v in f_values),
                    "simultaneous_zero_positions": bridge["basepoint_positions"],
                    "G_values": f_values,
                    "H_values": w_values,
                    "residue_line_bridge": bridge,
                }
                break
        return {
            "E": list(E_tuple),
            "size": len(E_tuple),
            "deg_F_E": degree(F_E),
            "deg_W_E": deg_W_E,
            "is_kernel": is_kernel,
            "quotient_by_blocks": quotient_by_blocks,
            "quotient_by_cosets": quotient_by_cosets,
            "residue_certificate": residue_certificate,
        }

    def optimized_crt_cross_check(self, E_tuple: Tuple[int, ...]) -> None:
        p, ell = self.p, self.ell
        F_E = locator(E_tuple, p)
        f_blocks = decompose_by_residue(F_E, ell)
        w_blocks = [
            interpolate(
                self.labels,
                [self.scalars[i] * eval_poly(f_r, self.labels[i], p) % p for i in range(self.t)],
                p,
            )
            for f_r in f_blocks
        ]
        W = compose_x_from_blocks(w_blocks, ell, p)
        assert degree(W) < self.t * ell
        for petal, scalar in zip(self.petals, self.scalars):
            for x in petal:
                assert eval_poly(W, x, p) == scalar * eval_poly(F_E, x, p) % p

    def run(self) -> Dict[str, object]:
        analyses: Dict[Tuple[int, ...], Dict[str, object]] = {}
        subsets_checked = 0
        for E in all_subsets(self.core, 1, min(self.cap, len(self.core))):
            subsets_checked += 1
            analysis = self.analyze_subset(E)
            if analysis["is_kernel"]:
                analyses[E] = analysis
        kernel_sets = list(analyses)
        minimal_kernel_sets = []
        for E in kernel_sets:
            proper_kernel = False
            for size in range(1, len(E)):
                for F in itertools.combinations(E, size):
                    if F in analyses:
                        proper_kernel = True
                        break
                if proper_kernel:
                    break
            if not proper_kernel:
                minimal_kernel_sets.append(E)

        quotient_kernel = []
        residue_bridge_kernel = []
        unclassified_kernel = []
        classification_errors = []
        sample_residue_certificates = []
        residue_bridge_certificates = 0
        residue_bridge_basepoint_certificates = 0
        max_residue_bridge_basepoints = 0
        for E in kernel_sets:
            a = analyses[E]
            if a["quotient_by_blocks"] != a["quotient_by_cosets"]:
                classification_errors.append({"E": list(E), "error": "quotient block/coset mismatch"})
            if a["quotient_by_blocks"]:
                quotient_kernel.append(E)
                continue
            cert = a["residue_certificate"]
            cert_ok = (
                cert is not None
                and cert["relation_ok"]
                and cert["G_not_zero_on_all_active_labels"]
                and cert["deg_G"] <= self.t - 2
                and cert["deg_H"] <= self.t - 2
                and cert["residue_line_bridge"]["ordinary_residue_line_datum_after_cancellation"]
            )
            if cert_ok:
                residue_bridge_kernel.append(E)
                bridge = cert["residue_line_bridge"]
                residue_bridge_certificates += 1
                basepoint_count = len(bridge["basepoint_positions"])
                if basepoint_count:
                    residue_bridge_basepoint_certificates += 1
                max_residue_bridge_basepoints = max(max_residue_bridge_basepoints, basepoint_count)
                if len(sample_residue_certificates) < 5:
                    sample_residue_certificates.append({"E": list(E), **cert})
            else:
                unclassified_kernel.append(E)
                classification_errors.append({"E": list(E), "error": "missing residue certificate", "cert": cert})

        minimal_quotient = [E for E in minimal_kernel_sets if E in quotient_kernel]
        minimal_residue = [E for E in minimal_kernel_sets if E in residue_bridge_kernel]
        minimal_unclassified = [E for E in minimal_kernel_sets if E not in quotient_kernel and E not in residue_bridge_kernel]
        return {
            "parameters": {
                "p": self.p,
                "ell": self.ell,
                "t": self.t,
                "m_core_cosets": self.m,
                "scalars": self.scalars,
                "labels": self.labels,
                "cap": self.cap,
                "core_size": len(self.core),
            },
            "counts": {
                "subsets_checked": subsets_checked,
                "kernel_sets": len(kernel_sets),
                "minimal_kernel_sets": len(minimal_kernel_sets),
                "quotient_kernel_sets": len(quotient_kernel),
                "residue_bridge_kernel_sets": len(residue_bridge_kernel),
                "unclassified_kernel_sets_after_quotient_or_residue_bridge": len(unclassified_kernel),
                "minimal_quotient": len(minimal_quotient),
                "minimal_residue_bridge": len(minimal_residue),
                "minimal_unclassified_after_quotient_or_residue_bridge": len(minimal_unclassified),
                "residue_bridge_certificates": residue_bridge_certificates,
                "residue_bridge_basepoint_certificates": residue_bridge_basepoint_certificates,
                "max_residue_bridge_basepoints": max_residue_bridge_basepoints,
            },
            "sample_residue_certificates": sample_residue_certificates,
            "classification_errors": classification_errors[:5],
            "ok": not classification_errors and not unclassified_kernel and not minimal_unclassified,
        }


def case_grid() -> List[CosetCase]:
    raw = [
        (17, 2, 4, 3, [1, 2, 4, 8]),
        (17, 2, 4, 4, [3, 5, 7, 11]),
        (19, 3, 3, 3, [1, 2, 5]),
        (19, 3, 3, 3, [4, 7, 11]),
        (29, 4, 3, 3, [1, 3, 9]),
        (29, 4, 3, 4, [2, 5, 13]),
        (31, 5, 3, 2, [1, 6, 17]),
        (31, 5, 3, 3, [2, 8, 19]),
    ]
    return [CosetCase(*args) for args in raw]


def run_self_tests() -> Dict[str, object]:
    cross_checks = 0
    for case in case_grid()[:3]:
        for size in range(1, min(case.cap, len(case.core), 4) + 1):
            case.optimized_crt_cross_check(tuple(case.core[:size]))
            cross_checks += 1

    bridge = cancel_projective_basepoints(
        G=[-1, 1],
        H=[-5, 5],
        labels=[1, 2, 3],
        scalars=[7, 5, 5],
        p=17,
    )
    assert bridge["ordinary_residue_line_datum_after_cancellation"]
    assert bridge["basepoint_positions"] == [0]
    assert bridge["active_count_after_basepoint_cancellation"] == 2
    assert bridge["reduced_deg_G"] == 0
    assert bridge["reduced_deg_H"] == 0
    return {
        "optimized_crt_cross_checks": cross_checks,
        "synthetic_basepoint_bridge_checked": True,
        "synthetic_basepoint_count": len(bridge["basepoint_positions"]),
    }


def build_certificate() -> Dict[str, object]:
    self_tests = run_self_tests()
    cases = [case.run() for case in case_grid()]
    totals = {
        "cases_checked": len(cases),
        "subsets_checked": sum(c["counts"]["subsets_checked"] for c in cases),
        "kernel_sets_checked": sum(c["counts"]["kernel_sets"] for c in cases),
        "minimal_kernel_sets_checked": sum(c["counts"]["minimal_kernel_sets"] for c in cases),
        "quotient_kernel_sets": sum(c["counts"]["quotient_kernel_sets"] for c in cases),
        "residue_bridge_kernel_sets": sum(c["counts"]["residue_bridge_kernel_sets"] for c in cases),
        "unclassified_kernel_sets_after_quotient_or_residue_bridge": sum(c["counts"]["unclassified_kernel_sets_after_quotient_or_residue_bridge"] for c in cases),
        "minimal_quotient_kernel_sets": sum(c["counts"]["minimal_quotient"] for c in cases),
        "minimal_residue_bridge_kernel_sets": sum(c["counts"]["minimal_residue_bridge"] for c in cases),
        "minimal_unclassified_kernel_sets_after_quotient_or_residue_bridge": sum(c["counts"]["minimal_unclassified_after_quotient_or_residue_bridge"] for c in cases),
        "residue_bridge_certificates_checked": sum(c["counts"]["residue_bridge_certificates"] for c in cases),
        "residue_bridge_basepoint_certificates": sum(c["counts"]["residue_bridge_basepoint_certificates"] for c in cases),
        "max_residue_bridge_basepoints": max(c["counts"]["max_residue_bridge_basepoints"] for c in cases),
    }
    all_ok = all(c["ok"] for c in cases) and totals["unclassified_kernel_sets_after_quotient_or_residue_bridge"] == 0
    return {
        "status": "PROVED_LOCAL_COSET_CHART_RESIDUE_BRIDGE_NORMAL_FORM" if all_ok else "FAIL",
        "object": "L1 full-petal coset-chart capped kernel sets",
        "theorem": {
            "classification": "Every capped coset-chart kernel set is quotient-coset or emits a degree <= t-2 projective pair.",
            "residue_line_bridge": "After cancelling simultaneous active basepoints, every emitted projective pair is an ordinary residue-line datum on the surviving quotient labels, with denominator nonzero and degree <= active_count-2.",
            "minimal_kernel_corollary": "The bridge classifies the non-quotient minimal-kernel examples by residue-line normal-form data; it does not declare them paid or absent from the current primitive ledger.",
            "dependencies": [
                "experimental/notes/l1/l1_coset_petal_rank_collapse.md.",
                "experimental/notes/l1/l1_general_reconstruction_collapse.md.",
            ],
            "ledger_condition": "The bridge proves a residue-line normal form. A separate ledger theorem is still needed to pay, bound, or absorb that residue-line family.",
        },
        "self_tests": self_tests,
        "totals": totals,
        "cases": cases,
        "nonclaims": [
            "Does not prove the full L1 generated-field locator local limit.",
            "Does not classify arbitrary non-coset petal configurations.",
            "Does not prove a quotient-only classification of mixed minimal sets.",
            "Does not prove primitive vacancy under the current stabilizer-primitive ledger.",
            "Does not prove a global quantitative bound for residue-line packing.",
            "Does not edit Papers A-D.",
        ],
    }


def assert_certificate(cert: Dict[str, object]) -> None:
    assert cert["status"] == "PROVED_LOCAL_COSET_CHART_RESIDUE_BRIDGE_NORMAL_FORM"
    assert cert["self_tests"]["optimized_crt_cross_checks"] == 12
    assert cert["self_tests"]["synthetic_basepoint_bridge_checked"] is True
    assert cert["self_tests"]["synthetic_basepoint_count"] == 1
    assert cert["totals"]["cases_checked"] == 8
    assert cert["totals"]["subsets_checked"] == 76086
    assert cert["totals"]["kernel_sets_checked"] == 187
    assert cert["totals"]["minimal_kernel_sets_checked"] == 25
    assert cert["totals"]["quotient_kernel_sets"] == 25
    assert cert["totals"]["residue_bridge_kernel_sets"] == 162
    assert cert["totals"]["minimal_quotient_kernel_sets"] == 23
    assert cert["totals"]["minimal_residue_bridge_kernel_sets"] == 2
    assert cert["totals"]["residue_bridge_certificates_checked"] == 162
    assert cert["totals"]["residue_bridge_basepoint_certificates"] == 0
    assert cert["totals"]["max_residue_bridge_basepoints"] == 0
    assert cert["totals"]["unclassified_kernel_sets_after_quotient_or_residue_bridge"] == 0
    assert cert["totals"]["minimal_unclassified_kernel_sets_after_quotient_or_residue_bridge"] == 0
    for case in cert["cases"]:
        assert case["ok"] is True
        assert not case["classification_errors"]


def report(cert: Dict[str, object]) -> str:
    totals = cert["totals"]
    lines = [
        "# L1 coset-chart residue-line bridge v1",
        "",
        f"Status: `{cert['status']}`.",
        "",
        "## Result",
        "",
        "Every capped full-petal coset-chart kernel set is either quotient-coset or emits a low-degree projective pair. After cancelling simultaneous active basepoints, the pair is an ordinary residue-line datum on the surviving quotient labels.",
        "",
        "```text",
        "w_r(a_i) = c_i f_r(a_i),",
        "1 <= r < ell,",
        "deg f_r, deg w_r <= t-2.",
        "```",
        "",
        "If `Z` is the simultaneous active zero set of the pair, cancellation by `prod_{i in Z}(Y-a_i)` gives denominator nonzero on the surviving labels and degree bound `<= active_count-2`.",
        "",
        "Thus the bridge classifies every non-quotient kernel set by residue-line normal-form data. It does not prove that this residue-line family is paid or globally small.",
        "",
        "## Verifier totals",
        "",
        "```text",
        f"cases_checked: {totals['cases_checked']}",
        f"subsets_checked: {totals['subsets_checked']}",
        f"kernel_sets_checked: {totals['kernel_sets_checked']}",
        f"minimal_kernel_sets_checked: {totals['minimal_kernel_sets_checked']}",
        f"quotient_kernel_sets: {totals['quotient_kernel_sets']}",
        f"residue_bridge_kernel_sets: {totals['residue_bridge_kernel_sets']}",
        f"minimal_quotient_kernel_sets: {totals['minimal_quotient_kernel_sets']}",
        f"minimal_residue_bridge_kernel_sets: {totals['minimal_residue_bridge_kernel_sets']}",
        f"residue_bridge_certificates_checked: {totals['residue_bridge_certificates_checked']}",
        f"residue_bridge_basepoint_certificates: {totals['residue_bridge_basepoint_certificates']}",
        f"max_residue_bridge_basepoints: {totals['max_residue_bridge_basepoints']}",
        f"unclassified_after_quotient_or_residue_bridge: {totals['unclassified_kernel_sets_after_quotient_or_residue_bridge']}",
        f"minimal_unclassified_after_quotient_or_residue_bridge: {totals['minimal_unclassified_kernel_sets_after_quotient_or_residue_bridge']}",
        f"optimized_crt_cross_checks: {cert['self_tests']['optimized_crt_cross_checks']}",
        f"synthetic_basepoint_count: {cert['self_tests']['synthetic_basepoint_count']}",
        "```",
        "",
        "## Validation",
        "",
        "```bash",
        "python -m py_compile experimental/scripts/verify_l1_coset_chart_residue_bridge_v1.py",
        "python experimental/scripts/verify_l1_coset_chart_residue_bridge_v1.py --check",
        "python experimental/scripts/verify_l1_coset_chart_residue_bridge_v1.py --json",
        "python -m json.tool experimental/data/certificates/l1-coset-chart-residue-bridge-v1/l1_coset_chart_residue_bridge_v1.json",
        "git diff --check",
        "```",
        "",
        "## Non-claims",
        "",
        "- Not a full L1 local-limit theorem.",
        "- Not a quotient-only classification.",
        "- Not an arbitrary-petal theorem.",
        "- Not a primitive-vacancy theorem under the current stabilizer-primitive ledger.",
        "- Not a proof that the residue-line family is paid or globally small.",
    ]
    return "\n".join(lines) + "\n"


def cert_readme() -> str:
    return """# L1 coset-chart residue-line bridge certificate

This directory contains generated artifacts for `l1_coset_chart_residue_bridge_v1`.

## Files

- `l1_coset_chart_residue_bridge_v1.json`: finite verifier certificate for the coset-chart quotient-or-residue-line-bridge classification.

## Regeneration

Run from the repository root:

```bash
python experimental/scripts/verify_l1_coset_chart_residue_bridge_v1.py --write
python experimental/scripts/verify_l1_coset_chart_residue_bridge_v1.py --check
```

## Claim

Every capped full-petal coset-chart kernel set is quotient-coset or carries a degree-`<=t-2` residue-line projective-pair certificate. After simultaneous active basepoints are cancelled, the certificate is an ordinary residue-line datum on the surviving quotient labels, with denominator nonzero and the sharp degree bound `<= active_count-2`.

## Non-claims

This is not a full L1 local-limit theorem, not an arbitrary-petal theorem, not a quotient-only classification, not a primitive-vacancy theorem under the current stabilizer-primitive ledger, and not a global quantitative bound for residue-line packing.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    cert = build_certificate()
    assert_certificate(cert)
    cert_bytes = (json.dumps(cert, indent=2, sort_keys=True) + "\n").encode("utf-8")
    report_bytes = report(cert).encode("utf-8")
    readme_bytes = cert_readme().encode("utf-8")

    if args.write:
        CERT_DIR.mkdir(parents=True, exist_ok=True)
        REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
        CERT_PATH.write_bytes(cert_bytes)
        REPORT_PATH.write_bytes(report_bytes)
        CERT_README_PATH.write_bytes(readme_bytes)

    if args.check:
        expected = {
            CERT_PATH: cert_bytes,
            REPORT_PATH: report_bytes,
            CERT_README_PATH: readme_bytes,
        }
        for path, expected_bytes in expected.items():
            if path.read_bytes() != expected_bytes:
                raise AssertionError(f"artifact mismatch: {path}")

    if args.json:
        print(json.dumps(cert, indent=2, sort_keys=True))

    if not (args.write or args.check or args.json):
        print(report(cert))


if __name__ == "__main__":
    main()
