#!/usr/bin/env python3
"""Search the M3 low-rank endpoint-capacity spectral target.

This is a counterexample-first utility for PR #170's normalized low-rank target:

    gcd(Phi_{m,r,0}, Phi_{m,r,1}) = 1,

where Phi_{m,r,h}=det(I+Z K_h) for the consecutive F_17^32 subgroup window.
With --shift-mode all-contiguous it instead probes the weaker contiguous-shift
target gcd(Phi_{m,r,h}: 0 <= h < 258-2m)=1, stopping once the running gcd is
constant.  It deliberately does not write a certificate.  Use it to probe ranks
beyond the current low-rank2..12 packet before deciding whether a larger packet
is worth emitting.

For ranks below the characteristic it uses the fast Newton-identity coefficient
routine from the certified packet.  At rank 17 and above it switches to
determinant interpolation, avoiding division by zero in characteristic 17.
"""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
import sys
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

SEARCH_SCRIPT_REF = "experimental/scripts/search_f17_32_m3_low_rank_spectral_target.py"

from experimental.scripts.extract_regular_hankel_minors import (  # noqa: E402
    PolynomialBasisField,
    determinant_field,
    fpoly_degree,
    fpoly_eval,
    fpoly_gcd,
    hash_json,
    interpolate_field,
    render,
)
from experimental.scripts import (  # noqa: E402
    verify_f17_32_m3_low_rank2_12_v10_affine_gcd as packet,
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--agreement-min",
        type=int,
        default=426,
        help="minimum exact agreement A to probe; default is first frontier probe 426",
    )
    parser.add_argument(
        "--agreement-max",
        type=int,
        default=426,
        help="maximum exact agreement A to probe; default is first frontier probe 426",
    )
    parser.add_argument(
        "--rank-min",
        type=int,
        default=13,
        help="minimum low-rank update size to probe; default is first uncertified rank 13",
    )
    parser.add_argument(
        "--rank-max",
        type=int,
        default=13,
        help="maximum low-rank update size to probe; default is first uncertified rank 13",
    )
    parser.add_argument(
        "--stop-on-collision",
        action="store_true",
        help="stop at the first positive common gcd degree",
    )
    parser.add_argument(
        "--shift-mode",
        choices=["adjacent", "all-contiguous"],
        default="adjacent",
        help=(
            "which shifted minors to gcd: adjacent keeps the saved h=0,1 "
            "target; all-contiguous uses every available contiguous shift and "
            "stops once the running gcd is constant"
        ),
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="print the full probe record JSON instead of the compact summary",
    )
    parser.add_argument("--write", type=Path, help="write deterministic probe JSON")
    parser.add_argument("--check", type=Path, help="check deterministic probe JSON")
    return parser.parse_args()


def validate_range(
    agreement_min: int,
    agreement_max: int,
    rank_min: int,
    rank_max: int,
) -> None:
    require(
        packet.AGREEMENT_MIN <= agreement_min <= agreement_max <= packet.AGREEMENT_MAX,
        "agreement range must lie inside the PR #170 M3 window",
    )
    require(1 <= rank_min <= rank_max, "rank range must be nonempty")
    require(
        rank_max <= packet.N - agreement_min + 1,
        "rank_max exceeds available consecutive update nodes",
    )


