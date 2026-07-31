#!/usr/bin/env sage
"""Compile the exact F02/F03 deletion in the aligned-positive (1,1,2) atlas.

This compiler is deliberately bounded:

* it imports the pinned 36-cell source compiler only after checking its raw
  SHA-256, git-blob SHA-1, certificate SHA-256, and certificate payload;
* it factors the four F02 q-slice equations before branching;
* it computes exactly nine localized Groebner bases over the deployed prime;
* it enumerates the two surviving zero-dimensional q-slice schemes over
  quadratic extensions and tests the *full* J/I quotient identities there;
* it proves literal b -> b^-1 transport of the complete source data for all
  twelve atlas assignments, and imports only F02 -> F03.

There is no generic saturation, random search, floating-point arithmetic,
Möbius covariance, owner assignment, charge, or K3 row closure.
"""

import argparse
import hashlib
import json
from pathlib import Path


SCHEMA = "kb-mca-v4-m2-aligned-positive-f02-f03-deletion-v1"
PRIME = ZZ(2130706433)
CHALLENGE_EXTENSION_DEGREE = 6
ATLAS_PARENT_COMMIT = "c2edcfa5cbfb8a41e7dea04ae1b34325c90ed5dc"
ATLAS_HEAD_COMMIT = "9e1d96cbf997c30efa448bbce9a7f48c2bea9643"
ATLAS_SOURCE_SHA256 = (
    "c382adee5be3b72dcb675b4932a681f65ae958f58e24c3f5fdb8163d4d1508b7"
)
ATLAS_SOURCE_BLOB_SHA1 = "946308dbc014ce952c0c1cc583cc3d579a61aecf"
ATLAS_CERT_SHA256 = (
    "91b3df40ec8721b2e95ef8170ff58cb0a68a4ef17be0f8c7dbe9f6a0291c8ac4"
)
ATLAS_CERT_BLOB_SHA1 = "017bc1447f6114ae91182560ad0c7ca708919b6b"
ATLAS_CERT_PAYLOAD_SHA256 = (
    "127a4574077d213b188c9e8a9fde93a5a1a4b6121e9f37f84fc01f66c313d990"
)

ROOT = Path(__file__).resolve().parents[1]
ATLAS_SOURCE = (
    ROOT
    / "scripts/compile_kb_mca_v4_m2_aligned_positive_qslice_atlas_v1.sage"
)
ATLAS_CERT = (
    ROOT
    / "data/certificates/kb-mca-v4-m2-aligned-positive-qslice-atlas-v1"
    / "kb_mca_v4_m2_aligned_positive_qslice_atlas_v1.json"
)
CERTIFICATE_PATH = (
    ROOT
    / "data/certificates/"
    "kb-mca-v4-m2-aligned-positive-f02-f03-deletion-v1/"
    "kb_mca_v4_m2_aligned_positive_f02_f03_deletion_v1.json"
)

EXPECTED_RAW_LOCALIZER = {
    "degree": 54,
    "terms": 34112,
    "sha256": "21d38166362e101d6505bdee2edc2373c27c9d6905bb6eb55d845043c133844e",
}
EXPECTED_RADICAL_LOCALIZER = {
    "factor_count": 34,
    "degree": 43,
    "terms": 12312,
    "sha256": "a5a4eb686175c86d5cd6f4a04dba92c9b8063cbbaf37856be6d28d5e1b1b36e1",
}
EXPECTED_RESIDUAL_FACTOR_HASHES = {
    "R02": {
        "c_constant": [
            "6487d12fbfc00b7544e53d11f779ce3a7f1b79c13ade210eac801791fb2d6fec",
            "94431ebab5b5b7bfd716d4e0aa979fac66ed82c8c460fa114e055e5cd97a6382",
        ],
        "d_constant": [
            "732b0dbe4af1f439da74223bb233b495f708fbc8f7248ea6eeaad0b35b497189",
            "31712bb6b3aec9b79ef350922ade01f95f5158ddf9cc332bb3d96c4106263d45",
        ],
    },
    "R11": {
        "c_constant": [
            "1de6e2699de59b642e44d00a81a1f122360b48702193bf78b86c0cb2b9d5a5bf",
        ],
        "d_constant": [
            "38ff5656e2ff6fc3b2788618b501a4bef37e45230064ad0a337574e2443852d2",
        ],
    },
    "R20": {
        "c_constant": [
            "d8d960cecb0c9da47f87606ee1c9e87f97b0f60ce4472a92d0a12d489dc88e3e",
            "716c2b0d3648d895929962d432de5de5c8230ad1d31a6e05317879d3f4d195de",
        ],
        "d_constant": [
            "6c0568b42b56834467a4b476fb38490dc52fea6cd2292f06f9ff76fbd42f9f77",
            "f91f47efcdd9cf39c85923d75550ed09137b9f557a4e9b185ae47cc9d8fa9f85",
        ],
    },
}
EXPECTED_MIDDLE_HASHES = {
    "R11": {
        "c_linear": "ff7657386b2e57385c6df465b2bbd33b5443711c2f88c18e2259b521ed86f00e",
        "d_linear": "1d537ac6ee9c82efe4412cdd1aa8a916867d900003b75f55289c04f3d0946327",
    },
}
EXPECTED_SURVIVOR_REMAINDERS = {
    "R02": {
        940017546: {
            "J": [317112865, 1161791022, 627736383],
            "I": [462252474, 145305698, 1796550960],
        },
    },
    "R20": {
        584912723: {
            "J": [1671616282, 297746731, 555560394],
            "I": [134663927, 1672091025, 1334100861],
        },
        1190675975: {
            "J": [309729886, 1997957961, 2008265187],
            "I": [1042061214, 2038553966, 1196113770],
        },
    },
}


