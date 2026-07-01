#!/usr/bin/env python3
"""Verify the M3 projective-infinity split-locator gate."""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from math import comb
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
    SUBGROUP_ORDER,
)


SCHEMA_VERSION = "f17-32-m3-projective-split-locator-gate-v1"
Q_LINE = 17**32
A_MIN = 385
A_MAX = 426
ROW_DESCRIPTOR_REF = (
    "experimental/data/certificates/hankel-f17-32-row-descriptor/"
    "f17_32_n512_k256_hankel_row_descriptor.json"
)
PROJECTIVE_INFINITY_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-projective-infinity-rank/"
    "f17_32_n512_k256_m3_projective_infinity_rank_criterion.json"
)
PROJECTIVE_KERNEL_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-m5-projective-infinity-kernel-chart/"
    "f17_32_n512_k256_m3_m5_projective_infinity_kernel_chart.json"
)
NULLPOLY_SPLIT_LOCATOR_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-nullpolynomial-split-locator-gate/"
    "f17_32_n512_k256_m3_nullpolynomial_split_locator_gate.json"
)


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


def trim(poly: list[int], prime: int) -> list[int]:
    out = [entry % prime for entry in poly]
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def poly_mul(left: list[int], right: list[int], prime: int) -> list[int]:
    out = [0] * (len(left) + len(right) - 1)
    for i, left_i in enumerate(left):
        for j, right_j in enumerate(right):
            out[i + j] = (out[i + j] + left_i * right_j) % prime
    return trim(out, prime)


def poly_divmod(numerator: list[int], denominator: list[int], prime: int) -> tuple[list[int], list[int]]:
    work = trim(numerator, prime)
    divisor = trim(denominator, prime)
    require(divisor != [0], "division by zero polynomial")
    quotient = [0] * max(1, len(work) - len(divisor) + 1)
    while len(work) >= len(divisor) and work != [0]:
        coeff = work[-1] * pow(divisor[-1], -1, prime) % prime
        shift = len(work) - len(divisor)
        quotient[shift] = coeff
        for index, term in enumerate(divisor):
            work[shift + index] = (work[shift + index] - coeff * term) % prime
        work = trim(work, prime)
    return trim(quotient, prime), work


def mat_vec(matrix: list[list[int]], vector: list[int], prime: int) -> list[int]:
    return [
        sum(row[col] * vector[col] for col in range(len(vector))) % prime
        for row in matrix
    ]


def rank_mod(matrix: list[list[int]], prime: int) -> int:
    work = [[entry % prime for entry in row] for row in matrix]
    rank = 0
    rows = len(work)
    cols = len(work[0]) if rows else 0
    for col in range(cols):
        pivot = None
        for row in range(rank, rows):
            if work[row][col] % prime:
                pivot = row
                break
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        inv = pow(work[rank][col], -1, prime)
        work[rank] = [entry * inv % prime for entry in work[rank]]
        for row in range(rows):
            if row == rank or work[row][col] == 0:
                continue
            factor = work[row][col]
            work[row] = [
                (work[row][entry_col] - factor * work[rank][entry_col]) % prime
                for entry_col in range(cols)
            ]
        rank += 1
    return rank


def locator_poly(roots: list[int], prime: int) -> list[int]:
    out = [1]
    for root in roots:
        out = poly_mul(out, [(-root) % prime, 1], prime)
    return out


def sanity_checks() -> list[dict[str, Any]]:
    prime = 17
    domain_poly = [(-1) % prime] + [0] * 15 + [1]

    split_locator = locator_poly([1, 2], prime)
    v_direction = [1, 0, 15, 11, 3]
    u_base = [1, 0, 0, 0, 0]
    v_matrix = [v_direction[row : row + 3] for row in range(3)]
    u_matrix = [u_base[row : row + 3] for row in range(3)]
    _quotient, split_remainder = poly_divmod(domain_poly, split_locator, prime)
    require(split_remainder == [0], "split endpoint locator does not divide domain")
    require(mat_vec(v_matrix, split_locator, prime) == [0, 0, 0], "projective endpoint recurrence failed")
    require(mat_vec(u_matrix, split_locator, prime) == [2, 0, 0], "projective endpoint noncontainment failed")

    ambient_only_locator = [0, 0, 1]
    ambient_v_matrix = [[1, 0, 0], [0, 1, 0], [0, 0, 0]]
    ambient_u_matrix = [[0, 0, 1], [0, 0, 0], [0, 0, 0]]
    _quotient, ambient_remainder = poly_divmod(domain_poly, ambient_only_locator, prime)
    require(ambient_remainder != [0], "ambient-only endpoint locator unexpectedly divides domain")
    require(mat_vec(ambient_v_matrix, ambient_only_locator, prime) == [0, 0, 0], "ambient endpoint kernel failed")
    require(mat_vec(ambient_u_matrix, ambient_only_locator, prime) == [1, 0, 0], "ambient endpoint noncontainment failed")
    require(rank_mod(ambient_v_matrix, prime) == 2, "ambient endpoint rank mismatch")

    return [
        {
            "prime": prime,
            "domain": "F_17^* roots of X^16-1",
            "split_locator_low_to_high": split_locator,
            "split_locator_divides_domain_polynomial": True,
            "projective_direction_values": mat_vec(v_matrix, split_locator, prime),
            "base_noncontainment_values": mat_vec(u_matrix, split_locator, prime),
            "result": "projective endpoint can be an actual split-locator witness",
        },
        {
            "prime": prime,
            "ambient_kernel_vector_low_to_high": ambient_only_locator,
            "ambient_kernel_divides_domain_polynomial": False,
            "projective_direction_values": mat_vec(ambient_v_matrix, ambient_only_locator, prime),
            "base_noncontainment_values": mat_vec(ambient_u_matrix, ambient_only_locator, prime),
            "result": "ambient projective endpoint can overcount split-domain locators",
        },
    ]


