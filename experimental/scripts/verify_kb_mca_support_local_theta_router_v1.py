#!/usr/bin/env python3
"""Verify the post-#1165 support-local theta refinement and route cut."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
from collections import Counter
from fractions import Fraction
from math import prod
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / (
    "experimental/data/certificates/"
    "kb-mca-support-local-theta-router-v1/manifest.json"
)
PARENT_HEAD = "d4d653723f2f82390fd4351476e1926e55fb0caf"
UPSTREAM_MAIN = "93fba1be3f3299b0ba4708d88715377bbb656e45"

PACKET_FILES = [
    "agents.md",
    "experimental/agents-log.md",
    "experimental/grande_finale.tex",
    "experimental/notes/thresholds/kb_mca_support_local_theta_and_error_rank_router_v1.md",
    "experimental/data/certificates/kb-mca-support-local-theta-router-v1/README.md",
    "experimental/scripts/verify_kb_mca_support_local_theta_router_v1.py",
    "experimental/scripts/verify_kb_mca_support_local_theta_router_v1.sage",
    "experimental/scripts/verify_kb_mca_support_local_theta_router_v1_flint.py",
    "experimental/scripts/verify_kb_mca_support_local_theta_router_v1.wl",
    "experimental/campaigns/kb-mca-support-local-theta-post-1165/campaign.json",
    "experimental/campaigns/kb-mca-support-local-theta-post-1165/00_contract.md",
    "experimental/campaigns/kb-mca-support-local-theta-post-1165/01_frontier_map.md",
    "experimental/campaigns/kb-mca-support-local-theta-post-1165/02_controls.md",
    "experimental/campaigns/kb-mca-support-local-theta-post-1165/03_idea_ledger.csv",
    "experimental/campaigns/kb-mca-support-local-theta-post-1165/04_dependency_ledger.csv",
    "experimental/campaigns/kb-mca-support-local-theta-post-1165/05_claim_registry.csv",
    "experimental/campaigns/kb-mca-support-local-theta-post-1165/06_review_registry.csv",
    "experimental/campaigns/kb-mca-support-local-theta-post-1165/reviews/literature_sweep.md",
    "experimental/campaigns/kb-mca-support-local-theta-post-1165/reviews/final_source_math_review.md",
]


class Reject(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise Reject(message)


def strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in out, f"duplicate JSON key: {key}")
        out[key] = value
    return out


def strict_load(path: Path) -> Any:
    return json.loads(
        path.read_text(),
        object_pairs_hook=strict_pairs,
        parse_float=lambda value: (_ for _ in ()).throw(Reject(f"float {value}")),
        parse_constant=lambda value: (_ for _ in ()).throw(Reject(f"constant {value}")),
    )


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def payload_hash(value: dict[str, Any]) -> str:
    unsigned = copy.deepcopy(value)
    unsigned.pop("payload_sha256", None)
    return sha256(canonical_bytes(unsigned))


def git_blob(data: bytes) -> str:
    return hashlib.sha1(
        b"blob " + str(len(data)).encode() + b"\0" + data
    ).hexdigest()


def falling(value: int, length: int) -> int:
    return prod(value - index for index in range(length))


def rising(value: int, length: int) -> int:
    return prod(value + index for index in range(length))


def rank_mod(rows: list[list[int]], modulus: int) -> int:
    matrix = [[entry % modulus for entry in row] for row in rows]
    rank = 0
    width = len(matrix[0]) if matrix else 0
    for column in range(width):
        pivot = next(
            (index for index in range(rank, len(matrix))
             if matrix[index][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inverse = pow(matrix[rank][column], -1, modulus)
        matrix[rank] = [(inverse * entry) % modulus
                        for entry in matrix[rank]]
        for index in range(len(matrix)):
            if index == rank or matrix[index][column] == 0:
                continue
            factor = matrix[index][column]
            matrix[index] = [
                (left - factor * right) % modulus
                for left, right in zip(matrix[index], matrix[rank])
            ]
        rank += 1
    return rank


def local_bound(
    n: int, K: int, m: int, rank: int, theta: int, g: int, c: int
) -> Fraction:
    w = m - K
    require(n >= m == K + w and w >= 0, "legal row")
    require(1 <= rank <= K, "legal affine rank")
    require(1 <= theta <= w + 1, "capped positive theta")
    require(g >= 0 and c >= 0 and g + c <= K - rank, "legal zero profile")
    return Fraction(
        falling(n - g - c, rank + 1),
        (m - g) * theta * rising(w + 1 + c, rank - 1),
    )


def closed_bound(n: int, K: int, m: int, rank: int, theta: int = 1) -> Fraction:
    w = m - K
    require(n >= m == K + w and w >= 0, "legal row")
    require(1 <= rank <= K, "legal affine rank")
    require(1 <= theta <= w + 1, "capped positive theta")
    first = Fraction(
        falling(n, rank + 1),
        m * theta * rising(w + 1, rank - 1),
    )
    second = Fraction(
        falling(n - K + rank, rank + 1),
        theta * rising(w + 1, rank),
    )
    return max(first, second)


def floor_fraction(value: Fraction) -> int:
    return value.numerator // value.denominator


def minimum_margin(
    n: int, K: int, m: int, rank: int, available_budget: int
) -> int:
    raw = closed_bound(n, K, m, rank, 1)
    # floor(raw / theta) <= B iff raw / theta < B + 1.
    theta = max(
        1,
        raw.numerator // (raw.denominator * (available_budget + 1)) + 1,
    )
    while theta <= m - K + 1 and floor_fraction(
        closed_bound(n, K, m, rank, theta)
    ) > available_budget:
        theta += 1
    return theta


def endpoint_controls() -> int:
    checks = 0
    for n in range(7, 25):
        for K in range(2, n - 1):
            for rank in range(1, min(5, K)):
                for w in range(1, min(6, n - K)):
                    m = K + w
                    if m > n:
                        continue
                    for theta in range(1, min(w + 2, 5)):
                        brute = max(
                            local_bound(n, K, m, rank, theta, g, c)
                            for c in range(K - rank + 1)
                            for g in range(K - rank - c + 1)
                        )
                        require(
                            brute == closed_bound(n, K, m, rank, theta),
                            "endpoint optimization",
                        )
                        checks += 1
    require(checks == 10716, "endpoint control count")
    return checks


def counterexample() -> dict[str, Any]:
    p, n, K, m = 257, 256, 1, 86
    w = m - K
    points = [(gamma, 0) for gamma in range(m)] + [(m, 1)]
    hyperplanes: list[tuple[int, int, str]] = [
        (0, 0, "common") for _ in range(w)
    ]
    connector_b: set[int] = set()
    for gamma in range(m):
        b = pow(m - gamma, -1, p)
        a = (-gamma * b) % p
        connector_b.add(b)
        hyperplanes.append((a, b, f"connector-{gamma}"))
    available_b = [value for value in range(1, p) if value not in connector_b]
    for index, b in enumerate(available_b[:w]):
        forbidden_a = {(lam - gamma * b) % p for gamma, lam in points}
        a = next(value for value in range(p) if value not in forbidden_a)
        hyperplanes.append((a, b, f"unused-{index}"))
    require(len(hyperplanes) == n, "coordinate count")
    require(
        len({b for _, b, role in hyperplanes if role != "common"}) == m + w,
        "distinct noncommon directions",
    )

    r0 = [a for a, _, _ in hyperplanes]
    r1 = [b for _, b, _ in hyperplanes]
    supports: list[list[int]] = []
    errors: list[list[int]] = []
    normal_ranks: list[int] = []
    near_distances: list[int] = []
    for gamma, lam in points:
        support = [
            index for index, (a, b, _) in enumerate(hyperplanes)
            if (a + gamma * b - lam) % p == 0
        ]
        require(len(support) == m, "exact support")
        require(
            len({r0[index] for index in support}) > 1
            or len({r1[index] for index in support}) > 1,
            "same-support pair noncontainment",
        )
        normal_ranks.append(rank_mod([[r1[index], -1] for index in support], p))
        supports.append(support)
        error = [
            (r0[index] + gamma * r1[index] - lam) % p
            for index in range(n)
        ]
        errors.append(error)
        word = [(r0[index] + gamma * r1[index]) % p for index in range(n)]
        near_distances.append(n - max(Counter(word).values()))

    require(set(normal_ranks) == {2}, "full incident normal rank")
    require(not set.intersection(*(set(support) for support in supports)),
            "empty global core")
    direction_max = max(Counter(r1).values())
    require(direction_max == w < m, "global direction separation")
    require(min(near_distances) == 170 > w, "outside near radius")
    error_rank = rank_mod([
        [(left - right) % p for left, right in zip(error, errors[0])]
        for error in errors[1:]
    ], p)
    require(error_rank == 2, "error rank")

    old_cap = max(
        falling(n, 2) // (m * w),
        falling(n - K + 1, 2) // (w * (w + 1)),
    )
    repaired_cap = floor_fraction(closed_bound(n, K, m, 1, 1))
    require(old_cap == 8 < len(points) == 87 <= repaired_cap == 759,
            "counterexample and repair")

    fixture = {
        "points": points,
        "hyperplanes": hyperplanes,
        "supports": supports,
    }
    return {
        "field": p,
        "domain": "GF(257)^*",
        "n": n,
        "K": K,
        "m": m,
        "w": w,
        "slopes": len(points),
        "support_sizes": sorted(set(map(len, supports))),
        "incident_normal_ranks": sorted(set(normal_ranks)),
        "explanation_affine_rank": 1,
        "error_affine_rank": error_rank,
        "global_core_size": 0,
        "direction_max_agreement": direction_max,
        "minimum_near_distance": min(near_distances),
        "old_printed_cap": old_cap,
        "repaired_theta1_cap": repaired_cap,
        "fixture_sha256": sha256(canonical_bytes(fixture)),
    }


def row_tables() -> dict[str, Any]:
    kb = {
        "n": 2097152,
        "K": 1048576,
        "m": 1116048,
        "w": 67472,
        "budget": 274980728111395087,
    }
    kb_caps = [
        floor_fraction(closed_bound(kb["n"], kb["K"], kb["m"], rank, 1))
        for rank in range(1, 10)
    ]
    require(kb_caps == [
        16295594,
        253241283,
        3935435218,
        118319201475,
        3677348367069,
        114289853114503,
        3552007973114420,
        110390969172173096,
        3430729820133944932,
    ], "Koala theta-one caps")
    near = 2 * kb["w"]
    available = kb["budget"] - near
    transitions = []
    for rank in (8, 9, 10, 11):
        theta = minimum_margin(kb["n"], kb["K"], kb["m"], rank, available)
        cap = floor_fraction(closed_bound(
            kb["n"], kb["K"], kb["m"], rank, theta
        ))
        previous_total = None
        if theta > 1:
            previous_total = floor_fraction(closed_bound(
                kb["n"], kb["K"], kb["m"], rank, theta - 1
            )) + near
            require(previous_total > kb["budget"], "minimal Koala theta")
        transitions.append({
            "explanation_rank": rank,
            "minimum_theta": theta,
            "exception_ceiling_if_unpaid": theta - 1,
            "cap": cap,
            "cap_plus_2w": cap + near,
            "slack": kb["budget"] - cap - near,
            "previous_total": previous_total,
        })
    require([item["minimum_theta"] for item in transitions]
            == [1, 13, 388, 12050], "Koala theta thresholds")

    m31 = {
        "n": 2097152,
        "K": 1048576,
        "m": 1116024,
        "w": 67448,
        "budget": 16777215,
    }
    m31_available = m31["budget"] - 2 * m31["w"]
    m31_transitions = []
    for rank in range(1, 5):
        theta = minimum_margin(
            m31["n"], m31["K"], m31["m"], rank, m31_available
        )
        cap = floor_fraction(closed_bound(
            m31["n"], m31["K"], m31["m"], rank, theta
        ))
        m31_transitions.append({
            "explanation_rank": rank,
            "minimum_theta": theta,
            "cap": cap,
            "cap_plus_2w": cap + 2 * m31["w"],
            "slack": m31["budget"] - cap - 2 * m31["w"],
        })
        if theta > 1:
            require(
                floor_fraction(closed_bound(
                    m31["n"], m31["K"], m31["m"], rank, theta - 1
                )) + 2 * m31["w"] > m31["budget"],
                "minimal M31 theta",
            )
    require([item["minimum_theta"] for item in m31_transitions]
            == [1, 16, 237, 7118], "M31 theta thresholds")

    R, d = 1048576, 67472
    shortened = []
    for rank in range(1, 15):
        n = R + rank
        K = rank
        m = d + rank
        cap = floor_fraction(closed_bound(n, K, m, rank, 1))
        theta = minimum_margin(n, K, m, rank, kb["budget"])
        shortened.append({
            "rank": rank,
            "theta1_cap": cap,
            "minimum_theta": theta,
            "theta_is_feasible": theta <= d + 1,
        })
        if 1 < theta <= d + 1:
            require(
                floor_fraction(closed_bound(
                    n, K, m, rank, theta - 1
                )) > kb["budget"],
                "minimal shortened theta",
            )
    require(shortened[8]["theta1_cap"] == 55413538236037195,
            "shortened rank-nine cap")
    require(shortened[9]["theta1_cap"] == 861057176799343503,
            "shortened rank-ten cap")
    require([shortened[index - 1]["minimum_theta"]
             for index in (10, 11, 12, 13, 14)]
            == [4, 49, 757, 11748, 182530], "shortened thresholds")
    require(shortened[13]["theta_is_feasible"] is False,
            "shortened rank fourteen cannot pay by theta")

    return {
        "KoalaBear": {
            **kb,
            "near_charge_2w": near,
            "theta1_caps_s1_through_s9": kb_caps,
            "transitions_s8_through_s11": transitions,
            "paid_error_rank_at_most": 9,
            "paid_total": 110390969172308040,
            "paid_slack": 164589758939087047,
            "error_rank_10_11_12_exception_ceilings": [12, 387, 12049],
        },
        "Mersenne31_stress_control": {
            **m31,
            "transitions_s1_through_s4": m31_transitions,
        },
        "shortened_complete_code": {
            "R": R,
            "d": d,
            "rows_s1_through_s14": shortened,
            "automatic_theta_paid_through_rank": 9,
            "rank_10_11_12_13_exception_ceilings": [3, 48, 756, 11747],
            "first_unpaid_even_at_maximum_theta": 14,
        },
    }


def source_binding(identifier: str, path: str, blob: str, digest: str,
                   role: str) -> dict[str, str]:
    return {
        "id": identifier,
        "path": path,
        "git_blob_sha1": blob,
        "sha256": digest,
        "role": role,
    }


def external_source_binding(
    identifier: str,
    commit: str,
    path: str,
    blob: str,
    digest: str,
    role: str,
) -> dict[str, str]:
    binding = source_binding(identifier, path, blob, digest, role)
    binding["commit"] = commit
    return binding


def build_manifest() -> dict[str, Any]:
    tables = row_tables()
    manifest: dict[str, Any] = {
        "schema": "rs-mca-kb-support-local-theta-router-v1",
        "artifact_kind": "POST_1165_SUPPORT_LOCAL_REFINEMENT_GAUGE_AND_ROUTE_CUT",
        "base": {
            "repository": "przchojecki/rs-mca",
            "exact_pr1165_head": PARENT_HEAD,
            "official_upstream_main_at_refresh": UPSTREAM_MAIN,
        },
        "source_bindings_at_parent": [
            source_binding(
                "ACTIVE_V4_AFTER_PR1165_REPAIR",
                "experimental/grande_finale.tex",
                "60bd5ca5c4e61791bccb89b87e9d7f01ee7b1b45",
                "9f77f20bd0eaf87555f9344a545d4117d68710fadb2b3fb4d8407921c1e2ff65",
                "GLOBAL_REPAIR_FULL_RANK_SPLIT_PUNCTURED_AND_GRAM_PROFILES",
            ),
            source_binding(
                "PR1165_COUNTEREXAMPLE_NOTE",
                "experimental/notes/thresholds/mca_affine_span_incidence_counterexample_v1.md",
                "984fe1fa4ff4ff34ed8a78499937243169ef9ffe",
                "83446a16a91f401ee76bbd89da888fa98638272eadfcc784cc3b1c7e94419883",
                "PARENT_COUNTEREXAMPLE_GLOBAL_REPAIR_AND_TOP_RANK_SCOPE",
            ),
            source_binding(
                "PR1165_GLOBAL_REPAIR_VERIFIER",
                "experimental/verify_mca_proper_subspace_occupancy_compiler_v1.py",
                "ee46de85140dc3e79a120f28fe447475d3303844",
                "9e319700ddfe6378a9cadbc902723db2a56726d26e34aa84dda3dfb5f8046f96",
                "PARENT_GLOBAL_L_FACTOR_AND_WALLS",
            ),
            source_binding(
                "PR1165_COUNTEREXAMPLE_VERIFIER",
                "experimental/verify_mca_affine_span_incidence_counterexample_v1.py",
                "3355975c6661551e78611083ebce343d3c540fda",
                "26c07a19f94007cca71cfcfabf1a4e053e27abfd3196c33f805971f2ecde939b",
                "PARENT_GF1009_REGRESSION",
            ),
            source_binding(
                "PR1165_INDEPENDENT_COUNTEREXAMPLE_VERIFIER",
                "experimental/verify_mca_affine_span_incidence_counterexample_v1_independent.py",
                "a447210884b2d3b9f7707f0af7913f7e9654c718",
                "bf48d7d533863b7b953e8080e5cd82f5159be4a3453e0d2391afc8f5437fff15",
                "PARENT_INDEPENDENT_GF1009_REPLAY",
            ),
            source_binding(
                "PR1165_FULL_RANK_GAUGE_VERIFIER",
                "experimental/verify_mca_full_explanation_lifted_rank_gauge_dichotomy_v1.py",
                "1ebd91022c7231354e5684be0dd0c61edd8d156e",
                "92abd35176f143a1fa9fb09b5a8b6641715d425300011f1031547286d359f567",
                "PARENT_FULL_EXPLANATION_GAUGE_OVERLAP_BOUNDARY",
            ),
            source_binding(
                "PR1165_PUNCTURED_JOHNSON_VERIFIER",
                "experimental/verify_mca_sparse_direction_punctured_johnson_profile_v1.py",
                "806738813012ff4aeda97db6b0c02473f4d0ea45",
                "b4fee5a75fcc716dee3c8ce02e129ad51e15bd537dc7404451d0bb58faf07c86",
                "PARENT_SPARSE_DIRECTION_ROUTE_OVERLAP_BOUNDARY",
            ),
            source_binding(
                "PR1165_NEAR_JOHNSON_GRAM_NOTE",
                "experimental/notes/thresholds/mca_sparse_direction_near_johnson_gram_rank_v1.md",
                "d303cb19770a258c1c8f2dfc0cd53401658b3ea1",
                "e155d107a5dc31c6de9ad8fbb3395cee70937467fb798633c50e0e34e94272b6",
                "PARENT_CENTERED_GRAM_CONTINUATION_SCOPE",
            ),
            source_binding(
                "PR1165_NEAR_JOHNSON_GRAM_VERIFIER",
                "experimental/verify_mca_sparse_direction_near_johnson_gram_rank_v1.py",
                "0e013330a0cba9aa985b73a856bcbae6dcc0673b",
                "5dd10235bb005ddfaeb0481952fae344886261bf5b62be66d8aa588bfe4cb4b6",
                "PARENT_CENTERED_GRAM_EXACT_WALLS",
            ),
            source_binding(
                "PR1165_MEAN_CENTERED_GRAM_NOTE",
                "experimental/notes/thresholds/mca_sparse_direction_mean_centered_gram_profile_v1.md",
                "aebf91a811eaeace0266a1a051219b240e0ec40f",
                "f8d7bbbfcf2cd20a72e30d6e06cdac1489204369d62b485ab6ea11685f7d8d94",
                "PARENT_MEAN_CENTERED_GRAM_CONTINUATION_SCOPE",
            ),
            source_binding(
                "PR1165_MEAN_CENTERED_GRAM_VERIFIER",
                "experimental/verify_mca_sparse_direction_mean_centered_gram_profile_v1.py",
                "5e55d792a38d7285979df7b2f867c3d6cbd46a1f",
                "f9b8ef1b5b3f4a64876f5eb19f7cf535c4780086f0d97e1bf9af96c29aa6c152",
                "PARENT_MEAN_CENTERED_GRAM_EXACT_WALLS",
            ),
        ],
        "external_source_bindings": [
            external_source_binding(
                "PR1160_NEAR_RATIONAL_2W_THEOREM",
                "c5f4ea7a0c78828c901ae5f3428894a8b2e2806b",
                "experimental/notes/thresholds/kb_mca_supportwise_near_rational_two_anchor_repair_v1.md",
                "12bc4a0f06189829a9490928e4855d1aa958f940",
                "7e75d67420f4ed37add3b4f6ea3aa45e043a782a6396f328b1e34ce659938989",
                "INTRINSIC_NEAR_RATIONAL_STRATUM_BOUND_LE_2W",
            ),
            external_source_binding(
                "PR1160_NEAR_RATIONAL_2W_VERIFIER",
                "c5f4ea7a0c78828c901ae5f3428894a8b2e2806b",
                "experimental/scripts/verify_kb_mca_supportwise_near_rational_two_anchor_repair_v1.py",
                "3b4533b53e947466de55262e3577108f125738c0",
                "5d284cb0f857f2ff7c0797e911a2047009d6883d54f9d0df0a682627c09b5a35",
                "INTRINSIC_NEAR_RATIONAL_STRATUM_EXACT_REPLAY",
            ),
        ],
        "external_provenance": [
            {
                "commit": "3a13f2dcdcab95f57fdda8a3a8beea024b0dd1de",
                "repository": "AllenGrahamHart/rs-mca-prize-dag",
                "status": "REFUTED_AT_FINAL_NORMAL_FLAT_STEP",
            },
            {
                "commit": "60db12dc5e741e24acaca032382bbbfa721ce499",
                "repository": "AllenGrahamHart/rs-mca-prize-dag",
                "status": "RANK_WALL_CONSEQUENCE_SUPERSEDED",
            },
            {
                "commit": "fc74e16cd3f3acfa1030317e8d1636f492aca11f",
                "repository": "AllenGrahamHart/rs-mca-prize-dag",
                "status": "COMPOSITION_REQUIRES_REAUDIT_WHERE_IT_USES_3A13",
            },
            {
                "commit": "c5f4ea7a0c78828c901ae5f3428894a8b2e2806b",
                "repository": "przchojecki/rs-mca",
                "status": "PR1160_EXTERNAL_2W_DELETION_DEPENDENCY_NOT_IN_PARENT",
            },
            {
                "search": "Exa targeted primary-source incidence/design-matrix sweep",
                "sources_reviewed": 24,
                "load_bearing_external_lemma_imported": False,
            },
        ],
        "counterexample": counterexample(),
        "support_local_refinement": {
            "name": "SUPPORT_LOCAL_REFINEMENT_OF_PROPER_SUBSPACE_COMPILER",
            "theta_definition": "MIN(w+1,MIN_{gamma,b_in_Cprime}|{x_in_Sgamma:r1(x)!=b(x)}|)",
            "theta_codeword_space": "DIRECTION_SPACE_CPRIME_NOT_AFFINE_TRANSLATE",
            "bound": "FLOOR_MAX(n_(s+1)/(m*theta*(w+1)^(rise s-1)),(n-K+s)_(s+1)/(theta*(w+1)^(rise s)))",
            "empty_rising_product_at_s1": 1,
            "endpoint_profile_checks": endpoint_controls(),
            "relation_to_pr1165_global_factor": "THETA_GE_L",
            "theta_recomputed_after_gauge": True,
            "independent_math_review": "GREEN_FINAL_SOURCE_MATH_REVIEW",
        },
        "gauge": {
            "kind": "REVERSIBLE_CODEWORD_TRANSLATION",
            "relation_to_pr1165": "ARBITRARY_RANK_EXTENSION_OF_FULL_EXPLANATION_EXISTENCE_BRANCH",
            "preserves": [
                "SLOPE_SET",
                "ERROR_WORDS",
                "EXACT_AGREEMENT_SUPPORTS",
                "SAME_SUPPORT_PAIR_NONCONTAINMENT",
            ],
            "does_not_preserve_literal_received_line_representative": True,
            "explanation_rank_from_error_rank": "s=a-1_FOR_AT_LEAST_TWO_SLOPES",
            "owner_chronology_recomputed_after_gauge": False,
        },
        "wolfram_replay": {
            "required_stdout_sentinel": "KB_MCA_SUPPORT_LOCAL_THETA_WOLFRAM_PASS",
            "wrapper_exit_status_alone_is_accepted": False,
        },
        "exact_tables": tables,
        "route_cut": {
            "conditional_partition": "Z_BAD=N_DISJOINT_UNION_Z_WITH_|N|_LE_2w",
            "pr1160_supplies_partition_when_integrated": True,
            "exception_reserve_31_used": False,
            "post_deletion_error_rank_at_most_9": "PAID",
            "post_deletion_error_rank_10": "DIRECTION_EXCEPTIONS_LE_12",
            "post_deletion_error_rank_11": "DIRECTION_EXCEPTIONS_LE_387",
            "post_deletion_error_rank_12": "DIRECTION_EXCEPTIONS_LE_12049",
            "post_deletion_error_rank_at_least_13": "UNPAID_HIGH_RANK",
            "active_v4_ledger_movement": 0,
            "KoalaBear_closed": False,
        },
        "nonduplicate_scope": [
            "SUPPORT_LOCAL_THETA_REFINES_PR1165_GLOBAL_L",
            "REVERSIBLE_ERROR_TO_EXPLANATION_RANK_GAUGE",
            "CONDITIONAL_DIRECT_KOALA_ERROR_RANK_NINE_PAYMENT",
            "EXACT_RANK_10_11_12_DIRECTION_EXCEPTION_TERMINALS",
            "GF257_SMOOTH_DOMAIN_INDEPENDENT_REGRESSION",
        ],
        "packet_files": PACKET_FILES,
        "packet_file_sha256": {
            path: sha256((ROOT / path).read_bytes()) for path in PACKET_FILES
        },
    }
    manifest["payload_sha256"] = payload_hash(manifest)
    return manifest


def verify_parent_sources(manifest: dict[str, Any]) -> None:
    for binding in manifest["source_bindings_at_parent"]:
        proc = subprocess.run(
            ["git", "-C", str(ROOT), "show", f"{PARENT_HEAD}:{binding['path']}"],
            capture_output=True,
        )
        require(proc.returncode == 0, f"parent path {binding['id']}")
        require(git_blob(proc.stdout) == binding["git_blob_sha1"],
                f"parent blob {binding['id']}")
        require(sha256(proc.stdout) == binding["sha256"],
                f"parent sha {binding['id']}")
    for binding in manifest["external_source_bindings"]:
        proc = subprocess.run(
            [
                "git", "-C", str(ROOT), "show",
                f"{binding['commit']}:{binding['path']}",
            ],
            capture_output=True,
        )
        require(
            proc.returncode == 0,
            "external path " + binding["id"]
            + "; fetch prerequisite with `git fetch upstream "
              "pull/1160/head:refs/remotes/upstream/pr-1160`",
        )
        require(git_blob(proc.stdout) == binding["git_blob_sha1"],
                f"external blob {binding['id']}")
        require(sha256(proc.stdout) == binding["sha256"],
                f"external sha {binding['id']}")


def verify_manifest(manifest: dict[str, Any], check_hashes: bool = True) -> None:
    expected = build_manifest()
    require(manifest == expected, "canonical manifest")
    require(manifest["payload_sha256"] == payload_hash(manifest), "payload hash")
    verify_parent_sources(manifest)
    require(manifest["counterexample"]["slopes"]
            > manifest["counterexample"]["old_printed_cap"], "old theorem false")
    require(manifest["counterexample"]["slopes"]
            <= manifest["counterexample"]["repaired_theta1_cap"], "repair accepts fixture")
    kb = manifest["exact_tables"]["KoalaBear"]
    require(kb["paid_total"] + kb["paid_slack"] == kb["budget"],
            "Koala paid total")
    require(kb["error_rank_10_11_12_exception_ceilings"]
            == [12, 387, 12049], "exception terminals")
    require(manifest["route_cut"]["exception_reserve_31_used"] is False,
            "no conditional 31 addback")
    require(manifest["route_cut"]["active_v4_ledger_movement"] == 0,
            "zero deployed movement")
    require(manifest["route_cut"]["KoalaBear_closed"] is False,
            "no closure claim")
    wl_text = (ROOT / "experimental/scripts/verify_kb_mca_support_local_theta_router_v1.wl").read_text()
    require(
        manifest["wolfram_replay"]["required_stdout_sentinel"] in wl_text,
        "Wolfram PASS sentinel",
    )
    require(
        manifest["wolfram_replay"]["wrapper_exit_status_alone_is_accepted"] is False,
        "Wolfram replay fail closed",
    )
    if check_hashes:
        for path, digest in manifest["packet_file_sha256"].items():
            require(sha256((ROOT / path).read_bytes()) == digest,
                    f"packet hash {path}")


def set_path(path: tuple[Any, ...], value: Any) -> Callable[[dict[str, Any]], None]:
    def mutate(data: dict[str, Any]) -> None:
        cursor: Any = data
        for key in path[:-1]:
            cursor = cursor[key]
        cursor[path[-1]] = value
    return mutate


def mutations() -> list[Callable[[dict[str, Any]], None]]:
    return [
        set_path(("counterexample", "slopes"), 8),
        set_path(("counterexample", "support_sizes", 0), 85),
        set_path(("counterexample", "incident_normal_ranks", 0), 1),
        set_path(("counterexample", "global_core_size"), 1),
        set_path(("counterexample", "direction_max_agreement"), 86),
        set_path(("counterexample", "minimum_near_distance"), 85),
        set_path(("counterexample", "old_printed_cap"), 87),
        set_path(("counterexample", "repaired_theta1_cap"), 8),
        set_path(("support_local_refinement", "relation_to_pr1165_global_factor"), "UNRELATED"),
        set_path(("support_local_refinement", "theta_codeword_space"), "AFFINE_TRANSLATE"),
        set_path(("support_local_refinement", "endpoint_profile_checks"), 10715),
        set_path(("gauge", "does_not_preserve_literal_received_line_representative"), False),
        set_path(("gauge", "relation_to_pr1165"), "DUPLICATE"),
        set_path(("gauge", "owner_chronology_recomputed_after_gauge"), True),
        set_path(("exact_tables", "KoalaBear", "near_charge_2w"), 134975),
        set_path(("exact_tables", "KoalaBear", "paid_error_rank_at_most"), 12),
        set_path(("exact_tables", "KoalaBear", "paid_total"), 110390969172308039),
        set_path(("exact_tables", "KoalaBear", "paid_slack"), 164589758939087048),
        set_path(("exact_tables", "KoalaBear", "error_rank_10_11_12_exception_ceilings", 0), 13),
        set_path(("exact_tables", "shortened_complete_code", "automatic_theta_paid_through_rank"), 13),
        set_path(("exact_tables", "shortened_complete_code", "first_unpaid_even_at_maximum_theta"), 15),
        set_path(("route_cut", "exception_reserve_31_used"), True),
        set_path(("route_cut", "post_deletion_error_rank_10"), "PAID"),
        set_path(("route_cut", "active_v4_ledger_movement"), 1),
        set_path(("route_cut", "KoalaBear_closed"), True),
        set_path(("base", "exact_pr1165_head"), "0" * 40),
        set_path(("source_bindings_at_parent", 0, "git_blob_sha1"), "0" * 40),
        set_path(("external_source_bindings", 0, "git_blob_sha1"), "0" * 40),
        set_path(("external_provenance", 4, "load_bearing_external_lemma_imported"), True),
        set_path(("wolfram_replay", "required_stdout_sentinel"), "MISSING_PASS_SENTINEL"),
        set_path(("wolfram_replay", "wrapper_exit_status_alone_is_accepted"), True),
    ]


def tamper_selftest(manifest: dict[str, Any]) -> int:
    caught = 0
    for mutation in mutations():
        changed = copy.deepcopy(manifest)
        mutation(changed)
        changed["payload_sha256"] = payload_hash(changed)
        try:
            verify_manifest(changed, check_hashes=False)
        except (Reject, KeyError, TypeError, ValueError):
            caught += 1
    require(caught == len(mutations()), "all semantic mutations rejected")
    duplicate = MANIFEST.read_text().replace(
        '"schema":', '"schema":"duplicate",\n  "schema":', 1
    )
    try:
        json.loads(duplicate, object_pairs_hook=strict_pairs)
    except Reject:
        caught += 1
    require(caught == len(mutations()) + 1, "duplicate key rejected")
    return caught


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()
    if args.write:
        MANIFEST.parent.mkdir(parents=True, exist_ok=True)
        MANIFEST.write_text(json.dumps(build_manifest(), indent=2) + "\n")
        print(f"WROTE {MANIFEST}")
        return
    manifest = strict_load(MANIFEST)
    verify_manifest(manifest)
    if args.tamper_selftest:
        caught = tamper_selftest(manifest)
        print(
            "KB_MCA_SUPPORT_LOCAL_THETA_TAMPER_PASS "
            f"mutations={caught}/{caught} payload_sha256={manifest['payload_sha256']}"
        )
    else:
        counter = manifest["counterexample"]
        kb = manifest["exact_tables"]["KoalaBear"]
        print(
            "KB_MCA_SUPPORT_LOCAL_THETA_PASS "
            f"slopes={counter['slopes']} false_cap={counter['old_printed_cap']} "
            f"repaired_cap={counter['repaired_theta1_cap']} "
            f"endpoint_checks={manifest['support_local_refinement']['endpoint_profile_checks']} "
            f"paid_error_rank_le={kb['paid_error_rank_at_most']} "
            f"paid_total={kb['paid_total']} slack={kb['paid_slack']} "
            f"ledger_movement=0 payload_sha256={manifest['payload_sha256']}"
        )


if __name__ == "__main__":
    main()
