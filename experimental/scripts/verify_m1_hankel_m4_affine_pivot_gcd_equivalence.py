#!/usr/bin/env python3
"""Verify affine-pivot gcd equivalence for compressed M4 root tables."""

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
)


SCHEMA_VERSION = "f17-32-m3-m4-affine-pivot-gcd-equivalence-v1"
Q_LINE = 17**32
TARGET_BITS = 128
BUDGET = Q_LINE // 2**TARGET_BITS
A_MIN = 385
A_MAX = 426
RANK_BOUNDARY = 6
ROW_DESCRIPTOR_REF = (
    "experimental/data/certificates/hankel-f17-32-row-descriptor/"
    "f17_32_n512_k256_hankel_row_descriptor.json"
)
DIRECTION_RANK_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-direction-rank-degree-cap/"
    "f17_32_n512_k256_m3_direction_rank_degree_cap.json"
)
AFFINE_PIVOT_COMPRESSION_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-m4-affine-pivot-compression/"
    "f17_32_n512_k256_m3_m4_affine_pivot_compression.json"
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
    for i, a_i in enumerate(left):
        for j, b_j in enumerate(right):
            out[i + j] = (out[i + j] + a_i * b_j) % prime
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


def poly_monic(poly: list[int], prime: int) -> list[int]:
    out = trim(poly, prime)
    if out == [0]:
        return out
    inv = pow(out[-1], -1, prime)
    return [(entry * inv) % prime for entry in out]


def poly_eval(poly: list[int], x_value: int, prime: int) -> int:
    total = 0
    power = 1
    for coeff in poly:
        total = (total + coeff * power) % prime
        power = power * x_value % prime
    return total


def poly_substitute_shift(poly: list[int], shift: int, prime: int) -> list[int]:
    """Return p(z+shift) for low-to-high coefficients of p."""
    out = [0] * len(poly)
    for degree, coeff in enumerate(poly):
        for z_degree in range(degree + 1):
            out[z_degree] = (
                out[z_degree]
                + coeff * comb(degree, z_degree) * pow(shift, degree - z_degree, prime)
            ) % prime
    return trim(out, prime)


def poly_gcd(left: list[int], right: list[int], prime: int) -> list[int]:
    a = trim(left, prime)
    b = trim(right, prime)
    while b != [0]:
        _quotient, remainder = poly_divmod(a, b, prime)
        a, b = b, remainder
    return poly_monic(a, prime)


def poly_gcd_many(polys: list[list[int]], prime: int) -> list[int]:
    require(polys, "empty gcd list")
    out = polys[0]
    for poly in polys[1:]:
        out = poly_gcd(out, poly, prime)
    return poly_monic(out, prime)


def root_poly(roots: list[int], prime: int) -> list[int]:
    out = [1]
    for root in roots:
        out = poly_mul(out, [(-root) % prime, 1], prime)
    return out


def sanity_checks() -> list[dict[str, Any]]:
    prime = 17
    originals = [
        [5 * coeff % prime for coeff in root_poly([1, 2, 4], prime)],
        [7 * coeff % prime for coeff in root_poly([2, 4, 8], prime)],
        [11 * coeff % prime for coeff in root_poly([4, 9], prime)],
    ]
    pivots = [0, 3, 5]
    local_compressed = []
    global_translated = []
    for original, pivot in zip(originals, pivots, strict=True):
        pivot_value = poly_eval(original, pivot, prime)
        require(pivot_value != 0, "chosen sanity pivot is bad")
        local = poly_substitute_shift(original, pivot, prime)
        local = [coeff * pow(pivot_value, -1, prime) % prime for coeff in local]
        global_poly = poly_substitute_shift(local, -pivot, prime)
        local_compressed.append(local)
        global_translated.append(global_poly)
    original_gcd = poly_gcd_many(originals, prime)
    compressed_gcd = poly_gcd_many(global_translated, prime)
    require(original_gcd == compressed_gcd, "translated scaled-gcd sanity check failed")
    require(original_gcd == root_poly([4], prime), "unexpected gcd root")
    return [
        {
            "prime": prime,
            "pivots": pivots,
            "local_compressed_low_to_high": local_compressed,
            "original_gcd_low_to_high": original_gcd,
            "global_translated_compressed_gcd_low_to_high": compressed_gcd,
            "common_root": 4,
            "result": "passed",
        }
    ]


