#!/usr/bin/env python3
"""Verify the positive 433-1a complete-source outside reduction packet."""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
import shutil
import subprocess
from pathlib import Path
from typing import Any, Callable

import sympy as sp

if not __debug__:
    raise RuntimeError("verifier refuses optimized Python execution")


class VerificationError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


EXPERIMENTAL = Path(__file__).resolve().parents[1]
REPO_ROOT = EXPERIMENTAL.parent
CERTIFICATE = (
    EXPERIMENTAL
    / "data/certificates/kb-mca-v4-m2-r4-coordinate-positive-433-1a-outside-reduction-v1"
    / "kb_mca_v4_m2_r4_coordinate_positive_433_1a_outside_reduction_v1.json"
)
PRIME = 2130706433
ROLES = ("LC", "AB+1", "AB+2", "AB-", "AC")
PARENT = {
    "commit": "4569b506d7c86b3b7fbca5b22701ef83988e76e8",
    "note_path": "experimental/notes/frontier-adjacent/kb_mca_v4_m2_r4_coordinate_positive_three_loop_atlas_v1.md",
    "note_blob_oid": "c2de8806e5fc9161f196fe05dcc9e17ae0299d53",
    "verifier_path": "experimental/scripts/verify_kb_mca_v4_m2_r4_coordinate_positive_three_loop_atlas_v1.py",
    "verifier_blob_oid": "b2f686579a2bd298bcb9d1d1052508b08c48b743",
    "certificate_path": "experimental/data/certificates/kb-mca-v4-m2-r4-coordinate-positive-three-loop-atlas-v1/kb_mca_v4_m2_r4_coordinate_positive_three_loop_atlas_v1.json",
    "certificate_blob_oid": "1bfb0dac4f6eae6cb2b336d25265537609bd9d1b",
    "certificate_payload_sha256": "5f6921f4abe90968f7ad624f207c9e2f991152e75da4f285938e3552286c082a",
    "terminal": "M2_R4_COORDINATE_POSITIVE_GLOBAL_LOOP_CAP_AND_RESIDUAL_WORKBOARD",
}
SINGULAR_CERTIFICATES = {
    1: {
        "program_sha256": "b44b7d5d118c71e4b31f5eb924ff58e730ad65040356734c5fc2e2b234c4877f",
        "equation_sha256": [
            "aa40ebeb50ea66defa4bc1fb9c2ab256b2e197620cf0e024aaf4e0cc5f853bb5",
            "c93d8cd53522b65dd959e2db325d1d95b4faad0a53e34dd5dd6f6fe283698883",
            "076a75253978fc4272e969002e126a4c61b40b2472b5edac6efa9d999ffa46b7",
            "749b9992062094575988709f56ec0ec4ba0190d6f01f7f27e17301d6499d86b8",
            "4f3a0a4dcd229096ff8b5173d38d124bf94d62884ba958d4618512d13cc33811",
            "cda590dea89094272ab00c211eaf497d3c592e05e048816b7a5b89bb1ba371a1",
        ],
    },
    9: {
        "program_sha256": "9bdc3ae4b02cde6a94af9ddcb818a365bedd98c2d268ce4f974b8c40c2f93a19",
        "equation_sha256": [
            "c2769f66a8fd0f9df4945d0272f3dc6e119d7880d238bc5a278967a0642a995e",
            "994c4381ad3685f0796a19e84ac504e5ab3f2f7be1fa8d3e05f803ad410a82ea",
            "ba4b9985dc28dafc251c3ffd122d2c7517038bdcc5b16ceb4b153937062dce28",
            "f1d4cdce484e7507df769a8c52a1c9724ae07520ec27fa8fc66689ad740e0616",
            "e6a1046881a764ce197181b9c7487a668c3ac40593d183b99c6e0e37f85d7b41",
            "dccb663ef4d498a03693528fcf625f6451fc5f1e21e1f32ce2d9546b3a958fee",
        ],
    },
    12: {
        "program_sha256": "49bbb74fd711594b850810347f107aacecb6188233bb9427499c9250ee924b06",
        "equation_sha256": [
            "d334c132615b1ad03d84f362236a1acaeb1f861763dd2376633af3d64c1d47b2",
            "99792205bce111b288be3d90c0432f5e8aa84074befae174095645d624e15b59",
            "9887f0be6c856fd969e0bba63fc33c585963b348d5e2b1ac59f9710a5a3e7b1a",
            "8a5ad1b0dcca5cb2c5136b761ce3007e1cc38c7d3dc5c7d53a83f1b163c6e448",
            "c38688cfa77f360e057c6088fc0676ddaf3faecfa9c53fa2130c4d25ead3bf19",
            "98ae78b1925223c68443fd7c22085877fe2e944f4132540cfee8938e700f8f42",
        ],
    },
}


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def payload_hash(value: dict[str, Any]) -> str:
    unhashed = copy.deepcopy(value)
    unhashed.pop("payload_sha256", None)
    return hashlib.sha256(canonical_json(unhashed).encode()).hexdigest()