def canonical_json(value):
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        default=lambda item: int(item) if item in ZZ else str(item),
    )


def sha_bytes(value):
    return hashlib.sha256(value).hexdigest()


def sha_text(value):
    return sha_bytes(str(value).encode())


def git_blob_sha1(value):
    header = f"blob {len(value)}\0".encode()
    return hashlib.sha1(header + value).hexdigest()


def payload_sha(data):
    copy = dict(data)
    copy.pop("payload_sha256", None)
    return sha_bytes(canonical_json(copy).encode())


def load_pinned_atlas():
    source_bytes = ATLAS_SOURCE.read_bytes()
    cert_bytes = ATLAS_CERT.read_bytes()
    if sha_bytes(source_bytes) != ATLAS_SOURCE_SHA256:
        raise AssertionError("atlas compiler raw SHA-256 mismatch")
    if git_blob_sha1(source_bytes) != ATLAS_SOURCE_BLOB_SHA1:
        raise AssertionError("atlas compiler git-blob SHA-1 mismatch")
    if sha_bytes(cert_bytes) != ATLAS_CERT_SHA256:
        raise AssertionError("atlas certificate raw SHA-256 mismatch")
    if git_blob_sha1(cert_bytes) != ATLAS_CERT_BLOB_SHA1:
        raise AssertionError("atlas certificate git-blob SHA-1 mismatch")
    atlas_cert = json.loads(cert_bytes)
    if atlas_cert["payload_sha256"] != ATLAS_CERT_PAYLOAD_SHA256:
        raise AssertionError("atlas certificate recorded payload mismatch")
    if payload_sha(atlas_cert) != ATLAS_CERT_PAYLOAD_SHA256:
        raise AssertionError("atlas certificate recomputed payload mismatch")
    if atlas_cert["parent"]["commit"] != ATLAS_PARENT_COMMIT:
        raise AssertionError("atlas parent commit mismatch")

    namespace = dict(globals())
    namespace.update({"__file__": str(ATLAS_SOURCE), "__name__": "atlas_module"})
    source = source_bytes.decode().split('if __name__ == "__main__":')[0]
    exec(compile(source, str(ATLAS_SOURCE), "exec"), namespace)
    return namespace


ATLAS = load_pinned_atlas()
R = ATLAS["R"]
b, c, d, w = R.gens()
K = ATLAS["K"]
KW = ATLAS["KW"]
W = ATLAS["W"]
strip_b_unit = ATLAS["strip_b_unit"]
radical_localizer_factors = ATLAS["radical_localizer_factors"]
build_assignment = ATLAS["build_assignment"]
assignment_geometry = ATLAS["assignment_geometry"]
edge = ATLAS["edge"]
evaluation = ATLAS["evaluation"]
VERTEX_FORMULAS = ATLAS["VERTEX_FORMULAS"]
ASSIGNMENT_EDGES = ATLAS["ASSIGNMENT_EDGES"]
B_INVERSION = ATLAS["B_INVERSION"]


def poly_metric(value):
    return {
        "degree": int(value.total_degree()),
        "terms": int(len(value.monomials())),
        "sha256": sha_text(value),
    }


def canonical_factor(value):
    value = strip_b_unit(value)
    if value.leading_coefficient() < 0:
        value = -value
    return value


