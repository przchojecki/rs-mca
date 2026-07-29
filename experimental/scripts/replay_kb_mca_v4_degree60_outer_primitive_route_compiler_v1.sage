#!/usr/bin/env sage
"""Independent Sage/GAP replay of the degree-60 outer route compiler.

This file deliberately does not import the companion Python verifier.  GAP's
PrimGrp library regenerates the primitive-group catalogue, while the remaining
checks reconstruct the source rows, strict-composition exits, the m=10,r=4
empty branch, the finite-field part of the m=6 degree-five loop deletion, and
the m=4,r=8 branch-cycle integer programme.

The geometric normalization used in the m=6 loop deletion is not a finite
calculation.  This replay checks the Riemann--Hurwitz and finite-field
consequences conditional on the certified normal form c*z^5; it does not
silently promote that calculation into a replacement proof of the
two-total-ramification classification.
"""

from sage.all import DiGraph, Integer, Partitions, PermutationGroup, gcd, is_prime
from sage.libs.gap.libgap import libgap
from sage.version import version as sage_version

import copy
import hashlib
import itertools
import json
from pathlib import Path


if not __debug__:
    raise RuntimeError("optimized Sage/Python is not supported")


class ReplayError(RuntimeError):
    """Fail-closed replay error."""


def require(condition, message):
    if not condition:
        raise ReplayError(message)


def reject_duplicate_keys(pairs):
    output = {}
    for key, value in pairs:
        require(key not in output, "duplicate JSON key: {}".format(key))
        output[key] = value
    return output


def load_json(path):
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle, object_pairs_hook=reject_duplicate_keys)
    require(isinstance(value, dict), "certificate top level is not an object")
    return value


def canonical_payload_hash(data):
    payload = copy.deepcopy(data)
    payload.pop("payload_sha256", None)
    blob = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("ascii")
    return hashlib.sha256(blob).hexdigest()


SCRIPT = Path(__file__).resolve()
EXPERIMENTAL = SCRIPT.parents[1]
CERTIFICATE = (
    EXPERIMENTAL
    / "data"
    / "certificates"
    / "kb-mca-v4-degree60-outer-primitive-route-compiler-v1"
    / "kb_mca_v4_degree60_outer_primitive_route_compiler_v1.json"
)

data = load_json(CERTIFICATE)
require(
    data["schema"]
    == "kb-mca-v4-degree60-outer-primitive-route-compiler-v1",
    "certificate schema",
)
require(
    data["payload_sha256"] == canonical_payload_hash(data),
    "certificate payload hash",
)
replay_metadata = data["independent_replays"]["sage_gap"]
require(sage_version == replay_metadata["sage_version"], "Sage version")
require(
    str(libgap.eval("GAPInfo.Version")) == replay_metadata["gap_version"],
    "GAP version",
)


# ---------------------------------------------------------------------------
# 1. GAP PrimGrp catalogue and all primitive point-stabilizer subdegrees.
# ---------------------------------------------------------------------------

degrees = [30, 20, 15, 10, 6, 5]
observed_catalogue = []
observed_by_degree = {}

for degree in degrees:
    require(
        bool(libgap.PrimitiveGroupsAvailable(degree)),
        "GAP PrimGrp unavailable at degree {}".format(degree),
    )
    group_count = int(libgap.NrPrimitiveGroups(degree))
    groups = []
    for index in range(1, group_count + 1):
        gap_group = libgap.PrimitiveGroup(degree, index)
        require(
            bool(libgap.IsPrimitive(gap_group)),
            "PrimitiveGroup({},{}) is not primitive".format(degree, index),
        )
        require(
            bool(libgap.IsTransitive(gap_group)),
            "PrimitiveGroup({},{}) is not transitive".format(degree, index),
        )
        group = PermutationGroup(gap_group=gap_group)
        stabilizer = group.stabilizer(1)
        subdegrees = sorted(int(len(orbit)) for orbit in stabilizer.orbits())
        require(
            sum(subdegrees) == degree,
            "subdegrees do not sum to degree for PrimitiveGroup({},{})".format(
                degree, index
            ),
        )
        non_diagonal = list(subdegrees)
        require(
            1 in non_diagonal,
            "missing diagonal stabilizer orbit for PrimitiveGroup({},{})".format(
                degree, index
            ),
        )
        non_diagonal.remove(1)
        groups.append(
            {
                "primitive_group_index": index,
                "structure": str(libgap.StructureDescription(gap_group)),
                "order": int(group.order()),
                "subdegrees": subdegrees,
                "non_diagonal_subdegrees": non_diagonal,
            }
        )
    row = {
        "degree": degree,
        "primitive_group_count": group_count,
        "groups": groups,
    }
    observed_catalogue.append(row)
    observed_by_degree[degree] = row

require(
    observed_catalogue == data["primitive_outer_catalogue"],
    "GAP primitive catalogue differs from certificate",
)
require(
    sum(row["primitive_group_count"] for row in observed_catalogue) == 32,
    "unexpected total number of primitive groups",
)


# ---------------------------------------------------------------------------
# 2. Independent reconstruction of all transverse source rows and exits.
# ---------------------------------------------------------------------------

