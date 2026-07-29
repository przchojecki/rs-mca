#!/usr/bin/env sage
"""Exact finite-field controls for the degree-60 source-pencil compiler.

This is an independent replay, not a proof of exhaustion or of any
same-record carrier/data/slope bridge.  It verifies:

* deterministic coefficient-matrix dimensions and ranks;
* split source and active fibres in explicit deployed-field controls;
* active-form membership in the relevant symmetric power of the pencil;
* explicit recursive right-component identities; and
* the absence of a nontrivial degree factorization for the prime inner
  degrees 2 and 3.

The degree-ten control is first built in the old ``z`` coordinate and then
conjugated by ``z=(t+1)/t``.  This keeps all twelve points of the inherited
source locator finite: the exceptional old points ``{0,infinity}`` become
``{-1,0}``, and none of the seven selected fibres contains ``z=1``.
"""

import hashlib
import json
from pathlib import Path


class DuplicateJSONKey(ValueError):
    pass


def reject_duplicate_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateJSONKey("duplicate JSON key: " + key)
        result[key] = value
    return result


def canonical_json(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def unhashed_digest(value):
    unhashed = dict(value)
    unhashed.pop("payload_sha256", None)
    return hashlib.sha256(canonical_json(unhashed).encode()).hexdigest()


EXPERIMENTAL = Path(__file__).resolve().parents[1]
REPO_ROOT = EXPERIMENTAL.parent
CERTIFICATE = (
    EXPERIMENTAL
    / "data"
    / "certificates"
    / "kb-mca-v4-degree60-source-pencil-rank-compiler-v1"
    / "kb_mca_v4_degree60_source_pencil_rank_compiler_v1.json"
)

certificate_data = json.loads(
    CERTIFICATE.read_text(encoding="utf-8"),
    object_pairs_hook=reject_duplicate_pairs,
)
assert certificate_data["payload_sha256"] == unhashed_digest(
    certificate_data
)
try:
    json.loads(
        '{"duplicated":1,"duplicated":2}',
        object_pairs_hook=reject_duplicate_pairs,
    )
except DuplicateJSONKey:
    pass
else:
    raise AssertionError("duplicate JSON key accepted")

wolfram_binding = certificate_data["independent_replays"]["wolfram"]
wolfram_replay = REPO_ROOT / wolfram_binding["path"]
assert hashlib.sha256(wolfram_replay.read_bytes()).hexdigest() == (
    wolfram_binding["sha256"]
)


P = Integer(2130706433)
Fp = GF(P)
Ru = PolynomialRing(Fp, "uu")
uu = Ru.gen()
assert (uu^2 + uu + 1).is_irreducible()
K = GF(P^2, "omega", modulus=uu^2 + uu + 1)
omega = K.gen()
Q = K.cardinality()
IOTA = Fp(16711679)
assert IOTA^2 == -Fp.one()

# Sage/Singular's multivariate finite-field backend is not valid for this
# characteristic (>2^29).  The generic polynomial-dictionary backend keeps
# all arithmetic in the exact Sage finite field.
R = PolynomialRing(K, names=("Z", "W"), implementation="generic")
Z, W = R.gens()
RK = PolynomialRing(K, "t")
t = RK.gen()

ENDPOINT_DEGREE = Integer(60)
PROFILE_ROWS = {
    2: (30, 6, 0, 10395),
    3: (20, 4, 0, 15400),
    4: (15, 3, 0, 5775),
    6: (10, 2, 0, 462),
    10: (6, 1, 1, 66),
    12: (5, 1, 0, 1),
}


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def coeff_column(form, degree):
    """Coefficients in affine degrees 0,...,degree as one column."""

    form = R(form)
    require(form.is_homogeneous(), "coefficient input is not homogeneous")
    require(form.total_degree() == degree, "coefficient degree mismatch")
    return vector(
        K,
        [
            form.monomial_coefficient(Z^i * W^(degree - i))
            for i in range(degree + 1)
        ],
    )


def coefficient_matrix(forms, degree):
    """Put degree-``degree`` forms in columns, as used by the compiler."""

    return matrix(
        K, [coeff_column(form, degree) for form in forms]
    ).transpose()


def normalize_form(form):
    """Normalize a nonzero homogeneous form by its first nonzero coefficient."""

    degree = form.total_degree()
    column = coeff_column(form, degree)
    pivot = next(value for value in column if value != 0)
    return R(form / pivot)


def split_locator(roots):
    locator = R.one()
    for root in roots:
        locator *= Z - K(root) * W
    return R(locator)


def binary_substitute(form, first_image, second_image):
    """Evaluate a binary form by an explicit simultaneous monomial sum."""

    result = R.zero()
    for (first_exponent, second_exponent), coefficient in form.dict().items():
        result += (
            coefficient
            * first_image^first_exponent
            * second_image^second_exponent
        )
    return R(result)


def homogenize_univariate(polynomial, degree):
    """Homogenize a univariate polynomial to the declared total degree."""

    polynomial = RK(polynomial)
    require(polynomial.degree() <= degree, "homogenization degree")
    return R(sum(
        polynomial[index] * Z^index * W^(degree - index)
        for index in range(polynomial.degree() + 1)
    ))


def fibre_roots_from_representative(
    representative, inner_degree, root_of_unity
):
    require(K(root_of_unity).multiplicative_order() == inner_degree,
            "wrong root-of-unity order")
    roots = [
        K(representative) * K(root_of_unity)^index
        for index in range(inner_degree)
    ]
    require(len(set(roots)) == inner_degree, "power fibre not reduced")
    return roots


def active_membership(H0, H1, outer_degree, active_values, active_form):
    """Return the symmetric-power and augmented coefficient matrices."""

    sym_forms = [
        H0^(outer_degree - index) * H1^index
        for index in range(outer_degree + 1)
    ]
    sym_matrix = coefficient_matrix(sym_forms, ENDPOINT_DEGREE)
    augmented = coefficient_matrix(
        sym_forms + [active_form], ENDPOINT_DEGREE
    )
    require(
        sym_matrix.dimensions() == (61, outer_degree + 1),
        "symmetric-power matrix dimensions",
    )
    require(sym_matrix.rank() == outer_degree + 1,
            "symmetric-power columns are not independent")
    require(augmented.rank() == sym_matrix.rank(),
            "active form is outside the symmetric power")

    expected = R.one()
    for value in active_values:
        expected *= H0 - value * H1
    require(normalize_form(active_form) == normalize_form(expected),
            "active product identity")
    return sym_matrix, augmented


def verify_power_control(
    inner_degree, root_of_unity, source_representatives,
    active_representatives
):
    """Verify the ``h=z^m`` control over the deployed quadratic field."""

    outer_degree, order_five_poles, simple_poles, _ = PROFILE_ROWS[
        inner_degree
    ]
    require(simple_poles == 0, "power control expects no exceptional block")
    require(len(source_representatives) == order_five_poles,
            "wrong source target count")
    require(len(active_representatives) == outer_degree,
            "wrong active target count")

    H0 = Z^inner_degree
    H1 = W^inner_degree
    source_representatives = [
        K(value) for value in source_representatives
    ]
    active_representatives = [
        K(value) for value in active_representatives
    ]
    source_values = [value^inner_degree for value in source_representatives]
    active_values = [value^inner_degree for value in active_representatives]
    require(
        len(set(source_values + active_values))
        == len(source_values) + len(active_values),
        "power target values collide",
    )

    source_blocks = []
    source_forms = []
    for representative, value in zip(source_representatives, source_values):
        roots = fibre_roots_from_representative(
            representative, inner_degree, root_of_unity
        )
        require(all(root^inner_degree == value for root in roots),
                "power source fibre equation")
        form = H0 - value * H1
        require(normalize_form(split_locator(roots)) == normalize_form(form),
                "power source split locator")
        source_blocks.append(roots)
        source_forms.append(form)

    active_blocks = []
    active_forms = []
    for representative, value in zip(active_representatives, active_values):
        roots = fibre_roots_from_representative(
            representative, inner_degree, root_of_unity
        )
        require(all(root^inner_degree == value for root in roots),
                "power active fibre equation")
        form = H0 - value * H1
        require(normalize_form(split_locator(roots)) == normalize_form(form),
                "power active split locator")
        active_blocks.append(roots)
        active_forms.append(form)

    source_points = [root for block in source_blocks for root in block]
    active_points = [root for block in active_blocks for root in block]
    require(len(source_points) == 12, "power source point count")
    require(len(set(source_points)) == 12, "power source points repeat")
    require(len(active_points) == 60, "power active point count")
    require(len(set(active_points)) == 60, "power active points repeat")
    require(set(source_points).isdisjoint(active_points),
            "power source/active overlap")

    source_matrix = coefficient_matrix(source_forms, inner_degree)
    require(
        source_matrix.dimensions()
        == (inner_degree + 1, order_five_poles),
        "power source matrix dimensions",
    )

    active_form = prod(active_forms, R.one())
    active_affine = RK(active_form(Z=t, W=K.one()))
    require(active_affine.degree() == 60, "power active degree")
    require(gcd(active_affine, active_affine.derivative()) == 1,
            "power active form is not squarefree")

    if inner_degree == 12:
        # The single forced source form has rank one.  Recover the canonical
        # second column exactly as in the source-fibre adapter.
        require(source_matrix.rank() == 1, "m12 raw source rank")
        source_value = source_values[0]
        residue = prod(
            [source_value - value for value in active_values], K.one()
        )
        inverse_five = inverse_mod(5, Q - 1)
        fifth_root = residue^inverse_five
        require(fifth_root^5 == residue, "m12 fifth-root recovery")
        N0 = fifth_root * H1
        canonical_source_matrix = coefficient_matrix(
            [source_forms[0], N0], inner_degree
        )
        require(canonical_source_matrix.dimensions() == (13, 2),
                "m12 canonical source dimensions")
        require(canonical_source_matrix.rank() == 2,
                "m12 canonical source rank")

        A_affine = RK(source_forms[0](Z=t, W=K.one()))
        N0_affine = RK(N0(Z=t, W=K.one()))
        require((N0_affine^5 - active_affine) % A_affine == 0,
                "m12 residue congruence")
        canonical_active_values = [
            (value - source_value) / fifth_root
            for value in active_values
        ]
        full_sym_matrix, full_augmented = active_membership(
            source_forms[0], N0, outer_degree,
            canonical_active_values, active_form
        )

        quotient, remainder = (active_affine - N0_affine^5).quo_rem(
            A_affine
        )
        require(remainder == 0, "m12 reduced quotient divisibility")
        require(quotient.degree() <= 48, "m12 reduced quotient degree")
        quotient_form = homogenize_univariate(quotient, 48)
        reduced_basis = [
            source_forms[0]^(4 - index) * N0^index
            for index in range(5)
        ]
        sym_matrix = coefficient_matrix(reduced_basis, 48)
        augmented = coefficient_matrix(
            reduced_basis + [quotient_form], 48
        )
        require(sym_matrix.dimensions() == (49, 5),
                "m12 reduced matrix dimensions")
        require(sym_matrix.rank() == 5, "m12 reduced matrix rank")
        require(augmented.dimensions() == (49, 6),
                "m12 reduced augmented dimensions")
        require(augmented.rank() == 5,
                "m12 reduced active membership")

        source_rank = source_matrix.rank()
        source_column_dimensions = source_matrix.dimensions()
        source_display_dimensions = (
            source_column_dimensions[1], source_column_dimensions[0]
        )
        canonical_source_dimensions = canonical_source_matrix.dimensions()
        canonical_source_rank = canonical_source_matrix.rank()
        full_symmetric_dimensions = full_sym_matrix.dimensions()
        full_symmetric_rank = full_sym_matrix.rank()
        full_augmented_dimensions = full_augmented.dimensions()
        full_augmented_rank = full_augmented.rank()
    else:
        require(source_matrix.rank() == 2, "power source rank")
        sym_matrix, augmented = active_membership(
            H0, H1, outer_degree, active_values, active_form
        )
        source_rank = source_matrix.rank()
        source_column_dimensions = source_matrix.dimensions()
        source_display_dimensions = (
            source_column_dimensions[1], source_column_dimensions[0]
        )
        canonical_source_dimensions = source_column_dimensions
        canonical_source_rank = source_rank
        full_symmetric_dimensions = sym_matrix.dimensions()
        full_symmetric_rank = sym_matrix.rank()
        full_augmented_dimensions = augmented.dimensions()
        full_augmented_rank = augmented.rank()

    proper_routes = [
        divisor
        for divisor in divisors(inner_degree)
        if 1 < divisor < inner_degree
    ]
    for right_degree in proper_routes:
        outer_right_degree = inner_degree // right_degree
        require(
            (Z^right_degree)^outer_right_degree == H0
            and (W^right_degree)^outer_right_degree == H1,
            "power recursive route identity",
        )

    return {
        "inner_degree": inner_degree,
        "outer_degree": outer_degree,
        "source_column_dimensions": source_column_dimensions,
        "source_display_dimensions": source_display_dimensions,
        "source_rank": source_rank,
        "canonical_source_dimensions": canonical_source_dimensions,
        "canonical_source_rank": canonical_source_rank,
        "symmetric_dimensions": sym_matrix.dimensions(),
        "symmetric_rank": sym_matrix.rank(),
        "augmented_dimensions": augmented.dimensions(),
        "augmented_rank": augmented.rank(),
        "full_symmetric_dimensions": full_symmetric_dimensions,
        "full_symmetric_rank": full_symmetric_rank,
        "full_augmented_dimensions": full_augmented_dimensions,
        "full_augmented_rank": full_augmented_rank,
        "source_points": len(source_points),
        "active_points": len(active_points),
        "recursive_right_degrees": proper_routes,
    }


M10_Y_ROOT_DATA = {
    243: {
        "x": [
            441863510, 709682263, 710497174, 796172940, 1603196979,
        ],
        "z": [
            74267057, 635415206, 824563947, 1188339233, 1311122138,
            1530081469, 1604873909, 1738540140, 1748005996, 2129029503,
        ],
    },
    3459: {
        "x": [
            85973857, 872107610, 1750292172, 1822723048, 1861022612,
        ],
        "z": [
            524247488, 669066773, 704716532, 738015176, 962409336,
            1012276996, 1153656275, 1336775124, 1511963758, 2040404707,
        ],
    },
    3574: {
        "x": [
            292496322, 598963494, 682863060, 937365616, 1749724374,
        ],
        "z": [
            714150458, 1005685328, 1258341041, 1471328886, 1514082436,
            1553989613, 1709052297, 1807884165, 1825444399, 2054986408,
        ],
    },
    8607: {
        "x": [
            301169065, 393923145, 587925168, 1160295361, 1818100127,
        ],
        "z": [
            168034917, 419890251, 448555045, 534454304, 711740316,
            1066041149, 1202773742, 1229101756, 1283645823, 1458588429,
        ],
    },
    19677: {
        "x": [
            133423276, 197786794, 426255696, 1635032333, 1868914767,
        ],
        "z": [
            10557685, 122865591, 223329671, 358247568, 574517956,
            1192307416, 1364654713, 1411702662, 1510667199, 1753975271,
        ],
    },
    30437: {
        "x": [
            114235151, 491570846, 570012245, 1308462057, 1777132567,
        ],
        "z": [
            215919938, 315566246, 407523600, 583041545, 725871186,
            992895811, 1561212629, 1837417984, 1974847492, 2039235734,
        ],
    },
    43384: {
        "x": [
            1052806569, 1180717393, 1312828491, 1366977764, 1478789082,
        ],
        "z": [
            133148234, 280420086, 668377073, 772386483, 810412009,
            1047569159, 1324342231, 1567326038, 1930358159, 2119192693,
        ],
    },
}


def verify_degree_ten_control():
    """Verify the split finite-coordinate degree-ten control over F_p."""

    inner_degree = Integer(10)
    outer_degree, order_five_poles, simple_poles, _ = PROFILE_ROWS[10]
    require((outer_degree, order_five_poles, simple_poles) == (6, 1, 1),
            "m10 profile")

    # Old z-coordinate forms for h=(x^5+x^2+x)o(z+2/z).
    old_numerator = (
        (Z^2 + 2 * W^2)^5
        + (Z^2 + 2 * W^2)^2 * (Z * W)^3
        + (Z^2 + 2 * W^2) * (Z * W)^4
    )
    old_denominator = (Z * W)^5

    # Substitute (Z,W)=(T+S,T), using the same symbols (Z,W) for (T,S).
    H0 = binary_substitute(old_numerator, Z + W, Z)
    H1 = binary_substitute(old_denominator, Z + W, Z)
    right_numerator = (Z + W)^2 + 2 * Z^2
    right_denominator = Z * (Z + W)
    require(
        H0
        == right_numerator^5
        + right_numerator^2 * right_denominator^3
        + right_numerator * right_denominator^4,
        "m10 conjugated numerator/composition identity",
    )
    require(H1 == right_denominator^5,
            "m10 conjugated denominator/composition identity")
    require(H0.total_degree() == 10 and H1.total_degree() == 10,
            "m10 homogeneous degrees")
    require(gcd(H0, H1) == 1, "m10 coprime pencil")
    require(H0(Z=K.one(), W=K.zero()) == 255 * H1(
        Z=K.one(), W=K.zero()
    ), "m10 conjugated infinity value")
    require(255 not in M10_Y_ROOT_DATA, "m10 selected y=255")

    transformed_by_y = {}
    all_old_roots = []
    all_transformed_roots = []
    for y_integer, data in M10_Y_ROOT_DATA.items():
        y = Fp(y_integer)
        require(
            H0(Z=K.one(), W=K.zero())
            - K(y) * H1(Z=K.one(), W=K.zero()) != 0,
            "m10 selected fibre meets infinity",
        )
        x_roots = [Fp(value) for value in data["x"]]
        old_roots = [Fp(value) for value in data["z"]]
        require(len(x_roots) == 5 and len(set(x_roots)) == 5,
                "m10 x-root count")
        require(len(old_roots) == 10 and len(set(old_roots)) == 10,
                "m10 z-root count")
        require(all(x^5 + x^2 + x == y for x in x_roots),
                "m10 outer quintic fibre")
        require(all(root != 0 and root != 1 for root in old_roots),
                "m10 old root hits conjugation pole")
        recovered_x = [root + Fp(2) / root for root in old_roots]
        require(set(recovered_x) == set(x_roots),
                "m10 quadratic-fibre root data")
        require(all(recovered_x.count(x) == 2 for x in x_roots),
                "m10 quadratic fibres are not pairs")
        require(
            all(root^2 - x * root + 2 == 0
                for x in x_roots for root in old_roots
                if root + Fp(2) / root == x),
            "m10 quadratic identity",
        )

        transformed = [Fp.one() / (root - 1) for root in old_roots]
        require(len(set(transformed)) == 10,
                "m10 transformed fibre repeats")
        require(
            all(
                Fp(H0(Z=K(root), W=K.one()))
                - y * Fp(H1(Z=K(root), W=K.one()))
                == 0
                for root in transformed
            ),
            "m10 transformed fibre equation",
        )
        fibre_form = H0 - K(y) * H1
        require(
            normalize_form(split_locator([K(root) for root in transformed]))
            == normalize_form(fibre_form),
            "m10 transformed split locator",
        )
        transformed_by_y[y_integer] = [K(root) for root in transformed]
        all_old_roots.extend(old_roots)
        all_transformed_roots.extend(transformed)

    require(len(set(all_old_roots)) == 70, "m10 old fibres collide")
    require(len(set(all_transformed_roots)) == 70,
            "m10 transformed fibres collide")

    source_y = 243
    active_ys = [3459, 3574, 8607, 19677, 30437, 43384]
    exceptional_points = [K.zero(), -K.one()]
    source_complete = transformed_by_y[source_y]
    source_points = source_complete + exceptional_points
    active_points = [
        root for y in active_ys for root in transformed_by_y[y]
    ]
    require(len(source_points) == 12 and len(set(source_points)) == 12,
            "m10 finite source split")
    require(len(active_points) == 60 and len(set(active_points)) == 60,
            "m10 active split")
    require(set(source_points).isdisjoint(active_points),
            "m10 source/active overlap")

    complete_source_form = H0 - K(source_y) * H1
    exceptional_locator = Z * (Z + W)
    require(H1 == exceptional_locator^5,
            "m10 exceptional fifth-power form")
    source_forms = [complete_source_form, exceptional_locator^5]
    source_matrix = coefficient_matrix(source_forms, inner_degree)
    require(source_matrix.dimensions() == (11, 2),
            "m10 source matrix dimensions")
    require(source_matrix.rank() == 2, "m10 source matrix rank")

    source_locator = split_locator(source_points)
    require(
        normalize_form(source_locator)
        == normalize_form(complete_source_form * exceptional_locator),
        "m10 inherited finite source locator",
    )
    require(
        normalize_form(source_locator^5)
        == normalize_form(complete_source_form^5 * H1),
        "m10 pole divisor identity",
    )

    active_values = [K(value) for value in active_ys]
    active_forms = [H0 - value * H1 for value in active_values]
    active_form = prod(active_forms, R.one())
    require(
        normalize_form(active_form)
        == normalize_form(split_locator(active_points)),
        "m10 active split product",
    )
    active_affine = RK(active_form(Z=t, W=K.one()))
    require(active_affine.degree() == 60, "m10 active degree")
    require(gcd(active_affine, active_affine.derivative()) == 1,
            "m10 active form is not squarefree")
    sym_matrix, augmented = active_membership(
        H0, H1, outer_degree, active_values, active_form
    )

    # The conjugated map factors through the displayed degree-two right
    # component.  This is an exact recursive route, not a carrier owner.
    require(right_numerator.total_degree() == 2,
            "m10 right numerator degree")
    require(right_denominator.total_degree() == 2,
            "m10 right denominator degree")
    require(gcd(right_numerator, right_denominator) == 1,
            "m10 right component coprimality")

    return {
        "inner_degree": 10,
        "outer_degree": 6,
        "source_column_dimensions": source_matrix.dimensions(),
        "source_display_dimensions": (2, 11),
        "source_rank": source_matrix.rank(),
        "canonical_source_dimensions": source_matrix.dimensions(),
        "canonical_source_rank": source_matrix.rank(),
        "symmetric_dimensions": sym_matrix.dimensions(),
        "symmetric_rank": sym_matrix.rank(),
        "augmented_dimensions": augmented.dimensions(),
        "augmented_rank": augmented.rank(),
        "full_symmetric_dimensions": sym_matrix.dimensions(),
        "full_symmetric_rank": sym_matrix.rank(),
        "full_augmented_dimensions": augmented.dimensions(),
        "full_augmented_rank": augmented.rank(),
        "source_points": len(source_points),
        "active_points": len(active_points),
        "recursive_right_degrees": [2],
        "source_y": source_y,
        "active_ys": active_ys,
        "exceptional_points": [0, -1],
    }


require(P.is_prime(), "deployed characteristic is not prime")
require(K.characteristic() == P and K.cardinality() == P^2,
        "deployed quadratic field")
require((Q - 1) % lcm([2, 3, 4, 6, 12]) == 0,
        "power-control roots of unity")
require(gcd(5, Q - 1) == 1, "deployed quadratic fifth-power gate")

# These are the exact roots of unity and small-integer representatives
# declared by the certificate.
ROOTS_OF_UNITY = {
    2: -K.one(),
    3: omega,
    4: K(IOTA),
    6: -omega,
    12: K(IOTA) * omega,
}
for degree, root in ROOTS_OF_UNITY.items():
    require(root.multiplicative_order() == degree,
            "declared root-of-unity order")

power_controls = {
    2: verify_power_control(
        2, ROOTS_OF_UNITY[2], list(range(1, 7)), list(range(7, 37))
    ),
    3: verify_power_control(
        3, ROOTS_OF_UNITY[3], list(range(1, 5)), list(range(5, 25))
    ),
    4: verify_power_control(
        4, ROOTS_OF_UNITY[4], list(range(1, 4)), list(range(4, 19))
    ),
    6: verify_power_control(
        6, ROOTS_OF_UNITY[6], list(range(1, 3)), list(range(3, 13))
    ),
    12: verify_power_control(
        12, ROOTS_OF_UNITY[12], [1], list(range(2, 7))
    ),
}
degree_ten_control = verify_degree_ten_control()
all_controls = [
    power_controls[2],
    power_controls[3],
    power_controls[4],
    power_controls[6],
    degree_ten_control,
    power_controls[12],
]

require(
    [row["inner_degree"] for row in all_controls] == [2, 3, 4, 6, 10, 12],
    "control row order",
)
require(all(row["source_points"] == 12 for row in all_controls),
        "source totals")
require(all(row["active_points"] == 60 for row in all_controls),
        "active totals")

expected_dimensions = {
    2: ((3, 6), (6, 3), 2, (61, 31), 31, (61, 32), 31),
    3: ((4, 4), (4, 4), 2, (61, 21), 21, (61, 22), 21),
    4: ((5, 3), (3, 5), 2, (61, 16), 16, (61, 17), 16),
    6: ((7, 2), (2, 7), 2, (61, 11), 11, (61, 12), 11),
    10: ((11, 2), (2, 11), 2, (61, 7), 7, (61, 8), 7),
    12: ((13, 1), (1, 13), 1, (49, 5), 5, (49, 6), 5),
}
for row in all_controls:
    actual = (
        row["source_column_dimensions"],
        row["source_display_dimensions"],
        row["source_rank"],
        row["symmetric_dimensions"],
        row["symmetric_rank"],
        row["augmented_dimensions"],
        row["augmented_rank"],
    )
    require(actual == expected_dimensions[row["inner_degree"]],
            "deterministic matrix dimension/rank table")

require(power_controls[12]["canonical_source_dimensions"] == (13, 2),
        "m12 canonical source dimensions")
require(power_controls[12]["canonical_source_rank"] == 2,
        "m12 canonical source rank")
require(power_controls[12]["full_symmetric_dimensions"] == (61, 6),
        "m12 full symmetric dimensions")
require(power_controls[12]["full_symmetric_rank"] == 6,
        "m12 full symmetric rank")

control_recursive_routes = {
    2: [],
    3: [],
    4: [2],
    6: [2, 3],
    10: [2],
    12: [2, 3, 4, 6],
}
require(
    {
        row["inner_degree"]: row["recursive_right_degrees"]
        for row in all_controls
    }
    == control_recursive_routes,
    "control recursive route table",
)
compiler_possible_routes = {
    4: [2],
    6: [2, 3],
    10: [2, 5],
    12: [2, 3, 4, 6],
}
prime_degree_survivors = [
    inner_degree
    for inner_degree in (2, 3)
    if (
        not control_recursive_routes[inner_degree]
        and Integer(inner_degree).is_prime()
    )
]
require(prime_degree_survivors == [2, 3],
        "prime-degree survivor control")

partition_total = sum(PROFILE_ROWS[m][3] for m in (2, 3, 4, 6, 10, 12))
require(partition_total == 32099, "source partition total")

# Bind the computed matrix controls to the certificate profiles.  The
# certificate displays source generators as rows, while the compiler puts
# them in columns; both orientations are recorded above and have the same
# rank.
certificate_profiles = {
    row["m"]: row for row in certificate_data["compiler"]["profiles"]
}
for row in all_controls:
    certified = certificate_profiles[row["inner_degree"]]
    require(certified["n"] == row["outer_degree"],
            "certificate outer degree")
    require(tuple(certified["source_matrix"])
            == row["source_column_dimensions"],
            "certificate source matrix")
    require(certified["source_rank"] == row["source_rank"],
            "certificate source rank")
    require(tuple(certified["active_matrix"])
            == row["symmetric_dimensions"],
            "certificate active matrix")
    require(certified["active_rank"] == row["symmetric_rank"],
            "certificate active rank")

require(
    {
        int(degree): values
        for degree, values in certificate_data[
            "strict_right_factor_routing"
        ]["routes"].items()
    }
    == compiler_possible_routes,
    "certificate strict right-factor routes",
)


def regenerate_primitive_subdegree_catalogue():
    """Replay all small primitive-group rows through GAP PrimGrp."""

    certified_catalogue = certificate_data[
        "same_fiber_route_cut"
    ]["small_degree_catalogue"]
    observed_catalogue = []
    degrees_with_subdegree_four = []

    for certified in certified_catalogue:
        degree = Integer(certified["degree"])
        require(bool(libgap.PrimitiveGroupsAvailable(degree)),
                "GAP primitive groups unavailable")
        group_count = Integer(libgap.NrPrimitiveGroups(degree))
        require(group_count == certified["primitive_group_count"],
                "GAP primitive group count")

        subdegree_rows = []
        for index in range(1, group_count + 1):
            gap_group = libgap.PrimitiveGroup(degree, index)
            require(bool(libgap.IsPrimitive(gap_group)),
                    "GAP group is not primitive")
            group = PermutationGroup(gap_group=gap_group)
            stabilizer = group.stabilizer(1)
            subdegrees = sorted(
                len(orbit) for orbit in stabilizer.orbits()
            )
            require(sum(subdegrees) == degree,
                    "GAP subdegrees do not sum to degree")
            subdegree_rows.append(subdegrees)

        require(subdegree_rows == certified["subdegree_rows"],
                "GAP subdegree row mismatch")
        if any(4 in row for row in subdegree_rows):
            degrees_with_subdegree_four.append(int(degree))
        observed_catalogue.append(
            {
                "degree": int(degree),
                "group_count": int(group_count),
                "subdegree_rows": subdegree_rows,
            }
        )

    require(degrees_with_subdegree_four == [5],
            "subdegree four is not isolated at degree five")
    route_cut = certificate_data["same_fiber_route_cut"]
    require(
        route_cut[
            "degree_five_is_only_profile_with_catalogue_subdegree_four"
        ],
        "certificate degree-five uniqueness flag",
    )
    require(
        certificate_data["strict_right_factor_routing"][
            "degree_five_terminal"
        ]
        == "DELETED_CHALLENGE_FIELD_FIFTH_POWER_FIBER_CONTRADICTION",
        "degree-five deletion terminal",
    )
    return observed_catalogue, degrees_with_subdegree_four


observed_catalogue, degrees_with_subdegree_four = (
    regenerate_primitive_subdegree_catalogue()
)


def regenerate_transverse_rows():
    rows = []
    for profile in certificate_data["compiler"]["profiles"]:
        inner_degree = Integer(profile["m"])
        outer_degree = Integer(profile["n"])
        pairs = [
            [int(r), int(4 * inner_degree // r)]
            for r in divisors(4 * inner_degree)
            if (
                r <= outer_degree - 1
                and 4 * inner_degree // r <= inner_degree^2
            )
        ]
        require(
            all(r * delta == 4 * inner_degree for r, delta in pairs),
            "transverse degree identity",
        )
        require(
            all(delta <= inner_degree^2 for _, delta in pairs),
            "transverse cover-degree bound",
        )
        rows.append(
            {
                "m": int(inner_degree),
                "n": int(outer_degree),
                "r_delta": pairs,
            }
        )
    return rows


transverse_rows = regenerate_transverse_rows()
require(
    transverse_rows
    == certificate_data["transverse_outer_terminal"]["rows"],
    "transverse outer row mismatch",
)
require(
    certificate_data["transverse_outer_terminal"]["degree_identity"]
    == "delta*r=4*m",
    "transverse degree identity string",
)
require(
    certificate_data["transverse_outer_terminal"][
        "cover_degree_upper_bound"
    ]
    == "delta<=m^2",
    "transverse cover-degree string",
)

print("status=PASS_EXACT_SOURCE_PENCIL_RANK_CONTROLS")
print("duplicate_json_keys=REJECTED")
print("payload_sha256=%s" % certificate_data["payload_sha256"])
print("wolfram_replay_sha256=%s" % wolfram_binding["sha256"])
print("field_order=%s" % Q)
print("partition_total=%s" % partition_total)
print("rows=%s" % [row["inner_degree"] for row in all_controls])
print("matrix_table=%s" % {
    row["inner_degree"]: {
        "source": (
            row["source_column_dimensions"], row["source_rank"]
        ),
        "symmetric": (
            row["symmetric_dimensions"], row["symmetric_rank"]
        ),
        "augmented": (
            row["augmented_dimensions"], row["augmented_rank"]
        ),
    }
    for row in all_controls
})
print("m12_raw_source=((13, 1), 1)")
print("m12_canonical_source_columns=((13, 2), 2)")
print("control_recursive_right_degrees=%s" % control_recursive_routes)
print("compiler_possible_right_degrees=%s" % compiler_possible_routes)
print("prime_degree_survivors=%s" % prime_degree_survivors)
print("m10_source_y=%s" % degree_ten_control["source_y"])
print("m10_active_ys=%s" % degree_ten_control["active_ys"])
print("m10_exceptional_finite_points=%s"
      % degree_ten_control["exceptional_points"])
print("m10_y255_absent=True")
print("primitive_group_counts=%s" % {
    row["degree"]: row["group_count"] for row in observed_catalogue
})
print("primitive_subdegree_rows=%s" % {
    row["degree"]: row["subdegree_rows"] for row in observed_catalogue
})
print("degrees_with_subdegree_four=%s"
      % degrees_with_subdegree_four)
print("degree5_terminal=DELETED_CHALLENGE_FIELD_FIFTH_POWER_FIBER_CONTRADICTION")
print("transverse_rows=%s" % transverse_rows)
print("scope=EXACT_DEPLOYED_FIELD_CONTROLS_NOT_EXHAUSTION_OR_PAYMENT")
