#!/usr/bin/env python3
"""Verify the boundary barycentric obstruction to separated rank-6 finite closure."""

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


SCHEMA_VERSION = "f17-32-m3-rank6-boundary-barycentric-obstruction-v1"
Q_LINE = 17**32
TARGET_BITS = 128
FINITE_BUDGET = Q_LINE // 2**TARGET_BITS
PROJECTIVE_DENOMINATOR = Q_LINE + 1
PROJECTIVE_BUDGET = PROJECTIVE_DENOMINATOR // 2**TARGET_BITS
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
ENDPOINT_UNIFORM_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-rank6-projective-endpoint-uniform/"
    "f17_32_n512_k256_m3_rank6_projective_endpoint_uniform.json"
)
PROJECTIVE_BUDGET_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-m4-projective-budget-split/"
    "f17_32_n512_k256_m3_m4_projective_budget_split.json"
)


FIELD = Field(P, MODULUS)
ZERO = FIELD.zero
ONE = FIELD.one


def f_add(left: Any, right: Any) -> tuple[int, ...]:
    a = FIELD.normalize(left)
    b = FIELD.normalize(right)
    return tuple((a_i + b_i) % P for a_i, b_i in zip(a, b))


def f_sub(left: Any, right: Any) -> tuple[int, ...]:
    a = FIELD.normalize(left)
    b = FIELD.normalize(right)
    return tuple((a_i - b_i) % P for a_i, b_i in zip(a, b))


def f_mul(left: Any, right: Any) -> tuple[int, ...]:
    return FIELD.mul(left, right)


def f_inv(value: Any) -> tuple[int, ...]:
    element = FIELD.normalize(value)
    if element == ZERO:
        raise ZeroDivisionError("zero field inverse")
    return FIELD.pow(element, FIELD.size - 2)


def f_is_zero(value: Any) -> bool:
    return FIELD.normalize(value) == ZERO


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


def field_encode_short(value: tuple[int, ...]) -> list[int]:
    return list(FIELD.normalize(value))


def powers(element: tuple[int, ...], count: int) -> list[tuple[int, ...]]:
    out = []
    cur = ONE
    for _ in range(count):
        out.append(cur)
        cur = f_mul(cur, element)
    return out


def barycentric_weights(nodes: list[tuple[int, ...]]) -> list[tuple[int, ...]]:
    weights = []
    for i, node_i in enumerate(nodes):
        denominator = ONE
        for j, node_j in enumerate(nodes):
            if i == j:
                continue
            denominator = f_mul(denominator, f_sub(node_i, node_j))
        weights.append(f_inv(denominator))
    return weights


def moment_sums(
    nodes: list[tuple[int, ...]], weights: list[tuple[int, ...]], count: int
) -> list[tuple[int, ...]]:
    node_powers = [powers(node, count) for node in nodes]
    sums = []
    for exponent in range(count):
        total = ZERO
        for node_index, weight in enumerate(weights):
            total = f_add(total, f_mul(weight, node_powers[node_index][exponent]))
        sums.append(total)
    return sums


def check_dependency_window(ref: str, data: dict[str, Any]) -> None:
    if "window" in data:
        require(data["window"]["A_min"] <= min(A_VALUES), f"{ref}: A_min too large")
        require(data["window"]["A_max"] >= max(A_VALUES), f"{ref}: A_max too small")
    if "row" in data:
        require(data["row"]["n"] == N, f"{ref}: n mismatch")
        require(data["row"]["k"] == K, f"{ref}: k mismatch")


