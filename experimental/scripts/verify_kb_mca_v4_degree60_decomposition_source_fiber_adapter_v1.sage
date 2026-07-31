#!/usr/bin/env sage
"""Exact Sage replay of the degree-60 decomposition source-fiber adapter.

The replay uses only divisor arithmetic and Riemann--Hurwitz.  Suppose that
``f = F o h`` has degree 60, its zero divisor consists of 60 simple points,
and its pole divisor consists of twelve points of order five.  Write
``m = deg(h)`` and ``n = deg(F)``.  Above an outer pole the local-order
identity is

    (outer pole order) * (ramification index of h) = 5.

Thus every outer pole is either order five with an unramified complete
``m``-point source fibre, or order one with an index-five source fibre.
"""


ENDPOINT_DEGREE = Integer(60)
POLE_ORDER = Integer(5)
SOURCE_POINT_COUNT = Integer(12)
FULL_DOMAIN_SIZE = Integer(2)^21
DEPLOYED_CHARACTERISTIC = Integer(2130706433)
CHALLENGE_FIELD_SIZE = DEPLOYED_CHARACTERISTIC^6


def enumerate_profiles():
    """Enumerate all nontrivial decomposition profiles allowed by RH."""

    admitted = []
    rejected_by_rh = []
    for inner_degree in divisors(ENDPOINT_DEGREE):
        inner_degree = Integer(inner_degree)
        if inner_degree in (1, ENDPOINT_DEGREE):
            continue

        outer_degree = ENDPOINT_DEGREE // inner_degree
        for simple_outer_poles in range(outer_degree + 1):
            remainder = outer_degree - simple_outer_poles
            if remainder % POLE_ORDER:
                continue
            order_five_outer_poles = remainder // POLE_ORDER

            # A simple outer pole requires every point in its fibre to
            # have ramification index five.
            if simple_outer_poles and inner_degree % POLE_ORDER:
                continue

            forced_ramification = (
                simple_outer_poles
                * (POLE_ORDER - 1)
                * inner_degree
                // POLE_ORDER
            )
            riemann_hurwitz_budget = 2 * inner_degree - 2
            row = {
                "inner_degree": int(inner_degree),
                "outer_degree": int(outer_degree),
                "order_five_outer_poles": int(order_five_outer_poles),
                "simple_outer_poles": int(simple_outer_poles),
                "active_outer_zeros": int(outer_degree),
                "active_complete_points": int(
                    outer_degree * inner_degree
                ),
                "complete_source_points": int(
                    order_five_outer_poles * inner_degree
                ),
                "exceptional_source_points": int(
                    simple_outer_poles * inner_degree // POLE_ORDER
                ),
                "forced_ramification": int(forced_ramification),
                "riemann_hurwitz_budget": int(riemann_hurwitz_budget),
                "riemann_hurwitz_slack": int(
                    riemann_hurwitz_budget - forced_ramification
                ),
                "source_partition_count": int(
                    factorial(SOURCE_POINT_COUNT)
                    // (
                        factorial(inner_degree)
                        ^ order_five_outer_poles
                        * factorial(order_five_outer_poles)
                        * factorial(inner_degree // POLE_ORDER)
                        ^ simple_outer_poles
                        * factorial(simple_outer_poles)
                    )
                ),
                "full_domain_divides_2power21": bool(
                    FULL_DOMAIN_SIZE % inner_degree == 0
                ),
            }
            if forced_ramification <= riemann_hurwitz_budget:
                admitted.append(row)
            else:
                rejected_by_rh.append(row)

    return admitted, rejected_by_rh


profiles, rejected_by_rh = enumerate_profiles()

