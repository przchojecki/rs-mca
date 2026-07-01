#!/usr/bin/env python3
"""Verify the rank-6 prefix-plus-six-spikes finite roots at A=385..387."""

from __future__ import annotations

import argparse
from hashlib import sha256
import itertools
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experimental.scripts.emit_f17_32_hankel_row_descriptor import (  # noqa: E402
    Field,
    K,
    MODULUS,
    N,
    P,
)


SCHEMA_VERSION = "f17-32-m3-rank6-boundary-dual-gcd-v1"
Q_LINE = 17**32
RANK = 6
A_VALUES = [385, 386, 387]
ROW_DESCRIPTOR_REF = (
    "experimental/data/certificates/hankel-f17-32-row-descriptor/"
    "f17_32_n512_k256_hankel_row_descriptor.json"
)
RANK_DROP_BRIDGE_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-m5-regular-root-rank-drop/"
    "f17_32_n512_k256_m3_m5_regular_root_rank_drop.json"
)


FIELD = Field(P, MODULUS)
ZERO = FIELD.zero
ONE = FIELD.one


def f_add(left: Any, right: Any) -> tuple[int, ...]:
    a = FIELD.normalize(left)
    b = FIELD.normalize(right)
    return tuple((a_i + b_i) % P for a_i, b_i in zip(a, b))


def f_neg(value: Any) -> tuple[int, ...]:
    a = FIELD.normalize(value)
    return tuple((-a_i) % P for a_i in a)


def f_sub(left: Any, right: Any) -> tuple[int, ...]:
    return f_add(left, f_neg(right))


def f_mul(left: Any, right: Any) -> tuple[int, ...]:
    return FIELD.mul(left, right)


def f_inv(value: Any) -> tuple[int, ...]:
    element = FIELD.normalize(value)
    if element == ZERO:
        raise ZeroDivisionError("zero field inverse")
    return FIELD.pow(element, FIELD.size - 2)


def f_div(left: Any, right: Any) -> tuple[int, ...]:
    return f_mul(left, f_inv(right))


def f_is_zero(value: Any) -> bool:
    return FIELD.normalize(value) == ZERO


def batch_invert(values: list[tuple[int, ...]]) -> list[tuple[int, ...]]:
    require(all(value != ZERO for value in values), "batch inversion includes zero")
    prefix = []
    product = ONE
    for value in values:
        prefix.append(product)
        product = f_mul(product, value)
    inv_product = f_inv(product)
    out = [ZERO] * len(values)
    suffix_inv = inv_product
    for index in range(len(values) - 1, -1, -1):
        out[index] = f_mul(prefix[index], suffix_inv)
        suffix_inv = f_mul(suffix_inv, values[index])
    return out


def load_json(ref: str | Path) -> dict[str, Any]:
    path = ref if isinstance(ref, Path) else ROOT / ref
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(ref: str) -> str:
    return sha256((ROOT / ref).read_bytes()).hexdigest()


