#!/usr/bin/env python3
"""Verify the degree-60 source-pencil compiler and route cut.

The certificate has two logically different parts.

* The compiler is uniform in a supplied endpoint record.  Its template
  counts, matrix shapes, strict right-factor routes, primitive subdegree
  table, and transverse outer degree rows are checked exactly.
* The deployed-field examples are controls for the divisor interface, not
  endpoint survivors.  They are reconstructed over F_(p^2) and F_p and
  checked by exact finite-field arithmetic.

This script deliberately does not claim a finite census of endpoint records,
a chronology-valid owner, or any movement of the KoalaBear ledger.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
import math
import subprocess
from pathlib import Path
from typing import Any, Callable, Iterable, Sequence


if not __debug__:
    raise RuntimeError("verifier refuses optimized Python execution")


class VerificationError(RuntimeError):
    """Raised when an exact certificate condition fails."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
CERTIFICATE = (
    ROOT
    / "data"
    / "certificates"
    / "kb-mca-v4-degree60-source-pencil-rank-compiler-v1"
    / "kb_mca_v4_degree60_source_pencil_rank_compiler_v1.json"
)

P = 2_130_706_433
FP2_ORDER = P * P
ONE2 = (1, 0)
ZERO2 = (0, 0)
STATUS = (
    "PROVED_EXACT_PER_RECORD_COMPILER_AND_TRANSVERSE_"
    "OUTER_ROUTE_CUT_ROW_OPEN"
)
EXPECTED_SCHEMA = "kb-mca-v4-degree60-source-pencil-rank-compiler-v1"
EXPECTED_PARENT_HEAD = "a14a05d9ba80068133e93e2fa77d6d1dc8828829"
EXPECTED_PARENT_PATH = (
    "experimental/data/certificates/"
    "kb-mca-v4-degree60-decomposition-source-fiber-adapter-v1/"
    "kb_mca_v4_degree60_decomposition_source_fiber_adapter_v1.json"
)
EXPECTED_PARENT_BLOB = "911bac3c1c5d1b4cd9822c59939d60e832b7ef23"
EXPECTED_PARENT_PAYLOAD = (
    "638190df24415e5609fa9c2f50dde8fd22bd150f60e7bef5cd1496cb22d75b4e"
)
EXPECTED_PARENT_TERMINAL = (
    "PROVED_SOURCE_FIBER_ADAPTER_DEGREE5_DELETION_"
    "DEGREE30_REFINEMENT_ROW_OPEN"
)

PROFILE_ROWS = [
    {
        "m": 2,
        "n": 30,
        "a": 6,
        "b": 0,
        "raw_templates": 10_395,
        "source_matrix": [3, 6],
        "source_rank": 2,
        "source_determinantal_codimension": 4,
        "active_matrix": [61, 31],
        "active_rank": 31,
        "active_syndromes": 30,
    },
    {
        "m": 3,
        "n": 20,
        "a": 4,
        "b": 0,
        "raw_templates": 15_400,
        "source_matrix": [4, 4],
        "source_rank": 2,
        "source_determinantal_codimension": 4,
        "active_matrix": [61, 21],
        "active_rank": 21,
        "active_syndromes": 40,
    },
    {
        "m": 4,
        "n": 15,
        "a": 3,
        "b": 0,
        "raw_templates": 5_775,
        "source_matrix": [5, 3],
        "source_rank": 2,
        "source_determinantal_codimension": 3,
        "active_matrix": [61, 16],
        "active_rank": 16,
        "active_syndromes": 45,
    },
    {
        "m": 6,
        "n": 10,
        "a": 2,
        "b": 0,
        "raw_templates": 462,
        "source_matrix": [7, 2],
        "source_rank": 2,
        "source_determinantal_codimension": 0,
        "active_matrix": [61, 11],
        "active_rank": 11,
        "active_syndromes": 50,
    },
    {
        "m": 10,
        "n": 6,
        "a": 1,
        "b": 1,
        "raw_templates": 66,
        "source_matrix": [11, 2],
        "source_rank": 2,
        "source_determinantal_codimension": 0,
        "active_matrix": [61, 7],
        "active_rank": 7,
        "active_syndromes": 54,
    },
    {
        "m": 12,
        "n": 5,
        "a": 1,
        "b": 0,
        "raw_templates": 1,
        "source_matrix": [13, 1],
        "source_rank": 1,
        "source_determinantal_codimension": 0,
        "active_matrix": [49, 5],
        "active_rank": 5,
        "active_syndromes": 44,
    },
]

EXPECTED_PRIMITIVE_CATALOGUE = [
    {
        "degree": 2,
        "primitive_group_count": 1,
        "subdegree_rows": [[1, 1]],
    },
    {
        "degree": 3,
        "primitive_group_count": 2,
        "subdegree_rows": [[1, 1, 1], [1, 2]],
    },
    {
        "degree": 4,
        "primitive_group_count": 2,
        "subdegree_rows": [[1, 3], [1, 3]],
    },
    {
        "degree": 5,
        "primitive_group_count": 5,
        "subdegree_rows": [
            [1, 1, 1, 1, 1],
            [1, 2, 2],
            [1, 4],
            [1, 4],
            [1, 4],
        ],
    },
    {
        "degree": 6,
        "primitive_group_count": 4,
        "subdegree_rows": [[1, 5], [1, 5], [1, 5], [1, 5]],
    },
    {
        "degree": 10,
        "primitive_group_count": 9,
        "subdegree_rows": [
            [1, 3, 6],
            [1, 3, 6],
            [1, 9],
            [1, 9],
            [1, 9],
            [1, 9],
            [1, 9],
            [1, 9],
            [1, 9],
        ],
    },
    {
        "degree": 12,
        "primitive_group_count": 6,
        "subdegree_rows": [
            [1, 11],
            [1, 11],
            [1, 11],
            [1, 11],
            [1, 11],
            [1, 11],
        ],
    },
]

EXPECTED_NONCLAIMS = [
    "The 32099 templates are not a finite census of all endpoint records.",
    (
        "The deployed-field controls are not inherited actual-component "
        "or received-line records."
    ),
    "No transverse outer correspondence is paid or deleted.",
    "No endpoint parameter is identified with a carrier coordinate.",
    (
        "No evaluation-domain, received-data, explaining-polynomial, "
        "or slope descent is proved."
    ),
    "No ledger quantity moves.",
    (
        "The u=2 branch, K3 workboard item, and KoalaBear row remain open."
    ),
]

EXPECTED_BINDINGS = [
    {
        "binding_id": "KB_SOURCE_PENCIL_COMPILER::parent_certificate",
        "commit": EXPECTED_PARENT_HEAD,
        "path": EXPECTED_PARENT_PATH,
        "blob_oid": EXPECTED_PARENT_BLOB,
        "role": (
            "six surviving source profiles, binary-pencil equivalence, "
            "field descent, and degree-five deletion"
        ),
    },
    {
        "binding_id": "KB_SOURCE_PENCIL_COMPILER::parent_note",
        "commit": EXPECTED_PARENT_HEAD,
        "path": (
            "experimental/notes/frontier-adjacent/"
            "kb_mca_v4_degree60_decomposition_source_fiber_adapter_v1.md"
        ),
        "blob_oid": "e15b77679b7dbc0bb28cf5642a04bb4c71e61429",
        "role": "source-fiber theorem and canonical degree-twelve pencil",
    },
    {
        "binding_id": "KB_SOURCE_PENCIL_COMPILER::actual_component",
        "commit": "44542e91e459364a521870ed2ebde7f6fe5055bf",
        "path": (
            "experimental/notes/frontier-adjacent/"
            "kb_mca_v4_equality_wall_geometry_v1/proof/"
            "pole_disjoint_conic_facet_collinearity_reduction.md"
        ),
        "blob_oid": "356ff4b47d0bb429d11ea10382762a6e95b5ce24",
        "role": (
            "actual irreducible bidegree-(4,4) component and endpoint "
            "parameter-line semantics"
        ),
    },
    {
        "binding_id": (
            "KB_SOURCE_PENCIL_COMPILER::primitive_degree60_route"
        ),
        "commit": EXPECTED_PARENT_HEAD,
        "path": (
            "experimental/notes/frontier-adjacent/"
            "kb_mca_v4_degree60_primitive_subdegree4_route_cut_v1.md"
        ),
        "blob_oid": "5d0ec0315fca34de80c22983b76bbafa12dd5661",
        "role": (
            "imported actual component bidegree and geometric "
            "decomposition route"
        ),
    },
    {
        "binding_id": "KB_SOURCE_PENCIL_COMPILER::deployed_field",
        "commit": EXPECTED_PARENT_HEAD,
        "path": "tex/cs25_cap_v13_2.tex",
        "blob_oid": "5ceff5dbc4b1ac4cef53eae7eada32046e4bafeb",
        "role": "deployed prime and extension field",
    },
]


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def payload_hash(value: dict[str, Any]) -> str:
    unhashed = dict(value)
    unhashed.pop("payload_sha256", None)
    return hashlib.sha256(canonical_json(unhashed).encode()).hexdigest()


