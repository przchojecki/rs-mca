#!/usr/bin/env python3
"""Replay selected shards of the Cycle84 projected census from current logs.

This verifier generates a small C++ replay program from the current
`slot_logs.json` projected-log certificate. The generated program rebuilds the
five-slot sorted tables, scans selected tau-canonical shards of the two-slot
tail, and reports projected duplicate bins exactly as the archived optimized
census did.

By default it replays the 30 shards that contain the recorded duplicate bins.
That verifies every recorded duplicate bin by recomputation from the current log
certificate and checks that no extra duplicate appears in those selected shards.
It does not prove that unselected shards have no duplicates. Use `--all-shards`
to rerun the complete 16,384-shard projected census.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import verify_m1_cycle84_projected_census_receipt as receipt_check
import verify_m1_cycle84_projected_log_certificate as log_cert


CPP_SOURCE_TEMPLATE = r"""
#include <parallel/algorithm>
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>

@@LOG_TABLES@@

static constexpr uint64_t KAP = 15337197211725320908ULL;
static constexpr uint64_t S0 = 7668598605862660454ULL;
static constexpr uint64_t S1 = 15778797251807138534ULL;
static constexpr uint64_t HALF = MOD / 2;
static constexpr int SHARDS = 16384;

static inline uint64_t addm(uint64_t a, uint64_t b) {
    __uint128_t z = static_cast<__uint128_t>(a) + b;
    if (z >= MOD) z -= MOD;
    return static_cast<uint64_t>(z);
}

static inline uint64_t subm(uint64_t a, uint64_t b) {
    return a >= b ? a - b : static_cast<uint64_t>(static_cast<__uint128_t>(a) + MOD - b);
}

static inline uint64_t mix(uint64_t x) {
    x += 0x9e3779b97f4a7c15ULL;
    x = (x ^ (x >> 30)) * 0xbf58476d1ce4e5b9ULL;
    x = (x ^ (x >> 27)) * 0x94d049bb133111ebULL;
    return x ^ (x >> 31);
}

static int tauk(int k) {
    int i = k / 16 + 1;
    int a = k % 16;
    if (i == 1) return 16 + (a + 6) % 16;
    if (i == 2) return (a + 10) % 16;
    return 32 + (a + 8) % 16;
}

template <class F>
static void circular_slice(
    const std::vector<uint64_t>& values,
    uint64_t start,
    uint64_t low,
    uint64_t high,
    F&& visit
) {
    if (low >= high) return;
    __uint128_t aa = static_cast<__uint128_t>(start) + low;
    __uint128_t bb = static_cast<__uint128_t>(start) + high;
    uint64_t a = static_cast<uint64_t>(aa % MOD);
    uint64_t b = static_cast<uint64_t>(bb % MOD);
    if (aa / MOD == ((bb - 1) / MOD)) {
        auto i = std::lower_bound(values.begin(), values.end(), a);
        auto j = (b == 0 ? values.end() : std::lower_bound(values.begin(), values.end(), b));
        for (auto p = i; p != j; ++p) visit(*p);
    } else {
        auto i = std::lower_bound(values.begin(), values.end(), a);
        for (auto p = i; p != values.end(); ++p) visit(*p);
        auto j = std::lower_bound(values.begin(), values.end(), b);
        for (auto p = values.begin(); p != j; ++p) visit(*p);
    }
}

struct Tail {
    uint64_t log_sum;
    uint8_t color;
};

struct Duplicate {
    uint64_t key;
    uint16_t count;
    int shard;
};

static std::vector<int> parse_shards(int argc, char** argv) {
    std::vector<int> shards;
    if (argc == 2 && std::string(argv[1]) == "all") {
        shards.reserve(SHARDS);
        for (int shard = 0; shard < SHARDS; ++shard) shards.push_back(shard);
        return shards;
    }
    for (int i = 1; i < argc; ++i) {
        int shard = std::atoi(argv[i]);
        if (shard < 0 || shard >= SHARDS) {
            throw std::runtime_error("selected shard out of range");
        }
        shards.push_back(shard);
    }
    std::sort(shards.begin(), shards.end());
    shards.erase(std::unique(shards.begin(), shards.end()), shards.end());
    if (shards.empty()) throw std::runtime_error("no shards selected");
    return shards;
}

