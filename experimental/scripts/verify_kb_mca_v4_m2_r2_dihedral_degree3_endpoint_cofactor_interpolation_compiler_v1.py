#!/usr/bin/env python3
"""Verify the KoalaBear cubic endpoint-cofactor interpolation compiler."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any, Callable

if not __debug__:
    raise RuntimeError("verifier refuses optimized Python execution")


class VerificationError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


EXPERIMENTAL = Path(__file__).resolve().parents[1]
REPO_ROOT = EXPERIMENTAL.parent
CERTIFICATE = (
    EXPERIMENTAL
    / "data/certificates/kb-mca-v4-m2-r2-dihedral-degree3-endpoint-cofactor-interpolation-compiler-v1"
    / "kb_mca_v4_m2_r2_dihedral_degree3_endpoint_cofactor_interpolation_compiler_v1.json"
)
PARENT = {
    "commit": "fce150e3323ce37f261b21c19685f4613552dd42",
    "certificate_path": "experimental/data/certificates/kb-mca-v4-m2-r2-dihedral-degree3-geometric-realization-fence-v1/kb_mca_v4_m2_r2_dihedral_degree3_geometric_realization_fence_v1.json",
    "certificate_blob_oid": "7adf13b9e343c51d96cdc7c8878cf5bba15c618c",
    "certificate_payload_sha256": "a7f42b038261ea137b2246987dcc398bdddbf807ede6ff46f70429d5a44b2be5",
    "imported_terminal": "M2_R2_DIHEDRAL_DEGREE3_GEOMETRIC_REALIZATION_FENCE",
}
P = 47
ALPHAS = [5, 10, 17, 19, 21, 23, 24, 26, 28, 30, 37, 42]
X_ROOTS = [3, 6, 8, 11, 12, 13, 14, 15, 16, 18, 20, 21,
           26, 27, 29, 31, 32, 33, 34, 35, 36, 39, 41, 44]
OWNED = [
    [32, 31], [11, 36], [6, 41], [16, 33],
    [3, 39], [12, 35], [18, 29], [34, 14],
    [20, 27], [44, 13], [21, 26], [15, 8],
]
INVARIANT = {1, 2, 5, 6, 8, 10}


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def payload_hash(value: dict[str, Any]) -> str:
    unhashed = copy.deepcopy(value)
    unhashed.pop("payload_sha256", None)
    return hashlib.sha256(canonical_json(unhashed).encode()).hexdigest()


def reject_duplicates(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise VerificationError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def parse_json(text: str, label: str) -> dict[str, Any]:
    try:
        value = json.loads(text, object_pairs_hook=reject_duplicates)
    except (json.JSONDecodeError, VerificationError) as error:
        raise VerificationError(f"cannot parse {label}: {error}") from error
    require(isinstance(value, dict), f"{label} is not an object")
    return value


def git_output(*args: str) -> str:
    try:
        result = subprocess.run(
            ["git", *args], cwd=REPO_ROOT, check=True, capture_output=True, text=True
        )
    except subprocess.CalledProcessError as error:
        raise VerificationError(error.stderr.strip()) from error
    return result.stdout.strip()


def verify_parent() -> None:
    path = PARENT["certificate_path"]
    require(git_output("rev-parse", f"{PARENT['commit']}:{path}") == PARENT["certificate_blob_oid"],
            "parent blob")
    data = parse_json(git_output("show", f"{PARENT['commit']}:{path}"), path)
    require(data.get("payload_sha256") == PARENT["certificate_payload_sha256"], "parent payload")
    require(payload_hash(data) == data.get("payload_sha256"), "parent seal")
    require(data.get("conclusion", {}).get("terminal") == PARENT["imported_terminal"], "parent terminal")


def inverse(value: int) -> int:
    require(value % P != 0, "modular inverse")
    return pow(value % P, P - 2, P)


def poly_mul(left: list[int], right: list[int]) -> list[int]:
    result = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] = (result[i + j] + a * b) % P
    return result


def root_poly(roots: list[int]) -> list[int]:
    result = [1]
    for root in roots:
        result = poly_mul(result, [-root % P, 1])
    return result


def divide_linear(poly: list[int], root: int) -> list[int]:
    quotient = [0] * (len(poly) - 1)
    quotient[-1] = poly[-1]
    for degree in range(len(quotient) - 1, 0, -1):
        quotient[degree - 1] = (poly[degree] + root * quotient[degree]) % P
    require((poly[0] + root * quotient[0]) % P == 0, "exact linear division")
    return quotient


def divide_roots(poly: list[int], roots: list[int]) -> list[int]:
    result = poly
    for root in roots:
        result = divide_linear(result, root)
    return result


def evaluate(poly: list[int], value: int) -> int:
    result = 0
    for coefficient in reversed(poly):
        result = (result * value + coefficient) % P
    return result


def phi(value: int) -> int:
    denominator = (value * value - 1) % P
    require(denominator != 0, "phi pole")
    numerator = (value * value + 2) * (2 * value**4 - 10 * value * value - 1)
    return numerator * inverse(denominator**3) % P


def psi(value: int) -> int:
    return 2 * inverse(value * value + 1) % P


def component_poly(alpha: int) -> list[int]:
    return [
        (1 + 2 * alpha * alpha) % P,
        (-6 * alpha) % P,
        (2 + 2 * alpha * alpha) % P,
        (-2 * alpha) % P,
        1,
    ]


def matrix_rank(matrix: list[list[int]]) -> tuple[int, list[list[int]], list[int]]:
    rows = [row[:] for row in matrix]
    rank = 0
    pivots: list[int] = []
    for column in range(len(rows[0])):
        pivot = next((row for row in range(rank, len(rows)) if rows[row][column] % P), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        scale = inverse(rows[rank][column])
        rows[rank] = [(scale * value) % P for value in rows[rank]]
        for row in range(len(rows)):
            if row == rank or rows[row][column] == 0:
                continue
            scale = rows[row][column]
            rows[row] = [
                (value - scale * pivot_value) % P
                for value, pivot_value in zip(rows[row], rows[rank])
            ]
        pivots.append(column)
        rank += 1
    return rank, rows, pivots


def determinant(matrix: list[list[int]]) -> int:
    rows = [row[:] for row in matrix]
    result = 1
    for column in range(len(rows)):
        pivot = next((row for row in range(column, len(rows)) if rows[row][column] % P), None)
        require(pivot is not None, "nonsingular pinned minor")
        if pivot != column:
            rows[column], rows[pivot] = rows[pivot], rows[column]
            result = -result
        value = rows[column][column] % P
        result = result * value % P
        scale = inverse(value)
        for row in range(column + 1, len(rows)):
            factor = rows[row][column] * scale % P
            for entry in range(column, len(rows)):
                rows[row][entry] = (rows[row][entry] - factor * rows[column][entry]) % P
    return result % P


def exact_replay() -> dict[str, Any]:
    locator = root_poly(ALPHAS)
    source_sum = sum(ALPHAS) % P
    for index, alpha in enumerate(ALPHAS):
        quotient = divide_linear(locator, alpha)
        derivative = 1
        for other_index, other in enumerate(ALPHAS):
            if other_index != index:
                derivative = derivative * (alpha - other) % P
        lagrange = [coefficient * inverse(derivative) % P for coefficient in quotient]
        for other_index, other in enumerate(ALPHAS):
            require(evaluate(lagrange, other) == int(index == other_index), "Lagrange evaluation")
        require(lagrange[11] == inverse(derivative), "T11 coefficient")
        require(lagrange[10] == (alpha - source_sum) * inverse(derivative) % P,
                "T10 coefficient")

    require([alpha for alpha in ALPHAS if phi(alpha) == 7] == [5, 17, 21, 26, 30, 42],
            "first cubic fiber")
    require([alpha for alpha in ALPHAS if phi(alpha) == 18] == [10, 19, 23, 24, 28, 37],
            "second cubic fiber")
    complete_roots = []
    for value in range(P):
        if (value * value + 1) % P == 0:
            continue
        image = psi(value)
        if (image * image - 1) % P != 0 and phi(image) in (7, 18):
            complete_roots.append(value)
    require(complete_roots == X_ROOTS, "complete source roots")

    stars: dict[int, list[int]] = {}
    star_roots: list[list[int]] = [[] for _ in ALPHAS]
    for root in X_ROOTS:
        labels = [index for index, alpha in enumerate(ALPHAS)
                  if evaluate(component_poly(alpha), root) == 0]
        require(len(labels) == 2, "star size")
        stars[root] = labels
        for label in labels:
            star_roots[label].append(root)
    require(all(len(roots) == 4 for roots in star_roots), "quartic stars")
    require(sorted(sum(OWNED, [])) == X_ROOTS, "locator partition")
    for label, roots in enumerate(OWNED):
        require(not set(roots) & set(star_roots[label]), "locator avoidance")

    fibers = {label: sorted(root for root in X_ROOTS if psi(root) == alpha)
              for label, alpha in enumerate(ALPHAS)}
    invariant = {label for label, roots in enumerate(OWNED)
                 if roots[0] + roots[1] == P and psi(roots[0]) == psi(roots[1])}
    require(invariant == INVARIANT, "invariant set")
    sigma = {owner: next(label for label, roots in fibers.items() if sorted(OWNED[owner]) == roots)
             for owner in INVARIANT}
    expected_sigma = {1: 10, 2: 8, 5: 6, 6: 5, 8: 2, 10: 1}
    require(sigma == expected_sigma, "invariant map")

    noninvariant = set(range(12)) - INVARIANT
    right_degrees = {label: 0 for label in noninvariant}
    for owner in noninvariant:
        targets = [next(label for label, roots in fibers.items() if root in roots) for root in OWNED[owner]]
        require(len(set(targets)) == 2 and set(targets) <= noninvariant, "simple pole graph")
        for target in targets:
            right_degrees[target] += 1
    require(set(right_degrees.values()) == {2}, "two-regular pole graph")
    color_count = sum(owner in stars[-root % P] for owner in noninvariant for root in OWNED[owner])
    require(color_count == 4, "component edge count")

    complete = root_poly(X_ROOTS)
    cofactors = []
    for label in range(12):
        require(component_poly(ALPHAS[label]) == root_poly(star_roots[label]), "component quartic")
        cofactors.append(divide_roots(complete, star_roots[label] + OWNED[label]))
    first = [[cofactors[column][row] for column in range(12)] for row in range(19)]
    second = [[ALPHAS[column] * cofactors[column][row] % P for column in range(12)]
              for row in range(19)]
    rank_first, reduced, pivots = matrix_rank(first)
    require(rank_first == 11, "first rank")
    free = next(column for column in range(12) if column not in pivots)
    kernel = [0] * 12
    kernel[free] = 1
    for row, pivot in enumerate(pivots):
        kernel[pivot] = -reduced[row][free] % P
    stacked = first + second
    require(matrix_rank(stacked)[0] == 12, "stacked rank")
    selected = list(range(11)) + [19]
    minor = determinant([stacked[row] for row in selected])
    require(minor == 7, "pinned determinant")

    owner_by_root = {
        root: owner
        for owner, roots in enumerate(OWNED)
        for root in roots
    }
    edge_root = {frozenset(labels): root for root, labels in stars.items()}
    require(len(edge_root) == 24, "distinct star edges")

    def transport(source: int, target: int) -> int:
        root = edge_root[frozenset((source, target))]
        owner = owner_by_root[root]
        require(owner not in (source, target), "transport locator avoidance")
        numerator = (
            -(ALPHAS[source] - ALPHAS[owner])
            * evaluate(cofactors[source], root)
        ) % P
        denominator = (
            (ALPHAS[target] - ALPHAS[owner])
            * evaluate(cofactors[target], root)
        ) % P
        require(numerator != 0 and denominator != 0, "nonzero edge transport")
        return numerator * inverse(denominator) % P

    square_holonomies = []
    for component in (
        [(0, 11), (2, 9), (4, 7)],
        [(1, 10), (3, 8), (5, 6)],
    ):
        for first_part, second_part in (
            (component[0], component[1]),
            (component[0], component[2]),
            (component[1], component[2]),
        ):
            cycle = [
                first_part[0], second_part[0],
                first_part[1], second_part[1],
            ]
            product = 1
            for index, source in enumerate(cycle):
                product = product * transport(source, cycle[(index + 1) % 4]) % P
            square_holonomies.append(product)
    require(square_holonomies == [11, 26, 17, 2, 41, 31],
            "canonical square holonomies")
    require(all(value != 1 for value in square_holonomies),
            "nonidentity square holonomies")
    return {
        "field": P,
        "cubic_pole_values": [7, 18],
        "source_labels": ALPHAS,
        "complete_source_roots": X_ROOTS,
        "locator_roots": OWNED,
        "invariant_labels": sorted(INVARIANT),
        "invariant_fiber_map": {str(key): value for key, value in sorted(sigma.items())},
        "noninvariant_pole_graph_degrees": {str(key): value for key, value in sorted(right_degrees.items())},
        "component_color_edge_count": color_count,
        "first_block_rank": rank_first,
        "first_block_kernel": kernel,
        "stacked_rank": 12,
        "minor_rows": selected,
        "minor_determinant": minor,
        "canonical_square_holonomies": square_holonomies,
        "all_canonical_squares_nonidentity": True,
    }


def build_certificate() -> dict[str, Any]:
    data = {
        "schema": "kb-mca-v4-m2-r2-dihedral-degree3-endpoint-cofactor-interpolation-compiler-v1",
        "parent_geometric_fence": PARENT,
        "interpolation": {
            "endpoint_form": "M(T,X)=sum_i kappa_i*L_i(T)*B(X)/z_i(X)",
            "cofactor_fibers": "E_i(X)=B(X)/(z_i(X)*H(alpha_i,X))",
            "matrix_shape": [38, 12],
            "kernel_equations": ["sum_i w_i*E_i=0", "sum_i alpha_i*w_i*E_i=0"],
            "support_requirement": "all twelve w_i are nonzero",
            "equivalence": "H divides M iff the stacked matrix has a full-support kernel",
            "star_transport": "rho_(a->b)(x)=-((alpha_a-alpha_c)E_a(x))/((alpha_b-alpha_c)E_b(x))",
            "cycle_gate": "every directed star cycle has transport product one",
            "gain_multigraph": "for every root x and ordered u,v in S_x, use the third label r in rho^x_(u->v)",
            "flatness_equivalence": "the full-support kernel exists iff every closed gain-graph walk has product one",
        },
        "fixture": exact_replay(),
        "conclusion": {
            "terminal": "M2_R2_DIHEDRAL_DEGREE3_ENDPOINT_COFACTOR_INTERPOLATION_COMPILER",
            "deleted_fixture": True,
            "row_status": "OPEN",
            "next_gate": "prove complete gain-graph nonflatness or exclude full-support kernels for every admissible s=6 ownership, or reconstruct an actual owner",
        },
        "nonclaims": [
            "no universal locator-ownership holonomy or rank exclusion",
            "no deployed endpoint-record deletion",
            "no carrier, data, explaining-polynomial, or slope owner",
            "no payment, K3, KoalaBear, endpoint, or Prize close",
        ],
    }
    data["payload_sha256"] = payload_hash(data)
    return data


def verify_certificate(data: dict[str, Any], verify_parents: bool) -> None:
    require(data.get("schema") == "kb-mca-v4-m2-r2-dihedral-degree3-endpoint-cofactor-interpolation-compiler-v1", "schema")
    require(data.get("payload_sha256") == payload_hash(data), "payload seal")
    require(data.get("parent_geometric_fence") == PARENT, "parent")
    if verify_parents:
        verify_parent()
    expected = build_certificate()
    for key in ("interpolation", "fixture", "conclusion", "nonclaims"):
        require(data.get(key) == expected[key], key)


def reseal(data: dict[str, Any]) -> None:
    data["payload_sha256"] = payload_hash(data)


def tamper_selftest(original: dict[str, Any]) -> int:
    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("parent", lambda row: row["parent_geometric_fence"].__setitem__("certificate_blob_oid", "0" * 40)),
        ("shape", lambda row: row["interpolation"].__setitem__("matrix_shape", [19, 12])),
        ("equation", lambda row: row["interpolation"]["kernel_equations"].pop()),
        ("support", lambda row: row["interpolation"].__setitem__("support_requirement", "optional")),
        ("equivalence", lambda row: row["interpolation"].__setitem__("equivalence", "necessary only")),
        ("cycle_gate", lambda row: row["interpolation"].__setitem__("cycle_gate", "optional")),
        ("flatness", lambda row: row["interpolation"].__setitem__("flatness_equivalence", "necessary only")),
        ("field", lambda row: row["fixture"].__setitem__("field", 43)),
        ("poles", lambda row: row["fixture"].__setitem__("cubic_pole_values", [7, 19])),
        ("labels", lambda row: row["fixture"]["source_labels"].pop()),
        ("roots", lambda row: row["fixture"]["complete_source_roots"].pop()),
        ("ownership", lambda row: row["fixture"]["locator_roots"][0].reverse()),
        ("invariant", lambda row: row["fixture"]["invariant_labels"].pop()),
        ("sigma", lambda row: row["fixture"]["invariant_fiber_map"].__setitem__("1", 1)),
        ("pole_graph", lambda row: row["fixture"]["noninvariant_pole_graph_degrees"].__setitem__("0", 1)),
        ("color", lambda row: row["fixture"].__setitem__("component_color_edge_count", 3)),
        ("rank1", lambda row: row["fixture"].__setitem__("first_block_rank", 12)),
        ("kernel", lambda row: row["fixture"]["first_block_kernel"].__setitem__(0, 1)),
        ("rank2", lambda row: row["fixture"].__setitem__("stacked_rank", 11)),
        ("minor_rows", lambda row: row["fixture"]["minor_rows"].pop()),
        ("det", lambda row: row["fixture"].__setitem__("minor_determinant", 0)),
        ("holonomy", lambda row: row["fixture"]["canonical_square_holonomies"].__setitem__(0, 1)),
        ("terminal", lambda row: row["conclusion"].__setitem__("terminal", "K3_CLOSED")),
        ("row", lambda row: row["conclusion"].__setitem__("row_status", "CLOSED")),
        ("nonclaim", lambda row: row["nonclaims"].pop()),
    ]
    passed = 0
    for name, mutate in mutations:
        candidate = copy.deepcopy(original)
        mutate(candidate)
        reseal(candidate)
        try:
            verify_certificate(candidate, False)
        except VerificationError:
            passed += 1
        else:
            raise VerificationError(f"tamper survived: {name}")
    bad_hash = copy.deepcopy(original)
    bad_hash["payload_sha256"] = "0" * 64
    try:
        verify_certificate(bad_hash, False)
    except VerificationError:
        passed += 1
    else:
        raise VerificationError("tamper survived: payload")
    try:
        parse_json('{"x":1,"x":2}', "duplicate")
    except VerificationError:
        passed += 1
    else:
        raise VerificationError("duplicate key survived")
    return passed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()
    if not args.write and not args.check and not args.tamper_selftest:
        parser.error("at least one action is required")
    if args.write:
        verify_parent()
        data = build_certificate()
        CERTIFICATE.parent.mkdir(parents=True, exist_ok=True)
        CERTIFICATE.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
        print(f"WROTE: {CERTIFICATE.relative_to(REPO_ROOT)}")
    data = parse_json(CERTIFICATE.read_text(), str(CERTIFICATE))
    verify_certificate(data, True)
    print("PASS: cubic endpoint divisibility is one exact full-support kernel gate")
    if args.tamper_selftest:
        count = tamper_selftest(data)
        print(f"PASS: {count}/{count} tamper mutations rejected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