def file_sha256(path: Path) -> str:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError as error:
        raise VerificationError(f"cannot hash replay: {path}") from error


def reject_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise VerificationError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=reject_duplicate_pairs,
        )
    except (OSError, json.JSONDecodeError) as error:
        raise VerificationError(f"cannot load certificate: {path}") from error
    require(isinstance(value, dict), "certificate root must be an object")
    return value


def parse_json_text(text: str, description: str) -> dict[str, Any]:
    try:
        value = json.loads(text, object_pairs_hook=reject_duplicate_pairs)
    except json.JSONDecodeError as error:
        raise VerificationError(f"invalid JSON in {description}") from error
    require(isinstance(value, dict), f"{description} must be an object")
    return value


def exact_keys(value: Any, expected: Iterable[str], context: str) -> None:
    require(isinstance(value, dict), f"{context} must be an object")
    expected_set = set(expected)
    actual_set = set(value)
    require(
        actual_set == expected_set,
        (
            f"{context} keys mismatch: missing={sorted(expected_set-actual_set)}, "
            f"extra={sorted(actual_set-expected_set)}"
        ),
    )


def git_output(*arguments: str) -> str:
    try:
        result = subprocess.run(
            ["git", *arguments],
            cwd=REPO_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError) as error:
        raise VerificationError(
            "git object binding failed: " + " ".join(arguments)
        ) from error
    return result.stdout.strip()


# ---------------------------------------------------------------------------
# Exact F_(p^2) arithmetic, with omega^2 + omega + 1 = 0.
# ---------------------------------------------------------------------------

Fp2 = tuple[int, int]
Poly2 = list[Fp2]


def fp2(value: Sequence[int] | int) -> Fp2:
    if isinstance(value, int):
        return (value % P, 0)
    require(len(value) == 2, "F_(p^2) coordinate must have length two")
    return (int(value[0]) % P, int(value[1]) % P)


def f2_add(left: Fp2, right: Fp2) -> Fp2:
    return ((left[0] + right[0]) % P, (left[1] + right[1]) % P)


def f2_neg(value: Fp2) -> Fp2:
    return (-value[0] % P, -value[1] % P)


def f2_sub(left: Fp2, right: Fp2) -> Fp2:
    return f2_add(left, f2_neg(right))


def f2_mul(left: Fp2, right: Fp2) -> Fp2:
    a, b = left
    c, d = right
    return ((a * c - b * d) % P, (a * d + b * c - b * d) % P)


def f2_inv(value: Fp2) -> Fp2:
    a, b = value
    norm = (a * a - a * b + b * b) % P
    require(norm != 0, "attempt to invert zero in F_(p^2)")
    inverse_norm = pow(norm, P - 2, P)
    return ((a - b) * inverse_norm % P, -b * inverse_norm % P)


def f2_pow(base: Fp2, exponent: int) -> Fp2:
    require(exponent >= 0, "negative F_(p^2) exponent")
    result = ONE2
    factor = base
    power = exponent
    while power:
        if power & 1:
            result = f2_mul(result, factor)
        factor = f2_mul(factor, factor)
        power >>= 1
    return result


def p2_trim(poly: Sequence[Fp2]) -> Poly2:
    result = [fp2(value) for value in poly]
    while len(result) > 1 and result[-1] == ZERO2:
        result.pop()
    return result or [ZERO2]


def p2_add(left: Sequence[Fp2], right: Sequence[Fp2]) -> Poly2:
    size = max(len(left), len(right))
    result = [ZERO2] * size
    for index in range(size):
        a = left[index] if index < len(left) else ZERO2
        b = right[index] if index < len(right) else ZERO2
        result[index] = f2_add(a, b)
    return p2_trim(result)


def p2_neg(poly: Sequence[Fp2]) -> Poly2:
    return p2_trim([f2_neg(value) for value in poly])


def p2_sub(left: Sequence[Fp2], right: Sequence[Fp2]) -> Poly2:
    return p2_add(left, p2_neg(right))


def p2_scale(poly: Sequence[Fp2], scalar: Fp2) -> Poly2:
    return p2_trim([f2_mul(value, scalar) for value in poly])


def p2_mul(left: Sequence[Fp2], right: Sequence[Fp2]) -> Poly2:
    result = [ZERO2] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] = f2_add(result[i + j], f2_mul(a, b))
    return p2_trim(result)


def p2_pow(base: Sequence[Fp2], exponent: int) -> Poly2:
    result = [ONE2]
    factor = p2_trim(base)
    power = exponent
    while power:
        if power & 1:
            result = p2_mul(result, factor)
        factor = p2_mul(factor, factor)
        power >>= 1
    return result


def p2_eval(poly: Sequence[Fp2], value: Fp2) -> Fp2:
    result = ZERO2
    for coefficient in reversed(poly):
        result = f2_add(f2_mul(result, value), coefficient)
    return result


def p2_from_roots(roots: Sequence[Fp2]) -> Poly2:
    result = [ONE2]
    for root in roots:
        result = p2_mul(result, [f2_neg(root), ONE2])
    return result


def p2_divmod(
    numerator: Sequence[Fp2], denominator: Sequence[Fp2]
) -> tuple[Poly2, Poly2]:
    num = p2_trim(numerator)
    den = p2_trim(denominator)
    require(den != [ZERO2], "polynomial division by zero")
    if len(num) < len(den):
        return [ZERO2], num
    quotient = [ZERO2] * (len(num) - len(den) + 1)
    inverse_lead = f2_inv(den[-1])
    remainder = num[:]
    while remainder != [ZERO2] and len(remainder) >= len(den):
        shift = len(remainder) - len(den)
        scalar = f2_mul(remainder[-1], inverse_lead)
        quotient[shift] = scalar
        for index, coefficient in enumerate(den):
            remainder[index + shift] = f2_sub(
                remainder[index + shift],
                f2_mul(scalar, coefficient),
            )
        remainder = p2_trim(remainder)
    return p2_trim(quotient), p2_trim(remainder)


