#!/usr/bin/env python3
"""Search exact GF(11) actual-record collisions with empty global core.

This is campaign scratch, not a release verifier.  We prescribe seven
size-seven maximal supports on the ten-point torus, solve the linear RS
incidence equations, and retain only fixtures with unique degree-<5
explanations, same-support MCA noncontainment, and balanced shifted-lattice
minimum d1=m-k+1=3 at every displayed slope.
"""

from __future__ import annotations

import itertools
import json
import random


P = 11
DOMAIN = tuple(range(1, 11))
K = 5
M = 7
W = M - K
SLOPES = (0, 2, 3, 5, 6, 8, 9)
RNG = random.Random(20260812)


def trim(poly: list[int]) -> tuple[int, ...]:
    out = [x % P for x in poly]
    while out and out[-1] == 0:
        out.pop()
    return tuple(out)


def degree(poly: tuple[int, ...]) -> int:
    return len(poly) - 1


def evaluate(poly: tuple[int, ...], x: int) -> int:
    value = 0
    for coefficient in reversed(poly):
        value = (value * x + coefficient) % P
    return value


def add(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    size = max(len(left), len(right))
    return trim([
        (left[i] if i < len(left) else 0)
        + (right[i] if i < len(right) else 0)
        for i in range(size)
    ])


def scale(poly: tuple[int, ...], scalar: int) -> tuple[int, ...]:
    return trim([scalar * x for x in poly])


def multiply(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    if not left or not right:
        return ()
    out = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            out[i + j] = (out[i + j] + a * b) % P
    return trim(out)


def interpolate(points: tuple[int, ...], values: tuple[int, ...]) -> tuple[int, ...]:
    result: tuple[int, ...] = ()
    for i, (x_i, y_i) in enumerate(zip(points, values)):
        basis = (1,)
        denominator = 1
        for j, x_j in enumerate(points):
            if i == j:
                continue
            basis = multiply(basis, ((-x_j) % P, 1))
            denominator = denominator * (x_i - x_j) % P
        result = add(result, scale(basis, y_i * pow(denominator, -1, P)))
    return result


def rref(matrix: list[list[int]]) -> tuple[list[list[int]], list[int]]:
    a = [[x % P for x in row] for row in matrix]
    pivots: list[int] = []
    row = 0
    for column in range(len(a[0]) if a else 0):
        pivot = next((i for i in range(row, len(a)) if a[i][column]), None)
        if pivot is None:
            continue
        a[row], a[pivot] = a[pivot], a[row]
        inverse = pow(a[row][column], -1, P)
        a[row] = [(inverse * x) % P for x in a[row]]
        for i in range(len(a)):
            if i != row and a[i][column]:
                factor = a[i][column]
                a[i] = [(x - factor * y) % P for x, y in zip(a[i], a[row])]
        pivots.append(column)
        row += 1
        if row == len(a):
            break
    return a, pivots


def nullspace(matrix: list[list[int]], columns: int) -> list[list[int]]:
    reduced, pivots = rref(matrix)
    free = [column for column in range(columns) if column not in pivots]
    basis = []
    for free_column in free:
        vector = [0] * columns
        vector[free_column] = 1
        for row, pivot in enumerate(pivots):
            vector[pivot] = (-reduced[row][free_column]) % P
        basis.append(vector)
    return basis


def matrix_rank(matrix: list[list[int]]) -> int:
    return len(rref(matrix)[1])


def shifted_minimum(word: tuple[int, ...]) -> int:
    for s in range(0, len(DOMAIN) + 1):
        columns = (s + 1) + (s + K)
        matrix = []
        for x, value in zip(DOMAIN, word):
            matrix.append(
                [value * pow(x, j, P) % P for j in range(s + 1)]
                + [(-pow(x, j, P)) % P for j in range(s + K)]
            )
        if matrix_rank(matrix) < columns:
            return s
    raise AssertionError("no shifted minimum")


FIVE_SUBSETS = tuple(itertools.combinations(DOMAIN, K))


def explanations(word: tuple[int, ...]) -> list[tuple[tuple[int, ...], tuple[int, ...]]]:
    found: dict[tuple[int, ...], tuple[int, ...]] = {}
    by_point = dict(zip(DOMAIN, word))
    for seed in FIVE_SUBSETS:
        poly = interpolate(seed, tuple(by_point[x] for x in seed))
        support = tuple(x for x in DOMAIN if evaluate(poly, x) == by_point[x])
        if len(support) >= M:
            found[poly] = support
    return sorted(found.items())


def random_error_sets() -> tuple[tuple[int, ...], ...]:
    # Point 1 is omitted only by support 6 and point 2 only by support 5.
    errors: list[set[int]] = []
    for _ in range(5):
        errors.append(set(RNG.sample(range(3, 11), 3)))
    errors.append({2, *RNG.sample(range(3, 11), 2)})
    errors.append({1, *RNG.sample(range(3, 11), 2)})
    if set().union(*errors) != set(DOMAIN):
        return random_error_sets()
    return tuple(tuple(sorted(error)) for error in errors)


PUBLIC_SUPPORTS = (
    (2, 5, 6, 7, 8, 9, 10),
    (1, 3, 5, 6, 7, 8, 10),
    (1, 2, 3, 4, 8, 9, 10),
    (1, 2, 5, 6, 8, 9, 10),
    (2, 4, 5, 6, 8, 9, 10),
    (1, 3, 5, 7, 8, 9, 10),
    (1, 2, 4, 5, 6, 7, 10),
)


def public_neighbors() -> tuple[tuple[tuple[int, ...], ...], ...]:
    """All one-swap neighbors that remove the fixture's global point 10."""
    out = []
    for index, support in enumerate(PUBLIC_SUPPORTS):
        outside = set(DOMAIN) - set(support)
        for added in sorted(outside):
            changed = [set(item) for item in PUBLIC_SUPPORTS]
            changed[index].remove(10)
            changed[index].add(added)
            if set.intersection(*changed):
                continue
            errors = tuple(tuple(sorted(set(DOMAIN) - item)) for item in changed)
            out.append(errors)
    return tuple(out)


def public_two_swap_neighbors():
    operations = []
    for index, support in enumerate(PUBLIC_SUPPORTS):
        for removed in support:
            for added in sorted(set(DOMAIN) - set(support)):
                operations.append((index, removed, added))
    seen = set()
    for first_index, first in enumerate(operations):
        if first[1] != 10:
            continue
        for second in operations[first_index + 1 :]:
            changed = [set(item) for item in PUBLIC_SUPPORTS]
            valid = True
            for index, removed, added in (first, second):
                if removed not in changed[index] or added in changed[index]:
                    valid = False
                    break
                changed[index].remove(removed)
                changed[index].add(added)
            if not valid or set.intersection(*changed):
                continue
            key = tuple(tuple(sorted(item)) for item in changed)
            if key in seen:
                continue
            seen.add(key)
            yield tuple(tuple(sorted(set(DOMAIN) - item)) for item in changed)


def solve_supports(errors: tuple[tuple[int, ...], ...]) -> dict[str, object] | None:
    supports = tuple(tuple(x for x in DOMAIN if x not in error) for error in errors)
    columns = 2 * len(DOMAIN) + len(SLOPES) * K
    matrix: list[list[int]] = []
    for i, (slope, support) in enumerate(zip(SLOPES, supports)):
        for x in support:
            row = [0] * columns
            row[x - 1] = 1
            row[len(DOMAIN) + x - 1] = slope
            offset = 2 * len(DOMAIN) + i * K
            for j in range(K):
                row[offset + j] = -pow(x, j, P)
            matrix.append(row)
    basis = nullspace(matrix, columns)
    if len(basis) <= 2 * K:
        return None

    for _ in range(300):
        coefficients = [RNG.randrange(P) for _ in basis]
        vector = [sum(c * b[j] for c, b in zip(coefficients, basis)) % P
                  for j in range(columns)]
        u = tuple(vector[: len(DOMAIN)])
        v = tuple(vector[len(DOMAIN) : 2 * len(DOMAIN)])
        if not any(v):
            continue
        records = []
        okay = True
        for i, (slope, expected_support) in enumerate(zip(SLOPES, supports)):
            word = tuple((a + slope * b) % P for a, b in zip(u, v))
            found = explanations(word)
            if len(found) != 1 or found[0][1] != expected_support:
                okay = False
                break
            poly, support = found[0]
            u_poly = interpolate(support, tuple(u[x - 1] for x in support))
            v_poly = interpolate(support, tuple(v[x - 1] for x in support))
            if degree(u_poly) < K and degree(v_poly) < K:
                okay = False
                break
            if shifted_minimum(word) != W + 1:
                okay = False
                break
            records.append({
                "slope": slope,
                "coefficients": list(poly) + [0] * (K - len(poly)),
                "maximal_support": list(support),
                "u_interpolant_degree": degree(u_poly),
                "v_interpolant_degree": degree(v_poly),
                "d1": W + 1,
            })
        if not okay:
            continue

        critical = []
        core_types: set[tuple[int, ...]] = set()
        for indices in itertools.combinations(range(len(SLOPES)), 6):
            core = set(DOMAIN)
            for index in indices:
                core.intersection_update(supports[index])
            if core:
                core_types.add(tuple(sorted(core)))
                critical.append({
                    "slopes": [SLOPES[index] for index in indices],
                    "common_core": sorted(core),
                })
        global_core = set(DOMAIN)
        for support in supports:
            global_core.intersection_update(support)
        if global_core or len(core_types) < 2 or len(critical) < 2:
            continue

        # Reject a global affine explanation block.
        h0 = tuple(records[0]["coefficients"])
        h1 = tuple(records[1]["coefficients"])
        delta = tuple((b - a) % P for a, b in zip(h0, h1))
        if all(tuple((a + slope * d) % P for a, d in zip(h0, delta))
               == tuple(item["coefficients"])
               for slope, item in zip(SLOPES, records)):
            continue
        return {
            "field": P,
            "domain": list(DOMAIN),
            "k": K,
            "m": M,
            "w": W,
            "critical_order": 6,
            "received_line": {"u": list(u), "v": list(v)},
            "explanations": records,
            "critical_records": critical,
            "global_core": [],
        }
    return None


def main() -> None:
    for trial, errors in enumerate(public_neighbors(), 1):
        fixture = solve_supports(errors)
        if fixture is not None:
            fixture["search_trial"] = f"public-one-swap-{trial}"
            print(json.dumps(fixture, sort_keys=True, indent=2))
            return
    print(f"public_neighbors={len(public_neighbors())}: none", flush=True)
    for trial, errors in enumerate(public_two_swap_neighbors(), 1):
        fixture = solve_supports(errors)
        if fixture is not None:
            fixture["search_trial"] = f"public-two-swap-{trial}"
            print(json.dumps(fixture, sort_keys=True, indent=2))
            return
        if trial % 1000 == 0:
            print(f"public_two_swap={trial}", flush=True)
    print("public_two_swap: none", flush=True)
    for trial in range(1, 2001):
        fixture = solve_supports(random_error_sets())
        if fixture is not None:
            fixture["search_trial"] = trial
            print(json.dumps(fixture, sort_keys=True, indent=2))
            return
        if trial % 100 == 0:
            print(f"searched={trial}", flush=True)
    raise SystemExit("no fixture found")


if __name__ == "__main__":
    main()
