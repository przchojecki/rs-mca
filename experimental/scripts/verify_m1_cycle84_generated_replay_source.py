#!/usr/bin/env python3
"""Verify the generated Cycle84 projected-census C++ source contract.

This nonmutating verifier audits the actual C++ source emitted by
verify_m1_cycle84_projected_census_shard_replay.py for the recorded
all-shards run with --threads 16. It checks that the generated source:

* has the expected SHA256;
* injects the current 7x48 projected-log and color tables exactly;
* contains no unresolved template markers;
* contains the constants, tau checks, five-two split, shard interval logic,
  canonical-key map, duplicate-energy accounting, and JSON output fields used
  by the replay algorithm audit.

It does not compile or run the replay; that is handled by the shard replay
verifier and saved full-replay receipt.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import verify_m1_cycle84_projected_census_shard_replay as replay


EXPECTED_THREADS = 16
EXPECTED_SOURCE_SHA256 = (
    "555ba27f00378d88b9406d571f64dee74d355ca124ed2292421f6a8e973969c5"
)

EXACT_FRAGMENT_COUNTS = {
    "thread_constant": "static constexpr int THREADS = 16;",
    "shard_constant": "static constexpr int SHARDS = 16384;",
    "tau_constant": "static constexpr uint64_t KAP = 15337197211725320908ULL;",
    "fixed_root_s0": "static constexpr uint64_t S0 = 7668598605862660454ULL;",
    "fixed_root_s1": "static constexpr uint64_t S1 = 15778797251807138534ULL;",
    "half_modulus": "static constexpr uint64_t HALF = MOD / 2;",
    "openmp_parallel": "#pragma omp parallel num_threads(THREADS)",
    "openmp_shard_loop": "#pragma omp for schedule(dynamic, 1)",
}

REQUIRED_FRAGMENTS = {
    "template_marker_removed": "@@",
    "tau_involution_guard": "tauk(tauk(k)) != k || tauk(k) == k",
    "tau_log_constant_guard": "addm(LOGS[t][k], LOGS[t][tauk(k)]) != kt",
    "tau_color_guard": "((COLORS[t][k] + COLORS[t][tauk(k)]) & 15) != 8",
    "tau_constants_guard": "kappa != KAP || addm(S0, S0) != KAP || addm(S1, S1) != KAP",
    "half_domain_orientation": "if (k < tauk(k)) half_keys.push_back(k);",
    "five_slot_count_loop": "for (int a : half_keys)",
    "five_slot_color_bucket": "std::array<std::vector<uint64_t>, 16> base;",
    "same_color_collision_guard": "throw std::runtime_error(\"five-slot same-color collision\");",
    "two_slot_tail_table": "std::vector<Tail> tails;",
    "color_complement_bucket": "base[(4 - tail.color) & 15]",
    "half_domain_total_guard": "expected_total != 26373783552ULL",
    "fixed_root_guard": "fixed0 != 0 || fixed1 != 0",
    "shard_low_bound": "static_cast<__uint128_t>(HALF) * shard / SHARDS",
    "shard_high_bound": "static_cast<__uint128_t>(HALF) * (shard + 1) / SHARDS",
    "second_branch_low": "uint64_t l2 = MOD - hi + 1;",
    "second_branch_high": "uint64_t u2 = upper > MOD ? MOD : static_cast<uint64_t>(upper);",
    "canonical_key": "uint64_t canonical = std::min(z, MOD - z);",
    "canonical_shard_guard": "if (!(lo <= canonical && canonical < hi))",
    "duplicate_energy_increment": "energy += 2ULL * old;",
    "duplicate_count_increment": "result.first->second = old + 1;",
    "hash_load_guard": "used.size() > CAP * 3 / 5",
    "selected_energy_atomic": "selected_energy.fetch_add(energy, std::memory_order_relaxed);",
    "duplicate_summary_guard": "duplicate_energy != selected_energy.load() || duplicate_max != selected_max.load()",
    "json_duplicate_bins": "\\\"duplicate_canonical_bins\\\"",
}

ORDERED_FRAGMENTS = [
    "static int tauk(int k)",
    "static void circular_slice(",
    "struct Tail",
    "struct Duplicate",
    "static std::vector<int> parse_shards",
    "int main(int argc, char** argv)",
    "const std::vector<int> selected_shards",
    "if (kappa != KAP || addm(S0, S0) != KAP || addm(S1, S1) != KAP)",
    "std::vector<int> half_keys;",
    "std::array<std::vector<uint64_t>, 16> base;",
    "std::vector<Tail> tails;",
    "uint64_t expected_total = 0;",
    "static constexpr size_t CAP = 1ULL << 22;",
    "#pragma omp parallel num_threads(THREADS)",
    "#pragma omp for schedule(dynamic, 1)",
    "uint64_t lo = static_cast<uint64_t>(",
    "auto insert = [&](uint64_t base_log, uint64_t tail_log)",
    "circular_slice(values, start, lo, hi",
    "selected_entries.fetch_add(entries, std::memory_order_relaxed);",
    "std::sort(duplicates.begin(), duplicates.end()",
    "std::cout << \"{\\n\";",
]


def source_for_threads(threads: int = EXPECTED_THREADS) -> tuple[str, Dict[str, Any]]:
    log_tables = replay.load_log_tables()
    source = replay.render_cpp_source(
        log_tables["logs_mod_m"],
        log_tables["colors"],
        threads,
    )
    return source, log_tables


def parse_cpp_table(source: str, table_name: str, suffix: str = "") -> list[list[int]]:
    pattern = re.compile(
        rf"static constexpr (?:uint64_t|uint8_t) {table_name}\[7\]\[48\] = \{{\n"
        rf"(?P<body>.*?)\n\}};",
        re.DOTALL,
    )
    match = pattern.search(source)
    if not match:
        raise AssertionError(f"missing generated table {table_name}")
    rows = []
    for row_text in re.findall(r"\{([^{}]+)\}", match.group("body")):
        values = []
        for token in row_text.split(","):
            clean = token.strip()
            if suffix and clean.endswith(suffix):
                clean = clean[: -len(suffix)]
            values.append(int(clean))
        rows.append(values)
    return rows


def fragment_presence(source: str) -> Dict[str, bool]:
    return {
        name: (
            fragment not in source
            if name == "template_marker_removed"
            else fragment in source
        )
        for name, fragment in REQUIRED_FRAGMENTS.items()
    }


def exact_fragment_counts(source: str) -> Dict[str, int]:
    return {
        name: source.count(fragment)
        for name, fragment in EXACT_FRAGMENT_COUNTS.items()
    }


def ordered_fragments(source: str) -> Dict[str, Any]:
    positions = []
    for fragment in ORDERED_FRAGMENTS:
        index = source.find(fragment)
        if index < 0:
            raise AssertionError(f"missing ordered fragment: {fragment}")
        positions.append(index)
    return {
        "fragment_count": len(ORDERED_FRAGMENTS),
        "strictly_in_source_order": positions == sorted(positions),
        "first_position": positions[0],
        "last_position": positions[-1],
    }


def table_matches(
    parsed: Sequence[Sequence[int]],
    expected: Sequence[Sequence[int]],
) -> bool:
    parsed_ints = [[int(value) for value in row] for row in parsed]
    expected_ints = [[int(value) for value in row] for row in expected]
    return parsed_ints == expected_ints


def build_report(threads: int = EXPECTED_THREADS) -> Dict[str, Any]:
    if threads != EXPECTED_THREADS:
        raise AssertionError(f"this contract is for --threads {EXPECTED_THREADS}")
    source, log_tables = source_for_threads(threads)
    source_sha256 = hashlib.sha256(source.encode()).hexdigest()
    parsed_logs = parse_cpp_table(source, "LOGS", "ULL")
    parsed_colors = parse_cpp_table(source, "COLORS")
    presence = fragment_presence(source)
    counts = exact_fragment_counts(source)
    order = ordered_fragments(source)

    checks = {
        "source_sha256_matches_expected": source_sha256 == EXPECTED_SOURCE_SHA256,
        "generated_source_has_no_template_markers": presence["template_marker_removed"],
        "logs_table_matches_projected_log_certificate": table_matches(
            parsed_logs,
            log_tables["logs_mod_m"],
        ),
        "colors_table_matches_projected_log_certificate": table_matches(
            parsed_colors,
            log_tables["colors"],
        ),
        "logs_table_shape_7_by_48": (
            len(parsed_logs) == 7 and all(len(row) == 48 for row in parsed_logs)
        ),
        "colors_table_shape_7_by_48": (
            len(parsed_colors) == 7 and all(len(row) == 48 for row in parsed_colors)
        ),
        "all_required_fragments_present": all(presence.values()),
        "exact_fragments_occur_once": all(count == 1 for count in counts.values()),
        "ordered_fragments_in_source_order": order["strictly_in_source_order"],
        "uses_current_log_certificate": log_tables["report"]["status"] == "PASS",
    }

    failed = [name for name, value in checks.items() if not value]
    if failed:
        raise AssertionError(f"failed checks: {', '.join(failed)}")

    return {
        "status": "PASS",
        "proof_status": "AUDIT / GENERATED-CYCLE84-CXX-SOURCE-CONTRACT",
        "theorem_problem_id": "M1 Cycle84 generated projected-census replay source",
        "source": {
            "threads": threads,
            "sha256": source_sha256,
            "line_count": len(source.splitlines()),
            "byte_count": len(source.encode()),
        },
        "tables": {
            "logs_rows": len(parsed_logs),
            "logs_columns": len(parsed_logs[0]) if parsed_logs else 0,
            "colors_rows": len(parsed_colors),
            "colors_columns": len(parsed_colors[0]) if parsed_colors else 0,
            "projected_log_certificate_sha256": log_tables["report"][
                "certificate_sha256"
            ],
        },
        "fragment_counts": counts,
        "required_fragment_count": len(REQUIRED_FRAGMENTS),
        "ordered_fragments": order,
        "checks": checks,
        "remaining_import": (
            "reviewer acceptance that this source contract is sufficient for "
            "promotion beyond audit status"
        ),
        "imports_required": [
            "Cycle84 replay algorithm audit",
            "saved all-shards replay receipt",
            "official ABF source gate verification",
        ],
        "nonmutating": True,
    }


def print_human(report: Dict[str, Any]) -> None:
    source = report["source"]
    tables = report["tables"]
    print("m1_cycle84_generated_replay_source: PASS")
    print(f"status={report['proof_status']}")
    print(f"theorem_problem_id={report['theorem_problem_id']}")
    print(
        "source="
        f"threads={source['threads']}, sha256={source['sha256']}, "
        f"lines={source['line_count']}, bytes={source['byte_count']}"
    )
    print(
        "tables="
        f"LOGS={tables['logs_rows']}x{tables['logs_columns']}, "
        f"COLORS={tables['colors_rows']}x{tables['colors_columns']}, "
        f"certificate_sha256={tables['projected_log_certificate_sha256']}"
    )
    print(
        "source_contract="
        f"constants={len(report['fragment_counts'])}, "
        f"landmarks={report['required_fragment_count']}, "
        f"ordered_fragments={report['ordered_fragments']['fragment_count']}"
    )
    print(f"remaining_import={report['remaining_import']}")
    print("imports_required=" + "; ".join(report["imports_required"]))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Verify the generated Cycle84 projected-census C++ source contract."
    )
    parser.add_argument(
        "--threads",
        type=int,
        default=EXPECTED_THREADS,
        help="thread setting for the generated source contract; only 16 is recorded",
    )
    parser.add_argument("--json", action="store_true", help="print JSON report")
    args = parser.parse_args()

    report = build_report(args.threads)
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print_human(report)


if __name__ == "__main__":
    main()