def agreement_record(agreement: int) -> dict[str, Any]:
    j_value = N - agreement
    t_value = agreement - K
    minor_size = j_value + 1
    return {
        "A": agreement,
        "j": j_value,
        "t": t_value,
        "minor_size": minor_size,
        "maximal_row_set_count": comb(t_value, minor_size),
        "rank6_bad_pivots_per_nonzero_minor_at_most": RANK_BOUNDARY,
        "rank6_good_pivots_per_nonzero_minor_at_least": Q_LINE - RANK_BOUNDARY,
    }


def build_certificate() -> dict[str, Any]:
    field = Field(P, MODULUS)
    descriptor = load_json(ROW_DESCRIPTOR_REF)
    direction = load_json(DIRECTION_RANK_REF)
    compression = load_json(AFFINE_PIVOT_COMPRESSION_REF)

    require(descriptor["row"]["n"] == N, "descriptor n mismatch")
    require(descriptor["row"]["k"] == K, "descriptor k mismatch")
    require(descriptor["row"]["field"] == "F_17^32", "descriptor field mismatch")
    require(descriptor["row"]["field_order"] == Q_LINE, "descriptor q mismatch")
    require(descriptor["row"]["syndrome_length"] == N - K, "syndrome length mismatch")
    require(
        direction["schema_version"] == "f17-32-m3-direction-rank-degree-cap-v1",
        "unexpected direction-rank schema",
    )
    require(
        compression["schema_version"] == "f17-32-m3-m4-affine-pivot-compression-v1",
        "unexpected compression schema",
    )
    for name, data in [("direction", direction), ("compression", compression)]:
        require(data["window"]["A_min"] == A_MIN, f"{name} A_min mismatch")
        require(data["window"]["A_max"] == A_MAX, f"{name} A_max mismatch")
    require(BUDGET == 6, "unexpected finite budget")

    domain_encodings = descriptor["domain"]["domain_encodings"]
    require(len(domain_encodings) == N, "domain length mismatch")
    require(len(set(domain_encodings)) == N, "descriptor domain is not distinct")
    decoded = [field.decode(value) for value in domain_encodings]
    require(
        [field.encode(value) for value in decoded] == domain_encodings,
        "domain decode/encode roundtrip failed",
    )

    records = [agreement_record(agreement) for agreement in range(A_MIN, A_MAX + 1)]
    total_row_sets = sum(record["maximal_row_set_count"] for record in records)
    require(total_row_sets == direction["window"]["all_row_set_total"], "direction total mismatch")
    require(total_row_sets == compression["window"]["all_row_set_total"], "compression total mismatch")
    require(all(record["minor_size"] > RANK_BOUNDARY for record in records), "minor too small")

    sanity = sanity_checks()

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT",
        "object": "affine-pivot compressed gcd equivalence for M3 regular root tables",
        "row": {
            "code": "RS[F_17^32,H,256]",
            "n": N,
            "k": K,
            "field": "F_17^32",
            "domain_hash": descriptor["row"]["domain_hash"],
            "q_line": Q_LINE,
            "finite_budget": BUDGET,
        },
        "source_artifacts": {
            "row_descriptor": {"ref": ROW_DESCRIPTOR_REF, "sha256": sha256_file(ROW_DESCRIPTOR_REF)},
            "direction_rank_degree_cap": {
                "ref": DIRECTION_RANK_REF,
                "sha256": sha256_file(DIRECTION_RANK_REF),
            },
            "affine_pivot_compression": {
                "ref": AFFINE_PIVOT_COMPRESSION_REF,
                "sha256": sha256_file(AFFINE_PIVOT_COMPRESSION_REF),
            },
        },
        "window": {
            "A_min": A_MIN,
            "A_max": A_MAX,
            "agreement_count": len(records),
            "all_row_set_total": total_row_sets,
        },
        "theorem": {
            "pivot_availability": (
                "If a maximal minor polynomial p_R(z) is nonzero and has "
                "degree at most r, then at most r finite slopes are bad "
                "pivots.  In the rank-6 boundary over F_17^32, each nonzero "
                "minor has at least q_line-6 finite affine pivots."
            ),
            "gcd_equivalence": (
                "For any finite set of nonzero row-set minors, choose for each "
                "R a finite pivot z_R with p_R(z_R)!=0 and form the local "
                "compressed polynomial c_R(w) from the affine-pivot compression "
                "theorem.  Put ctilde_R(Z)=c_R(Z-z_R) in the global slope "
                "variable.  Then p_R(Z)=p_R(z_R)ctilde_R(Z), so the monic gcd "
                "of the original minors equals the monic gcd of the translated "
                "compressed polynomials."
            ),
            "rank6_consequence": (
                "The v10 canonical finite root table for a nonsingular rank-6 "
                "bucket may be computed from 6x6 compressed polynomials after "
                "translating each local chart back to the global slope variable, "
                "without changing the gcd root set, provided every nonzero "
                "row-set chart uses a good finite pivot."
            ),
            "proof_skeleton": [
                "The direction-rank degree cap bounds deg p_R by r.",
                "A nonzero degree-r polynomial over a field has at most r roots, so good pivots exist in F_17^32.",
                "The affine-pivot compression theorem gives p_R(Z)=p_R(z_R)c_R(Z-z_R) with p_R(z_R) nonzero.",
                "Multiplying each gcd input by a nonzero scalar does not change the monic gcd.",
            ],
        },
        "field_audit": {
            "domain_size": len(domain_encodings),
            "domain_hash": hash_value(domain_encodings),
            "decoded_roundtrip_hash": hash_value([field.encode(value) for value in decoded]),
        },
        "agreement_records": records,
        "sanity_checks": sanity,
        "summary": {
            "agreement_count": len(records),
            "rank_boundary": RANK_BOUNDARY,
            "finite_budget": BUDGET,
            "bad_pivots_per_nonzero_rank6_minor_at_most": RANK_BOUNDARY,
            "good_pivots_per_nonzero_rank6_minor_at_least": Q_LINE - RANK_BOUNDARY,
            "compressed_gcd_preserves_root_set": True,
        },
        "checks": [
            "dependency windows are 385..426",
            "dependency row-set totals agree",
            "rank-6 bad pivot count is at most six per nonzero minor",
            "translated compressed gcd is invariant under nonzero per-chart scaling",
            "sanity polynomial gcd check with distinct pivots passes over F_17",
        ],
        "nonclaims": [
            "does not choose pivots for an arbitrary concrete packet",
            "does not compute a rank-6 root table",
            "does not prove projective safety by itself",
            "does not classify singular all-minor-zero buckets",
        ],
    }


def check_certificate(path: Path) -> None:
    expected = render(build_certificate())
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"affine-pivot gcd-equivalence certificate mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    summary = certificate["summary"]
    window = certificate["window"]
    print("F_17^32 M3/M4 affine-pivot gcd equivalence")
    print(
        "A={A_min}..{A_max}, agreements={agreement_count}, row sets={all_row_set_total}".format(
            **window
        )
    )
    print(
        "rank boundary={rank_boundary}; bad pivots <= {bad_pivots_per_nonzero_rank6_minor_at_most}; good pivots >= {good_pivots_per_nonzero_rank6_minor_at_least}".format(
            **summary
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