def full_label_localizer(atlas_factors):
    """Return the exact localizer used by every F02 branch.

    The first product is the atlas denominator/reconstruction localizer.
    The second and third products are the literal reduced/distinct J labels
    and the moving I/J label differences.  Repeated factors are retained in
    ``raw`` because that is the exact Rabinowitsch generator used below.
    """
    j_units = (
        b, b - 1, b + 1, b - 2, 2*b - 1,
        c, c - 1, c + 1, c - 2, 2*c - 1,
        d, d - 1, d + 1, d - 2, 2*d - 1,
        c - d, c*d - 1,
        c - b, b*c - 1, d - b, b*d - 1,
    )
    moving_units = (
        w, w - 1, w + 1, w - 2, 2*w - 1,
        w - b, b*w - 1,
        w - c, c*w - 1,
        w - d, d*w - 1,
    )
    raw = R(prod(atlas_factors) * prod(j_units) * prod(moving_units))
    distinct = {}
    for value in (*atlas_factors, *j_units, *moving_units):
        for factor, _ in R(value).factor():
            if factor.is_constant():
                continue
            factor = R(factor)
            if factor.leading_coefficient() < 0:
                factor = -factor
            distinct[str(factor)] = factor
    radical_factors = [distinct[key] for key in sorted(distinct)]
    radical = R(prod(radical_factors))
    record = {
        "provenance": [
            "atlas complete-line denominators and reconstruction units",
            "reduced and pairwise-distinct J={2,1/2,b,b^-1,c,d}",
            "moving-label differences for w against J and deck partners",
        ],
        "raw": poly_metric(raw),
        "rabinowitsch": {
            "degree": int(raw.total_degree() + 1),
            "terms": int(len(raw.monomials()) + 1),
            "formula": "tt*H_raw-1",
        },
        "radical": {
            **poly_metric(radical),
            "factor_count": len(radical_factors),
            "factors": [str(value) for value in radical_factors],
            "factor_set_sha256": sha_bytes(
                canonical_json([str(value) for value in radical_factors]).encode()
            ),
        },
    }
    for key, expected in EXPECTED_RAW_LOCALIZER.items():
        if record["raw"][key] != expected:
            raise AssertionError(f"raw localizer {key} mismatch")
    for key, expected in EXPECTED_RADICAL_LOCALIZER.items():
        if record["radical"][key] != expected:
            raise AssertionError(
                f"radical localizer {key} mismatch: "
                f"{record['radical'][key]} != {expected}"
            )
    return raw, radical_factors, record


def residual_factor_records(equation, localizer_keys):
    records = []
    factors = []
    for factor, exponent in R(equation).factor():
        factor = canonical_factor(factor)
        if str(factor) in localizer_keys:
            continue
        records.append(
            {
                "factor": str(factor),
                "exponent": int(exponent),
                "metric": poly_metric(factor),
            }
        )
        factors.extend([factor] * int(exponent))
    return factors, records


FP = GF(PRIME)
P = PolynomialRing(
    FP, names=("tt", "bb", "cc", "dd", "ww"), order="degrevlex"
)
tt, bb, cc, dd, ww = P.gens()
L = PolynomialRing(FP, names=("tt", "bb", "cc", "dd", "ww"), order="lex")
lt, lb, lc, ld, lw = L.gens()


def to_degrevlex(value):
    value = R(value)
    return P(
        sum(
            FP(coefficient.numerator()) / FP(coefficient.denominator())
            * bb**monomial[0]
            * cc**monomial[1]
            * dd**monomial[2]
            * ww**monomial[3]
            for monomial, coefficient in value.dict().items()
        )
    )


def basis_record(basis):
    expressions = [str(value) for value in basis]
    return {
        "size": len(basis),
        "unit": basis == [basis[0].parent()(1)],
        "basis_sha256": sha_bytes(canonical_json(expressions).encode()),
        "basis": [
            {
                "expression": expression,
                "leading_monomial": str(value.lm()),
                "metric": poly_metric(value),
            }
            for expression, value in zip(expressions, basis)
        ],
    }


def source_record(assignment_id):
    """Rebuild the complete rational source U,V,z for one assignment."""
    geometry = assignment_geometry(assignment_id)
    common = VERTEX_FORMULAS[geometry["common_vertex"]]
    right = VERTEX_FORMULAS[geometry["first_other_vertex"]]
    left = VERTEX_FORMULAS[geometry["second_other_vertex"]]
    first = edge(geometry["first_edge"])
    second = edge(geometry["second_edge"])
    bK, cK, dK, wK = map(K, R.gens())

    q0, q1 = cK*dK, -(cK+dK)
    f, g, m = q0-wK, 1-wK*q0, q1*(1-wK)
    v = vector(KW, (f+g*W, m*(1+W), g+f*W))
    v_common = v[0] + common*v[1] + common**2*v[2]
    z = -K(v_common[0])/K(v_common[1])
    v_z = vector(K, (entry(z) for entry in v))
    linear_1 = v_z[2]
    linear_0 = v_z[1] + common*v_z[2]
    target = (
        (linear_0+left*linear_1)*first
        + (linear_0+right*linear_1)*second
    )/(left-right)

    target_0, target_1, target_2 = target
    difference = (target_0-target_2)/(1-z**2)
    rhs_sum = target_0+target_2
    rhs_source = -(
        (1+q0)*(1-wK**2)*difference/(2*(1-q0))
    )
    block_det = (wK-z)*(1-wK*z)
    sum_outer = (rhs_sum*wK-2*z*rhs_source)/block_det
    x1 = ((1+z**2)*rhs_source-(1+wK**2)*rhs_sum/2)/block_det
    x0 = (sum_outer+difference)/2
    x2 = (sum_outer-difference)/2
    at_w_2 = x2+x1*wK+x0*wK**2
    x3 = (target_1*wK-z*q1*at_w_2)/block_det
    x4 = ((1+z**2)*q1*at_w_2-(1+wK**2)*target_1)/block_det
    u = vector(
        KW,
        (
            x0+x1*W+x2*W**2,
            x3*(1+W**2)+x4*W,
            x2+x1*W+x0*W**2,
        ),
    )
    return u, v, K(z)