EXPECTED_ORIGINAL_ROWS = [
    (2, 30, 2, 4),
    (2, 30, 4, 2),
    (2, 30, 8, 1),
    (3, 20, 2, 6),
    (3, 20, 3, 4),
    (3, 20, 4, 3),
    (3, 20, 6, 2),
    (3, 20, 12, 1),
    (4, 15, 1, 16),
    (4, 15, 2, 8),
    (4, 15, 4, 4),
    (4, 15, 8, 2),
    (6, 10, 1, 24),
    (6, 10, 2, 12),
    (6, 10, 3, 8),
    (6, 10, 4, 6),
    (6, 10, 6, 4),
    (6, 10, 8, 3),
    (10, 6, 1, 40),
    (10, 6, 2, 20),
    (10, 6, 4, 10),
    (10, 6, 5, 8),
    (12, 5, 1, 48),
    (12, 5, 2, 24),
    (12, 5, 3, 16),
    (12, 5, 4, 12),
]
PARENT_DELETED = {(12, 5, 1, 48), (12, 5, 3, 16)}
ALLOWED_SOURCE_INNER_DEGREES = {2, 3, 4, 5, 6, 10, 12, 30}
TERMINAL_INNER_DEGREES = [2, 3, 4, 6, 10, 12]

require(len(EXPECTED_ORIGINAL_ROWS) == 26, "original row count")
for m, n, r, delta in EXPECTED_ORIGINAL_ROWS:
    require(m * n == 60, "endpoint degree identity")
    require(delta * r == 4 * m, "component degree identity")
    require(delta <= m * m, "cover bound")
    require(r <= n - 1, "outer component degree bound")

certified_deleted = {
    (int(row["m"]), int(row["n"]), int(row["r"]), int(row["delta"]))
    for row in data["parent_deleted_rows"]
}
require(certified_deleted == PARENT_DELETED, "parent-deleted rows")

expected_live = [
    row for row in EXPECTED_ORIGINAL_ROWS if row not in PARENT_DELETED
]
certified_live = [
    (
        int(row["m"]),
        int(row["n"]),
        int(row["r"]),
        int(row["delta"]),
    )
    for row in data["live_row_classification"]
]
require(certified_live == expected_live, "live row chronology")


def proper_divisors(value):
    return [
        divisor
        for divisor in range(2, value)
        if value % divisor == 0
    ]


target_subdegrees = {}
for m, _n, r, delta in expected_live:
    # The directly proved m=10,r=4 contradiction cannot be a coarser image.
    if (m, r, delta) == (10, 4, 10):
        continue
    target_subdegrees.setdefault(m, set()).add(r)
# The parent compiler immediately refines the degree-two m=30 profile to m=6.
target_subdegrees[30] = {1}


def independent_decomposition_analysis(m, n, r):
    output = []
    for right_degree in proper_divisors(n):
        new_inner_degree = m * right_degree
        admitted = new_inner_degree in ALLOWED_SOURCE_INNER_DEGREES
        field_obstruction = None
        if m == 6 and right_degree == 5:
            field_obstruction = (
                "M6_DEGREE5_OUTER_RIGHT_FACTOR_FIFTH_POWER_"
                "SPLIT_FIBER_CONTRADICTION"
            )
        same_fiber = (
            admitted
            and field_obstruction is None
            and r <= right_degree - 1
        )
        transverse = []
        if admitted and field_obstruction is None:
            for image_r in sorted(target_subdegrees.get(new_inner_degree, [])):
                numerator = right_degree * r
                if numerator % image_r:
                    continue
                cover_degree = numerator // image_r
                if cover_degree <= right_degree * right_degree:
                    transverse.append(
                        {
                            "image_inner_degree": new_inner_degree,
                            "image_r": image_r,
                            "cover_degree": cover_degree,
                            "degree_identity": "{}*{}={}*{}".format(
                                cover_degree, image_r, right_degree, r
                            ),
                        }
                    )
        output.append(
            {
                "outer_right_degree": right_degree,
                "new_inner_degree": new_inner_degree,
                "source_profile_admitted": admitted,
                "field_obstruction": field_obstruction,
                "same_right_fiber_possible": same_fiber,
                "transverse_image_targets": transverse,
                "viable": same_fiber or bool(transverse),
            }
        )
    return output


computed_terminals = []
for certified in data["live_row_classification"]:
    m = int(certified["m"])
    n = int(certified["n"])
    r = int(certified["r"])
    degree_row = observed_by_degree[n]
    raw_matches = [
        {
            "primitive_group_index": group["primitive_group_index"],
            "structure": group["structure"],
            "order": group["order"],
        }
        for group in degree_row["groups"]
        if r in group["non_diagonal_subdegrees"]
    ]
    require(
        raw_matches == certified["raw_primitive_matches"],
        "raw primitive matches at (m,r)=({},{})".format(m, r),
    )

    filtered_matches = list(raw_matches)
    if (m, r) == (4, 8):
        filtered_matches = []
    elif (m, r) == (12, 4):
        filtered_matches = [
            row for row in raw_matches if row["structure"] in {"A5", "S5"}
        ]
    require(
        filtered_matches == certified["primitive_matches"],
        "profile-filtered primitive matches at (m,r)=({},{})".format(m, r),
    )

    decomposition = independent_decomposition_analysis(m, n, r)
    require(
        decomposition == certified["decomposition_analysis"],
        "decomposition exits at (m,r)=({},{})".format(m, r),
    )
    decomposable = any(branch["viable"] for branch in decomposition)
    require(
        decomposable == certified["decomposable_realization_possible"],
        "decomposable flag at (m,r)=({},{})".format(m, r),
    )
    if filtered_matches:
        terminal = "PRIMITIVE_OUTER_COMPATIBLE_SURVIVOR"
    elif decomposable:
        terminal = "FORCED_STRICT_OUTER_DECOMPOSITION"
    else:
        terminal = "ACTUAL_PRODUCER_CONTRADICTION"
    require(
        terminal == certified["terminal"],
        "terminal at (m,r)=({},{})".format(m, r),
    )
    computed_terminals.append((m, r, int(certified["delta"]), terminal))

