#!/usr/bin/env python3
"""Extract regular overdetermined Hankel-minor certificates from row data.

This is the first reusable M3 extractor for the Paper D v9 atlas.  It reads a
prime-field syndrome-pencil input, tries candidate maximal Hankel row minors
for each exact agreement, and emits an ``aperiodic-hankel-eliminant-v1`` packet.

The determinant polynomial is recovered by interpolation from numeric
determinants, avoiding the factorial permutation determinant used by the first
hard-coded toy verifier.  The current implementation is intentionally limited
to prime fields ``F_p``; extension-field row adapters are a later M3/F1 task.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from hashlib import sha256
import json
from itertools import combinations
from pathlib import Path
from typing import Any


DEFAULT_MAX_ROOT_ENUM_FIELD_SIZE = 10000
DEFAULT_MAX_BAD_SLOPE_SUBSETS = 200000


def mod(value: int, prime: int) -> int:
    return value % prime


def trim(poly: list[int], prime: int) -> list[int]:
    out = [mod(coeff, prime) for coeff in poly]
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def poly_add(left: list[int], right: list[int], prime: int) -> list[int]:
    size = max(len(left), len(right))
    out = [0] * size
    for index in range(size):
        out[index] = (
            (left[index] if index < len(left) else 0)
            + (right[index] if index < len(right) else 0)
        ) % prime
    return trim(out, prime)


def poly_mul(left: list[int], right: list[int], prime: int) -> list[int]:
    out = [0] * (len(left) + len(right) - 1)
    for i, left_coeff in enumerate(left):
        for j, right_coeff in enumerate(right):
            out[i + j] = (out[i + j] + left_coeff * right_coeff) % prime
    return trim(out, prime)


def poly_scale(poly: list[int], scalar: int, prime: int) -> list[int]:
    return trim([(scalar * coeff) % prime for coeff in poly], prime)


def poly_eval(poly: list[int], value: int, prime: int) -> int:
    total = 0
    power = 1
    for coeff in poly:
        total = (total + coeff * power) % prime
        power = (power * value) % prime
    return total


def poly_degree(poly: list[int], prime: int) -> int:
    return len(trim(poly, prime)) - 1


def hash_json(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return sha256(payload).hexdigest()


def hash_file(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def optional_file_hash(path_text: str | None) -> str | None:
    if path_text is None:
        return None
    path = Path(path_text)
    if not path.exists():
        return None
    return hash_file(path)


def parse_prime_field(field_name: str) -> int:
    if not (field_name.startswith("F_") and field_name[2:].isdigit()):
        raise ValueError(f"only prime fields F_p are supported, got {field_name!r}")
    prime = int(field_name[2:])
    if prime < 2:
        raise ValueError("field prime must be at least 2")
    return prime


def determinant_mod(matrix: list[list[int]], prime: int) -> int:
    """Return det(matrix) over F_prime by Gaussian elimination."""
    size = len(matrix)
    work = [[entry % prime for entry in row] for row in matrix]
    det = 1
    for col in range(size):
        pivot = None
        for row in range(col, size):
            if work[row][col] % prime:
                pivot = row
                break
        if pivot is None:
            return 0
        if pivot != col:
            work[col], work[pivot] = work[pivot], work[col]
            det = (-det) % prime
        pivot_value = work[col][col] % prime
        det = (det * pivot_value) % prime
        inv_pivot = pow(pivot_value, -1, prime)
        for row in range(col + 1, size):
            factor = (work[row][col] * inv_pivot) % prime
            if factor == 0:
                continue
            for entry_col in range(col, size):
                work[row][entry_col] = (
                    work[row][entry_col] - factor * work[col][entry_col]
                ) % prime
    return det % prime


def interpolate(points: list[tuple[int, int]], prime: int) -> list[int]:
    """Interpolate the unique degree < len(points) polynomial over F_prime."""
    out = [0]
    for index, (x_i, y_i) in enumerate(points):
        basis = [1]
        denominator = 1
        for other_index, (x_j, _y_j) in enumerate(points):
            if other_index == index:
                continue
            basis = poly_mul(basis, [(-x_j) % prime, 1], prime)
            denominator = (denominator * (x_i - x_j)) % prime
        scale = y_i * pow(denominator, -1, prime)
        out = poly_add(out, poly_scale(basis, scale, prime), prime)
    return trim(out, prime)


def matrix_at_slope(
    u: list[int],
    v: list[int],
    row_set: list[int],
    cols: int,
    slope: int,
    prime: int,
) -> list[list[int]]:
    return [
        [(u[row + col] + slope * v[row + col]) % prime for col in range(cols)]
        for row in row_set
    ]


def determinant_polynomial_by_interpolation(
    u: list[int],
    v: list[int],
    row_set: list[int],
    cols: int,
    prime: int,
) -> list[int]:
    degree_bound = cols
    if prime <= degree_bound:
        raise ValueError(
            f"need prime > degree bound for base-field interpolation, got {prime} <= {degree_bound}"
        )
    points = []
    for slope in range(degree_bound + 1):
        det = determinant_mod(matrix_at_slope(u, v, row_set, cols, slope, prime), prime)
        points.append((slope, det))
    poly = interpolate(points, prime)
    for slope, det in points:
        if poly_eval(poly, slope, prime) != det:
            raise AssertionError(("interpolation check failed", slope, det, poly))
    return poly


def locator_coefficients(roots: tuple[int, ...], prime: int) -> list[int]:
    coeffs = [1]
    for root in roots:
        coeffs = poly_mul(coeffs, [(-root) % prime, 1], prime)
    return coeffs


def hankel_times_locator(
    syndrome: list[int], t: int, locator: list[int], prime: int
) -> list[int]:
    j = len(locator) - 1
    return [
        sum(syndrome[row + col] * locator[col] for col in range(j + 1)) % prime
        for row in range(t)
    ]


def finite_bad_slopes_for_exact_agreement(
    u: list[int],
    v: list[int],
    domain: list[int],
    n: int,
    k: int,
    exact_agreement: int,
    prime: int,
) -> list[int]:
    j = n - exact_agreement
    t = exact_agreement - k
    slopes: set[int] = set()
    for roots in combinations(domain, j):
        locator = locator_coefficients(roots, prime)
        a_vec = hankel_times_locator(u, t, locator, prime)
        b_vec = hankel_times_locator(v, t, locator, prime)
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
            slope = (-a_i * pow(b_i, -1, prime)) % prime
            if candidate is None:
                candidate = slope
            elif candidate != slope:
                consistent = False
                break
        if consistent and candidate is not None:
            slopes.add(candidate)
    return sorted(slopes)


def n_choose_k(n: int, k: int) -> int:
    if k < 0 or k > n:
        return 0
    k = min(k, n - k)
    numerator = 1
    denominator = 1
    for value in range(1, k + 1):
        numerator *= n - k + value
        denominator *= value
    return numerator // denominator


@dataclass(frozen=True)
class ExtractionResult:
    exact_agreement: int
    j: int
    t: int
    status: str
    row_set: list[int] | None
    polynomial: list[int] | None
    roots: list[int] | None
    enumerated_bad_slopes: list[int] | None
    tested_row_sets: int
    residual_label: str | None = None
    residual_reason: str | None = None


def candidate_row_sets(t: int, size: int, config: dict[str, Any]) -> list[list[int]]:
    explicit = config.get("candidate_row_sets")
    if explicit is not None:
        rows = [[int(value) for value in row_set] for row_set in explicit]
    else:
        strategy = config.get("type", "prefix")
        if strategy == "prefix":
            rows = [list(range(size))]
        elif strategy == "contiguous":
            limit = int(config.get("limit", max(0, t - size + 1)))
            rows = [
                list(range(start, start + size))
                for start in range(max(0, t - size + 1))
            ][:limit]
        else:
            raise ValueError(f"unknown row_set_strategy {strategy!r}")
    for row_set in rows:
        if len(row_set) != size:
            raise ValueError(("bad row_set size", row_set, size))
        if len(set(row_set)) != len(row_set):
            raise ValueError(("duplicate row in row_set", row_set))
        if min(row_set) < 0 or max(row_set) >= t:
            raise ValueError(("row_set outside Hankel row range", row_set, t))
    return rows


def extract_for_agreement(
    spec: dict[str, Any],
    exact_agreement: int,
    prime: int,
) -> ExtractionResult:
    row = spec["row"]
    n = int(row["n"])
    k = int(row["k"])
    u = [value % prime for value in spec["line_syndrome"]["u"]]
    v = [value % prime for value in spec["line_syndrome"]["v"]]
    j = n - exact_agreement
    t = exact_agreement - k
    size = j + 1
    if t < size:
        return ExtractionResult(
            exact_agreement,
            j,
            t,
            "residual_obstruction",
            None,
            None,
            None,
            None,
            0,
            residual_label="unknown",
            residual_reason="regular overdetermined condition t>=j+1 fails",
        )
    if len(u) < t + j or len(v) < t + j:
        raise ValueError(
            f"syndrome length must be at least t+j={t + j} for A={exact_agreement}"
        )

    row_config = spec.get("row_set_strategy", {"type": "prefix"})
    tested = 0
    for row_set in candidate_row_sets(t, size, row_config):
        tested += 1
        polynomial = determinant_polynomial_by_interpolation(
            u, v, row_set, size, prime
        )
        if any(coeff % prime for coeff in polynomial):
            roots: list[int] | None = None
            bad_slopes: list[int] | None = None
            if prime <= int(
                spec.get("max_root_enum_field_size", DEFAULT_MAX_ROOT_ENUM_FIELD_SIZE)
            ):
                roots = [
                    value
                    for value in range(prime)
                    if poly_eval(polynomial, value, prime) == 0
                ]
            domain = spec.get("row", {}).get("domain")
            if domain is not None and spec.get("enumerate_split_bad_slopes", False):
                domain_values = [int(value) % prime for value in domain]
                subset_count = n_choose_k(len(domain_values), j)
                if subset_count <= int(
                    spec.get(
                        "max_bad_slope_subsets", DEFAULT_MAX_BAD_SLOPE_SUBSETS
                    )
                ):
                    bad_slopes = finite_bad_slopes_for_exact_agreement(
                        u,
                        v,
                        domain_values,
                        n,
                        k,
                        exact_agreement,
                        prime,
                    )
                    if roots is not None and not set(bad_slopes).issubset(roots):
                        raise AssertionError(
                            ("bad slopes not contained in roots", exact_agreement)
                        )
            return ExtractionResult(
                exact_agreement,
                j,
                t,
                "regular_minor",
                row_set,
                polynomial,
                roots,
                bad_slopes,
                tested,
            )

    return ExtractionResult(
        exact_agreement,
        j,
        t,
        "residual_obstruction",
        None,
        None,
        None,
        None,
        tested,
        residual_label="unknown",
        residual_reason="all tested regular maximal minors vanished",
    )


def result_to_packet_item(result: ExtractionResult, prime: int) -> dict[str, Any]:
    item: dict[str, Any] = {
        "A": result.exact_agreement,
        "j": result.j,
        "t": result.t,
        "status": result.status,
    }
    if result.status == "regular_minor":
        assert result.row_set is not None
        assert result.polynomial is not None
        degree = poly_degree(result.polynomial, prime)
        roots = result.roots
        item["regular_minor"] = {
            "row_set": result.row_set,
            "polynomial_ref": (
                f"inline:regular_minor.coefficients_mod_{prime}_ascending"
            ),
            "degree": degree,
            "root_hash": hash_json(
                roots
                if roots is not None
                else {
                    "roots": "not_enumerated",
                    "degree_bound": degree,
                    "row_set": result.row_set,
                }
            ),
        }
        item["regular_minor_polynomial_data"] = {
            f"coefficients_mod_{prime}_ascending": result.polynomial
        }
        if roots is not None:
            item["regular_minor_data"] = {
                f"coefficients_mod_{prime}_ascending": result.polynomial,
                f"roots_mod_{prime}": roots,
            }
            if result.enumerated_bad_slopes is not None:
                item["regular_minor_data"][
                    f"enumerated_bad_slopes_mod_{prime}"
                ] = result.enumerated_bad_slopes
        item["extractor_audit"] = {
            "tested_row_sets": result.tested_row_sets,
            "root_count": len(roots) if roots is not None else "not_enumerated",
            "degree_bound": degree,
        }
    else:
        item["residual_label"] = result.residual_label or "unknown"
        item["residual_reason"] = result.residual_reason
        item["extractor_audit"] = {"tested_row_sets": result.tested_row_sets}
    return item


def build_packet(spec: dict[str, Any], input_ref: str | None = None) -> dict[str, Any]:
    row = spec["row"]
    prime = parse_prime_field(row["field"])
    agreements = [int(value) for value in spec["exact_agreements"]]
    results = [extract_for_agreement(spec, agreement, prime) for agreement in agreements]
    all_roots_enumerated = all(
        result.status == "regular_minor" and result.roots is not None
        for result in results
    )
    root_union = sorted(
        {
            root
            for result in results
            if result.roots is not None
            for root in result.roots
        }
    )
    bad_union = sorted(
        {
            slope
            for result in results
            if result.enumerated_bad_slopes is not None
            for slope in result.enumerated_bad_slopes
        }
    )
    if bad_union and not set(bad_union).issubset(root_union):
        raise AssertionError(("closed-range bad slopes not contained in roots"))

    packet: dict[str, Any] = {
        "schema_version": "aperiodic-hankel-eliminant-v1",
        "row": {
            "n": int(row["n"]),
            "k": int(row["k"]),
            "field": row["field"],
            "domain_hash": row.get("domain_hash")
            or hash_json(row.get("domain", row.get("domain_description", ""))),
            "domain_description": row.get(
                "domain_description", "domain supplied in extractor input"
            ),
        },
        "agreement_threshold": int(spec.get("agreement_threshold", min(agreements))),
        "sampler": spec.get("sampler", "finite_affine_line"),
        "removed_ledgers": spec.get("removed_ledgers", []),
        "exact_agreements": [
            result_to_packet_item(result, prime) for result in results
        ],
        "extractor": {
            "name": "regular-hankel-minor-extractor",
            "method": "numeric determinant interpolation over the base prime field",
            "input_ref": input_ref,
            "input_sha256": optional_file_hash(input_ref),
            "row_set_strategy": spec.get("row_set_strategy", {"type": "prefix"}),
            "scope": "prime-field syndrome pencils only",
        },
        "status": spec.get("status", "EXPERIMENTAL"),
        "nonclaims": spec.get(
            "nonclaims",
            [
                "not a prize-row threshold theorem",
                "not an extension-field row adapter",
                "not a singular pivot-chart certificate",
            ],
        ),
    }
    if all_roots_enumerated:
        packet["declared_aperiodic_numerator"] = len(root_union)
        packet["root_union_table_ref"] = f"inline:root_union_mod_{prime}"
        packet[f"root_union_mod_{prime}"] = root_union
        packet[f"enumerated_bad_slope_union_mod_{prime}"] = bad_union
    else:
        packet["root_union_table_ref"] = "not_enumerated"
        packet["regular_root_bound_sum"] = sum(
            poly_degree(result.polynomial, prime)
            for result in results
            if result.status == "regular_minor" and result.polynomial is not None
        )
    return packet


def render(packet: dict[str, Any]) -> str:
    return json.dumps(packet, indent=2, sort_keys=True) + "\n"


def check_packet(spec_path: Path, packet_path: Path) -> None:
    expected = render(build_packet(load_json(spec_path), str(spec_path)))
    actual = packet_path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"packet mismatch: {packet_path}")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def print_summary(packet: dict[str, Any]) -> None:
    print("regular Hankel-minor extractor")
    print(
        "row: {field}, n={n}, k={k}, threshold={threshold}".format(
            field=packet["row"]["field"],
            n=packet["row"]["n"],
            k=packet["row"]["k"],
            threshold=packet["agreement_threshold"],
        )
    )
    for item in packet["exact_agreements"]:
        if item["status"] == "regular_minor":
            data = item.get("regular_minor_data", {})
            root_keys = [key for key in data if key.startswith("roots_mod_")]
            roots: list[int] | str = data[root_keys[0]] if root_keys else "not_enumerated"
            print(
                "A={A} j={j} t={t} row_set={row_set} degree={degree} "
                "roots={roots} tested={tested}".format(
                    A=item["A"],
                    j=item["j"],
                    t=item["t"],
                    row_set=item["regular_minor"]["row_set"],
                    degree=item["regular_minor"]["degree"],
                    roots=roots,
                    tested=item["extractor_audit"]["tested_row_sets"],
                )
            )
        else:
            print(
                "A={A} j={j} t={t} residual={label} tested={tested}".format(
                    A=item["A"],
                    j=item["j"],
                    t=item["t"],
                    label=item.get("residual_label"),
                    tested=item["extractor_audit"]["tested_row_sets"],
                )
            )
    if "declared_aperiodic_numerator" in packet:
        print(f"declared_aperiodic_numerator={packet['declared_aperiodic_numerator']}")
    else:
        print(f"regular_root_bound_sum={packet.get('regular_root_bound_sum')}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path, help="regular-minor extractor input JSON")
    parser.add_argument("--write", type=Path, help="write deterministic v9 packet")
    parser.add_argument("--check", type=Path, help="check deterministic v9 packet")
    parser.add_argument("--json", action="store_true", help="print packet JSON")
    args = parser.parse_args()

    spec = load_json(args.input)
    packet = build_packet(spec, str(args.input))

    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(render(packet), encoding="utf-8")
    if args.check:
        check_packet(args.input, args.check)
    if args.json:
        print(render(packet), end="")
        return
    print_summary(packet)


if __name__ == "__main__":
    main()
