#!/usr/bin/env python3
"""Verify the F1 Cycle-18 graph gate on finite forced-resonance samples.

Status: EXPERIMENTAL / AUDIT.

This checks the restricted F1 toy window

    B=F_p, F=F_{p^2}, D=F_p, t=sigma=2, j=3,

using the local Fable-loop arithmetic already integrated in
`experimental/scripts/fable_loop/local_checks/`.

For off-R0 samples, the Cycle-12 landing polynomial Delta(tau1,tau2,tau3)
has leading tau3^2 coefficient wedge([W]_E,[Bnum]_E). After normalizing by
that nonzero coefficient, Cycle 18 predicts

    Delta0 is monic quadratic in tau3,
    Delta1 = s(tau1,tau2) tau3 + h(tau1,tau2).

The graph gate is

    G = h^2 - A h s + B s^2,

where Delta0 = tau3^2 + A tau3 + B. If Delta1 is not identically zero and
G is nonzero, the whole common-zero branch is curve-sized over B and cannot
produce a two-dimensional slope image.

The script also checks the cleared-remainder identity

    s^2 Delta0 = Delta1 * (s tau3 + A s - h) + G,

so G is the exact resultant/divisibility obstruction for the graph branch.
Every split-triple landing is then classified into the base-valued gate
Delta1==0, the graph gate s!=0 and G=0, or the exceptional locus s=h=0.
The exceptional locus is independently curve-sized whenever Delta1 is not
identically zero.
On the graph branch, the verifier also records the projective coefficient
image [q1:(p1-q2):p2] controlling the slope quadratic.

The default run uses random off-R0 samples to exercise the graph algebra and a
tiny forced-Ra sample to hit the exact resonance gates quickly. Larger forced
nullspace scans should be run separately when hunting counterpackets.
"""

from __future__ import annotations

from itertools import combinations
from pathlib import Path
import importlib.util
import json
import random
from typing import Dict, Iterable, List, Tuple


ROOT = Path(__file__).resolve().parent
C15 = ROOT / "fable_loop/local_checks/20260618_cycle15_forced_ra_slope_scan.py"
spec = importlib.util.spec_from_file_location("cycle15_forced", C15)
c15 = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(c15)
c12r = c15.c12r
c12 = c15.c12
c11 = c15.c11

FElement = Tuple[int, int]
Exp3 = Tuple[int, int, int]
Poly2 = Dict[Tuple[int, int], int]


def inv_mod(x: int, p: int) -> int:
    if x % p == 0:
        raise ZeroDivisionError("zero denominator")
    return pow(x % p, p - 2, p)


def pclean(poly: Poly2, p: int) -> Poly2:
    return {mon: coeff % p for mon, coeff in poly.items() if coeff % p}


def padd(a: Poly2, b: Poly2, p: int) -> Poly2:
    out = dict(a)
    for mon, coeff in b.items():
        out[mon] = (out.get(mon, 0) + coeff) % p
    return pclean(out, p)


def pneg(a: Poly2, p: int) -> Poly2:
    return {mon: (-coeff) % p for mon, coeff in a.items() if coeff % p}


def psub(a: Poly2, b: Poly2, p: int) -> Poly2:
    return padd(a, pneg(b, p), p)


def pmul(a: Poly2, b: Poly2, p: int) -> Poly2:
    out: Poly2 = {}
    for (i, j), av in a.items():
        for (k, ell), bv in b.items():
            mon = (i + k, j + ell)
            out[mon] = (out.get(mon, 0) + av * bv) % p
    return pclean(out, p)


def peval(poly: Poly2, x: int, y: int, p: int) -> int:
    total = 0
    for (i, j), coeff in poly.items():
        total = (total + coeff * pow(x, i, p) * pow(y, j, p)) % p
    return total


def pdegree(poly: Poly2) -> int:
    if not poly:
        return -1
    return max(i + j for i, j in poly)


def is_zero_poly(poly: Poly2) -> bool:
    return not poly


def coeff_poly(
    coeffs: Dict[Exp3, FElement],
    component: int,
    tau3_power: int,
    p: int,
) -> Poly2:
    out: Poly2 = {}
    for (i, j, k), value in coeffs.items():
        if k == tau3_power and value[component] % p:
            out[(i, j)] = value[component] % p
    return pclean(out, p)