def rank_fp2(rows: Sequence[Sequence[Fp2]]) -> int:
    if not rows:
        return 0
    width = len(rows[0])
    require(all(len(row) == width for row in rows), "ragged Fp2 matrix")
    matrix = [[fp2(value) for value in row] for row in rows]
    pivot_row = 0
    for column in range(width):
        pivot = next(
            (
                row
                for row in range(pivot_row, len(matrix))
                if matrix[row][column] != ZERO2
            ),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = (
            matrix[pivot],
            matrix[pivot_row],
        )
        inverse = f2_inv(matrix[pivot_row][column])
        matrix[pivot_row] = [
            f2_mul(value, inverse) for value in matrix[pivot_row]
        ]
        for row in range(len(matrix)):
            if row == pivot_row:
                continue
            scalar = matrix[row][column]
            if scalar == ZERO2:
                continue
            matrix[row] = [
                f2_sub(value, f2_mul(scalar, pivot_value))
                for value, pivot_value in zip(
                    matrix[row], matrix[pivot_row], strict=True
                )
            ]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return pivot_row


def coefficient_rows_fp2(
    columns: Sequence[Sequence[Fp2]], height: int
) -> list[list[Fp2]]:
    return [
        [
            column[row] if row < len(column) else ZERO2
            for column in columns
        ]
        for row in range(height)
    ]


def canonical_equal_block_partitions(
    points: tuple[int, ...], block_size: int, block_count: int
) -> Iterable[tuple[tuple[int, ...], ...]]:
    """Generate unordered equal-block partitions in a canonical order.

    The least remaining point is forced into the next block.  Consequently
    every unordered partition appears once and blocks are ordered by their
    least elements.
    """

    require(block_size >= 1, "block size must be positive")
    require(block_count >= 0, "block count must be nonnegative")
    require(
        len(points) == block_size * block_count,
        "equal-block partition has the wrong number of points",
    )
    if block_count == 0:
        yield ()
        return
    first = points[0]
    for companions in itertools.combinations(points[1:], block_size - 1):
        block = (first, *companions)
        block_set = set(block)
        remainder = tuple(point for point in points if point not in block_set)
        for tail in canonical_equal_block_partitions(
            remainder, block_size, block_count - 1
        ):
            yield (block, *tail)


def canonical_source_partitions(
    m: int, a: int, b: int
) -> Iterable[tuple[tuple[tuple[int, ...], ...], tuple[tuple[int, ...], ...]]]:
    """Enumerate canonical index templates for one supplied endpoint record.

    This enumerates partitions of the *twelve indices of that record*.  It
    does not enumerate endpoint records or field-valued source locators.
    Complete and exceptional blocks are different types.  Within either
    type the blocks are unordered.
    """

    require(a * m + b * (m // 5) == 12, "source profile does not cover 12")
    points = tuple(range(12))
    complete_size = a * m
    for complete_union in itertools.combinations(points, complete_size):
        complete_set = set(complete_union)
        exceptional_union = tuple(
            point for point in points if point not in complete_set
        )
        for complete_blocks in canonical_equal_block_partitions(
            tuple(complete_union), m, a
        ):
            for exceptional_blocks in canonical_equal_block_partitions(
                exceptional_union, m // 5 if b else 1, b
            ):
                yield complete_blocks, exceptional_blocks


def forced_forms_from_partition_fp2(
    source_points: Sequence[Fp2],
    partition: tuple[
        tuple[tuple[int, ...], ...], tuple[tuple[int, ...], ...]
    ],
) -> list[Poly2]:
    """Construct L_S and L_R^5 from one canonical source template."""

    require(len(source_points) == 12, "a supplied record needs 12 sources")
    complete_blocks, exceptional_blocks = partition
    forms = [
        p2_from_roots([source_points[index] for index in block])
        for block in complete_blocks
    ]
    forms.extend(
        p2_pow(
            p2_from_roots([source_points[index] for index in block]), 5
        )
        for block in exceptional_blocks
    )
    return forms


def classify_source_template_fp2(
    *,
    source_points: Sequence[Fp2],
    partition: tuple[
        tuple[tuple[int, ...], ...], tuple[tuple[int, ...], ...]
    ],
    m: int,
    n: int,
    active_locator: Sequence[Fp2],
    canonical_degree_twelve_second_form: Sequence[Fp2] | None = None,
    strict_right_factor_degree: int | None = None,
) -> dict[str, Any]:
    """Run the exact source-rank and active-membership gates on a template.

    A passing result is only a per-record linear-interface classification.
    In particular, ``LINEAR_GATES_PASS`` does not assert an inherited
    bidegree-(4,4) component.  The optional strict route is supplied only
    after an independent exact decomposition of the recovered pencil.
    """

    forms = forced_forms_from_partition_fp2(source_points, partition)
    require(all(len(form) <= m + 1 for form in forms), "forced form degree")
    padded_forms = [
        form + [ZERO2] * (m + 1 - len(form)) for form in forms
    ]
    source_rank = rank_fp2(padded_forms)
    if m == 12:
        require(
            canonical_degree_twelve_second_form is not None,
            "degree twelve needs its canonical recovered second form",
        )
        require(len(forms) == 1 and source_rank == 1, "degree-twelve source")
        h0 = forms[0]
        h1 = p2_trim(canonical_degree_twelve_second_form)
        pencil_rank = rank_fp2(
            [
                h0 + [ZERO2] * (13 - len(h0)),
                h1 + [ZERO2] * (13 - len(h1)),
            ]
        )
        if pencil_rank != 2:
            return {
                "terminal": "SOURCE_RANK_FAILURE",
                "source_rank": source_rank,
                "pencil_rank": pencil_rank,
                "active_rank": None,
                "augmented_rank": None,
            }
    else:
        if source_rank != 2:
            return {
                "terminal": "SOURCE_RANK_FAILURE",
                "source_rank": source_rank,
                "pencil_rank": source_rank,
                "active_rank": None,
                "augmented_rank": None,
            }
        h0, h1 = forms[:2]
        pencil_rank = source_rank

    columns = [
        p2_mul(p2_pow(h0, n - j), p2_pow(h1, j))
        for j in range(n + 1)
    ]
    matrix = coefficient_rows_fp2(columns, 61)
    active_rank = rank_fp2(matrix)
    active = p2_trim(active_locator)
    augmented = [
        row + [active[index] if index < len(active) else ZERO2]
        for index, row in enumerate(matrix)
    ]
    augmented_rank = rank_fp2(augmented)
    if active_rank != n + 1 or augmented_rank != active_rank:
        terminal = "ACTIVE_SYNDROME_FAILURE"
    elif strict_right_factor_degree is not None:
        require(
            1 < strict_right_factor_degree < m
            and m % strict_right_factor_degree == 0,
            "invalid strict right-factor degree",
        )
        terminal = "STRICT_RIGHT_FACTOR_ROUTE"
    else:
        terminal = "LINEAR_GATES_PASS"
    return {
        "terminal": terminal,
        "source_rank": source_rank,
        "pencil_rank": pencil_rank,
        "active_rank": active_rank,
        "augmented_rank": augmented_rank,
    }


# ---------------------------------------------------------------------------
# Exact F_p polynomial and matrix arithmetic.
# ---------------------------------------------------------------------------

Poly = list[int]


def poly_trim(poly: Sequence[int]) -> Poly:
    result = [int(value) % P for value in poly]
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result or [0]


def poly_add(left: Sequence[int], right: Sequence[int]) -> Poly:
    size = max(len(left), len(right))
    return poly_trim(
        [
            (
                (left[index] if index < len(left) else 0)
                + (right[index] if index < len(right) else 0)
            )
            % P
            for index in range(size)
        ]
    )


def poly_neg(poly: Sequence[int]) -> Poly:
    return poly_trim([-value % P for value in poly])


def poly_sub(left: Sequence[int], right: Sequence[int]) -> Poly:
    return poly_add(left, poly_neg(right))


def poly_scale(poly: Sequence[int], scalar: int) -> Poly:
    return poly_trim([scalar * value % P for value in poly])


def poly_mul(left: Sequence[int], right: Sequence[int]) -> Poly:
    result = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] = (result[i + j] + a * b) % P
    return poly_trim(result)


def poly_pow(base: Sequence[int], exponent: int) -> Poly:
    result = [1]
    factor = poly_trim(base)
    power = exponent
    while power:
        if power & 1:
            result = poly_mul(result, factor)
        factor = poly_mul(factor, factor)
        power >>= 1
    return result


def poly_shift(poly: Sequence[int], amount: int) -> Poly:
    return [0] * amount + poly_trim(poly)


def poly_eval(poly: Sequence[int], value: int) -> int:
    result = 0
    for coefficient in reversed(poly):
        result = (result * value + coefficient) % P
    return result


def poly_from_roots(roots: Sequence[int]) -> Poly:
    result = [1]
    for root in roots:
        result = poly_mul(result, [-root % P, 1])
    return result


def poly_divmod(
    numerator: Sequence[int], denominator: Sequence[int]
) -> tuple[Poly, Poly]:
    num = poly_trim(numerator)
    den = poly_trim(denominator)
    require(den != [0], "polynomial division by zero")
    if len(num) < len(den):
        return [0], num
    quotient = [0] * (len(num) - len(den) + 1)
    inverse_lead = pow(den[-1], P - 2, P)
    remainder = num[:]
    while remainder != [0] and len(remainder) >= len(den):
        shift = len(remainder) - len(den)
        scalar = remainder[-1] * inverse_lead % P
        quotient[shift] = scalar
        for index, coefficient in enumerate(den):
            remainder[index + shift] = (
                remainder[index + shift] - scalar * coefficient
            ) % P
        remainder = poly_trim(remainder)
    return poly_trim(quotient), poly_trim(remainder)


def poly_gcd(left: Sequence[int], right: Sequence[int]) -> Poly:
    a = poly_trim(left)
    b = poly_trim(right)
    while b != [0]:
        _, remainder = poly_divmod(a, b)
        a, b = b, remainder
    inverse = pow(a[-1], P - 2, P)
    return poly_scale(a, inverse)


def rank_mod(rows: Sequence[Sequence[int]]) -> int:
    if not rows:
        return 0
    width = len(rows[0])
    require(all(len(row) == width for row in rows), "ragged Fp matrix")
    matrix = [[value % P for value in row] for row in rows]
    pivot_row = 0
    for column in range(width):
        pivot = next(
            (
                row
                for row in range(pivot_row, len(matrix))
                if matrix[row][column] != 0
            ),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = (
            matrix[pivot],
            matrix[pivot_row],
        )
        inverse = pow(matrix[pivot_row][column], P - 2, P)
        matrix[pivot_row] = [
            value * inverse % P for value in matrix[pivot_row]
        ]
        for row in range(len(matrix)):
            if row == pivot_row:
                continue
            scalar = matrix[row][column]
            if scalar == 0:
                continue
            matrix[row] = [
                (value - scalar * pivot_value) % P
                for value, pivot_value in zip(
                    matrix[row], matrix[pivot_row], strict=True
                )
            ]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return pivot_row


def coefficient_rows(
    columns: Sequence[Sequence[int]], height: int
) -> list[list[int]]:
    return [
        [
            column[row] if row < len(column) else 0
            for column in columns
        ]
        for row in range(height)
    ]


def mobius_old_z_one_plus_inverse_t(
    homogeneous_affine_poly: Sequence[int], degree: int
) -> Poly:
    """Return t^degree*f((t+1)/t), preserving homogenized degree."""

    result = [0]
    t_plus_one = [1, 1]
    for exponent, coefficient in enumerate(homogeneous_affine_poly):
        if coefficient % P == 0:
            continue
        term = poly_mul(
            poly_pow(t_plus_one, exponent),
            [0] * (degree - exponent) + [1],
        )
        result = poly_add(result, poly_scale(term, coefficient))
    return poly_trim(result)


def exact_schema(data: dict[str, Any]) -> None:
    exact_keys(
        data,
        {
            "schema",
            "payload_sha256",
            "statement",
            "parent_stack",
            "compiler",
            "degree_twelve_reduction",
            "strict_right_factor_routing",
            "same_fiber_route_cut",
            "transverse_outer_terminal",
            "deployed_field_controls",
            "source_bindings",
            "independent_replays",
            "conclusion",
            "nonclaims",
        },
        "certificate",
    )
    exact_keys(
        data["statement"],
        {
            "workboard_item",
            "row",
            "object",
            "agreement",
            "B_star",
            "deployed_characteristic",
            "challenge_field_degree",
            "endpoint_degree",
            "component_u",
            "component_bidegree",
            "record_quantifier",
            "template_count_scope",
            "status",
            "ledger_movement",
        },
        "statement",
    )
    exact_keys(
        data["parent_stack"],
        {
            "head_commit",
            "certificate_path",
            "certificate_blob_oid",
            "certificate_payload_sha256",
            "imported_terminal",
        },
        "parent_stack",
    )
    exact_keys(
        data["compiler"],
        {
            "raw_template_total",
            "source_coefficient_order",
            "active_coefficient_order",
            "source_gate",
            "active_gate",
            "active_columns",
            "terminal_order",
            "profiles",
        },
        "compiler",
    )
    require(
        isinstance(data["compiler"]["profiles"], list),
        "compiler.profiles must be a list",
    )
    profile_keys = set(PROFILE_ROWS[0])
    for index, profile in enumerate(data["compiler"]["profiles"]):
        exact_keys(profile, profile_keys, f"compiler.profiles[{index}]")
    exact_keys(
        data["degree_twelve_reduction"],
        {
            "unique_source_partition",
            "canonical_pencil",
            "residue_equation",
            "residue_unique",
            "gcd_A_N0_automatic_from_active_source_disjointness",
            "reduced_quotient",
            "degree_bound_B",
            "basis",
            "matrix_shape",
            "matrix_rank",
            "syndromes",
        },
        "degree_twelve_reduction",
    )
    exact_keys(
        data["strict_right_factor_routing"],
        {
            "routes",
            "degree_five_terminal",
            "strictly_decreasing",
            "terminal_inner_degrees",
        },
        "strict_right_factor_routing",
    )
    exact_keys(
        data["same_fiber_route_cut"],
        {
            "same_fiber_form",
            "actual_component_irreducible",
            "actual_component_bidegree",
            "required_subdegree_if_contained",
            "small_degree_catalogue",
            "degree_five_is_only_profile_with_catalogue_subdegree_four",
            "degree_five_already_deleted",
            "terminal",
        },
        "same_fiber_route_cut",
    )
    for index, row in enumerate(
        data["same_fiber_route_cut"]["small_degree_catalogue"]
    ):
        exact_keys(
            row,
            {"degree", "primitive_group_count", "subdegree_rows"},
            f"small_degree_catalogue[{index}]",
        )
    exact_keys(
        data["transverse_outer_terminal"],
        {
            "image",
            "image_irreducible",
            "image_nondiagonal",
            "degree_identity",
            "cover_degree_upper_bound",
            "terminal",
            "rows",
            "paid",
        },
        "transverse_outer_terminal",
    )
    for index, row in enumerate(data["transverse_outer_terminal"]["rows"]):
        exact_keys(row, {"m", "n", "r_delta"}, f"outer.rows[{index}]")
    controls = data["deployed_field_controls"]
    exact_keys(
        controls,
        {
            "scope",
            "field_embedding",
            "fp2_model",
            "sqrt_minus_one",
            "power_controls",
            "degree_ten_control",
            "prime_degree_controls_indecomposable",
            "composite_control_routes",
        },
        "deployed_field_controls",
    )
    for index, row in enumerate(controls["power_controls"]):
        exact_keys(
            row,
            {
                "m",
                "n",
                "a",
                "zeta",
                "target_representatives",
                "right_factor_degree",
            },
            f"power_controls[{index}]",
        )
    degree_ten = controls["degree_ten_control"]
    exact_keys(
        degree_ten,
        {
            "field",
            "outer_polynomial",
            "right_component",
            "inner_map",
            "source_value",
            "active_values",
            "h_at_old_z_1",
            "coordinate_change",
            "exceptional_source_points_new_t",
            "right_factor_degree",
            "fibers",
            "source_points_all_finite_after_conjugation",
            "active_points_all_finite_after_conjugation",
            "source_matrix_rank",
            "active_matrix_rank",
            "active_membership",
        },
        "degree_ten_control",
    )
    for index, fiber in enumerate(degree_ten["fibers"]):
        exact_keys(
            fiber,
            {"y", "x_roots", "z_roots"},
            f"degree_ten_control.fibers[{index}]",
        )
    require(isinstance(data["source_bindings"], list), "bindings must be list")
    for index, binding in enumerate(data["source_bindings"]):
        exact_keys(
            binding,
            {"binding_id", "commit", "path", "blob_oid", "role"},
            f"source_bindings[{index}]",
        )
    exact_keys(
        data["independent_replays"],
        {"sage", "wolfram", "live_wolfram_plugin"},
        "independent_replays",
    )
    exact_keys(
        data["independent_replays"]["sage"],
        {"path", "sha256"},
        "independent_replays.sage",
    )
    exact_keys(
        data["independent_replays"]["wolfram"],
        {"path", "sha256"},
        "independent_replays.wolfram",
    )
    exact_keys(
        data["independent_replays"]["live_wolfram_plugin"],
        {
            "profile_total",
            "power_divisibility",
            "degree_ten_all_x_checks",
            "degree_ten_all_z_checks",
            "degree_ten_all_roots_distinct",
        },
        "live_wolfram_plugin",
    )
    exact_keys(
        data["conclusion"],
        {
            "terminal",
            "missing_theorem",
            "u2_closed",
            "K3_closed",
            "row_closed",
        },
        "conclusion",
    )


def verify_statement_and_compiler(data: dict[str, Any]) -> None:
    statement = data["statement"]
    require(data["schema"] == EXPECTED_SCHEMA, "schema mismatch")
    require(statement["workboard_item"] == "K3", "wrong workboard item")
    require(statement["row"] == "KoalaBear MCA at 2^-128", "wrong row")
    require(statement["object"] == "MCA", "wrong object")
    require(statement["agreement"] == 1_116_048, "wrong agreement")
    require(statement["B_star"] == "274980728111395087", "wrong B_star")
    require(statement["deployed_characteristic"] == P, "wrong prime")
    require(statement["challenge_field_degree"] == 6, "wrong field degree")
    require(statement["endpoint_degree"] == 60, "wrong endpoint degree")
    require(statement["component_u"] == 2, "wrong component u")
    require(statement["component_bidegree"] == [4, 4], "wrong bidegree")
    require(
        statement["record_quantifier"]
        == (
            "every supplied actual endpoint record (K,A,V_act,Gamma) "
            "satisfying the imported parent hypotheses"
        ),
        "record quantifier changed",
    )
    require(
        statement["template_count_scope"]
        == (
            "per supplied endpoint record, not a finite census of all "
            "endpoint records"
        ),
        "template scope changed",
    )
    require(statement["status"] == STATUS, "status mismatch")
    require(statement["ledger_movement"] == 0, "ledger movement is nonzero")

    parent = data["parent_stack"]
    require(parent["head_commit"] == EXPECTED_PARENT_HEAD, "parent head")
    require(parent["certificate_path"] == EXPECTED_PARENT_PATH, "parent path")
    require(parent["certificate_blob_oid"] == EXPECTED_PARENT_BLOB, "parent blob")
    require(
        parent["certificate_payload_sha256"] == EXPECTED_PARENT_PAYLOAD,
        "parent payload",
    )
    require(
        parent["imported_terminal"] == EXPECTED_PARENT_TERMINAL,
        "parent terminal",
    )

    compiler = data["compiler"]
    require(compiler["raw_template_total"] == 32_099, "template total")
    require(
        compiler["source_coefficient_order"] == "degrees 0 through m",
        "source coefficient order",
    )
    require(
        compiler["active_coefficient_order"] == "degrees 0 through 60",
        "active coefficient order",
    )
    require(
        compiler["source_gate"]
        == (
            "rank(S_pi)=2 for m in {2,3,4,6,10}; "
            "m=12 uses degree_twelve_reduction"
        ),
        "source gate",
    )
    require(
        compiler["active_gate"]
        == (
            "rank([C_mn|coeff(V_act)])=rank(C_mn)=n+1 "
            "for m in {2,3,4,6,10}; "
            "m=12 uses degree_twelve_reduction"
        ),
        "active gate",
    )
    require(
        compiler["active_columns"]
        == (
            "for m in {2,3,4,6,10}: "
            "coeff(H0^(n-j)*H1^j), j=0,...,n; "
            "m=12 uses degree_twelve_reduction"
        ),
        "active columns",
    )
    require(
        compiler["terminal_order"]
        == [
            "SOURCE_RANK_FAILURE",
            "ACTIVE_SYNDROME_FAILURE",
            "STRICT_RIGHT_FACTOR_ROUTE",
            "SAME_FIBER_SUBDEGREE4_IMPOSSIBLE",
            "TRANSVERSE_OUTER_CORRESPONDENCE",
        ],
        "terminal order",
    )
    require(compiler["profiles"] == PROFILE_ROWS, "profile table mismatch")

    computed_total = 0
    for row in PROFILE_ROWS:
        m, n, a, b = row["m"], row["n"], row["a"], row["b"]
        require(m * n == 60, f"profile m={m} does not multiply to 60")
        require(a * m + b * (m // 5) == 12, f"profile m={m} source count")
        denominator = (
            math.factorial(m) ** a
            * math.factorial(a)
            * math.factorial(m // 5) ** b
            * math.factorial(b)
        )
        templates = math.factorial(12) // denominator
        require(templates == row["raw_templates"], f"profile m={m} count")
        computed_total += templates
        if m != 12:
            require(
                row["source_matrix"] == [m + 1, a + b],
                f"profile m={m} source matrix",
            )
            require(
                row["active_matrix"] == [61, n + 1],
                f"profile m={m} active matrix",
            )
            require(row["active_rank"] == n + 1, f"profile m={m} rank")
            require(
                row["active_syndromes"] == 60 - n,
                f"profile m={m} syndromes",
            )
    require(computed_total == 32_099, "recomputed template total")


def verify_canonical_template_enumeration() -> None:
    """Actually enumerate the 32,099 per-record source index templates."""

    grand_total = 0
    for row in PROFILE_ROWS:
        m, a, b = row["m"], row["a"], row["b"]
        seen: set[
            tuple[
                tuple[tuple[int, ...], ...],
                tuple[tuple[int, ...], ...],
            ]
        ] = set()
        count = 0
        for partition in canonical_source_partitions(m, a, b):
            complete_blocks, exceptional_blocks = partition
            require(partition not in seen, f"duplicate canonical template m={m}")
            seen.add(partition)
            require(
                all(
                    tuple(sorted(block)) == block and len(block) == m
                    for block in complete_blocks
                ),
                f"malformed complete block m={m}",
            )
            require(
                all(
                    tuple(sorted(block)) == block and len(block) == m // 5
                    for block in exceptional_blocks
                ),
                f"malformed exceptional block m={m}",
            )
            require(
                tuple(sorted(complete_blocks)) == complete_blocks,
                f"complete blocks are not canonical m={m}",
            )
            require(
                tuple(sorted(exceptional_blocks)) == exceptional_blocks,
                f"exceptional blocks are not canonical m={m}",
            )
            flattened = [
                point
                for block in (*complete_blocks, *exceptional_blocks)
                for point in block
            ]
            require(
                sorted(flattened) == list(range(12)),
                f"template does not partition record indices m={m}",
            )
            count += 1
        require(
            count == row["raw_templates"],
            f"enumerated template count mismatch m={m}",
        )
        require(len(seen) == count, f"template uniqueness mismatch m={m}")
        grand_total += count
    require(grand_total == 32_099, "enumerated grand template total")


def verify_degree_twelve_and_routes(data: dict[str, Any]) -> None:
    degree_twelve = data["degree_twelve_reduction"]
    require(
        degree_twelve
        == {
            "unique_source_partition": True,
            "canonical_pencil": "<A,N0>",
            "residue_equation": "N0^5=V_act mod A with deg(N0)<12",
            "residue_unique": True,
            "gcd_A_N0_automatic_from_active_source_disjointness": True,
            "reduced_quotient": "B=(V_act-N0^5)/A",
            "degree_bound_B": 48,
            "basis": [
                "A^4",
                "A^3*N0",
                "A^2*N0^2",
                "A*N0^3",
                "N0^4",
            ],
            "matrix_shape": [49, 5],
            "matrix_rank": 5,
            "syndromes": 44,
        },
        "degree-twelve reduction changed",
    )
    routes = data["strict_right_factor_routing"]
    require(
        routes
        == {
            "routes": {
                "4": [2],
                "6": [2, 3],
                "10": [2, 5],
                "12": [2, 3, 4, 6],
            },
            "degree_five_terminal": (
                "DELETED_CHALLENGE_FIELD_FIFTH_POWER_FIBER_CONTRADICTION"
            ),
            "strictly_decreasing": True,
            "terminal_inner_degrees": [2, 3, 4, 6, 10, 12],
        },
        "strict right-factor routes changed",
    )
    for source, targets in routes["routes"].items():
        require(
            all(1 < target < int(source) for target in targets),
            f"route from {source} is not strict",
        )


def verify_same_fiber_and_transverse(data: dict[str, Any]) -> None:
    route_cut = data["same_fiber_route_cut"]
    require(
        route_cut["same_fiber_form"]
        == "Delta_h(T,W)=H0(T)H1(W)-H1(T)H0(W)",
        "same-fiber form",
    )
    require(route_cut["actual_component_irreducible"] is True, "irreducible")
    require(route_cut["actual_component_bidegree"] == [4, 4], "bidegree")
    require(route_cut["required_subdegree_if_contained"] == 4, "subdegree")
    require(
        route_cut["small_degree_catalogue"]
        == EXPECTED_PRIMITIVE_CATALOGUE,
        "primitive subdegree catalogue mismatch",
    )
    for row in EXPECTED_PRIMITIVE_CATALOGUE:
        require(
            row["primitive_group_count"] == len(row["subdegree_rows"]),
            f"primitive count mismatch at degree {row['degree']}",
        )
        require(
            all(sum(subdegrees) == row["degree"] for subdegrees in row["subdegree_rows"]),
            f"subdegrees do not sum at degree {row['degree']}",
        )
    degrees_with_four = {
        row["degree"]
        for row in EXPECTED_PRIMITIVE_CATALOGUE
        if any(4 in subdegrees for subdegrees in row["subdegree_rows"])
    }
    require(degrees_with_four == {5}, "catalogue subdegree-four locus")
    require(
        route_cut["degree_five_is_only_profile_with_catalogue_subdegree_four"]
        is True,
        "degree-five uniqueness assertion",
    )
    require(route_cut["degree_five_already_deleted"] is True, "degree five")
    require(
        route_cut["terminal"] == "SAME_FIBER_SUBDEGREE4_IMPOSSIBLE",
        "same-fiber terminal",
    )

    outer = data["transverse_outer_terminal"]
    require(outer["image"] == "C=closure((h x h)(Gamma))", "outer image")
    require(outer["image_irreducible"] is True, "outer irreducible")
    require(outer["image_nondiagonal"] is True, "outer diagonal")
    require(outer["degree_identity"] == "delta*r=4*m", "degree identity")
    require(
        outer["cover_degree_upper_bound"] == "delta<=m^2",
        "cover-degree upper bound",
    )
    require(
        outer["terminal"] == "TRANSVERSE_OUTER_CORRESPONDENCE",
        "outer terminal",
    )
    require(outer["paid"] is False, "outer terminal cannot be paid")
    expected_rows = []
    for profile in PROFILE_ROWS:
        m, n = profile["m"], profile["n"]
        pairs = [
            [r, 4 * m // r]
            for r in range(1, n)
            if (4 * m) % r == 0 and 4 * m // r <= m * m
        ]
        expected_rows.append({"m": m, "n": n, "r_delta": pairs})
    require(outer["rows"] == expected_rows, "transverse r-delta rows")
    for row in outer["rows"]:
        for r, delta in row["r_delta"]:
            require(r * delta == 4 * row["m"], "r-delta identity")
            require(r <= row["n"] - 1, "outer degree exceeds n-1")
            require(
                delta <= row["m"] * row["m"],
                "cover degree exceeds degree(h x h)",
            )


def verify_power_controls(data: dict[str, Any]) -> None:
    controls = data["deployed_field_controls"]
    require(
        controls["scope"] == "DIVISOR_INTERFACE_CONTROLS_NOT_ENDPOINT_SURVIVORS",
        "control scope",
    )
    require(
        controls["field_embedding"]
        == "F_(p^2) is a subfield of K=F_(p^6)",
        "field embedding",
    )
    require(controls["fp2_model"] == "omega^2+omega+1=0", "Fp2 model")
    iota = controls["sqrt_minus_one"]
    require(iota == 16_711_679, "sqrt(-1) changed")
    require(iota * iota % P == P - 1, "incorrect sqrt(-1)")
    require(P % 3 == 2, "omega polynomial is not certified irreducible")

    expected_controls = [
        (2, 30, 6, (P - 1, 0), 36, None),
        (3, 20, 4, (0, 1), 24, None),
        (4, 15, 3, (iota, 0), 18, 2),
        (6, 10, 2, (0, P - 1), 12, 2),
        (12, 5, 1, (0, iota), 6, 2),
    ]
    actual_controls = controls["power_controls"]
    require(len(actual_controls) == len(expected_controls), "power rows")

    for row, expected in zip(actual_controls, expected_controls, strict=True):
        m, n, a, zeta_raw, representatives, right_degree = expected
        require(
            (
                row["m"],
                row["n"],
                row["a"],
                tuple(row["zeta"]),
                row["target_representatives"],
                row["right_factor_degree"],
            )
            == expected,
            f"power control metadata changed for m={m}",
        )
        require(m * n == 60 and a * m == 12, f"power profile m={m}")
        require(representatives == a + n, f"representatives m={m}")
        require((P * P - 1) % m == 0, f"m={m} does not divide p^2-1")

        zeta = fp2(zeta_raw)
        require(f2_pow(zeta, m) == ONE2, f"zeta_{m} power")
        require(
            all(f2_pow(zeta, exponent) != ONE2 for exponent in range(1, m)),
            f"zeta_{m} does not have exact order",
        )

        targets = [pow(u, m, P) for u in range(1, representatives + 1)]
        require(len(set(targets)) == representatives, f"targets collide m={m}")
        fibers: list[Poly2] = []
        fiber_roots: list[list[Fp2]] = []
        all_roots: set[Fp2] = set()
        for u, target in zip(
            range(1, representatives + 1), targets, strict=True
        ):
            roots = [
                f2_mul((u, 0), f2_pow(zeta, exponent))
                for exponent in range(m)
            ]
            require(len(set(roots)) == m, f"fiber is not reduced m={m}")
            require(
                all(p2_eval([f2_neg((target, 0))] + [ZERO2] * (m - 1) + [ONE2], root) == ZERO2 for root in roots),
                f"root misses power fiber m={m}",
            )
            require(
                not (set(roots) & all_roots), f"power fibers overlap m={m}"
            )
            all_roots.update(roots)
            locator = [f2_neg((target, 0))] + [ZERO2] * (m - 1) + [ONE2]
            require(p2_from_roots(roots) == locator, f"locator roots m={m}")
            fibers.append(locator)
            fiber_roots.append(roots)

        source_roots = set().union(*(set(roots) for roots in fiber_roots[:a]))
        active_roots = set().union(*(set(roots) for roots in fiber_roots[a:]))
        require(len(source_roots) == 12, f"source roots m={m}")
        require(len(active_roots) == 60, f"active roots m={m}")
        require(not (source_roots & active_roots), f"source-active overlap m={m}")

        source_rows = [
            locator + [ZERO2] * (m + 1 - len(locator))
            for locator in fibers[:a]
        ]
        expected_source_rank = 1 if m == 12 else 2
        require(
            rank_fp2(source_rows) == expected_source_rank,
            f"source rank m={m}",
        )

        h0 = [ZERO2] * m + [ONE2]
        h1 = [ONE2]
        active_columns = [
            p2_mul(p2_pow(h0, n - j), p2_pow(h1, j))
            for j in range(n + 1)
        ]
        active = [ONE2]
        for locator in fibers[a:]:
            active = p2_mul(active, locator)
        matrix = coefficient_rows_fp2(active_columns, 61)
        require(rank_fp2(matrix) == n + 1, f"active rank m={m}")
        augmented = [
            row + [active[index] if index < len(active) else ZERO2]
            for index, row in enumerate(matrix)
        ]
        require(rank_fp2(augmented) == n + 1, f"active membership m={m}")

        canonical_second_form: Poly2 | None = None
        if m == 12:
            source_locator = fibers[0]
            quotient, remainder = p2_divmod(active, source_locator)
            del quotient
            require(len(remainder) == 1, "m=12 residue is not constant")
            require(remainder[0] != ZERO2, "m=12 residue vanishes")
            require(math.gcd(5, FP2_ORDER - 1) == 1, "fifth power not bijective")
            inverse_five = pow(5, -1, FP2_ORDER - 1)
            n0_scalar = f2_pow(remainder[0], inverse_five)
            require(
                f2_pow(n0_scalar, 5) == remainder[0],
                "m=12 fifth-root recovery",
            )
            canonical_second_form = [n0_scalar]
            numerator = p2_sub(active, [f2_pow(n0_scalar, 5)])
            reduced, reduced_remainder = p2_divmod(
                numerator, source_locator
            )
            require(reduced_remainder == [ZERO2], "m=12 quotient remainder")
            require(len(reduced) <= 49, "m=12 quotient degree")
            n0 = [n0_scalar]
            basis = [
                p2_mul(
                    p2_pow(source_locator, 4 - j),
                    p2_pow(n0, j),
                )
                for j in range(5)
            ]
            reduced_matrix = coefficient_rows_fp2(basis, 49)
            require(rank_fp2(reduced_matrix) == 5, "m=12 basis rank")
            reduced_augmented = [
                row
                + [reduced[index] if index < len(reduced) else ZERO2]
                for index, row in enumerate(reduced_matrix)
            ]
            require(
                rank_fp2(reduced_augmented) == 5,
                "m=12 reduced membership",
            )

        source_points = [
            root for roots in fiber_roots[:a] for root in roots
        ]
        complete_blocks = tuple(
            tuple(range(block * m, (block + 1) * m))
            for block in range(a)
        )
        control_partition = (complete_blocks, ())
        require(
            any(
                partition == control_partition
                for partition in canonical_source_partitions(m, a, 0)
            ),
            f"control source partition is not canonical m={m}",
        )
        classification = classify_source_template_fp2(
            source_points=source_points,
            partition=control_partition,
            m=m,
            n=n,
            active_locator=active,
            canonical_degree_twelve_second_form=canonical_second_form,
            strict_right_factor_degree=right_degree,
        )
        expected_terminal = (
            "STRICT_RIGHT_FACTOR_ROUTE"
            if right_degree is not None
            else "LINEAR_GATES_PASS"
        )
        require(
            classification["terminal"] == expected_terminal,
            f"per-template classifier terminal m={m}",
        )
        require(
            classification["active_rank"] == n + 1
            and classification["augmented_rank"] == n + 1,
            f"per-template classifier active ranks m={m}",
        )
        require(
            classification["source_rank"] == expected_source_rank,
            f"per-template classifier source rank m={m}",
        )

        if right_degree is not None:
            require(m % right_degree == 0, f"power route m={m}")

    require(
        controls["prime_degree_controls_indecomposable"] == [2, 3],
        "prime-degree control claim",
    )
    require(
        controls["composite_control_routes"]
        == {"4": 2, "6": 2, "10": 2, "12": 2},
        "composite control routes",
    )


def verify_degree_ten_control(data: dict[str, Any]) -> None:
    control = data["deployed_field_controls"]["degree_ten_control"]
    require(control["field"] == "F_p", "degree-ten field")
    require(control["outer_polynomial"] == "s5(x)=x^5+x^2+x", "outer s")
    require(control["right_component"] == "r(z)=z+2/z", "right component")
    require(control["inner_map"] == "h=s5 composed with r", "inner map")
    require(control["source_value"] == 243, "source value")
    active_values = [3459, 3574, 8607, 19677, 30437, 43384]
    require(control["active_values"] == active_values, "active values")
    require(control["h_at_old_z_1"] == 255, "h(1)")
    require(control["coordinate_change"] == "old z=1+1/t", "conjugation")
    require(
        control["exceptional_source_points_new_t"] == [0, P - 1],
        "exceptional source points",
    )
    require(control["right_factor_degree"] == 2, "right-factor degree")

    q = [2, 0, 1]
    d_old = [0, 0, 0, 0, 0, 1]
    n_old = poly_add(
        poly_add(poly_pow(q, 5), poly_shift(poly_pow(q, 2), 3)),
        poly_shift(q, 4),
    )
    require(len(n_old) == 11, "degree-ten numerator degree")
    require(poly_eval(n_old, 1) == 255, "computed h(1) numerator")
    require(poly_eval(d_old, 1) == 1, "computed h(1) denominator")

    fibers = control["fibers"]
    expected_values = [243] + active_values
    require([fiber["y"] for fiber in fibers] == expected_values, "fiber order")
    all_z_roots: set[int] = set()
    transformed_by_value: dict[int, list[int]] = {}
    new_fibers: dict[int, Poly] = {}

    for fiber in fibers:
        y = fiber["y"]
        x_roots = [int(value) % P for value in fiber["x_roots"]]
        z_roots = [int(value) % P for value in fiber["z_roots"]]
        require(len(x_roots) == 5 == len(set(x_roots)), f"x roots y={y}")
        require(len(z_roots) == 10 == len(set(z_roots)), f"z roots y={y}")
        x_polynomial = [-y % P, 1, 1, 0, 0, 1]
        require(
            poly_from_roots(x_roots) == x_polynomial,
            f"outer polynomial roots y={y}",
        )
        require(
            all((pow(x, 5, P) + x * x + x - y) % P == 0 for x in x_roots),
            f"outer root evaluation y={y}",
        )

        preimage_counts = {x: 0 for x in x_roots}
        for z in z_roots:
            require(z != 0, f"selected old z=0 y={y}")
            x = (z + 2 * pow(z, P - 2, P)) % P
            require(x in preimage_counts, f"z does not map to x y={y}")
            require((z * z - x * z + 2) % P == 0, f"quadratic y={y}")
            preimage_counts[x] += 1
        require(
            set(preimage_counts.values()) == {2},
            f"quadratic fibers not two-to-one y={y}",
        )
        require(
            not (set(z_roots) & all_z_roots), f"old fibers overlap y={y}"
        )
        all_z_roots.update(z_roots)

        old_fiber = poly_sub(n_old, poly_scale(d_old, y))
        require(poly_from_roots(z_roots) == old_fiber, f"old fiber y={y}")
        require(
            all(poly_eval(old_fiber, z) == 0 for z in z_roots),
            f"old root evaluation y={y}",
        )
        require(1 not in z_roots, f"conjugation pole in fiber y={y}")
        transformed = [pow(z - 1, P - 2, P) for z in z_roots]
        require(
            len(set(transformed)) == 10, f"transformed roots collide y={y}"
        )
        transformed_by_value[y] = transformed

    require(len(all_z_roots) == 70, "degree-ten old roots not globally distinct")
    n_new = mobius_old_z_one_plus_inverse_t(n_old, 10)
    d_new = mobius_old_z_one_plus_inverse_t(d_old, 10)
    rn_new = [1, 2, 3]
    rd_new = [0, 1, 1]
    expected_n_new = poly_add(
        poly_add(
            poly_pow(rn_new, 5),
            poly_mul(poly_pow(rn_new, 2), poly_pow(rd_new, 3)),
        ),
        poly_mul(rn_new, poly_pow(rd_new, 4)),
    )
    expected_d_new = poly_pow(rd_new, 5)
    require(n_new == expected_n_new, "conjugated composition numerator")
    require(d_new == expected_d_new, "conjugated composition denominator")
    require(poly_gcd(rn_new, rd_new) == [1], "degree-two right map cancels")
    require(len(rn_new) - 1 == 2 and len(rd_new) - 1 == 2, "right degree")

    for y in expected_values:
        new_fiber = poly_sub(n_new, poly_scale(d_new, y))
        transformed = transformed_by_value[y]
        root_product = poly_from_roots(transformed)
        require(new_fiber[-1] == (255 - y) % P, f"leading value y={y}")
        require(
            new_fiber == poly_scale(root_product, new_fiber[-1]),
            f"conjugated fiber identity y={y}",
        )
        require(
            all(poly_eval(new_fiber, root) == 0 for root in transformed),
            f"conjugated root evaluation y={y}",
        )
        new_fibers[y] = new_fiber

    source_roots = set(transformed_by_value[243]) | {0, P - 1}
    active_roots = set().union(
        *(set(transformed_by_value[y]) for y in active_values)
    )
    require(len(source_roots) == 12, "degree-ten finite source roots")
    require(len(active_roots) == 60, "degree-ten finite active roots")
    require(not (source_roots & active_roots), "degree-ten source-active overlap")
    source_locator = poly_mul([0, 1, 1], new_fibers[243])
    require(
        source_locator
        == poly_scale(
            poly_from_roots(sorted(source_roots)), source_locator[-1]
        ),
        "degree-ten source locator roots",
    )

    source_forms = [
        new_fibers[243] + [0] * (11 - len(new_fibers[243])),
        d_new + [0] * (11 - len(d_new)),
    ]
    source_rank = rank_mod(source_forms)
    require(source_rank == 2, "degree-ten source matrix rank")
    require(control["source_matrix_rank"] == source_rank, "source rank field")

    active_locator = [1]
    for y in active_values:
        active_locator = poly_mul(active_locator, new_fibers[y])
    require(
        active_locator
        == poly_scale(
            poly_from_roots(sorted(active_roots)), active_locator[-1]
        ),
        "degree-ten active locator roots",
    )
    columns = [
        poly_mul(poly_pow(n_new, 6 - j), poly_pow(d_new, j))
        for j in range(7)
    ]
    matrix = coefficient_rows(columns, 61)
    active_rank = rank_mod(matrix)
    require(active_rank == 7, "degree-ten active symmetric-power rank")
    augmented = [
        row
        + [
            active_locator[index]
            if index < len(active_locator)
            else 0
        ]
        for index, row in enumerate(matrix)
    ]
    require(rank_mod(augmented) == 7, "degree-ten active membership")
    require(control["active_matrix_rank"] == 7, "active rank field")
    require(control["active_membership"] is True, "active membership field")
    require(
        control["source_points_all_finite_after_conjugation"] is True,
        "source finiteness field",
    )
    require(
        control["active_points_all_finite_after_conjugation"] is True,
        "active finiteness field",
    )

    control_partition = (
        (tuple(range(10)),),
        ((10, 11),),
    )
    require(
        any(
            partition == control_partition
            for partition in canonical_source_partitions(10, 1, 1)
        ),
        "degree-ten control source partition is not canonical",
    )
    source_points_ordered = [
        *(fp2(root) for root in transformed_by_value[243]),
        fp2(0),
        fp2(P - 1),
    ]
    classification = classify_source_template_fp2(
        source_points=source_points_ordered,
        partition=control_partition,
        m=10,
        n=6,
        active_locator=[fp2(value) for value in active_locator],
        strict_right_factor_degree=2,
    )
    require(
        classification
        == {
            "terminal": "STRICT_RIGHT_FACTOR_ROUTE",
            "source_rank": 2,
            "pencil_rank": 2,
            "active_rank": 7,
            "augmented_rank": 7,
        },
        "degree-ten per-template classifier",
    )


def verify_bindings(data: dict[str, Any]) -> None:
    require(data["source_bindings"] == EXPECTED_BINDINGS, "source bindings")
    for binding in data["source_bindings"]:
        commit = binding["commit"]
        path = binding["path"]
        git_output("cat-file", "-e", f"{commit}^{{commit}}")
        actual_blob = git_output("rev-parse", f"{commit}:{path}")
        require(
            actual_blob == binding["blob_oid"],
            f"blob binding mismatch: {binding['binding_id']}",
        )

    historical_parent = parse_json_text(
        git_output("show", f"{EXPECTED_PARENT_HEAD}:{EXPECTED_PARENT_PATH}"),
        "historical parent certificate",
    )
    require(
        payload_hash(historical_parent) == historical_parent["payload_sha256"],
        "historical parent self-hash",
    )
    require(
        historical_parent["payload_sha256"] == EXPECTED_PARENT_PAYLOAD,
        "historical parent payload",
    )
    require(
        historical_parent.get("conclusion", {}).get("status")
        == EXPECTED_PARENT_TERMINAL,
        "historical parent terminal",
    )


def verify_replays_and_nonclaims(data: dict[str, Any]) -> None:
    replays = data["independent_replays"]
    expected_sage = (
        "experimental/scripts/"
        "verify_kb_mca_v4_degree60_source_pencil_rank_compiler_v1.sage"
    )
    expected_wolfram = (
        "experimental/scripts/"
        "verify_kb_mca_v4_degree60_source_pencil_rank_compiler_v1.wl"
    )
    require(replays["sage"]["path"] == expected_sage, "Sage replay path")
    require(replays["wolfram"]["path"] == expected_wolfram, "Wolfram path")
    sage_path = REPO_ROOT / expected_sage
    wolfram_path = REPO_ROOT / expected_wolfram
    require(sage_path.is_file(), "Sage replay missing")
    require(wolfram_path.is_file(), "Wolfram replay missing")
    require(
        replays["sage"]["sha256"] == file_sha256(sage_path),
        "Sage replay hash",
    )
    require(
        replays["wolfram"]["sha256"] == file_sha256(wolfram_path),
        "Wolfram replay hash",
    )
    live = replays["live_wolfram_plugin"]
    require(live["profile_total"] == 32_099, "live Wolfram total")
    require(
        live["power_divisibility"]
        == {
            "2": True,
            "3": True,
            "4": True,
            "6": True,
            "10": False,
            "12": True,
        },
        "live Wolfram divisibility",
    )
    require(live["degree_ten_all_x_checks"] is True, "Wolfram x checks")
    require(live["degree_ten_all_z_checks"] is True, "Wolfram z checks")
    require(
        live["degree_ten_all_roots_distinct"] is True,
        "Wolfram root-distinctness check",
    )
    require(data["nonclaims"] == EXPECTED_NONCLAIMS, "nonclaims changed")
    conclusion = data["conclusion"]
    require(
        conclusion["terminal"] == "TRANSVERSE_OUTER_CORRESPONDENCE_UNPAID",
        "conclusion terminal",
    )
    require(
        conclusion["missing_theorem"]
        == (
            "uniform source-coupled outer-correspondence incidence or a "
            "same-record carrier/data/explaining-polynomial/slope bridge"
        ),
        "missing theorem",
    )
    require(conclusion["u2_closed"] is False, "u2 closure claimed")
    require(conclusion["K3_closed"] is False, "K3 closure claimed")
    require(conclusion["row_closed"] is False, "row closure claimed")


def verify_certificate(
    data: dict[str, Any], *, check_git_bindings: bool = True
) -> None:
    exact_schema(data)
    digest = data["payload_sha256"]
    require(
        isinstance(digest, str)
        and len(digest) == 64
        and all(character in "0123456789abcdef" for character in digest),
        "payload_sha256 is not a lowercase SHA-256 digest",
    )
    require(payload_hash(data) == digest, "payload hash mismatch")
    verify_statement_and_compiler(data)
    verify_canonical_template_enumeration()
    verify_degree_twelve_and_routes(data)
    verify_same_fiber_and_transverse(data)
    verify_power_controls(data)
    verify_degree_ten_control(data)
    if check_git_bindings:
        verify_bindings(data)
    else:
        require(data["source_bindings"] == EXPECTED_BINDINGS, "bindings")
    verify_replays_and_nonclaims(data)


def reseal(data: dict[str, Any]) -> None:
    data["payload_sha256"] = payload_hash(data)


def run_tamper_selftest(original: dict[str, Any]) -> int:
    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        (
            "template-count",
            lambda value: value["compiler"]["profiles"][0].__setitem__(
                "raw_templates", 10_394
            ),
        ),
        (
            "erase-degree-twelve-gate-exception",
            lambda value: value["compiler"].__setitem__(
                "source_gate", "rank(S_pi)=2"
            ),
        ),
        (
            "template-count-as-record-census",
            lambda value: value["statement"].__setitem__(
                "template_count_scope",
                "finite exhaustive census of all endpoint records",
            ),
        ),
        (
            "active-matrix-dimension",
            lambda value: value["compiler"]["profiles"][1].__setitem__(
                "active_matrix", [61, 20]
            ),
        ),
        (
            "right-route",
            lambda value: value["strict_right_factor_routing"]["routes"][
                "10"
            ].append(3),
        ),
        (
            "primitive-subdegree",
            lambda value: value["same_fiber_route_cut"][
                "small_degree_catalogue"
            ][4]["subdegree_rows"][0].__setitem__(1, 4),
        ),
        (
            "transverse-r-delta",
            lambda value: value["transverse_outer_terminal"]["rows"][3][
                "r_delta"
            ][0].__setitem__(1, 23),
        ),
        (
            "transverse-cover-degree-bound",
            lambda value: value["transverse_outer_terminal"].__setitem__(
                "cover_degree_upper_bound", "delta<=2*m^2"
            ),
        ),
        (
            "restore-impossible-m2-cover",
            lambda value: value["transverse_outer_terminal"]["rows"][0][
                "r_delta"
            ].insert(0, [1, 8]),
        ),
        (
            "sqrt-minus-one",
            lambda value: value["deployed_field_controls"].__setitem__(
                "sqrt_minus_one", 16_711_680
            ),
        ),
        (
            "power-zeta",
            lambda value: value["deployed_field_controls"]["power_controls"][
                1
            ].__setitem__("zeta", [1, 0]),
        ),
        (
            "power-route",
            lambda value: value["deployed_field_controls"][
                "composite_control_routes"
            ].__setitem__("12", 3),
        ),
        (
            "degree-ten-x-root",
            lambda value: value["deployed_field_controls"][
                "degree_ten_control"
            ]["fibers"][0]["x_roots"].__setitem__(0, 441_863_511),
        ),
        (
            "degree-ten-z-root",
            lambda value: value["deployed_field_controls"][
                "degree_ten_control"
            ]["fibers"][6]["z_roots"].__setitem__(9, 2_119_192_694),
        ),
        (
            "conjugation",
            lambda value: value["deployed_field_controls"][
                "degree_ten_control"
            ].__setitem__("coordinate_change", "old z=1/t"),
        ),
        (
            "exceptional-point",
            lambda value: value["deployed_field_controls"][
                "degree_ten_control"
            ]["exceptional_source_points_new_t"].__setitem__(1, 1),
        ),
        (
            "active-membership",
            lambda value: value["deployed_field_controls"][
                "degree_ten_control"
            ].__setitem__("active_membership", False),
        ),
        (
            "parent-payload",
            lambda value: value["parent_stack"].__setitem__(
                "certificate_payload_sha256", "0" * 64
            ),
        ),
        (
            "replay-hash",
            lambda value: value["independent_replays"]["sage"].__setitem__(
                "sha256", "0" * 64
            ),
        ),
        (
            "source-binding",
            lambda value: value["source_bindings"][0].__setitem__(
                "blob_oid", "0" * 40
            ),
        ),
        (
            "drop-nonclaim",
            lambda value: value["nonclaims"].pop(),
        ),
        (
            "claim-row-closed",
            lambda value: value["conclusion"].__setitem__("row_closed", True),
        ),
        (
            "extra-top-level-field",
            lambda value: value.__setitem__("unexpected", 1),
        ),
        (
            "extra-nested-field",
            lambda value: value["compiler"]["profiles"][0].__setitem__(
                "unexpected", 1
            ),
        ),
    ]
    passed = 0
    for name, mutate in mutations:
        candidate = copy.deepcopy(original)
        mutate(candidate)
        reseal(candidate)
        try:
            verify_certificate(candidate, check_git_bindings=False)
        except VerificationError:
            passed += 1
        else:
            raise VerificationError(f"tamper survived: {name}")

    bad_hash = copy.deepcopy(original)
    bad_hash["payload_sha256"] = "0" * 64
    try:
        verify_certificate(bad_hash, check_git_bindings=False)
    except VerificationError:
        passed += 1
    else:
        raise VerificationError("tamper survived: payload-hash")

    try:
        parse_json_text('{"duplicate":1,"duplicate":2}', "duplicate-key test")
    except VerificationError:
        passed += 1
    else:
        raise VerificationError("tamper survived: duplicate-json-key")
    return passed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify the committed certificate",
    )
    parser.add_argument(
        "--tamper-selftest",
        action="store_true",
        help="run fail-closed semantic mutation tests",
    )
    arguments = parser.parse_args()
    if not arguments.check and not arguments.tamper_selftest:
        parser.error("at least one of --check or --tamper-selftest is required")

    certificate = load_json(CERTIFICATE)
    verify_certificate(certificate, check_git_bindings=True)
    print(
        "PASS: degree-60 source-pencil compiler, strict routing, "
        "same-fiber route cut, transverse rows, and deployed-field controls"
    )
    if arguments.tamper_selftest:
        count = run_tamper_selftest(certificate)
        print(f"PASS: {count}/{count} tamper mutations rejected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
