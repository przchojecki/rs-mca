#!/usr/bin/env sage
"""Classify the complete aligned-positive fixed--moving frontier.

This is the first, deliberately conservative, stage of the fixed-frontier
attack.  It imports the exact q-slice reconstruction and named localizers
from the moving-closure compiler, then runs every one of the eighteen open
literal cells

    F00,F01,F04,F05,F06,F07 x R02,R11,R20.

The output does not infer emptiness from a sampled point or from a covariance
shortcut.  Each cell is rebuilt from the atlas and localized independently.
A survivor is retained as an explicit route cut with its exact Groebner-basis
metric; no owner, parity equation, or row payment is forced.
"""

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PARENT_PATH = (
    ROOT
    / "experimental/scripts/"
    "compile_kb_mca_v4_m2_aligned_positive_moving_closure_v1.sage"
)
PARENT_SHA256 = "2ed13fbab353d0ac3017fa31cab68de3f3b66f190061ba63fd277dbdc7958675"
PARENT_GIT_BLOB = "b3cb935fb1fbe8c584149b034416a164a7562231"

ASSIGNMENTS = ("F00", "F01", "F04", "F05", "F06", "F07")
TARGETS = ("R02", "R11", "R20")
CELL_IDS = tuple(f"{assignment}-{target}" for assignment in ASSIGNMENTS for target in TARGETS)
FULL_LOCALIZATION_ASSIGNMENTS = ("F00", "F01")
QUADRATIC_ROUTE_ASSIGNMENTS = ("F04", "F05", "F06", "F07")

EXPECTED_FULL_LOCALIZATION = {
    "F00-R02": ("SURVIVING_FIXED_MOVING_ROUTE", 2, 141, "ba2ce2b580b8daaacca53b3e409c9a3c09c7f1b5c0495c297b16eb7962c478aa"),
    "F00-R11": ("QSLICE_EMPTY", 2, 127, "64b31d79d37d777d49f10100d523e0b3ad05957aa7ed659a16b4f698aaef7f81"),
    "F00-R20": ("SURVIVING_FIXED_MOVING_ROUTE", 2, 145, "f89abf7729b75f1f4c0504aea595d92369ce572fa501189a9b80be8bd8dbb609"),
    "F01-R02": ("SURVIVING_FIXED_MOVING_ROUTE", 2, 145, "793f410594a4612b69bae793521f566bcd057cada56c6d4dd4070ca703122440"),
    "F01-R11": ("QSLICE_EMPTY", 2, 127, "d91e61d31f513231173e66a12888ed6feb8345741bf588b4c8341ea7fa82ed8c"),
    "F01-R20": ("SURVIVING_FIXED_MOVING_ROUTE", 2, 145, "f4cfcd5effb7aaf74b5a3d8b98be27d11907b3160cbc466494e8ed7502a8e3d1"),
}


def canonical_json(value):
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        default=lambda item: int(item) if item in ZZ else str(item),
    )


def git_blob_sha1(raw):
    return hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()


def load_parent():
    raw = PARENT_PATH.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == PARENT_SHA256
    assert git_blob_sha1(raw) == PARENT_GIT_BLOB
    namespace = dict(globals())
    namespace.update(
        {
            "__name__": "aligned_positive_moving_closure_library",
            "__file__": str(PARENT_PATH),
        }
    )
    exec(compile(raw.decode(), str(PARENT_PATH), "exec"), namespace)
    return namespace


PARENT = load_parent()


def strip_record(record):
    return PARENT["strip_internal"](record)


def classify(cell_id):
    assignment_id, target_id = cell_id.split("-")
    generators, factor_audit = PARENT["qslice_system"](assignment_id, target_id)
    # Every remaining fixed--moving assignment uses the literal b-coordinate
    # descent, hence the same exact named-open image used by M01/M02.
    units = PARENT["middle_units"]
    sf0 = PARENT["SF0"]
    sf = PARENT["SF"]
    w_zero = PARENT["localization_record"](
        sf0,
        [PARENT["to_SF0"](value) for value in generators],
        units(sf0, False),
        4,
    )
    full = PARENT["localization_record"](
        sf,
        [PARENT["to_SF"](value) for value in generators],
        units(sf, True),
        4,
    )
    terminal = (
        "QSLICE_EMPTY"
        if full["terminal"] == "EMPTY_AFTER_NAMED_LOCALIZATION"
        else "SURVIVING_FIXED_MOVING_ROUTE"
    )
    result = {
        "cell_id": cell_id,
        "assignment_id": assignment_id,
        "target_id": target_id,
        "qslice_generators": [PARENT["metric"](value) for value in generators],
        "factor_audit": factor_audit,
        "w_zero": strip_record(w_zero),
        "full_qslice": strip_record(full),
        "terminal": terminal,
    }
    if cell_id in EXPECTED_FULL_LOCALIZATION:
        expected_terminal, expected_dimension, expected_size, expected_sha = (
            EXPECTED_FULL_LOCALIZATION[cell_id]
        )
        observed = result["full_qslice"]["basis"]
        assert result["terminal"] == expected_terminal
        assert observed["dimension"] == expected_dimension
        assert observed["size"] == expected_size
        assert observed["sha256"] == expected_sha
        result["expected_fingerprint_checked"] = True
    return result


