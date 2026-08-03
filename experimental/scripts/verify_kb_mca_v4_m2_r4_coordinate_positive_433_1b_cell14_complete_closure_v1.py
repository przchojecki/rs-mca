#!/usr/bin/env python3
"""Fail-closed verifier for the positive 433-1b cell-14 complete closure.

Pure python, no third-party imports. Replays the census arithmetic and
the canonical matching classification, cross-checks the certificate
JSON, and checks the note's ledger and nonclaim sentences. The
per-family proofs are pinned by node id to the canonical DAG
(https://github.com/AllenGrahamHart/rs-mca-prize-dag), where their own
verifiers were replayed at audit; they are NOT re-verified here.
"""

import json
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parents[2]
NAME = "kb_mca_v4_m2_r4_coordinate_positive_433_1b_cell14_complete_closure_v1"
NOTE = ROOT / "experimental/notes/frontier-adjacent" / (NAME + ".md")
CERT = (ROOT / "experimental/data/certificates"
        / "kb-mca-v4-m2-r4-coordinate-positive-433-1b-cell14-complete-closure-v1"
        / (NAME + ".json"))

EXPECTED_NODES = (
    "rate_half_kb_m2_r4_coordinate_positive_433_1b_cell14_quadratic_curve_structure",
    "rate_half_kb_m2_r4_coordinate_positive_433_1b_cell14_linear_pair_outside_exclusion",
    "rate_half_kb_m2_r4_coordinate_positive_433_1b_cell14_rankone_target_projection_exclusion",
    "rate_half_kb_m2_r4_coordinate_positive_433_1b_cell14_fixed_a_rankone_chain_exclusion",
    "rate_half_kb_m2_r4_coordinate_positive_433_1b_cell14_fixed_a_rankone_allmixed_exclusion",
)


class Reject(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise Reject(message)


def pairings(values):
    """Canonical first-element recursive enumeration of perfect matchings."""
    values = tuple(values)
    if not values:
        yield ()
        return
    first = values[0]
    for index in range(1, len(values)):
        rest = values[1:index] + values[index + 1:]
        for tail in pairings(rest):
            yield ((first, values[index]),) + tail


def verify_matchings():
    matchings = tuple(pairings(range(6)))
    require(len(matchings) == 15, "fifteen matchings")
    require(len(set(matchings)) == 15, "matchings distinct")
    for matching in matchings:
        flat = sorted(x for pair in matching for x in pair)
        require(flat == list(range(6)), "each matching is perfect")
    paired01 = {i for i, m in enumerate(matchings) if (0, 1) in m}
    require(paired01 == {0, 1, 2}, "indices {0,1,2} are exactly the (0,1)-pairings")
    return matchings


def verify_census(cert):
    require(cert["deployed_prime"] == 2130706433, "deployed prime")
    require(cert["source_signs"] == 4 and cert["target_lanes"] == 4 and
            cert["missing_records"] == 7 and cert["matchings"] == 15,
            "atlas shape")
    require(cert["total_raw_cases"] == 4 * 4 * 7 * 15 == 1680, "raw ledger")
    require(len(cert["outside_records"]) == 7 and
            cert["outside_records"][:3] == ["de", "de", "-de"],
            "record list")
    families = cert["families"]
    require(len(families) == 4, "four families")
    seen = set()
    total = 0
    for family in families:
        roles = tuple(family["missing_roles"])
        idxs = tuple(family["matching_indices"])
        cases = family["cases"]
        require(cases == 4 * 4 * len(roles) * len(idxs), "family formula: " + family["family"])
        for role in roles:
            for idx in idxs:
                require((role, idx) not in seen, "overlap at " + str((role, idx)))
                seen.add((role, idx))
        total += cases
    require(total == 1680, "family totals")
    require(len(seen) == 7 * 15, "tiling covers every (role, matching) pair")
    require(seen == {(r, i) for r in range(7) for i in range(15)}, "exact tiling")
    by_name = {f["family"]: f for f in families}
    require(tuple(by_name["linear_pair"]["matching_indices"]) == (0, 1, 2),
            "linear-pair matchings are the (0,1)-pairings")
    require(set(by_name["linear_pair"]["missing_roles"]) ==
            set(by_name["fixed_a_rankone_chain"]["missing_roles"]) ==
            set(by_name["fixed_a_rankone_allmixed"]["missing_roles"]) == {0, 1, 2},
            "missing-de families")
    require(set(by_name["rankone_target_projection"]["missing_roles"]) == {3, 4, 5, 6},
            "non-de family")
    de_idx = (set(by_name["linear_pair"]["matching_indices"])
              | set(by_name["fixed_a_rankone_chain"]["matching_indices"])
              | set(by_name["fixed_a_rankone_allmixed"]["matching_indices"]))
    require(de_idx == set(range(15)), "missing-de matching classes tile all fifteen")


def verify_pins(cert):
    require(tuple(cert["pinned_nodes"]) == EXPECTED_NODES, "pinned node ids")
    nodes = {f["node"] for f in cert["families"]}
    nodes.add(cert["structural_theorem"]["node"])
    require(nodes == set(EXPECTED_NODES), "family/structural nodes match pins")
    prov = cert["provenance"]
    require(prov["canonical_repo"].endswith("rs-mca-prize-dag"), "canonical repo")
    for key in ("wave42_integration_commit", "wave43_integration_commit", "worker_pin"):
        require(len(prov[key]) >= 8, "provenance pin: " + key)
    require("WAVE42_AUDIT" in prov["audit_notes"] and
            "WAVE43_AUDIT" in prov["audit_notes"], "audit notes")
    require("not characteristic-uniform" in cert["nonclaim"] and
            "Prize" in cert["nonclaim"], "certificate nonclaim")


def verify_note():
    text = NOTE.read_text(encoding="utf-8")
    for marker in (
        "(KBP1B14C-0)", "(KBP1B14C-1)", "(KBP1B14C-2)",
        "de, de, -de, df, sigma_o ef, bf, sigma_c cf",
        "1,680 cases",
        "Retained frontier: **none**",
        "| kernel normalization (structural) |",
        "| linear-pair (144) |",
        "| rank-one (960) |",
        "| fixed-a chain (432) |",
        "| all-mixed (144) |",
        "not characteristic-uniform",
        "This closes **one role cell of one coordinate route**",
        "either Prize problem",
        "Cell 3 remains **open**",
        "F_2130706433",
    ):
        require(marker in text, "note marker: " + marker)


def main():
    verify_matchings()
    cert = json.loads(CERT.read_text(encoding="utf-8"))
    verify_census(cert)
    verify_pins(cert)
    verify_note()
    print("PASS " + NAME + ": matchings=15 classes=ok tiling=1680/1680 "
          "families=4 pins=5 note=ok")


if __name__ == "__main__":
    main()
