#!/usr/bin/env sage
"""Independent Sage replay for the K3 source-bound route cut.

This implementation does not import the primary Python verifier.  It checks
the deployed field, exact route enumeration, diagonal involution census,
outside-label orbit arithmetic, O0b residual totals, and the fact that the
known joint reserve is not enough to define a K3 allocation.  In particular,
the exact 11,304 arithmetic below is only a conditional candidate abstract-
label-orbit workload: it is not a census, elimination, or payment.
"""

from itertools import permutations
import json


P = 2130706433
B_STAR = 274980728111395087
U_PAID = 981104
EXPECTED_RESERVE = 274980728110413983


def require(condition, message):
    if not condition:
        raise AssertionError(message)


# Field-level replay of the repeated-BC transport invariant.
F = GF(P)
require(F.characteristic() != 2, "odd characteristic")
require(F(1) != F(-1), "parallel-product ratios are distinct")


COMMON = {
    "442-0a": (2, 0),
    "442-1b": (1, 1),
    "433-0": (0, 0),
    "433-1a": (3, 1),
    "433-1b": (1, 1),
}
OUTSIDE = {
    "O0a": (2, 0),
    "O0b": (0, 0),
    "O1a": (5, 1),
    "O1b": (1, 1),
    "O1c": (3, 1),
    "O1d": (1, 1),
}
CLOSED = {("433-1a", "O0b"), ("433-1b", "O0a")}

routes = []
for common in sorted(COMMON):
    for outside in sorted(OUTSIDE):
        cdef, cloop = COMMON[common]
        odef, oloop = OUTSIDE[outside]
        if cdef + odef > 3 or (cloop and oloop):
            continue
        routes.append((common, outside))

expected_routes = sorted([
    ("442-0a", "O0b"), ("442-0a", "O1b"), ("442-0a", "O1d"),
    ("442-1b", "O0a"), ("442-1b", "O0b"),
    ("433-0", "O0a"), ("433-0", "O0b"), ("433-0", "O1b"),
    ("433-0", "O1c"), ("433-0", "O1d"),
    ("433-1a", "O0b"),
    ("433-1b", "O0a"), ("433-1b", "O0b"),
])
require(sorted(routes) == expected_routes, "thirteen-route table")
require(len(routes) == 13 and len([r for r in routes if r not in CLOSED]) == 11,
        "closed/remaining route split")


def fpf_involutions(labels):
    labels = tuple(labels)
    if not labels:
        yield {}
        return
    head, rest = labels[0], labels[1:]
    for index, partner in enumerate(rest):
        tail = rest[:index] + rest[index + 1:]
        for sub in fpf_involutions(tail):
            tau = dict(sub)
            tau[head] = partner
            tau[partner] = head
            yield tau


I = set(range(6))
J = set(range(6, 12))
K0 = set(range(5))
xi = 5
rows = {}
total = 0
deleted = 0
for tau in fpf_involutions(range(12)):
    total += 1
    tauI = {tau[x] for x in I}
    if tauI == I:
        deleted += 1
        continue
    tauJ = {tau[x] for x in J}
    c = len(I.intersection(tauJ))
    require(c == len(J.intersection(tauI)), "crossing symmetry")
    a = sum(1 for k in K0 if tau[k] in K0 and tau[k] > k)
    b = ZZ(tau[xi] in K0)
    rows[(a, b, c)] = rows.get((a, b, c), 0) + 1

require(total == 10395 and deleted == 225, "involution totals")
require(rows == {
    (0, 0, 6): 720,
    (0, 1, 4): 1800,
    (1, 0, 4): 3600,
    (1, 1, 2): 2700,
    (2, 0, 2): 1350,
}, "diagonal row census")


def matchings(items):
    items = tuple(items)
    if not items:
        return [frozenset()]
    first = items[0]
    out = []
    for index in range(1, len(items)):
        pair = frozenset((first, items[index]))
        rest = items[1:index] + items[index + 1:]
        for matching in matchings(rest):
            out.append(matching | {pair})
    return out