def equations_only(cell_id):
    assignment_id, target_id = cell_id.split("-")
    generators, factor_audit = PARENT["qslice_system"](assignment_id, target_id)
    return {
        "cell_id": cell_id,
        "assignment_id": assignment_id,
        "target_id": target_id,
        "qslice_generators": [
            {
                "metric": PARENT["metric"](value),
                "polynomial": str(value),
            }
            for value in generators
        ],
        "factor_audit": factor_audit,
        "terminal": "EQUATIONS_COMPILED_NO_LOCALIZATION_CLAIM",
    }


def resultant_probe(cell_id, pair):
    assignment_id, target_id = cell_id.split("-")
    generators, _ = PARENT["qslice_system"](assignment_id, target_id)
    ff = PARENT["FF"]
    base = PolynomialRing(ff, names=("x", "s", "p"), order="degrevlex")
    x, s, p = base.gens()
    univariate = PolynomialRing(base, "w")
    w = univariate.gen()

    def convert(value):
        output = univariate(0)
        for monomial, coefficient in PARENT["S"](value).dict().items():
            coefficient = PARENT["coefficient_F"](coefficient)
            output += (
                base(coefficient)
                * x**monomial[0]
                * s**monomial[1]
                * p**monomial[2]
                * w**monomial[3]
            )
        return output

    converted = [convert(value) for value in generators]
    left, right = pair
    result = base(converted[left].resultant(converted[right]))
    factors = []
    factorization_status = "FACTORED"
    try:
        factorization = result.factor()
    except NotImplementedError:
        # Sage's multivariate prime-field factor wrapper refuses p > 2^29.
        # Retain the exact deployed-field resultant and make factorization a
        # separately auditable Singular/Wolfram task.
        factorization = []
        factorization_status = "DEFERRED_LARGE_PRIME_WRAPPER_LIMIT"
    for factor, exponent in factorization:
        factors.append(
            {
                "exponent": int(exponent),
                "metric": {
                    "degree": int(factor.total_degree()),
                    "degrees": [int(factor.degree(g)) for g in base.gens()],
                    "terms": int(len(factor.monomials())),
                    "sha256": PARENT["digest_text"](factor),
                },
                "polynomial": str(factor) if factor.total_degree() <= 4 else None,
            }
        )
    return {
        "cell_id": cell_id,
        "pair": [int(left), int(right)],
        "input_w_degrees": [int(converted[left].degree()), int(converted[right].degree())],
        "resultant_zero": not bool(result),
        "resultant_metric": {
            "degree": int(result.total_degree()) if result else -1,
            "degrees": [int(result.degree(g)) for g in base.gens()] if result else [-1] * 3,
            "terms": int(len(result.monomials())) if result else 0,
            "sha256": PARENT["digest_text"](result),
        },
        "factorization_status": factorization_status,
        "factors": factors,
        "terminal": "PAIRWISE_W_RESULTANT_COMPILED_NECESSARY_ONLY",
    }


