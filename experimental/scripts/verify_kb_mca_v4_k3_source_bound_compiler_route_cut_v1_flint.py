#!/usr/bin/env python3
"""Independent python-flint replay of K3 route-cut integer/matrix data.

The exact 11,304 arithmetic is a conditional candidate abstract-label-orbit
workload only.  It is not a census, elimination, or payment.
"""

from itertools import permutations
import json

from flint import fmpz, fmpz_mat


def require(condition, message):
    if not condition:
        raise AssertionError(message)


P = fmpz(2_130_706_433)
B_STAR = fmpz(274_980_728_111_395_087)
U_PAID = fmpz(981_104)
RESERVE = fmpz(274_980_728_110_413_983)

require(P % 2 == 1, "odd characteristic")
require((fmpz(1) - (P - 1)) % P != 0, "+1 and -1 differ")
require(B_STAR - U_PAID == RESERVE, "joint reserve")

A0 = fmpz_mat([[0, 3, 1], [3, 0, 1], [1, 1, 2]])
A1 = fmpz_mat([[0, 2, 2], [2, 1, 1], [2, 1, 1]])
matches = 0
for perm in permutations(range(3)):
    Pm = fmpz_mat(3, 3)
    for i, j in enumerate(perm):
        Pm[i, j] = 1
    if Pm * A1 * Pm.transpose() == A0:
        matches += 1
require(matches == 0, "outside incidence matrices are not permutation-isomorphic")

split_raw = fmpz(6) * 15 * 4 * 105
rep12 = fmpz(16) * 105
rep1114 = fmpz(32) * 105
total = split_raw + rep12 + rep1114
conditional_candidate_abstract_label_orbit_workload = (
    fmpz(2) * 15 * 4 * 60
    + fmpz(2) * 6 * 4 * 57
    + fmpz(2) * 3 * 4 * 57
)
require(split_raw == 37800, "split raw")
require(rep12 == 1680 and rep1114 == 3360, "repeated raw")
require(total == 42840, "O0b total")
require(
    conditional_candidate_abstract_label_orbit_workload == 11304,
    "conditional candidate abstract-label-orbit workload arithmetic",
)

print(json.dumps({
    "status": "FLINT_PASS_ROUTE_CUT_NOT_PAYMENT",
    "permutations_checked": 6,
    "incidence_isomorphisms": matches,
    "o0b_raw_labels": int(total),
    "conditional_candidate_abstract_label_orbit_workload": int(
        conditional_candidate_abstract_label_orbit_workload
    ),
    "conditional_workload_is_census": False,
    "conditional_workload_is_elimination": False,
    "conditional_workload_is_payment": False,
    "joint_unpaid_reserve": int(RESERVE),
    "joint_reserve_is_K3_allocation": False,
}, sort_keys=True))