forced = [row for row in computed_terminals if row[3] == "FORCED_STRICT_OUTER_DECOMPOSITION"]
empty = [row for row in computed_terminals if row[3] == "ACTUAL_PRODUCER_CONTRADICTION"]
survivors = [
    row
    for row in computed_terminals
    if row[3] == "PRIMITIVE_OUTER_COMPATIBLE_SURVIVOR"
]
require(len(forced) == 18, "forced-decomposition count")
require(empty == [(10, 4, 10, "ACTUAL_PRODUCER_CONTRADICTION")], "new empty row")
require(
    [(m, r, delta) for m, r, delta, _terminal in survivors]
    == [(6, 3, 8), (6, 6, 4), (10, 5, 8), (12, 2, 24), (12, 4, 12)],
    "primitive-compatible survivors",
)


# ---------------------------------------------------------------------------
# 3. m=10,r=4: exhaustive strict-composition arithmetic.
# ---------------------------------------------------------------------------

m10_r4 = next(
    row
    for row in data["live_row_classification"]
    if (int(row["m"]), int(row["r"])) == (10, 4)
)
require(proper_divisors(6) == [2, 3], "degree-six right factors")
require(
    all(
        4 not in group["non_diagonal_subdegrees"]
        for group in observed_by_degree[6]["groups"]
    ),
    "degree-six primitive r=4 exclusion",
)
require(10 * 2 == 20 and 20 not in ALLOWED_SOURCE_INNER_DEGREES, "e=2 profile gate")
require(4 > 3 - 1, "e=3 same-fiber exclusion")
require(3 * 4 == 12 and 12 > 3 * 3, "e=3 transverse cover bound")
require(
    all(not branch["viable"] for branch in m10_r4["decomposition_analysis"]),
    "m=10,r=4 has a viable decomposition exit",
)
require(
    m10_r4["terminal"] == "ACTUAL_PRODUCER_CONTRADICTION",
    "m=10,r=4 terminal",
)


# ---------------------------------------------------------------------------
# 4. m=6 degree-five right factor: exact arithmetic after normal-form descent.
# ---------------------------------------------------------------------------

m6_cut = data["m6_degree_five_outer_right_factor_exclusion"]
field = m6_cut["field_arithmetic"]
p = Integer(field["p"])
extension_degree = int(field["extension_degree"])
q = p ** extension_degree
require(is_prime(p), "challenge characteristic is not prime")
require(p % 5 == 3, "challenge characteristic modulo five")
require(q % 5 == 4, "challenge field size modulo five")
require(gcd(Integer(5), q - 1) == 1, "fifth-power exponent is not invertible")
require(field["gcd_5_q_minus_1"] == 1, "certified fifth-power gcd")
require(field["fifth_power_permutates_K"] is True, "certified fifth-power permutation")
# Two total ramification points of a degree-five rational map exhaust RH:
# 2*(5-1) = 2*5-2.  The source coordinate is K-rational; the target
# normalization need only be geometric.  Equality inside one K-rational
# fibre still makes ratios of source coordinates fifth roots in K.
require(2 * (5 - 1) == 2 * 5 - 2, "degree-five RH exhaustion")
require(
    m6_cut["normal_form"]
    == (
        "c*z^5 after the K-rational source coordinate and a "
        "geometric target change"
    ),
    "m=6 normal-form statement",
)
require(
    m6_cut["terminal"] == "M6_DEGREE5_OUTER_RIGHT_FACTOR_DELETED",
    "m=6 loop terminal",
)


# ---------------------------------------------------------------------------
# 5. m=4,r=8: exact S6/A6 branch-cycle index table and integer programme.
# ---------------------------------------------------------------------------


def representative_permutation(cycle_type):
    degree = sum(cycle_type)
    permutation = list(range(degree))
    offset = 0
    for length in cycle_type:
        cycle = list(range(offset, offset + length))
        offset += length
        for source, target in zip(cycle, cycle[1:] + cycle[:1]):
            permutation[source] = target
    return permutation


def permutation_index(permutation):
    visited = set()
    cycles = 0
    for start in range(len(permutation)):
        if start in visited:
            continue
        cycles += 1
        point = start
        while point not in visited:
            visited.add(point)
            point = permutation[point]
    return len(permutation) - cycles