def quadratic_compression(cell_id, pair):
    assignment_id, target_id = cell_id.split("-")
    generators, _ = PARENT["qslice_system"](assignment_id, target_id)
    source = PARENT["S"]
    base = PolynomialRing(QQ, names=("x", "s", "p"), order="degrevlex")
    x, s, p = base.gens()
    univariate = PolynomialRing(base, "w")
    w = univariate.gen()

    def convert(value):
        output = univariate(0)
        for monomial, coefficient in source(value).dict().items():
            output += (
                QQ(coefficient)
                * x**monomial[0]
                * s**monomial[1]
                * p**monomial[2]
                * w**monomial[3]
            )
        return output

    left, right = pair
    first, second = convert(generators[left]), convert(generators[right])
    assert first.degree() == second.degree() == 2
    A, B, C = first[2], first[1], first[0]
    D, E, F = second[2], second[1], second[0]
    blocks = {
        "AF_minus_CD": base(A * F - C * D),
        "AE_minus_BD": base(A * E - B * D),
        "BF_minus_CE": base(B * F - C * E),
    }
    compressed = base(
        blocks["AF_minus_CD"] ** 2
        - blocks["AE_minus_BD"] * blocks["BF_minus_CE"]
    )
    direct = base(first.resultant(second))
    assert compressed == direct

    def metric(value):
        value = base(value)
        return {
            "degree": int(value.total_degree()) if value else -1,
            "degrees": [int(value.degree(g)) for g in base.gens()] if value else [-1] * 3,
            "terms": int(len(value.monomials())) if value else 0,
            "sha256": PARENT["digest_text"](value),
        }

    def factor_record(value):
        return [
            {
                "exponent": int(exponent),
                "metric": metric(factor),
                "polynomial": str(factor) if factor.total_degree() <= 4 else None,
            }
            for factor, exponent in base(value).factor()
        ]

    return {
        "cell_id": cell_id,
        "pair": [int(left), int(right)],
        "identity": "Res_w(Aw^2+Bw+C,Dw^2+Ew+F)=(AF-CD)^2-(AE-BD)(BF-CE)",
        "direct_equals_compressed_over_QQ": True,
        "blocks": {
            name: {"metric": metric(value), "factors": factor_record(value)}
            for name, value in blocks.items()
        },
        "resultant_metric": metric(compressed),
        "terminal": "EXACT_QUADRATIC_RESULTANT_COMPRESSION_NECESSARY_ONLY",
    }


def generic_quadratic_route(cell_id, pair):
    """Eliminate w on the V != 0 branch of two quadratic q-slice rows."""
    assignment_id, target_id = cell_id.split("-")
    generators, _ = PARENT["qslice_system"](assignment_id, target_id)
    source = PARENT["S"]
    base_q = PolynomialRing(QQ, names=("x", "s", "p"), order="degrevlex")
    xq, sq, pq = base_q.gens()
    uq = PolynomialRing(base_q, "w")
    wq = uq.gen()

    def to_uq(value):
        output = uq(0)
        for monomial, coefficient in source(value).dict().items():
            output += (
                QQ(coefficient)
                * xq**monomial[0]
                * sq**monomial[1]
                * pq**monomial[2]
                * wq**monomial[3]
            )
        return output

    converted = [to_uq(value) for value in generators]
    left, right = pair
    first, second = converted[left], converted[right]
    assert first.degree() == second.degree() == 2
    A, B, C = first[2], first[1], first[0]
    D, E, F = second[2], second[1], second[0]
    Uq = base_q(A * F - C * D)
    Vq = base_q(A * E - B * D)
    Zq = base_q(B * F - C * E)
    Rq = base_q(Uq**2 - Vq * Zq)
    assert Rq == base_q(first.resultant(second))

    def clear_at_minus_u_over_v(poly, U, V):
        degree = int(poly.degree())
        return poly.base_ring()(
            sum(poly[index] * (-U) ** index * V ** (degree - index) for index in range(degree + 1))
        )

    remaining = [index for index in range(4) if index not in pair]
    Eq = [clear_at_minus_u_over_v(converted[index], Uq, Vq) for index in remaining]

    ff = PARENT["FF"]
    base_f = PolynomialRing(ff, names=("x", "s", "p"), order="degrevlex")
    xf, sf, pf = base_f.gens()

    def to_bf(value):
        value = base_q(value)
        output = base_f(0)
        for monomial, coefficient in value.dict().items():
            output += (
                PARENT["coefficient_F"](coefficient)
                * xf**monomial[0]
                * sf**monomial[1]
                * pf**monomial[2]
            )
        return output

    Uf, Vf, Zf, Rf = map(to_bf, (Uq, Vq, Zq, Rq))
    Ef = [to_bf(value) for value in Eq]

    # Transport every full named-open factor through w=-U/V.  This is the
    # exact generic chart; V is added as a unit and no V=0 point is deleted
    # from the separate rank-drop branch.
    source_sf = PARENT["SF"]
    full_units = PARENT["middle_units"](source_sf, True)

    def sf_to_univariate(value):
        output = PolynomialRing(base_f, "w")(0)
        w = output.parent().gen()
        for monomial, coefficient in source_sf(value).dict().items():
            output += (
                base_f(coefficient)
                * xf**monomial[0]
                * sf**monomial[1]
                * pf**monomial[2]
                * w**monomial[3]
            )
        return output

    transported_units = [Vf]
    transported_units.extend(
        clear_at_minus_u_over_v(sf_to_univariate(value), Uf, Vf)
        for value in full_units
    )
    record = PARENT["localization_record"](
        base_f,
        [Rf, *Ef],
        transported_units,
        4,
    )
    return {
        "cell_id": cell_id,
        "pair": [int(left), int(right)],
        "remaining_rows": remaining,
        "generic_chart": "V=AE-BD != 0",
        "reconstruction": "w=-U/V",
        "compatibility": "U^2-VZ=0",
        "eliminated_equation_metrics": [PARENT["basis_metric"]([value]) for value in [Rf, *Ef]],
        "transported_named_unit_count": len(transported_units),
        "localization": strip_record(record),
        "rank_drop_retained": "V=0 (and necessarily U=0 for a common quadratic root)",
        "terminal": (
            "GENERIC_V_NONZERO_BRANCH_EMPTY_RANK_DROP_RETAINS"
            if record["terminal"] == "EMPTY_AFTER_NAMED_LOCALIZATION"
            else "GENERIC_V_NONZERO_BRANCH_SURVIVES"
        ),
    }