def agreement_record(agreement: int, domain: list[tuple[int, ...]]) -> dict[str, Any]:
    j_value = N - agreement
    t_value = agreement - K
    column_count = j_value + 1
    support_size = column_count + RANK
    deficit = support_size - t_value

    require(deficit > 0, f"A={agreement}: not a boundary-deficit agreement")
    require(t_value <= support_size - 1, f"A={agreement}: barycentric annihilator too short")
    require(column_count >= RANK + 1, f"A={agreement}: endpoint survivor count fails")

    sample_nodes = domain[:support_size]
    sample_weights = barycentric_weights(sample_nodes)
    require(all(weight != ZERO for weight in sample_weights), f"A={agreement}: zero residue")
    sums = moment_sums(sample_nodes, sample_weights, t_value)
    require(all(f_is_zero(value) for value in sums), f"A={agreement}: moment sum did not vanish")
    next_sum = moment_sums(sample_nodes, sample_weights, support_size)[-1]
    require(next_sum != ZERO, f"A={agreement}: unexpected zero top residue moment")

    return {
        "A": agreement,
        "j": j_value,
        "t": t_value,
        "base_support_size": column_count,
        "direction_support_size": RANK,
        "combined_support_size": support_size,
        "boundary_deficit": deficit,
        "support_choice_count": comb(N, column_count) * comb(N - column_count, RANK),
        "obstruction_weights": {
            "support_uniform_formula": (
                "for S=X union Y, set omega_s = 1 / prod_{r in S, r!=s}(s-r); "
                "use a_x=omega_x and b_y=omega_y"
            ),
            "finite_root": "z=1",
            "kernel_locator": "ell(T)=1",
            "moment_range": f"0 <= r < {t_value}",
            "moment_identity": "sum_{s in S} omega_s s^r = 0 for 0 <= r <= |S|-2",
            "sample_prefix_weight_hash": hash_value([field_encode_short(w) for w in sample_weights]),
            "sample_top_moment_nonzero": field_encode_short(next_sum),
        },
        "finite_affine": {
            "z_zero_rank": column_count,
            "z_one_rank_drop": True,
            "finite_root_lower_bound": 1,
            "finite_root_witness": 1,
            "finite_budget": FINITE_BUDGET,
        },
        "projective_infinity": {
            "endpoint_source": ENDPOINT_UNIFORM_REF,
            "projective_endpoint_lower_bound": 1,
            "projective_total_lower_bound": 2,
            "projective_budget": PROJECTIVE_BUDGET,
        },
    }