def delta_from_coeffs(coeffs: Dict[Exp3, FElement], x: int, y: int, z: int, p: int) -> FElement:
    total = c11.zero
    for exp in c12r.MONOMIALS_DEG_LE_2:
        coeff = coeffs[exp]
        scale = c12r.monomial_value(exp, x, y, z, p)
        total = c11.fadd(total, c11.fmul(coeff, c11.b(scale)))
    return total


def normalize_delta_coeffs(W: List[FElement], E: List[FElement], bnum: List[FElement], D: List[FElement]):
    Wres = c11.residue2(W, E)
    Bres = c11.residue2(bnum, E)
    r0 = c11.wedge(Wres, Bres)
    if r0 == c11.zero:
        return None, r0
    coeff_pairs = c15.coeff_pairs_for_W(W, E, bnum, D)
    coeffs = {
        exp: c11.fdiv(value, r0)
        for exp, value in zip(c12r.MONOMIALS_DEG_LE_2, coeff_pairs)
    }
    return coeffs, r0


def graph_gate(coeffs: Dict[Exp3, FElement], p: int) -> Tuple[Poly2, Poly2, Poly2, Poly2, Poly2]:
    """Return A, B, s, h, G for normalized Delta.

    Delta0 = tau3^2 + A tau3 + B and Delta1 = s tau3 + h.
    """
    a_poly = coeff_poly(coeffs, 0, 1, p)
    b_poly = coeff_poly(coeffs, 0, 0, p)
    s_poly = coeff_poly(coeffs, 1, 1, p)
    h_poly = coeff_poly(coeffs, 1, 0, p)
    g_poly = padd(
        psub(pmul(h_poly, h_poly, p), pmul(pmul(a_poly, h_poly, p), s_poly, p), p),
        pmul(b_poly, pmul(s_poly, s_poly, p), p),
        p,
    )
    return a_poly, b_poly, s_poly, h_poly, g_poly


def decompose_in_wb(residue, Wres, Bres, r0):
    """Write residue = c1*Wres + c2*Bres in the off-R0 basis."""
    return (
        c11.fdiv(c11.wedge(residue, Bres), r0),
        c11.fdiv(c11.wedge(Wres, residue), r0),
    )


def projective_normalize(triple):
    for coord in triple:
        if coord != c11.zero:
            inv = c11.finv(coord)
            return tuple(c11.fmul(x, inv) for x in triple)
    return None


def slope_quadratic_value(q1, p1, q2, p2, slope):
    return c11.fsub(
        c11.fsub(c11.fmul(q1, c11.fmul(slope, slope)), c11.fmul(c11.fsub(p1, q2), slope)),
        p2,
    )


def assert_remainder_identity(a_poly: Poly2, b_poly: Poly2, s_poly: Poly2, h_poly: Poly2, g_poly: Poly2, p: int) -> None:
    """Check s^2 Delta0 = Delta1*(s*tau3 + A*s - h) + G coefficientwise."""
    s_sq = pmul(s_poly, s_poly, p)
    # tau3^0 coefficient:
    # left B*s^2; right h*(A*s-h)+G.
    quotient_const = psub(pmul(a_poly, s_poly, p), h_poly, p)
    rhs_const = padd(pmul(h_poly, quotient_const, p), g_poly, p)
    lhs_const = pmul(b_poly, s_sq, p)
    if lhs_const != rhs_const:
        raise AssertionError("G remainder identity failed in tau3^0")

    # tau3^1 coefficient:
    # left A*s^2; right s*(A*s-h)+h*s.
    rhs_linear = padd(pmul(s_poly, quotient_const, p), pmul(h_poly, s_poly, p), p)
    lhs_linear = pmul(a_poly, s_sq, p)
    if lhs_linear != rhs_linear:
        raise AssertionError("G remainder identity failed in tau3^1")


def all_alpha_coeffs_zero(coeffs: Dict[Exp3, FElement], p: int) -> bool:
    return all(value[1] % p == 0 for value in coeffs.values())