expected = [
    {
        "inner_degree": 2,
        "outer_degree": 30,
        "order_five_outer_poles": 6,
        "simple_outer_poles": 0,
        "active_outer_zeros": 30,
        "active_complete_points": 60,
        "complete_source_points": 12,
        "exceptional_source_points": 0,
        "forced_ramification": 0,
        "riemann_hurwitz_budget": 2,
        "riemann_hurwitz_slack": 2,
        "source_partition_count": 10395,
        "full_domain_divides_2power21": True,
    },
    {
        "inner_degree": 3,
        "outer_degree": 20,
        "order_five_outer_poles": 4,
        "simple_outer_poles": 0,
        "active_outer_zeros": 20,
        "active_complete_points": 60,
        "complete_source_points": 12,
        "exceptional_source_points": 0,
        "forced_ramification": 0,
        "riemann_hurwitz_budget": 4,
        "riemann_hurwitz_slack": 4,
        "source_partition_count": 15400,
        "full_domain_divides_2power21": False,
    },
    {
        "inner_degree": 4,
        "outer_degree": 15,
        "order_five_outer_poles": 3,
        "simple_outer_poles": 0,
        "active_outer_zeros": 15,
        "active_complete_points": 60,
        "complete_source_points": 12,
        "exceptional_source_points": 0,
        "forced_ramification": 0,
        "riemann_hurwitz_budget": 6,
        "riemann_hurwitz_slack": 6,
        "source_partition_count": 5775,
        "full_domain_divides_2power21": True,
    },
    {
        "inner_degree": 5,
        "outer_degree": 12,
        "order_five_outer_poles": 2,
        "simple_outer_poles": 2,
        "active_outer_zeros": 12,
        "active_complete_points": 60,
        "complete_source_points": 10,
        "exceptional_source_points": 2,
        "forced_ramification": 8,
        "riemann_hurwitz_budget": 8,
        "riemann_hurwitz_slack": 0,
        "source_partition_count": 8316,
        "full_domain_divides_2power21": False,
    },
    {
        "inner_degree": 6,
        "outer_degree": 10,
        "order_five_outer_poles": 2,
        "simple_outer_poles": 0,
        "active_outer_zeros": 10,
        "active_complete_points": 60,
        "complete_source_points": 12,
        "exceptional_source_points": 0,
        "forced_ramification": 0,
        "riemann_hurwitz_budget": 10,
        "riemann_hurwitz_slack": 10,
        "source_partition_count": 462,
        "full_domain_divides_2power21": False,
    },
    {
        "inner_degree": 10,
        "outer_degree": 6,
        "order_five_outer_poles": 1,
        "simple_outer_poles": 1,
        "active_outer_zeros": 6,
        "active_complete_points": 60,
        "complete_source_points": 10,
        "exceptional_source_points": 2,
        "forced_ramification": 8,
        "riemann_hurwitz_budget": 18,
        "riemann_hurwitz_slack": 10,
        "source_partition_count": 66,
        "full_domain_divides_2power21": False,
    },
    {
        "inner_degree": 12,
        "outer_degree": 5,
        "order_five_outer_poles": 1,
        "simple_outer_poles": 0,
        "active_outer_zeros": 5,
        "active_complete_points": 60,
        "complete_source_points": 12,
        "exceptional_source_points": 0,
        "forced_ramification": 0,
        "riemann_hurwitz_budget": 22,
        "riemann_hurwitz_slack": 22,
        "source_partition_count": 1,
        "full_domain_divides_2power21": False,
    },
    {
        "inner_degree": 30,
        "outer_degree": 2,
        "order_five_outer_poles": 0,
        "simple_outer_poles": 2,
        "active_outer_zeros": 2,
        "active_complete_points": 60,
        "complete_source_points": 0,
        "exceptional_source_points": 12,
        "forced_ramification": 48,
        "riemann_hurwitz_budget": 58,
        "riemann_hurwitz_slack": 10,
        "source_partition_count": 462,
        "full_domain_divides_2power21": False,
    },
]