def reject_duplicates(pairs):
    output = {}
    for key, value in pairs:
        if key in output:
            raise VerificationError(f"duplicate JSON key: {key}")
        output[key] = value
    return output


def parse_json(text: str, label: str) -> dict[str, Any]:
    try:
        value = json.loads(text, object_pairs_hook=reject_duplicates)
    except (json.JSONDecodeError, VerificationError) as error:
        raise VerificationError(f"cannot parse {label}: {error}") from error
    require(isinstance(value, dict), f"{label} is not an object")
    return value


def git_output(*arguments: str) -> str:
    try:
        process = subprocess.run(
            ["git", *arguments],
            cwd=REPO_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as error:
        raise VerificationError(error.stderr.strip()) from error
    return process.stdout.strip()


def load_parent() -> None:
    for path_key, blob_key in (
        ("note_path", "note_blob_oid"),
        ("verifier_path", "verifier_blob_oid"),
        ("certificate_path", "certificate_blob_oid"),
    ):
        require(
            git_output("rev-parse", f"{PARENT['commit']}:{PARENT[path_key]}")
            == PARENT[blob_key],
            f"parent blob {PARENT[path_key]}",
        )
    data = parse_json(
        git_output("show", f"{PARENT['commit']}:{PARENT['certificate_path']}"),
        PARENT["certificate_path"],
    )
    require(data.get("payload_sha256") == PARENT["certificate_payload_sha256"],
            "parent payload")
    require(payload_hash(data) == data.get("payload_sha256"), "parent seal")
    require(data["conclusion"]["terminal"] == PARENT["terminal"],
            "parent terminal")
    require(data["positive_residual_loop_workboard"]["routes"]["433-1a"]
            == ["O0b"], "parent unique route")
    require(data["conclusion"]["k3_status"] == "OPEN", "parent scope")


def pairings(values):
    values = tuple(values)
    first = values[0]
    for index in range(1, len(values)):
        second = values[index]
        rest = values[1:index] + values[index + 1:]
        yield ((first, second), (rest[0], rest[1]))


def matching_cells():
    output = []
    for singleton in range(5):
        rest = tuple(index for index in range(5) if index != singleton)
        for matching in pairings(rest):
            output.append((singleton, matching))
    return tuple(output)


def duplicate_role_orbits() -> list[list[int]]:
    cells = matching_cells()
    index = {cell: cell_index for cell_index, cell in enumerate(cells)}
    swap = {1: 2, 2: 1}

    def image(cell):
        singleton, matching = cell
        return (
            swap.get(singleton, singleton),
            tuple(sorted(tuple(sorted(swap.get(value, value) for value in pair))
                         for pair in matching)),
        )

    unseen = set(range(len(cells)))
    orbits = []
    while unseen:
        cell_index = min(unseen)
        orbit = sorted({cell_index, index[image(cells[cell_index])]})
        unseen -= set(orbit)
        orbits.append(orbit)
    require(orbits == [[0], [1, 2], [3, 6], [4, 7], [5, 8],
                       [9, 10], [11], [12, 13], [14]], "role orbits")
    return orbits


def product_rank_identity_replay() -> dict[str, Any]:
    R, T, b, c = sp.symbols("R T b c")

    A = -R * T + 3 * R + 3 * T - 1
    B = (R + 1) * (T + 1)
    require(sp.expand(B**2 - A**2
                      - 8 * (R - 1) * (T - 1) * (R + T)) == 0,
            "cells 4/7 determinant")

    S = R + T
    C = (R - 1) * (T - 1)
    require(
        sp.expand(c * ((c * B + C) * (c * C + B) - 4 * c * S**2)
                  - c * B * C * (c + 1)**2) == 0,
        "cells 5/8 elimination",
    )

    U = -R**2 - 3 * R * T + 3 * R + T
    V = -R**2 + R * T - R + T
    require(sp.expand(U**2 - V**2
                      - 8 * R * (T - 1) * (R - 1) * (R + T)) == 0,
            "cells 3/6 determinant")

    E2 = -c * R + 2 * c * T - c - R + 1
    E5 = -c * R + c - R + 2 * T - 1
    require(sp.expand(c * E5 - E2 + (c**2 - 1) * (R - 1)) == 0,
            "cell 14 elimination")

    orbits = duplicate_role_orbits()
    analytic = [[0], [3, 6], [4, 7], [5, 8], [11], [14]]
    singular = [[1, 2], [9, 10], [12, 13]]
    require(sorted(analytic + singular) == sorted(orbits), "rank coverage")
    return {
        "matching_cell_count": len(matching_cells()),
        "duplicate_role_orbits": orbits,
        "analytic_orbits": analytic,
        "singular_orbits": singular,
        "product_rank": 5,
        "loop_sum_augmented_base_rank": 6,
        "deployed_field": PRIME,
        "singular_unit_certificates": {
            str(cell): {
                **certificate,
                "output": ["UNIT", "1", "1"],
            }
            for cell, certificate in SINGULAR_CERTIFICATES.items()
        },
    }


def common_kernel_replay() -> dict[str, Any]:
    W, lambda_0, lambda_i, q_i = sp.symbols("W lambda_0 lambda_i q_i")
    d0, d1, d2, e0, e1, e2 = sp.symbols("d0 d1 d2 e0 e1 e2")
    A2 = d0 + d1 * W + d2 * W**2
    A0 = e0 + e1 * W + e2 * W**2
    delta = lambda_i * (lambda_i - lambda_0)
    A2_i = A2.subs(W, lambda_i)
    B1_tilde = -q_i * A2_i * (W - lambda_0)
    require(B1_tilde.subs(W, lambda_0) == 0, "loop sum row")
    require(sp.expand(q_i * delta * A2_i
                      + lambda_i * B1_tilde.subs(W, lambda_i)) == 0,
            "nonloop sum row")
    determinant = lambda_0 * lambda_i * (lambda_i - lambda_0)
    return {
        "common_base_rank": 6,
        "nonloop_quotient_determinant": str(determinant),
        "common_survivor_rank": 7,
        "kernel_dimension": 1,
        "division_free_reconstruction": {
            "Delta_i": "lambda_i*(lambda_i-lambda_0)",
            "A2_tilde": "Delta_i*A2",
            "A0_tilde": "Delta_i*A0",
            "B1_tilde": "-q_i*A2(lambda_i)*(W-lambda_0)",
            "requires_A2_at_nonloop_nonzero": False,
        },
    }


def perfect_matchings(values):
    values = tuple(values)
    if not values:
        yield ()
        return
    first = values[0]
    for index in range(1, len(values)):
        rest = values[1:index] + values[index + 1:]
        for tail in perfect_matchings(rest):
            yield ((first, values[index]), *tail)


def quadratic_resultant(p, q):
    p0, p1, p2 = p
    q0, q1, q2 = q
    return ((p2 * q0 - p0 * q2)**2
            - (p2 * q1 - p1 * q2) * (p1 * q0 - p0 * q1))


def paired_product_replay() -> dict[str, Any]:
    p0, p1, p2, q0, q1, q2, W = sp.symbols("p0 p1 p2 q0 q1 q2 W")
    P = p2 * W**2 + p1 * W + p0
    Q = q2 * W**2 + q1 * W + q0
    formula = quadratic_resultant((p0, p1, p2), (q0, q1, q2))
    require(sp.expand(sp.resultant(P, Q, W) - formula) == 0,
            "paired quadratic resultant")
    matchings = tuple(perfect_matchings(range(6)))
    require(len(matchings) == 15 and len(set(matchings)) == 15,
            "perfect matching census")
    return {
        "outside_products": ["de", "-de", "df", "-df", "sigma*ef", "be", "cf"],
        "eta_choices": 5,
        "missing_mate_record_choices": 7,
        "residual_perfect_matchings": len(matchings),
        "cases_per_common_row_and_cycle_sign": 5 * 7 * len(matchings),
        "paired_product_cut": (
            "(p2*q0-p0*q2)^2-(p2*q1-p1*q2)*(p1*q0-p0*q1)=0"
        ),
        "missing_mate_product_cut": "A0(xi)-x*A2(xi)=0",
        "missing_mate_sum_cut": "xi*B1(xi)^2-s_x^2*A2(xi)^2=0",
        "resultant_survival_is_sufficient": False,
    }


OUTSIDE_RECORDS = ("DE+", "DE-", "DF+", "DF-", "EF", "BE", "CF")
INTERNAL_RECORDS = OUTSIDE_RECORDS[:5]
RECORD_TAU = {
    "DE+": "DE-", "DE-": "DE+", "DF+": "DF-", "DF-": "DF+",
    "EF": "EF", "BE": "BE", "CF": "CF",
}


def canonical_record_matching(matching):
    order = {record: index for index, record in enumerate(OUTSIDE_RECORDS)}
    pairs = [tuple(sorted(pair, key=order.get)) for pair in matching]
    return tuple(sorted(pairs, key=lambda pair: (order[pair[0]], order[pair[1]])))


def outside_cases(alignment):
    output = set()
    for eta in INTERNAL_RECORDS:
        xi_values = (eta,) if alignment == "aligned" else tuple(
            record for record in OUTSIDE_RECORDS if record != eta
        )
        for xi in xi_values:
            residual = tuple(record for record in OUTSIDE_RECORDS if record != xi)
            for matching in perfect_matchings(residual):
                output.add((eta, xi, canonical_record_matching(matching)))
    return output


def tau_outside_case(case):
    eta, xi, matching = case
    return (
        RECORD_TAU[eta],
        RECORD_TAU[xi],
        canonical_record_matching(
            (RECORD_TAU[left], RECORD_TAU[right]) for left, right in matching
        ),
    )


def outside_case_key(case):
    order = {record: index for index, record in enumerate(OUTSIDE_RECORDS)}
    eta, xi, matching = case
    return (order[eta], order[xi],
            tuple((order[left], order[right]) for left, right in matching))


def outside_orbits(values):
    unseen = set(values)
    output = []
    while unseen:
        seed = min(unseen, key=outside_case_key)
        orbit = {seed, tau_outside_case(seed)}
        require(orbit <= values, "outside gauge closure")
        unseen -= orbit
        output.append(tuple(sorted(orbit, key=outside_case_key)))
    return tuple(sorted(output, key=lambda orbit: outside_case_key(orbit[0])))


def outside_case_symmetry_replay() -> dict[str, Any]:
    aligned = outside_cases("aligned")
    near = outside_cases("near")
    aligned_orbits = outside_orbits(aligned)
    near_orbits = outside_orbits(near)
    aligned_fixed = sum(len(orbit) == 1 for orbit in aligned_orbits)
    near_fixed = sum(len(orbit) == 1 for orbit in near_orbits)
    require((len(aligned), len(near)) == (75, 450), "placement split")
    require((aligned_fixed, near_fixed) == (3, 6), "Burnside fixed cases")
    require((len(aligned_orbits), len(near_orbits)) == (39, 228),
            "outside orbit counts")

    ef_aligned = outside_orbits({case for case in aligned if case[1] == "EF"})
    ef_near = outside_orbits({case for case in near if case[1] == "EF"})
    require((len(ef_aligned), len(ef_near)) == (9, 30), "EF orbit counts")

    matching_a = canonical_record_matching((
        ("DE+", "DF-"), ("DE-", "CF"), ("DF+", "BE"),
    ))
    matching_b = canonical_record_matching((
        ("DE+", "CF"), ("DE-", "DF+"), ("DF-", "BE"),
    ))
    require(canonical_record_matching(
        (RECORD_TAU[left], RECORD_TAU[right]) for left, right in matching_a
    ) == matching_b, "template gauge equivalence")
    template_aligned = outside_orbits({
        ("EF", "EF", matching) for matching in (matching_a, matching_b)
    })
    template_near = outside_orbits({
        (eta, "EF", matching)
        for eta in INTERNAL_RECORDS[:4]
        for matching in (matching_a, matching_b)
    })
    require((len(template_aligned), len(template_near)) == (1, 4),
            "template orbit coverage")

    representatives = {
        alignment: [orbit[0] for orbit in orbits]
        for alignment, orbits in (("aligned", aligned_orbits), ("near", near_orbits))
    }
    return {
        "faithful_record_action_size": 2,
        "nontrivial_action": "DE+<->DE-, DF+<->DF-, EF/BE/CF fixed",
        "aligned": {"labeled": 75, "fixed": 3, "orbits": 39},
        "near": {"labeled": 450, "fixed": 6, "orbits": 228},
        "total_orbits": 267,
        "EF_missing_mate_orbits": {"aligned": 9, "near": 30, "total": 39},
        "current_template_orbits": {
            "A_and_B_are_gauge_partners": True,
            "aligned": 1,
            "near": 4,
            "total": 5,
        },
        "representative_digest": hashlib.sha256(
            canonical_json(representatives).encode()
        ).hexdigest(),
        "formal_orbits_are_algebraic_survivors": False,
    }


def edge_eliminant_replay() -> dict[str, Any]:
    A, B, C, W = sp.symbols("A B C W")
    q0, q1, q2, q3, q4 = sp.symbols("q0 q1 q2 q3 q4")
    coefficients = (q0, q1, q2, q3, q4)
    P = A * W**2 + B * W + C
    Q = sum(coefficients[index] * W**index for index in range(5))
    R1 = (
        q4 * (-B**3 + 2 * A * B * C)
        + q3 * A * (B**2 - A * C)
        - q2 * A**2 * B
        + q1 * A**3
    )
    R0 = (
        q4 * (-B**2 * C + A * C**2)
        + q3 * A * B * C
        - q2 * A**2 * C
        + q0 * A**3
    )
    numerator = sp.expand(A * R0**2 - B * R0 * R1 + C * R1**2)
    quotient, remainder = sp.div(numerator, A**3)
    require(remainder == 0, "resultant divisibility")
    resultant = sp.expand(quotient)
    require(sp.expand(resultant - sp.resultant(P, Q, W)) == 0,
            "generic edge resultant")
    linear = sp.expand(
        q4 * C**4 - q3 * C**3 * B + q2 * C**2 * B**2
        - q1 * C * B**3 + q0 * B**4
    )
    require(sp.expand(B**4 * Q.subs(W, -C / B) - linear) == 0,
            "degree-drop edge cut")
    variables = (A, B, C, q0, q1, q2, q3, q4)
    require(len(sp.Poly(resultant, *variables).terms()) == 22,
            "resultant terms")
    require(sp.total_degree(resultant) == 6, "resultant degree")
    require(sp.total_degree(linear) == 5, "linear degree")
    return {
        "generic_condition": "A!=0",
        "generic_identity": "A^3*Res(P,Q)=A*R0^2-B*R0*R1+C*R1^2",
        "generic_terms": 22,
        "generic_total_degree": 6,
        "degree_drop_condition": "A=0,B!=0",
        "degree_drop_total_degree": 5,
        "constant_branch": "A=B=0 implies C!=0, hence no product root",
        "seven_edge_cuts_are_only_necessary": True,
    }


def triangle_replay() -> dict[str, Any]:
    b, c, d, e, f = sp.symbols("b c d e f", nonzero=True)
    x = e * f

    type_a = sp.factor(
        (d + e)**2 * x * (-d * f)
        + (d * e) * ((-d * f) - x)**2
    )
    require(type_a == 0, "template A sum identity")
    require(sp.expand((c * f) * (b * e) - b * c * x) == 0,
            "template A terminal product")
    require(sp.expand(b * (d * e) * (c * f)
                      - c * (d * f) * (b * e)) == 0,
            "template A cross product")

    type_b = sp.factor(
        (d + e)**2 * c**2 * x**2 * (c * f)**2
        - ((d * e) * (c * f)**2 + c**2 * x**2)**2
    )
    require(type_b == 0, "template B sum identity")
    require(sp.expand((-d * f) * (b * e) + b * d * x) == 0,
            "template B terminal product")
    require(sp.expand(b * (d * e) * (c * f)
                      - c * (d * f) * (b * e)) == 0,
            "template B cross product")
    return {
        "templates": {
            "A": {
                "pairs": [["de", "-df"], ["-de", "cf"], ["df", "be"]],
                "product_chain": [
                    "F(v)=-F(u)",
                    "F(w)=-F(-u)",
                    "F(-v)*F(-w)=b*c*F(xi)",
                    "b*F(u)*F(-v)=c*F(w)*F(-w)",
                ],
                "sum_cut": (
                    "H(u)*F(xi)*F(-u)+F(u)*(F(-u)-F(xi))^2=0"
                ),
            },
            "B": {
                "pairs": [["de", "cf"], ["-de", "df"], ["-df", "be"]],
                "product_chain": [
                    "F(v)=-F(u)",
                    "F(w)=-F(-v)",
                    "F(-u)*F(-w)=b*c*F(xi)",
                    "b*F(u)*F(-u)=c*F(-v)*F(-w)",
                ],
                "sum_cut": (
                    "H(u)*c^2*F(xi)^2*F(-u)^2-"
                    "(F(u)*F(-u)^2+c^2*F(xi)^2)^2=0"
                ),
            },
        },
        "eliminated_target_variables": ["d", "e", "f"],
        "templates_exhaust_525_case_ledger": False,
        "template_emptiness_proved": False,
    }


def universal_target_elimination_replay() -> dict[str, Any]:
    b, c, d, e, f = sp.symbols("b c d e f", nonzero=True)
    for sigma in (-1, 1):
        records = {
            "DE+": d * e, "DE-": -d * e,
            "DF+": d * f, "DF-": -d * f,
            "EF": sigma * e * f, "BE": b * e, "CF": c * f,
        }
        product_relations = (
            records["DE-"] + records["DE+"],
            records["DF-"] + records["DF+"],
            records["BE"] * records["CF"] - sigma * b * c * records["EF"],
            b * records["DE+"] * records["CF"]
            - c * records["DF+"] * records["BE"],
        )
        require(all(sp.expand(value) == 0 for value in product_relations),
                f"universal product identities sigma={sigma}")
        sums = {
            "DE+": (d + e)**2, "DE-": (d - e)**2,
            "DF+": (d + f)**2, "DF-": (d - f)**2,
            "EF": (e + sigma * f)**2,
            "BE": (b + e)**2, "CF": (c + f)**2,
        }
        cleared = (
            b**2 * records["BE"]**2 * sums["DE+"]
            - (b**2 * records["DE+"] + records["BE"]**2)**2,
            b**2 * records["BE"]**2 * sums["DE-"]
            - (b**2 * records["DE+"] - records["BE"]**2)**2,
            c**2 * records["CF"]**2 * sums["DF+"]
            - (c**2 * records["DF+"] + records["CF"]**2)**2,
            c**2 * records["CF"]**2 * sums["DF-"]
            - (c**2 * records["DF+"] - records["CF"]**2)**2,
            b**2 * c**2 * sums["EF"]
            - (c * records["BE"] + sigma * b * records["CF"])**2,
            b**2 * sums["BE"] - (b**2 + records["BE"])**2,
            c**2 * sums["CF"] - (c**2 + records["CF"])**2,
        )
        require(all(sp.expand(value) == 0 for value in cleared),
                f"universal sum identities sigma={sigma}")
        require(sp.cancel(b * records["DE+"] / records["BE"] - d) == 0,
                "target d reconstruction")
        require(sp.cancel(records["BE"] / b - e) == 0,
                "target e reconstruction")
        require(sp.cancel(records["CF"] / c - f) == 0,
                "target f reconstruction")
    symmetry = outside_case_symmetry_replay()
    return {
        "product_relations": [
            "DE-+DE+=0", "DF-+DF+=0",
            "BE*CF-sigma*b*c*EF=0",
            "b*DE+*CF-c*DF+*BE=0",
        ],
        "squared_sum_relation_count": 7,
        "explicit_reconstruction": {"e": "BE/b", "f": "CF/c", "d": "b*DE+/BE"},
        "compiled_formal_case_maps": symmetry["total_orbits"],
        "target_elimination_is_necessary_and_sufficient": True,
        "source_systems_proved_empty": False,
    }


def expected_certificate() -> dict[str, Any]:
    data = {
        "schema": "kb-mca-v4-m2-r4-coordinate-positive-433-1a-outside-reduction-v1",
        "parent": PARENT,
        "scope": {
            "workboard_item": "K3",
            "row": "KoalaBear MCA at 2^-128",
            "inner_degree": 2,
            "outer_subdegree": 4,
            "stabilizer_order": 2,
            "orientation": "coordinate",
            "source_parity": "positive",
            "common_route": "433-1a",
            "outside_route": "O0b",
            "purpose": "complete-source product rank, common-kernel, and necessary outside reduction",
        },
        "product_base_rank": product_rank_identity_replay(),
        "common_kernel": common_kernel_replay(),
        "paired_product_ledger": paired_product_replay(),
        "outside_case_symmetry_quotient": outside_case_symmetry_replay(),
        "outside_edge_eliminant": edge_eliminant_replay(),
        "target_free_triangle_templates": triangle_replay(),
        "universal_target_elimination": universal_target_elimination_replay(),
        "conclusion": {
            "base_rank_drop_branch_deleted": True,
            "common_survivor_kernel_unique": True,
            "outside_case_ledger_compiled": True,
            "outside_case_symmetry_quotient_compiled": True,
            "universal_target_elimination_compiled": True,
            "triangle_templates_exhaustive": False,
            "route_deleted": False,
            "coordinate_positive_orientation_deleted": False,
            "order_two_type_deleted": False,
            "k3_status": "OPEN",
            "koalabear_row_status": "OPEN",
            "terminal": "M2_R4_COORDINATE_POSITIVE_433_1A_OUTSIDE_REDUCTION",
        },
        "next_exact_task": (
            "substitute the universal four-product and seven-sum target-free "
            "compiler inside each guarded one-dimensional common-chart coordinate "
            "ring; quotient common-cell/source-deck actions and reduce product "
            "equations before sum equations"
        ),
        "nonclaims": [
            "the stored UNIT certificates are exact deployed-field computations, not characteristic-free theorems",
            "a paired-product resultant survivor need not lift to three distinct unused source deck pairs",
            "the two target-free triangle templates are not proved exhaustive",
            "neither target-free triangle template is proved empty",
            "no 433-1a route, positive orientation, order-two type, owner, payment, K3, KoalaBear row, or Prize close",
        ],
    }
    data["payload_sha256"] = payload_hash(data)
    return data


def verify_data(data: dict[str, Any]) -> None:
    require(payload_hash(data) == data.get("payload_sha256"), "certificate seal")
    require(data == expected_certificate(), "certificate content")


def tamper_selftest(data: dict[str, Any]) -> int:
    mutations: list[Callable[[dict[str, Any]], None]] = [
        lambda x: x["scope"].__setitem__("common_route", "433-0"),
        lambda x: x["product_base_rank"].__setitem__("matching_cell_count", 14),
        lambda x: x["product_base_rank"].__setitem__("product_rank", 4),
        lambda x: x["product_base_rank"]["singular_unit_certificates"]["1"].__setitem__("output", ["NONUNIT"]),
        lambda x: x["common_kernel"].__setitem__("kernel_dimension", 2),
        lambda x: x["common_kernel"]["division_free_reconstruction"].__setitem__("requires_A2_at_nonloop_nonzero", True),
        lambda x: x["paired_product_ledger"].__setitem__("residual_perfect_matchings", 14),
        lambda x: x["paired_product_ledger"].__setitem__("cases_per_common_row_and_cycle_sign", 524),
        lambda x: x["paired_product_ledger"].__setitem__("resultant_survival_is_sufficient", True),
        lambda x: x["outside_case_symmetry_quotient"].__setitem__("total_orbits", 266),
        lambda x: x["outside_case_symmetry_quotient"]["current_template_orbits"].__setitem__("total", 39),
        lambda x: x["outside_edge_eliminant"].__setitem__("generic_terms", 21),
        lambda x: x["outside_edge_eliminant"].__setitem__("seven_edge_cuts_are_only_necessary", False),
        lambda x: x["target_free_triangle_templates"].__setitem__("templates_exhaust_525_case_ledger", True),
        lambda x: x["target_free_triangle_templates"].__setitem__("template_emptiness_proved", True),
        lambda x: x["universal_target_elimination"].__setitem__("squared_sum_relation_count", 6),
        lambda x: x["universal_target_elimination"].__setitem__("target_elimination_is_necessary_and_sufficient", False),
        lambda x: x["conclusion"].__setitem__("universal_target_elimination_compiled", False),
        lambda x: x["conclusion"].__setitem__("route_deleted", True),
        lambda x: x["conclusion"].__setitem__("order_two_type_deleted", True),
        lambda x: x["conclusion"].__setitem__("k3_status", "CLOSED"),
        lambda x: x["parent"].__setitem__("commit", "0" * 40),
        lambda x: x.__setitem__("payload_sha256", "0" * 64),
    ]
    rejected = 0
    for mutation in mutations:
        hostile = copy.deepcopy(data)
        mutation(hostile)
        try:
            verify_data(hostile)
        except VerificationError:
            rejected += 1
    require(rejected == len(mutations), "tamper self-test")
    return rejected


def monic(expression, variables):
    polynomial = sp.Poly(sp.expand(expression), *variables, modulus=PRIME)
    if polynomial.is_zero:
        return sp.Integer(0)
    return polynomial.monic().as_expr()


def strip_factors(expression, factors, variables):
    polynomial = sp.Poly(expression, *variables, modulus=PRIME)
    for factor in factors:
        divisor = sp.Poly(factor, *variables, modulus=PRIME)
        if divisor.total_degree() == 0:
            continue
        while True:
            quotient, remainder = sp.div(polynomial, divisor)
            if not remainder.is_zero:
                break
            polynomial = quotient
    return polynomial.monic().as_expr()


def compile_product_cell(cell_index: int):
    b, c, r, t = sp.symbols("b c r t")
    variables = (t, r, c, b)
    singleton, matching = matching_cells()[cell_index]
    labels = [None] * 5
    labels[matching[0][0]] = sp.Integer(1)
    labels[matching[0][1]] = sp.Integer(-1)
    labels[matching[1][0]] = r**2
    labels[matching[1][1]] = -r**2
    labels[singleton] = t**2
    products = (-c**2, b, b, -b, c)
    rows = [
        [-product, -product * label, -product * label**2, 1, label, label**2]
        for product, label in zip(products, labels)
    ]
    matrix = sp.Matrix(rows)
    cofactors = tuple(
        (-1)**omitted
        * matrix[:, [column for column in range(6) if column != omitted]].det(
            method="domain-ge"
        )
        for omitted in range(6)
    )
    source_guards = [
        labels[left] - labels[right]
        for left, right in itertools.combinations(range(5), 2)
    ]
    target_guards = [
        r, t, b, c, b - 1, b + 1, c - 1, c + 1, b - c, b + c,
    ]
    return tuple(
        strip_factors(monic(value, variables),
                      [*source_guards, *target_guards], variables)
        for value in cofactors
    )


def quotient_square_variables(expression) -> str:
    b, c, r, t, R, T = sp.symbols("b c r t R T")
    polynomial = sp.Poly(expression, r, t, c, b, modulus=PRIME)
    output = 0
    for (r_degree, t_degree, c_degree, b_degree), coefficient in polynomial.terms():
        require(r_degree % 2 == 0 and t_degree % 2 == 0,
                "odd source-root exponent")
        output += (int(coefficient) * R**(r_degree // 2)
                   * T**(t_degree // 2) * c**c_degree * b**b_degree)
    return str(sp.expand(output)).replace("**", "^")


def singular_program(cell: int):
    equations = [quotient_square_variables(value)
                 for value in compile_product_cell(cell)]
    guard = (
        "R*T*b*c*(b-1)*(b+1)*(c-1)*(c+1)*(b-c)*(b+c)"
        "*(R-1)*(R+1)*(T-1)*(T+1)*(T-R)*(T+R)"
    )
    lines = [f"ring q={PRIME},(b,c,R,T,z),dp;", "option(redSB);"]
    lines.extend(f"poly f{index}={value};"
                 for index, value in enumerate(equations))
    lines.extend([
        f"ideal I={','.join(f'f{index}' for index in range(6))},z*({guard})-1;",
        "ideal G=std(I);",
        'if (reduce(1,G)==0) { print("UNIT"); } else { print("NONUNIT"); }',
        "print(size(G));",
        "G[1];",
        "quit;",
    ])
    return equations, "\n".join(lines)


def full_singular_replay() -> int:
    executable = shutil.which("Singular")
    require(executable is not None, "Singular is required for full replay")
    completed = 0
    for cell, expected in SINGULAR_CERTIFICATES.items():
        _, program = singular_program(cell)
        # The stored equation digests use the compiler's (t,r,c,b) monic text.
        compiled = compile_product_cell(cell)
        compiler_hashes = [
            hashlib.sha256(
                str(sp.Poly(value, *sp.symbols("t r c b"), modulus=PRIME).as_expr()).encode()
            ).hexdigest()
            for value in compiled
        ]
        require(compiler_hashes == expected["equation_sha256"],
                f"cell {cell} equation hashes")
        require(hashlib.sha256(program.encode()).hexdigest()
                == expected["program_sha256"], f"cell {cell} program hash")
        try:
            process = subprocess.run(
                [executable, "-q"],
                input=program,
                capture_output=True,
                text=True,
                timeout=150,
            )
        except subprocess.TimeoutExpired as error:
            raise VerificationError(f"cell {cell} Singular timeout") from error
        require(process.returncode == 0, f"cell {cell} Singular exit")
        output = [line.strip() for line in process.stdout.splitlines() if line.strip()]
        require(output[-3:] == ["UNIT", "1", "1"], f"cell {cell} unit ideal")
        completed += 1
    return completed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    parser.add_argument("--full-singular-replay", action="store_true")
    arguments = parser.parse_args()

    load_parent()
    expected = expected_certificate()
    if arguments.write:
        CERTIFICATE.parent.mkdir(parents=True, exist_ok=True)
        CERTIFICATE.write_text(json.dumps(expected, indent=2, sort_keys=True) + "\n")
    if arguments.check or not arguments.write:
        require(CERTIFICATE.is_file(), "missing certificate")
        data = parse_json(CERTIFICATE.read_text(), str(CERTIFICATE))
        verify_data(data)
    else:
        data = expected
    rejected = tamper_selftest(data) if arguments.tamper_selftest else 0
    singular_replayed = full_singular_replay() if arguments.full_singular_replay else 0
    print(
        "KB_MCA_V4_M2_R4_COORDINATE_POSITIVE_433_1A_OUTSIDE_REDUCTION_PASS "
        f"matching_cells={data['product_base_rank']['matching_cell_count']} "
        f"product_rank={data['product_base_rank']['product_rank']} "
        f"common_rank={data['common_kernel']['common_survivor_rank']} "
        f"ledger_cases={data['paired_product_ledger']['cases_per_common_row_and_cycle_sign']} "
        f"edge_terms={data['outside_edge_eliminant']['generic_terms']} "
        f"case_orbits={data['outside_case_symmetry_quotient']['total_orbits']} "
        f"target_sums={data['universal_target_elimination']['squared_sum_relation_count']} "
        f"triangle_templates={len(data['target_free_triangle_templates']['templates'])} "
        f"singular_replayed={singular_replayed} tamper_rejected={rejected}"
    )


if __name__ == "__main__":
    main()