def build_certificate() -> dict[str, Any]:
    descriptor = load_json(ROW_DESCRIPTOR_REF)
    rank_drop = load_json(RANK_DROP_BRIDGE_REF)
    endpoint_uniform = load_json(ENDPOINT_UNIFORM_REF)
    projective_budget = load_json(PROJECTIVE_BUDGET_REF)

    require(descriptor["row"]["n"] == N, "descriptor n mismatch")
    require(descriptor["row"]["k"] == K, "descriptor k mismatch")
    require(descriptor["row"]["field"] == "F_17^32", "descriptor field mismatch")
    require(descriptor["row"]["field_order"] == Q_LINE, "descriptor q mismatch")
    require(descriptor["row"]["syndrome_length"] == N - K, "descriptor syndrome mismatch")
    require(
        descriptor["m3_regular_window"]["A_min"] <= min(A_VALUES)
        and descriptor["m3_regular_window"]["A_max"] >= max(A_VALUES),
        "descriptor M3 window mismatch",
    )
    require(
        rank_drop["schema_version"] == "f17-32-m3-m5-regular-root-rank-drop-v1",
        "rank-drop schema mismatch",
    )
    require(
        endpoint_uniform["schema_version"]
        == "f17-32-m3-rank6-projective-endpoint-uniform-v1",
        "endpoint-uniform schema mismatch",
    )
    require(
        projective_budget["schema_version"] == "f17-32-m3-m4-projective-budget-split-v1",
        "projective budget schema mismatch",
    )
    for ref, data in {
        RANK_DROP_BRIDGE_REF: rank_drop,
        ENDPOINT_UNIFORM_REF: endpoint_uniform,
        PROJECTIVE_BUDGET_REF: projective_budget,
    }.items():
        check_dependency_window(ref, data)

    domain_encodings = descriptor["domain"]["domain_encodings"]
    require(len(domain_encodings) == N, "domain length mismatch")
    require(len(set(domain_encodings)) == N, "descriptor domain is not distinct")
    require(N % P != 0, "X^512-1 is not separable in this characteristic")
    domain = [FIELD.decode(value) for value in domain_encodings]
    require(
        [FIELD.encode(value) for value in domain] == domain_encodings,
        "domain decode/encode roundtrip failed",
    )

    records = [agreement_record(agreement, domain) for agreement in A_VALUES]
    require([record["boundary_deficit"] for record in records] == [5, 3, 1], "deficit mismatch")
    require(FINITE_BUDGET == 6 and PROJECTIVE_BUDGET == 6, "unexpected budget")

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "COUNTEREXAMPLE / PROVED",
        "object": "M3 separated rank-6 boundary barycentric finite-root obstruction",
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
            "regular_root_rank_drop": {
                "ref": RANK_DROP_BRIDGE_REF,
                "sha256": sha256_file(RANK_DROP_BRIDGE_REF),
            },
            "rank6_projective_endpoint_uniform": {
                "ref": ENDPOINT_UNIFORM_REF,
                "sha256": sha256_file(ENDPOINT_UNIFORM_REF),
            },
            "m4_projective_budget_split": {
                "ref": PROJECTIVE_BUDGET_REF,
                "sha256": sha256_file(PROJECTIVE_BUDGET_REF),
            },
        },
        "window": {
            "agreements": A_VALUES,
            "agreement_count": len(A_VALUES),
        },
        "family": {
            "base_support": "any subset X of H with |X|=j+1",
            "direction_support": "any subset Y of H\\X with |Y|=6",
            "combined_support": "S=X union Y",
            "weights": (
                "choose barycentric residues omega_s=1/prod_{r in S,r!=s}(s-r); "
                "set a_x=omega_x and b_y=omega_y"
            ),
            "finite_root": "z=1",
            "kernel_locator": "constant locator ell(T)=1",
        },
        "theorem": {
            "boundary_deficit": (
                "For A=385,386,387, the combined separated support has size "
                "j+7, while t=A-256 is smaller by 5,3,1 respectively."
            ),
            "barycentric_identity": (
                "For any distinct support S and residues omega_s=1/prod_{r!=s}(s-r), "
                "sum_s omega_s s^e=0 for 0<=e<=|S|-2."
            ),
            "finite_root_obstruction": (
                "Since t<=|S|-1 in the three boundary agreements, the constant "
                "locator ell=1 lies in ker H(u+v), giving a finite rank-drop "
                "slope z=1 with nonzero separated weights."
            ),
            "regular_base": (
                "At z=0, the base support X has size j+1 and t>=j+1, so "
                "H(u) has full column rank by weighted Vandermonde factorization."
            ),
            "projective_endpoint": (
                "The endpoint-uniform theorem applies to the same nonzero weights, "
                "so the projective endpoint [0:1] is also present."
            ),
            "consequence": (
                "The separated six-spike tall closure is sharp at A=388: it "
                "cannot be extended support/weight-uniformly to A=385,386,387 "
                "with an empty finite root table."
            ),
        },
        "sampler_denominators": {
            "finite_line": {
                "denominator": Q_LINE,
                "denominator_formula": "|F|",
                "budget_floor_denominator_over_2_128": FINITE_BUDGET,
            },
            "projective_line": {
                "denominator": PROJECTIVE_DENOMINATOR,
                "denominator_formula": "|P^1(F)| = |F| + 1",
                "budget_floor_denominator_over_2_128": PROJECTIVE_BUDGET,
            },
        },
        "field_audit": {
            "full_domain_distinct": True,
            "domain_size": len(domain_encodings),
            "domain_hash": hash_value(domain_encodings),
            "decoded_roundtrip_hash": hash_value([FIELD.encode(value) for value in domain]),
            "x_512_minus_1_squarefree": True,
        },
        "agreement_records": records,
        "summary": {
            "agreement_count": len(records),
            "boundary_deficits": [record["boundary_deficit"] for record in records],
            "finite_root_lower_bound_per_agreement": 1,
            "finite_root_witness": 1,
            "projective_endpoint_lower_bound_per_agreement": 1,
            "projective_total_lower_bound_per_agreement": 2,
            "finite_budget": FINITE_BUDGET,
            "projective_budget": PROJECTIVE_BUDGET,
            "support_weight_uniform_empty_finite_table_refuted": True,
        },
        "checks": [
            "row descriptor and dependency schemas match",
            "domain has 512 distinct nonzero elements and X^512-1 is separable",
            "boundary deficits are 5,3,1 for A=385,386,387",
            "barycentric residues are nonzero on the sampled prefix supports",
            "sampled barycentric moment sums vanish through the required t rows",
            "z=0 is full rank by weighted Vandermonde on X",
            "z=1 has the constant locator in the finite kernel",
            "endpoint-uniform dependency supplies the projective split-locator witness",
        ],
        "nonclaims": [
            "does not compute the exact finite root count for these weights",
            "does not produce an over-budget support-wise MCA lower bound",
            "does not classify overlapping-support rank-6 pencils",
            "does not refute the prefix/unit-weight boundary dual-gcd closure",
            "does not prove endpoint payment by quotient, tangent, or extension ledgers",
        ],
    }


def check_certificate(path: Path, certificate: dict[str, Any]) -> None:
    expected = render(certificate)
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"rank-6 boundary barycentric obstruction mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    summary = certificate["summary"]
    print("F_17^32 M3 rank-6 boundary barycentric obstruction")
    print("A={}".format(",".join(str(value) for value in certificate["window"]["agreements"])))
    print(
        "finite root lower bound={finite_root_lower_bound_per_agreement}, projective total lower bound={projective_total_lower_bound_per_agreement}".format(
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
        check_certificate(args.check, certificate)
    print_summary(certificate)


if __name__ == "__main__":
    main()