def pull_b_rational(value):
    value = K(value)
    numerator = K(R(value.numerator())(b=1/b))
    denominator = K(R(value.denominator())(b=1/b))
    return K(numerator/denominator)


def pull_b_kw(value):
    value = KW(value)
    return KW(sum(pull_b_rational(coefficient)*W**index
                  for index, coefficient in enumerate(value)))


def rational_sort_key(value):
    value = K(value)
    return (str(value.numerator()), str(value.denominator()))


def check_multiset(left, right):
    unmatched = list(right)
    for item in left:
        for index, candidate in enumerate(unmatched):
            if item == candidate:
                unmatched.pop(index)
                break
        else:
            return False
    return not unmatched


def literal_inversion_records():
    """Prove complete source transport for every declared atlas pair."""
    sources = {
        assignment_id: source_record(assignment_id)
        for assignment_id in ASSIGNMENT_EDGES
    }
    records = []
    expected_sign = {
        "F00": 1, "F01": 1, "F02": 1, "F03": 1,
        "F04": 1, "F05": 1, "F06": 1, "F07": 1,
        "M00": -1, "M01": 1, "M02": 1, "M03": -1,
    }
    bK, cK, dK, wK = map(K, R.gens())
    for assignment_id in ASSIGNMENT_EDGES:
        partner_id = B_INVERSION[assignment_id]
        source_u, source_v, source_z = sources[assignment_id]
        target_u, target_v, target_z = sources[partner_id]

        pulled_u = vector(KW, (pull_b_kw(value) for value in source_u))
        pulled_v = vector(KW, (pull_b_kw(value) for value in source_v))
        if pulled_u == target_u:
            sign = 1
        elif pulled_u == -target_u:
            sign = -1
        else:
            raise AssertionError(
                f"U transport failed {assignment_id}->{partner_id}"
            )
        if sign != expected_sign[assignment_id]:
            raise AssertionError(f"unexpected U sign on {assignment_id}")
        if pulled_v != target_v:
            raise AssertionError(
                f"V transport failed {assignment_id}->{partner_id}"
            )
        if pull_b_rational(source_z) != target_z:
            raise AssertionError(
                f"z transport failed {assignment_id}->{partner_id}"
            )

        source_j = [K(2), K(1)/2, bK, 1/bK, cK, dK]
        target_j = list(source_j)
        source_i = [1/cK, 1/dK, wK, 1/wK, source_z, 1/source_z]
        target_i = [1/cK, 1/dK, wK, 1/wK, target_z, 1/target_z]
        source_k = [wK, source_z, 1/source_z, 1/cK, 1/dK]
        target_k = [wK, target_z, 1/target_z, 1/cK, 1/dK]
        source_r = [1/wK, *source_j]
        target_r = [1/wK, *target_j]

        multiset_checks = {}
        for name, left, right in (
            ("J", source_j, target_j),
            ("I", source_i, target_i),
            ("K", source_k, target_k),
            ("R", source_r, target_r),
        ):
            pulled = [pull_b_rational(value) for value in left]
            exact = check_multiset(pulled, right)
            if not exact:
                raise AssertionError(
                    f"{name} label transport failed "
                    f"{assignment_id}->{partner_id}"
                )
            multiset_checks[name] = exact

        records.append(
            {
                "source": assignment_id,
                "target": partner_id,
                "U_global_sign": sign,
                "V_exact": True,
                "z_exact": True,
                "q_exact": True,
                "G_equals_U2_minus_WV2_exact": True,
                "label_factor_multisets_exact": multiset_checks,
                "full_J_identity_exact_by_factor_transport": True,
                "full_I_identity_exact_by_factor_transport": True,
            }
        )
    return records


def eval_r_poly(value, field, point):
    images = point
    value = R(value)
    return sum(
        field(coefficient.numerator()) / field(coefficient.denominator())
        * prod(images[index]**monomial[index] for index in range(4))
        for monomial, coefficient in value.dict().items()
    )


def eval_k(value, field, point):
    value = K(value)
    denominator = eval_r_poly(value.denominator(), field, point)
    if not denominator:
        raise AssertionError("zero rational denominator at q-slice point")
    return eval_r_poly(value.numerator(), field, point)/denominator


