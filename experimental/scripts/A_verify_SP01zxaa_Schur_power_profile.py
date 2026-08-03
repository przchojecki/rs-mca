import hashlib
import itertools
import json
import sys


P = 2147483647


def read_fixture(path):
    tokens = iter(map(int, open(path, encoding="ascii").read().split()))
    assert next(tokens) == P
    core = [next(tokens) for _ in range(next(tokens))]
    branch_count = next(tokens)
    branches = []
    for _ in range(branch_count):
        next(tokens)
        next(tokens)
        branches.append({next(tokens) for _ in range(next(tokens))})
    assert len(core) == 509 and branch_count == 16
    return core, branches


def vector_rank(vectors):
    basis = {}
    for source in vectors:
        vector = source[:]
        while True:
            pivot = next((index for index, value in enumerate(vector) if value), None)
            if pivot is None:
                break
            if pivot not in basis:
                inverse = pow(vector[pivot], P - 2, P)
                vector = [value * inverse % P for value in vector]
                basis[pivot] = vector
                break
            factor = vector[pivot]
            vector = [
                (left - factor * right) % P
                for left, right in zip(vector, basis[pivot])
            ]
    return len(basis), sorted(basis)


def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: verifier FIXTURE OUTPUT")
    fixture_path, output_path = sys.argv[1:]
    core, branches = read_fixture(fixture_path)
    universe = set().union(*branches)
    columns = []
    for branch in branches:
        column = []
        for x in core:
            value = 1
            for root in universe - branch:
                value = value * (x - root) % P
            column.append(value)
        columns.append(column)

    profiles = []
    for power in (1, 2, 3):
        index_multisets = list(itertools.combinations_with_replacement(range(16), power))
        vectors = []
        for indices in index_multisets:
            vector = [1] * len(core)
            for index in indices:
                vector = [
                    left * right % P
                    for left, right in zip(vector, columns[index])
                ]
            vectors.append(vector)
        rank, pivots = vector_rank(vectors)
        profiles.append(
            {
                "power": power,
                "monomials": len(vectors),
                "rank": rank,
                "pivot_count": len(pivots),
                "pivot_sha256": hashlib.sha256(
                    b"".join(pivot.to_bytes(2, "big") for pivot in pivots)
                ).hexdigest(),
            }
        )

    assert [profile["rank"] for profile in profiles] == [16, 136, 509]
    report = {
        "schema": "sp01zxaa-Schur-power-profile/v1",
        "status": "PASS_MAXIMAL_SQUARE_AND_FULL_AMBIENT_CUBE",
        "field": P,
        "code_length": len(core),
        "code_dimension": 16,
        "profiles": profiles,
        "GRS_square_dimension_if_applicable": 31,
        "fixture_sha256": hashlib.sha256(open(fixture_path, "rb").read()).hexdigest(),
        "scope_guard": (
            "The maximal Schur-square dimension refutes a generalized "
            "Reed-Solomon or low-product-dimension explanation for this "
            "evaluation code. It does not by itself prove or refute MDS."
        ),
    }
    with open(output_path, "w", encoding="ascii") as output:
        json.dump(report, output, indent=2, sort_keys=True)
        output.write("\n")
    print("PASS SP01zxaa Schur-power profile")


if __name__ == "__main__":
    main()
