#!/usr/bin/env python3
"""Verify the near-aligned negative diagonal-(1,1,2) q-slice packet."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[2]
CERTIFICATE = (
    ROOT
    / "experimental/data/certificates/"
    "kb-mca-v4-m2-diagonal-112-near-negative-qslice-v1/"
    "kb_mca_v4_m2_diagonal_112_near_negative_qslice_v1.json"
)
SAGE_REPLAY = (
    ROOT
    / "experimental/scripts/"
    "verify_kb_mca_v4_m2_diagonal_112_near_negative_qslice_v1.sage"
)
WOLFRAM_REPLAY = (
    ROOT
    / "experimental/scripts/"
    "verify_kb_mca_v4_m2_diagonal_112_near_negative_qslice_v1.wl"
)
PARENT = {
    "certificate_blob_oid": "844b7885620bf10fe19336f3acd7866cf1d9a204",
    "certificate_path": (
        "experimental/data/certificates/"
        "kb-mca-v4-m2-u2-universal-source-facet-census-v1/"
        "kb_mca_v4_m2_u2_universal_source_facet_census_v1.json"
    ),
    "commit": "c2edcfa5cbfb8a41e7dea04ae1b34325c90ed5dc",
    "note_blob_oid": "cc315015998cf9ab0ecf2970c13f1e27f1f132d6",
    "note_path": (
        "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_m2_u2_universal_source_facet_census_v1.md"
    ),
    "verifier_blob_oid": "e810f286d5b67d19660c3c382501a690e3e76fb0",
    "verifier_path": (
        "experimental/scripts/"
        "verify_kb_mca_v4_m2_u2_universal_source_facet_census_v1.py"
    ),
}


class VerificationError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_certificate() -> dict[str, Any]:
    raw = CERTIFICATE.read_text()
    data = json.loads(
        raw,
        object_pairs_hook=reject_duplicate_keys,
    )
    canonical = json.dumps(
        data, sort_keys=True, indent=2, ensure_ascii=False
    ) + "\n"
    require(raw == canonical, "certificate canonical formatting")
    return data


def payload_hash(data: dict[str, Any]) -> str:
    payload = copy.deepcopy(data)
    payload.pop("payload_sha256", None)
    encoded = json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode()
    return hashlib.sha256(encoded).hexdigest()


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_blob(commit: str, path: str) -> str:
    process = subprocess.run(
        ["git", "rev-parse", f"{commit}:{path}"],
        cwd=ROOT,
        check=False,
        text=True,
        capture_output=True,
    )
    require(process.returncode == 0, f"missing parent path: {commit}:{path}")
    return process.stdout.strip()


def poly_trim(poly: list[int]) -> list[int]:
    result = list(poly)
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result


def poly_add(left: list[int], right: list[int], prime: int) -> list[int]:
    return poly_trim(
        [
            (
                (left[index] if index < len(left) else 0)
                + (right[index] if index < len(right) else 0)
            )
            % prime
            for index in range(max(len(left), len(right)))
        ]
    )


def poly_scale(poly: list[int], scalar: int, prime: int) -> list[int]:
    return poly_trim([(scalar * value) % prime for value in poly])


def poly_multiply(left: list[int], right: list[int], prime: int) -> list[int]:
    result = [0] * (len(left) + len(right) - 1)
    for left_index, left_value in enumerate(left):
        for right_index, right_value in enumerate(right):
            result[left_index + right_index] = (
                result[left_index + right_index] + left_value * right_value
            ) % prime
    return poly_trim(result)


def poly_divide_exact(
    dividend: list[int], divisor: list[int], prime: int
) -> list[int]:
    work = poly_trim(dividend)
    divisor = poly_trim(divisor)
    quotient = [0] * (len(work) - len(divisor) + 1)
    while len(work) >= len(divisor) and work != [0]:
        shift = len(work) - len(divisor)
        coefficient = work[-1] * pow(divisor[-1], -1, prime) % prime
        quotient[shift] = coefficient
        for index, value in enumerate(divisor):
            work[index + shift] = (
                work[index + shift] - coefficient * value
            ) % prime
        work = poly_trim(work)
    require(work == [0], "positive control exact division")
    return poly_trim(quotient)


def evaluate_T_rows(
    rows: list[list[int]], point: int, prime: int
) -> list[int]:
    result = [0]
    power = 1
    for row in rows:
        result = poly_add(result, poly_scale(row, power, prime), prime)
        power = power * point % prime
    return result


def replay_positive_control(control: dict[str, Any]) -> None:
    prime = control["field_prime"]
    require(prime == 43, "positive control prime")
    require(control["template"] == "fixed-moving", "positive control template")
    require(len(set(control["labels"])) == 12, "positive control labels distinct")
    require(0 not in control["labels"], "positive control labels nonzero")
    require(
        control["labels"] == control["J"] + control["I"],
        "positive control label order",
    )
    require(
        control["J"]
        == [
            2,
            pow(2, -1, prime),
            control["b"],
            pow(control["b"], -1, prime),
            control["c"],
            control["d"],
        ],
        "positive control J orientation",
    )
    require(
        control["I"]
        == [
            control["z"],
            pow(control["z"], -1, prime),
            control["w"],
            control["t_tau_ell"],
            control["s_tau_xi"],
            control["xi"],
        ],
        "positive control I orientation",
    )
    require(
        set(control["J"]).isdisjoint(control["I"])
        and set(control["J"]) | set(control["I"]) == set(control["labels"]),
        "positive control I/J partition",
    )
    require(
        control["K"] == control["I"][:-1],
        "positive control K facet",
    )
    require(
        control["w"] == pow(control["c"], -1, prime)
        and control["t_tau_ell"] == pow(control["d"], -1, prime)
        and control["xi"] == pow(control["s_tau_xi"], -1, prime),
        "positive control involution labels",
    )
    require(
        control["z"] * control["I"][1] % prime == 1
        and control["s_tau_xi"] * control["xi"] % prime == 1,
        "positive control remaining reciprocal pairs",
    )

    u_rows = control["U_coefficients_by_T_degree"]
    v_rows = control["V_coefficients_by_T_degree"]
    require(
        u_rows[2] == list(reversed(u_rows[0]))
        and u_rows[1] == list(reversed(u_rows[1])),
        "positive control U reciprocity",
    )
    require(
        v_rows[2] == list(reversed(v_rows[0]))
        and v_rows[1] == list(reversed(v_rows[1])),
        "positive control V reciprocity",
    )
    quotients = []
    for root, expected in zip(
        (control["c"], control["d"]),
        (control["q_c"], control["q_d"]),
    ):
        u_at = evaluate_T_rows(u_rows, root, prime)
        v_at = evaluate_T_rows(v_rows, root, prime)
        norm = poly_add(
            poly_multiply(u_at, u_at, prime),
            poly_scale([0] + poly_multiply(v_at, v_at, prime), -1, prime),
            prime,
        )
        w = control["w"]
        quotient = poly_divide_exact(
            norm, [w * w % prime, -2 * w % prime, 1], prime
        )
        require(quotient == expected, "positive control residual quadratic")
        quotients.append(quotient)

    observed = poly_multiply(quotients[0], quotients[1], prime)
    target = [1]
    for root in (control["t_tau_ell"], control["s_tau_xi"]):
        target = poly_multiply(target, [root * root % prime, -2 * root, 1], prime)
    target = poly_scale(target, 13, prime)
    require(observed == target, "positive control q-slice factorization")

    product_h = [1]
    for label in control["J"]:
        u_at = evaluate_T_rows(u_rows, label, prime)
        v_at = evaluate_T_rows(v_rows, label, prime)
        h_at = [0] * max(2 * len(u_at) - 1, 2 * len(v_at))
        for index, value in enumerate(u_at):
            h_at[2 * index] = (h_at[2 * index] + value) % prime
        for index, value in enumerate(v_at):
            h_at[2 * index + 1] = (h_at[2 * index + 1] + value) % prime
        product_h = poly_multiply(product_h, h_at, prime)
    has_odd_coefficient = any(
        value for index, value in enumerate(product_h) if index % 2
    )
    require(has_odd_coefficient, "positive control full-quotient parity failure")
    require(
        control["full_quotient_even_pullback"] is False,
        "positive control scope",
    )


def verify_data(data: dict[str, Any]) -> None:
    require(
        data["schema"] == "kb-mca-v4-m2-diagonal-112-near-negative-qslice-v1",
        "schema",
    )
    require(data["payload_sha256"] == payload_hash(data), "payload hash")
    require(
        data["scope"]
        == {
            "ledger_movement": 0,
            "profile": "(a,b,c)=(1,1,2)",
            "source_branch": "source-line",
            "target": "near-aligned negative q-slice",
        },
        "scope",
    )
    require(
        data["field_context"]
        == {
            "challenge_field": "GF(2130706433^6)",
            "characteristic": 2130706433,
            "descent": "cleared-denominator integer identities reduce "
            "modulo the deployed odd prime",
            "small_characteristics_excluded": [2, 3, 5],
            "symbolic_field": "QQ(b,c,d)",
        },
        "field context",
    )
    require(
        data["conclusion"]
        == {
            "aligned_positive_deleted": False,
            "near_positive_deleted": False,
            "near_negative_deleted": True,
            "row_112_deleted": False,
            "terminal": "DELETED_BY_FORBIDDEN_XI_TAU_ELL_COLLISION",
        },
        "conclusion",
    )
    near = data["near_negative"]
    require(
        near["loci"]
        == ["fixed-moving:B", "moving-moving:B", "moving-moving:C"],
        "negative loci",
    )
    require(
        near["nonzero_denominators"]
        == {
            "common": ["d", "Lambda"],
            "fixed-moving:B": ["P"],
            "moving-moving:B": ["P"],
            "moving-moving:C": ["Q"],
        },
        "denominators",
    )
    require(
        near["inherited_chart_units"]
        == "all incidence and reconstruction denominators declared nonzero "
        "in parent equations (9.25)-(9.26)",
        "inherited chart units",
    )
    require(
        near["evaluation_identity"] == "R(1/d)=Phi^2/(d^4*Lambda^4)",
        "evaluation identity",
    )
    require(
        near["difference_identity"]
        == "R(W)-((W-1/d)(W-d))^2=2*Phi/(d*Lambda^2)*(W+W^3)"
        "-Phi*Psi/(d^2*Lambda^4)*W^2",
        "difference identity",
    )
    require(
        near["default_minor_identity"]
        == "det(0,1,2,3)=3*(d-2)*(2d-1)*(c-2)*(c+d)*(2c-1)"
        "*(c-1)^4*(c+1)^4*(cd-1)*A/(c^4*Lambda^4)",
        "default minor identity",
    )
    require(
        near["lambda_parent_relation"]
        == "Lambda=c*E after w=1/c; parent chart has c*E nonzero",
        "Lambda parent relation",
    )
    require(
        near["leading_coefficient_identity"]
        == "lc=(c-1)^2*(c+1)^-2*(d-1)^2*(d+1)^2*(cd-1)^4"
        "*A^-4*Lambda^4",
        "leading coefficient identity",
    )
    require(
        near["residual_when_phi_zero"]
        == "((W-tau(ell))(W-ell))^2",
        "residual factorization",
    )
    require(
        near["terminal_implication"]
        == "target equality forces tau(xi)=ell, hence xi=tau(ell) in K, "
        "contradicting xi in I\\K",
        "terminal implication",
    )
    require(
        near["polynomials"]
        == {
            "Lambda_sha256": "e0321c19b9cf82b6f56a2a1f9905dcb96e506520be6621de01a33d66f3b00c8a",
            "Phi_sha256": "d2b294670e7f4d0afe675c1f00f4e88c16d5f147ba061c63be46fe1b0fd680a0",
            "Psi_sha256": "f24e8c678524b56faef5a27aab257da9bec19d5cf9c75b26c1dc3f7a70b57a6f",
        },
        "polynomial hashes",
    )
    require(
        data["label_map"]
        == {
            "I": [
                "tau(eta)",
                "tau(ell)",
                "tau(xi)",
                "xi",
                "z",
                "tau(z)",
            ],
            "J0": ["2", "1/2", "b", "1/b"],
            "J1": ["eta=c", "ell=d"],
            "K": [
                "tau(eta)",
                "tau(ell)",
                "tau(xi)",
                "z",
                "tau(z)",
            ],
            "forced_value": "w=tau(eta)=1/c",
            "target_roots": ["tau(ell)=1/d", "tau(xi)"],
        },
        "label map",
    )
    require(
        data["nonclaims"]
        == [
            "The near-aligned positive sign is not deleted.",
            "The aligned positive sign is not deleted.",
            "The full diagonal (1,1,2) row is not deleted.",
            "No owner, payment, K3 value, or KoalaBear row bound is booked.",
            "The GF(43) positive packet is a q-slice control, not a "
            "deployed-field component.",
        ],
        "nonclaims",
    )

    parent = data["parent"]
    require(parent == PARENT, "exact parent binding")
    for kind in ("certificate", "note", "verifier"):
        require(
            git_blob(parent["commit"], parent[f"{kind}_path"])
            == parent[f"{kind}_blob_oid"],
            f"parent {kind} binding",
        )
    require(
        data["replays"]["sage_script_sha256"] == file_hash(SAGE_REPLAY),
        "Sage replay hash",
    )
    require(
        data["replays"]["wolfram_script_sha256"] == file_hash(WOLFRAM_REPLAY),
        "Wolfram replay hash",
    )
    require(
        data["replays"]["sage_payload_sha256"]
        == "b084042da8e91a531b7fc474f1c93f7a1467f4f98d9ec85b717f985754bf7cda",
        "Sage payload binding",
    )
    replay_positive_control(data["positive_qslice_control"])


def tamper_selftest(data: dict[str, Any]) -> int:
    mutations: list[Callable[[dict[str, Any]], None]] = [
        lambda x: x.__setitem__("schema", "wrong"),
        lambda x: x.__setitem__("payload_sha256", "0" * 64),
        lambda x: x["scope"].__setitem__("ledger_movement", 1),
        lambda x: x["scope"].__setitem__("profile", "wrong"),
        lambda x: x["scope"].__setitem__("source_branch", "biquadratic"),
        lambda x: x["field_context"].__setitem__("characteristic", 43),
        lambda x: x["field_context"]["small_characteristics_excluded"].pop(),
        lambda x: x["conclusion"].__setitem__("near_negative_deleted", False),
        lambda x: x["conclusion"].__setitem__("near_positive_deleted", True),
        lambda x: x["conclusion"].__setitem__("row_112_deleted", True),
        lambda x: x["near_negative"]["loci"].pop(),
        lambda x: x["near_negative"]["nonzero_denominators"]["common"].pop(),
        lambda x: x["near_negative"].__setitem__("inherited_chart_units", "wrong"),
        lambda x: x["near_negative"].__setitem__("evaluation_identity", "wrong"),
        lambda x: x["near_negative"].__setitem__("difference_identity", "wrong"),
        lambda x: x["near_negative"].__setitem__("default_minor_identity", "wrong"),
        lambda x: x["near_negative"].__setitem__("lambda_parent_relation", "wrong"),
        lambda x: x["near_negative"].__setitem__(
            "leading_coefficient_identity", "wrong"
        ),
        lambda x: x["near_negative"].__setitem__(
            "residual_when_phi_zero", "wrong"
        ),
        lambda x: x["near_negative"].__setitem__("terminal_implication", "wrong"),
        lambda x: x["near_negative"]["polynomials"].__setitem__(
            "Phi_sha256", "0" * 64
        ),
        lambda x: x["label_map"]["J1"].reverse(),
        lambda x: x["label_map"]["target_roots"].reverse(),
        lambda x: x["label_map"]["I"].pop(),
        lambda x: x["label_map"]["K"].remove("tau(ell)"),
        lambda x: x["label_map"]["K"].__setitem__(2, "xi"),
        lambda x: x["label_map"]["K"].append("xi"),
        lambda x: x["parent"].__setitem__("commit", "0" * 40),
        lambda x: x["parent"].__setitem__("note_blob_oid", "0" * 40),
        lambda x: x["replays"].__setitem__("sage_script_sha256", "0" * 64),
        lambda x: x["replays"].__setitem__("wolfram_script_sha256", "0" * 64),
        lambda x: x["replays"].__setitem__("sage_payload_sha256", "0" * 64),
        lambda x: x["positive_qslice_control"].__setitem__("field_prime", 41),
        lambda x: x["positive_qslice_control"].__setitem__("w", 37),
        lambda x: x["positive_qslice_control"].__setitem__("b", 27),
        lambda x: x["positive_qslice_control"].__setitem__("z", 24),
        lambda x: x["positive_qslice_control"]["labels"].pop(),
        lambda x: x["positive_qslice_control"]["K"].__setitem__(2, 24),
        lambda x: x["positive_qslice_control"][
            "U_coefficients_by_T_degree"
        ][2].__setitem__(0, 39),
        lambda x: x["positive_qslice_control"][
            "V_coefficients_by_T_degree"
        ][2].__setitem__(0, 33),
        lambda x: x["positive_qslice_control"]["q_c"].__setitem__(0, 35),
        lambda x: x["positive_qslice_control"]["q_d"].__setitem__(2, 39),
        lambda x: x["positive_qslice_control"].__setitem__(
            "full_quotient_even_pullback", True
        ),
        lambda x: x["positive_qslice_control"]["J"].__setitem__(0, 23),
        lambda x: x["nonclaims"].pop(),
    ]
    rejected = 0
    accepted: list[int] = []
    payload_only_mutation = 1
    for mutation_index, mutation in enumerate(mutations):
        candidate = copy.deepcopy(data)
        mutation(candidate)
        if mutation_index != payload_only_mutation:
            candidate["payload_sha256"] = payload_hash(candidate)
        try:
            verify_data(candidate)
        except (VerificationError, ValueError, KeyError, IndexError):
            rejected += 1
        else:
            accepted.append(mutation_index)
    require(
        rejected == len(mutations),
        f"tamper rejection count; accepted={accepted}",
    )
    return rejected


def main() -> None:
    require(__debug__, "optimized Python is unsupported")
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()
    require(args.check or args.tamper_selftest, "select a verifier mode")
    data = load_certificate()
    verify_data(data)
    print(
        "PASS near-negative q-slice "
        f"payload={data['payload_sha256']} "
        "terminal=DELETED_BY_FORBIDDEN_XI_TAU_ELL_COLLISION"
    )
    if args.tamper_selftest:
        rejected = tamper_selftest(data)
        print(f"PASS tamper self-test: {rejected}/{rejected} rejected")


if __name__ == "__main__":
    main()
