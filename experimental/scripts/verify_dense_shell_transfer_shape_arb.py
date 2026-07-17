#!/usr/bin/env python3
"""Rigorous verifier for the uniform dense-shell transfer-shape theorem.

The script certifies the finite bases, direct finite TS1--TS3 range, and all
scalar inequalities consumed by the symbolic tail induction in
``experimental/notes/thresholds/dense_shell_transfer_shape.md``.

It requires python-flint == 0.9.0.  All theorem arithmetic uses 448-bit Arb
balls.  The emitted certificate is deterministic: wall-clock timings and
platform diagnostics are printed separately and are not certificate fields.
"""

import argparse
import hashlib
import json
import sys
import time
from fractions import Fraction
from functools import lru_cache
from pathlib import Path

try:
    import flint
except ImportError as exc:
    raise SystemExit(
        'install dependency: python -m pip install "python-flint==0.9.0"'
    ) from exc

from flint import arb, arb_mat, ctx


PYTHON_FLINT_TESTED = "0.9.0"
if flint.__version__ != PYTHON_FLINT_TESTED:
    raise SystemExit(
        "dense-shell certificate replay requires "
        f"python-flint=={PYTHON_FLINT_TESTED}; found {flint.__version__}"
    )

ctx.prec = 448
ctx.threads = 1

PI = arb.pi()
KDEG = 320
RHO = arb(2)
Y = arb(3) / 16
CH = (2 * PI * Y / 3).cosh()
LOP = (1 + CH) / 2
A1 = PI * CH
A2 = 2 * PI * PI * CH
A3 = 4 * PI**3 * CH
ERRFAC = 16 * RHO ** (-KDEG) / (RHO - 1)
LAM = arb(241) / 500
CC = arb(1289) / 500
MU = CC.sqrt()
PARAMETER_RADIUS = arb(1) / 100000
LAM_BOX = arb(LAM, PARAMETER_RADIUS)
CC_BOX = arb(CC, PARAMETER_RADIUS)

SCRIPT_PATH = Path(__file__).resolve()
REPO_ROOT = SCRIPT_PATH.parents[2]
PROOF_PATH = REPO_ROOT / "experimental/notes/thresholds/dense_shell_transfer_shape.md"
CONSUMED_NOTE_PATH = (
    REPO_ROOT / "experimental/notes/thresholds/dense_shell_class_charges.md"
)
CONSUMER_SCRIPT_PATH = (
    REPO_ROOT / "experimental/scripts/verify_dense_shell_class_charges.py"
)
REPLAY_SCRIPT_PATH = (
    REPO_ROOT / "experimental/scripts/replay_dense_shell_transfer_shape.py"
)
CERT_PATH = (
    REPO_ROOT
    / "experimental/data/certificates/dense-shell-transfer-shape"
    / "dense_shell_transfer_shape.json"
)
CONTRACT_PATH = CERT_PATH.parent / "consumer_contract.json"
UPSTREAM_BASE = "c4856fa6db0b2cd491f5c5fe2a0f3c8468de645e"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def arb_text(value):
    return value.str(20, radius=True)


def arb_bounds(value):
    return {
        "lower": arb_text(value.lower()),
        "upper": arb_text(value.upper()),
    }


def tracker():
    return {"score": None, "value": None, "location": None}


def track_minimum(state, value, location):
    score = float(value.lower())
    if state["score"] is None or score < state["score"]:
        state.update(score=score, value=value, location=location)


def tracked_margin(state, positivity="nonnegative"):
    return {
        "certified_bounds": arb_bounds(state["value"]),
        "required": positivity,
        "worst_cell": state["location"],
    }


def load_contract():
    return json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))


def contract_fraction(contract, name):
    return Fraction(contract[name])


def rat(value):
    if isinstance(value, Fraction):
        return arb(value.numerator) / value.denominator
    return arb(value)


def interval(lo, hi):
    lo = Fraction(lo)
    hi = Fraction(hi)
    return arb(rat((lo + hi) / 2), rat((hi - lo) / 2))


def positive(value):
    return bool(value.lower() > 0)


def nonnegative(value):
    return bool(value.lower() >= 0)


def contains_zero(value):
    return bool(value.lower() <= 0 and value.upper() >= 0)


def add_radius(value, radius):
    return value + arb(0, radius.abs_upper())


def d(t):
    return -(2 * PI * t).cos() / 2


def ap(t):
    return PI * (2 * PI * t).sin()


def app(t):
    return 2 * PI * PI * (2 * PI * t).cos()


def appp(t):
    return -4 * PI**3 * (2 * PI * t).sin()


XS = [(PI * j / KDEG).cos() for j in range(KDEG + 1)]
XP = [(2 + x) / 3 for x in XS]
XM = [-x / 3 for x in XS]


