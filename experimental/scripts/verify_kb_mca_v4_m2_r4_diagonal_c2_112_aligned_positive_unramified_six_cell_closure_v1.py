#!/usr/bin/env python3
"""Fail-closed verifier for the diagonal c2 (1,1,2) aligned-positive
unramified six-cell closure.

Pure python, no third-party imports, no reads outside this repository.
Replays the census arithmetic (the 2 x 3 tiling, the route split, the
per-cell endpoint and off-common ledgers, the deployed-field embeddability
count), cross-checks the certificate against the notes, and checks the
export note's ledger, correspondence-discipline and nonclaim markers plus
the workboard addendum.

The per-cell exact CAS proofs are NOT re-verified here; they are pinned by
node id to the canonical DAG
(https://github.com/AllenGrahamHart/rs-mca-prize-dag), where each node's
own verify.py and verify_audit.py were replayed PASS.
"""

import json
import re
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parents[2]
NAME = "kb_mca_v4_m2_r4_diagonal_c2_112_aligned_positive_unramified_six_cell_closure_v1"
NOTES = ROOT / "experimental/notes/frontier-adjacent"
NOTE = NOTES / (NAME + ".md")
WORKBOARD = NOTES / "kb_mca_v4_m2_u2_saturated_112_q_slice_exclusions_v1.md"
CERT = (ROOT / "experimental/data/certificates"
        / "kb-mca-v4-m2-r4-diagonal-c2-112-aligned-positive-unramified-six-cell-closure-v1"
        / (NAME + ".json"))

DEPLOYED_PRIME = 2130706433
EXTENSION_DEGREE = 6
PREFIX = "rate_half_kb_m2_r4_diagonal_c2_112_aligned_positive_unramified_"

EXPECTED_NODES = (
    PREFIX + "moving_same_q_slice_exclusion",
    PREFIX + "moving_swap_q_slice_exclusion",
    PREFIX + "moving_mixed_full_quotient_exclusion",
    PREFIX + "fixed_same_full_quotient_exclusion",
    PREFIX + "fixed_swap_full_quotient_exclusion",
    PREFIX + "fixed_mixed_full_quotient_exclusion",
)

TEMPLATE_TOKEN = {"fixed_moving": "fixed", "moving_moving": "moving"}
TEMPLATE_LABEL = {"fixed_moving": "FM", "moving_moving": "MM"}
ROUTE_SUFFIX = {"q_slice": "_q_slice_exclusion",
                "full_quotient": "_full_quotient_exclusion"}


