import hashlib
import itertools
import json
import sys


P = 2147483647


def parse_fixture(path):
    data = iter(map(int, open(path, encoding="ascii").read().split()))
    assert next(data) == P
    core = [next(data) for _ in range(next(data))]
    branch_count = next(data)
    branches = []
    for _ in range(branch_count):
        next(data)
        next(data)
        branches.append([next(data) for _ in range(next(data))])
    assert len(core) == 509 and branch_count == 16
    return core, branches


def polynomial_from_roots(roots):
    polynomial = [1]
    for root in roots:
        product = [0] * (len(polynomial) + 1)
        for degree, coefficient in enumerate(polynomial):
            product[degree] = (product[degree] - root * coefficient) % P
            product[degree + 1] = (product[degree + 1] + coefficient) % P
        polynomial = product
    return polynomial


def evaluate(polynomial, point):
    value = 0
    for coefficient in reversed(polynomial):
        value = (value * point + coefficient) % P
    return value


def matrix_rank_by_columns(columns):
    basis = {}
    for source in columns:
        vector = source[:]
        while True:
            pivot = next(
                (index for index in range(len(vector) - 1, -1, -1)
                 if vector[index]),
                None,
            )
            if pivot is None:
                break
            if pivot not in basis:
                inverse = pow(vector[pivot], P - 2, P)
                basis[pivot] = [value * inverse % P for value in vector]
                break
            factor = vector[pivot]
            vector = [
                (left - factor * right) % P
                for left, right in zip(vector, basis[pivot])
            ]
    return len(basis)


def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: auditor FIXTURE OUTPUT")
    fixture_path, output_path = sys.argv[1:]
    core, branch_lists = parse_fixture(fixture_path)
    universe = set().union(*map(set, branch_lists))
    polynomials = [
        polynomial_from_roots(universe - set(branch))
        for branch in branch_lists
    ]
    assert {len(polynomial) - 1 for polynomial in polynomials} == {479}
    columns = [
        [evaluate(polynomial, point) for point in core]
        for polynomial in polynomials
    ]

    reports = []
    for power in (1, 2, 3):
        products = []
        for indices in itertools.combinations_with_replacement(range(16), power):
            product = [1] * len(core)
            for index in indices:
                product = [
                    left * right % P
                    for left, right in zip(product, columns[index])
                ]
            products.append(product)
        rank = matrix_rank_by_columns(products)
        reports.append({"power": power, "monomials": len(products), "rank": rank})
    assert [report["rank"] for report in reports] == [16, 136, 509]

    report = {
        "schema": "sp01zxaa-Schur-power-profile-independent-audit/v1",
        "status": "PASS_INDEPENDENT_COEFFICIENT_HORNER_SCHUR_AUDIT",
        "field": P,
        "code_length": len(core),
        "locator_coefficients_constructed": True,
        "evaluation_method": "Horner evaluation of expanded degree-479 locators",
        "profiles": reports,
        "profile_sha256": hashlib.sha256(
            json.dumps(reports, sort_keys=True).encode("ascii")
        ).hexdigest(),
        "scope_guard": (
            "This is a code-invariant route cut, not a proof of full-spark "
            "or complete affine-hull rigidity."
        ),
    }
    with open(output_path, "w", encoding="ascii") as output:
        json.dump(report, output, indent=2, sort_keys=True)
        output.write("\n")
    print("PASS independent SP01zxaa Schur-power audit")


if __name__ == "__main__":
    main()