def eval_l_poly(value, field, point):
    """Evaluate a five-variable deployed-field polynomial."""
    return sum(
        field(coefficient)
        * prod(point[index]**monomial[index] for index in range(5))
        for monomial, coefficient in value.dict().items()
    )


def coordinate_pair(value):
    coefficients = list(value.polynomial())
    coefficients += [value.parent().prime_subfield()(0)]*(2-len(coefficients))
    if len(coefficients) > 2:
        raise AssertionError("point escaped quadratic subfield")
    return [int(coefficients[0]), int(coefficients[1])]


def solve_linear_relation(relation, field, known, variable_index):
    zero = list(known)
    zero[variable_index] = field(0)
    one = list(known)
    one[variable_index] = field(1)
    two = list(known)
    two[variable_index] = field(2)
    constant = eval_l_poly(relation, field, zero)
    coefficient = eval_l_poly(relation, field, one)-constant
    if not coefficient:
        raise AssertionError("triangular lex relation lost linear pivot")
    if eval_l_poly(relation, field, two) != constant+2*coefficient:
        raise AssertionError("purported lex relation is not linear")
    return -constant/coefficient


def univariate_in_variable(relation, field, known, variable_index, name):
    ring = PolynomialRing(field, name)
    variable = ring.gen()
    result = ring(0)
    for monomial, coefficient in relation.dict().items():
        term = field(coefficient)
        for index, exponent in enumerate(monomial):
            if index == variable_index:
                term *= variable**exponent
            else:
                term *= known[index]**exponent
        result += term
    return result


def full_quotient_mismatches(source, field, semantic_point):
    """Return first nonzero J/I projective mismatch coefficients."""
    u, v, z = source
    b0, c0, d0, w0 = semantic_point
    PY = PolynomialRing(field, "Y")
    Y = PY.gen()

    def ev(value):
        return eval_k(value, field, semantic_point)

    u_at = [
        PY(sum(ev(coefficient)*Y**index
               for index, coefficient in enumerate(poly)))
        for poly in u
    ]
    v_at = [
        PY(sum(ev(coefficient)*Y**index
               for index, coefficient in enumerate(poly)))
        for poly in v
    ]
    z0 = ev(z)

    def g_at(label):
        uu = sum(u_at[index]*label**index for index in range(3))
        vv = sum(v_at[index]*label**index for index in range(3))
        return PY(uu**2-Y*vv**2)

    def locator(labels):
        return prod(Y-label for label in labels)

    j_labels = (field(2), field(1)/2, b0, 1/b0, c0, d0)
    i_labels = (1/c0, 1/d0, w0, 1/w0, z0, 1/z0)
    k_labels = (w0, z0, 1/z0, 1/c0, 1/d0)
    r_labels = (1/w0, *j_labels)
    q = (Y-c0)*(Y-d0)
    pairs = {
        "J": (
            prod(g_at(label) for label in j_labels),
            locator(k_labels)**4*q**2,
        ),
        "I": (
            q**2*prod(g_at(label) for label in i_labels),
            locator(r_labels)**4,
        ),
    }
    result = {}
    for identity, (observed, expected) in pairs.items():
        mismatch = (
            observed*expected.leading_coefficient()
            - expected*observed.leading_coefficient()
        )
        nonzero = [
            (index, coefficient)
            for index, coefficient in enumerate(mismatch)
            if coefficient
        ]
        if not nonzero:
            raise AssertionError(
                f"full {identity} quotient identity unexpectedly holds"
            )
        result[identity] = {
            "first_nonzero_coefficient": int(nonzero[0][0]),
            "value": nonzero[0][1],
            "nonzero_coefficient_count": len(nonzero),
        }
    return result