labels = []
for missing in range(7):
    rest = tuple(x for x in range(7) if x != missing)
    labels.extend((missing, matching) for matching in matchings(rest))
require(len(labels) == 105 and len(set(labels)) == 105, "outside label universe")


def make_perm(cycles):
    out = list(range(7))
    for cycle in cycles:
        for index, item in enumerate(cycle):
            out[item] = cycle[(index + 1) % len(cycle)]
    return tuple(out)


def act(perm, label):
    missing, matching = label
    return (perm[missing],
            frozenset(frozenset(perm[x] for x in pair) for pair in matching))


def orbit_profile(generators):
    seen = set()
    profile = {}
    for label in labels:
        if label in seen:
            continue
        component = {label}
        stack = [label]
        while stack:
            current = stack.pop()
            for generator in generators:
                image = act(generator, current)
                if image not in component:
                    component.add(image)
                    stack.append(image)
        seen.update(component)
        profile[len(component)] = profile.get(len(component), 0) + 1
    return len(profile) and sum(profile.values()), profile


cases = {
    "o0b_d_sign": ([make_perm(((2, 3), (4, 5)))], (57, {1: 9, 2: 48})),
    "o0a_universal": ([make_perm(((0, 1),)), make_perm(((3, 4),))],
                      (36, {1: 3, 2: 15, 4: 18})),
    "o0b_identical_pair": ([make_perm(((2, 3),))], (60, {1: 15, 2: 45})),
    "o0b_s0_role": ([make_perm(((0, 1), (2, 4), (3, 5)))],
                    (56, {1: 7, 2: 49})),
    "o0b_s0_both": ([make_perm(((0, 1), (2, 4), (3, 5))),
                      make_perm(((2, 3), (4, 5)))],
                     (32, {1: 3, 2: 7, 4: 22})),
}
for name, (generators, expected) in cases.items():
    got = orbit_profile(generators)
    require(got == expected, "label orbit census: " + name)
    require(sum(size * count for size, count in got[1].items()) == 105,
            "weighted label census: " + name)


# Exact full-system incidence obstruction under every outside-role permutation.
A0 = matrix(ZZ, [[0, 3, 1], [3, 0, 1], [1, 1, 2]])
A1 = matrix(ZZ, [[0, 2, 2], [2, 1, 1], [2, 1, 1]])
isomorphisms = 0
for perm in permutations(range(3)):
    Pm = matrix(ZZ, 3, 3, lambda i, j: ZZ(perm[i] == j))
    isomorphisms += ZZ(Pm * A1 * Pm.transpose() == A0)
require(isomorphisms == 0, "outside incidence transport obstruction")


conditional_candidate_abstract_label_orbit_workload = (
    0 + 2 * 15 * 4 * 60 + 2 * 6 * 4 * 57 + 2 * 3 * 4 * 57
)
require(
    conditional_candidate_abstract_label_orbit_workload == 11304,
    "conditional candidate abstract-label-orbit workload arithmetic",
)
require(360 * 105 == 37800, "split raw labels")
require(16 * 105 == 1680 and 32 * 105 == 3360, "repeated raw labels")
require(37800 + 1680 + 3360 == 42840, "O0b residual total")
require(B_STAR - U_PAID == EXPECTED_RESERVE, "joint unpaid reserve")


print(json.dumps({
    "status": "PASS_ROUTE_CUT_NOT_PAYMENT",
    "field": int(P),
    "routes": int(len(routes)),
    "raw_closed": int(len(CLOSED)),
    "remaining": int(len(routes) - len(CLOSED)),
    "diagonal_involutions": int(total),
    "o0b_raw_labels": int(42840),
    "conditional_candidate_abstract_label_orbit_workload": int(
        conditional_candidate_abstract_label_orbit_workload
    ),
    "conditional_workload_is_census": False,
    "conditional_workload_is_elimination": False,
    "conditional_workload_is_payment": False,
    "U_K3_allocation": None,
}, sort_keys=True))