two_subsets = list(itertools.combinations(range(6), 2))
two_subset_lookup = {subset: index for index, subset in enumerate(two_subsets)}
intersection_one_orbital = [
    (first_index, second_index)
    for first_index, first in enumerate(two_subsets)
    for second_index, second in enumerate(two_subsets)
    if len(set(first).intersection(second)) == 1
]
require(len(two_subsets) == 15, "two-subset action degree")
require(len(intersection_one_orbital) == 120, "r=8 orbital degree")
orbital_lookup = {
    pair: index for index, pair in enumerate(intersection_one_orbital)
}


def induced_two_subset_permutation(permutation):
    return [
        two_subset_lookup[
            tuple(sorted((permutation[first], permutation[second])))
        ]
        for first, second in two_subsets
    ]


def induced_orbital_permutation(two_subset_permutation):
    return [
        orbital_lookup[
            (
                two_subset_permutation[first_index],
                two_subset_permutation[second_index],
            )
        ]
        for first_index, second_index in intersection_one_orbital
    ]


class_table = []
for partition in Partitions(6):
    cycle_type = tuple(int(part) for part in partition)
    permutation = representative_permutation(cycle_type)
    natural_index = permutation_index(permutation)
    subset_permutation = induced_two_subset_permutation(permutation)
    orbital_permutation = induced_orbital_permutation(subset_permutation)
    class_table.append(
        {
            "natural_cycle_type": list(cycle_type),
            "natural_sign": -1 if natural_index % 2 else 1,
            "degree_fifteen_index": permutation_index(subset_permutation),
            "r8_orbital_index": permutation_index(orbital_permutation),
        }
    )

m4 = data["m4_r8_primitive_branch_cycle_exclusion"]
require(class_table == m4["class_index_table"], "m=4 class-index table")
require(
    m4["outer_group_candidates"] == ["A6", "S6"],
    "m=4 primitive group candidates",
)
require(m4["degree_fifteen_total_index"] == 28, "degree-fifteen RH total")
require(m4["allowed_r8_total_indices"] == [238, 240, 242], "r=8 RH totals")

nonidentity = [row for row in class_table if row["degree_fifteen_index"] > 0]
pole_index = next(
    index
    for index, row in enumerate(nonidentity)
    if row["natural_cycle_type"] == [5, 1]
)


def branch_multisets(allowed_signs):
    solutions = []

    def search(position, point_remaining, orbital_remaining, counts):
        if position == len(nonidentity):
            if (
                point_remaining == 0
                and orbital_remaining == 0
                and counts[pole_index] >= 1
            ):
                solutions.append(tuple(counts))
            return
        row = nonidentity[position]
        if row["natural_sign"] not in allowed_signs:
            search(
                position + 1,
                point_remaining,
                orbital_remaining,
                counts + [0],
            )
            return
        point_index = row["degree_fifteen_index"]
        orbital_index = row["r8_orbital_index"]
        maximum = min(
            point_remaining // point_index,
            orbital_remaining // orbital_index,
        )
        for count in range(maximum + 1):
            search(
                position + 1,
                point_remaining - count * point_index,
                orbital_remaining - count * orbital_index,
                counts + [count],
            )

    for orbital_total in [238, 240, 242]:
        search(0, 28, orbital_total, [])
    return sorted(set(solutions))


a6_solutions = branch_multisets({1})
s6_solutions = branch_multisets({-1, 1})
require(a6_solutions == [], "A6 branch multiset should be empty")
require(len(s6_solutions) == 1, "S6 branch multiset should be unique")

unique = s6_solutions[0]
unique_rows = [
    {
        "natural_cycle_type": nonidentity[index]["natural_cycle_type"],
        "count": count,
    }
    for index, count in enumerate(unique)
    if count
]
unique_sign = 1
for row, count in zip(nonidentity, unique):
    unique_sign *= row["natural_sign"] ** count

require(
    unique_rows
    == [
        {"natural_cycle_type": [5, 1], "count": 2},
        {"natural_cycle_type": [2, 1, 1, 1, 1], "count": 1},
    ],
    "S6 unique branch multiset",
)
require(unique_sign == -1, "S6 unique multiset must have odd sign")
require(m4["A6_necessary_class_multisets"] == [], "certified A6 branch ledger")
require(
    m4["S6_necessary_class_multisets"] == [unique_rows],
    "certified S6 branch ledger",
)
require(
    m4["S6_unique_multiset_product_sign"] == unique_sign,
    "certified S6 product sign",
)
require(m4["S6_product_one_possible"] is False, "certified product-one flag")
require(
    m4["terminal"] == "M4_R8_PRIMITIVE_OUTER_BRANCH_CYCLE_CONTRADICTION",
    "m=4 primitive terminal",
)


# ---------------------------------------------------------------------------
# 6. Exhaustive low-genus Nielsen ledger for the m=6 and m=10 survivors.
# ---------------------------------------------------------------------------


def gap_mapping(permutation, degree):
    """Return a GAP permutation as a one-based image tuple."""

    return tuple(
        int(image) for image in libgap.ListPerm(permutation, degree)
    )