def evaluation_matrix_x(targets):
    rows = []
    for x in targets:
        row = [arb(1), x]
        for _ in range(2, KDEG + 1):
            row.append(2 * x * row[-1] - row[-2])
        rows.append(row)
    return arb_mat(rows)


def evaluation_matrix_t(targets):
    return evaluation_matrix_x([4 * t - 1 for t in targets])


EP = evaluation_matrix_x(XP)
EM = evaluation_matrix_x(XM)

DCT_ROWS = []
for k in range(KDEG + 1):
    ck = 2 if k in (0, KDEG) else 1
    row = []
    for j in range(KDEG + 1):
        cj = 2 if j in (0, KDEG) else 1
        row.append(
            arb(2) / (KDEG * ck * cj) * (PI * k * j / KDEG).cos()
        )
    DCT_ROWS.append(row)
DCT = arb_mat(DCT_ROWS)

TP = [(1 + x) / 4 for x in XP]
TM = [(1 + x) / 4 for x in XM]
DP = [d(t) for t in TP]
DM = [d(t) for t in TM]
AP = [ap(t) for t in TP]
AM = [ap(t) for t in TM]
APP = [app(t) for t in TP]
APM = [app(t) for t in TM]
APPP = [appp(t) for t in TP]
APPM = [appp(t) for t in TM]


def n_operator(vector, diagonal):
    out = [diagonal * value for value in vector] + [arb(0)]
    out[1] += vector[0] / 2
    for i in range(1, len(vector)):
        out[i - 1] += vector[i] / 4
        out[i + 1] += vector[i] / 4
    return out


def k_abs(vector):
    out = [arb(0)] * (len(vector) + 1)
    out[1] += vector[0] / 2
    for i in range(1, len(vector)):
        out[i - 1] += vector[i] / 4
        out[i + 1] += vector[i] / 4
    return out


def a_vector(vector, lam=LAM):
    out = k_abs(vector)
    for i, value in enumerate(vector):
        out[i] -= lam * value
    return out


def a_abs(vector, lam=LAM):
    out = k_abs(vector)
    for i, value in enumerate(vector):
        out[i] += lam * value
    return out


def n_abs(vector, diagonal_max=arb(1) / 2):
    out = k_abs(vector)
    for i, value in enumerate(vector):
        out[i] += diagonal_max * value
    return out


def vector_add(left, right):
    size = max(len(left), len(right))
    out = [arb(0)] * size
    for i, value in enumerate(left):
        out[i] += value
    for i, value in enumerate(right):
        out[i] += value
    return out


