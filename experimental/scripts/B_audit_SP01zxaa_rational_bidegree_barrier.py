import hashlib
import json
import sys


P = 2147483647
TOTAL = 12


def parse_fixture(path):
    data = iter(map(int, open(path, encoding="ascii").read().split()))
    assert next(data) == P
    core = [next(data) for _ in range(next(data))]
    branch_count = next(data)
    coefficients = []
    branches = []
    for _ in range(branch_count):
        coefficients.append((next(data), next(data)))
        branches.append({next(data) for _ in range(next(data))})
    assert len(core) == 509 and branch_count == 16
    return core, coefficients, branches


def rank(matrix):
    matrix = [row[:] for row in matrix]
    row = 0
    for column in range(len(matrix[0])):
        pivot = next(
            (candidate for candidate in range(row, len(matrix))
             if matrix[candidate][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[row], matrix[pivot] = matrix[pivot], matrix[row]
        inverse = pow(matrix[row][column], P - 2, P)
        matrix[row] = [entry * inverse % P for entry in matrix[row]]
        for candidate in range(len(matrix)):
            if candidate == row or matrix[candidate][column] == 0:
                continue
            factor = matrix[candidate][column]
            matrix[candidate] = [
                (left - factor * right) % P
                for left, right in zip(matrix[candidate], matrix[row])
            ]
        row += 1
    return row


def columns(parameter, value, left_degree, right_degree):
    powers = [1]
    for _ in range(max(left_degree, right_degree)):
        powers.append(powers[-1] * parameter % P)
    return (
        powers[: left_degree + 1]
        + [value * power % P for power in powers[: right_degree + 1]]
    )


def main():
    if len(sys.argv) != 4:
        raise SystemExit("usage: auditor FIXTURE SP01ZXA2_JSON OUTPUT")
    fixture_path, pencil_path, output_path = sys.argv[1:]
    core, coefficients, branches = parse_fixture(fixture_path)
    certificate = json.load(open(pencil_path, encoding="utf-8"))["certificate"]
    principal = certificate["principal_branch_indices"]
    base = certificate["principal_base_coefficients"]
    direction = certificate["principal_direction_coefficients"]
    assert direction[0]
    direction_inverse = pow(direction[0], P - 2, P)

    parameters = []
    for index in principal:
        parameter = (coefficients[index][0] - base[0]) * direction_inverse % P
        assert coefficients[index][1] == (
            base[1] + parameter * direction[1]
        ) % P
        parameters.append(parameter)
    claimed = {
        int(key): value
        for key, value in certificate["principal_parameters"].items()
    }
    assert parameters == [claimed[index] for index in principal]
    assert len(set(parameters)) == 14

    universe = set().union(*branches)
    values_by_row = []
    for x in core:
        global_product = 1
        for root in universe:
            global_product = global_product * (x - root) % P
        row = []
        for index in principal:
            omitted_product = 1
            for root in branches[index]:
                omitted_product = omitted_product * (x - root) % P
            row.append(global_product * pow(omitted_product, P - 2, P) % P)
        values_by_row.append(row)

    mode_reports = {}
    rank_checks = 0
    digest = hashlib.sha256()
    for mode in ("evaluation", "reciprocal"):
        pair_reports = []
        for left_degree in range(TOTAL + 1):
            right_degree = TOTAL - left_degree
            full_rank = 0
            for row in values_by_row:
                values = row if mode == "evaluation" else [
                    pow(value, P - 2, P) for value in row
                ]
                matrix = [
                    columns(parameter, value, left_degree, right_degree)
                    for parameter, value in zip(parameters, values)
                ]
                matrix_rank = rank(matrix)
                digest.update(bytes((left_degree, matrix_rank)))
                full_rank += matrix_rank == 14
                rank_checks += 1
            assert full_rank == len(core)
            pair_reports.append(
                {
                    "left_degree": left_degree,
                    "right_degree": right_degree,
                    "full_rank_rows": full_rank,
                }
            )
        mode_reports[mode] = pair_reports

    report = {
        "schema": "sp01zxaa-rational-bidegree-barrier-independent-audit/v1",
        "status": "PASS_INDEPENDENT_ALTERNANT_RANK_AUDIT",
        "field": P,
        "core_rows": len(core),
        "boundary_total_degree": TOTAL,
        "rank_checks": rank_checks,
        "rank_trace_sha256": digest.hexdigest(),
        "parameters_rederived_from_coefficient_line": True,
        "locator_values_rederived_by_global_product_quotient": True,
        "modes": mode_reports,
        "scope_guard": (
            "Full rank at every a+b=12 boundary pair excludes every lower "
            "bidegree submatrix. Types with a+b>=13 are not excluded."
        ),
    }
    with open(output_path, "w", encoding="ascii") as output:
        json.dump(report, output, indent=2, sort_keys=True)
        output.write("\n")
    print("PASS independent SP01zxaa rational bidegree audit")


if __name__ == "__main__":
    main()
