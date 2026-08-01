#!/usr/bin/env sage
"""Exact compiler for the aligned-positive moving--moving closure packet.

The checked-in 36-cell q-slice atlas is the source authority.  This compiler
reconstructs its source equations, factors before localization, descends the
eight non-imported moving representatives to symmetric coordinates, and
checks exact named-unit localization over ``GF(2130706433)``.  The two
balanced q-slice survivors receive independently derived full-quotient
J/I-parity equations.

Scope:

* M00-R02 and M00-R20 are rebuilt directly.
* M01-R02/R11/R20 are rebuilt directly.
* M02-R02/R11/R20 are transported only by the literal checked
  ``b -> b^-1`` source identity.
* M03-R02/R11/R20 are rebuilt directly.
* M00-R11 is an explicit operational import from PR #1138, pinned below.

No generic saturation, covariance, owner payment, ledger movement, K3
closure, or KoalaBear-row closure is used or claimed.
"""

import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path


P0 = ZZ(2130706433)
FF = GF(P0)
ROOT = Path(__file__).resolve().parents[2]
SELF_PATH = (
    ROOT
    / "experimental/scripts/"
    "compile_kb_mca_v4_m2_aligned_positive_moving_closure_v1.sage"
)
ATLAS_PATH = (
    ROOT
    / "experimental/scripts/"
    "compile_kb_mca_v4_m2_aligned_positive_qslice_atlas_v1.sage"
)
ATLAS_SHA256 = "c382adee5be3b72dcb675b4932a681f65ae958f58e24c3f5fdb8163d4d1508b7"
ATLAS_BLOB = "946308dbc014ce952c0c1cc583cc3d579a61aecf"
CERTIFICATE_PATH = (
    ROOT
    / "experimental/data/certificates/"
    "kb-mca-v4-m2-aligned-positive-moving-closure-v1/"
    "kb_mca_v4_m2_aligned_positive_moving_closure_v1.json"
)

BASE_COMMIT = "826c0e7610604d550b8dd9b772c197a4e660e525"
BASE_CERT_PATH = (
    ROOT
    / "experimental/data/certificates/"
    "kb-mca-v4-m2-aligned-positive-f02-f03-deletion-v1/"
    "kb_mca_v4_m2_aligned_positive_f02_f03_deletion_v1.json"
)
BASE_COMPILER_PATH = (
    ROOT
    / "experimental/scripts/"
    "compile_kb_mca_v4_m2_aligned_positive_f02_f03_deletion_v1.sage"
)
BASE_VERIFIER_PATH = (
    ROOT
    / "experimental/scripts/"
    "verify_kb_mca_v4_m2_aligned_positive_f02_f03_deletion_v1.py"
)
BASE_DEPENDENCY = {
    "commit": BASE_COMMIT,
    "certificate": {
        "path": str(BASE_CERT_PATH.relative_to(ROOT)),
        "sha256": "4cfbc86bdf1c295e832fa23414d2a7b98ebc5a05bfe2cc88e0ecbf076c5e7925",
        "git_blob": "43fd4daa9c48d5f8fc7b4f5ad09f6e85b2c4160b",
        "payload_sha256": (
            "51572f4d190a3bceb31494ae7ee48f6b026346413ae398d2da4f7b1da1402438"
        ),
    },
    "compiler": {
        "path": str(BASE_COMPILER_PATH.relative_to(ROOT)),
        "sha256": "e65439765b029443f8f309da74e4195ba7cd96db9f1d0c89145d3582e3d04061",
        "git_blob": "cc4263b27a77ea4bd485602d14f8458e665a0ad9",
    },
    "verifier": {
        "path": str(BASE_VERIFIER_PATH.relative_to(ROOT)),
        "sha256": "80ab8beb9a4644b6d6779918c679baff440552bcd3c3134b4b405438c194cb4a",
        "git_blob": "3fd02ddb5d8b5e9fb84a27ca13215f23095f2166",
    },
    "closed_cells": [
        "F02-R02",
        "F02-R11",
        "F02-R20",
        "F03-R02",
        "F03-R11",
        "F03-R20",
    ],
}

M00_R11_IMPORT = {
    "pull_request": 1138,
    "commit": "cd41c6c71b5b7d114f4ca9b2f5c853ccdd3c341d",
    "cell_id": "M00-R11",
    "certificate_path": (
        "experimental/data/certificates/"
        "kb-mca-v4-m2-diagonal-112-moving-positive-balanced-v1/"
        "kb_mca_v4_m2_diagonal_112_moving_positive_balanced_v1.json"
    ),
    "certificate_blob": "f73d6a7841aec868f4e7788a688afbd9cffa117e",
    "certificate_payload_sha256": (
        "3f32af654c6527e97c036d09a07c1d5554923c484300d5c3141fd997cc3a7a05"
    ),
    "sage_path": (
        "experimental/scripts/"
        "verify_kb_mca_v4_m2_diagonal_112_moving_positive_balanced_v1.sage"
    ),
    "sage_blob": "42633c999aca12c0c4eb0726d4c84fc5bf0de3a9",
    "sage_sha256": "aacd902ddde53abde40ff29c8264758bb57b9741fd6593318a98df974075ee89",
    "sage_result_payload_sha256": (
        "329c9b206d6f03671fd8233afe7c49a005f7e4af0f668b2d2eb97f29efb9cc76"
    ),
    "terminal": "EMPTY_AFTER_NAMED_LOCALIZATION",
    "operational_dependency": True,
}


def digest_text(value):
    return hashlib.sha256(str(value).encode()).hexdigest()


def file_sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_blob_sha1(value):
    return hashlib.sha1(f"blob {len(value)}\0".encode() + value).hexdigest()


def canonical_json(value):
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        default=lambda item: int(item) if item in ZZ else str(item),
    )


def payload_sha(value):
    copied = dict(value)
    copied.pop("payload_sha256", None)
    return hashlib.sha256(canonical_json(copied).encode()).hexdigest()


def verify_base_dependency():
    for path, record in (
        (BASE_CERT_PATH, BASE_DEPENDENCY["certificate"]),
        (BASE_COMPILER_PATH, BASE_DEPENDENCY["compiler"]),
        (BASE_VERIFIER_PATH, BASE_DEPENDENCY["verifier"]),
    ):
        raw = path.read_bytes()
        assert hashlib.sha256(raw).hexdigest() == record["sha256"]
        assert git_blob_sha1(raw) == record["git_blob"]
    certificate = json.loads(BASE_CERT_PATH.read_text())
    expected_payload = BASE_DEPENDENCY["certificate"]["payload_sha256"]
    assert certificate["payload_sha256"] == expected_payload
    assert payload_sha(certificate) == expected_payload
    assert sorted(certificate["conclusions"]) == BASE_DEPENDENCY["closed_cells"]
    assert set(BASE_DEPENDENCY["closed_cells"]).isdisjoint(certificate["open_cells"])
    return True