def build_models(jmax=27):
    initial = [[arb(1)]] + [[arb(0)] for _ in range(KDEG)]
    cb = [arb_mat(initial)]
    ce = [arb_mat(KDEG + 1, 1)]
    cf = [arb_mat(KDEG + 1, 1)]
    cj = [arb_mat(KDEG + 1, 1)]

    mb = [arb(1)]
    me = [arb(0)]
    mf = [arb(0)]
    mj = [arb(0)]
    eb = [arb(0)]
    ee = [arb(0)]
    ef = [arb(0)]
    ej = [arb(0)]
    interpolation_norm = arb(2 * KDEG)

    for n in range(1, jmax + 1):
        evaluated = []
        for coefficients in (cb[-1], ce[-1], cf[-1], cj[-1]):
            plus = EP * coefficients
            minus = EM * coefficients
            evaluated.append(
                (
                    [
                        [plus[j, i] for i in range(n)]
                        for j in range(KDEG + 1)
                    ],
                    [
                        [minus[j, i] for i in range(n)]
                        for j in range(KDEG + 1)
                    ],
                )
            )

        (bp_all, bm_all), (ep_all, em_all), (fp_all, fm_all), (
            jp_all,
            jm_all,
        ) = evaluated
        b_rows = []
        e_rows = []
        f_rows = []
        j_rows = []

        for q in range(KDEG + 1):
            bp, bm = bp_all[q], bm_all[q]
            eplus, eminus = ep_all[q], em_all[q]
            fplus, fminus = fp_all[q], fm_all[q]
            jplus, jminus = jp_all[q], jm_all[q]
            nbp, nbm = n_operator(bp, DP[q]), n_operator(bm, DM[q])
            nep, nem = n_operator(eplus, DP[q]), n_operator(eminus, DM[q])
            nfp, nfm = n_operator(fplus, DP[q]), n_operator(fminus, DM[q])
            njp, njm = n_operator(jplus, DP[q]), n_operator(jminus, DM[q])
            b_row = []
            e_row = []
            f_row = []
            j_row = []
            for i in range(n + 1):
                bpi = bp[i] if i < n else arb(0)
                bmi = bm[i] if i < n else arb(0)
                epi = eplus[i] if i < n else arb(0)
                emi = eminus[i] if i < n else arb(0)
                fpi = fplus[i] if i < n else arb(0)
                fmi = fminus[i] if i < n else arb(0)
                b_row.append(nbp[i] + nbm[i])
                e_row.append(
                    (nep[i] - nem[i] - AP[q] * bpi + AM[q] * bmi) / 3
                )
                f_row.append(
                    (
                        nfp[i]
                        + nfm[i]
                        + 2 * AP[q] * epi
                        + 2 * AM[q] * emi
                        - APP[q] * bpi
                        - APM[q] * bmi
                    )
                    / 9
                )
                j_row.append(
                    (
                        njp[i]
                        - njm[i]
                        + 3 * AP[q] * fpi
                        - 3 * AM[q] * fmi
                        + 3 * APP[q] * epi
                        - 3 * APM[q] * emi
                        - APPP[q] * bpi
                        + APPM[q] * bmi
                    )
                    / 27
                )
            b_rows.append(b_row)
            e_rows.append(e_row)
            f_rows.append(f_row)
            j_rows.append(j_row)

        cb.append(DCT * arb_mat(b_rows))
        ce.append(DCT * arb_mat(e_rows))
        cf.append(DCT * arb_mat(f_rows))
        cj.append(DCT * arb_mat(j_rows))

        b0, e0, f0, j0 = mb[-1], me[-1], mf[-1], mj[-1]
        mb.append(2 * LOP * b0)
        me.append((2 * LOP * e0 + 2 * A1 * b0) / 3)
        mf.append((2 * LOP * f0 + 4 * A1 * e0 + 2 * A2 * b0) / 9)
        mj.append(
            (2 * LOP * j0 + 6 * A1 * f0 + 6 * A2 * e0 + 2 * A3 * b0)
            / 27
        )

        inherited_b = 2 * eb[-1]
        inherited_e = (2 * ee[-1] + 2 * PI * eb[-1]) / 3
        inherited_f = (
            2 * ef[-1] + 4 * PI * ee[-1] + 4 * PI * PI * eb[-1]
        ) / 9
        inherited_j = (
            2 * ej[-1]
            + 6 * PI * ef[-1]
            + 12 * PI * PI * ee[-1]
            + 8 * PI**3 * eb[-1]
        ) / 27
        eb.append(ERRFAC * mb[-1] + interpolation_norm * inherited_b)
        ee.append(ERRFAC * me[-1] + interpolation_norm * inherited_e)
        ef.append(ERRFAC * mf[-1] + interpolation_norm * inherited_f)
        ej.append(ERRFAC * mj[-1] + interpolation_norm * inherited_j)

    return cb, ce, cf, cj, eb, ee, ef, ej


def sup_vector(coefficients, error):
    out = []
    for i in range(coefficients.ncols()):
        total = error.abs_upper()
        for k in range(KDEG + 1):
            total += coefficients[k, i].abs_upper()
        out.append(arb(total))
    return out


def evaluate_rows(coefficients, error, points):
    values = evaluation_matrix_t(points) * coefficients
    return [
        [add_radius(values[j, i], error) for i in range(coefficients.ncols())]
        for j in range(len(points))
    ]


def midpoints(lo, hi, count):
    lo = Fraction(lo)
    hi = Fraction(hi)
    width = (hi - lo) / count
    return (
        [rat(lo + (k + Fraction(1, 2)) * width) for k in range(count)],
        rat(width / 2),
    )


def check_nonnegative(vector):
    for i, value in enumerate(vector):
        if not nonnegative(value):
            return False, (i, value)
    return True, None


def a_matrix(coefficients, lam=LAM):
    return arb_mat(
        [
            a_vector(
                [coefficients[k, i] for i in range(coefficients.ncols())],
                lam,
            )
            for k in range(coefficients.nrows())
        ]
    )


def sup_vector_with_coordinate_errors(coefficients, errors):
    out = []
    for i in range(coefficients.ncols()):
        total = errors[i].abs_upper()
        for k in range(coefficients.nrows()):
            total += coefficients[k, i].abs_upper()
        out.append(arb(total))
    return out


def raw_multiply_root(coefficients, a_value):
    out = [arb(0)] * (len(coefficients) + 1)
    for i, value in enumerate(coefficients):
        out[i] += (arb(1) / 2 - a_value) * value
        out[i + 1] += (arb(1) / 4 if i >= 1 else arb(1) / 2) * value
        if i >= 1:
            out[i - 1] += value / 4
    return out


