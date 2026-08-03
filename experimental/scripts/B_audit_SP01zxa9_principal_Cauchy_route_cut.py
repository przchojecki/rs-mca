import itertools
import json
import sys

P = 2147483647


def determinant(matrix):
    matrix = [row[:] for row in matrix]
    answer = 1
    for column in range(len(matrix)):
        pivot = next(
            (row for row in range(column, len(matrix)) if matrix[row][column]), None
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
            factor = matrix[row][column] * inverse % P
            for entry in range(column, len(matrix)):
                matrix[row][entry] = (
                    matrix[row][entry] - factor * matrix[column][entry]
                ) % P
    return answer % P


def main():
    if len(sys.argv) != 4:
        raise SystemExit("usage: auditor FIXTURE SP01ZXA2_JSON OUTPUT")
    fixture_path, pencil_path, output_path = sys.argv[1:]
    tokens = list(map(int, open(fixture_path, encoding="ascii").read().split()))
    cursor = iter(tokens)
    assert next(cursor) == P
    core = [next(cursor) for _ in range(next(cursor))]
    branch_count = next(cursor)
    branches = []
    for _ in range(branch_count):
        next(cursor)
        next(cursor)
        branches.append(set(next(cursor) for _ in range(next(cursor))))
    data = json.load(open(pencil_path, encoding="utf-8"))["certificate"]
    principal = data["principal_branch_indices"]
    parameter = {int(key): value for key, value in data["principal_parameters"].items()}
    outside = sorted(set().union(*branches))

    witnesses = {"evaluation": [], "reciprocal": []}
    for core_index, x in enumerate(core):
        values = []
        for branch_index in principal:
            value = 1
            branch = branches[branch_index]
            for root in outside:
                if root not in branch:
                    value = value * (x - root) % P
            values.append(value)
        for mode in witnesses:
            active = values if mode == "evaluation" else [pow(value, P - 2, P) for value in values]
            rows = [
                [1, parameter[index], value, parameter[index] * value % P]
                for index, value in zip(principal, active)
            ]
            witness = None
            for selected in itertools.combinations(range(len(principal)), 4):
                if determinant([rows[index] for index in selected]) != 0:
                    witness = [principal[index] for index in selected]
                    break
            if witness is None:
                raise RuntimeError(f"Mobius rank below four at row {core_index}, mode {mode}")
            witnesses[mode].append(witness)

    report = {
        "schema": "sp01zxa9-independent-Cauchy-route-cut-audit/v1",
        "status": "PASS_INDEPENDENT_NONZERO_MINOR_WITNESSES_ALL_ROWS",
        "core_rows": len(core),
        "evaluation_witness_rows": len(witnesses["evaluation"]),
        "reciprocal_witness_rows": len(witnesses["reciprocal"]),
        "first_evaluation_witness": witnesses["evaluation"][0],
        "first_reciprocal_witness": witnesses["reciprocal"][0],
        "scope_guard": "Nonzero 4-by-4 minors refute only the simple Mobius model.",
    }
    with open(output_path, "w", encoding="ascii") as output:
        json.dump(report, output, indent=2, sort_keys=True)
        output.write("\n")
    print("PASS independent SP01zxa9 Cauchy route-cut audit")


if __name__ == "__main__":
    main()