def mapping_from_cycles(degree, cycles):
    mapping = list(range(1, degree + 1))
    used_points = set()
    for cycle in cycles:
        require(len(cycle) >= 2, "witness contains a trivial written cycle")
        require(len(set(cycle)) == len(cycle), "repeated point in witness cycle")
        require(
            used_points.isdisjoint(cycle),
            "written witness cycles are not disjoint",
        )
        used_points.update(cycle)
        for source, target in zip(cycle, cycle[1:] + cycle[:1]):
            require(1 <= source <= degree, "witness cycle source out of range")
            require(1 <= target <= degree, "witness cycle target out of range")
            mapping[source - 1] = target
    require(sorted(mapping) == list(range(1, degree + 1)), "witness is not a permutation")
    return tuple(mapping)


def compose_mappings(left, right):
    """Composition left after right, matching the companion witness convention."""

    require(len(left) == len(right), "permutation composition degree")
    return tuple(left[right[index] - 1] for index in range(len(left)))


def inverse_mapping(mapping):
    inverse = [0] * len(mapping)
    for source, target in enumerate(mapping, start=1):
        inverse[target - 1] = source
    return tuple(inverse)


def mapping_cycle_type(mapping):
    visited = set()
    lengths = []
    for start in range(1, len(mapping) + 1):
        if start in visited:
            continue
        point = start
        length = 0
        while point not in visited:
            visited.add(point)
            length += 1
            point = mapping[point - 1]
        lengths.append(length)
    return sorted(lengths, reverse=True)


def mapping_index(mapping):
    return len(mapping) - len(mapping_cycle_type(mapping))


def generated_mapping_group(generators):
    """Exact closure of a small permutation generating set."""

    degree = len(generators[0])
    identity = tuple(range(1, degree + 1))
    seen = {identity}
    frontier = [identity]
    while frontier:
        element = frontier.pop()
        for generator in generators:
            product = compose_mappings(generator, element)
            if product not in seen:
                seen.add(product)
                frontier.append(product)
    return seen


def conjugate_mapping(conjugator, element):
    return compose_mappings(
        conjugator,
        compose_mappings(element, inverse_mapping(conjugator)),
    )


def survivor_group_model(outer_degree, group_index, subdegree):
    """Regenerate class and orbital indices for one primitive survivor."""

    gap_group = libgap.PrimitiveGroup(outer_degree, group_index)
    group_elements = {
        gap_mapping(element, outer_degree)
        for element in libgap.AsList(gap_group)
    }
    group_order = int(libgap.Size(gap_group))
    require(len(group_elements) == group_order, "primitive group element census")

    stabilizer_elements = [
        gap_mapping(element, outer_degree)
        for element in libgap.AsList(libgap.Stabilizer(gap_group, 1))
    ]
    unseen = set(range(2, outer_degree + 1))
    suborbits = []
    while unseen:
        point = min(unseen)
        orbit = {element[point - 1] for element in stabilizer_elements}
        suborbits.append(orbit)
        unseen.difference_update(orbit)
    matching_suborbits = [
        orbit for orbit in suborbits if len(orbit) == subdegree
    ]
    require(
        len(matching_suborbits) == 1,
        "survivor suborbit is not unique at ({},{},{})".format(
            outer_degree, group_index, subdegree
        ),
    )
    representative = min(matching_suborbits[0])
    orbital = sorted(
        {
            (element[0], element[representative - 1])
            for element in group_elements
        }
    )
    component_degree = outer_degree * subdegree
    require(len(orbital) == component_degree, "survivor orbital degree")
    orbital_lookup = {pair: index for index, pair in enumerate(orbital)}

    def component_index(element):
        induced = tuple(
            orbital_lookup[
                (element[first - 1], element[second - 1])
            ]
            + 1
            for first, second in orbital
        )
        return mapping_index(induced)

    class_rows = []
    classes = list(libgap.ConjugacyClasses(gap_group))
    for class_index, conjugacy_class in enumerate(classes, start=1):
        representative_mapping = gap_mapping(
            libgap.Representative(conjugacy_class),
            outer_degree,
        )
        class_elements = {
            gap_mapping(element, outer_degree)
            for element in libgap.AsList(conjugacy_class)
        }
        class_rows.append(
            {
                "class_index": class_index,
                "cycle_type": mapping_cycle_type(representative_mapping),
                "point_index": mapping_index(representative_mapping),
                "component_index": component_index(representative_mapping),
                "representative": representative_mapping,
                "elements": class_elements,
            }
        )
    require(
        set().union(*(row["elements"] for row in class_rows))
        == group_elements,
        "conjugacy classes do not partition primitive group",
    )
    return {
        "outer_degree": outer_degree,
        "group_index": group_index,
        "structure": str(libgap.StructureDescription(gap_group)),
        "group_order": group_order,
        "subdegree": subdegree,
        "component_degree": component_degree,
        "group_elements": group_elements,
        "class_rows": class_rows,
        "component_index": component_index,
    }