def enumerate_lex_points(target_id, lex_basis, generators, raw_localizer, source):
    """Enumerate the surviving lex scheme component by component over Fp^2."""
    leading = [str(value.lm()) for value in lex_basis]
    if leading[:4] != ["tt", "bb", "cc", "dd^2"]:
        raise AssertionError(f"unexpected triangular lex pivots: {leading}")
    last = lex_basis[-1].univariate_polynomial()
    factorization = list(last.factor())
    if any(int(exponent) != 1 or factor.degree() != 2
           for factor, exponent in factorization):
        raise AssertionError("w eliminant is not squarefree quadratic factors")
    standard_monomial_dimension = 2*sum(
        int(factor.degree()) for factor, _ in factorization
    )
    expected_dimension = 4 if target_id == "R02" else 8
    if standard_monomial_dimension != expected_dimension:
        raise AssertionError("unexpected quotient dimension")

    components = []
    total_points = 0
    for component_index, (factor, _) in enumerate(factorization):
        factor = factor.monic()
        coefficients = [int(value) for value in factor]
        if coefficients != [1, coefficients[1], 1]:
            raise AssertionError("unexpected reciprocal quadratic eliminant")
        middle = coefficients[1]
        extension = GF(
            PRIME**2,
            name=f"a{target_id.lower()}{component_index}",
            modulus=factor,
        )
        omega = extension.gen()
        XX = PolynomialRing(extension, "X")
        split_factor = XX([extension(value) for value in factor])
        w_roots = split_factor.roots(multiplicities=False)
        if len(w_roots) != 2:
            raise AssertionError("quadratic eliminant did not split twice")

        component_points = []
        mismatch_values = {"J": [], "I": []}
        for w0 in w_roots:
            known = [extension(0)]*5
            known[4] = w0
            d_polynomial = univariate_in_variable(
                lex_basis[3], extension, known, 3, "D"
            )
            d_roots = d_polynomial.roots(multiplicities=False)
            if len(d_roots) != 2:
                raise AssertionError("d lex relation did not split twice")
            for d0 in d_roots:
                known[3] = d0
                known[2] = solve_linear_relation(
                    lex_basis[2], extension, known, 2
                )
                known[1] = solve_linear_relation(
                    lex_basis[1], extension, known, 1
                )
                known[0] = solve_linear_relation(
                    lex_basis[0], extension, known, 0
                )
                if any(eval_l_poly(value, extension, known)
                       for value in lex_basis):
                    raise AssertionError("lex point does not annihilate basis")
                if any(eval_l_poly(L(value), extension, known)
                       for value in generators):
                    raise AssertionError("lex point does not annihilate generators")
                semantic = tuple(known[index] for index in (1, 2, 3, 4))
                if not eval_r_poly(raw_localizer, extension, semantic):
                    raise AssertionError("lex point lies off localized chart")
                mismatches = full_quotient_mismatches(
                    source, extension, semantic
                )
                for identity in ("J", "I"):
                    if mismatches[identity]["first_nonzero_coefficient"] != 1:
                        raise AssertionError(
                            f"{identity} mismatch did not occur at coefficient 1"
                        )
                    mismatch_values[identity].append(
                        (w0, mismatches[identity]["value"])
                    )
                z0 = eval_k(source[2], extension, semantic)
                component_points.append(
                    {
                        "b": coordinate_pair(known[1]),
                        "c": coordinate_pair(known[2]),
                        "d": coordinate_pair(known[3]),
                        "w": coordinate_pair(known[4]),
                        "z": coordinate_pair(z0),
                    }
                )

        mismatch_records = {}
        for identity in ("J", "I"):
            values = mismatch_values[identity]
            first_w, first_value = values[0]
            second = next(
                (item for item in values if item[0] != first_w), None
            )
            if second is None:
                raise AssertionError("missing conjugate w root")
            second_w, second_value = second
            slope = (first_value-second_value)/(first_w-second_w)
            intercept = first_value-slope*first_w
            if coordinate_pair(slope)[1] or coordinate_pair(intercept)[1]:
                raise AssertionError("mismatch interpolation left prime field")
            slope_int = coordinate_pair(slope)[0]
            intercept_int = coordinate_pair(intercept)[0]
            if any(value != slope*w_value+intercept
                   for w_value, value in values):
                raise AssertionError("mismatch is not uniform linear in w")
            norm = int((extension(slope)*omega+extension(intercept)).norm())
            expected = EXPECTED_SURVIVOR_REMAINDERS[target_id][middle][identity]
            if [slope_int, intercept_int, norm] != expected:
                raise AssertionError(
                    f"{target_id} {middle} {identity} remainder mismatch"
                )
            if norm == 0:
                raise AssertionError("full quotient mismatch norm vanished")
            mismatch_records[identity] = {
                "coefficient_index": 1,
                "remainder_mod_w_factor": {
                    "w_coefficient": slope_int,
                    "constant": intercept_int,
                },
                "norm_to_prime_field": norm,
                "nonzero": True,
                "uniform_over_d_roots_and_w_conjugates": True,
            }

        components.append(
            {
                "component_index": component_index,
                "w_minimal_polynomial_coefficients": coefficients,
                "w_minimal_polynomial_middle": middle,
                "irreducible_degree": 2,
                "point_count": len(component_points),
                "points": component_points,
                "full_quotient_mismatches": mismatch_records,
            }
        )
        total_points += len(component_points)
    if total_points != expected_dimension:
        raise AssertionError("point count differs from quotient dimension")
    return {
        "standard_monomial_dimension": standard_monomial_dimension,
        "point_count_over_Fp2": total_points,
        "all_points_lie_in_Fp2_subfield_of_Fp6": True,
        "components": components,
        "full_J_identity_false_at_every_point": True,
        "full_I_identity_false_at_every_point": True,
    }