int main(int argc, char** argv) {
    const std::vector<int> selected_shards = parse_shards(argc, argv);

    uint64_t kappa = 0;
    for (int t = 0; t < 7; ++t) {
        uint64_t kt = addm(LOGS[t][0], LOGS[t][tauk(0)]);
        for (int k = 0; k < 48; ++k) {
            if (tauk(tauk(k)) != k || tauk(k) == k) {
                throw std::runtime_error("tau is not a fixed-point-free involution");
            }
            if (addm(LOGS[t][k], LOGS[t][tauk(k)]) != kt) {
                throw std::runtime_error("tau log sum is not constant");
            }
            if (((COLORS[t][k] + COLORS[t][tauk(k)]) & 15) != 8) {
                throw std::runtime_error("tau color complement failed");
            }
        }
        kappa = addm(kappa, kt);
    }
    if (kappa != KAP || addm(S0, S0) != KAP || addm(S1, S1) != KAP) {
        throw std::runtime_error("tau constants do not match receipt");
    }

    std::vector<int> half_keys;
    for (int k = 0; k < 48; ++k) {
        if (k < tauk(k)) half_keys.push_back(k);
    }
    if (half_keys.size() != 24) throw std::runtime_error("bad tau orientation");

    std::array<std::vector<uint64_t>, 16> base;
    std::array<size_t, 16> counts{};
    for (int a : half_keys) {
        for (int b = 0; b < 48; ++b) {
            for (int c = 0; c < 48; ++c) {
                for (int d = 0; d < 48; ++d) {
                    for (int e = 0; e < 48; ++e) {
                        int color = (
                            COLORS[0][a] + COLORS[1][b] + COLORS[2][c] +
                            COLORS[3][d] + COLORS[4][e]
                        ) & 15;
                        counts[color]++;
                    }
                }
            }
        }
    }
    for (int color = 0; color < 16; ++color) base[color].reserve(counts[color]);

    for (int a : half_keys) {
        for (int b = 0; b < 48; ++b) {
            for (int c = 0; c < 48; ++c) {
                uint64_t s3 = addm(addm(LOGS[0][a], LOGS[1][b]), LOGS[2][c]);
                int c3 = (COLORS[0][a] + COLORS[1][b] + COLORS[2][c]) & 15;
                for (int d = 0; d < 48; ++d) {
                    uint64_t s4 = addm(s3, LOGS[3][d]);
                    int c4 = (c3 + COLORS[3][d]) & 15;
                    for (int e = 0; e < 48; ++e) {
                        int color = (c4 + COLORS[4][e]) & 15;
                        base[color].push_back(addm(s4, LOGS[4][e]));
                    }
                }
            }
        }
    }
    for (int color = 0; color < 16; ++color) {
        __gnu_parallel::sort(base[color].begin(), base[color].end());
        for (size_t i = 1; i < base[color].size(); ++i) {
            if (base[color][i] == base[color][i - 1]) {
                throw std::runtime_error("five-slot same-color collision");
            }
        }
    }

    std::vector<Tail> tails;
    tails.reserve(48 * 48);
    for (int f = 0; f < 48; ++f) {
        for (int g = 0; g < 48; ++g) {
            tails.push_back({
                addm(LOGS[5][f], LOGS[6][g]),
                static_cast<uint8_t>((COLORS[5][f] + COLORS[6][g]) & 15),
            });
        }
    }

    uint64_t expected_total = 0;
    for (const auto& tail : tails) {
        expected_total += base[(4 - tail.color) & 15].size();
    }
    if (expected_total != 26373783552ULL) {
        throw std::runtime_error("unexpected tau half-domain count");
    }

    uint64_t fixed0 = 0;
    uint64_t fixed1 = 0;
    for (const auto& tail : tails) {
        const auto& values = base[(4 - tail.color) & 15];
        fixed0 += std::binary_search(values.begin(), values.end(), subm(S0, tail.log_sum));
        fixed1 += std::binary_search(values.begin(), values.end(), subm(S1, tail.log_sum));
    }
    if (fixed0 != 0 || fixed1 != 0) {
        throw std::runtime_error("fixed tau roots have selected tuples");
    }

    static constexpr size_t CAP = 1ULL << 22;
    static constexpr size_t MASK = CAP - 1;
    std::vector<uint64_t> table(CAP, std::numeric_limits<uint64_t>::max());
    std::vector<uint32_t> used;
    used.reserve(1800000);
    std::unordered_map<uint64_t, uint16_t> duplicate_counts;
    duplicate_counts.reserve(32);
    std::vector<Duplicate> duplicates;
    uint64_t selected_entries = 0;
    uint64_t selected_energy = 0;
    uint16_t selected_max = 1;

    for (int shard : selected_shards) {
        uint64_t lo = static_cast<uint64_t>(
            static_cast<__uint128_t>(HALF) * shard / SHARDS
        );
        uint64_t hi = static_cast<uint64_t>(
            static_cast<__uint128_t>(HALF) * (shard + 1) / SHARDS
        );
        uint64_t l2 = MOD - hi + 1;
        __uint128_t upper = static_cast<__uint128_t>(MOD) - lo + 1;
        uint64_t u2 = upper > MOD ? MOD : static_cast<uint64_t>(upper);

        uint64_t entries = 0;
        uint64_t energy = 0;
        uint16_t max_multiplicity = 1;
        used.clear();
        duplicate_counts.clear();

        auto insert = [&](uint64_t base_log, uint64_t tail_log) {
            uint64_t projected = addm(base_log, tail_log);
            uint64_t z = subm(projected, S0);
            uint64_t canonical = std::min(z, MOD - z);
            if (!(lo <= canonical && canonical < hi)) {
                throw std::runtime_error("canonical key outside shard range");
            }
            entries++;
            size_t position = mix(canonical) & MASK;
            for (;;) {
                uint64_t current = table[position];
                if (current == std::numeric_limits<uint64_t>::max()) {
                    table[position] = canonical;
                    used.push_back(static_cast<uint32_t>(position));
                    return;
                }
                if (current == canonical) {
                    auto result = duplicate_counts.emplace(canonical, 1);
                    uint16_t old = result.first->second;
                    energy += 2ULL * old;
                    result.first->second = old + 1;
                    max_multiplicity = std::max(max_multiplicity, result.first->second);
                    return;
                }
                position = (position + 1) & MASK;
            }
        };

        for (const auto& tail : tails) {
            const auto& values = base[(4 - tail.color) & 15];
            uint64_t start = subm(S0, tail.log_sum);
            circular_slice(values, start, lo, hi, [&](uint64_t base_log) {
                insert(base_log, tail.log_sum);
            });
            if (l2 < MOD && l2 < u2) {
                circular_slice(values, start, l2, u2, [&](uint64_t base_log) {
                    insert(base_log, tail.log_sum);
                });
            }
        }

        if (used.size() > CAP * 3 / 5) {
            throw std::runtime_error("hash table load is too high");
        }
        for (uint32_t position : used) table[position] = std::numeric_limits<uint64_t>::max();

        selected_entries += entries;
        selected_energy += energy;
        selected_max = std::max(selected_max, max_multiplicity);
        for (const auto& item : duplicate_counts) {
            duplicates.push_back({item.first, item.second, shard});
        }
    }

    std::sort(duplicates.begin(), duplicates.end(), [](const auto& a, const auto& b) {
        if (a.key != b.key) return a.key < b.key;
        return a.shard < b.shard;
    });
    uint64_t duplicate_energy = 0;
    uint16_t duplicate_max = 1;
    for (const auto& item : duplicates) {
        duplicate_energy += static_cast<uint64_t>(item.count) * (item.count - 1);
        duplicate_max = std::max(duplicate_max, item.count);
    }
    if (duplicate_energy != selected_energy || duplicate_max != selected_max) {
        throw std::runtime_error("duplicate summary mismatch");
    }

    std::cout << "{\n";
    std::cout << "  \"selected_shard_count\": " << selected_shards.size() << ",\n";
    std::cout << "  \"all_shards\": " << (selected_shards.size() == SHARDS ? "true" : "false") << ",\n";
    if (selected_shards.size() <= 256) {
        std::cout << "  \"selected_shards\": [";
        for (size_t i = 0; i < selected_shards.size(); ++i) {
            if (i) std::cout << ", ";
            std::cout << selected_shards[i];
        }
        std::cout << "],\n";
    }
    std::cout << "  \"tau_half_domain_expected\": " << expected_total << ",\n";
    std::cout << "  \"fixed_selected_counts\": [" << fixed0 << ", " << fixed1 << "],\n";
    std::cout << "  \"selected_entries\": " << selected_entries << ",\n";
    std::cout << "  \"selected_folded_ordered_energy\": " << selected_energy << ",\n";
    std::cout << "  \"selected_max_canonical_projected_multiplicity\": " << selected_max << ",\n";
    std::cout << "  \"duplicate_canonical_bins\": [\n";
    for (size_t i = 0; i < duplicates.size(); ++i) {
        const auto& item = duplicates[i];
        std::cout << "    {\"key\": " << item.key
                  << ", \"count\": " << item.count
                  << ", \"shard\": " << item.shard << "}";
        if (i + 1 != duplicates.size()) std::cout << ",";
        std::cout << "\n";
    }
    std::cout << "  ]\n";
    std::cout << "}\n";
    return 0;
}
"""


def load_log_tables() -> Dict[str, Any]:
    log_report = log_cert.build_report()
    raw = log_cert.DEFAULT_CERTIFICATE.read_bytes()
    certificate = json.loads(raw)
    tables = log_cert.verify_records(certificate)
    return {
        "report": log_report,
        "logs_mod_m": tables["logs_mod_m"],
        "colors": tables["colors"],
    }


def load_receipt(receipt_path: Path) -> tuple[Dict[str, Any], Dict[str, Any]]:
    receipt_report = receipt_check.build_report(receipt_path)
    receipt_data = json.loads(receipt_path.read_bytes())
    return receipt_report, receipt_data


def render_cpp_table(
    type_name: str,
    table_name: str,
    values: Sequence[Sequence[int]],
    suffix: str = "",
) -> str:
    rows = []
    for row in values:
        rows.append("  {" + ", ".join(f"{int(value)}{suffix}" for value in row) + "}")
    return (
        f"static constexpr {type_name} {table_name}[7][48] = {{\n"
        + ",\n".join(rows)
        + "\n};"
    )


def render_cpp_source(logs_mod_m: Sequence[Sequence[int]], colors: Sequence[Sequence[int]]) -> str:
    tables = "\n".join(
        [
            f"static constexpr uint64_t MOD = {log_cert.M}ULL;",
            render_cpp_table("uint64_t", "LOGS", logs_mod_m, "ULL"),
            render_cpp_table("uint8_t", "COLORS", colors),
        ]
    )
    return CPP_SOURCE_TEMPLATE.replace("@@LOG_TABLES@@", tables)


def receipt_bins_for_shards(
    receipt_data: Dict[str, Any],
    selected_shards: Sequence[int],
) -> list[Dict[str, int]]:
    selected = set(selected_shards)
    return [
        {
            "key": int(item["key"]),
            "count": int(item["count"]),
            "shard": int(item["shard"]),
        }
        for item in receipt_data["duplicate_canonical_bins"]
        if int(item["shard"]) in selected
    ]


def normalize_bins(items: Sequence[Dict[str, Any]]) -> list[Dict[str, int]]:
    return sorted(
        [
            {
                "key": int(item["key"]),
                "count": int(item["count"]),
                "shard": int(item["shard"]),
            }
            for item in items
        ],
        key=lambda item: (item["key"], item["shard"], item["count"]),
    )


def selected_shards_from_args(args: argparse.Namespace, receipt_data: Dict[str, Any]) -> list[int]:
    shard_count = int(receipt_data["canonical_shards"])
    if args.all_shards:
        return list(range(shard_count))
    if args.shards:
        shards = sorted(set(args.shards))
    else:
        shards = sorted(
            {int(item["shard"]) for item in receipt_data["duplicate_canonical_bins"]}
        )
    bad = [shard for shard in shards if shard < 0 or shard >= shard_count]
    if bad:
        raise AssertionError(("selected shard out of range", bad))
    if not shards:
        raise AssertionError("no shards selected")
    return shards


def run_cpp_replay(
    source: str,
    selected_shards: Sequence[int],
    all_shards: bool,
    cxx: str,
) -> Dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="m1-cycle84-shards-") as tmp:
        tmp_path = Path(tmp)
        source_path = tmp_path / "cycle84_shard_replay.cpp"
        exe_path = tmp_path / "cycle84_shard_replay"
        source_path.write_text(source)

        compile_cmd = [
            cxx,
            "-O3",
            "-std=c++17",
            "-fopenmp",
            str(source_path),
            "-o",
            str(exe_path),
        ]
        compile_result = subprocess.run(
            compile_cmd,
            cwd=tmp_path,
            text=True,
            capture_output=True,
            check=False,
        )
        if compile_result.returncode != 0:
            raise RuntimeError(
                "C++ shard replay compilation failed\n"
                + compile_result.stdout
                + compile_result.stderr
            )

        run_args = ["all"] if all_shards else [str(shard) for shard in selected_shards]
        run_result = subprocess.run(
            [str(exe_path), *run_args],
            cwd=tmp_path,
            text=True,
            capture_output=True,
            check=False,
        )
        if run_result.returncode != 0:
            raise RuntimeError(
                "C++ shard replay failed\n" + run_result.stdout + run_result.stderr
            )
        return json.loads(run_result.stdout)


def verify_replay(
    replay: Dict[str, Any],
    receipt_report: Dict[str, Any],
    receipt_data: Dict[str, Any],
    selected_shards: Sequence[int],
    all_shards: bool,
) -> Dict[str, bool]:
    expected_bins = normalize_bins(receipt_bins_for_shards(receipt_data, selected_shards))
    replay_bins = normalize_bins(replay["duplicate_canonical_bins"])
    selected_energy = sum(item["count"] * (item["count"] - 1) for item in replay_bins)
    selected_max = max([1, *(item["count"] for item in replay_bins)])

    checks = {
        "receipt_verifier_passes": receipt_report["status"] == "PASS",
        "selected_shard_count_matches": (
            int(replay["selected_shard_count"]) == len(selected_shards)
        ),
        "selected_shards_match_when_reported": (
            "selected_shards" not in replay
            or [int(value) for value in replay["selected_shards"]] == list(selected_shards)
        ),
        "all_shards_flag_matches": bool(replay["all_shards"]) == all_shards,
        "tau_half_domain_expected_matches_receipt": (
            int(replay["tau_half_domain_expected"])
            == int(receipt_data["tau_half_domain_expected"])
        ),
        "fixed_selected_counts_match_receipt": (
            [int(value) for value in replay["fixed_selected_counts"]]
            == [int(value) for value in receipt_data["fixed_selected_counts"]]
        ),
        "duplicate_bins_match_receipt_on_selected_shards": replay_bins == expected_bins,
        "selected_energy_matches_replayed_bins": (
            int(replay["selected_folded_ordered_energy"]) == selected_energy
        ),
        "selected_max_matches_replayed_bins": (
            int(replay["selected_max_canonical_projected_multiplicity"]) == selected_max
        ),
    }
    if all_shards:
        checks.update(
            {
                "all_shard_entries_match_receipt": (
                    int(replay["selected_entries"])
                    == int(receipt_data["tau_half_domain_counted"])
                ),
                "all_shard_energy_matches_receipt": (
                    int(replay["selected_folded_ordered_energy"])
                    == int(receipt_data["folded_ordered_energy"])
                ),
                "all_shard_max_matches_receipt": (
                    int(replay["selected_max_canonical_projected_multiplicity"])
                    == int(receipt_data["max_canonical_projected_multiplicity"])
                ),
            }
        )

    return checks


def build_report(args: argparse.Namespace) -> Dict[str, Any]:
    receipt_path = args.receipt
    receipt_report, receipt_data = load_receipt(receipt_path)
    log_tables = load_log_tables()
    selected_shards = selected_shards_from_args(args, receipt_data)
    cpp_source = render_cpp_source(log_tables["logs_mod_m"], log_tables["colors"])
    replay = run_cpp_replay(cpp_source, selected_shards, args.all_shards, args.cxx)
    checks = verify_replay(
        replay,
        receipt_report,
        receipt_data,
        selected_shards,
        args.all_shards,
    )
    failed = [name for name, value in checks.items() if not value]
    if failed:
        raise AssertionError(f"failed checks: {', '.join(failed)}")

    replay_bins = normalize_bins(replay["duplicate_canonical_bins"])
    status = (
        "AUDIT / FINITE-MODEL-PROJECTED-CENSUS-FULL-REPLAYED / CONDITIONAL"
        if args.all_shards
        else "AUDIT / FINITE-MODEL-PROJECTED-CENSUS-SHARD-REPLAYED / CONDITIONAL"
    )
    remaining_import = (
        "source-code audit of this generated replay"
        if args.all_shards
        else (
            "unselected census shards; run this verifier with --all-shards for "
            "a complete projected-census replay"
        )
    )
    try:
        display_receipt_path = str(receipt_path.resolve().relative_to(receipt_check.REPO_ROOT))
    except ValueError:
        display_receipt_path = str(receipt_path)

    return {
        "status": "PASS",
        "proof_status": status,
        "theorem_problem_id": "M1 Cycle84 projected census shard replay",
        "receipt_path": display_receipt_path,
        "selected_shard_count": len(selected_shards),
        "all_shards": args.all_shards,
        "selected_shards": selected_shards if len(selected_shards) <= 256 else None,
        "duplicate_bins_replayed": len(replay_bins),
        "selected_entries": int(replay["selected_entries"]),
        "selected_folded_ordered_energy": int(
            replay["selected_folded_ordered_energy"]
        ),
        "selected_max_canonical_projected_multiplicity": int(
            replay["selected_max_canonical_projected_multiplicity"]
        ),
        "checks": checks,
        "remaining_import": remaining_import,
        "imports_required": [
            remaining_import,
            "official ABF source gate verification",
        ],
        "nonmutating": True,
    }


def print_human(report: Dict[str, Any]) -> None:
    print("m1_cycle84_projected_census_shard_replay: PASS")
    print(f"status={report['proof_status']}")
    print(f"theorem_problem_id={report['theorem_problem_id']}")
    print(
        "replay="
        f"selected_shards={report['selected_shard_count']}, "
        f"all_shards={report['all_shards']}, "
        f"duplicate_bins={report['duplicate_bins_replayed']}, "
        f"entries={report['selected_entries']}, "
        f"energy={report['selected_folded_ordered_energy']}, "
        f"max={report['selected_max_canonical_projected_multiplicity']}"
    )
    print(f"remaining_import={report['remaining_import']}")
    print("imports_required=" + "; ".join(report["imports_required"]))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Replay selected shards of the M1 Cycle84 projected census."
    )
    parser.add_argument(
        "--receipt",
        type=Path,
        default=receipt_check.DEFAULT_RECEIPT,
        help="path to projected_census_receipt.json",
    )
    parser.add_argument(
        "--shards",
        type=int,
        nargs="+",
        default=None,
        help="specific canonical shards to replay; defaults to receipt duplicate shards",
    )
    parser.add_argument(
        "--all-shards",
        action="store_true",
        help="replay all 16,384 shards instead of only selected shards",
    )
    parser.add_argument(
        "--cxx",
        default=os.environ.get("CXX", "g++"),
        help="C++ compiler to use",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="print the audit report as JSON",
    )
    args = parser.parse_args()
    if args.all_shards and args.shards:
        parser.error("--all-shards cannot be combined with --shards")

    report = build_report(args)
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print_human(report)


if __name__ == "__main__":
    main()