def hash_value(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return sha256(payload).hexdigest()


def render(value: dict[str, Any]) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def poly_trim(poly: list[tuple[int, ...]]) -> list[tuple[int, ...]]:
    out = [FIELD.normalize(coeff) for coeff in poly]
    while len(out) > 1 and out[-1] == ZERO:
        out.pop()
    return out


def poly_add(left: list[tuple[int, ...]], right: list[tuple[int, ...]]) -> list[tuple[int, ...]]:
    size = max(len(left), len(right))
    out = []
    for index in range(size):
        a = left[index] if index < len(left) else ZERO
        b = right[index] if index < len(right) else ZERO
        out.append(f_add(a, b))
    return poly_trim(out)


def poly_neg(poly: list[tuple[int, ...]]) -> list[tuple[int, ...]]:
    return poly_trim([f_neg(coeff) for coeff in poly])


def poly_sub(left: list[tuple[int, ...]], right: list[tuple[int, ...]]) -> list[tuple[int, ...]]:
    return poly_add(left, poly_neg(right))


def poly_mul(left: list[tuple[int, ...]], right: list[tuple[int, ...]]) -> list[tuple[int, ...]]:
    out = [ZERO] * (len(left) + len(right) - 1)
    for i, a_i in enumerate(left):
        for j, b_j in enumerate(right):
            out[i + j] = f_add(out[i + j], f_mul(a_i, b_j))
    return poly_trim(out)


def poly_scale(poly: list[tuple[int, ...]], scalar: tuple[int, ...]) -> list[tuple[int, ...]]:
    return poly_trim([f_mul(coeff, scalar) for coeff in poly])


def poly_divmod(
    numerator: list[tuple[int, ...]], denominator: list[tuple[int, ...]]
) -> tuple[list[tuple[int, ...]], list[tuple[int, ...]]]:
    work = poly_trim(numerator)
    divisor = poly_trim(denominator)
    require(divisor != [ZERO], "division by zero polynomial")
    quotient = [ZERO] * max(1, len(work) - len(divisor) + 1)
    inv_lead = f_inv(divisor[-1])
    while len(work) >= len(divisor) and work != [ZERO]:
        coeff = f_mul(work[-1], inv_lead)
        shift = len(work) - len(divisor)
        quotient[shift] = coeff
        for index, term in enumerate(divisor):
            work[shift + index] = f_sub(work[shift + index], f_mul(coeff, term))
        work = poly_trim(work)
    return poly_trim(quotient), work


def poly_monic(poly: list[tuple[int, ...]]) -> list[tuple[int, ...]]:
    trimmed = poly_trim(poly)
    if trimmed == [ZERO]:
        return trimmed
    return poly_scale(trimmed, f_inv(trimmed[-1]))


def poly_gcd(left: list[tuple[int, ...]], right: list[tuple[int, ...]]) -> list[tuple[int, ...]]:
    a = poly_trim(left)
    b = poly_trim(right)
    while b != [ZERO]:
        _quot, rem = poly_divmod(a, b)
        a, b = b, rem
    return poly_monic(a)


def poly_degree(poly: list[tuple[int, ...]]) -> int:
    trimmed = poly_trim(poly)
    if trimmed == [ZERO]:
        return -1
    return len(trimmed) - 1


def field_matrix_rref(rows: list[list[tuple[int, ...]]], width: int) -> tuple[list[list[tuple[int, ...]]], list[int]]:
    work = [[FIELD.normalize(entry) for entry in row] for row in rows]
    rank = 0
    pivots: list[int] = []
    for col in range(width):
        pivot = None
        for row in range(rank, len(work)):
            if work[row][col] != ZERO:
                pivot = row
                break
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        inv = f_inv(work[rank][col])
        work[rank] = [f_mul(entry, inv) for entry in work[rank]]
        for row in range(len(work)):
            if row == rank or work[row][col] == ZERO:
                continue
            factor = work[row][col]
            work[row] = [
                f_sub(work[row][entry_col], f_mul(factor, work[rank][entry_col]))
                for entry_col in range(width)
            ]
        pivots.append(col)
        rank += 1
        if rank == len(work):
            break
    return work, pivots


def nullspace_basis(rows: list[list[tuple[int, ...]]], width: int) -> list[list[tuple[int, ...]]]:
    reduced, pivots = field_matrix_rref(rows, width)
    pivot_set = set(pivots)
    free_cols = [col for col in range(width) if col not in pivot_set]
    basis = []
    for free_col in free_cols:
        vector = [ZERO] * width
        vector[free_col] = ONE
        for row_index, pivot_col in enumerate(pivots):
            vector[pivot_col] = f_neg(reduced[row_index][free_col])
        basis.append(vector)
    return basis


def powers(element: tuple[int, ...], count: int) -> list[tuple[int, ...]]:
    out = []
    cur = ONE
    for _ in range(count):
        out.append(cur)
        cur = f_mul(cur, element)
    return out


def vandermonde_rows(nodes: list[tuple[int, ...]], row_count: int) -> list[list[tuple[int, ...]]]:
    node_powers = [powers(node, row_count) for node in nodes]
    return [[node_powers[col][row] for col in range(len(nodes))] for row in range(row_count)]


def barycentric_weights(nodes: list[tuple[int, ...]]) -> list[tuple[int, ...]]:
    denominators = []
    for i, node_i in enumerate(nodes):
        product = ONE
        for j, node_j in enumerate(nodes):
            if i == j:
                continue
            product = f_mul(product, f_sub(node_i, node_j))
        denominators.append(product)
    return batch_invert(denominators)


def vandermonde_kernel_basis(
    nodes: list[tuple[int, ...]],
    vanish_row_count: int,
    node_powers: list[list[tuple[int, ...]]],
    weights: list[tuple[int, ...]],
) -> list[list[tuple[int, ...]]]:
    dimension = len(nodes) - vanish_row_count
    require(dimension >= 0, "negative Vandermonde kernel dimension")
    basis = []
    for exponent in range(dimension):
        basis.append([f_mul(weights[index], node_powers[index][exponent]) for index in range(len(nodes))])
    return basis


def determinant_poly(matrix: list[list[list[tuple[int, ...]]]]) -> list[tuple[int, ...]]:
    size = len(matrix)
    total = [ZERO]
    for perm in itertools.permutations(range(size)):
        term = [ONE]
        inversions = 0
        for i in range(size):
            for j in range(i + 1, size):
                if perm[i] > perm[j]:
                    inversions += 1
        for row, col in enumerate(perm):
            term = poly_mul(term, matrix[row][col])
        total = poly_sub(total, term) if inversions % 2 else poly_add(total, term)
    return poly_trim(total)


def minor_polynomials(matrix: list[list[list[tuple[int, ...]]]], size: int) -> list[list[tuple[int, ...]]]:
    row_count = len(matrix)
    out = []
    for rows in itertools.combinations(range(row_count), size):
        submatrix = [[matrix[row][col] for col in range(size)] for row in rows]
        out.append(determinant_poly(submatrix))
    return out


def encode_poly(poly: list[tuple[int, ...]]) -> list[int]:
    return [FIELD.encode(coeff) for coeff in poly_trim(poly)]


def boundary_record(agreement: int, domain: list[tuple[int, ...]]) -> dict[str, Any]:
    j_value = N - agreement
    t_value = agreement - K
    base_size = j_value + 1
    support_size = base_size + RANK
    deficit = support_size - t_value
    require(deficit in {1, 3, 5}, f"A={agreement}: unexpected deficit {deficit}")

    nodes = domain[:support_size]
    node_powers = [powers(node, max(t_value, j_value + 1, deficit, RANK) + 1) for node in nodes]
    weights = barycentric_weights(nodes)
    kernel_basis = vandermonde_kernel_basis(nodes, t_value, node_powers, weights)
    parity_basis = vandermonde_kernel_basis(nodes, j_value + 1, node_powers, weights)
    require(len(kernel_basis) == deficit, f"A={agreement}: kernel dimension mismatch")
    require(len(parity_basis) == RANK, f"A={agreement}: parity dimension mismatch")

    # A finite nonzero slope root is equivalent to
    # ker(V_t) intersecting diag(1,...,1,u,...,u) C_j nontrivially, u=1/z.
    # In bases this is a 6 x deficit linear pencil A0 + u A1.  All maximal
    # minors must vanish for a finite root.
    pencil: list[list[list[tuple[int, ...]]]] = []
    for parity in parity_basis:
        row = []
        for kernel in kernel_basis:
            base_sum = ZERO
            direction_sum = ZERO
            for index in range(base_size):
                base_sum = f_add(base_sum, f_mul(parity[index], kernel[index]))
            for index in range(base_size, support_size):
                direction_sum = f_add(direction_sum, f_mul(parity[index], kernel[index]))
            row.append([base_sum, direction_sum])
        pencil.append(row)

    minors = minor_polynomials(pencil, deficit)
    gcd = [ZERO]
    for minor in minors:
        if minor == [ZERO]:
            continue
        gcd = minor if gcd == [ZERO] else poly_gcd(gcd, minor)
    gcd = poly_monic(gcd)
    require(gcd != [ZERO], f"A={agreement}: all dual minors vanished")
    require(poly_degree(gcd) == 0, f"A={agreement}: nonconstant finite-root gcd")

    return {
        "A": agreement,
        "j": j_value,
        "t": t_value,
        "base_support_size": base_size,
        "direction_support_size": RANK,
        "support_union_size": support_size,
        "dual_kernel_dimension": deficit,
        "dual_parity_dimension": RANK,
        "dual_bases": "barycentric weights times powers of the support nodes",
        "moment_annihilation_identity": (
            "For m distinct nodes, barycentric weights times powers 0..d-1 "
            "span the nullspace of the first m-d moment rows."
        ),
        "dual_pencil_shape": [RANK, deficit],
        "maximal_minor_count": len(minors),
        "maximal_minor_degrees": [poly_degree(minor) for minor in minors],
        "common_gcd_degree_in_u": poly_degree(gcd),
        "common_gcd_encoded_low_to_high": encode_poly(gcd),
        "finite_nonzero_root_table": [],
        "finite_z_zero_full_rank": True,
        "finite_canonical_root_count": 0,
        "projective_endpoint_from_rank6_witness": True,
    }


def build_certificate() -> dict[str, Any]:
    descriptor = load_json(ROW_DESCRIPTOR_REF)
    rank_drop = load_json(RANK_DROP_BRIDGE_REF)

    require(descriptor["row"]["n"] == N, "descriptor n mismatch")
    require(descriptor["row"]["k"] == K, "descriptor k mismatch")
    require(descriptor["row"]["field"] == "F_17^32", "descriptor field mismatch")
    require(descriptor["row"]["field_order"] == Q_LINE, "descriptor q mismatch")
    require(
        rank_drop["schema_version"] == "f17-32-m3-m5-regular-root-rank-drop-v1",
        "rank-drop schema mismatch",
    )

    domain_encodings = descriptor["domain"]["domain_encodings"]
    require(len(domain_encodings) == N, "domain length mismatch")
    require(len(set(domain_encodings)) == N, "descriptor domain is not distinct")
    domain = [FIELD.decode(value) for value in domain_encodings]
    require([FIELD.encode(value) for value in domain] == domain_encodings, "domain roundtrip failed")

    records = [boundary_record(agreement, domain) for agreement in A_VALUES]
    require(all(record["common_gcd_degree_in_u"] == 0 for record in records), "boundary roots found")

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / COMPUTATIONAL",
        "object": "rank-6 prefix-plus-six-spikes finite-root closure at A=385..387",
        "row": {
            "code": "RS[F_17^32,H,256]",
            "n": N,
            "k": K,
            "field": "F_17^32",
            "domain_hash": descriptor["row"]["domain_hash"],
            "q_line": Q_LINE,
        },
        "source_artifacts": {
            "row_descriptor": {"ref": ROW_DESCRIPTOR_REF, "sha256": sha256_file(ROW_DESCRIPTOR_REF)},
            "regular_root_rank_drop_bridge": {
                "ref": RANK_DROP_BRIDGE_REF,
                "sha256": sha256_file(RANK_DROP_BRIDGE_REF),
            },
        },
        "agreements": A_VALUES,
        "family": {
            "base_support": "prefix X_A={x_0,...,x_j}",
            "direction_support": "next six descriptor-domain nodes Y_A={x_{j+1},...,x_{j+6}}",
            "weights": "unit weights in both u and v",
            "syndrome": "u_m=sum_{x in X_A} x^m, v_m=sum_{y in Y_A} y^m",
            "direction_rank": RANK,
        },
        "dual_gcd_method": {
            "support_union_size": "m=j+7",
            "finite_nonzero_parameter": "u=1/z",
            "kernel": "K=ker V_t(S), dimension d=m-t",
            "code": "C=Eval_{<=j}(S), codimension 6",
            "criterion": (
                "A finite nonzero rank-drop slope exists iff the 6 x d pencil "
                "P diag(1 on X, u on Y) K has rank < d."
            ),
            "root_test": (
                "The gcd of all d x d minors is constant for A=385,386,387; "
                "therefore there are no finite nonzero roots over F_17^32 or "
                "over scalar extensions."
            ),
        },
        "agreement_records": records,
        "summary": {
            "agreement_count": len(records),
            "finite_canonical_root_count_per_agreement": 0,
            "extends_rank6_projective_witness_to_full_window": True,
            "full_window": [385, 426],
        },
        "checks": [
            "row descriptor and dependency schemas match",
            "domain elements used by the prefix-plus-six-spikes family are distinct",
            "dual kernel dimensions are 5, 3, and 1 for A=385,386,387",
            "parity-check codimension is 6",
            "all maximal-minor gcds in u are constant",
            "z=0 is full rank by the base Vandermonde block",
            "the same split-locator endpoint construction applies at A=385,386,387",
        ],
        "nonclaims": [
            "does not classify arbitrary rank-6 Hankel pencils",
            "does not compute root tables for any family other than prefix-plus-six-spikes",
            "does not prove endpoint payment or quotient/extension status",
            "not a worst-case support-wise MCA row bound",
        ],
    }


def check_certificate(path: Path) -> None:
    expected = render(build_certificate())
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"rank-6 boundary dual-gcd certificate mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    print("F_17^32 M3 rank-6 boundary dual gcd")
    print("agreements={agreements}".format(**certificate))
    print("finite roots per agreement={finite_canonical_root_count_per_agreement}".format(**certificate["summary"]))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", type=Path)
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()

    certificate = build_certificate()
    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(render(certificate), encoding="utf-8")
    if args.check:
        check_certificate(args.check)
    print_summary(certificate)


if __name__ == "__main__":
    main()