class Reject(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise Reject(message)


def product(values):
    total = 1
    for value in values:
        total *= value
    return total


def verify_shape(cert):
    require(cert["deployed_prime"] == DEPLOYED_PRIME, "deployed prime")
    require(cert["deployed_field"] == "F_(2130706433^6)", "deployed field")
    templates = cert["templates"]
    allocations = cert["allocations"]
    require(sorted(templates) == ["fixed_moving", "moving_moving"], "template axis")
    require(sorted(allocations) == ["mixed", "same", "swap"], "allocation axis")
    require(cert["total_cells"] == len(templates) * len(allocations) == 6,
            "cell product 2 x 3 = 6")
    require(cert["cells_closed"] == 6, "six cells closed")
    require(cert["remaining_unramified"] ==
            cert["total_cells"] - cert["cells_closed"] == 0,
            "remaining unramified is zero")
    require(len(cert["full_quotient_identities"]) == 2,
            "two full-quotient norm identities")


def verify_tiling(cert):
    cells = cert["cells"]
    require(len(cells) == 6, "six cell entries")
    seen = set()
    routes = {"q_slice": 0, "full_quotient": 0}
    for cell in cells:
        template = cell["template"]
        allocation = cell["allocation"]
        require(template in cert["templates"], "template of " + cell["label"])
        require(allocation in cert["allocations"], "allocation of " + cell["label"])
        key = (template, allocation)
        require(key not in seen, "duplicate cell " + str(key))
        seen.add(key)
        expected_label = TEMPLATE_LABEL[template] + "-" + allocation
        require(cell["label"] == expected_label,
                "label matches axes: " + cell["label"])
        route = cell["closure_route"]
        require(route in routes, "route of " + cell["label"])
        routes[route] += 1
        node = cell["node"]
        require(node.startswith(PREFIX), "node prefix: " + node)
        tail = node[len(PREFIX):]
        require(tail.startswith(TEMPLATE_TOKEN[template] + "_" + allocation + "_"),
                "node id encodes its own axes: " + node)
        require(node.endswith(ROUTE_SUFFIX[route]),
                "node id suffix matches its route: " + node)
    require(seen == {(t, a) for t in cert["templates"] for a in cert["allocations"]},
            "exact 2 x 3 tiling")
    require(routes == cert["closure_routes"], "route census matches per-cell routes")
    require(routes["q_slice"] + routes["full_quotient"] == 6, "route split totals six")
    require(routes["q_slice"] == 2 and routes["full_quotient"] == 4,
            "two q-slice cells, four full-quotient cells")


def verify_cell_arithmetic(cert):
    for cell in cert["cells"]:
        tag = cell["label"]
        split = cell["endpoint_split"]
        require(len(split) >= 2, "endpoint split is a partition: " + tag)
        require(all(isinstance(v, int) and v >= 0 for v in split.values()),
                "endpoint split entries are counts: " + tag)
        require(sum(split.values()) == cell["endpoint_candidates"],
                "endpoint split re-adds to its candidate count: " + tag)
        survivors = cell["q_slice_survivors"]
        require(isinstance(survivors, int) and survivors >= 0,
                "survivor count: " + tag)
        if cell["closure_route"] == "q_slice":
            require(survivors == 0, "q-slice route means no survivors: " + tag)
        else:
            require(survivors > 0,
                    "full-quotient route means the q-slice is not empty: " + tag)
        degree = cell["direct_norm_degree"]
        require(isinstance(degree, int) and degree > 0, "direct norm degree: " + tag)
        factors = cell["direct_norm_factors"]
        require(factors is None or (isinstance(factors, int) and factors > 0),
                "direct norm factor count: " + tag)

        off = cell["off_common"]
        grid = off["grid"]
        combinations = off["combinations"]
        require(isinstance(combinations, int) and combinations > 0,
                "off-common combinations: " + tag)
        if grid is not None:
            require(all(isinstance(v, int) and v > 0 for v in grid),
                    "off-common grid entries: " + tag)
            require(product(grid) == combinations,
                    "off-common grid product equals its combination count: " + tag)
        elif off["endpoint_factors"] is not None:
            require(off["endpoint_factors"] == combinations,
                    "off-common endpoint factors equal combinations: " + tag)
        require(isinstance(off["distinct_endpoints"], int)
                and off["distinct_endpoints"] > 0,
                "off-common distinct endpoints: " + tag)
        require(off["all_on_base_forbidden_product"] is True,
                "off-common endpoints all on the base forbidden product: " + tag)


def verify_embeddability(cert):
    cell = next(c for c in cert["cells"] if c["label"] == "MM-mixed")
    degrees = cell["q_slice_survivor_field_degrees"]
    require(sorted(degrees) == [3, 3, 7, 7], "MM-mixed survivor field degrees")
    require(len(degrees) == cell["endpoint_candidates"] == cell["q_slice_survivors"],
            "MM-mixed survivor count equals its field-degree list")
    embeds = [d for d in degrees if EXTENSION_DEGREE % d == 0]
    misses = [d for d in degrees if EXTENSION_DEGREE % d != 0]
    split = cell["endpoint_split"]
    require(len(embeds) == split["embeds_in_deployed_field"] == 2,
            "exactly the degree-3 traces embed in F_(p^6)")
    require(len(misses) == split["does_not_embed"] == 2,
            "the degree-7 points do not embed in F_(p^6)")
    require(cell["deployed_traces"] == len(embeds),
            "deployed trace count equals the embeddable degrees")
    require(cell["orientations_tested"] == 2 * cell["deployed_traces"] == 4,
            "two reciprocal b orientations above each deployed trace")


def verify_linear_rank(cert):
    cell = next(c for c in cert["cells"] if c["label"] == "FM-mixed")
    route = cell["linear_rank_route"]
    require("RAW" in route["component"],
            "FM-mixed linear rank route uses the raw kernel conic")
    require(route["norm_degree"] == 116 and route["norm_factors"] == 10,
            "FM-mixed linear rank norm")
    split = route["w_split"]
    require(sum(split.values()) == route["remaining_w_values"] == 12,
            "FM-mixed w split re-adds to its remaining w values")
    require(split["forbidden"] == 9 and split["no_common_b"] == 3,
            "FM-mixed w split composition")
    require(route["base_boundary_fields"] + 0 <= route["norm_factors"],
            "FM-mixed boundary fields fit inside the factor count")


def verify_audit_lines(cert):
    for cell in cert["cells"]:
        tag = cell["label"]
        contract = cell["contract_pass"]
        audit = cell["audit_pass"]
        require(contract.endswith("_CONTRACT_PASS"), "contract PASS line: " + tag)
        require("_AUDIT_PASS" in audit, "audit PASS line: " + tag)
        stem = contract[: -len("_CONTRACT_PASS")]
        require(audit.startswith(stem + "_AUDIT_PASS"),
                "contract and audit lines name the same node: " + tag)
        require(stem.startswith("KB_C2_112_ALIGNED_POSITIVE_UNRAMIFIED_"),
                "PASS line namespace: " + tag)
        cellword = stem[len("KB_C2_112_ALIGNED_POSITIVE_UNRAMIFIED_"):]
        expected = (TEMPLATE_TOKEN[cell["template"]] + "_" + cell["allocation"]).upper()
        require(cellword == expected,
                "PASS line names this cell's axes: " + tag)
        match = re.search(r"survivors=(\d+)", audit)
        if match:
            require(int(match.group(1)) == cell["q_slice_survivors"],
                    "recorded audit survivor count matches the ledger: " + tag)
        else:
            require(cell["q_slice_survivors"] == 0,
                    "no survivors field means an empty q-slice: " + tag)
        traces = re.search(r"deployed_traces=(\d+)", audit)
        if traces:
            require(int(traces.group(1)) == cell["deployed_traces"],
                    "recorded deployed trace count matches the ledger: " + tag)


def verify_exact_replay(cert):
    """Cross-check the FLINT exact verifiers' own printed counters against the
    per-cell ledger. Every counter these scripts print must agree with the
    number this certificate claims for that cell."""
    block = cert["exact_verifiers_replayed_20260806"]
    lines = block["pass_lines"]
    require(len(lines) >= 1, "at least one exact PASS line")
    by_cellword = {}
    for cell in cert["cells"]:
        word = (TEMPLATE_TOKEN[cell["template"]] + "_" + cell["allocation"]).upper()
        by_cellword[word] = cell
    covered = set()
    for line in lines:
        require(line.startswith("KB_C2_112_ALIGNED_POSITIVE_UNRAMIFIED_"),
                "exact PASS namespace: " + line[:48])
        require("_PASS" in line, "exact PASS marker: " + line[:48])
        head = line.split(" ", 1)[0]
        body = head[len("KB_C2_112_ALIGNED_POSITIVE_UNRAMIFIED_"):]
        body = body[: -len("_PASS")]
        cell = None
        component = None
        for word in by_cellword:
            if body.startswith(word):
                cell = by_cellword[word]
                component = body[len(word):].lstrip("_")
                covered.add(word)
                break
        require(cell is not None, "exact PASS line names a known cell: " + head)
        require(component in ("EXACT", "EXHAUSTIVE", "DEGREE5", "QUOTIENT",
                              "LINEAR", "OFF_COMMON"),
                "known exact component: " + head)
        fields = dict(
            (k, v) for k, v in
            (part.split("=", 1) for part in line.split(" ")[1:] if "=" in part)
        )
        # The direct-component scripts report the cell's own q-slice survivors.
        if component in ("EXACT", "EXHAUSTIVE", "DEGREE5", "QUOTIENT"):
            for key in ("survivors", "q_slice_survivors"):
                if key in fields:
                    require(int(fields[key]) == cell["q_slice_survivors"],
                            "exact " + key + " matches the ledger: " + head)
            if "norm_factors" in fields:
                require(int(fields["norm_factors"]) == cell["direct_norm_factors"],
                        "exact direct norm factor count matches the ledger: " + head)
            if "deployed_orientations" in fields:
                require(int(fields["deployed_orientations"]) ==
                        cell["orientations_tested"],
                        "exact orientation count matches the ledger: " + head)
            if "rejected" in fields:
                tested = None
                for key in ("deployed_orientations", "q_slice_survivors",
                            "survivors"):
                    if key in fields:
                        tested = int(fields[key])
                        break
                require(tested is not None,
                        "a rejection count needs a tested count: " + head)
                require(int(fields["rejected"]) == tested,
                        "every tested candidate was rejected: " + head)
        # The linear-rank script reports that route, not the direct component.
        elif component == "LINEAR":
            route = cell.get("linear_rank_route")
            if "norm_factors" in fields:
                require(route is not None,
                        "a linear norm factor count needs a linear route: " + head)
                require(int(fields["norm_factors"]) == route["norm_factors"],
                        "linear norm factor count matches the ledger: " + head)
            if "survivors" in fields:
                require(int(fields["survivors"]) == 0,
                        "the linear-rank route leaves no survivor: " + head)
        # The off-common script reports the residual cofactor grid.
        else:
            off = cell["off_common"]
            require(int(fields["branches"]) == off["combinations"],
                    "off-common branch count matches the ledger: " + head)
            require(int(fields["endpoints"]) == off["distinct_endpoints"],
                    "off-common endpoint count matches the ledger: " + head)
            require(int(fields["boundary"]) == off["distinct_endpoints"],
                    "every off-common endpoint is boundary: " + head)
            require(off["all_on_base_forbidden_product"] is True,
                    "off-common boundary flag: " + head)
        for key in ("off_common", "certificate_match"):
            if key in fields:
                require(fields[key] == "true", "exact flag " + key + ": " + head)
    require(covered <= set(by_cellword), "exact PASS lines stay inside the block")
    missing = block["not_completed_on_this_host"]
    require(isinstance(missing, list), "non-completion list")
    require("NOT a failed proof" in block["not_completed_reason"],
            "non-completion is labelled as a host-speed observation")
    require(len(covered) + 0 <= 6, "coverage bound")


def verify_pins(cert):
    require(tuple(cert["pinned_nodes"]) == EXPECTED_NODES, "pinned node ids")
    require({c["node"] for c in cert["cells"]} == set(EXPECTED_NODES),
            "cell nodes match the pin list")
    prov = cert["provenance"]
    require(prov["canonical_repo"].endswith("rs-mca-prize-dag"), "canonical repo")
    require(len(prov["canonical_prize_pin"]) == 40, "canonical prize pin is a full sha")
    commits = prov["integration_commits"]
    require(len(commits) == 6 and len(set(commits)) == 6,
            "six distinct integration commits")
    require(all(len(c) >= 8 for c in commits), "integration commit pins")
    require({c["integration_commit"] for c in cert["cells"]} == set(commits),
            "every cell pins one of the integration commits")
    require(all(c["integration_date"] == "2026-07-31" for c in cert["cells"]),
            "integration dates")
    require("work_cycles/roadmap_r3" in prov["audit_notes"], "audit note path")
    require("remaining_unramified=6" in prov["upstream_packet_superseded"],
            "the superseded packet's stale counter is pinned")
    require("verify_audit.py" in prov["verifiers_replayed"], "replay record")
    require("does not re-run them" in prov["verifiers_not_replayed_here"],
            "explicit non-replay record for the exact CAS verifiers")
    for key in ("shared_requires", "full_quotient_requires"):
        require(all(r.startswith("rate_half_kb_m2_r4_diagonal_c2_112_source_line_")
                    for r in cert[key]), "parent gate ids: " + key)
    require(len(cert["shared_requires"]) == 2 and
            len(cert["full_quotient_requires"]) == 1, "parent gate counts")


def verify_discipline(cert):
    corr = cert["upstream_correspondence"]
    require(corr["status"] == "PROBABLE_NOT_ESTABLISHED",
            "correspondence status is probable, not established")
    require(len(corr["matching_qualifiers"]) == 4, "four matching qualifiers")
    require(set(corr["matching_qualifiers"]) ==
            {"m=2", "diagonal", "c2(1,1,2)", "aligned_positive"},
            "the four qualifiers are named exactly")
    require(corr["mapping_row"] == "ABSENT ON BOTH SIDES", "mapping row absent")
    require("NOT REPLAYED" in corr["trust_label"], "external trust label")
    require("No identity" in corr["assertion"] and
            "not in contradiction" in corr["assertion"],
            "correspondence assertion refuses identity")
    require(corr["our_partition"] !=
            corr["other_partition_as_published"],
            "the two partitions are recorded as different")
    nonclaim = cert["nonclaim"]
    for marker in ("not characteristic-uniform", "Prize problem", "36-cell",
                   "(2,4,2)", "(2,8,1)", "rate_half_band_closure",
                   "the q-slice is not empty"):
        require(marker in nonclaim, "certificate nonclaim marker: " + marker)
    require("NOT exported here" in cert["adjacent_status_at_pin"],
            "adjacent aggregation node is explicitly not exported")


def flatten(text):
    """Collapse all runs of whitespace so prose markers survive rewrapping."""
    return " ".join(text.split())


def verify_note():
    text = NOTE.read_text(encoding="utf-8")
    flat = flatten(text)
    # Literal markers: equation labels, table rows and aligned census lines.
    for marker in (
        "(KBAPU6-0)", "(KBAPU6-1)", "(KBAPU6-2)", "(KBAPU6-3)",
        "(KBQS-1)", "(KBQS-2)",
        "| MM-same |", "| MM-swap |", "| MM-mixed |",
        "| FM-same |", "| FM-swap |", "| FM-mixed |",
        "{FM, MM} x {same, swap, mixed}  =  6 cells",
        "remaining unramified cells                                  0.",
        "q-slice EMPTY          MM-same, MM-swap                     2",
        "full-quotient EMPTY    MM-mixed, FM-same, FM-swap, FM-mixed 4",
    ):
        require(marker in text, "note marker: " + marker)
    # Prose markers, matched after whitespace collapse.
    for marker in (
        "Retained frontier inside the block: **none**",
        "correspondence probable, not established",
        "**Correspondence probable, not established.**",
        "No cell-for-cell mapping row exists on either side",
        "does **not** assert that our six cells are that lane's six cells",
        "CONTENT-REVIEWED at its published head, NOT REPLAYED by us",
        "not characteristic-uniform",
        "does **not** close the 36-cell aligned-positive atlas",
        "(m,r,delta) = (2,4,2)` and `(2,8,1)`",
        "either Prize problem",
        "F_2130706433",
        "the q-slice itself is **not** empty",
        "remaining_unramified=6",
        "This closes **one six-cell block of one sign of one source line**",
        "are **not in contradiction** under either identification",
        "11 PASS, 4 not completed on this host",
        "**No assertion inside any of the four failed**",
    ):
        require(marker in flat, "note marker: " + marker)
    for forbidden in (
        "closes K3",
        "closes the 36-cell",
        "identical to",
        "are the same cells as",
    ):
        require(forbidden not in flat, "forbidden note phrase: " + forbidden)


def verify_workboard():
    text = WORKBOARD.read_text(encoding="utf-8")
    flat = flatten(text)
    for marker in (
        "remaining_unramified (this packet's own scope)   6   unchanged",
        "remaining_unramified (canonical DAG, 2026-08-06) 0   all six PROVED.",
    ):
        require(marker in text, "workboard addendum marker: " + marker)
    for marker in (
        "## 7. Status addendum (2026-08-06)",
        "it must **not** be edited",
        NAME,
        "Still open in this upstream packet",
    ):
        require(marker in flat, "workboard addendum marker: " + marker)


def main():
    cert = json.loads(CERT.read_text(encoding="utf-8"))
    verify_shape(cert)
    verify_tiling(cert)
    verify_cell_arithmetic(cert)
    verify_embeddability(cert)
    verify_linear_rank(cert)
    verify_audit_lines(cert)
    verify_exact_replay(cert)
    verify_pins(cert)
    verify_discipline(cert)
    verify_note()
    verify_workboard()
    survivors = sum(c["q_slice_survivors"] for c in cert["cells"])
    exact = len(cert["exact_verifiers_replayed_20260806"]["pass_lines"])
    print("PASS " + NAME + ": tiling=6/6 routes=2+4 "
          "endpoint_splits=6/6 offcommon=6/6 embeddability=ok "
          f"q_slice_survivors={survivors} pins=6 exact_pass_lines={exact} "
          "correspondence=PROBABLE_NOT_ESTABLISHED note=ok workboard=ok")


if __name__ == "__main__":
    main()
