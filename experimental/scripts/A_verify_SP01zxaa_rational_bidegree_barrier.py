import hashlib
import json
import sys


P = 2147483647
BOUNDARY_TOTAL_DEGREE = 12


def read_fixture(path):
    tokens = iter(map(int, open(path, encoding="ascii").read().split()))
    field = next(tokens)
    core_size = next(tokens)
    core = [next(tokens) for _ in range(core_size)]
    branch_count = next(tokens)
    branches = []
    for _ in range(branch_count):
        next(tokens)
        next(tokens)
        size = next(tokens)
        branches.append(set(next(tokens) for _ in range(size)))
    assert field == P and core_size == 509 and branch_count == 16
    return core, branches


def determinant(matrix):
    matrix = [row[:] for row in matrix]
    answer = 1
    for column in range(len(matrix)):
        pivot = next(
            (row for row in range(column, len(matrix)) if matrix[row][column]),
            None,
        )
        if pivot is None:
            return 0
        if pivot != column:
            matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
            answer = -answer
        value = matrix[column][column]
        answer = answer * value % P
        inverse = pow(value, P - 2, P)
        for row in range(column + 1, len(matrix)):
            if matrix[row][column] == 0:
                continue
            factor = matrix[row][column] * inverse % P
            for local_column in range(column, len(matrix)):
                matrix[row][local_column] = (
                    matrix[row][local_column]
                    - factor * matrix[column][local_column]
                ) % P
    return answer % P


def alternant_matrix(parameters, values, numerator_degree, denominator_degree):
    matrix = []
    maximum_degree = max(numerator_degree, denominator_degree)
    for parameter, value in zip(parameters, values):
        powers = [1]
        for _ in range(maximum_degree):
            powers.append(powers[-1] * parameter % P)
        matrix.append(
            powers[: numerator_degree + 1]
            + [value * power % P for power in powers[: denominator_degree + 1]]
        )
    return matrix


def main():
    if len(sys.argv) != 4:
        raise SystemExit("usage: verifier FIXTURE SP01ZXA2_JSON OUTPUT")
    fixture_path, pencil_path, output_path = sys.argv[1:]
    core, branches = read_fixture(fixture_path)
    certificate = json.load(open(pencil_path, encoding="utf-8"))["certificate"]
    principal = certificate["principal_branch_indices"]
    parameter_map = {
        int(key): value
        for key, value in certificate["principal_parameters"].items()
    }
    parameters = [parameter_map[index] for index in principal]
    assert len(principal) == 14 and len(set(parameters)) == 14

    outside = set().union(*branches)
    evaluations = []
    for x in core:
        row = []
        for index in principal:
            value = 1
            for root in outside - branches[index]:
                value = value * (x - root) % P
            assert value
            row.append(value)
        evaluations.append(row)

    modes = {}
    for mode in ("evaluation", "reciprocal"):
        boundary = []
        for numerator_degree in range(BOUNDARY_TOTAL_DEGREE + 1):
            denominator_degree = BOUNDARY_TOTAL_DEGREE - numerator_degree
            determinant_product = 1
            digest = hashlib.sha256()
            nonzero = 0
            for row in evaluations:
                values = row
                if mode == "reciprocal":
                    values = [pow(value, P - 2, P) for value in row]
                value = determinant(
                    alternant_matrix(
                        parameters,
                        values,
                        numerator_degree,
                        denominator_degree,
                    )
                )
                if value:
                    nonzero += 1
                determinant_product = determinant_product * value % P
                digest.update(value.to_bytes(4, "big"))
            assert nonzero == len(core)
            boundary.append(
                {
                    "numerator_degree": numerator_degree,
                    "denominator_degree": denominator_degree,
                    "nonzero_determinants": nonzero,
                    "determinant_product": determinant_product,
                    "determinant_sequence_sha256": digest.hexdigest(),
                }
            )
        modes[mode] = boundary

    report = {
        "schema": "sp01zxaa-rational-bidegree-barrier/v1",
        "status": "PASS_NO_ROW_HAS_RATIONAL_TYPE_A_PLUS_B_AT_MOST_12",
        "field": P,
        "core_rows": len(core),
        "principal_columns": len(principal),
        "principal_indices": principal,
        "boundary_total_degree": BOUNDARY_TOTAL_DEGREE,
        "boundary_pairs_per_mode": BOUNDARY_TOTAL_DEGREE + 1,
        "determinants_checked": 2 * len(core) * (BOUNDARY_TOTAL_DEGREE + 1),
        "modes": modes,
        "fixture_sha256": hashlib.sha256(open(fixture_path, "rb").read()).hexdigest(),
        "pencil_sha256": hashlib.sha256(open(pencil_path, "rb").read()).hexdigest(),
        "scope_guard": (
            "Rules out row-wise rational representations P_a(t)/Q_b(t) "
            "for a+b<=12 in evaluation and reciprocal modes. It does not "
            "rule out the dimension-forced a+b>=13 range or row-coupled laws."
        ),
    }
    with open(output_path, "w", encoding="ascii") as output:
        json.dump(report, output, indent=2, sort_keys=True)
        output.write("\n")
    print("PASS SP01zxaa rational bidegree barrier")


if __name__ == "__main__":
    main()