def necessary_low_genus_class_profiles(model, required_pole_type):
    """Enumerate every class multiset surviving the two RH index bounds."""

    nonidentity = [
        row for row in model["class_rows"] if row["class_index"] != 1
    ]
    pole_rows = [
        row for row in nonidentity if row["cycle_type"] == required_pole_type
    ]
    require(pole_rows, "required pole class is absent")
    point_total = 2 * model["outer_degree"] - 2
    component_floor = 2 * model["component_degree"] - 2
    component_totals = {component_floor, component_floor + 2}
    profiles = []

    for pole in pole_rows:
        def search(start, point_remaining, component_sum, chosen):
            if point_remaining == 0:
                total_component_index = (
                    pole["component_index"] + component_sum
                )
                if total_component_index in component_totals:
                    profiles.append(
                        (
                            pole["class_index"],
                            *(row["class_index"] for row in chosen),
                        )
                    )
                return
            for position in range(start, len(nonidentity)):
                row = nonidentity[position]
                if row["point_index"] > point_remaining:
                    continue
                search(
                    position,
                    point_remaining - row["point_index"],
                    component_sum + row["component_index"],
                    chosen + [row],
                )

        search(
            0,
            point_total - pole["point_index"],
            0,
            [],
        )

    require(
        all(len(profile) == 3 for profile in profiles),
        "a necessary low-genus profile has more than three branch values",
    )
    return sorted(set(profiles))


def normalized_triple_orbit_keys(model, class_indices):
    """Enumerate product-one generating triples modulo simultaneous conjugacy."""

    require(len(class_indices) == 3, "Nielsen profile is not a triple")
    classes = {
        row["class_index"]: row for row in model["class_rows"]
    }
    first_class, second_class, third_class = [
        classes[index] for index in class_indices
    ]
    first = first_class["representative"]
    first_inverse = inverse_mapping(first)
    identity = tuple(range(1, model["outer_degree"] + 1))
    require(
        compose_mappings(first, first_inverse) == identity,
        "first-class inverse",
    )

    centralizer = [
        element
        for element in model["group_elements"]
        if compose_mappings(element, first)
        == compose_mappings(first, element)
    ]
    require(
        len(centralizer)
        * len(first_class["elements"])
        == model["group_order"],
        "class-centralizer identity",
    )

    def orbit_key(second, third):
        return min(
            (
                conjugate_mapping(element, second),
                conjugate_mapping(element, third),
            )
            for element in centralizer
        )

    keys = set()
    for second in second_class["elements"]:
        # The witness convention multiplies as third after second after first.
        third = inverse_mapping(compose_mappings(second, first))
        if third not in third_class["elements"]:
            continue
        generated = generated_mapping_group([first, second])
        if len(generated) != model["group_order"]:
            continue
        require(
            generated == model["group_elements"],
            "full-order generated subgroup differs from primitive group",
        )
        require(
            compose_mappings(
                third, compose_mappings(second, first)
            )
            == identity,
            "enumerated triple product",
        )
        keys.add(orbit_key(second, third))
    return keys, centralizer


def normalized_witness_orbit_key(model, passport, witness, centralizer):
    """Validate one stored witness and return its normalized orbit key."""

    degree = model["outer_degree"]
    generators = [
        mapping_from_cycles(degree, cycles)
        for cycles in witness["generators_in_point_action_cycles"]
    ]
    require(len(generators) == 3, "stored Nielsen witness arity")
    identity = tuple(range(1, degree + 1))
    product = identity
    for generator in generators:
        product = compose_mappings(generator, product)
    require(product == identity, "stored Nielsen witness product one")
    require(
        all(generator in model["group_elements"] for generator in generators),
        "stored witness generator is outside primitive group",
    )
    require(
        [
            mapping_cycle_type(generator) for generator in generators
        ]
        == passport["point_cycle_types"],
        "stored witness point cycle types",
    )
    require(
        [mapping_index(generator) for generator in generators]
        == passport["point_indices"],
        "stored witness point indices",
    )
    witness_group = generated_mapping_group(generators)
    require(
        len(witness_group) == passport["group_order"],
        "stored witness generated group order",
    )
    require(
        witness_group == model["group_elements"],
        "stored witness does not generate the certified primitive group",
    )
    require(
        [
            model["component_index"](generator)
            for generator in generators
        ]
        == passport["component_indices"],
        "stored witness component indices",
    )
    classes = {
        row["class_index"]: row for row in model["class_rows"]
    }
    require(
        all(
            generator in classes[class_index]["elements"]
            for generator, class_index in zip(
                generators,
                passport["gap_conjugacy_class_indices"],
            )
        ),
        "stored witness GAP class membership",
    )
    require(witness["product_one"] is True, "stored witness product flag")
    require(
        witness["generated_group_order"] == passport["group_order"],
        "stored witness group-order field",
    )
    require(
        witness["point_cycle_types"] == passport["point_cycle_types"],
        "stored witness point-cycle field",
    )
    require(
        witness["point_indices"] == passport["point_indices"],
        "stored witness point-index field",
    )
    require(
        witness["component_indices"] == passport["component_indices"],
        "stored witness component-index field",
    )
    require(
        witness["component_genus"] == passport["component_genus"],
        "stored witness component-genus field",
    )

    first_representative = classes[
        passport["gap_conjugacy_class_indices"][0]
    ]["representative"]
    conjugator = next(
        (
            element
            for element in model["group_elements"]
            if conjugate_mapping(element, generators[0])
            == first_representative
        ),
        None,
    )
    require(conjugator is not None, "cannot normalize stored first generator")
    normalized = [
        conjugate_mapping(conjugator, generator)
        for generator in generators
    ]
    require(
        normalized[0] == first_representative,
        "stored witness first-generator normalization",
    )
    return min(
        (
            conjugate_mapping(element, normalized[1]),
            conjugate_mapping(element, normalized[2]),
        )
        for element in centralizer
    )