@lru_cache(maxsize=None)
def raw_b(n, t_fraction):
    if n == 0:
        return [arb(1)]
    plus_fraction = (1 + t_fraction) / 3
    minus_fraction = (1 - t_fraction) / 3
    plus = rat(plus_fraction)
    minus = rat(minus_fraction)
    raw = vector_add(
        raw_multiply_root(
            raw_b(n - 1, plus_fraction), d(plus) + arb(1) / 2
        ),
        raw_multiply_root(
            raw_b(n - 1, minus_fraction), d(minus) + arb(1) / 2
        ),
    )
    return raw


def flip_raw(coefficients):
    degree = len(coefficients) - 1
    return [
        value if (degree - i) % 2 == 0 else -value
        for i, value in enumerate(coefficients)
    ]


@lru_cache(maxsize=None)
def direct_bef(n, t_fraction):
    if n == 0:
        return [arb(1)], [arb(0)], [arb(0)]
    plus_fraction = (1 + t_fraction) / 3
    minus_fraction = (1 - t_fraction) / 3
    plus = rat(plus_fraction)
    minus = rat(minus_fraction)
    bp, ep, fp = direct_bef(n - 1, plus_fraction)
    bm, em, fm = direct_bef(n - 1, minus_fraction)
    nbp = n_operator(bp, d(plus))
    nbm = n_operator(bm, d(minus))
    nep = n_operator(ep, d(plus))
    nem = n_operator(em, d(minus))
    nfp = n_operator(fp, d(plus))
    nfm = n_operator(fm, d(minus))
    b_out = vector_add(nbp, nbm)
    e_out = []
    f_out = []
    for i in range(n + 1):
        bpi = bp[i] if i < n else arb(0)
        bmi = bm[i] if i < n else arb(0)
        epi = ep[i] if i < n else arb(0)
        emi = em[i] if i < n else arb(0)
        e_out.append((nep[i] - nem[i] - ap(plus) * bpi + ap(minus) * bmi) / 3)
        f_out.append(
            (
                nfp[i]
                + nfm[i]
                + 2 * ap(plus) * epi
                + 2 * ap(minus) * emi
                - app(plus) * bpi
                - app(minus) * bmi
            )
            / 9
        )
    return b_out, e_out, f_out


def model_gate(cb, ce, cf, eb, ee, ef, tamper_top=False):
    point_fractions = [Fraction(0), Fraction(1, 7), Fraction(1, 3), Fraction(1, 2)]
    points = [rat(value) for value in point_fractions]
    worst = {"score": -1.0, "value": arb(0), "location": None}
    checks = 0

    def check_identity(value, location):
        nonlocal checks
        checks += 1
        radius = float(value.rad().upper())
        if radius > worst["score"]:
            worst.update(score=radius, value=value, location=location)
        return contains_zero(value)

    for n in range(1, 8):
        b_values = evaluate_rows(cb[n], eb[n], points)
        e_values = evaluate_rows(ce[n], ee[n], points)
        f_values = evaluate_rows(cf[n], ef[n], points)
        expected_top = rat(Fraction(1, 2 ** (n - 1)))
        if tamper_top:
            expected_top /= 2
        for j, t_fraction in enumerate(point_fractions):
            b_direct, e_direct, f_direct = direct_bef(n, t_fraction)
            b_raw = flip_raw(raw_b(n, t_fraction))
            for i in range(n + 1):
                if not check_identity(
                    b_values[j][i] - b_direct[i], ["B-model", n, j, i]
                ):
                    return False, ("B-model", n, j, i)
                if not check_identity(
                    e_values[j][i] - e_direct[i], ["E-model", n, j, i]
                ):
                    return False, ("E-model", n, j, i)
                if not check_identity(
                    f_values[j][i] - f_direct[i], ["F-model", n, j, i]
                ):
                    return False, ("F-model", n, j, i)
                if not check_identity(
                    b_direct[i] - b_raw[i], ["raw-flip", n, j, i]
                ):
                    return False, ("raw-flip", n, j, i)
            if not check_identity(
                b_direct[-1] - expected_top, ["top-B", n, j, n]
            ):
                return False, ("top-B", n, j)
            if not check_identity(e_direct[-1], ["top-E", n, j, n]) or not check_identity(
                f_direct[-1], ["top-F", n, j, n]
            ):
                return False, ("top-EF", n, j)
    return True, {
        "identity_checks": checks,
        "max_equality_enclosure": arb_text(worst["value"]),
        "worst_cell": worst["location"],
    }