def count_g_zero_pairs(g_poly: Poly2, p: int) -> int:
    return sum(1 for x in range(p) for y in range(p) if peval(g_poly, x, y, p) == 0)


def nonzero_gate_bound(delta1_zero: bool, s_poly: Poly2, g_poly: Poly2, p: int) -> int | None:
    """Return a crude B^3 common-zero bound when the exact gates are inactive."""
    if delta1_zero or is_zero_poly(g_poly):
        return None
    g_degree = pdegree(g_poly)
    if is_zero_poly(s_poly):
        # Then Delta1=h is nonzero of degree <=2; h=0 has <=2p base pairs,
        # and monic quadratic Delta0 gives at most two tau3 values.
        return 4 * p
    # On s != 0, all common zeros lie over G=0, giving <=deg(G)*p
    # base pairs. On s=0, the exceptional locus is contained in one line,
    # with at most two tau3 values from the monic quadratic Delta0.
    return g_degree * p + 2 * p


def exceptional_locus_bound(delta1_zero: bool, s_poly: Poly2, p: int) -> int | None:
    """Return a crude B^3 bound for s=h=0 when Delta1 is nonzero."""
    if delta1_zero:
        return None
    if is_zero_poly(s_poly):
        # Then h is a nonzero degree <=2 polynomial; each base zero gives at
        # most two tau3 values from monic Delta0.
        return 4 * p
    # s=0 is a line, again with at most two tau3 values from monic Delta0.
    return 2 * p