nielsen = data["primitive_survivor_low_genus_nielsen_ledger"]
certified_passports = nielsen["m6_passports"] + nielsen["m10_passports"]
certified_by_key = {
    (
        int(row["m"]),
        int(row["outer_degree"]),
        int(row["subdegree"]),
        int(row["primitive_group_index"]),
        tuple(int(index) for index in row["gap_conjugacy_class_indices"]),
    ): row
    for row in certified_passports
}
require(
    len(certified_by_key) == len(certified_passports),
    "duplicate certified Nielsen passport",
)

survivor_models = [
    (6, 10, 3, 1, [5, 5]),
    (6, 10, 6, 1, [5, 5]),
    (6, 10, 3, 2, [5, 5]),
    (6, 10, 6, 2, [5, 5]),
    (10, 6, 5, 1, [5, 1]),
    (10, 6, 5, 2, [5, 1]),
    (10, 6, 5, 3, [5, 1]),
    (10, 6, 5, 4, [5, 1]),
]
observed_passport_keys = set()
observed_orbit_count = 0
necessary_profile_count = 0

for m, outer_degree, subdegree, group_index, pole_type in survivor_models:
    model = survivor_group_model(outer_degree, group_index, subdegree)
    necessary_profiles = necessary_low_genus_class_profiles(model, pole_type)
    necessary_profile_count += len(necessary_profiles)
    for class_indices in necessary_profiles:
        orbit_keys, centralizer = normalized_triple_orbit_keys(
            model, class_indices
        )
        if not orbit_keys:
            continue
        passport_key = (
            m,
            outer_degree,
            subdegree,
            group_index,
            tuple(class_indices),
        )
        observed_passport_keys.add(passport_key)
        require(
            passport_key in certified_by_key,
            "unrecorded generating Nielsen passport {}".format(passport_key),
        )
        passport = certified_by_key[passport_key]
        class_by_index = {
            row["class_index"]: row for row in model["class_rows"]
        }
        class_rows = [
            class_by_index[index] for index in class_indices
        ]
        point_indices = [row["point_index"] for row in class_rows]
        component_indices = [
            row["component_index"] for row in class_rows
        ]
        component_genus_numerator = (
            sum(component_indices)
            - (2 * model["component_degree"] - 2)
        )
        require(
            component_genus_numerator in {0, 2},
            "observed component genus exceeds one",
        )
        require(passport["m"] == m, "passport inner degree")
        require(passport["outer_degree"] == outer_degree, "passport outer degree")
        require(passport["subdegree"] == subdegree, "passport subdegree")
        require(
            passport["primitive_group_index"] == group_index,
            "passport primitive group index",
        )
        require(passport["structure"] == model["structure"], "passport structure")
        require(passport["group_order"] == model["group_order"], "passport group order")
        require(
            passport["point_cycle_types"]
            == [row["cycle_type"] for row in class_rows],
            "passport point cycle types",
        )
        require(passport["point_indices"] == point_indices, "passport point indices")
        require(sum(point_indices) == 2 * outer_degree - 2, "point genus zero")
        require(
            passport["component_degree"] == model["component_degree"],
            "passport component degree",
        )
        require(
            passport["component_indices"] == component_indices,
            "passport component indices",
        )
        require(
            passport["component_genus"] == component_genus_numerator // 2,
            "passport component genus",
        )
        require(
            passport["simultaneous_conjugacy_orbit_count"]
            == len(orbit_keys),
            "passport simultaneous-conjugacy orbit count",
        )
        witness_keys = {
            normalized_witness_orbit_key(
                model, passport, witness, centralizer
            )
            for witness in passport["orbit_witnesses"]
        }
        require(
            len(witness_keys) == len(passport["orbit_witnesses"]),
            "duplicate stored witness orbit",
        )
        require(
            witness_keys == orbit_keys,
            "stored witnesses do not exhaust simultaneous-conjugacy orbits",
        )
        observed_orbit_count += len(orbit_keys)

require(
    observed_passport_keys == set(certified_by_key),
    "certified Nielsen passport set differs from exhaustive replay",
)
require(necessary_profile_count == 25, "necessary low-genus class-profile count")
require(len(observed_passport_keys) == 16, "Nielsen passport count")
require(observed_orbit_count == 18, "Nielsen orbit count")
require(nielsen["passport_count"] == 16, "certified Nielsen passport count")
require(
    nielsen["simultaneous_conjugacy_orbit_count"] == 18,
    "certified Nielsen orbit count",
)
require(
    nielsen["all_survivors_have_three_branch_values"] is True,
    "certified three-branch flag",
)
require(
    nielsen["terminal"] == "FINITE_PRIMITIVE_NIELSEN_TARGETS_UNPAID",
    "Nielsen terminal",
)


# ---------------------------------------------------------------------------
# 7. Global strict-route graph after the exact m=6 edge deletion.
# ---------------------------------------------------------------------------


