#!/usr/bin/env python3
"""Verify the deployed F_17^32 moving-zero sparse witness.

The certificate instantiates the moving-zero lower bound from
experimental/notes/thresholds/cap25_v12_sparse_sigma_first_layer_audit.md at
the deployed-shaped row C = RS[F_17^32, H, 256], |H| = 512.

It proves by construction that one r=129 sparse pair has at least 258 finite
MCA-bad slopes.  The displayed finite witness has status PROVED, while its use
as prob:mutual evidence is EXPERIMENTAL; it is not an upper bound on sigma_C
and not a deployed soundness claim.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import sys
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from experimental.scripts.verify_m1_cycle120_self_contained_certificate import (
    FQ,
    QONE,
    QZERO,
    THETA,
    p_degree,
    p_eval,
    qadd,
    qeq,
    qis_zero,
    qmul,
    qpow,
    qsub,
)


SCHEMA_VERSION = "deployed-sparse-witness-f17-32-v1"
N = 512
K = 256
M = N - K
R = M // 2 + 1
Z_SIZE = K - 2
EXPECTED_MOVING = M - R + 2
EXPECTED_TOTAL = R + EXPECTED_MOVING
CERT_PATH = REPO_ROOT / (
    "experimental/data/certificates/deployed-sparse-witness-f17-32/"
    "deployed_sparse_witness_f17_32_r129.json"
)
CAP25_NOTE = (
    "experimental/notes/thresholds/"
    "cap25_v12_sparse_sigma_first_layer_audit.md"
)
SOURCE_SCRIPT = "experimental/scripts/verify_m1_cycle120_self_contained_certificate.py"


def render(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def object_sha256(value: Any) -> str:
    return sha256(render(value).encode("utf-8")).hexdigest()


def text_sha256_lf(path: Path) -> str:
    return sha256(path.read_text(encoding="utf-8").replace("\r\n", "\n").encode()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def qneg(x):
    return qsub(QZERO, x)


def f16_vector(a: list[int]) -> list[int]:
    out = [0] * 16
    for index, value in enumerate(a[:16]):
        out[index] = value % 17
    return out


def q_vector(x) -> list[int]:
    return f16_vector(x[0]) + f16_vector(x[1])


def build_domain():
    domain = []
    x = QONE
    for _ in range(N):
        domain.append(x)
        x = qmul(x, THETA)
    require(qeq(x, QONE), "theta^512 returns to one")
    require(not qeq(qpow(THETA, N // 2), QONE), "theta has order 512, not 256")
    require(len({tuple(q_vector(point)) for point in domain}) == N, "domain points distinct")
    return domain


def poly_mul_linear(poly, root):
    """Return poly(X) * (X - root), coefficients in ascending degree."""
    out = [QZERO for _ in range(len(poly) + 1)]
    neg_root = qneg(root)
    for i, coeff in enumerate(poly):
        out[i] = qadd(out[i], qmul(coeff, neg_root))
        out[i + 1] = qadd(out[i + 1], coeff)
    return out


def build_pi(domain, z_indices: list[int]):
    poly = [QONE]
    for index in z_indices:
        poly = poly_mul_linear(poly, domain[index])
    require(p_degree(poly, FQ) == len(z_indices), "Pi degree")
    return poly


def moving_codeword_hash(pi_poly, gamma) -> str:
    return object_sha256([q_vector(coeff) for coeff in poly_mul_linear(pi_poly, gamma)])


def zero_codeword_hash() -> str:
    return object_sha256([[0] * 32])


def support_for_tangent(e_indices: list[int], j0: int) -> list[int]:
    return [i for i in range(N) if i not in set(e_indices)] + [j0]


def support_for_moving(z_indices: list[int], e_indices: list[int], x_index: int) -> list[int]:
    return z_indices + e_indices + [x_index]


def build_certificate() -> dict[str, Any]:
    domain = build_domain()
    z_indices = list(range(Z_SIZE))
    e_indices = list(range(Z_SIZE, Z_SIZE + R))
    moving_indices = list(range(Z_SIZE + R, N))
    require(len(z_indices) == Z_SIZE, "Z_* size")
    require(len(e_indices) == R, "E' size")
    require(len(moving_indices) == EXPECTED_MOVING, "moving slope count")
    require(set(z_indices).isdisjoint(e_indices), "Z and E disjoint")
    require(set(z_indices).isdisjoint(moving_indices), "Z and moving slopes disjoint")
    require(set(e_indices).isdisjoint(moving_indices), "E and moving slopes disjoint")

    pi_poly = build_pi(domain, z_indices)
    pi_values = {index: p_eval(pi_poly, domain[index], FQ) for index in e_indices}
    require(all(not qis_zero(value) for value in pi_values.values()), "Pi nonzero on E'")

    epsilon_values = []
    for index in e_indices:
        pi_value = pi_values[index]
        epsilon_values.append(
            {
                "domain_index": index,
                "epsilon_1": q_vector(qmul(domain[index], pi_value)),
                "epsilon_2": q_vector(qneg(pi_value)),
            }
        )

    records = []
    zero_hash = zero_codeword_hash()
    for index in e_indices:
        support = support_for_tangent(e_indices, index)
        records.append(
            {
                "kind": "tangent",
                "gamma_domain_index": index,
                "support_indices": support,
                "support_size": len(support),
                "close_codeword": {
                    "kind": "zero",
                    "coefficients_sha256": zero_hash,
                    "degree_bound": 0,
                },
                "one_sided_failure": {
                    "reason": "epsilon_2 is zero on D\\E' but nonzero at gamma in E'",
                    "vanishing_points": N - R,
                    "nonzero_point": index,
                },
            }
        )

    first_e = e_indices[0]
    second_e = e_indices[1]
    for index in moving_indices:
        gamma = domain[index]
        support = support_for_moving(z_indices, e_indices, index)
        codeword = poly_mul_linear(pi_poly, gamma)
        require(p_degree(codeword, FQ) == K - 1, "moving codeword degree")
        for e_index in e_indices:
            line_value = qadd(
                qmul(domain[e_index], pi_values[e_index]),
                qmul(gamma, qneg(pi_values[e_index])),
            )
            require(
                qeq(line_value, qmul(qsub(domain[e_index], gamma), pi_values[e_index])),
                "moving line agrees on E'",
            )
        c_from_first = qmul(qneg(QONE), qpow(qsub(domain[first_e], gamma), 17**32 - 2))
        require(
            not qeq(
                qmul(c_from_first, qsub(domain[second_e], gamma)),
                qneg(QONE),
            ),
            "moving one-sided failure from two E' points",
        )
        records.append(
            {
                "kind": "moving_zero",
                "gamma_domain_index": index,
                "support_indices": support,
                "support_size": len(support),
                "close_codeword": {
                    "kind": "linear_factor_times_pi",
                    "linear_factor_root_domain_index": index,
                    "coefficients_sha256": moving_codeword_hash(pi_poly, gamma),
                    "degree_bound": K - 1,
                },
                "one_sided_failure": {
                    "reason": "degree<k extension would be c*(X-gamma)Pi, but two E' points force incompatible constants",
                    "zero_indices_for_epsilon_2": z_indices + [index],
                    "incompatibility_e_indices": [first_e, second_e],
                },
            }
        )

    require(len(records) == EXPECTED_TOTAL, "record count")
    require(len({record["gamma_domain_index"] for record in records}) == EXPECTED_TOTAL, "distinct slopes")
    require(all(record["support_size"] >= N - R for record in records), "support size threshold")

    certificate: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / EXPERIMENTAL",
        "theorem_problem_id": "prob:mutual / sparse moving-zero lower bound",
        "claim": (
            "For RS[F_17^32,H,256] with |H|=512 and r=129, the displayed "
            "sparse pair has at least 258 distinct finite MCA-bad slopes."
        ),
        "endpoint_conventions": {
            "n": N,
            "k": K,
            "m": M,
            "r": R,
            "delta_convention": "r = floor(delta*n)",
            "finite_slopes_only": True,
            "threshold": "2r >= m+1",
            "support_union_bound": "|supp epsilon_1 union supp epsilon_2| <= r",
        },
        "field": {
            "name": "F_17^32",
            "tower": "F_17[X]/(X^16+X^8+3), then theta^2 = 6X^9",
            "domain": "H=<theta>, theta order 512",
            "element_encoding": "32 little-endian F_17 coefficients: first F16 part, then theta F16 part",
        },
        "construction": {
            "z_star_indices": z_indices,
            "e_prime_indices": e_indices,
            "moving_zero_indices": moving_indices,
            "pi_coefficients": [q_vector(coeff) for coeff in pi_poly],
            "pi_coefficients_sha256": object_sha256([q_vector(coeff) for coeff in pi_poly]),
            "epsilon_support_values": epsilon_values,
        },
        "records": records,
        "aggregate": {
            "tangent_slopes": R,
            "moving_zero_slopes": EXPECTED_MOVING,
            "total_bad_slopes_certified": EXPECTED_TOTAL,
            "expected_n_minus_k_plus_2": N - K + 2,
            "sigma_lower_bound": EXPECTED_TOTAL,
            "support_size": K - 1 + R,
            "minimum_required_support_size": N - R,
        },
        "source_artifacts": [
            {
                "name": "moving_zero_audit_note",
                "ref": CAP25_NOTE,
                "sha256_lf": text_sha256_lf(REPO_ROOT / CAP25_NOTE),
            },
            {
                "name": "tower_arithmetic_script",
                "ref": SOURCE_SCRIPT,
                "sha256_lf": text_sha256_lf(REPO_ROOT / SOURCE_SCRIPT),
            },
        ],
        "non_claims": [
            "not an upper bound on sigma_C",
            "not a leaderboard row",
            "not a deployed soundness claim",
            "does not supersede the CAP25 sparse first-layer audit",
        ],
    }
    certificate["payload_sha256"] = object_sha256(
        {key: value for key, value in certificate.items() if key != "payload_sha256"}
    )
    return certificate


def verify_certificate(certificate: dict[str, Any], sample: int | None) -> dict[str, Any]:
    require(certificate["schema_version"] == SCHEMA_VERSION, "schema version")
    require(certificate["status"] == "PROVED / EXPERIMENTAL", "status")
    expected = build_certificate()
    expected_payload = expected["payload_sha256"]
    require(certificate["payload_sha256"] == expected_payload, "payload sha256")

    if sample is None:
        checked = len(certificate["records"])
    else:
        checked = min(sample, len(certificate["records"]))
    require(checked > 0, "nonzero sample")

    for index, record in enumerate(certificate["records"][:checked]):
        expected_record = expected["records"][index]
        require(record == expected_record, f"record {index} matches deterministic witness")

    return {
        "checked_records": checked,
        "total_records": len(certificate["records"]),
        "payload_sha256": expected_payload,
        "status": "PROVED / EXPERIMENTAL",
    }


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", type=Path, help="write deterministic certificate JSON")
    parser.add_argument("--check", type=Path, help="check deterministic certificate JSON")
    parser.add_argument("--sample", type=int, default=16, help="number of records to replay unless --full is set")
    parser.add_argument("--full", action="store_true", help="replay every certified slope")
    parser.add_argument("--json", action="store_true", help="print JSON summary")
    args = parser.parse_args()

    certificate = build_certificate()
    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(render(certificate), encoding="utf-8")

    summary = {
        "status": "PROVED / EXPERIMENTAL",
        "row": "F_17^32 n=512 k=256 r=129",
        "certified_bad_slopes": EXPECTED_TOTAL,
        "deployed_soundness_claim": False,
    }
    if args.check:
        checked_sample = None if args.full else args.sample
        summary.update(verify_certificate(load_json(args.check), checked_sample))

    if args.json:
        print(render(summary), end="")
        return

    print("F_17^32 deployed sparse moving-zero witness")
    print(f"status: {summary['status']}")
    print(f"row: {summary['row']}")
    print(f"certified_bad_slopes: {summary['certified_bad_slopes']}")
    if "checked_records" in summary:
        print(f"checked_records: {summary['checked_records']}/{summary['total_records']}")


if __name__ == "__main__":
    main()