def split_triple_stats(
    p: int,
    E: List[FElement],
    bnum: List[FElement],
    W: List[FElement],
    coeffs: Dict[Exp3, FElement],
    r0: FElement,
) -> Dict[str, object]:
    D = [c11.b(x) for x in range(p)]
    n = len(D)
    LD = c11.locator(D)
    D1 = c12.sum_points(D)
    D2 = c12.elem2(D)
    Wres = c11.residue2(W, E)
    LDres = c11.residue2(LD, E)
    Bres = c11.residue2(bnum, E)
    a_poly, b_poly, s_poly, h_poly, g_poly = graph_gate(coeffs, p)
    assert_remainder_identity(a_poly, b_poly, s_poly, h_poly, g_poly, p)
    delta1_zero = all_alpha_coeffs_zero(coeffs, p)
    g_zero = not g_poly
    g_zero_pairs = p * p if g_zero else count_g_zero_pairs(g_poly, p)
    g_schwartz_bound = p * p if g_zero else pdegree(g_poly) * p
    active_bound = nonzero_gate_bound(delta1_zero, s_poly, g_poly, p)
    exceptional_bound = exceptional_locus_bound(delta1_zero, s_poly, p)

    if coeffs.get((0, 0, 2), c11.zero) != c11.one:
        raise AssertionError("normalized tau3^2 coefficient is not 1")
    for exp, value in coeffs.items():
        if exp[2] == 2 and value[1] % p:
            raise AssertionError("alpha component has tau3^2 term")
    if pdegree(g_poly) > 4:
        raise AssertionError("graph gate degree exceeded 4")
    if pdegree(s_poly) > 1:
        raise AssertionError("s unexpectedly has degree > 1")
    if pdegree(h_poly) > 2:
        raise AssertionError("h unexpectedly has degree > 2")
    if not g_zero and g_zero_pairs > g_schwartz_bound:
        raise AssertionError("G-zero pair count exceeds Schwartz-Zippel bound")

    direct_slopes = {}
    base_gate_slopes = {}
    graph_slopes = {}
    graph_projective_images = set()
    graph_nondegenerate_slopes = set()
    graph_degenerate_slopes = set()
    exceptional_slopes = {}
    split_landings = 0
    base_gate_common = 0
    graph_common = 0
    exceptional_common = 0
    graph_identity_checks = 0
    graph_formula_checks = 0

    for idxs in combinations(range(n), 3):
        T = [D[i] for i in idxs]
        tau1 = c12.sum_points(T)
        tau2 = c12.elem2(T)
        tau3 = c12.elem3(T)
        x, y, z = tau1[0] % p, tau2[0] % p, tau3[0] % p

        direct_delta = c11.fdiv(
            c12r.delta_for_tau(Wres, LDres, Bres, E, W, D1, D2, n, tau1, tau2, tau3),
            r0,
        )
        poly_delta = delta_from_coeffs(coeffs, x, y, z, p)
        if direct_delta != poly_delta:
            raise AssertionError("interpolated Delta disagrees with direct landing determinant")

        s_val = peval(s_poly, x, y, p)
        h_val = peval(h_poly, x, y, p)
        if direct_delta[1] % p != (s_val * z + h_val) % p:
            raise AssertionError("Delta1 graph decomposition failed")
        graph_identity_checks += 1

        if direct_delta[1] % p == 0 and s_val % p:
            graph_z = (-h_val * inv_mod(s_val, p)) % p
            if graph_z != z:
                raise AssertionError("Delta1 graph value did not recover tau3")
            graph_formula_checks += 1

        if direct_delta != c11.zero:
            continue

        split_landings += 1
        LT = c11.locator(T)
        Ls, rem = c11.pdivmod(LD, LT)
        if rem != [c11.zero]:
            raise AssertionError("split triple locator did not divide L_D")
        _, Is = c11.pdivmod(W, Ls)
        slope = c11.line_scalar(c11.residue2(Is, E), Bres)
        if slope is None:
            raise AssertionError("Delta zero but direct slope test failed")
        direct_slopes[slope] = direct_slopes.get(slope, 0) + 1

        Q = c12.q_formula_j3(W, n, D1, D2, tau1, tau2)
        LT = c11.trim([c11.fneg(tau3), tau2, c11.fneg(tau1), c11.one])
        LTres = c11.residue2(LT, E)
        Qres = c11.residue2(Q, E)
        Pres = c11.rsub(c11.rmul(Wres, LTres, E), c11.rmul(LDres, Qres, E))
        Bpp = c11.rmul(Bres, LTres, E)
        p1_minus_tau3, p2 = decompose_in_wb(Pres, Wres, Bres, r0)
        q1, q2_minus_tau3 = decompose_in_wb(Bpp, Wres, Bres, r0)
        p1 = c11.fadd(p1_minus_tau3, tau3)
        q2 = c11.fadd(q2_minus_tau3, tau3)
        if slope_quadratic_value(q1, p1, q2, p2, slope) != c11.zero:
            raise AssertionError("direct slope failed the projective slope quadratic")

        if delta1_zero:
            base_gate_common += 1
            base_gate_slopes[slope] = base_gate_slopes.get(slope, 0) + 1
        elif s_val % p:
            graph_common += 1
            graph_slopes[slope] = graph_slopes.get(slope, 0) + 1
            projective = projective_normalize((q1, c11.fsub(p1, q2), p2))
            if projective is None:
                graph_degenerate_slopes.add(slope)
            else:
                graph_projective_images.add(projective)
                graph_nondegenerate_slopes.add(slope)
            if not g_zero and peval(g_poly, x, y, p) != 0:
                raise AssertionError("graph common zero did not pass G=0")
        elif h_val % p == 0:
            exceptional_common += 1
            exceptional_slopes[slope] = exceptional_slopes.get(slope, 0) + 1
        else:
            raise AssertionError("landing escaped the gate partition")

    if split_landings != base_gate_common + graph_common + exceptional_common:
        raise AssertionError("gate partition did not cover all landings")
    if not delta1_zero and not g_zero and graph_common > g_zero_pairs:
        raise AssertionError("graph branch exceeds the G-zero pair count")
    if len(graph_nondegenerate_slopes) > 2 * len(graph_projective_images):
        raise AssertionError("graph slopes exceed the projective quadratic root-count bound")
    if exceptional_bound is not None and exceptional_common > exceptional_bound:
        raise AssertionError("exceptional branch exceeds the finite exceptional bound")
    if active_bound is not None and split_landings > active_bound:
        raise AssertionError("nonzero-gate split landings exceed the active finite bound")

    return {
        "Delta1_zero": delta1_zero,
        "G_zero": g_zero,
        "G_degree": pdegree(g_poly),
        "G_zero_pairs": g_zero_pairs,
        "G_schwartz_bound": g_schwartz_bound,
        "nonzero_gate_bound": active_bound,
        "exceptional_bound": exceptional_bound,
        "remainder_identity": True,
        "gate_partition": True,
        "gate_status": (
            "base_valued" if delta1_zero else
            "graph_divisibility" if g_zero else
            "nonzero_gate"
        ),
        "split_triples_examined": n * (n - 1) * (n - 2) // 6,
        "split_landings": split_landings,
        "C2": len(direct_slopes),
        "base_gate_common": base_gate_common,
        "base_gate_C2": len(base_gate_slopes),
        "graph_common": graph_common,
        "graph_C2": len(graph_slopes),
        "graph_projective_image_size": len(graph_projective_images),
        "graph_nondegenerate_C2": len(graph_nondegenerate_slopes),
        "graph_degenerate_C2": len(graph_degenerate_slopes),
        "graph_projective_root_bound": 2 * len(graph_projective_images) + len(graph_degenerate_slopes),
        "exceptional_common": exceptional_common,
        "exceptional_C2": len(exceptional_slopes),
        "max_slope_fiber": max(direct_slopes.values()) if direct_slopes else 0,
        "graph_identity_checks": graph_identity_checks,
        "graph_formula_checks": graph_formula_checks,
    }