def independent_route_table():
    rows = []
    for m in TERMINAL_INNER_DEGREES:
        n = 60 // m
        targets = []
        for right_degree in proper_divisors(n):
            new_inner_degree = m * right_degree
            admitted = new_inner_degree in ALLOWED_SOURCE_INNER_DEGREES
            field_compatible = not (m == 6 and right_degree == 5)
            if not admitted:
                terminal = "SOURCE_PROFILE_IMPOSSIBLE"
            elif not field_compatible:
                terminal = "M6_DEGREE5_OUTER_RIGHT_FACTOR_DELETED"
            elif new_inner_degree == 30:
                terminal = "M30_REFINES_TO_M6"
            else:
                terminal = "REENTER_INNER_DEGREE_{}".format(new_inner_degree)
            targets.append(
                {
                    "outer_right_degree": right_degree,
                    "new_inner_degree": new_inner_degree,
                    "source_profile_admitted": admitted,
                    "field_compatible": field_compatible,
                    "terminal": terminal,
                }
            )
        rows.append(
            {
                "from_inner_degree": m,
                "outer_degree": n,
                "proper_outer_right_degrees": proper_divisors(n),
                "targets": targets,
            }
        )
    return rows


routes = independent_route_table()
require(routes == data["strict_outer_decomposition_routes"], "strict route table")

admitted_edges = []
impossible_targets = []
deleted_edges = []
for route in routes:
    source = route["from_inner_degree"]
    for target in route["targets"]:
        edge = [source, target["new_inner_degree"]]
        if target["source_profile_admitted"] and target["field_compatible"]:
            admitted_edges.append(edge)
        elif not target["source_profile_admitted"]:
            impossible_targets.append(edge)
        if not target["field_compatible"]:
            deleted_edges.append(edge)
# The imported m=30 fifth-power refinement is a directed return to m=6.
admitted_edges.append([30, 6])

admitted_edges = sorted(admitted_edges)
impossible_targets = sorted(impossible_targets)
deleted_edges = sorted(deleted_edges)
route_graph = data["route_graph"]
require(admitted_edges == sorted(route_graph["admitted_edges"]), "admitted route edges")
require(
    impossible_targets == sorted(route_graph["source_profile_impossible_targets"]),
    "source-profile-impossible route targets",
)
require(deleted_edges == sorted(route_graph["field_deleted_edges"]), "deleted route edges")

live_edges = [
    tuple(edge) for edge in admitted_edges if edge not in deleted_edges
]
graph = DiGraph(live_edges)
require(graph.is_directed_acyclic(), "normalized route graph has a cycle")
nontrivial_sccs = sorted(
    sorted(int(vertex) for vertex in component)
    for component in graph.strongly_connected_components()
    if len(component) > 1
)
require(nontrivial_sccs == [], "normalized route graph SCCs")
require(route_graph["route_graph_acyclic"] is True, "certified route DAG flag")
require(
    route_graph["nontrivial_strongly_connected_components"] == [],
    "certified route SCC list",
)


conclusion = data["conclusion"]
require(conclusion["original_transverse_type_count"] == 26, "conclusion original count")
require(conclusion["parent_deleted_type_count"] == 2, "conclusion deletion count")
require(conclusion["live_input_type_count"] == 24, "conclusion live count")
require(
    conclusion["forced_strict_outer_decomposition_type_count"] == 18,
    "conclusion forced count",
)
require(
    conclusion["new_actual_producer_contradiction_type_count"] == 1,
    "conclusion contradiction count",
)
require(
    conclusion["primitive_outer_survivor_type_count"] == 5,
    "conclusion survivor count",
)
require(conclusion["ledger_movement"] == 0, "ledger movement")
require(conclusion["K3_closed"] is False, "K3 closure overclaim")

print(
    "PASS: GAP PrimGrp catalogue regenerated for degrees {} (32 groups; "
    "Sage {}; GAP {})".format(
        degrees, sage_version, str(libgap.eval("GAPInfo.Version"))
    )
)
print(
    "PASS: transverse partition original=26 parent_deleted=2 live=24 "
    "forced_decomposition=18 contradiction=1 primitive_survivors=5"
)
print(
    "PASS: m=10,r=4 excluded by primitive subdegrees and both strict "
    "right-factor branches"
)
print(
    "PASS: m=6 loop arithmetic p={} q_mod_5={} gcd(5,q-1)={} RH=8; "
    "finite-field contradiction is conditional on the imported geometric normal form".format(
        p, q % 5, gcd(Integer(5), q - 1)
    )
)
print(
    "PASS: m=4,r=8 branch DP A6_solutions=0 S6_solutions=1 "
    "unique_product_sign={}".format(unique_sign)
)
print(
    "PASS: primitive-survivor Nielsen ledger necessary_profiles={} "
    "generating_passports={} simultaneous_conjugacy_orbits={}".format(
        necessary_profile_count,
        len(observed_passport_keys),
        observed_orbit_count,
    )
)
print(
    "PASS: normalized strict-route graph vertices={} edges={} acyclic=True".format(
        graph.num_verts(), graph.num_edges()
    )
)
print("PASS: payload_sha256={}".format(data["payload_sha256"]))