def probe_records(
    agreement_min: int,
    agreement_max: int,
    rank_min: int,
    rank_max: int,
    stop_on_collision: bool,
    shift_mode: str,
) -> dict[str, Any]:
    row_descriptor = packet.load_json(packet.ROW_DESCRIPTOR_REF)
    field = packet.field_from_descriptor(row_descriptor)
    domain = [
        field.decode(value)
        for value in row_descriptor["domain"]["domain_encodings"]
    ]
    require(len(domain) == packet.N, "domain length")
    require(all(not field.is_zero(node) for node in domain), "domain contains zero")

    ranks = list(range(rank_min, rank_max + 1))
    base_nodes: list[tuple[int, ...]] = []
    denominators: list[tuple[int, ...]] = []
    base_determinant = field.one
    base_product = field.one
    records: list[dict[str, Any]] = []
    gcd_histogram: Counter[int] = Counter()
    degree_failures = 0
    parameters = {
        "agreement_min": agreement_min,
        "agreement_max": agreement_max,
        "rank_min": rank_min,
        "rank_max": rank_max,
        "stop_on_collision": stop_on_collision,
    }
    if shift_mode != "adjacent":
        parameters["shift_mode"] = shift_mode

    for size in range(1, packet.N - agreement_min + 2):
        new_node = domain[size - 1]
        new_denominator = field.one
        for old_node in base_nodes:
            new_denominator = field.mul(
                new_denominator,
                field.sub(new_node, old_node),
            )
        for index, old_node in enumerate(base_nodes):
            denominators[index] = field.mul(
                denominators[index],
                field.sub(old_node, new_node),
            )
        denominators.append(new_denominator)
        base_nodes.append(new_node)
        base_determinant = field.mul(
            base_determinant,
            field.mul(new_denominator, new_denominator),
        )
        base_product = field.mul(base_product, new_node)

        agreement = packet.N - size + 1
        if not (agreement_min <= agreement <= agreement_max):
            continue

        j = packet.N - agreement
        t = agreement - packet.K
        shift_count = t - j
        require(size == j + 1, f"A={agreement}: size mismatch")
        require(shift_count >= 2, f"A={agreement}: shifted rows unavailable")

        update_nodes = domain[size : size + rank_max]
        basis_values = packet.lagrange_basis_values(
            field,
            base_nodes,
            denominators,
            update_nodes,
        )
        kernel_cache: dict[int, tuple[list[list[tuple[int, ...]]], tuple[int, ...]]] = {}

        def shifted_kernel_and_scale(
            shift: int,
        ) -> tuple[list[list[tuple[int, ...]]], tuple[int, ...]]:
            if shift not in kernel_cache:
                kernel_cache[shift] = (
                    packet.weighted_kernel(
                        field,
                        basis_values,
                        [field.pow(node, -shift) for node in base_nodes],
                        [field.pow(node, shift) for node in update_nodes],
                    ),
                    field.mul(base_determinant, field.pow(base_product, shift)),
                )
            return kernel_cache[shift]

        for rank in ranks:
            if shift_mode == "adjacent":
                record, common_degree, degree_failed = adjacent_record(
                    field,
                    agreement,
                    size,
                    rank,
                    shifted_kernel_and_scale,
                )
            else:
                record, common_degree, degree_failed = all_contiguous_record(
                    field,
                    agreement,
                    size,
                    rank,
                    shift_count,
                    shifted_kernel_and_scale,
                )
            if degree_failed:
                degree_failures += 1
            gcd_histogram[common_degree] += 1
            records.append(record)
            if stop_on_collision and common_degree > 0:
                return summary(
                    row_descriptor,
                    parameters,
                    records,
                    gcd_histogram,
                    degree_failures,
                )

    return summary(
        row_descriptor,
        parameters,
        records,
        gcd_histogram,
        degree_failures,
    )


def adjacent_record(
    field: PolynomialBasisField,
    agreement: int,
    size: int,
    rank: int,
    shifted_kernel_and_scale,
) -> tuple[dict[str, Any], int, bool]:
    prefix_kernel, prefix_scale = shifted_kernel_and_scale(0)
    shifted_kernel, shifted_scale = shifted_kernel_and_scale(1)
    prefix_coefficients, prefix_method = determinant_coefficients_from_kernel(
        field,
        prefix_kernel,
        rank,
        prefix_scale,
    )
    shifted_coefficients, shifted_method = determinant_coefficients_from_kernel(
        field,
        shifted_kernel,
        rank,
        shifted_scale,
    )
    require(prefix_method == shifted_method, "coefficient method mismatch")
    prefix_degree = fpoly_degree(prefix_coefficients, field)
    shifted_degree = fpoly_degree(shifted_coefficients, field)
    common_degree = fpoly_degree(
        fpoly_gcd(prefix_coefficients, shifted_coefficients, field),
        field,
    )
    record = {
        "A": agreement,
        "m": size,
        "rank": rank,
        "rank_capacity": size // 2,
        "within_endpoint_capacity": rank <= size // 2,
        "coefficient_method": prefix_method,
        "prefix_degree": prefix_degree,
        "shifted_degree": shifted_degree,
        "common_gcd_degree": common_degree,
        "prefix_hash": hash_json(
            [field.encode(coefficient) for coefficient in prefix_coefficients]
        ),
        "shifted_hash": hash_json(
            [field.encode(coefficient) for coefficient in shifted_coefficients]
        ),
    }
    return record, common_degree, prefix_degree != rank or shifted_degree != rank