def agreement_record(agreement: int) -> dict[str, Any]:
    j_value = N - agreement
    t_value = agreement - K
    size = j_value + 1
    return {
        "A": agreement,
        "j": j_value,
        "t": t_value,
        "minor_size": size,
        "projective_kernel_dimension_if_rank_6": size - 6,
        "split_locator_degree_required": j_value,
        "maximal_row_set_count": comb(t_value, size),
    }


def check_dependency_windows(data_by_name: dict[str, dict[str, Any]]) -> None:
    for name, data in data_by_name.items():
        require(data["row"]["n"] == N, f"{name} n mismatch")
        require(data["row"]["k"] == K, f"{name} k mismatch")
        require(data["window"]["A_min"] == A_MIN, f"{name} A_min mismatch")
        require(data["window"]["A_max"] == A_MAX, f"{name} A_max mismatch")


def build_certificate() -> dict[str, Any]:
    field = Field(P, MODULUS)
    descriptor = load_json(ROW_DESCRIPTOR_REF)
    projective = load_json(PROJECTIVE_INFINITY_REF)
    projective_kernel = load_json(PROJECTIVE_KERNEL_REF)
    nullpoly = load_json(NULLPOLY_SPLIT_LOCATOR_REF)

    require(descriptor["schema_version"] == "f17-32-hankel-row-descriptor-v1", "descriptor schema mismatch")
    require(projective["schema_version"] == "f17-32-m3-projective-infinity-rank-criterion-v1", "projective schema mismatch")
    require(projective_kernel["schema_version"] == "f17-32-m3-m5-projective-infinity-kernel-chart-v1", "kernel schema mismatch")
    require(nullpoly["schema_version"] == "f17-32-m3-nullpolynomial-split-locator-gate-v1", "nullpoly schema mismatch")

    require(descriptor["row"]["n"] == N, "descriptor n mismatch")
    require(descriptor["row"]["k"] == K, "descriptor k mismatch")
    require(descriptor["row"]["field"] == "F_17^32", "descriptor field mismatch")
    require(descriptor["row"]["field_order"] == Q_LINE, "descriptor q mismatch")
    check_dependency_windows(
        {
            "projective": projective,
            "projective_kernel": projective_kernel,
            "nullpoly": nullpoly,
        }
    )

    domain = descriptor["domain"]["domain_encodings"]
    require(len(domain) == SUBGROUP_ORDER == N, "domain size mismatch")
    require(len(set(domain)) == N, "domain is not distinct")
    require(field.encode(field.zero) not in domain, "zero belongs to domain")
    generator = field.decode(descriptor["domain"]["generator_encoding"])
    powers = []
    current = field.one
    for _ in range(N):
        powers.append(field.encode(current))
        current = field.mul(current, generator)
    require(powers == domain, "domain is not the recorded generator power list")
    require(current == field.one, "generator does not close after 512 powers")
    require(field.pow(generator, N // 2) != field.one, "generator order is not exact")
    require(N % P != 0, "domain polynomial derivative vanishes identically")

    records = [agreement_record(agreement) for agreement in range(A_MIN, A_MAX + 1)]
    total_row_sets = sum(record["maximal_row_set_count"] for record in records)
    require(total_row_sets == projective["window"]["all_row_set_total"], "projective total mismatch")
    require(total_row_sets == projective_kernel["window"]["all_row_set_total"], "kernel total mismatch")
    require(
        min(record["projective_kernel_dimension_if_rank_6"] for record in records) == 81,
        "unexpected rank-6 minimum kernel dimension",
    )
    require(
        max(record["projective_kernel_dimension_if_rank_6"] for record in records) == 122,
        "unexpected rank-6 maximum kernel dimension",
    )

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT",
        "object": "M3 projective-infinity split-locator gate",
        "row": {
            "code": "RS[F_17^32,H,256]",
            "n": N,
            "k": K,
            "field": "F_17^32",
            "q_line": Q_LINE,
            "domain_hash": descriptor["row"]["domain_hash"],
        },
        "source_artifacts": {
            "row_descriptor": {"ref": ROW_DESCRIPTOR_REF, "sha256": sha256_file(ROW_DESCRIPTOR_REF)},
            "projective_infinity_rank_criterion": {
                "ref": PROJECTIVE_INFINITY_REF,
                "sha256": sha256_file(PROJECTIVE_INFINITY_REF),
            },
            "projective_infinity_kernel_chart": {
                "ref": PROJECTIVE_KERNEL_REF,
                "sha256": sha256_file(PROJECTIVE_KERNEL_REF),
            },
            "nullpolynomial_split_locator_gate": {
                "ref": NULLPOLY_SPLIT_LOCATOR_REF,
                "sha256": sha256_file(NULLPOLY_SPLIT_LOCATOR_REF),
            },
        },
        "window": {
            "A_min": A_MIN,
            "A_max": A_MAX,
            "agreement_count": len(records),
            "all_row_set_total": total_row_sets,
            "rank6_projective_kernel_dimension_min": min(
                record["projective_kernel_dimension_if_rank_6"] for record in records
            ),
            "rank6_projective_kernel_dimension_max": max(
                record["projective_kernel_dimension_if_rank_6"] for record in records
            ),
        },
        "domain_locator_gate": {
            "domain_polynomial": "X^512 - 1",
            "derivative": "512 X^511 = 2 X^511 in characteristic 17",
            "squarefree": True,
            "split_locator_criterion": (
                "A monic degree-j polynomial is the locator of a j-subset of H "
                "iff it divides X^512-1."
            ),
        },
        "theorem": {
            "ambient_projective_chart": (
                "The ambient projective-infinity chart is H_{t,j}(v) ell=0 "
                "and H_{t,j}(u) ell != 0, modulo nonzero scaling of ell."
            ),
            "split_locator_gate": (
                "An ambient projective kernel vector gives an actual "
                "support-wise endpoint witness only after normalization to a "
                "monic degree-j divisor of X^512-1."
            ),
            "noncontainment_gate": (
                "The endpoint is support-wise noncontained exactly when "
                "H_{t,j}(u) ell != 0.  If H(u)ell=H(v)ell=0, both endpoints "
                "are explained on the same support and the witness is contained."
            ),
            "rank6_boundary_consequence": (
                "In the M3 window, a direction-rank-6 bucket has ambient "
                "projective kernel dimension j+1-6, ranging from 81 to 122.  "
                "This large ambient kernel must still be intersected with the "
                "finite split-locator divisor gate before the endpoint is an "
                "actual support-wise projective witness."
            ),
            "certificate_payload": [
                "kernel vector ell for H(v)",
                "normalization degree and leading coefficient of L(X)",
                "divisor proof or remainder for L(X) against X^512-1",
                "projective direction vector H(v)ell",
                "base noncontainment vector H(u)ell",
            ],
        },
        "agreement_records": records,
        "sanity_checks": sanity_checks(),
        "field_audit": {
            "domain_size": len(domain),
            "domain_hash": hash_value(domain),
            "generator_encoding": descriptor["domain"]["generator_encoding"],
            "generator_exact_order": N,
            "domain_polynomial_derivative_coefficient_mod_17": N % P,
            "x_512_minus_1_squarefree": True,
        },
        "summary": {
            "agreement_count": len(records),
            "projective_split_locator_gate_available": True,
            "ambient_projective_endpoint_is_safe_upper_bound": True,
            "rank6_projective_kernel_dimension_min": min(
                record["projective_kernel_dimension_if_rank_6"] for record in records
            ),
            "rank6_projective_kernel_dimension_max": max(
                record["projective_kernel_dimension_if_rank_6"] for record in records
            ),
        },
        "checks": [
            "dependency schemas and windows match the F_17^32 M3 regular window",
            "the recorded domain is the exact order-512 subgroup generated in the row descriptor",
            "X^512-1 is squarefree in characteristic 17",
            "monic degree-j divisors of X^512-1 are exactly split squarefree j-subgroup locators",
            "projective ambient kernel and split-domain endpoint witnesses are separated",
            "sanity examples distinguish ambient projective endpoints from split-locator endpoints",
        ],
        "nonclaims": [
            "does not compute whether an arbitrary rank-6 endpoint has a split locator",
            "does not prove endpoint payment or emptiness for rank-6 buckets",
            "does not compute finite affine root tables",
            "does not close singular buckets without pivot eliminants or paid ledgers",
        ],
    }


def check_certificate(path: Path) -> None:
    expected = render(build_certificate())
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"projective split-locator certificate mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    window = certificate["window"]
    print("F_17^32 M3 projective split-locator gate")
    print(
        "A={A_min}..{A_max}, agreements={agreement_count}, rank6 endpoint kernel dim={rank6_projective_kernel_dimension_min}..{rank6_projective_kernel_dimension_max}".format(
            **window
        )
    )


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