def compile_f02_cells():
    _, _, systems = build_assignment("F02")
    atlas_localizers = radical_localizer_factors(
        systems["R02"]["localizer_factors"]
    )
    raw_localizer, radical_factors, localizer_record = full_label_localizer(
        atlas_localizers
    )
    localizer_keys = {str(canonical_factor(value))
                      for value in radical_factors}
    source = source_record("F02")
    cells = []
    expected_unit_pattern = {
        "R02": {(0, 0): False, (0, 1): True, (1, 0): True, (1, 1): True},
        "R11": {(0, 0): True},
        "R20": {(0, 0): False, (0, 1): True, (1, 0): True, (1, 1): True},
    }

    for target_id in ("R02", "R11", "R20"):
        system = systems[target_id]
        equations = system["equations"]
        c_factors, c_records = residual_factor_records(
            equations[0], localizer_keys
        )
        d_factors, d_records = residual_factor_records(
            equations[2], localizer_keys
        )
        middle_c_factors, middle_c_records = residual_factor_records(
            equations[1], localizer_keys
        )
        middle_d_factors, middle_d_records = residual_factor_records(
            equations[3], localizer_keys
        )
        factor_hashes = {
            "c_constant": [
                record["metric"]["sha256"] for record in c_records
            ],
            "d_constant": [
                record["metric"]["sha256"] for record in d_records
            ],
        }
        if factor_hashes != EXPECTED_RESIDUAL_FACTOR_HASHES[target_id]:
            raise AssertionError(f"{target_id} residual factor order mismatch")
        if target_id == "R11":
            middle_hashes = {
                "c_linear": sha_text(prod(middle_c_factors)),
                "d_linear": sha_text(prod(middle_d_factors)),
            }
            if middle_hashes != EXPECTED_MIDDLE_HASHES[target_id]:
                raise AssertionError("R11 middle factor mismatch")

        middle_c = R(prod(middle_c_factors))
        middle_d = R(prod(middle_d_factors))
        branches = []
        survivor = None
        for c_index, c_factor in enumerate(c_factors):
            for d_index, d_factor in enumerate(d_factors):
                generators = [
                    to_degrevlex(c_factor),
                    to_degrevlex(d_factor),
                    to_degrevlex(middle_c),
                    to_degrevlex(middle_d),
                    tt*to_degrevlex(raw_localizer)-1,
                ]
                basis = list(P.ideal(generators).groebner_basis())
                unit = len(basis) == 1 and basis[0] == P(1)
                if unit != expected_unit_pattern[target_id][
                    (c_index, d_index)
                ]:
                    raise AssertionError(
                        f"{target_id} branch {(c_index, d_index)} "
                        "unit classification mismatch"
                    )
                branch = {
                    "branch": [c_index, d_index],
                    "selected_factor_sha256": {
                        "c_constant": sha_text(c_factor),
                        "d_constant": sha_text(d_factor),
                    },
                    "generator_metrics": [poly_metric(value)
                                          for value in generators],
                    "localized_groebner": basis_record(basis),
                    "classification": (
                        "EMPTY_LOCALIZED_UNIT_IDEAL"
                        if unit else "ZERO_DIMENSIONAL_QSLICE_SURVIVOR"
                    ),
                }
                branches.append(branch)
                if not unit:
                    if survivor is not None:
                        raise AssertionError(
                            f"multiple q-slice survivors in {target_id}"
                        )
                    lex_basis = list(
                        L.ideal([L(value) for value in basis]).groebner_basis()
                    )
                    lex_record = basis_record(lex_basis)
                    point_record = enumerate_lex_points(
                        target_id,
                        lex_basis,
                        generators,
                        raw_localizer,
                        source,
                    )
                    survivor = {
                        "branch": [c_index, d_index],
                        "lex_groebner": lex_record,
                        "point_census": point_record,
                        "classification": (
                            "EMPTY_AFTER_FULL_QUOTIENT_IDENTITIES"
                        ),
                    }

        if target_id == "R11":
            if survivor is not None:
                raise AssertionError("R11 unexpectedly has a survivor")
            conclusion = "EMPTY_LOCALIZED_QSLICE"
            proof_mode = "DIRECT_UNIT_IDEAL"
        else:
            if survivor is None:
                raise AssertionError(f"{target_id} survivor missing")
            conclusion = "EMPTY_FULL_SOURCE"
            proof_mode = "FULL_J_AND_I_QUOTIENT_MISMATCH_ON_EXACT_POINT_CENSUS"
        cells.append(
            {
                "cell_id": f"F02-{target_id}",
                "factor_first": {
                    "equation_order": [
                        "c_constant", "c_linear",
                        "d_constant", "d_linear",
                    ],
                    "c_constant": c_records,
                    "c_linear": middle_c_records,
                    "d_constant": d_records,
                    "d_linear": middle_d_records,
                    "dropped_factors": (
                        "only exact factors of the declared 34-factor localizer"
                    ),
                },
                "branch_exhaustivity": {
                    "c_factor_count": len(c_factors),
                    "d_factor_count": len(d_factors),
                    "cartesian_branch_count": len(branches),
                    "all_cartesian_branches_present_once": True,
                },
                "branches": branches,
                "survivor": survivor,
                "conclusion": conclusion,
                "proof_mode": proof_mode,
                "ledger_movement": 0,
            }
        )
    return localizer_record, cells


