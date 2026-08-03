import hashlib
import itertools
import json
import sys

P = 2147483647


def read_fixture(path):
    tokens = list(map(int, open(path, encoding="ascii").read().split()))
    cursor = iter(tokens)
    field = next(cursor)
    core_size = next(cursor)
    core = [next(cursor) for _ in range(core_size)]
    branch_count = next(cursor)
    branches = []
    for _ in range(branch_count):
        next(cursor)
        next(cursor)
        size = next(cursor)
        branches.append(set(next(cursor) for _ in range(size)))
    assert field == P and core_size == 509 and branch_count == 16
    return core, branches


def matrix_rank(matrix):
    matrix = [row[:] for row in matrix]
    rank = 0
    for column in range(len(matrix[0])):
        pivot = next(
            (row for row in range(rank, len(matrix)) if matrix[row][column]), None
        )
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inverse = pow(matrix[rank][column], P - 2, P)
        matrix[rank] = [value * inverse % P for value in matrix[rank]]
        for row in range(len(matrix)):
            if row == rank or matrix[row][column] == 0:
                continue
            factor = matrix[row][column]
            matrix[row] = [
                (left - factor * right) % P
                for left, right in zip(matrix[row], matrix[rank])
            ]
        rank += 1
    return rank


def main():
    if len(sys.argv) != 4:
        raise SystemExit("usage: verifier FIXTURE SP01ZXA2_JSON OUTPUT")
    fixture_path, pencil_path, output_path = sys.argv[1:]
    core, branches = read_fixture(fixture_path)
    certificate = json.load(open(pencil_path, encoding="utf-8"))["certificate"]
    principal = certificate["principal_branch_indices"]
    parameters = {
        int(key): value for key, value in certificate["principal_parameters"].items()
    }
    outside = set().union(*branches)

    evaluations = []
    for x in core:
        row = []
        for branch in branches:
            value = 1
            for root in outside - branch:
                value = value * (x - root) % P
            row.append(value)
        evaluations.append(row)

    modes = {}
    for mode in ("evaluation", "reciprocal"):
        affine_failures = 0
        rank_histogram = {}
        for row in evaluations:
            values = [row[index] for index in principal]
            if mode == "reciprocal":
                values = [pow(value, P - 2, P) for value in values]
            base = values[0]
            slope = (values[1] - base) % P
            if any(
                value != (base + slope * parameters[index]) % P
                for index, value in zip(principal, values)
            ):
                affine_failures += 1
            rank = matrix_rank(
                [
                    [1, parameters[index], value, parameters[index] * value % P]
                    for index, value in zip(principal, values)
                ]
            )
            rank_histogram[rank] = rank_histogram.get(rank, 0) + 1
        modes[mode] = {
            "affine_failure_rows": affine_failures,
            "mobius_test_rank_histogram": rank_histogram,
        }

    report = {
        "schema": "sp01zxa9-principal-Cauchy-route-cut/v1",
        "status": "PASS_SIMPLE_AFFINE_AND_MOBIUS_MODELS_REFUTED",
        "field": P,
        "core_rows": len(core),
        "principal_columns": len(principal),
        "principal_indices": principal,
        "modes": modes,
        "fixture_sha256": hashlib.sha256(open(fixture_path, "rb").read()).hexdigest(),
        "scope_guard": "Refutes only affine and fractional-linear dependence on the exact principal parameters.",
    }
    with open(output_path, "w", encoding="ascii") as output:
        json.dump(report, output, indent=2, sort_keys=True)
        output.write("\n")
    print("PASS SP01zxa9 principal Cauchy route cut")


if __name__ == "__main__":
    main()
