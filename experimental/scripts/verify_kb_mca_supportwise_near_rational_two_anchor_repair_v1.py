#!/usr/bin/env python3
"""Verify the support-wise near-rational two-anchor repair.

The checker binds the original false source statements, the repaired files,
the exact deployed counterexample, the uniform 2w contract, and an exhaustive
syndrome-normalized toy row.  It never converts witness counts to slope counts
or claims Q/BC/K3 ownership.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
import re
import subprocess
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = ROOT / "experimental/data/certificates/kb-mca-supportwise-near-rational-two-anchor-repair-v1/manifest.json"
SCHEMA_PATH = ROOT / "experimental/data/schemas/kb_mca_supportwise_near_rational_two_anchor_repair_v1.schema.json"
BASE_HEAD = "e603e0cedc5220ec2f29bd53836e732e3ec14934"
DAG_HEAD = "3edb8b31b6735a0a2302a578a21dc6e50bd64046"


class CheckError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckError(message)


def strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in out, f"duplicate JSON key: {key}")
        out[key] = value
    return out


def strict_load_text(text: str) -> Any:
    try:
        return json.loads(
            text,
            object_pairs_hook=strict_pairs,
            parse_float=lambda value: (_ for _ in ()).throw(
                CheckError(f"floating JSON number forbidden: {value}")
            ),
            parse_constant=lambda value: (_ for _ in ()).throw(
                CheckError(f"non-finite JSON number forbidden: {value}")
            ),
        )
    except json.JSONDecodeError as exc:
        raise CheckError(f"invalid JSON: {exc}") from exc


def strict_load(path: Path) -> Any:
    return strict_load_text(path.read_text())


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode()


def payload_hash(manifest: dict[str, Any]) -> str:
    value = copy.deepcopy(manifest)
    value.pop("payload_sha256", None)
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(
        b"blob " + str(len(data)).encode() + b"\0" + data
    ).hexdigest()


def git_show(commit: str, path: str) -> bytes:
    proc = subprocess.run(
        ["git", "-C", str(ROOT), "show", f"{commit}:{path}"],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    require(proc.returncode == 0, f"cannot read pinned source {commit}:{path}")
    return proc.stdout


def verify_line_ranges(binding: dict[str, Any], data: bytes) -> None:
    count = len(data.decode().splitlines())
    for item in binding["line_ranges"]:
        match = re.fullmatch(r"([0-9]+)-([0-9]+)", item)
        require(match is not None, f"invalid line range {item}")
        lo, hi = map(int, match.groups())
        require(1 <= lo <= hi <= count, f"out-of-range source pin {item}")


def exact_keys(value: Any, keys: tuple[str, ...], label: str) -> None:
    require(isinstance(value, dict), f"{label} must be an object")
    require(set(value) == set(keys), f"{label} exact key set")


def require_exact_typed(actual: Any, expected: Any, label: str) -> None:
    """Recursive equality that distinguishes JSON booleans from integers."""

    require(type(actual) is type(expected), f"{label} exact JSON type")
    if isinstance(expected, dict):
        exact_keys(actual, tuple(expected), label)
        for key, expected_value in expected.items():
            require_exact_typed(actual[key], expected_value, f"{label}.{key}")
        return
    if isinstance(expected, list):
        require(len(actual) == len(expected), f"{label} exact list length")
        for index, (actual_value, expected_value) in enumerate(zip(actual, expected)):
            require_exact_typed(actual_value, expected_value, f"{label}[{index}]")
        return
    require(actual == expected, f"{label} exact value")


def verify_exact_semantic_contract(manifest: dict[str, Any]) -> None:
    """Reject a re-sealed packet whose sources, theorem, or units drift."""

    expected_base = {
        "repository": "przchojecki/rs-mca",
        "base_head": BASE_HEAD,
        "base_is_exact_pr1159_head": True,
        "upstream_main_at_refresh": "93fba1be3f3299b0ba4708d88715377bbb656e45",
        "public_dag_repository": "AllenGrahamHart/rs-mca-prize-dag",
        "public_dag_head_at_refresh": DAG_HEAD,
        "pr_heads": {
            "1157": "d7f0fd9370b3c13ff93293f08e03cadddb59b921",
            "1158": "5145fc8e0abca6325b8226294cdc2661e0891dcc",
            "1159": BASE_HEAD,
        },
    }
    exact_keys(
        manifest["base_repository"], tuple(expected_base), "base_repository"
    )
    exact_keys(
        manifest["base_repository"]["pr_heads"],
        ("1157", "1158", "1159"),
        "base_repository.pr_heads",
    )
    require_exact_typed(manifest["base_repository"], expected_base, "base_repository")

    expected_sources = [
        {
            "binding_id": "FOUNDATION_ORIGINAL_SUPPORTWISE_DEFINITION_AND_FALSE_NEAR_RATIONAL_CHAIN",
            "commit": BASE_HEAD,
            "path": "tex/cs25_cap_v13_2.tex",
            "line_ranges": ["215-226", "9518-9564", "9880-9897", "9977-10003"],
            "git_blob_sha1": "5ceff5dbc4b1ac4cef53eae7eada32046e4bafeb",
            "sha256": "356f1ad4b972746b664260191387b25a89a2e10fcc61962a49dc8282412f93ce",
            "role": "PINNED_FALSE_STATEMENTS_AND_VALID_NEAR_RATIONAL_DICHOTOMY",
        },
        {
            "binding_id": "GRANDE_ORIGINAL_SAME_SUPPORT_DEPENDENCIES",
            "commit": BASE_HEAD,
            "path": "experimental/grande_finale.tex",
            "line_ranges": [
                "132-149",
                "5744-5773",
                "6815-6846",
                "6885-6940",
                "7202-7279",
            ],
            "git_blob_sha1": "6b21d6ea937a8a9f85fc7ade6032d73efd4c7222",
            "sha256": "336ba3c9a6d9483d0eab74677d6224aae23adf15d84891c6099f6d2f45cf226d",
            "role": "EXACT_SPARSIFICATION_AND_PROOFS_REQUIRING_SAME_SUPPORT_REPAIR",
        },
    ]
    for index, binding in enumerate(manifest["source_bindings"]):
        exact_keys(
            binding,
            (
                "binding_id",
                "commit",
                "path",
                "line_ranges",
                "git_blob_sha1",
                "sha256",
                "role",
            ),
            f"source_bindings[{index}]",
        )
    require_exact_typed(manifest["source_bindings"], expected_sources, "source_bindings")

    expected_repairs = {
        "tex/cs25_cap_v13_2.tex": [
            "TWO_ANCHOR_2W_NEAR_RATIONAL_BOUND",
            "COMMON_SUPPORT_TO_EXACT_SPARSE_TRANSLATION",
            "EXACT_M_SUPPORT_NONCOMMON_SHRINK",
            "NONCOMMON_WITNESS_RANK_ONE_INJECTION_WITH_POSITIVE_W",
            "FIXED_SPLIT_KERNEL_THRESHOLD_SCOPING",
            "STALE_ONE_SLOPE_PROSE_REMOVAL",
        ],
        "experimental/grande_finale.tex": [
            "GLOBAL_CODE_LINE_SAME_WITNESS_COUNT",
            "OWNER_LOCALIZATION_SAME_SUPPORT_PUNCTURE",
            "TRIPLE_COLLAPSE_LARGE_COMMON_CORE_CASE",
            "CORRECTION_RAY_MCA_RICH_SCOPE",
        ],
    }
    require(
        [item["path"] for item in manifest["repaired_sources"]]
        == list(expected_repairs),
        "exact repaired source order",
    )
    for index, item in enumerate(manifest["repaired_sources"]):
        exact_keys(
            item,
            ("path", "git_blob_sha1", "sha256", "repairs"),
            f"repaired_sources[{index}]",
        )
        require_exact_typed(
            item["repairs"], expected_repairs[item["path"]], f"repaired_sources[{index}].repairs"
        )

    expected_rows = [
        {
            "row": "KoalaBear MCA at 2^-128",
            "n": 2097152,
            "K": 1048576,
            "agreement_m": 1116048,
            "w": 67472,
            "three_w": 202416,
            "minimum_distance": 1048577,
            "minimum_distance_margin": 846161,
            "near_rational_charge": 134944,
            "B_star": 274980728111395087,
            "B_star_minus_charge": 274980728111260143,
        },
        {
            "row": "Mersenne-31 MCA at 2^-100",
            "n": 2097152,
            "K": 1048576,
            "agreement_m": 1116024,
            "w": 67448,
            "three_w": 202344,
            "minimum_distance": 1048577,
            "minimum_distance_margin": 846233,
            "near_rational_charge": 134896,
            "B_star": 16777215,
            "B_star_minus_charge": 16642319,
        },
    ]
    row_keys = tuple(expected_rows[0])
    for index, row in enumerate(manifest["deployed_rows"]):
        exact_keys(row, row_keys, f"deployed_rows[{index}]")
    require_exact_typed(manifest["deployed_rows"], expected_rows, "deployed_rows")

    expected_counterexample = {
        "row": "KoalaBear MCA at 2^-128",
        "error_coordinate_count": 67472,
        "distinct_base_field_slopes": 67472,
        "received_line": "v(e_i)=1, u(e_i)=-gamma_i on E; u=v=0 off E",
        "common_support_size": 2029680,
        "bad_witness_support_size": 1116048,
        "bad_slope_count_lower_bound": 67472,
        "near_rational_d1_upper_bound": 67472,
        "balanced_slope_count": 0,
        "old_claimed_near_rational_allowance": 1,
        "refutes_old_displayed_bound": True,
        "same_support_noncontainment": True,
        "common_support_elsewhere": True,
    }
    exact_keys(
        manifest["actual_counterexample"],
        tuple(expected_counterexample),
        "actual_counterexample",
    )
    require_exact_typed(
        manifest["actual_counterexample"], expected_counterexample, "actual_counterexample"
    )

    expected_theorem = {
        "quantifier": "every finite field, every Reed-Solomon evaluation domain, every actual received line",
        "hypotheses": [
            "m=K+w",
            "w>=1",
            "3w<=n-K",
            "finite affine slopes",
            "support-wise MCA badness on the identical witness support",
            "near-rational slope word distance at most w from C",
        ],
        "anchor_count": 2,
        "anchor_union_support_bound": "2w",
        "third_error_union_bound": "3w",
        "projection": "z=-e_u(x)/e_v(x) on a same-witness noncontainment coordinate",
        "fiber_bound": 1,
        "conclusion": "number of near-rational support-wise MCA-bad slopes <=2w",
        "uses_layer_cake": False,
        "uses_moments": False,
        "uses_asymptotics": False,
    }
    exact_keys(
        manifest["two_anchor_theorem"], tuple(expected_theorem), "two_anchor_theorem"
    )
    require_exact_typed(
        manifest["two_anchor_theorem"], expected_theorem, "two_anchor_theorem"
    )

    expected_chronology = {
        "unit": "DISTINCT_FINITE_AFFINE_BAD_SLOPES_PER_ACTUAL_RECEIVED_LINE",
        "local_payment_proved": True,
        "first_match_owner_bound": "every first-match subset of the near-rational stratum is also <=2w",
        "global_ledger_movement": 0,
        "reason_global_movement_zero": "the active v4 maximum-type S/A/E reserve and owner chronology have not yet been regenerated",
        "U_Q": None,
        "U_BC": None,
        "U_K3": None,
        "U_new": None,
        "KoalaBear_closed": False,
    }
    exact_keys(manifest["chronology"], tuple(expected_chronology), "chronology")
    require_exact_typed(manifest["chronology"], expected_chronology, "chronology")

    expected_failures = [
        "restore common-support-implies-no-MCA statement",
        "restore one-slope near-rational allowance",
        "drop same-support noncontainment",
        "weaken 3w minimum-distance guard",
        "replace distinct slopes by witness or support counts",
        "claim Q/BC/K3 ownership",
        "claim complete-row closure",
        "mutate a source blob hash",
        "duplicate a JSON key",
    ]
    expected_toy = {
        "field": 7,
        "n": 6,
        "K": 3,
        "m": 4,
        "w": 1,
        "syndrome_pair_count": 117649,
        "expected_max_near_rational_bad_slopes": 2,
        "exhaustive": True,
    }
    exact_keys(
        manifest["regression_contract"],
        ("mandatory_failures", "toy_exact_census"),
        "regression_contract",
    )
    exact_keys(
        manifest["regression_contract"]["toy_exact_census"],
        tuple(expected_toy),
        "regression_contract.toy_exact_census",
    )
    require_exact_typed(
        manifest["regression_contract"]["mandatory_failures"],
        expected_failures,
        "regression_contract.mandatory_failures",
    )
    require_exact_typed(
        manifest["regression_contract"]["toy_exact_census"],
        expected_toy,
        "regression_contract.toy_exact_census",
    )

    expected_packet_files = [
        "experimental/notes/thresholds/kb_mca_supportwise_near_rational_two_anchor_repair_v1.md",
        "experimental/data/certificates/kb-mca-supportwise-near-rational-two-anchor-repair-v1/README.md",
        "experimental/data/schemas/kb_mca_supportwise_near_rational_two_anchor_repair_v1.schema.json",
        "experimental/scripts/verify_kb_mca_supportwise_near_rational_two_anchor_repair_v1.py",
        "experimental/scripts/verify_kb_mca_supportwise_near_rational_two_anchor_repair_v1.sage",
        "experimental/scripts/verify_kb_mca_supportwise_near_rational_two_anchor_repair_v1_flint.py",
        "experimental/scripts/verify_kb_mca_supportwise_near_rational_two_anchor_repair_v1.wl",
    ]
    require_exact_typed(manifest["packet_files"], expected_packet_files, "packet_files")


def verify_schema_shape(manifest: dict[str, Any]) -> None:
    schema = strict_load(SCHEMA_PATH)
    expected = set(schema["required"])
    require(set(manifest) == expected, "top-level schema keys")
    require(manifest["schema"] == schema["properties"]["schema"]["const"], "schema id")
    require(
        manifest["artifact_kind"]
        == schema["properties"]["artifact_kind"]["const"],
        "artifact kind",
    )
    require(len(manifest["source_bindings"]) == 2, "source binding count")
    require(len(manifest["public_dag_bindings"]) == 3, "public DAG binding count")
    require(
        len({item["binding_id"] for item in manifest["public_dag_bindings"]}) == 3,
        "duplicate public DAG binding",
    )
    require(len(manifest["repaired_sources"]) == 2, "repaired source count")
    require(len(manifest["deployed_rows"]) == 2, "deployed row count")
    require(len(manifest["packet_files"]) == 7, "packet file count")
    require(len(set(manifest["packet_files"])) == 7, "duplicate packet file")
    require(set(manifest["packet_file_sha256"]) == set(manifest["packet_files"]), "packet hash key set")
    require(
        all(re.fullmatch(r"[0-9a-f]{64}", value) for value in manifest["packet_file_sha256"].values()),
        "packet hash syntax",
    )
    require(
        re.fullmatch(r"[0-9a-f]{64}", manifest["payload_sha256"]) is not None,
        "payload hash syntax",
    )
    verify_exact_semantic_contract(manifest)


def verify_source_bindings(manifest: dict[str, Any], *, check_files: bool) -> None:
    require(manifest["base_repository"]["base_head"] == BASE_HEAD, "base head")
    require(manifest["base_repository"]["base_is_exact_pr1159_head"] is True, "PR1159 base")
    require(
        manifest["base_repository"]["public_dag_head_at_refresh"] == DAG_HEAD,
        "public DAG head",
    )
    for binding in manifest["source_bindings"]:
        require(binding["commit"] == BASE_HEAD, "source commit")
        data = git_show(binding["commit"], binding["path"])
        require(git_blob_sha1(data) == binding["git_blob_sha1"], "pinned blob hash")
        require(sha256(data) == binding["sha256"], "pinned source sha256")
        verify_line_ranges(binding, data)

    if check_files:
        for binding in manifest["repaired_sources"]:
            data = (ROOT / binding["path"]).read_bytes()
            require(git_blob_sha1(data) == binding["git_blob_sha1"], "repaired blob hash")
            require(sha256(data) == binding["sha256"], "repaired source sha256")

        foundation = (ROOT / "tex/cs25_cap_v13_2.tex").read_text()
        grande = (ROOT / "experimental/grande_finale.tex").read_text()
        required_foundation = [
            r"3w\le n-K",
            r"at most $2w$",
            r"preserves the MCA-bad slope set exactly",
            r"non-common witness support for every bad slope",
            r"z=-e_u(x)/e_v(x)",
            r"w=m-K\ge1",
            r"does not delete support-wise bad slopes",
            r"No such payment follows at arbitrary deficiency",
            r"costs at most $2w$ distinct bad slopes per line",
        ]
        for token in required_foundation:
            require(token in foundation, f"missing repaired foundation token: {token}")
        require("which by definition excludes MCA-badness" not in foundation, "old global/local implication remains")
        require("Therefore no slope is MCA-bad" not in foundation, "old near-rational deletion remains")
        require("The possible existence of a different common support is irrelevant" in grande, "owner-localization repair")
        require(r"If $c\ge m$, pair noncontainment on the same $S_\gamma$" in grande, "global-block repair")
        require(r"If $c_0\ge m$, the identical bad witness support" in grande, "triple-collapse repair")
        require(r"Call a parameter pair $(\gamma,c)$ \emph{MCA-rich}" in grande, "MCA-rich ray scope")


def verify_public_dag_bindings(manifest: dict[str, Any]) -> None:
    expected = {
        "DAG_VALID_TWO_ANCHOR_PAIR_PROXIMITY": (
            "background/nodes/v13_2_near_rational_pair_proximity/node.json",
            "320312c9385168f13de7ed02891e2bde17931040",
            "bef1ef1c35a1e788d96bc0d8d326e149441a51d6f113bfecee34c3042ae46fc7",
            "PROVED",
            "VALID_COMMON_2W_ERROR_SUPPORT_STEP",
        ),
        "DAG_REFUTED_SUPPORTWISE_PAYMENT": (
            "background/nodes/v13_2_near_rational_supportwise_payment/node.json",
            "96b7e41df6df1b53e1ed9eb605ba3aa833ff0d1c",
            "181f7d0c3c5a6b3201c9e73bce4ff306f83dc1bee3d72b87dc159c5d3152a941",
            "REFUTED",
            "PREVIOUS_TOY_REFUTATION_LEFT_DISPLAYED_PLUS_ONE_OPEN",
        ),
        "DAG_DISTINCT_LIST_EXACT_SHELL_RESULT": (
            "background/nodes/l1_exact_shell_balanced_shifted_lattice_reduction/node.json",
            "4aede45fee92421f5817e6b782d5df7f95b05524",
            "a4e05bc8e4e57b1dbaaa2465c8627bbdde45a17ed2c9349462a8d777d4250e7a",
            "PROVED",
            "DISTINCT_LIST_EXACT_SHELL_STATEMENT_NOT_REFUTED_OR_USED",
        ),
    }
    require(
        manifest["base_repository"]["public_dag_repository"]
        == "AllenGrahamHart/rs-mca-prize-dag",
        "public DAG repository",
    )
    actual = {item["binding_id"]: item for item in manifest["public_dag_bindings"]}
    require(set(actual) == set(expected), "public DAG binding ids")
    for binding_id, (path, blob, digest, status, role) in expected.items():
        item = actual[binding_id]
        exact_keys(
            item,
            (
                "binding_id",
                "repository",
                "commit",
                "path",
                "git_blob_sha1",
                "sha256",
                "status",
                "role",
            ),
            f"public_dag_bindings[{binding_id}]",
        )
        require(item["repository"] == "AllenGrahamHart/rs-mca-prize-dag", "DAG repository")
        require(item["commit"] == DAG_HEAD, "DAG commit")
        require(item["path"] == path, "DAG path")
        require(item["git_blob_sha1"] == blob, "DAG blob")
        require(item["sha256"] == digest, "DAG sha256")
        require(item["status"] == status, "DAG status")
        require(item["role"] == role, "DAG role")


def row_by_name(manifest: dict[str, Any], name: str) -> dict[str, Any]:
    rows = [row for row in manifest["deployed_rows"] if row["row"] == name]
    require(len(rows) == 1, f"row lookup {name}")
    return rows[0]


def verify_row(row: dict[str, Any]) -> None:
    n, K, m = row["n"], row["K"], row["agreement_m"]
    w = m - K
    require(w >= 1, "positive w")
    require(row["w"] == w, "w arithmetic")
    require(row["three_w"] == 3 * w, "three-w arithmetic")
    dmin = n - K + 1
    require(row["minimum_distance"] == dmin, "minimum distance")
    require(3 * w < dmin, "three-anchor minimum-distance guard")
    require(row["minimum_distance_margin"] == dmin - 3 * w, "distance margin")
    require(row["near_rational_charge"] == 2 * w, "two-anchor charge")
    require(row["B_star_minus_charge"] == row["B_star"] - 2 * w, "row remainder")


def verify_actual_counterexample(manifest: dict[str, Any]) -> None:
    row = row_by_name(manifest, "KoalaBear MCA at 2^-128")
    c = manifest["actual_counterexample"]
    n, K, m, w = row["n"], row["K"], row["agreement_m"], row["w"]
    require(c["error_coordinate_count"] == w, "counterexample E size")
    require(c["distinct_base_field_slopes"] == w, "counterexample slope count")
    require(c["common_support_size"] == n - w, "common support size")
    require(n - w >= m, "common support qualifies")
    require(m - 1 >= K, "same-witness zero-root guard")
    require(c["bad_witness_support_size"] == m, "bad support size")
    require(c["bad_slope_count_lower_bound"] == w, "bad slope lower bound")
    require(c["near_rational_d1_upper_bound"] == w, "near-rational bound")
    require(c["balanced_slope_count"] == 0, "counterexample balanced set")
    require(c["old_claimed_near_rational_allowance"] == 1, "old allowance")
    require(w > 1, "counterexample must refute +1")
    require(c["refutes_old_displayed_bound"] is True, "counterexample verdict")
    require(c["same_support_noncontainment"] is True, "same-support guard")
    require(c["common_support_elsewhere"] is True, "different common support")


def verify_theorem_contract(manifest: dict[str, Any]) -> None:
    theorem = manifest["two_anchor_theorem"]
    require(theorem["anchor_count"] == 2, "anchor count")
    require(theorem["anchor_union_support_bound"] == "2w", "anchor union")
    require(theorem["third_error_union_bound"] == "3w", "third union")
    require(theorem["fiber_bound"] == 1, "coordinate-ratio fiber")
    require("<=2w" in theorem["conclusion"], "theorem conclusion")
    require(
        any("identical witness support" in item for item in theorem["hypotheses"]),
        "same-support hypothesis",
    )
    require(theorem["uses_layer_cake"] is False, "layer cake nonclaim")
    require(theorem["uses_moments"] is False, "moment nonclaim")
    require(theorem["uses_asymptotics"] is False, "asymptotic nonclaim")

    chronology = manifest["chronology"]
    require(chronology["unit"] == "DISTINCT_FINITE_AFFINE_BAD_SLOPES_PER_ACTUAL_RECEIVED_LINE", "slope unit")
    require(chronology["local_payment_proved"] is True, "local theorem status")
    require(chronology["global_ledger_movement"] == 0, "global ledger fence")
    for key in ("U_Q", "U_BC", "U_K3", "U_new"):
        require(chronology[key] is None, f"null owner fence {key}")
    require(chronology["KoalaBear_closed"] is False, "row closure fence")


def add_vec(a: tuple[int, ...], b: tuple[int, ...], scale: int, q: int) -> tuple[int, ...]:
    return tuple((x + scale * y) % q for x, y in zip(a, b))


def span(columns: tuple[tuple[int, ...], ...], q: int) -> set[tuple[int, ...]]:
    if not columns:
        return {(0,) * 3}
    out: set[tuple[int, ...]] = set()
    for coeffs in itertools.product(range(q), repeat=len(columns)):
        value = (0, 0, 0)
        for coefficient, column in zip(coeffs, columns):
            value = add_vec(value, column, coefficient, q)
        out.add(value)
    return out


def toy_exact_census() -> tuple[int, int]:
    """Exhaust the syndrome quotient of RS[GF(7),6,3] at m=4."""

    q, n, K, m = 7, 6, 3, 4
    w = m - K
    require(3 * w <= n - K, "toy guard")
    domain = tuple(range(n))
    columns = tuple((1, x % q, x * x % q) for x in domain)
    planes = [span(tuple(columns[i] for i in pair), q) for pair in itertools.combinations(range(n), n - m)]
    near = {(0, 0, 0)}
    for column in columns:
        near |= span((column,), q)

    syndromes = tuple(itertools.product(range(q), repeat=n - K))
    max_count = 0
    pair_count = 0
    for su in syndromes:
        for sv in syndromes:
            pair_count += 1
            count = 0
            for z in range(q):
                word_syndrome = add_vec(su, sv, z, q)
                if word_syndrome not in near:
                    continue
                bad = any(
                    word_syndrome in plane
                    and not (su in plane and sv in plane)
                    for plane in planes
                )
                count += int(bad)
            max_count = max(max_count, count)
    require(pair_count == q ** (2 * (n - K)), "toy pair count")
    require(max_count == 2 * w, "toy exact two-anchor maximum")
    return pair_count, max_count


def verify_toy_contract(manifest: dict[str, Any], *, run_exhaustive: bool) -> None:
    toy = manifest["regression_contract"]["toy_exact_census"]
    require((toy["field"], toy["n"], toy["K"], toy["m"], toy["w"]) == (7, 6, 3, 4, 1), "toy row")
    require(toy["syndrome_pair_count"] == 117649, "toy pair total")
    require(toy["expected_max_near_rational_bad_slopes"] == 2, "toy maximum")
    require(toy["exhaustive"] is True, "toy exhaustiveness")
    if run_exhaustive:
        pair_count, maximum = toy_exact_census()
        require(pair_count == toy["syndrome_pair_count"], "toy replay pair total")
        require(maximum == toy["expected_max_near_rational_bad_slopes"], "toy replay maximum")


def verify_manifest(
    manifest: dict[str, Any], *, check_files: bool, run_exhaustive: bool
) -> None:
    verify_schema_shape(manifest)
    verify_source_bindings(manifest, check_files=check_files)
    verify_public_dag_bindings(manifest)
    for row in manifest["deployed_rows"]:
        verify_row(row)
    verify_actual_counterexample(manifest)
    verify_theorem_contract(manifest)
    verify_toy_contract(manifest, run_exhaustive=run_exhaustive)
    if check_files:
        for path in manifest["packet_files"]:
            require((ROOT / path).is_file(), f"missing packet file: {path}")
            require(
                sha256((ROOT / path).read_bytes()) == manifest["packet_file_sha256"][path],
                f"packet file hash: {path}",
            )
    require(payload_hash(manifest) == manifest["payload_sha256"], "payload hash")


def mutation_cases(manifest: dict[str, Any]) -> list[tuple[str, Callable[[dict[str, Any]], None]]]:
    unrelated = git_show(BASE_HEAD, "agents.md")

    def source_retarget(x: dict[str, Any]) -> None:
        binding = x["source_bindings"][0]
        binding["path"] = "agents.md"
        binding["line_ranges"] = []
        binding["git_blob_sha1"] = git_blob_sha1(unrelated)
        binding["sha256"] = sha256(unrelated)

    def duplicate_repaired_source(x: dict[str, Any]) -> None:
        x["repaired_sources"][0] = copy.deepcopy(x["repaired_sources"][1])

    def paired_budget_mutation(x: dict[str, Any]) -> None:
        target = row_by_name(x, "KoalaBear MCA at 2^-128")
        target["B_star"] += 1
        target["B_star_minus_charge"] += 1

    return [
        ("charge", lambda x: row_by_name(x, "KoalaBear MCA at 2^-128").__setitem__("near_rational_charge", 1)),
        ("guard", lambda x: row_by_name(x, "KoalaBear MCA at 2^-128").__setitem__("three_w", 1048577)),
        ("remainder", lambda x: row_by_name(x, "Mersenne-31 MCA at 2^-100").__setitem__("B_star_minus_charge", 16642320)),
        ("counter-count", lambda x: x["actual_counterexample"].__setitem__("bad_slope_count_lower_bound", 1)),
        ("old-allowance", lambda x: x["actual_counterexample"].__setitem__("old_claimed_near_rational_allowance", 67472)),
        ("same-support", lambda x: x["actual_counterexample"].__setitem__("same_support_noncontainment", False)),
        ("common-support", lambda x: x["actual_counterexample"].__setitem__("common_support_elsewhere", False)),
        ("anchor-count", lambda x: x["two_anchor_theorem"].__setitem__("anchor_count", 1)),
        ("fiber", lambda x: x["two_anchor_theorem"].__setitem__("fiber_bound", 2)),
        ("unit", lambda x: x["chronology"].__setitem__("unit", "WITNESSES")),
        ("q-owner", lambda x: x["chronology"].__setitem__("U_Q", 0)),
        ("ledger", lambda x: x["chronology"].__setitem__("global_ledger_movement", 134944)),
        ("closure", lambda x: x["chronology"].__setitem__("KoalaBear_closed", True)),
        ("source-hash", lambda x: x["source_bindings"][0].__setitem__("sha256", "0" * 64)),
        ("source-retarget", source_retarget),
        ("repair-duplicate", duplicate_repaired_source),
        ("paired-budget", paired_budget_mutation),
        ("theorem-quantifier", lambda x: x["two_anchor_theorem"].__setitem__("quantifier", "KoalaBear only")),
        ("theorem-hypotheses", lambda x: x["two_anchor_theorem"].__setitem__("hypotheses", ["identical witness support"])),
        ("theorem-conclusion", lambda x: x["two_anchor_theorem"].__setitem__("conclusion", "number of slopes <=2w; KoalaBear is closed")),
        ("nested-extra-key", lambda x: x["chronology"].__setitem__("owner", "Q")),
        ("fiber-bool", lambda x: x["two_anchor_theorem"].__setitem__("fiber_bound", True)),
        ("old-allowance-bool", lambda x: x["actual_counterexample"].__setitem__("old_claimed_near_rational_allowance", True)),
        ("ledger-bool", lambda x: x["chronology"].__setitem__("global_ledger_movement", False)),
        ("local-payment-int", lambda x: x["chronology"].__setitem__("local_payment_proved", 1)),
        ("dag-head", lambda x: x["base_repository"].__setitem__("public_dag_head_at_refresh", "0" * 40)),
        ("dag-hash", lambda x: x["public_dag_bindings"][0].__setitem__("sha256", "0" * 64)),
        ("repair-hash", lambda x: x["repaired_sources"][0].__setitem__("sha256", "0" * 64)),
        ("toy-max", lambda x: x["regression_contract"]["toy_exact_census"].__setitem__("expected_max_near_rational_bad_slopes", 1)),
        ("packet-duplicate", lambda x: x["packet_files"].__setitem__(1, x["packet_files"][0])),
        ("packet-hash", lambda x: x["packet_file_sha256"].__setitem__(x["packet_files"][0], "0" * 64)),
        ("drop-key", lambda x: x.pop("chronology")),
    ]


def tamper_selftest(manifest: dict[str, Any]) -> int:
    passed = 0
    for name, mutate in mutation_cases(manifest):
        candidate = copy.deepcopy(manifest)
        mutate(candidate)
        candidate["payload_sha256"] = payload_hash(candidate)
        try:
            verify_manifest(candidate, check_files=True, run_exhaustive=False)
        except CheckError:
            passed += 1
        else:
            raise CheckError(f"mutation survived: {name}")

    duplicate = '{"a":1,"a":2}'
    try:
        strict_load_text(duplicate)
    except CheckError:
        passed += 1
    else:
        raise CheckError("duplicate-key mutation survived")

    floating = '{"a":1.25}'
    try:
        strict_load_text(floating)
    except CheckError:
        passed += 1
    else:
        raise CheckError("floating-number mutation survived")
    return passed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    parser.add_argument("--print-payload-hash", action="store_true")
    parser.add_argument("--skip-toy", action="store_true")
    args = parser.parse_args()

    manifest = strict_load(MANIFEST_PATH)
    if args.print_payload_hash:
        print(payload_hash(manifest))
        return
    require(args.check, "use --check")
    verify_manifest(manifest, check_files=True, run_exhaustive=not args.skip_toy)
    mutations = tamper_selftest(manifest) if args.tamper_selftest else 0
    kb = row_by_name(manifest, "KoalaBear MCA at 2^-128")
    toy = manifest["regression_contract"]["toy_exact_census"]
    print("support-wise near-rational two-anchor verifier")
    print(f"  KoalaBear charge: {kb['near_rational_charge']}")
    print(f"  minimum-distance margin: {kb['minimum_distance_margin']}")
    print(f"  actual old-bound falsifier: {manifest['actual_counterexample']['bad_slope_count_lower_bound']} slopes")
    if not args.skip_toy:
        print(f"  toy exhaustive pairs: {toy['syndrome_pair_count']}, max={toy['expected_max_near_rational_bad_slopes']}")
    print(f"  hostile mutations rejected: {mutations}")
    print("RESULT: PASS")


if __name__ == "__main__":
    main()