def expected_certificate():
    localizer, cells = compile_f02_cells()
    inversion = literal_inversion_records()
    data = {
        "schema": SCHEMA,
        "source_pins": {
            "atlas_parent_commit": ATLAS_PARENT_COMMIT,
            "atlas_head_commit": ATLAS_HEAD_COMMIT,
            "atlas_compiler": {
                "relative_path": str(ATLAS_SOURCE.relative_to(ROOT.parent)),
                "sha256": ATLAS_SOURCE_SHA256,
                "git_blob_sha1": ATLAS_SOURCE_BLOB_SHA1,
            },
            "atlas_certificate": {
                "relative_path": str(ATLAS_CERT.relative_to(ROOT.parent)),
                "sha256": ATLAS_CERT_SHA256,
                "git_blob_sha1": ATLAS_CERT_BLOB_SHA1,
                "payload_sha256": ATLAS_CERT_PAYLOAD_SHA256,
            },
        },
        "field": {
            "prime": int(PRIME),
            "challenge_extension_degree": CHALLENGE_EXTENSION_DEGREE,
            "symbolic_source_field": "QQ(b,c,d,w)",
            "q_slice_field": f"GF({int(PRIME)})",
            "survivor_field": f"GF({int(PRIME)}^2) subset GF({int(PRIME)}^6)",
        },
        "scope": {
            "direct_assignment": "F02",
            "transported_assignment": "F03",
            "targets": ["R02", "R11", "R20"],
            "direct_cells_deleted": 3,
            "transported_cells_deleted": 3,
            "ledger_movement": 0,
        },
        "localizer": localizer,
        "cells": cells,
        "literal_b_inversion": {
            "map": B_INVERSION,
            "records": inversion,
            "proved_for_all_twelve_assignments": True,
            "imported_conclusion": "F02_EMPTY_IMPLIES_F03_EMPTY",
            "other_conclusions_imported": [],
            "method": (
                "literal coefficientwise b->b^-1 source transport; "
                "not Mobius covariance"
            ),
        },
        "conclusions": {
            "F02-R02": "EMPTY",
            "F02-R11": "EMPTY",
            "F02-R20": "EMPTY",
            "F03-R02": "EMPTY_BY_LITERAL_INVERSION",
            "F03-R11": "EMPTY_BY_LITERAL_INVERSION",
            "F03-R20": "EMPTY_BY_LITERAL_INVERSION",
        },
        "open_cells": [
            "F00-R02", "F00-R11", "F00-R20",
            "F01-R02", "F01-R11", "F01-R20",
            "F04-R02", "F04-R11", "F04-R20",
            "F05-R02", "F05-R11", "F05-R20",
            "F06-R02", "F06-R11", "F06-R20",
            "F07-R02", "F07-R11", "F07-R20",
            "M00-R02", "M00-R11", "M00-R20",
            "M01-R02", "M01-R11", "M01-R20",
            "M02-R02", "M02-R11", "M02-R20",
            "M03-R02", "M03-R11", "M03-R20",
        ],
        "evidence_level": {
            "F02_F03_local_lemma": "PROVED_EXACT_GREEN",
            "K3_row": "OPEN",
            "global_ledger": "UNCHANGED",
        },
        "nonclaims": [
            "no F00/F01 conclusion is imported from external PR pins",
            "no F04-F07 or moving-moving assignment is deleted",
            "no generic saturation",
            "no Mobius covariance",
            "no owner or charge",
            "no K3 or KoalaBear row closure",
        ],
    }
    if len(cells) != 3:
        raise AssertionError("F02 target coverage mismatch")
    if len(inversion) != 12:
        raise AssertionError("literal inversion coverage mismatch")
    data["payload_sha256"] = payload_sha(data)
    return data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not (args.emit or args.check):
        parser.error("choose --emit or --check")
    expected = expected_certificate()
    if args.emit:
        CERTIFICATE_PATH.parent.mkdir(parents=True, exist_ok=True)
        CERTIFICATE_PATH.write_text(
            json.dumps(
                expected,
                indent=2,
                default=lambda item: int(item) if item in ZZ else str(item),
            )
            + "\n"
        )
        print(f"WROTE {CERTIFICATE_PATH}")
    if args.check:
        observed = json.loads(CERTIFICATE_PATH.read_text())
        if observed != expected:
            raise AssertionError("certificate differs from exact recompilation")
        if observed["payload_sha256"] != payload_sha(observed):
            raise AssertionError("certificate payload mismatch")
        print(
            "PASS: F02/F03 aligned-positive deletion "
            f"direct={len(observed['cells'])} "
            f"transported=3 payload={observed['payload_sha256']}"
        )


if __name__ == "__main__":
    main()