def all_contiguous_record(
    field: PolynomialBasisField,
    agreement: int,
    size: int,
    rank: int,
    shift_count: int,
    shifted_kernel_and_scale,
) -> tuple[dict[str, Any], int, bool]:
    common_coefficients: list[tuple[int, ...]] | None = None
    coefficient_method: str | None = None
    checked_degrees: list[int] = []
    first_shift_hash: str | None = None
    last_checked_shift_hash: str | None = None
    common_degree = -1

    for shift in range(shift_count):
        kernel, scale = shifted_kernel_and_scale(shift)
        coefficients, method = determinant_coefficients_from_kernel(
            field,
            kernel,
            rank,
            scale,
        )
        if coefficient_method is None:
            coefficient_method = method
        require(coefficient_method == method, "coefficient method mismatch")
        degree = fpoly_degree(coefficients, field)
        checked_degrees.append(degree)
        coefficient_hash = hash_json(
            [field.encode(coefficient) for coefficient in coefficients]
        )
        if first_shift_hash is None:
            first_shift_hash = coefficient_hash
        last_checked_shift_hash = coefficient_hash
        if common_coefficients is None:
            common_coefficients = coefficients
        else:
            common_coefficients = fpoly_gcd(
                common_coefficients,
                coefficients,
                field,
            )
        common_degree = fpoly_degree(common_coefficients, field)
        if common_degree == 0:
            break

    require(coefficient_method is not None, "no shifts checked")
    degree_histogram = Counter(checked_degrees)
    record = {
        "A": agreement,
        "m": size,
        "rank": rank,
        "rank_capacity": size // 2,
        "within_endpoint_capacity": rank <= size // 2,
        "shift_mode": "all-contiguous",
        "available_shift_count": shift_count,
        "checked_shift_count": len(checked_degrees),
        "gcd_stopped_early": len(checked_degrees) < shift_count,
        "coefficient_method": coefficient_method,
        "checked_shift_degree_histogram": {
            str(key): value for key, value in sorted(degree_histogram.items())
        },
        "common_gcd_degree": common_degree,
        "first_shift_hash": first_shift_hash,
        "last_checked_shift_hash": last_checked_shift_hash,
    }
    return record, common_degree, any(degree != rank for degree in checked_degrees)


def determinant_coefficients_from_kernel(
    field: PolynomialBasisField,
    kernel: list[list[tuple[int, ...]]],
    rank: int,
    scale: tuple[int, ...],
) -> tuple[list[tuple[int, ...]], str]:
    """Return scaled coefficients of det(I+ZK) and the method used.

    Newton identities are fast but divide by 1,2,...,rank.  Over the
    characteristic-17 row field they are only valid for rank < 17.  The
    interpolation path is slower but works uniformly through the endpoint
    capacity range.
    """

    if rank < field.p:
        return (
            packet.determinant_coefficients_from_kernel(
                field,
                kernel,
                rank,
                scale,
            ),
            "newton",
        )

    subkernel = [row[:rank] for row in kernel[:rank]]
    coefficients = characteristic_coefficients_by_interpolation(field, subkernel)
    return (
        [field.mul(scale, coefficient) for coefficient in coefficients],
        "interpolation",
    )


def characteristic_coefficients_by_interpolation(
    field: PolynomialBasisField,
    kernel: list[list[tuple[int, ...]]],
) -> list[tuple[int, ...]]:
    """Compute det(I+ZK) by interpolation over the extension field."""

    rank = len(kernel)
    require(field.size > rank, "field too small for interpolation nodes")
    points = []
    for index in range(rank + 1):
        slope = field.decode(index)
        matrix = []
        for row_index in range(rank):
            row = []
            for col_index in range(rank):
                entry = field.mul(slope, kernel[row_index][col_index])
                if row_index == col_index:
                    entry = field.add(field.one, entry)
                row.append(entry)
            matrix.append(row)
        points.append((slope, determinant_field(matrix, field)))

    coefficients = interpolate_field(points, field)
    for slope, value in points:
        if fpoly_eval(coefficients, slope, field) != value:
            raise AssertionError("kernel determinant interpolation check failed")
    return coefficients