assert profiles == expected
assert [row["inner_degree"] for row in profiles] == [
    2, 3, 4, 5, 6, 10, 12, 30
]
proper_inner_degrees = {
    int(value)
    for value in divisors(ENDPOINT_DEGREE)
    if value not in (1, ENDPOINT_DEGREE)
}
excluded_inner_degrees = sorted(
    proper_inner_degrees
    - {row["inner_degree"] for row in profiles}
)
assert excluded_inner_degrees == [15, 20]
assert all(
    any(
        row["inner_degree"] == inner_degree
        for row in rejected_by_rh
    )
    for inner_degree in excluded_inner_degrees
)

for row in profiles:
    assert (
        5 * row["order_five_outer_poles"]
        + row["simple_outer_poles"]
        == row["outer_degree"]
    )
    assert row["active_complete_points"] == ENDPOINT_DEGREE
    assert (
        row["complete_source_points"]
        + row["exceptional_source_points"]
        == SOURCE_POINT_COUNT
    )
    assert (
        row["forced_ramification"]
        + row["riemann_hurwitz_slack"]
        == row["riemann_hurwitz_budget"]
    )

assert [
    row["inner_degree"]
    for row in profiles
    if row["full_domain_divides_2power21"]
] == [2, 4]

# In the degree-five row, the two simple outer poles pull back to two
# totally ramified points of index five.  They consume the complete
# Riemann--Hurwitz budget 2m-2=8, so geometrically h is a two-branch-point
# cyclic (power-map) cover.  The challenge field has q=p^6 elements and
# gcd(5,q-1)=1, so fifth powering is bijective on K^x.  It therefore
# cannot have one of the reduced five-point K-rational active fibres.
degree_five = next(
    row for row in profiles if row["inner_degree"] == 5
)
assert degree_five["simple_outer_poles"] == 2
assert degree_five["exceptional_source_points"] == 2
assert degree_five["forced_ramification"] == 8
assert degree_five["riemann_hurwitz_budget"] == 8
assert degree_five["riemann_hurwitz_slack"] == 0

p = DEPLOYED_CHARACTERISTIC
q = CHALLENGE_FIELD_SIZE
assert p.is_prime()
assert p % 5 == 3
assert q % 5 == 4
assert gcd(5, q - 1) == 1
fifth_root_exponent = inverse_mod(5, q - 1)
assert (5 * fifth_root_exponent) % (q - 1) == 1

# In the degree-thirty row, the two exceptional pole fibres are reduced
# degree-six divisors pulled back with multiplicity five.  After sending
# their outer values to zero and infinity, the numerator and denominator
# of h are fifth powers of degree-six forms.  Thus h=p_5 o r with
# deg(r)=6, so the row refines to inner degree six.
degree_thirty = next(
    row for row in profiles if row["inner_degree"] == 30
)
assert degree_thirty["simple_outer_poles"] == 2
assert degree_thirty["complete_source_points"] == 0
assert degree_thirty["exceptional_source_points"] == 12
assert degree_thirty["inner_degree"] // 5 == 6
assert 5 * 6 == degree_thirty["inner_degree"]

degree_twelve = next(
    row for row in profiles if row["inner_degree"] == 12
)
assert degree_twelve["source_partition_count"] == 1

print("status=PROVED_DEGREE60_DECOMPOSITION_SOURCE_FIBER_ADAPTER")
print("inner_degrees=%s" % [row["inner_degree"] for row in profiles])
print("rh_rejected_inner_degrees=%s" % excluded_inner_degrees)
print("conditional_same_degree_carrier_eligible_degrees=%s" % [2, 4])
print("source_splits=%s" % [
    (
        row["inner_degree"],
        row["complete_source_points"],
        row["exceptional_source_points"],
    )
    for row in profiles
])
print("source_partition_counts=%s" % [
    row["source_partition_count"] for row in profiles
])
print("degree5_rh_saturated=True")
print("challenge_field_cardinality_mod5=%s" % (q % 5))
print("fifth_power_on_challenge_field_bijective=True")
print("degree30_refined_inner_degree=6")
print("degree12_canonical_source_partition_count=1")