def random_W(p: int, rng: random.Random, D: List[FElement]) -> List[FElement]:
    w0 = [c11.b(rng.randrange(p)) for _ in D]
    w1 = [c11.b(rng.randrange(p)) for _ in D]
    values = [c11.fadd(w0[i], c11.fmul(c11.alpha, w1[i])) for i in range(len(D))]
    return c11.interp(D, values)


def classify_sample(
    p: int,
    nr: int,
    seed: int,
    mode: str,
    E: List[FElement],
    bnum: List[FElement],
    W: List[FElement],
    extra: Dict[str, object] | None = None,
) -> Dict[str, object] | None:
    D = [c11.b(x) for x in range(p)]
    coeffs, r0 = normalize_delta_coeffs(W, E, bnum, D)
    if coeffs is None:
        return None
    stats = split_triple_stats(p, E, bnum, W, coeffs, r0)
    row = {
        "p": p,
        "q_gen": p,
        "q_line": p * p,
        "seed": seed,
        "nr": nr,
        "mode": mode,
        **stats,
    }
    if extra:
        row.update(extra)
    return row


def better_row(row: Dict[str, object], best: Dict[str, object] | None) -> bool:
    if best is None:
        return True
    return (
        row["G_zero"],
        row["Delta1_zero"],
        row["C2"],
        row["graph_C2"],
        row["split_landings"],
    ) > (
        best["G_zero"],
        best["Delta1_zero"],
        best["C2"],
        best["graph_C2"],
        best["split_landings"],
    )


def scan_random_case(p: int, nr: int, seed: int, samples: int) -> Dict[str, object]:
    c11.set_field(p, nr)
    rng = random.Random(seed)
    D = [c11.b(x) for x in range(p)]
    E = c11.random_separated_quadratic(rng)
    bnum = c11.random_bnum(rng)

    best = None
    off_r0 = 0
    for sample in range(samples):
        W = random_W(p, rng, D)
        if W == [c11.zero]:
            continue
        row = classify_sample(p, nr, seed, "random", E, bnum, W, {"sample": sample})
        if row is None:
            continue
        off_r0 += 1
        if better_row(row, best):
            best = row

    return {
        "mode": "random",
        "p": p,
        "seed": seed,
        "checked": samples,
        "off_R0_checked": off_r0,
        "best": best,
    }


