#!/usr/bin/env python3
"""Verify a Paper D v12 regular Hankel-minor certificate toy row.

The certificate is intentionally small and exact:

    F = F_17
    D = F_17^*
    n = 16
    k = 8
    agreement threshold a = 13

For exact agreements A=13,14,15,16 the overdetermined condition
``t=A-k >= j+1=n-A+1`` holds.  The verifier constructs deterministic line
syndromes u,v, supplies one regular maximal minor for each exact agreement,
and independently enumerates all split co-supports of the corresponding size
to check that every finite noncontained bad slope is a root of the minor.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from hashlib import sha256
import json
from itertools import combinations, permutations
from pathlib import Path
from typing import Any


P = 17
N = 16
K = 8
R = N - K
AGREEMENT_THRESHOLD = 13
DOMAIN = tuple(range(1, P))
CERTIFICATE_PATH = Path(
    "experimental/data/certificates/aperiodic-hankel-regular-minor-toy/"
    "f17_n16_k8_a13_regular_minor_certificate.json"
)


def mod(value: int) -> int:
    return value % P


def trim(poly: list[int]) -> list[int]:
    out = [mod(x) for x in poly]
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def poly_add(left: list[int], right: list[int]) -> list[int]:
    size = max(len(left), len(right))
    out = [0] * size
    for index in range(size):
        out[index] = mod(
            (left[index] if index < len(left) else 0)
            + (right[index] if index < len(right) else 0)
        )
    return trim(out)


def poly_mul(left: list[int], right: list[int]) -> list[int]:
    out = [0] * (len(left) + len(right) - 1)
    for i, a_i in enumerate(left):
        for j, b_j in enumerate(right):
            out[i + j] = mod(out[i + j] + a_i * b_j)
    return trim(out)


def poly_eval(poly: list[int], value: int) -> int:
    total = 0
    power = 1
    for coeff in poly:
        total = mod(total + coeff * power)
        power = mod(power * value)
    return total


def poly_degree(poly: list[int]) -> int:
    return len(trim(poly)) - 1


def determinant_poly(matrix: list[list[list[int]]]) -> list[int]:
    size = len(matrix)
    total = [0]
    for perm in permutations(range(size)):
        inversions = sum(
            1
            for i in range(size)
            for j in range(i + 1, size)
            if perm[i] > perm[j]
        )
        term = [1]
        for row, col in enumerate(perm):
            term = poly_mul(term, matrix[row][col])
        if inversions % 2:
            term = [mod(-coeff) for coeff in term]
        total = poly_add(total, term)
    return trim(total)


def syndrome_vectors() -> tuple[list[int], list[int]]:
    """Deterministic non-special line syndromes over F_17."""
    u = [mod(3 + 5 * m + 2 * m * m + m * m * m) for m in range(R)]
    v = [mod(7 + 4 * m + 6 * m * m + 3 * m * m * m) for m in range(R)]
    return u, v


def hankel_entry(w: list[int], row: int, col: int) -> int:
    return w[row + col]


def hankel_minor_polynomial(
    u: list[int], v: list[int], exact_agreement: int, row_set: list[int]
) -> list[int]:
    j = N - exact_agreement
    matrix: list[list[list[int]]] = []
    for row in row_set:
        matrix_row: list[list[int]] = []
        for col in range(j + 1):
            matrix_row.append([hankel_entry(u, row, col), hankel_entry(v, row, col)])
        matrix.append(matrix_row)
    return determinant_poly(matrix)


def locator_coefficients(roots: tuple[int, ...]) -> list[int]:
    coeffs = [1]
    for root in roots:
        coeffs = poly_mul(coeffs, [mod(-root), 1])
    return coeffs


def hankel_times_locator(w: list[int], t: int, locator: list[int]) -> list[int]:
    j = len(locator) - 1
    return [
        mod(sum(w[row + col] * locator[col] for col in range(j + 1)))
        for row in range(t)
    ]


def finite_bad_slopes_for_exact_agreement(
    u: list[int], v: list[int], exact_agreement: int
) -> list[int]:
    j = N - exact_agreement
    t = exact_agreement - K
    slopes: set[int] = set()
    for roots in combinations(DOMAIN, j):
        locator = locator_coefficients(roots)
        a_vec = hankel_times_locator(u, t, locator)
        b_vec = hankel_times_locator(v, t, locator)
        if all(value == 0 for value in b_vec):
            continue
        candidate = None
        consistent = True
        for a_i, b_i in zip(a_vec, b_vec):
            if b_i == 0:
                if a_i != 0:
                    consistent = False
                    break
                continue
            slope = mod(-a_i * pow(b_i, -1, P))
            if candidate is None:
                candidate = slope
            elif candidate != slope:
                consistent = False
                break
        if consistent and candidate is not None:
            if any(mod(a_i + candidate * b_i) != 0 for a_i, b_i in zip(a_vec, b_vec)):
                raise AssertionError(("bad candidate", exact_agreement, roots, candidate))
            slopes.add(candidate)
    return sorted(slopes)


def hash_json(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return sha256(payload).hexdigest()


@dataclass(frozen=True)
class AgreementCertificate:
    exact_agreement: int
    j: int
    t: int
    row_set: list[int]
    polynomial: list[int]
    roots: list[int]
    enumerated_bad_slopes: list[int]

    @property
    def degree(self) -> int:
        return poly_degree(self.polynomial)


def build_agreement_certificate(
    u: list[int], v: list[int], exact_agreement: int
) -> AgreementCertificate:
    j = N - exact_agreement
    t = exact_agreement - K
    if t < j + 1:
        raise AssertionError(("not overdetermined", exact_agreement, j, t))
    row_set = list(range(j + 1))
    polynomial = hankel_minor_polynomial(u, v, exact_agreement, row_set)
    if all(coeff == 0 for coeff in polynomial):
        raise AssertionError(("zero regular minor", exact_agreement))
    roots = [value for value in range(P) if poly_eval(polynomial, value) == 0]
    bad_slopes = finite_bad_slopes_for_exact_agreement(u, v, exact_agreement)
    missing = sorted(set(bad_slopes) - set(roots))
    if missing:
        raise AssertionError(("root containment failed", exact_agreement, missing))
    if poly_degree(polynomial) > j + 1:
        raise AssertionError(("degree bound failed", exact_agreement, polynomial))
    return AgreementCertificate(
        exact_agreement=exact_agreement,
        j=j,
        t=t,
        row_set=row_set,
        polynomial=polynomial,
        roots=roots,
        enumerated_bad_slopes=bad_slopes,
    )


def build_certificate() -> dict[str, Any]:
    u, v = syndrome_vectors()
    agreements = [
        build_agreement_certificate(u, v, exact_agreement)
        for exact_agreement in range(AGREEMENT_THRESHOLD, N + 1)
    ]
    root_union = sorted({root for agreement in agreements for root in agreement.roots})
    bad_union = sorted(
        {
            slope
            for agreement in agreements
            for slope in agreement.enumerated_bad_slopes
        }
    )
    if not set(bad_union).issubset(root_union):
        raise AssertionError(("closed-range containment failed", bad_union, root_union))

    return {
        "schema_version": "aperiodic-hankel-eliminant-v1",
        "row": {
            "n": N,
            "k": K,
            "field": "F_17",
            "domain_hash": hash_json(list(DOMAIN)),
            "domain_description": "sorted nonzero elements of F_17",
        },
        "agreement_threshold": AGREEMENT_THRESHOLD,
        "sampler": "finite_affine_line",
        "line_syndrome": {
            "u": u,
            "v": v,
            "description": (
                "deterministic toy syndrome pair; entries are cubic polynomials "
                "in the syndrome index modulo 17"
            ),
        },
        "removed_ledgers": [],
        "exact_agreements": [
            {
                "A": agreement.exact_agreement,
                "j": agreement.j,
                "t": agreement.t,
                "status": "regular_minor",
                "regular_minor": {
                    "row_set": agreement.row_set,
                    "polynomial_ref": (
                        "inline:regular_minor.coefficients_mod_17_ascending"
                    ),
                    "degree": agreement.degree,
                    "root_hash": hash_json(agreement.roots),
                },
                "regular_minor_data": {
                    "coefficients_mod_17_ascending": agreement.polynomial,
                    "roots_mod_17": agreement.roots,
                    "enumerated_bad_slopes_mod_17": agreement.enumerated_bad_slopes,
                },
            }
            for agreement in agreements
        ],
        "declared_aperiodic_numerator": len(root_union),
        "root_union_table_ref": "inline:root_union_mod_17",
        "root_union_mod_17": root_union,
        "enumerated_bad_slope_union_mod_17": bad_union,
        "status": "PROVED",
        "nonclaims": [
            "not a prize-row certificate",
            "not a quotient/tangent removal theorem",
            "not a full M1 aperiodic local-limit theorem",
            "certificate is for one deterministic toy syndrome pair",
        ],
    }


def validate_certificate_shape(certificate: dict[str, Any]) -> None:
    required = {
        "schema_version",
        "row",
        "agreement_threshold",
        "removed_ledgers",
        "exact_agreements",
    }
    missing = required - set(certificate)
    if missing:
        raise AssertionError(("missing top-level fields", sorted(missing)))
    if certificate["schema_version"] != "aperiodic-hankel-eliminant-v1":
        raise AssertionError(("bad schema version", certificate["schema_version"]))
    row = certificate["row"]
    for field in ("n", "k", "field", "domain_hash"):
        if field not in row:
            raise AssertionError(("missing row field", field))
    for item in certificate["exact_agreements"]:
        for field in ("A", "j", "t", "status"):
            if field not in item:
                raise AssertionError(("missing exact-agreement field", field, item))
        if item["j"] != row["n"] - item["A"]:
            raise AssertionError(("bad j", item))
        if item["t"] != item["A"] - row["k"]:
            raise AssertionError(("bad t", item))
        if item["status"] != "regular_minor":
            raise AssertionError(("unexpected status", item))
        minor = item.get("regular_minor")
        data = item.get("regular_minor_data")
        if not minor or not data:
            raise AssertionError(("missing regular minor data", item))
        if minor["degree"] != poly_degree(data["coefficients_mod_17_ascending"]):
            raise AssertionError(("degree mismatch", item))
        if minor["degree"] > item["j"] + 1:
            raise AssertionError(("regular degree bound", item))
        if minor["root_hash"] != hash_json(data["roots_mod_17"]):
            raise AssertionError(("root hash mismatch", item))
        if not set(data["enumerated_bad_slopes_mod_17"]).issubset(
            data["roots_mod_17"]
        ):
            raise AssertionError(("root containment", item))


def render(certificate: dict[str, Any]) -> str:
    return json.dumps(certificate, indent=2, sort_keys=True) + "\n"


def check_certificate(path: Path) -> None:
    expected = render(build_certificate())
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"certificate mismatch: {path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", type=Path, help="write deterministic certificate")
    parser.add_argument("--check", type=Path, help="check deterministic certificate")
    parser.add_argument("--json", action="store_true", help="print certificate JSON")
    args = parser.parse_args()

    certificate = build_certificate()
    validate_certificate_shape(certificate)

    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(render(certificate), encoding="utf-8")
    if args.check:
        check_certificate(args.check)
    if args.json:
        print(render(certificate), end="")
        return

    print("Paper D v12 regular Hankel-minor toy certificate")
    print(f"row: F_17, n={N}, k={K}, threshold a={AGREEMENT_THRESHOLD}")
    print(f"domain_hash={certificate['row']['domain_hash']}")
    for item in certificate["exact_agreements"]:
        data = item["regular_minor_data"]
        print(
            "A={A} j={j} t={t} degree={degree} roots={roots} bad={bad}".format(
                A=item["A"],
                j=item["j"],
                t=item["t"],
                degree=item["regular_minor"]["degree"],
                roots=data["roots_mod_17"],
                bad=data["enumerated_bad_slopes_mod_17"],
            )
        )
    print(f"declared_aperiodic_numerator={certificate['declared_aperiodic_numerator']}")
    print("regular Hankel-minor certificate checks passed")


if __name__ == "__main__":
    main()