def base_gate(
    cb,
    ce,
    cf,
    cj,
    eb,
    ee,
    ef,
    ej,
    cell_count=512,
    lam=LAM,
    cc=CC,
):
    margins = {
        f"{domain}-A{q}": tracker()
        for domain in ("inner", "outer")
        for q in range(3)
    }
    margins.update({"B26-strict": tracker(), "F26": tracker(), "CF26": tracker()})
    n = 25
    b_matrices = [cb[n]]
    e_matrices = [ce[n]]
    b_errors = [[eb[n]] * (n + 1)]
    e_errors = [[ee[n]] * (n + 1)]
    for _ in range(2):
        b_matrices.append(a_matrix(b_matrices[-1], lam))
        e_matrices.append(a_matrix(e_matrices[-1], lam))
        b_errors.append(a_abs(b_errors[-1], lam))
        e_errors.append(a_abs(e_errors[-1], lam))
    b_suprema = [
        sup_vector_with_coordinate_errors(b_matrices[q], b_errors[q])
        for q in range(3)
    ]
    e_suprema = [
        sup_vector_with_coordinate_errors(e_matrices[q], e_errors[q])
        for q in range(3)
    ]

    domains = [((0, Fraction(1, 4)), False), ((Fraction(1, 4), Fraction(1, 2)), True)]
    for domain, is_outer in domains:
        points, radius = midpoints(*domain, cell_count // 2)
        b_values = evaluate_rows(cb[n], eb[n], points)
        for index, t in enumerate(points):
            value = n_operator(b_values[index], d(t)) if is_outer else b_values[index]
            for q in range(3):
                if is_outer:
                    derivative = n_abs(e_suprema[q])
                    b_derivative = [PI * entry for entry in b_suprema[q]] + [arb(0)]
                    derivative = [
                        derivative[i] + b_derivative[i]
                        for i in range(len(derivative))
                    ]
                else:
                    derivative = e_suprema[q]
                enclosure = [
                    add_radius(value[i], derivative[i] * radius)
                    for i in range(len(value))
                ]
                metric = f"{'outer' if is_outer else 'inner'}-A{q}"
                for coordinate, entry in enumerate(enclosure):
                    track_minimum(
                        margins[metric],
                        entry,
                        {"cell": index, "coordinate": coordinate},
                    )
                ok, bad = check_nonnegative(enclosure)
                if not ok:
                    return False, ("outer" if is_outer else "inner", q, index, bad)
                value = a_vector(value, lam)

    n = 26
    points, radius = midpoints(0, Fraction(1, 2), cell_count)
    b_values = evaluate_rows(cb[n], eb[n], points)
    f_values = evaluate_rows(cf[n], ef[n], points)
    e_supremum = sup_vector(ce[n], ee[n])
    j_supremum = sup_vector(cj[n], ej[n])
    for k, _ in enumerate(points):
        b_value = b_values[k]
        f_value = f_values[k]
        b_enclosure = [
            add_radius(b_value[i], e_supremum[i] * radius)
            for i in range(n + 1)
        ]
        for coordinate, entry in enumerate(b_enclosure):
            track_minimum(
                margins["B26-strict"],
                entry,
                {"cell": k, "coordinate": coordinate},
            )
        if any(not positive(entry) for entry in b_enclosure):
            return False, ("B26-strict", k)
        f_enclosure = [
            add_radius(f_value[i], j_supremum[i] * radius) for i in range(n)
        ]
        for coordinate, entry in enumerate(f_enclosure):
            track_minimum(
                margins["F26"], entry, {"cell": k, "coordinate": coordinate}
            )
        ok, bad = check_nonnegative(f_enclosure)
        if not ok:
            return False, ("F26", k, bad)
        gaps = [cc * b_value[i] - f_value[i] for i in range(n)]
        gap_enclosure = [
            add_radius(
                gaps[i],
                (arb(cc.abs_upper()) * e_supremum[i] + j_supremum[i]) * radius,
            )
            for i in range(n)
        ]
        for coordinate, entry in enumerate(gap_enclosure):
            track_minimum(
                margins["CF26"], entry, {"cell": k, "coordinate": coordinate}
            )
        ok, bad = check_nonnegative(gap_enclosure)
        if not ok:
            return False, ("CF26", k, bad)
    return True, {
        name: tracked_margin(state, "positive" if name == "B26-strict" else "nonnegative")
        for name, state in margins.items()
    }


def finite_gate(
    cb,
    ce,
    eb,
    ee,
    cell_count=256,
    c1=Fraction(543, 500),
    c2=Fraction(1663, 1000),
    gamma=Fraction(7, 6),
):
    margins = {
        name: tracker()
        for name in ("TS1-lower", "TS1-upper", "TS2-lower", "TS2-upper", "TS3")
    }
    epsilon, radius = midpoints(0, Fraction(1, 4), cell_count)
    c1 = rat(c1)
    c2 = rat(c2)
    gamma = rat(gamma)
    maps = {
        "tin": [arb(1) / 4 - value / 3 for value in epsilon],
        "r": [arb(1) / 4 + value / 9 for value in epsilon],
        "s": [arb(7) / 36 - value / 9 for value in epsilon],
        "r2": [arb(5) / 12 - value / 9 for value in epsilon],
        "s2": [arb(17) / 36 + value / 9 for value in epsilon],
    }
    for n in range(5, 27):
        values = {
            key: evaluate_rows(cb[n], eb[n], points)
            for key, points in maps.items()
            if key != "tin"
        }
        tin_values = evaluate_rows(cb[n + 1], eb[n + 1], maps["tin"])
        b_supremum = sup_vector(cb[n], eb[n])
        e_supremum = sup_vector(ce[n], ee[n])
        next_e_supremum = sup_vector(ce[n + 1], ee[n + 1])
        exp1 = (c1 / 9).exp()
        exp2 = (c2 / 9).exp()
        for k, value in enumerate(epsilon):
            gap = arb(1) / 18 + 2 * value / 9
            lo1, hi1 = (-c1 * gap).exp(), (c1 * gap).exp()
            lo2, hi2 = (-c2 * gap).exp(), (c2 * gap).exp()
            gaps = []
            radii = []
            for i in range(n + 1):
                br = values["r"][k][i]
                bs = values["s"][k][i]
                br2 = values["r2"][k][i]
                bs2 = values["s2"][k][i]
                gaps.extend([bs - lo1 * br, hi1 * br - bs, bs2 - lo2 * br2, hi2 * br2 - bs2])
                radius1 = e_supremum[i] / 9 + exp1 * (
                    e_supremum[i] / 9 + 2 * c1 * b_supremum[i] / 9
                )
                radius2 = e_supremum[i] / 9 + exp2 * (
                    e_supremum[i] / 9 + 2 * c2 * b_supremum[i] / 9
                )
                radii.extend([radius1, radius1, radius2, radius2])
            enclosure = [
                add_radius(gaps[i], radii[i] * radius) for i in range(len(gaps))
            ]
            labels = ("TS1-lower", "TS1-upper", "TS2-lower", "TS2-upper")
            for flat_index, entry in enumerate(enclosure):
                metric = labels[flat_index % 4]
                track_minimum(
                    margins[metric],
                    entry,
                    {
                        "level_n": n,
                        "epsilon_cell": k,
                        "coordinate": flat_index // 4,
                    },
                )
            ok, bad = check_nonnegative(enclosure)
            if not ok:
                return False, ("TS12", n, k, bad)

            share = []
            for i in range(n + 1):
                difference = tin_values[k][i] - gamma * values["r"][k][i]
                derivative = next_e_supremum[i] / 3 + gamma * e_supremum[i] / 9
                share.append(add_radius(difference, derivative * radius))
            for coordinate, entry in enumerate(share):
                track_minimum(
                    margins["TS3"],
                    entry,
                    {"level_n": n, "epsilon_cell": k, "coordinate": coordinate},
                )
            ok, bad = check_nonnegative(share)
            if not ok:
                return False, ("TS3", n, k, bad)
    return True, {
        name: tracked_margin(state) for name, state in margins.items()
    }


def scalar_gate(
    cell_count=512,
    h1_cap=Fraction(543, 500),
    h2_cap=Fraction(1663, 1000),
    gamma=Fraction(7, 6),
    master_margin_floor=Fraction(57, 10000),
    lam=LAM,
    cc=CC,
):
    h1_cap = rat(h1_cap)
    h2_cap = rat(h2_cap)
    gamma = rat(gamma)
    master_margin_floor = rat(master_margin_floor)
    mu = cc.sqrt()
    margins = {
        name: tracker()
        for name in (
            "H1",
            "H2",
            "inner-cm",
            "share",
            "master-key",
            "closure-dm",
            "closure-dp-plus-dm",
            "lower-curvature",
        )
    }
    h2_margin = h2_cap - mu * (mu / 2).tan()
    track_minimum(margins["H2"], h2_margin, {"point": "t=1/2"})
    if not positive(h2_margin):
        return False, "H2"
    h1_margin = h1_cap - mu * (mu * arb(5) / 18).tan()
    track_minimum(margins["H1"], h1_margin, {"point": "t=5/18"})
    if not positive(h1_margin):
        return False, "H1"
    inner_cm = lam - arb(1) / 4
    track_minimum(margins["inner-cm"], inner_cm, {"point": "m=1/6"})
    if not positive(inner_cm):
        return False, "inner-cm"

    ranges = [((0, Fraction(1, 4)), "share"), ((0, Fraction(1, 2)), "closure")]
    for (lo, hi), kind in ranges:
        width = (hi - lo) / cell_count
        for k in range(cell_count):
            x = interval(lo + k * width, lo + (k + 1) * width)
            if kind == "share":
                r = arb(1) / 4 + x / 9
                r2 = arb(5) / 12 - x / 9
                rho = (mu * r2).cos() / (mu * r).cos()
                share = lam + d(r) + rho * (lam + d(r2)) - gamma
                track_minimum(margins["share"], share, {"cell": k})
                if not positive(share):
                    return False, (kind, k, share)
                gap = arb(1) / 18 + 2 * x / 9
                need = (2 * PI * x / 3).sin() / (
                    2 * PI * (arb(1) / 6 + x / 3)
                ).sin()
                deficit = (4 * PI / 9).sin() * (PI * gap).sin()
                key = (
                    ((-h2_cap * gap).exp() - need)
                    * gamma
                    * (-h1_cap * gap).exp()
                    - deficit
                )
                track_minimum(margins["master-key"], key, {"cell": k})
                if not positive(key - master_margin_floor):
                    return False, ("master-key", k, key)
            else:
                t = x
                p = (1 + t) / 3
                m = (1 - t) / 3
                cp = lam + d(p)
                cm = lam + d(m)
                hp = mu * (mu * p).tan()
                hm = mu * (mu * m).tan()
                p_source = 2 * ap(p) * hp - app(p)
                m_source = 2 * ap(m) * hm - app(m)
                if lo + k * width < Fraction(1, 4) < lo + (k + 1) * width:
                    return False, "interval-crosses-1/4"
                chi = arb(1) if lo + (k + 1) * width <= Fraction(1, 4) else lam / cm
                dp = 8 * cc * cp - p_source
                dm = (9 * cc - cc * chi) * cm - m_source
                track_minimum(margins["closure-dm"], dm, {"cell": k})
                track_minimum(
                    margins["closure-dp-plus-dm"], dp + dm, {"cell": k}
                )
                if not positive(dm) or not positive(dp + dm):
                    return False, (kind, k, dm, dp + dm)
                if lo + k * width >= Fraction(1, 4):
                    ratio = (mu * m).cos() / (mu * p).cos()
                    lower = -app(p) + (cc * d(m) - app(m)) * ratio
                    track_minimum(
                        margins["lower-curvature"], lower, {"cell": k}
                    )
                    if not positive(lower):
                        return False, ("lower-curvature", k, lower)
    details = {name: tracked_margin(state, "positive") for name, state in margins.items()}
    details["master-key"]["required"] = "greater-than-contract-floor"
    details["master-key"]["required_floor"] = arb_bounds(master_margin_floor)
    return True, details


EXPECTED_CONTRACT = {
    "schema": "dense-shell-transfer-shape-consumer/v1",
    "producer": "experimental/notes/thresholds/dense_shell_transfer_shape.md",
    "consumer": "experimental/notes/thresholds/dense_shell_class_charges.md",
    "ts1_envelope": "543/500",
    "ts2_envelope": "1663/1000",
    "ts3_share": "7/6",
    "master_margin_floor": "57/10000",
}


def consumer_contract_gate(contract):
    if contract != EXPECTED_CONTRACT:
        return False, {
            "expected": EXPECTED_CONTRACT,
            "actual": contract,
        }
    return True, {
        "contract_sha256": sha256(CONTRACT_PATH),
        "consumer_script_sha256": sha256(CONSUMER_SCRIPT_PATH),
        "master_inputs": {
            name: contract[name]
            for name in (
                "ts1_envelope",
                "ts2_envelope",
                "ts3_share",
                "master_margin_floor",
            )
        },
    }


def parameter_neighborhood_gate(models, contract):
    cb, ce, cf, cj, eb, ee, ef, ej = models
    scalar_ok, scalar_detail = scalar_gate(
        h1_cap=contract_fraction(contract, "ts1_envelope"),
        h2_cap=contract_fraction(contract, "ts2_envelope"),
        gamma=contract_fraction(contract, "ts3_share"),
        master_margin_floor=contract_fraction(contract, "master_margin_floor"),
        lam=LAM_BOX,
        cc=CC_BOX,
    )
    if not scalar_ok:
        return False, {"part": "scalar", "detail": str(scalar_detail)}
    base_ok, base_detail = base_gate(
        cb,
        ce,
        cf,
        cj,
        eb,
        ee,
        ef,
        ej,
        lam=LAM_BOX,
        cc=CC_BOX,
    )
    if not base_ok:
        return False, {"part": "finite-base", "detail": str(base_detail)}
    return True, {
        "lambda_box": arb_bounds(LAM_BOX),
        "curvature_C_box": arb_bounds(CC_BOX),
        "radius_each_parameter": arb_bounds(PARAMETER_RADIUS),
        "scalar_margins": scalar_detail,
        "finite_base_margins": base_detail,
    }


def run_tamper_selftest(models, contract):
    cb, ce, cf, cj, eb, ee, ef, ej = models
    tests = [
        ("wrong-top-formula", lambda: model_gate(cb, ce, cf, eb, ee, ef, True)),
        ("weak-master-share", lambda: scalar_gate(gamma=Fraction(1, 1))),
        ("too-tight-H2", lambda: scalar_gate(h2_cap=Fraction(8, 5))),
        ("too-tight-TS1", lambda: finite_gate(cb, ce, eb, ee, c1=Fraction(3, 5))),
        ("zero-TS2-envelope", lambda: finite_gate(cb, ce, eb, ee, c2=Fraction(0, 1))),
        ("too-strong-TS3", lambda: finite_gate(cb, ce, eb, ee, gamma=Fraction(13, 10))),
        (
            "consumer-share-mismatch",
            lambda: consumer_contract_gate({**contract, "ts3_share": "6/5"}),
        ),
        (
            "too-wide-C-neighborhood",
            lambda: scalar_gate(cc=arb(CC, arb(1) / 100)),
        ),
    ]
    caught = 0
    for name, test in tests:
        ok, _ = test()
        if ok:
            print(f"tamper {name}: NOT DETECTED")
        else:
            print(f"tamper {name}: detected")
            caught += 1
    print(f"tamper-selftest: caught {caught}/{len(tests)}")
    return caught == len(tests)


def certificate_payload(results):
    return {
        "schema": "dense-shell-transfer-shape-arb/v3",
        "pass": all(result["pass"] for result in results),
        "upstream_base": UPSTREAM_BASE,
        "python_flint_tested": PYTHON_FLINT_TESTED,
        "arb_precision_bits": ctx.prec,
        "chebyshev_degree": KDEG,
        "bernstein_rho": 2,
        "interpolation_operator_bound": f"2*K={2 * KDEG}",
        "lambda": "241/500",
        "curvature_C": "1289/500",
        "parameter_neighborhood_radius": "1/100000",
        "two_state_base_level": 25,
        "curvature_base_level": 26,
        "finite_target_levels_n": [5, 26],
        "scalar_interval_cells": 512,
        "base_interval_cells": 512,
        "epsilon_interval_cells": 256,
        "source_sha256": sha256(SCRIPT_PATH),
        "replay_source_sha256": sha256(REPLAY_SCRIPT_PATH),
        "proof_sha256": sha256(PROOF_PATH),
        "consumed_note_sha256": sha256(CONSUMED_NOTE_PATH),
        "consumer_contract_sha256": sha256(CONTRACT_PATH),
        "consumer_script_sha256": sha256(CONSUMER_SCRIPT_PATH),
        "results": results,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit-cert", type=Path)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()

    started = time.time()
    models = build_models()
    cb, ce, cf, cj, eb, ee, ef, ej = models
    contract = load_contract()

    if args.tamper_selftest:
        return 0 if run_tamper_selftest(models, contract) else 1

    gates = [
        ("model-consistency", lambda: model_gate(cb, ce, cf, eb, ee, ef)),
        ("consumer-contract", lambda: consumer_contract_gate(contract)),
        (
            "scalar-closure",
            lambda: scalar_gate(
                h1_cap=contract_fraction(contract, "ts1_envelope"),
                h2_cap=contract_fraction(contract, "ts2_envelope"),
                gamma=contract_fraction(contract, "ts3_share"),
                master_margin_floor=contract_fraction(
                    contract, "master_margin_floor"
                ),
            ),
        ),
        (
            "finite-base-cones",
            lambda: base_gate(cb, ce, cf, cj, eb, ee, ef, ej),
        ),
        ("finite-TS1-TS3", lambda: finite_gate(cb, ce, eb, ee)),
        (
            "parameter-neighborhood",
            lambda: parameter_neighborhood_gate(models, contract),
        ),
    ]
    results = []
    for name, gate in gates:
        ok, detail = gate()
        results.append(
            {
                "name": name,
                "pass": bool(ok),
                "detail": detail if ok else str(detail),
            }
        )
        print(f"{name}: {'PASS' if ok else 'FAIL'}")
        if not ok:
            break

    payload = certificate_payload(results)
    encoded = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    payload_hash = hashlib.sha256(encoded.encode("utf-8")).hexdigest()
    print(f"certificate_sha256={payload_hash}")
    print(f"runtime_seconds={time.time() - started:.3f}")

    if args.emit_cert is not None:
        args.emit_cert.parent.mkdir(parents=True, exist_ok=True)
        args.emit_cert.write_text(encoded, encoding="utf-8")

    if args.check:
        if not CERT_PATH.exists():
            print(f"missing_certificate={CERT_PATH}")
            return 1
        expected = CERT_PATH.read_text(encoding="utf-8")
        if expected != encoded:
            print("certificate_mismatch")
            return 1
        print("certificate_check: PASS")

    passed = len(results) == len(gates) and all(row["pass"] for row in results)
    print(f"RESULT: {'PASS' if passed else 'FAIL'} ({sum(row['pass'] for row in results)}/{len(gates)})")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