def scan_forced_case(
    p: int,
    nr: int,
    seed: int,
    samples_per_direction: int,
    directions: Iterable[Tuple[int, int]],
) -> Dict[str, object]:
    c11.set_field(p, nr)
    rng = random.Random(seed)
    D = [c11.b(x) for x in range(p)]
    E = c11.random_separated_quadratic(rng)
    bnum = c11.random_bnum(rng)

    best = None
    checked = 0
    off_r0 = 0
    for direction in directions:
        basis = c15.forced_line_nullspace(p, nr, E, bnum, direction)
        if not basis:
            continue
        for _ in range(samples_per_direction):
            W = c15.vec_to_W(c15.random_from_basis(basis, p, rng))
            if W == [c11.zero]:
                continue
            checked += 1
            row = classify_sample(
                p,
                nr,
                seed,
                "forced_Ra",
                E,
                bnum,
                W,
                {"direction": direction, "kernel_dim": len(basis)},
            )
            if row is None:
                continue
            off_r0 += 1
            if better_row(row, best):
                best = row

    return {
        "mode": "forced_Ra",
        "p": p,
        "seed": seed,
        "checked": checked,
        "off_R0_checked": off_r0,
        "best": best,
    }


def main() -> None:
    records = []
    global_best = None

    random_cases = [(7, 3, 6, 2), (11, 2, 2, 1)]
    for p, nr, seeds, samples in random_cases:
        for seed in range(seeds):
            record = scan_random_case(p, nr, seed, samples)
            records.append(record)
            best = record["best"]
            if best is None:
                print(f"mode={record['mode']} p={p} seed={seed} checked={record['checked']} no off-R0 samples")
                continue
            if better_row(best, global_best):
                global_best = best
            print(
                "mode={record_mode} p={p} seed={seed} checked={checked} off_R0={off_R0_checked} "
                "best_C2={C2} graph_C2={graph_C2} split_landings={split_landings} "
                "gate={gate_status} Delta1_zero={Delta1_zero} G_zero={G_zero} G_degree={G_degree} "
                "G_zero_pairs={G_zero_pairs} active_bound={nonzero_gate_bound} "
                "exceptional_bound={exceptional_bound} "
                "base={base_gate_common} graph={graph_common} graph_img={graph_projective_image_size} "
                "exceptional={exceptional_common}".format(
                    record_mode=record["mode"],
                    checked=record["checked"],
                    off_R0_checked=record["off_R0_checked"],
                    **best,
                )
            )

    forced_cases = [(7, 3, 2, 1, [(1, 0), (1, 1), (0, 1)])]
    for p, nr, seeds, samples_per_direction, directions in forced_cases:
        for seed in range(seeds):
            record = scan_forced_case(p, nr, seed, samples_per_direction, directions)
            records.append(record)
            best = record["best"]
            if best is None:
                print(f"mode={record['mode']} p={p} seed={seed} checked={record['checked']} no off-R0 samples")
                continue
            if better_row(best, global_best):
                global_best = best
            print(
                "mode={record_mode} p={p} seed={seed} checked={checked} off_R0={off_R0_checked} "
                "best_C2={C2} graph_C2={graph_C2} split_landings={split_landings} "
                "gate={gate_status} Delta1_zero={Delta1_zero} G_zero={G_zero} G_degree={G_degree} "
                "G_zero_pairs={G_zero_pairs} active_bound={nonzero_gate_bound} "
                "exceptional_bound={exceptional_bound} "
                "base={base_gate_common} graph={graph_common} graph_img={graph_projective_image_size} "
                "exceptional={exceptional_common}".format(
                    record_mode=record["mode"],
                    checked=record["checked"],
                    off_R0_checked=record["off_R0_checked"],
                    **best,
                )
            )

    samples = sum(record["checked"] for record in records)
    off_r0 = sum(record["off_R0_checked"] for record in records)
    g_zero_hits = sum(1 for record in records if record["best"] and record["best"]["G_zero"])
    delta1_zero_hits = sum(1 for record in records if record["best"] and record["best"]["Delta1_zero"])
    max_c2 = max((record["best"]["C2"] for record in records if record["best"]), default=0)
    max_graph_c2 = max((record["best"]["graph_C2"] for record in records if record["best"]), default=0)
    print(
        "f1_resonance_graph_gate: PASS "
        f"samples={samples} off_R0_samples={off_r0} "
        f"Delta1_zero_best_records={delta1_zero_hits} "
        f"G_zero_best_records={g_zero_hits} max_C2={max_c2} max_graph_C2={max_graph_c2}"
    )
    if global_best is not None:
        print("CERT " + json.dumps(global_best, sort_keys=True))


if __name__ == "__main__":
    main()