def git_output(*arguments):
    process = subprocess.run(
        ["git", *arguments],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    assert process.returncode == 0, (
        f"git {' '.join(arguments)} failed: "
        f"{process.stderr.decode(errors='replace').strip()}"
    )
    return process.stdout


def verify_m00_r11_import():
    """Fail closed unless the exact external #1138 objects are available."""

    commit = M00_R11_IMPORT["commit"]
    resolved = git_output("rev-parse", f"{commit}^{{commit}}").decode().strip()
    assert resolved == commit
    assert git_output("cat-file", "-t", commit).decode().strip() == "commit"

    observed = {}
    raw_objects = {}
    for name, path_key, blob_key in (
        ("certificate", "certificate_path", "certificate_blob"),
        ("sage", "sage_path", "sage_blob"),
    ):
        path = M00_R11_IMPORT[path_key]
        blob = git_output("rev-parse", f"{commit}:{path}").decode().strip()
        assert blob == M00_R11_IMPORT[blob_key]
        raw = git_output("show", f"{commit}:{path}")
        assert git_blob_sha1(raw) == blob
        observed[name] = {
            "path": path,
            "git_blob": blob,
            "bytes": len(raw),
        }
        raw_objects[name] = raw

    certificate = json.loads(raw_objects["certificate"])
    payload = M00_R11_IMPORT["certificate_payload_sha256"]
    assert certificate["payload_sha256"] == payload
    assert payload_sha(certificate) == payload
    assert certificate["artifacts"]["sage_output_payload_sha256"] == (
        M00_R11_IMPORT["sage_result_payload_sha256"]
    )
    assert hashlib.sha256(raw_objects["sage"]).hexdigest() == (
        M00_R11_IMPORT["sage_sha256"]
    )
    assert certificate["artifacts"]["sage_sha256"] == (
        M00_R11_IMPORT["sage_sha256"]
    )
    assert certificate["schema"] == (
        "kb-mca-v4-m2-diagonal-112-moving-positive-balanced-v1"
    )
    assert certificate["field"]["prime"] == int(P0)
    assert certificate["field"]["challenge_extension_degree"] == 6
    assert certificate["scope"] == {
        "assignment_count": 1,
        "ledger_movement": 0,
        "profile": "(a,b,c)=(1,1,2)",
        "root_distribution": [1, 1],
        "source_branch": "saturated source-line",
        "target": "canonical moving-moving aligned-positive balanced pattern",
    }
    normalization = certificate["normalization"]
    assert normalization["moving_moving_edges"] == [
        ["2", "b"],
        ["2", "1/b"],
    ]
    assert normalization["root_distribution"] == [1, 1]
    assert normalization["target_quadratic"] == "(W-1/c)(W-1/d)"
    assert normalization["J0"] == ["2", "1/2", "b", "1/b"]
    assert normalization["J1"] == ["c", "d"]
    assert normalization["assignment_scope"] == {
        "canonical_only": True,
        "canonical_unordered_source_star_pair": [
            ["2", "b"],
            ["2", "1/b"],
        ],
        "covariance_used": False,
        "other_three_moving_moving_assignments": (
            "OPEN_SEPARATE_EXACT_SYSTEMS"
        ),
    }
    assert certificate["proof_status"] == (
        "PROVED_CANONICAL_MOVING_MOVING_ALIGNED_POSITIVE_BALANCED_1_1_EMPTY"
    )
    assert certificate["conclusion"][
        "canonical_source_star_pair_aligned_positive_balanced_1_1_empty"
    ]
    assert certificate["scope"]["ledger_movement"] == 0
    assert certificate["conclusion"] == {
        "canonical_source_star_pair_aligned_positive_balanced_1_1_empty": True,
        "complete_112_row_deleted": False,
        "k3_status": "OPEN",
        "koalabear_row_status": "OPEN",
        "ledger_movement": 0,
        "moving_moving_doubled_root_distributions_status": "OPEN",
        "near_aligned_and_exceptional_status": "OPEN",
        "other_three_moving_moving_assignments_status": (
            "OPEN_SEPARATE_EXACT_SYSTEMS"
        ),
    }
    assert certificate["nonclaims"] == [
        "no covariance or orbit transport from the canonical source-star pair",
        "no deletion of the other three moving-moving assignment systems",
        "no moving-moving doubled-root deletion",
        "no near-aligned positive or exceptional-branch deletion",
        "no complete (1,1,2) row deletion",
        "no owner, payment, K3 value, KoalaBear row bound, or Prize closure",
        "no theorem over arbitrary characteristics",
        "no use of the lower squared-quotient coefficients",
    ]
    assert certificate["review_status"] == {
        "fresh_independent_review": True,
        "result": "NO_ISSUE",
        "verdict": "GREEN",
    }
    return {
        "commit_object_exact": True,
        "objects": observed,
        "certificate_payload_recomputed": True,
        "sage_bytes_sha256_exact": True,
        "sage_result_payload_pin_exact": True,
        "statement_compatibility_exact": True,
        "canonical_edge_target_scope_exact": True,
        "nonclaims_exact": True,
        "proof_status_exact": True,
        "fresh_review_green": True,
    }


def metric(value):
    value = value.parent()(value)
    if not value:
        return {
            "degree": -1,
            "degrees": [-1 for _ in value.parent().gens()],
            "terms": 0,
            "sha256": digest_text(value),
        }
    return {
        "degree": int(value.total_degree()),
        "degrees": [int(value.degree(g)) for g in value.parent().gens()],
        "terms": int(len(value.monomials())),
        "sha256": digest_text(value),
    }


def representative_metric(value):
    """Metric for a noncanonical normal-form representative.

    Degree support is retained as an execution guard, but the textual digest
    is deliberately omitted: reduction by a non-reduced ``slimgb`` basis can
    select different representatives of the same quotient class.
    """

    result = metric(value)
    result.pop("sha256")
    return result


def primitive_in(ring, value):
    value = ring(value)
    if not value:
        return value
    value = ring(value / value.content())
    return -value if value.leading_coefficient() < 0 else value


def load_atlas():
    source_bytes = ATLAS_PATH.read_bytes()
    assert hashlib.sha256(source_bytes).hexdigest() == ATLAS_SHA256
    assert git_blob_sha1(source_bytes) == ATLAS_BLOB
    source = source_bytes.decode()
    needle = "        cells[cell_id] = {\n"
    assert source.count(needle) == 1
    source = source.replace(
        needle,
        "        RAW_CACHE[cell_id] = raw_lines\n" + needle,
    )
    namespace = dict(globals())
    namespace.update(
        {
            "__name__": "aligned_positive_atlas_library",
            "__file__": str(ATLAS_PATH),
            "RAW_CACHE": {},
        }
    )
    exec(compile(source, str(ATLAS_PATH), "exec"), namespace)
    return namespace


ATLAS = load_atlas()
R = ATLAS["R"]
K = ATLAS["K"]
b, c, d, w = R.gens()


def primitive_R(value):
    return primitive_in(R, value)


def factor_key(value):
    return str(primitive_R(value))


def factor_set(values):
    result = {}
    for value in values:
        for factor, _ in primitive_R(value).factor():
            factor = primitive_R(factor)
            result[factor_key(factor)] = factor
    return result


def named_units_R(assignment_id):
    common = [
        b,
        b - 1,
        b + 1,
        2 * b - 1,
        b - 2,
        c,
        d,
        c - d,
        c - 1,
        c + 1,
        d - 1,
        d + 1,
        c - 2,
        2 * c - 1,
        d - 2,
        2 * d - 1,
        c * d - 1,
        b - c,
        b - d,
        b * c - 1,
        b * d - 1,
        w - 1,
        w + 1,
        w**2 - (c + d) * w + c * d,
        1 - (c + d) * w + c * d * w**2,
    ]
    if assignment_id in ("M00", "M03"):
        common += [
            5 * c * d - 4 * c - 4 * d + 5,
            (
                c * d * w
                - 4 * c * d
                - 2 * c * w
                - 2 * d * w
                + 2 * c
                + 2 * d
                + 4 * w
                - 1
            ),
            (
                4 * c * d * w
                - c * d
                - 2 * c * w
                - 2 * d * w
                + 2 * c
                + 2 * d
                + w
                - 4
            ),
        ]
    else:
        common += [
            b**2 * c * d + b**2 - 2 * b * c - 2 * b * d + c * d + 1,
            (
                b**2 * c * d
                - b**2 * w
                + b * c * w
                + b * d * w
                - c * d * w
                - b * c
                - b * d
                + 1
            ),
            (
                b**2 * c * d * w
                - b * c * w
                - b * d * w
                - b**2
                + b * c
                + b * d
                - c * d
                + w
            ),
        ]
    return factor_set(common)


def factor_records(value):
    return [
        {
            "factor": str(primitive_R(factor))
            if factor.total_degree() <= 4
            else None,
            "exponent": int(exponent),
            "metric": metric(primitive_R(factor)),
        }
        for factor, exponent in primitive_R(value).factor()
    ]


def denominator_support_R(value, units):
    value = primitive_R(value)
    factors = []
    for factor, exponent in value.factor():
        factor = primitive_R(factor)
        named = factor_key(factor) in units
        assert named
        factors.append(
            {
                "factor": str(factor),
                "exponent": int(exponent),
                "named_unit": named,
            }
        )
    return {
        "denominator": metric(value),
        "factors": factors,
        "all_factors_named_units": True,
    }


def essential(value, units):
    kept = R(1)
    dropped = []
    for factor, exponent in primitive_R(value).factor():
        factor = primitive_R(factor)
        if factor_key(factor) in units:
            dropped.append(
                {
                    "factor": str(factor),
                    "exponent": int(exponent),
                }
            )
        else:
            kept *= factor**exponent
    return primitive_R(kept), dropped


# Symmetric q-slice coordinates.  x=b+b^-1 for M00/M03 and x=b for M01.
S = PolynomialRing(QQ, names=("x", "s", "p", "w"), order="degrevlex")
xS, sS, pS, wS = S.gens()
XS = PolynomialRing(S, "root")
root = XS.gen()
root_relation = root**2 - sS * root + pS


def fixed_descend(poly):
    ypoly, _ = ATLAS["palindromic_to_y"](poly)
    source_ring = ATLAS["Y_RING"]
    substitute = source_ring.hom([xS, root, sS - root, wS], XS)
    remainder = substitute(ypoly).mod(root_relation)
    return S(remainder[0]), S(remainder[1])


moving_substitute = R.hom([xS, root, sS - root, wS], XS)


def moving_descend(poly):
    remainder = moving_substitute(poly).mod(root_relation)
    return S(remainder[0]), S(remainder[1])


def symmetric_cd_dict(poly):
    """Exact coefficient-orbit descent c,d -> s=c+d,p=cd.

    Sage polynomial dictionaries use ETuple keys.  Keeping the partner in
    that exact key type is load-bearing: a Python tuple silently misses every
    partner and triggers an avoidable high-complexity fallback.
    """

    poly = primitive_R(poly)
    data = poly.dict()
    max_difference = max(abs(mon[1] - mon[2]) for mon in data)
    powers = [{(0, 0): QQ(2)}, {(1, 0): QQ(1)}]
    for _ in range(2, max_difference + 1):
        nxt = {}
        for (es, ep), coefficient in powers[-1].items():
            nxt[(es + 1, ep)] = nxt.get((es + 1, ep), 0) + coefficient
        for (es, ep), coefficient in powers[-2].items():
            nxt[(es, ep + 1)] = nxt.get((es, ep + 1), 0) - coefficient
        powers.append({mon: q for mon, q in nxt.items() if q})
    output = {}
    for mon, coefficient in data.items():
        eb, ec, ed, ew = mon
        partner = type(mon)((eb, ed, ec, ew))
        assert data.get(partner) == coefficient
        if ec > ed:
            continue
        if ec == ed:
            key = (eb, 0, ec, ew)
            output[key] = output.get(key, 0) + QQ(coefficient)
        else:
            for (es, ep), qcoefficient in powers[ed - ec].items():
                key = (eb, es, ep + ec, ew)
                output[key] = (
                    output.get(key, 0) + QQ(coefficient) * qcoefficient
                )
    return S({mon: q for mon, q in output.items() if q})


def qslice_system(assignment_id, target_id):
    ATLAS["build_assignment"](assignment_id)
    cell_id = f"{assignment_id}-{target_id}"
    raw = ATLAS["RAW_CACHE"][cell_id]
    units = named_units_R(assignment_id)
    essential_rows = []
    factor_audit = []
    for row in raw:
        fraction = K(row)
        numerator = primitive_R(fraction.numerator())
        denominator = primitive_R(fraction.denominator())
        reduced, dropped = essential(numerator, units)
        essential_rows.append(reduced)
        factor_audit.append(
            {
                "raw": metric(numerator),
                "clear_denominator_support": denominator_support_R(
                    denominator, units
                ),
                "factors_before_localization": factor_records(numerator),
                "essential": metric(reduced),
                "dropped_named_factors": dropped,
            }
        )
    descend = (
        fixed_descend
        if assignment_id in ("M00", "M03")
        else moving_descend
    )
    A0, B0 = descend(essential_rows[0])
    A1, B1 = descend(essential_rows[1])
    A2, B2 = descend(essential_rows[2])
    A3, B3 = descend(essential_rows[3])
    # The d-side is the c-side conjugate, up to one harmless projective-line
    # scalar already fixed by primitive whole-line normalization.
    assert A2 * (-B0) - B2 * (A0 + sS * B0) == 0
    assert A3 * (-B1) - B3 * (A1 + sS * B1) == 0
    generators = [A0, B0, A1, B1]
    return generators, factor_audit


SF = PolynomialRing(FF, names=("x", "s", "p", "w"), order="degrevlex")
xF, sF, pF, wF = SF.gens()
SF0 = PolynomialRing(FF, names=("x", "s", "p"), order="degrevlex")
x0, s0, p0 = SF0.gens()


def coefficient_F(value):
    value = QQ(value)
    return FF(value.numerator()) / FF(value.denominator())


def to_SF(value):
    result = SF(0)
    for mon, coefficient in S(value).dict().items():
        result += coefficient_F(coefficient) * prod(
            generator**exponent
            for generator, exponent in zip(SF.gens(), mon)
        )
    return result


def to_SF0(value):
    result = SF0(0)
    for mon, coefficient in S(value).dict().items():
        if mon[3]:
            continue
        result += coefficient_F(coefficient) * prod(
            generator**exponent
            for generator, exponent in zip(SF0.gens(), mon[:3])
        )
    return result


def fixed_units(ring, include_w):
    x, s, p = ring.gens()[:3]
    result = [
        p,
        s**2 - 4 * p,
        p - 1,
        1 - s + p,
        1 + s + p,
        4 - 2 * s + p,
        1 - 2 * s + 4 * p,
        5 * p - 4 * s + 5,
        x**2 - 4,
        2 * x - 5,
        1 + s**2 + p**2 - 2 * p + p * x**2 - s * (1 + p) * x,
    ]
    if include_w:
        w = ring.gens()[3]
        result += [
            w,
            w**2 - 1,
            w**2 - s * w + p,
            1 - s * w + p * w**2,
            p * w - 4 * p - 2 * s * w + 2 * s + 4 * w - 1,
            4 * p * w - p - 2 * s * w + 2 * s + w - 4,
        ]
    else:
        result += [2 * s - 4 * p - 1, 2 * s - p - 4]
    return result


def middle_units(ring, include_w):
    x, s, p = ring.gens()[:3]
    result = [
        p,
        s**2 - 4 * p,
        p - 1,
        1 - s + p,
        1 + s + p,
        4 - 2 * s + p,
        1 - 2 * s + 4 * p,
        x,
        x**2 - 1,
        x - 2,
        2 * x - 1,
        x**2 - s * x + p,
        1 - s * x + p * x**2,
        x**2 * p + x**2 - 2 * x * s + p + 1,
    ]
    if include_w:
        w = ring.gens()[3]
        result += [
            x**2 * p - x**2 * w + x * s * w - p * w - x * s + 1,
            x**2 * p * w - x * s * w - x**2 + x * s - p + w,
            w,
            w**2 - 1,
            w**2 - s * w + p,
            1 - s * w + p * w**2,
        ]
    else:
        result += [x**2 * p - x * s + 1]
    return result


def basis_metric(basis):
    return {
        "size": len(basis),
        "dimension": -1 if basis == [basis[0].parent()(1)] else int(
            basis[0].parent().ideal(basis).dimension()
        ),
        "sha256": digest_text("\n".join(str(value) for value in basis)),
    }


def localization_record(ring, generators, units, maximum_power=4):
    basis = list(
        ring.ideal(generators).groebner_basis(algorithm="singular:slimgb")
    )
    if basis == [ring(1)]:
        return {
            "basis": {
                "size": 1,
                "dimension": -1,
                "sha256": digest_text("1"),
            },
            "reduced_localizer_powers": [],
            "nilpotence_index": 0,
            "terminal": "UNIT_IDEAL",
        }
    localizer = ring(1)
    for unit in units:
        localizer = (localizer * unit).reduce(basis)
    powers = []
    current = ring(1)
    nilpotence_index = None
    for exponent in range(1, maximum_power + 1):
        current = (current * localizer).reduce(basis)
        powers.append({"exponent": exponent, **metric(current)})
        if current == 0:
            nilpotence_index = exponent
            break
    return {
        "basis": basis_metric(basis),
        "localizer_factor_count": len(units),
        "reduced_localizer": metric(localizer),
        "reduced_localizer_powers": powers,
        "nilpotence_index": nilpotence_index,
        "terminal": (
            "EMPTY_AFTER_NAMED_LOCALIZATION"
            if nilpotence_index is not None
            else "SURVIVES_NAMED_LOCALIZATION"
        ),
        "_basis": basis,
    }


def strip_internal(record):
    return {key: value for key, value in record.items() if key != "_basis"}


def primitive_S(value):
    return primitive_in(S, value)


def denominator_support_S(value, units):
    value = primitive_S(value)
    named = {
        str(primitive_S(factor))
        for unit in units
        for factor, _ in primitive_S(unit).factor()
    }
    factors = []
    for factor, exponent in value.factor():
        factor = primitive_S(factor)
        exact = str(factor) in named
        assert exact
        factors.append(
            {
                "factor": str(factor),
                "exponent": int(exponent),
                "named_unit": exact,
            }
        )
    return {
        "denominator": metric(value),
        "factors": factors,
        "all_factors_named_units": True,
    }


def edge_over(field, left, right):
    return vector(field, (left * right, -(left + right), 1))


def clear_lambda_one(field, value):
    value = field(value)
    equation = primitive_S(value.numerator())
    denominator = primitive_S(value.denominator())
    scalar = field(equation) / field(value.numerator())
    assert scalar.numerator().is_constant()
    assert scalar.denominator().is_constant()
    return equation, denominator, str(QQ(scalar))


def direct_middle_parity():
    """Direct M01 parity in x=b,s=c+d,p=cd coordinates."""

    field = S.fraction_field()
    x, s, p, w = map(field, S.gens())
    FW = PolynomialRing(field, "Wq")
    Wq = FW.gen()
    common, right, left = x, field(2), field(1) / 2
    first = edge_over(field, common, right)
    second = edge_over(field, left, common)
    f, g, m = p - w, 1 - w * p, -s * (1 - w)
    v = vector(FW, (f + g * Wq, m * (1 + Wq), g + f * Wq))
    v_common = v[0] + common * v[1] + common**2 * v[2]
    z = -field(v_common[0]) / field(v_common[1])
    vz = vector(field, (entry(z) for entry in v))
    linear_1 = vz[2]
    linear_0 = vz[1] + common * vz[2]
    target = (
        (linear_0 + left * linear_1) * first
        + (linear_0 + right * linear_1) * second
    ) / (left - right)
    target_0, target_1, target_2 = target
    difference = (target_0 - target_2) / (1 - z**2)
    rhs_sum = target_0 + target_2
    rhs_source = -((1 + p) * (1 - w**2) * difference / (2 * (1 - p)))
    block_det = w * (1 + z**2) - z * (1 + w**2)
    sum_outer = (rhs_sum * w - 2 * z * rhs_source) / block_det
    x1 = ((1 + z**2) * rhs_source - (1 + w**2) * rhs_sum / 2) / block_det
    x0 = (sum_outer + difference) / 2
    x2 = (sum_outer - difference) / 2
    at_w_2 = x2 + x1 * w + x0 * w**2
    x3 = (target_1 * w + z * s * at_w_2) / block_det
    x4 = (-(1 + z**2) * s * at_w_2 - (1 + w**2) * target_1) / block_det
    u = vector(
        FW,
        (
            x0 + x1 * Wq + x2 * Wq**2,
            x3 * (1 + Wq**2) + x4 * Wq,
            x2 + x1 * Wq + x0 * Wq**2,
        ),
    )
    FL = PolynomialRing(field, "lam")
    lam = FL.gen()
    FLT = PolynomialRing(FL, "T")
    T = FLT.gen()

    def endpoint(coefficients, source_index):
        return sum(
            FL(coefficients[index][source_index]) * T**index
            for index in range(3)
        )

    H = endpoint(u, 0) + lam * endpoint(v, 0)

    def evaluate(point):
        return FL(H(T=FL(point)))

    reciprocal_core = p * T**2 - s * T + 1
    core = T**2 - s * T + p
    pair_I = reciprocal_core.resultant(H) / p**2
    pair_J = core.resultant(H)
    product_J = pair_J
    for point in (field(2), field(1) / 2, x, 1 / x):
        product_J *= evaluate(point)
    product_I = pair_I
    for point in (w, 1 / w, z, 1 / z):
        product_I *= evaluate(point)
    equation_J, denominator_J, scalar_J = clear_lambda_one(
        field, field(product_J[1])
    )
    equation_I, denominator_I, scalar_I = clear_lambda_one(
        field, field(product_I[1])
    )
    E = xS**2 * pS - xS**2 * wS + xS * sS * wS - pS * wS - xS * sS + 1
    N = xS**2 * pS * wS - xS * sS * wS - xS**2 + xS * sS - pS + wS
    J, remainder_J = equation_J.quo_rem(wS**2 * E**6 * N)
    I, remainder_I = equation_I.quo_rem(E**3)
    assert remainder_J == 0 and remainder_I == 0
    return {
        "J": primitive_S(J),
        "I": primitive_S(I),
        "audit": {
            "J_equation": metric(equation_J),
            "J_denominator": metric(denominator_J),
            "J_denominator_support": denominator_support_S(
                denominator_J, middle_units(S, True)
            ),
            "J_clear_scalar": scalar_J,
            "J_divisor": "w^2*E_M^6*N_M",
            "I_equation": metric(equation_I),
            "I_denominator": metric(denominator_I),
            "I_denominator_support": denominator_support_S(
                denominator_I, middle_units(S, True)
            ),
            "I_clear_scalar": scalar_I,
            "I_divisor": "E_M^3",
        },
    }


def direct_fixed_parity(common_value):
    """Direct M00/M03 parity in x=b+b^-1,s=c+d,p=cd."""

    field = S.fraction_field()
    x, s, p, w = map(field, S.gens())
    common = field(common_value)
    FW = PolynomialRing(field, "Wq")
    Wq = FW.gen()
    f, g, m = p - w, 1 - w * p, -s * (1 - w)
    v = vector(FW, (f + g * Wq, m * (1 + Wq), g + f * Wq))
    v_common = v[0] + common * v[1] + common**2 * v[2]
    z = -field(v_common[0]) / field(v_common[1])
    vz = vector(field, (entry(z) for entry in v))
    linear_1 = vz[2]
    linear_0 = vz[1] + common * vz[2]
    # delta=b-b^-1.  The displayed symmetric vector is the numerator
    # before division by 1/b-b=-delta, hence delta*target is its negative.
    numerator_target = vector(
        field,
        (
            common * (x * linear_0 + 2 * linear_1),
            -(
                (2 * common + x) * linear_0
                + (common * x + 2) * linear_1
            ),
            2 * linear_0 + x * linear_1,
        ),
    )
    scaled_target = -numerator_target

    def evaluation(point):
        return matrix(
            field,
            (
                (1, point, point**2, 0, 0),
                (0, 0, 0, 1 + point**2, point),
                (point**2, point, 1, 0, 0),
            ),
        )

    at_w, at_z = evaluation(w), evaluation(z)
    coefficient_matrix = matrix(
        field,
        (
            at_w[0] - p * at_w[2],
            at_w[1] + s * at_w[2],
            *at_z.rows(),
        ),
    )
    solution = coefficient_matrix.solve_right(
        vector(field, (0, 0, *scaled_target))
    )
    u = vector(
        FW,
        (
            solution[0] + solution[1] * Wq + solution[2] * Wq**2,
            solution[3] * (1 + Wq**2) + solution[4] * Wq,
            solution[2] + solution[1] * Wq + solution[0] * Wq**2,
        ),
    )
    FL = PolynomialRing(field, "lam")
    lam = FL.gen()
    FLT = PolynomialRing(FL, "T")
    T = FLT.gen()

    def endpoint(coefficients, source_index):
        return sum(
            FL(coefficients[index][source_index]) * T**index
            for index in range(3)
        )

    H = endpoint(u, 0) + lam * endpoint(v, 0)

    def pair_norm(trace, product):
        quadratic = T**2 - FL(trace) * T + FL(product)
        remainder = H.mod(quadratic)
        constant = remainder[0]
        coefficient = remainder[1] if remainder.degree() == 1 else FL(0)
        return FL(
            constant**2
            + constant * coefficient * FL(trace)
            + coefficient**2 * FL(product)
        )

    def evaluate_T(point):
        return FL(H(T=FL(point)))

    product_J = (
        evaluate_T(field(2))
        * evaluate_T(field(1) / 2)
        * pair_norm(x, 1)
        * pair_norm(s, p)
    )
    product_I = (
        pair_norm(s / p, 1 / p)
        * evaluate_T(w)
        * evaluate_T(1 / w)
        * evaluate_T(z)
        * evaluate_T(1 / z)
    )
    equation_J, denominator_J, scalar_J = clear_lambda_one(
        field, field(product_J[1])
    )
    equation_I, denominator_I, scalar_I = clear_lambda_one(
        field, field(product_I[1])
    )
    E = pS * wS - 4 * pS - 2 * sS * wS + 2 * sS + 4 * wS - 1
    D = 4 * pS * wS - pS - 2 * sS * wS + 2 * sS + wS - 4
    L2 = xS * (pS + 1) - 2 * sS
    if common_value == 2:
        # L2 is not a parent unit.  Preserve the L2=0 component in the
        # parity equation; the subsequent I equation closes that chart.
        divisor_J = wS**2 * D * E**6
        divisor_I = E**3
        divisor_J_name = "w^2*D*E^6 (L2 retained)"
        divisor_I_name = "E^3"
    else:
        assert QQ(common_value) == QQ(1) / 2
        # Literal reciprocal fixed chart: again L2 is a genuine component,
        # not a named unit, and must remain in J=L2*P25.
        divisor_J = wS**2 * E * D**6
        divisor_I = D**3
        divisor_J_name = "w^2*E*D^6 (L2 retained)"
        divisor_I_name = "D^3"
    J, remainder_J = equation_J.quo_rem(divisor_J)
    I, remainder_I = equation_I.quo_rem(divisor_I)
    assert remainder_J == 0 and remainder_I == 0
    P25, remainder_L2 = J.quo_rem(L2)
    assert remainder_L2 == 0
    return {
        "J": primitive_S(J),
        "I": primitive_S(I),
        "audit": {
            "J_equation": metric(equation_J),
            "J_denominator": metric(denominator_J),
            "J_denominator_support": denominator_support_S(
                denominator_J, fixed_units(S, True)
            ),
            "J_clear_scalar": scalar_J,
            "J_divisor": divisor_J_name,
            "J_retained_L2": True,
            "P25_after_L2": metric(primitive_S(P25)),
            "I_equation": metric(equation_I),
            "I_denominator": metric(denominator_I),
            "I_denominator_support": denominator_support_S(
                denominator_I, fixed_units(S, True)
            ),
            "I_clear_scalar": scalar_I,
            "I_divisor": divisor_I_name,
        },
    }


def add_parity(base_record, parity):
    current = base_record["_basis"]
    stages = []
    units = middle_units(SF, True) if parity["kind"] == "middle" else fixed_units(SF, True)
    for name in ("J", "I"):
        polynomial = parity[name]
        polynomial_SF = to_SF(polynomial)
        remainder = polynomial_SF.reduce(current)
        # Singular's reduction against a non-reduced slimgb basis may choose
        # different representatives across otherwise identical runs.  The
        # representative hash is therefore not a proof invariant.  What is
        # invariant, and what we certify here, is
        #
        #   polynomial - remainder in <current>,
        #
        # so adjoining either polynomial gives exactly the same ideal.  The
        # augmented Groebner basis, localizer normal forms, and nilpotence
        # witness below remain pinned exactly.
        assert (polynomial_SF - remainder).reduce(current) == 0
        current = list(
            SF.ideal(current + [remainder]).groebner_basis(
                algorithm="singular:slimgb"
            )
        )
        stage = localization_record(SF, current, units, 4)
        stages.append(
            {
                "parity": name,
                "polynomial": metric(polynomial),
                "remainder": representative_metric(remainder),
                "remainder_provenance": {
                    "input_minus_remainder_in_prior_ideal": True,
                    "augmented_ideal_equals_direct_parity_ideal": True,
                    "representative_sha256_is_not_pinned": True,
                },
                **strip_internal(stage),
            }
        )
        if stage["terminal"] != "SURVIVES_NAMED_LOCALIZATION":
            break
    return stages


DIRECT_CELL_IDS = (
    "M00-R02",
    "M00-R20",
    "M01-R02",
    "M01-R11",
    "M01-R20",
    "M03-R02",
    "M03-R11",
    "M03-R20",
)

EXPECTED_BALANCED = {
    "M01-R11": {
        "polynomials": {
            "J": {
                "degree": 30,
                "terms": 10852,
                "sha256": (
                    "c8223c17919b39c46a7e55cfeb99badc6f1f5a2060c19a5dd0a11e44f0b276bb"
                ),
            },
            "I": {
                "degree": 64,
                "terms": 151178,
                "sha256": (
                    "b45202d5ff561fd29573f68af87e4236cfc2f764f090c730ae35e4c61bb5abcf"
                ),
            },
        },
        "stages": {
            "J": {
                "remainder": {
                    "degree": 21,
                    "terms": 6510,
                },
                "basis": {
                    "size": 174,
                    "dimension": 2,
                    "sha256": (
                        "ca39e61bb131e6374c40c618b593d4628685c9312c57a687d739c6d7e05ade4b"
                    ),
                },
                "reduced_localizer": {
                    "degree": 29,
                    "terms": 10663,
                    "sha256": (
                        "ce205ff564851d70594e436f89ad201a5158d685412f7b145fd4721f216fd080"
                    ),
                },
                "powers": [
                    {
                        "exponent": 1,
                        "degree": 29,
                        "terms": 10663,
                        "sha256": (
                            "ce205ff564851d70594e436f89ad201a5158d685412f7b145fd4721f216fd080"
                        ),
                    },
                    {
                        "exponent": 2,
                        "degree": 19,
                        "terms": 4435,
                        "sha256": (
                            "f37ec8bc24a65d1a76a48e964a767579b2158a976e81741b3f80de10b4de2541"
                        ),
                    },
                    {
                        "exponent": 3,
                        "degree": 19,
                        "terms": 4435,
                        "sha256": (
                            "22c07d45947eeef0501b5885a6d8eb524ad31d2a1f6327db108dc92828299d8a"
                        ),
                    },
                    {
                        "exponent": 4,
                        "degree": 19,
                        "terms": 4435,
                        "sha256": (
                            "0d1eb961f1bb4a1caaec230ee76649c1eb6531262345743095e3a84d341ed4e0"
                        ),
                    },
                ],
                "nilpotence_index": None,
                "terminal": "SURVIVES_NAMED_LOCALIZATION",
            },
            "I": {
                "remainder": {
                    "degree": 19,
                    "terms": 4435,
                },
                "basis": {
                    "size": 168,
                    "dimension": 2,
                    "sha256": (
                        "716d41185640c419fc02323fea1ae6a4d51c56f7af7b2ebd61d0d7dc82af4da2"
                    ),
                },
                "reduced_localizer": {
                    "degree": 29,
                    "terms": 10653,
                    "sha256": (
                        "77c4a7906b263686268a2422e65bd5172c6b790284e55a0b4dcb027b74898c37"
                    ),
                },
                "powers": [
                    {
                        "exponent": 1,
                        "degree": 29,
                        "terms": 10653,
                        "sha256": (
                            "77c4a7906b263686268a2422e65bd5172c6b790284e55a0b4dcb027b74898c37"
                        ),
                    },
                    {
                        "exponent": 2,
                        "degree": -1,
                        "terms": 0,
                        "sha256": (
                            "5feceb66ffc86f38d952786c6d696c79c2dbc239dd4e91b46729d73a27fb57e9"
                        ),
                    },
                ],
                "nilpotence_index": 2,
                "terminal": "EMPTY_AFTER_NAMED_LOCALIZATION",
            },
        },
    },
    "M03-R11": {
        "polynomials": {
            "J": {
                "degree": 27,
                "terms": 6249,
                "sha256": (
                    "8a77375685f0b7c5c14fe249cfe5b854a4f69c59d1220231b319e1660e2aabb0"
                ),
            },
            "I": {
                "degree": 46,
                "terms": 35534,
                "sha256": (
                    "e0dfb63e9c4120d9e85e126452404bba5d808e2a5bd22fc5075186aabe615793"
                ),
            },
        },
        "stages": {
            "J": {
                "remainder": {
                    "degree": 16,
                    "terms": 2382,
                },
                "basis": {
                    "size": 128,
                    "dimension": 2,
                    "sha256": (
                        "e40e327c73baf2fb8f52f6f77b06948e03d4d6bca4b1402e229d318b207765d6"
                    ),
                },
                "reduced_localizer": {
                    "degree": 23,
                    "terms": 3438,
                    "sha256": (
                        "3977ebccf184ea27187b5109166a40e06250afc15476c3dbb36de554c5ea03fb"
                    ),
                },
                "powers": [
                    {
                        "exponent": 1,
                        "degree": 23,
                        "terms": 3438,
                        "sha256": (
                            "3977ebccf184ea27187b5109166a40e06250afc15476c3dbb36de554c5ea03fb"
                        ),
                    },
                    {
                        "exponent": 2,
                        "degree": 14,
                        "terms": 1431,
                        "sha256": (
                            "03d3375e7d8b0abe430cb4203631b4b43cce99f48d5f6d4f6cd8176a049e9783"
                        ),
                    },
                    {
                        "exponent": 3,
                        "degree": 14,
                        "terms": 1431,
                        "sha256": (
                            "0bfdcd9047bcb0a75da061233cdb1a27d347ee0c489b0e25cf2fd9bd7d431668"
                        ),
                    },
                    {
                        "exponent": 4,
                        "degree": 14,
                        "terms": 1431,
                        "sha256": (
                            "8e2a3e8576d6ce17d4789a4b1758dd40ebad1a4ccadd67990ecc447e3f51b560"
                        ),
                    },
                ],
                "nilpotence_index": None,
                "terminal": "SURVIVES_NAMED_LOCALIZATION",
            },
            "I": {
                "remainder": {
                    "degree": 14,
                    "terms": 1431,
                },
                "basis": {
                    "size": 125,
                    "dimension": 2,
                    "sha256": (
                        "b5e83240875f0814497ee8378facc63dd70ae5f287ff3505dce86ce8f0636b05"
                    ),
                },
                "reduced_localizer": {
                    "degree": 23,
                    "terms": 3429,
                    "sha256": (
                        "3a4b3feb0c7386b7969735587edf4a024570249ceaa50581a0e7a8348578f2d5"
                    ),
                },
                "powers": [
                    {
                        "exponent": 1,
                        "degree": 23,
                        "terms": 3429,
                        "sha256": (
                            "3a4b3feb0c7386b7969735587edf4a024570249ceaa50581a0e7a8348578f2d5"
                        ),
                    },
                    {
                        "exponent": 2,
                        "degree": -1,
                        "terms": 0,
                        "sha256": (
                            "5feceb66ffc86f38d952786c6d696c79c2dbc239dd4e91b46729d73a27fb57e9"
                        ),
                    },
                ],
                "nilpotence_index": 2,
                "terminal": "EMPTY_AFTER_NAMED_LOCALIZATION",
            },
        },
    },
}


def assert_expected_fields(observed, expected):
    for key, value in expected.items():
        assert observed[key] == value, (
            f"fingerprint mismatch for {key}: "
            f"observed={observed[key]!r} expected={value!r}"
        )


def assert_balanced_fingerprints(cell_id, parity, stages):
    expected = EXPECTED_BALANCED[cell_id]
    for name in ("J", "I"):
        assert_expected_fields(metric(parity[name]), expected["polynomials"][name])
    assert [stage["parity"] for stage in stages] == ["J", "I"]
    for stage in stages:
        stage_expected = expected["stages"][stage["parity"]]
        assert_expected_fields(stage["remainder"], stage_expected["remainder"])
        assert_expected_fields(stage["basis"], stage_expected["basis"])
        assert_expected_fields(
            stage["reduced_localizer"],
            stage_expected["reduced_localizer"],
        )
        assert len(stage["reduced_localizer_powers"]) == len(
            stage_expected["powers"]
        )
        for observed_power, expected_power in zip(
            stage["reduced_localizer_powers"],
            stage_expected["powers"],
        ):
            assert_expected_fields(observed_power, expected_power)
        assert stage["nilpotence_index"] == stage_expected["nilpotence_index"]
        assert stage["terminal"] == stage_expected["terminal"]


def classify_direct_cell(cell_id):
    assignment_id, target_id = cell_id.split("-")
    generators, factor_audit = qslice_system(assignment_id, target_id)
    unit_builder = (
        fixed_units if assignment_id in ("M00", "M03") else middle_units
    )
    w_zero = localization_record(
        SF0,
        [to_SF0(value) for value in generators],
        unit_builder(SF0, False),
        4,
    )
    full = localization_record(
        SF,
        [to_SF(value) for value in generators],
        unit_builder(SF, True),
        4,
    )
    result = {
        "cell_id": cell_id,
        "method": "DIRECT_QSLICE_AND_NAMED_LOCALIZATION",
        "qslice_generators": [metric(value) for value in generators],
        "factor_audit": factor_audit,
        "w_zero": strip_internal(w_zero),
        "full_qslice": strip_internal(full),
        "parity": [],
    }
    balanced_requires_parity = cell_id in EXPECTED_BALANCED
    if balanced_requires_parity:
        # A mutated or weakened q-slice computation must not bypass the
        # load-bearing pinned J/I stages by reporting the balanced cell
        # directly empty.
        assert full["terminal"] == "SURVIVES_NAMED_LOCALIZATION"
    if full["terminal"] == "SURVIVES_NAMED_LOCALIZATION":
        assert target_id == "R11" and assignment_id in ("M01", "M03")
        if assignment_id == "M01":
            parity = direct_middle_parity()
            parity["kind"] = "middle"
        else:
            parity = direct_fixed_parity(QQ(1) / 2)
            parity["kind"] = "fixed"
        result["parity_derivation"] = {
            **parity["audit"],
            "J_essential": metric(parity["J"]),
            "I_essential": metric(parity["I"]),
        }
        result["parity"] = add_parity(full, parity)
        assert_balanced_fingerprints(cell_id, parity, result["parity"])
        terminal = result["parity"][-1]["terminal"]
    else:
        assert not balanced_requires_parity
        terminal = full["terminal"]
    assert w_zero["terminal"] == "EMPTY_AFTER_NAMED_LOCALIZATION"
    assert terminal == "EMPTY_AFTER_NAMED_LOCALIZATION"
    result["terminal"] = terminal
    result["ledger_movement"] = 0
    return result


def build_source_R(assignment_id):
    geometry = ATLAS["assignment_geometry"](assignment_id)
    common = ATLAS["VERTEX_FORMULAS"][geometry["common_vertex"]]
    right = ATLAS["VERTEX_FORMULAS"][geometry["first_other_vertex"]]
    left = ATLAS["VERTEX_FORMULAS"][geometry["second_other_vertex"]]
    first = ATLAS["edge"](geometry["first_edge"])
    second = ATLAS["edge"](geometry["second_edge"])
    bK, cK, dK, wK = map(K, R.gens())
    KW = ATLAS["KW"]
    W = ATLAS["W"]
    q0, q1 = cK * dK, -(cK + dK)
    f, g, m = q0 - wK, 1 - wK * q0, q1 * (1 - wK)
    v = vector(KW, (f + g * W, m * (1 + W), g + f * W))
    v_common = v[0] + common * v[1] + common**2 * v[2]
    z = -K(v_common[0]) / K(v_common[1])
    vz = vector(K, (entry(z) for entry in v))
    linear_1 = vz[2]
    linear_0 = vz[1] + common * vz[2]
    target = (
        (linear_0 + left * linear_1) * first
        + (linear_0 + right * linear_1) * second
    ) / (left - right)
    target_0, target_1, target_2 = target
    difference = (target_0 - target_2) / (1 - z**2)
    rhs_sum = target_0 + target_2
    rhs_source = -((1 + q0) * (1 - wK**2) * difference / (2 * (1 - q0)))
    block_det = wK * (1 + z**2) - z * (1 + wK**2)
    sum_outer = (rhs_sum * wK - 2 * z * rhs_source) / block_det
    x1 = ((1 + z**2) * rhs_source - (1 + wK**2) * rhs_sum / 2) / block_det
    x0 = (sum_outer + difference) / 2
    x2 = (sum_outer - difference) / 2
    at_w_2 = x2 + x1 * wK + x0 * wK**2
    x3 = (target_1 * wK - z * q1 * at_w_2) / block_det
    x4 = ((1 + z**2) * q1 * at_w_2 - (1 + wK**2) * target_1) / block_det
    u = vector(
        KW,
        (
            x0 + x1 * W + x2 * W**2,
            x3 * (1 + W**2) + x4 * W,
            x2 + x1 * W + x0 * W**2,
        ),
    )
    return u, v, z


def reverse_b_R(value):
    """Return b^deg_b(value) value(1/b) without fraction substitution."""

    value = R(value)
    if value == 0:
        return value
    degree = value.degree(b)
    return R(
        {
            (degree - mon[0], mon[1], mon[2], mon[3]): coefficient
            for mon, coefficient in value.dict().items()
        }
    )


def pull_b_K(value):
    """Apply b -> 1/b exactly using numerator/denominator reversal."""

    value = K(value)
    numerator = R(value.numerator())
    denominator = R(value.denominator())
    numerator_degree = numerator.degree(b) if numerator else 0
    denominator_degree = denominator.degree(b)
    return K(
        reverse_b_R(numerator) * b**denominator_degree
        / (reverse_b_R(denominator) * b**numerator_degree)
    )


def pull_b_KW(value):
    value = ATLAS["KW"](value)
    return ATLAS["KW"](
        [pull_b_K(value[index]) for index in range(value.degree() + 1)]
    )


def check_multiset(left, right):
    unmatched = list(right)
    for value in left:
        for index, candidate in enumerate(unmatched):
            if value == candidate:
                unmatched.pop(index)
                break
        else:
            return False
    return not unmatched


def literal_middle_transport():
    source_u, source_v, source_z = build_source_R("M01")
    target_u, target_v, target_z = build_source_R("M02")
    z_exact = pull_b_K(source_z) == target_z
    V_exact = (
        vector(ATLAS["KW"], (pull_b_KW(value) for value in source_v))
        == target_v
    )
    U_exact = (
        vector(ATLAS["KW"], (pull_b_KW(value) for value in source_u))
        == target_u
    )
    assert z_exact and V_exact and U_exact
    bK, cK, dK, wK = map(K, R.gens())
    source_J = [K(2), K(1) / 2, bK, 1 / bK, cK, dK]
    target_J = list(source_J)
    source_I = [1 / cK, 1 / dK, wK, 1 / wK, source_z, 1 / source_z]
    target_I = [1 / cK, 1 / dK, wK, 1 / wK, target_z, 1 / target_z]
    source_K = [wK, source_z, 1 / source_z, 1 / cK, 1 / dK]
    target_K = [wK, target_z, 1 / target_z, 1 / cK, 1 / dK]
    source_R = [1 / wK, *source_J]
    target_R = [1 / wK, *target_J]
    label_checks = {}
    for name, source_labels, target_labels in (
        ("J", source_J, target_J),
        ("I", source_I, target_I),
        ("K", source_K, target_K),
        ("R", source_R, target_R),
    ):
        exact = check_multiset(
            [pull_b_K(value) for value in source_labels],
            target_labels,
        )
        assert exact
        label_checks[name] = exact

    # The complete named open is invariant.  The monomial b is handled
    # separately: under inversion it is 1/b and remains a unit.  Every other
    # irreducible named factor transports, after clearing a power of b, to
    # exactly one target named factor up to primitive sign.
    source_unit_factors = list(named_units_R("M01").values())
    target_unit_factors = list(named_units_R("M02").values())
    source_nonmonomial = [
        factor for factor in source_unit_factors if factor_key(factor) != factor_key(b)
    ]
    target_nonmonomial = [
        factor for factor in target_unit_factors if factor_key(factor) != factor_key(b)
    ]
    pulled_unit_factors = []
    for factor in source_nonmonomial:
        pulled_unit_factors.append(primitive_R(reverse_b_R(factor)))
    named_unit_multiset_exact = check_multiset(
        pulled_unit_factors, target_nonmonomial
    )
    assert named_unit_multiset_exact

    # Compute, rather than assume, transport of G and of every factor product
    # entering the full J/I quotient identities.
    KW = ATLAS["KW"]
    Wsource = ATLAS["W"]
    KT = PolynomialRing(KW, "Tsource")
    Tsource = KT.gen()

    def source_polynomial(coefficients):
        return KT(
            sum(KT(coefficients[index]) * Tsource**index for index in range(3))
        )

    def G_polynomial(u_values, v_values):
        U = source_polynomial(u_values)
        V = source_polynomial(v_values)
        return U**2 - KT(Wsource) * V**2

    def pull_KT(value):
        value = KT(value)
        return KT(
            [pull_b_KW(value[index]) for index in range(value.degree() + 1)]
        )

    source_G = G_polynomial(source_u, source_v)
    target_G = G_polynomial(target_u, target_v)
    G_exact = pull_KT(source_G) == target_G
    assert G_exact

    def G_values(G, labels):
        return [KW(G(KW(label))) for label in labels]

    J_G_factor_multiset_exact = check_multiset(
        [pull_b_KW(value) for value in G_values(source_G, source_J)],
        G_values(target_G, target_J),
    )
    I_G_factor_multiset_exact = check_multiset(
        [pull_b_KW(value) for value in G_values(source_G, source_I)],
        G_values(target_G, target_I),
    )
    assert J_G_factor_multiset_exact and I_G_factor_multiset_exact
    # Equality of exact factor multisets proves equality of their products
    # without expanding the six large rational factors.
    J_G_product_exact = J_G_factor_multiset_exact
    I_G_product_exact = I_G_factor_multiset_exact

    LT = PolynomialRing(K, "Ylabel")
    Ylabel = LT.gen()

    def locator(labels):
        return prod((Ylabel - K(label) for label in labels), LT(1))

    def pull_LT(value):
        value = LT(value)
        return LT(
            [pull_b_K(value[index]) for index in range(value.degree() + 1)]
        )

    source_q = (Ylabel - cK) * (Ylabel - dK)
    target_q = (Ylabel - cK) * (Ylabel - dK)
    q_exact = pull_LT(source_q) == target_q
    K_locator_exact = pull_LT(locator(source_K)) == locator(target_K)
    R_locator_exact = pull_LT(locator(source_R)) == locator(target_R)
    assert q_exact and K_locator_exact and R_locator_exact
    full_J_exact = J_G_product_exact and K_locator_exact and q_exact
    full_I_exact = I_G_product_exact and R_locator_exact and q_exact
    assert full_J_exact and full_I_exact

    qslice_checks = []
    ATLAS["build_assignment"]("M01")
    ATLAS["build_assignment"]("M02")
    for target_id in ("R02", "R11", "R20"):
        source_rows = ATLAS["RAW_CACHE"][f"M01-{target_id}"]
        target_rows = ATLAS["RAW_CACHE"][f"M02-{target_id}"]
        assert len(source_rows) == len(target_rows) == 4
        row_checks = []
        for source, target in zip(source_rows, target_rows):
            source_rational = K(source)
            target_rational = K(target)
            source_denominator = primitive_R(source_rational.denominator())
            target_denominator = primitive_R(target_rational.denominator())
            source_denominator_support = denominator_support_R(
                source_denominator,
                named_units_R("M01"),
            )
            target_denominator_support = denominator_support_R(
                target_denominator,
                named_units_R("M02"),
            )
            pulled_rational = pull_b_K(source_rational)
            ratio = K(pulled_rational / target_rational)
            ratio_numerator_support = denominator_support_R(
                primitive_R(ratio.numerator()),
                named_units_R("M02"),
            )
            ratio_denominator_support = denominator_support_R(
                primitive_R(ratio.denominator()),
                named_units_R("M02"),
            )
            source_numerator = primitive_R(source_rational.numerator())
            target_numerator = primitive_R(target_rational.numerator())
            pulled_numerator = primitive_R(reverse_b_R(source_numerator))
            numerator_exact = (
                pulled_numerator == target_numerator
                or pulled_numerator == -target_numerator
            )
            assert numerator_exact
            row_checks.append(
                {
                    "cleared_numerator_up_to_projective_sign": numerator_exact,
                    "source_denominator_support": source_denominator_support,
                    "target_denominator_support": target_denominator_support,
                    "transport_ratio_numerator_support": (
                        ratio_numerator_support
                    ),
                    "transport_ratio_denominator_support": (
                        ratio_denominator_support
                    ),
                    "full_rational_zero_locus_transport_by_named_unit": True,
                }
            )
        assert all(
            row["full_rational_zero_locus_transport_by_named_unit"]
            for row in row_checks
        )
        qslice_checks.append(
            {
                "source_cell": f"M01-{target_id}",
                "target_cell": f"M02-{target_id}",
                "row_count": len(row_checks),
                "all_cleared_numerators_transport_up_to_projective_sign": all(
                    row["cleared_numerator_up_to_projective_sign"]
                    for row in row_checks
                ),
                "all_full_rational_zero_loci_transport_by_named_units": all(
                    row["full_rational_zero_locus_transport_by_named_unit"]
                    for row in row_checks
                ),
                "rows": row_checks,
            }
        )
    return {
        "map": "b -> b^-1",
        "source_assignment": "M01",
        "target_assignment": "M02",
        "z_exact": z_exact,
        "V_exact": V_exact,
        "U_exact": U_exact,
        "named_unit_transport": {
            "b_nonzero_chart_maps_to_reciprocal_unit": True,
            "source_factor_count": len(source_unit_factors),
            "target_factor_count": len(target_unit_factors),
            "nonmonomial_factor_multiset_exact": named_unit_multiset_exact,
        },
        "label_factor_multisets_exact": label_checks,
        "computed_full_identity_transport": {
            "G_equals_U2_minus_WV2_exact": G_exact,
            "J_G_factor_multiset_exact": J_G_factor_multiset_exact,
            "I_G_factor_multiset_exact": I_G_factor_multiset_exact,
            "J_G_product_exact": J_G_product_exact,
            "I_G_product_exact": I_G_product_exact,
            "q_locator_exact": q_exact,
            "K_locator_exact": K_locator_exact,
            "R_locator_exact": R_locator_exact,
            "full_J_identity_exact_by_factor_transport": full_J_exact,
            "full_I_identity_exact_by_factor_transport": full_I_exact,
        },
        "qslice_checks": qslice_checks,
    }


def open_cell_fence():
    deleted_on_base = {
        f"{assignment}-{target}"
        for assignment in ("F02", "F03")
        for target in ("R02", "R11", "R20")
    }
    deleted_here = {
        f"{assignment}-{target}"
        for assignment in ("M00", "M01", "M02", "M03")
        for target in ("R02", "R11", "R20")
    }
    all_cells = {
        f"{assignment}-{target}"
        for assignment in ATLAS["ASSIGNMENT_EDGES"]
        for target in ("R02", "R11", "R20")
    }
    remaining = sorted(all_cells - deleted_on_base - deleted_here)
    assert len(all_cells) == 36
    assert len(deleted_on_base) == 6
    assert len(deleted_here) == 12
    assert len(remaining) == 18
    assert all(cell.startswith(("F00-", "F01-", "F04-", "F05-", "F06-", "F07-")) for cell in remaining)
    return {
        "atlas_cells": 36,
        "base_deleted_cells": sorted(deleted_on_base),
        "moving_cells_closed": sorted(deleted_here),
        "remaining_open_cells": remaining,
        "remaining_open_count": 18,
    }


def build_packet(selected_cell=None, precomputed_cells=None):
    assert verify_base_dependency()
    assert not (selected_cell is not None and precomputed_cells is not None)
    if precomputed_cells is None:
        cells = []
        selected = DIRECT_CELL_IDS if selected_cell is None else (selected_cell,)
        assert all(cell in DIRECT_CELL_IDS for cell in selected)
        for cell_id in selected:
            cells.append(classify_direct_cell(cell_id))
    else:
        cells = list(precomputed_cells)
        assert [cell["cell_id"] for cell in cells] == list(DIRECT_CELL_IDS)
        assert all(
            cell["terminal"] == "EMPTY_AFTER_NAMED_LOCALIZATION"
            and cell["ledger_movement"] == 0
            for cell in cells
        )
    imported_cell = dict(M00_R11_IMPORT)
    imported_cell["runtime_verification"] = verify_m00_r11_import()
    packet = {
        "schema": "rs-mca-kb-v4-m2-aligned-positive-moving-closure-v1",
        "field": {
            "base_prime": int(P0),
            "challenge_extension_degree": 6,
            "empty_localization_is_geometric_over_base_closure": True,
        },
        "statement": (
            "All twelve moving-moving aligned-positive (1,1,2) atlas "
            "cells are empty on the declared named open."
        ),
        "scope": {
            "atlas_cell_count": 36,
            "direct_cell_count": 8,
            "literal_transport_cell_count": 3,
            "imported_cell_count": 1,
            "closed_cell_count": 12,
            "remaining_open_cell_count": 18,
            "ledger_movement": 0,
        },
        "atlas_dependency": {
            "path": str(ATLAS_PATH.relative_to(ROOT)),
            "sha256": ATLAS_SHA256,
            "git_blob": ATLAS_BLOB,
        },
        "base_dependency": BASE_DEPENDENCY,
        "direct_cells": cells,
        "imported_cell": imported_cell,
        "ledger_movement": 0,
        "K3_closed": False,
        "KoalaBear_row_closed": False,
        "generic_saturation_used": False,
        "proof_status": (
            "PROVED_EXACT_ALL_12_MOVING_MOVING_ALIGNED_POSITIVE_CELLS_EMPTY"
        ),
        "nonclaims": [
            "no deletion of the eighteen remaining fixed-moving atlas cells",
            "no owner, charge, or ledger payment",
            "no K3 or KoalaBear-row closure",
            "no theorem over arbitrary characteristics",
            "no generic saturation or undeclared covariance",
        ],
    }
    if selected_cell is None:
        packet["execution"] = {
            "direct_cells_sharded": precomputed_cells is not None,
            "fresh_sage_process_per_direct_cell": precomputed_cells is not None,
            "reason": (
                "avoid long-lived Sage-Singular IPC state across independent cells"
                if precomputed_cells is not None
                else "monolithic diagnostic mode"
            ),
        }
        packet["literal_transport"] = literal_middle_transport()
        packet["open_cell_fence"] = open_cell_fence()
        packet["conclusion"] = {
            "all_twelve_moving_moving_cells_empty": True,
            "closed_cells": packet["open_cell_fence"]["moving_cells_closed"],
            "remaining_open_cells": packet["open_cell_fence"][
                "remaining_open_cells"
            ],
            "ledger_movement": 0,
            "K3_status": "OPEN",
            "KoalaBear_row_status": "OPEN",
        }
        packet["terminal"] = "ALL_12_MOVING_MOVING_CELLS_EMPTY"
    else:
        packet["statement"] = (
            f"Selected direct atlas cell {selected_cell} is empty on the "
            "declared named open."
        )
        packet["scope"] = {
            "selected_direct_cell": selected_cell,
            "direct_cell_count": 1,
            "ledger_movement": 0,
        }
        packet["proof_status"] = "PROVED_SELECTED_DIRECT_CELL_EMPTY"
        packet["nonclaims"] = [
            "no all-moving-cell closure claimed in selected-cell mode",
            "no owner, charge, or ledger payment",
            "no K3 or KoalaBear-row closure",
        ]
        packet["terminal"] = "SELECTED_DIRECT_CELL_EMPTY"
    packet["payload_sha256"] = payload_sha(packet)
    return packet


def selected_cell_shard(cell_id):
    """Replay one direct cell in a fresh Sage/Singular process."""

    sage = shutil.which("sage") or "/usr/local/bin/sage"
    process = subprocess.run(
        [sage, str(SELF_PATH), "--cell", cell_id, "--json"],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    assert process.returncode == 0, (
        f"direct shard {cell_id} failed:\n"
        f"{process.stderr.decode(errors='replace')}\n"
        f"{process.stdout.decode(errors='replace')}"
    )
    output_lines = process.stdout.decode().splitlines()
    json_lines = [
        line for line in output_lines
        if line.startswith("{") and line.endswith("}")
    ]
    assert len(json_lines) == 1, (
        f"direct shard {cell_id} emitted {len(json_lines)} JSON records"
    )
    packet = json.loads(json_lines[0])
    assert packet["payload_sha256"] == payload_sha(packet)
    assert packet["terminal"] == "SELECTED_DIRECT_CELL_EMPTY"
    assert packet["proof_status"] == "PROVED_SELECTED_DIRECT_CELL_EMPTY"
    assert packet["scope"] == {
        "selected_direct_cell": cell_id,
        "direct_cell_count": 1,
        "ledger_movement": 0,
    }
    assert len(packet["direct_cells"]) == 1
    cell = packet["direct_cells"][0]
    assert cell["cell_id"] == cell_id
    assert cell["terminal"] == "EMPTY_AFTER_NAMED_LOCALIZATION"
    assert cell["ledger_movement"] == 0
    return cell


def build_sharded_packet():
    cells = [selected_cell_shard(cell_id) for cell_id in DIRECT_CELL_IDS]
    return build_packet(precomputed_cells=cells)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--cell", choices=DIRECT_CELL_IDS)
    parser.add_argument("--parity-only", choices=("M01", "M03"))
    parser.add_argument("--denominator-only", action="store_true")
    parser.add_argument("--transport-only", action="store_true")
    parser.add_argument("--import-only", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--emit", action="store_true")
    args = parser.parse_args()
    assert sum(
        bool(value)
        for value in (
            args.cell,
            args.parity_only,
            args.denominator_only,
            args.transport_only,
            args.import_only,
            args.emit,
        )
    ) <= 1
    if args.parity_only:
        assert verify_base_dependency()
        if args.parity_only == "M01":
            parity = direct_middle_parity()
            cell_id = "M01-R11"
        else:
            parity = direct_fixed_parity(QQ(1) / 2)
            cell_id = "M03-R11"
        expected = EXPECTED_BALANCED[cell_id]["polynomials"]
        for name in ("J", "I"):
            assert_expected_fields(metric(parity[name]), expected[name])
        packet = {
            "schema": "rs-mca-kb-v4-m2-aligned-positive-moving-closure-v1",
            "base_dependency": BASE_DEPENDENCY,
            "cell_id": cell_id,
            "parity_derivation": {
                **parity["audit"],
                "J_essential": metric(parity["J"]),
                "I_essential": metric(parity["I"]),
            },
            "cell_closure_claimed": False,
            "terminal": "PARITY_DENOMINATORS_AND_FINGERPRINTS_VERIFIED",
        }
        packet["payload_sha256"] = payload_sha(packet)
    elif args.denominator_only:
        assert verify_base_dependency()
        cells = []
        for cell_id in DIRECT_CELL_IDS:
            generators, factor_audit = qslice_system(*cell_id.split("-"))
            cells.append(
                {
                    "cell_id": cell_id,
                    "qslice_generators": [metric(value) for value in generators],
                    "factor_audit": factor_audit,
                }
            )
        packet = {
            "schema": "rs-mca-kb-v4-m2-aligned-positive-moving-closure-v1",
            "base_dependency": BASE_DEPENDENCY,
            "direct_cells": cells,
            "cell_closure_claimed": False,
            "terminal": "QSLICE_DENOMINATOR_SUPPORT_VERIFIED",
        }
        packet["payload_sha256"] = payload_sha(packet)
    elif args.transport_only:
        assert verify_base_dependency()
        packet = {
            "schema": "rs-mca-kb-v4-m2-aligned-positive-moving-closure-v1",
            "base_dependency": BASE_DEPENDENCY,
            "literal_transport": literal_middle_transport(),
            "base_open_cell_count": 30,
            "moving_cells_closed_by_this_mode": [],
            "terminal": "M01_M02_LITERAL_TRANSPORT_EXACT_NO_CELL_CLOSURE",
        }
        packet["payload_sha256"] = payload_sha(packet)
    elif args.import_only:
        assert verify_base_dependency()
        imported_cell = dict(M00_R11_IMPORT)
        imported_cell["runtime_verification"] = verify_m00_r11_import()
        packet = {
            "schema": "rs-mca-kb-v4-m2-aligned-positive-moving-closure-v1",
            "base_dependency": BASE_DEPENDENCY,
            "imported_cell": imported_cell,
            "terminal": "M00_R11_IMPORT_RUNTIME_VERIFIED",
        }
        packet["payload_sha256"] = payload_sha(packet)
    else:
        packet = build_packet(args.cell) if args.cell else build_sharded_packet()
    if args.emit:
        CERTIFICATE_PATH.parent.mkdir(parents=True, exist_ok=True)
        CERTIFICATE_PATH.write_text(
            json.dumps(
                packet,
                indent=2,
                sort_keys=True,
                default=lambda item: int(item) if item in ZZ else str(item),
            )
            + "\n"
        )
    encoded = canonical_json(packet)
    if args.json:
        print(encoded)
    print(
        "PASS aligned-positive moving closure compiler "
        f"scope={('parity-' + args.parity_only) if args.parity_only else ('denominators' if args.denominator_only else ('transport' if args.transport_only else ('import' if args.import_only else ('all' if args.cell is None else args.cell))))} "
        f"payload_sha256={packet['payload_sha256']}"
    )


if __name__ == "__main__":
    main()