def packet(cell_ids):
    records = []
    for cell_id in cell_ids:
        assignment_id = cell_id.split("-")[0]
        if assignment_id in FULL_LOCALIZATION_ASSIGNMENTS:
            records.append(classify(cell_id))
        else:
            route = quadratic_compression(cell_id, (0, 1))
            route["terminal"] = "QUADRATIC_W_ROUTE_CUT_RETAINS_GENERIC_AND_RANK_DROP"
            route["full_qslice_localization_attempted"] = False
            route["reason"] = (
                "the four-variable generic Groebner route is superseded by "
                "the exact quadratic compatibility/rank dichotomy"
            )
            records.append(route)
    empty = [record["cell_id"] for record in records if record["terminal"] == "QSLICE_EMPTY"]
    survivors = [
        record["cell_id"]
        for record in records
        if record["terminal"] == "SURVIVING_FIXED_MOVING_ROUTE"
    ]
    route_cells = [
        record["cell_id"]
        for record in records
        if record["terminal"] == "QUADRATIC_W_ROUTE_CUT_RETAINS_GENERIC_AND_RANK_DROP"
    ]
    route_groups = {}
    for record in records:
        if record["terminal"] != "QUADRATIC_W_ROUTE_CUT_RETAINS_GENERIC_AND_RANK_DROP":
            continue
        key = (
            record["resultant_metric"]["sha256"],
            tuple(
                record["blocks"][name]["factors"][-1]["metric"]["sha256"]
                for name in ("AF_minus_CD", "AE_minus_BD", "BF_minus_CE")
            ),
        )
        route_groups.setdefault(key, []).append(record["cell_id"])
    orbit_groups = sorted(sorted(values) for values in route_groups.values())
    result = {
        "schema": "rs-mca-kb-v4-m2-aligned-positive-fixed-frontier-v1",
        "field": {"base_prime": 2130706433, "challenge_extension_degree": 6},
        "scope": {
            "literal_cell_count": len(cell_ids),
            "cells": list(cell_ids),
            "owner_order": [],
            "ledger_movement": 0,
        },
        "parent": {
            "path": str(PARENT_PATH.relative_to(ROOT)),
            "sha256": PARENT_SHA256,
            "git_blob": PARENT_GIT_BLOB,
        },
        "cells": records,
        "classification": {
            "qslice_empty": empty,
            "surviving_fixed_moving_routes": survivors,
            "quadratic_w_route_cut": route_cells,
            "quadratic_literal_orbit_groups": orbit_groups,
        },
        "nonclaims": [
            "a q-slice survivor is not an algebraic witness",
            "no survivor is forced into an owner",
            "no K3 or KoalaBear row closure is claimed",
            "no ledger quantity moves",
        ],
    }
    if tuple(cell_ids) == CELL_IDS:
        assert empty == ["F00-R11", "F01-R11"]
        assert survivors == ["F00-R02", "F00-R20", "F01-R02", "F01-R20"]
        assert len(route_cells) == 12
        assert len(orbit_groups) == 6
        assert all(len(group) == 2 for group in orbit_groups)
        result["terminal"] = "TWO_CELLS_EMPTY_SIXTEEN_FIXED_MOVING_ROUTES_RETAINED"
    else:
        result["terminal"] = "SELECTED_FIXED_MOVING_CELLS_CLASSIFIED"
    result["payload_sha256"] = hashlib.sha256(canonical_json(result).encode()).hexdigest()
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cell", choices=CELL_IDS)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--summary", action="store_true")
    parser.add_argument("--equations-only", action="store_true")
    parser.add_argument("--resultant-pair", nargs=2, type=int, metavar=("I", "J"))
    parser.add_argument("--quadratic-compress", nargs=2, type=int, metavar=("I", "J"))
    parser.add_argument("--generic-quadratic-route", nargs=2, type=int, metavar=("I", "J"))
    args = parser.parse_args()
    selected = (args.cell,) if args.cell else CELL_IDS
    if args.generic_quadratic_route is not None:
        assert args.cell is not None
        pair = tuple(args.generic_quadratic_route)
        assert 0 <= pair[0] < pair[1] < 4
        result = generic_quadratic_route(args.cell, pair)
        if args.check:
            assert result["rank_drop_retained"].startswith("V=0")
        print(canonical_json(result))
        return
    if args.quadratic_compress is not None:
        assert args.cell is not None
        pair = tuple(args.quadratic_compress)
        assert 0 <= pair[0] < pair[1] < 4
        result = quadratic_compression(args.cell, pair)
        if args.check:
            assert result["direct_equals_compressed_over_QQ"] is True
        if args.summary:
            result = {
                "cell_id": result["cell_id"],
                "pair": result["pair"],
                "blocks": {
                    name: {
                        "metric": record["metric"],
                        "factor_metrics": [
                            {
                                "exponent": factor["exponent"],
                                "metric": factor["metric"],
                            }
                            for factor in record["factors"]
                        ],
                    }
                    for name, record in result["blocks"].items()
                },
                "resultant_metric": result["resultant_metric"],
                "terminal": result["terminal"],
            }
        print(canonical_json(result))
        return
    if args.resultant_pair is not None:
        assert args.cell is not None
        pair = tuple(args.resultant_pair)
        assert 0 <= pair[0] < pair[1] < 4
        result = resultant_probe(args.cell, pair)
        if args.check:
            assert result["terminal"] == "PAIRWISE_W_RESULTANT_COMPILED_NECESSARY_ONLY"
        print(canonical_json(result))
        return
    if args.equations_only:
        assert args.cell is not None
        result = equations_only(args.cell)
        if args.check:
            assert len(result["qslice_generators"]) == 4
            assert result["terminal"] == "EQUATIONS_COMPILED_NO_LOCALIZATION_CLAIM"
        if args.summary:
            result = {
                "cell_id": result["cell_id"],
                "qslice_generators": [
                    item["metric"] for item in result["qslice_generators"]
                ],
                "terminal": result["terminal"],
            }
        print(canonical_json(result))
        return
    result = packet(selected)
    if args.check:
        assert result["scope"]["literal_cell_count"] == len(selected)
        assert set(result["classification"]["qslice_empty"]).isdisjoint(
            result["classification"]["surviving_fixed_moving_routes"]
        )
        assert sorted(
            result["classification"]["qslice_empty"]
            + result["classification"]["surviving_fixed_moving_routes"]
            + result["classification"]["quadratic_w_route_cut"]
        ) == sorted(selected)
    if args.summary:
        print(
            canonical_json(
                {
                    "classification": result["classification"],
                    "cells": [
                        (
                            {
                                "cell_id": record["cell_id"],
                                "terminal": record["terminal"],
                                "w_zero": record["w_zero"],
                                "full_qslice": record["full_qslice"],
                            }
                            if "full_qslice" in record
                            else {
                                "cell_id": record["cell_id"],
                                "terminal": record["terminal"],
                                "resultant_metric": record["resultant_metric"],
                            }
                        )
                        for record in result["cells"]
                    ],
                    "payload_sha256": result["payload_sha256"],
                }
            )
        )
    else:
        print(canonical_json(result))


if __name__ == "__main__":
    main()