def summary(
    row_descriptor: dict[str, Any],
    parameters: dict[str, Any],
    records: list[dict[str, Any]],
    gcd_histogram: Counter[int],
    degree_failures: int,
) -> dict[str, Any]:
    shift_mode = parameters.get("shift_mode", "adjacent")
    schema_version = "f17-32-m3-low-rank-spectral-target-search-v3"
    target_formula = "gcd(Phi_{m,r,0}(Z), Phi_{m,r,1}(Z)) = 1"
    recorded_probe = "top-window frontier beyond low-rank2..12"
    if shift_mode == "all-contiguous":
        schema_version = "f17-32-m3-low-rank-spectral-target-search-v4"
        target_formula = "gcd(Phi_{m,r,h}(Z): 0 <= h < 258-2m) = 1"
        recorded_probe = "contiguous all-shift target probe"
    collisions = [
        record
        for record in records
        if record["common_gcd_degree"] > 0
    ]
    return {
        "schema_version": schema_version,
        "status": "EXPERIMENTAL / AUDIT",
        "claim": "counterexample-first exact probe for the PR #170 synthetic low-rank spectral target",
        "row": {
            "n": packet.N,
            "k": packet.K,
            "field": row_descriptor["row"]["field"],
            "domain_hash": row_descriptor["row"]["domain_hash"],
            "domain_description": (
                "order-512 subgroup from the accepted F_17^32 row descriptor"
            ),
        },
        "target": {
            "formula": target_formula,
            "window": "normalized consecutive subgroup window",
            "m_range": [87, 128],
            "rank_range": "2 <= r <= ceil((m-1)/2)",
            "recorded_probe": recorded_probe,
        },
        "parameters": parameters,
        "source_artifacts": [
            packet.source_record(
                "row_descriptor",
                packet.ROW_DESCRIPTOR_REF,
                row_descriptor,
            ),
            packet.source_record(
                "low_rank2_12_affine_verifier",
                "experimental/scripts/verify_f17_32_m3_low_rank2_12_v10_affine_gcd.py",
            ),
            packet.source_record("search_script", SEARCH_SCRIPT_REF),
        ],
        "record_count": len(records),
        "degree_failure_count": degree_failures,
        "coefficient_method_histogram": dict(
            sorted(Counter(record["coefficient_method"] for record in records).items())
        ),
        "common_gcd_degree_histogram": {
            str(key): value for key, value in sorted(gcd_histogram.items())
        },
        "collision_count": len(collisions),
        "first_collision": collisions[0] if collisions else None,
        "records": records,
    }


def print_summary(result: dict[str, Any]) -> None:
    print("F_17^32 M3 low-rank spectral target search")
    print(f"status: {result['status']}")
    print(f"records: {result['record_count']}")
    print(f"degree failures: {result['degree_failure_count']}")
    print(f"coefficient methods: {result['coefficient_method_histogram']}")
    print(f"common gcd degree histogram: {result['common_gcd_degree_histogram']}")
    if result["first_collision"] is None:
        print("first collision: none")
    else:
        print(f"first collision: {result['first_collision']}")


def main() -> None:
    args = parse_args()
    validate_range(
        args.agreement_min,
        args.agreement_max,
        args.rank_min,
        args.rank_max,
    )
    result = probe_records(
        args.agreement_min,
        args.agreement_max,
        args.rank_min,
        args.rank_max,
        args.stop_on_collision,
        args.shift_mode,
    )
    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(render(result), encoding="utf-8")
    if args.check:
        actual = args.check.read_text(encoding="utf-8")
        expected = render(result)
        if actual != expected:
            raise AssertionError(f"spectral target search mismatch: {args.check}")
    if args.json:
        print(render(result), end="")
        return
    print_summary(result)


if __name__ == "__main__":
    main()
