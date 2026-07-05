#!/usr/bin/env python3
"""Replay the QA.23 wild-row audit packet."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict, deque
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
NOTE = REPO / "experimental" / "notes" / "thresholds" / "wild_row_audit.md"
ARTIFACT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "wild-row-audit"
    / "wild_row_audit.json"
)

P = 7
INF = P
DOMAIN = tuple(range(P + 1))
ID = tuple(range(P + 1))

ANCHORS = {
    "status": "Status: PROVED / AUDIT.",
    "source_node": "wild_row_audit",
    "row_count": "There are `26` such `(n,q)` rows.",
    "dickson": "Dickson subgroup lattice of `PGL2(F_{n-1})`",
    "non_claim": "does not price every prize-scale Dickson window family",
}


def inv(a: int) -> int:
    return pow(a % P, P - 2, P)


def act_matrix(matrix: tuple[int, int, int, int], x: int) -> int:
    a, b, c, d = matrix
    if x == INF:
        return INF if c == 0 else a * inv(c) % P
    den = (c * x + d) % P
    if den == 0:
        return INF
    return (a * x + b) * inv(den) % P


def canonical_matrix(a: int, b: int, c: int, d: int) -> tuple[int, int, int, int]:
    vals = [a % P, b % P, c % P, d % P]
    scale = next(x for x in vals if x)
    s = inv(scale)
    return tuple((s * x) % P for x in vals)  # type: ignore[return-value]


def pgl2_group() -> list[tuple[int, ...]]:
    out = set()
    for a in range(P):
        for b in range(P):
            for c in range(P):
                for d in range(P):
                    if (a * d - b * c) % P == 0:
                        continue
                    matrix = canonical_matrix(a, b, c, d)
                    out.add(tuple(act_matrix(matrix, x) for x in DOMAIN))
    return sorted(out)


def compose(g: tuple[int, ...], h: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(g[h[i]] for i in DOMAIN)


def multiplication_table(group: list[tuple[int, ...]]) -> tuple[tuple[int, ...], ...]:
    index = {g: i for i, g in enumerate(group)}
    return tuple(tuple(index[compose(g, h)] for h in group) for g in group)


def inverse_table(mult: tuple[tuple[int, ...], ...], id_idx: int) -> tuple[int, ...]:
    out = []
    for g, row in enumerate(mult):
        out.append(next(h for h, gh in enumerate(row) if gh == id_idx and mult[h][g] == id_idx))
    return tuple(out)


def mask_iter(mask: int):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def subgroup_generated_mask(
    gens: tuple[int, ...],
    mult: tuple[tuple[int, ...], ...],
    invs: tuple[int, ...],
    id_idx: int,
) -> int:
    walk_gens = tuple(sorted(set(gens + tuple(invs[g] for g in gens))))
    mask = 1 << id_idx
    queue: deque[int] = deque([id_idx])
    while queue:
        h = queue.popleft()
        for g in walk_gens:
            gh = mult[g][h]
            bit = 1 << gh
            if not mask & bit:
                mask |= bit
                queue.append(gh)
    return mask


def all_subgroups_idx(
    group: list[tuple[int, ...]],
    mult: tuple[tuple[int, ...], ...],
    id_idx: int,
) -> list[int]:
    n = len(group)
    invs = inverse_table(mult, id_idx)
    subgroups = {1 << id_idx}
    subgroup_gens = {1 << id_idx: tuple()}

    def add_generated(gens: tuple[int, ...], queue: deque[int] | None = None) -> None:
        sub = subgroup_generated_mask(gens, mult, invs, id_idx)
        if sub not in subgroups:
            subgroups.add(sub)
            subgroup_gens[sub] = gens
            if queue is not None:
                queue.append(sub)

    for g in range(n):
        add_generated((g,))
    for g in range(n):
        for h in range(g, n):
            add_generated((g, h))

    queue = deque(sorted(subgroups, key=lambda sub: (sub.bit_count(), sub)))
    while queue:
        sub = queue.popleft()
        gens = subgroup_gens[sub]
        for g in range(n):
            if sub >> g & 1:
                continue
            add_generated(gens + (g,), queue)
    return sorted(subgroups, key=lambda sub: (sub.bit_count(), sub))


def orbits_idx(subgroup: int, group: list[tuple[int, ...]]) -> tuple[tuple[int, ...], ...]:
    remaining = set(DOMAIN)
    out = []
    while remaining:
        start = min(remaining)
        orbit = {group[g][start] for g in mask_iter(subgroup)}
        changed = True
        while changed:
            changed = False
            for x in list(orbit):
                for g in mask_iter(subgroup):
                    y = group[g][x]
                    if y not in orbit:
                        orbit.add(y)
                        changed = True
        out.append(tuple(sorted(orbit)))
        remaining -= orbit
    return tuple(sorted(out, key=lambda orbit: (len(orbit), orbit)))


def orbit_size_partition_idx(subgroup: int, group: list[tuple[int, ...]]) -> tuple[int, ...]:
    return tuple(sorted(len(orbit) for orbit in orbits_idx(subgroup, group)))


def subgroup_invariant_subsets_idx(subgroup: int, group: list[tuple[int, ...]]) -> set[int]:
    inv_subsets = set()
    for mask in range(1 << len(DOMAIN)):
        ok = True
        for g in mask_iter(subgroup):
            image = 0
            for i in DOMAIN:
                if mask >> i & 1:
                    image |= 1 << group[g][i]
            if image != mask:
                ok = False
                break
        if ok:
            inv_subsets.add(mask)
    return inv_subsets


def orbit_union_subsets_idx(subgroup: int, group: list[tuple[int, ...]]) -> set[int]:
    orbit_masks = []
    for orbit in orbits_idx(subgroup, group):
        mask = 0
        for i in orbit:
            mask |= 1 << i
        orbit_masks.append(mask)
    out = set()
    for choose in range(1 << len(orbit_masks)):
        mask = 0
        for j, orbit_mask in enumerate(orbit_masks):
            if choose >> j & 1:
                mask |= orbit_mask
        out.add(mask)
    return out


def element_order_idx(g: int, mult: tuple[tuple[int, ...], ...], id_idx: int) -> int:
    x = id_idx
    for r in range(1, 400):
        x = mult[g][x]
        if x == id_idx:
            return r
    raise AssertionError("element order too large")


def sylow2_subgroup_idx(
    group: list[tuple[int, ...]],
    mult: tuple[tuple[int, ...], ...],
    id_idx: int,
) -> int:
    invs = inverse_table(mult, id_idx)
    for g in range(len(group)):
        if element_order_idx(g, mult, id_idx) == 8:
            for h in range(len(group)):
                subgroup = subgroup_generated_mask((g, h), mult, invs, id_idx)
                if subgroup.bit_count() == 16:
                    return subgroup
    raise AssertionError("no Sylow-2 subgroup found")


def admissible_wild_rows() -> list[dict[str, object]]:
    rows = []
    for r in (13, 17, 19, 31):
        p = (1 << r) - 1
        n = 1 << r
        s = 1
        while p ** (2 * s) < (1 << 256):
            rows.append(
                {
                    "r": r,
                    "n": n,
                    "mersenne_p": p,
                    "extension_degree": 2 * s,
                    "q": str(p ** (2 * s)),
                    "log2_q_upper": 2 * s * r,
                    "wild_reason": "mu_n is the norm-one/subfield circle over F_p inside F_{p^2}; cosets are dilation-conjugate",
                }
            )
            s += 1
    return rows


def window_summary(subgroups: list[int], group: list[tuple[int, ...]]) -> dict[str, object]:
    partitions: dict[tuple[int, ...], set[int]] = defaultdict(set)
    subsets_by_size: dict[int, set[int]] = defaultdict(set)
    for subgroup in subgroups:
        part = orbit_size_partition_idx(subgroup, group)
        partitions[part].add(subgroup.bit_count())
        for mask in orbit_union_subsets_idx(subgroup, group):
            subsets_by_size[mask.bit_count()].add(mask)
    return {
        "orbit_partitions": [
            {"partition": list(part), "subgroup_orders": sorted(orders)}
            for part, orders in sorted(partitions.items())
        ],
        "distinct_invariant_subsets_by_size": {
            str(size): len(subsets) for size, subsets in sorted(subsets_by_size.items())
        },
    }


def compute_payload() -> dict[str, object]:
    rows = admissible_wild_rows()
    expected_counts = {13: 9, 17: 7, 19: 6, 31: 4}
    got_counts: dict[int, int] = defaultdict(int)
    for row in rows:
        got_counts[int(row["r"])] += 1
    if dict(got_counts) != expected_counts:
        raise AssertionError(got_counts)
    if not all(row["wild_reason"] for row in rows):
        raise AssertionError("missing wildness reason")

    group = pgl2_group()
    id_idx = {g: i for i, g in enumerate(group)}[ID]
    mult = multiplication_table(group)
    if len(group) != 336 or len(group) != 8 * 7 * 6:
        raise AssertionError("PGL2(F7) action check failed")
    subgroups = all_subgroups_idx(group, mult, id_idx)
    if not (subgroups[0].bit_count() == 1 and subgroups[-1].bit_count() == 336):
        raise AssertionError("subgroup endpoints missing")
    if len(subgroups) != 413:
        raise AssertionError(len(subgroups))

    bad = 0
    for subgroup in subgroups:
        if subgroup_invariant_subsets_idx(subgroup, group) != orbit_union_subsets_idx(
            subgroup, group
        ):
            bad += 1
    if bad:
        raise AssertionError("invariant subsets not orbit unions")

    sylow = sylow2_subgroup_idx(group, mult, id_idx)
    if sylow.bit_count() != 16:
        raise AssertionError("bad Sylow-2 subgroup size")
    dihedral_subgroups = [subgroup for subgroup in subgroups if subgroup & ~sylow == 0]
    if not (0 < len(dihedral_subgroups) < len(subgroups)):
        raise AssertionError("dihedral lattice comparison failed")

    wild_windows = window_summary(subgroups, group)
    tame_windows = window_summary(dihedral_subgroups, group)
    wild_parts = {tuple(item["partition"]) for item in wild_windows["orbit_partitions"]}
    tame_parts = {tuple(item["partition"]) for item in tame_windows["orbit_partitions"]}
    new_parts = sorted(wild_parts - tame_parts)
    if not new_parts:
        raise AssertionError("no new wild partitions found")

    note_text = NOTE.read_text(encoding="utf-8")
    anchor_checks = {
        "note_exists": NOTE.exists(),
        **{name: needle in note_text for name, needle in ANCHORS.items()},
    }
    failed_anchors = [name for name, ok in anchor_checks.items() if not ok]
    if failed_anchors:
        raise AssertionError(f"failed anchors: {failed_anchors}")

    return {
        "schema": "wild-row-audit-v1",
        "node": "wild_row_audit",
        "task": "QA.23",
        "status": "PROVED_AUDIT",
        "anchor_checks": anchor_checks,
        "admissible_wild_rows": rows,
        "expected_counts_by_r": {str(key): value for key, value in expected_counts.items()},
        "total_wild_rows": len(rows),
        "coset_inheritance": "Every alpha*mu_n is dilation-conjugate to mu_n, so the PGL2 stabilizer is conjugate and wildness is inherited by every coset.",
        "pgl2_f7": {
            "group_order": len(group),
            "subgroup_count": len(subgroups),
            "dihedral_sylow2_subgroup_count": len(dihedral_subgroups),
            "wild_window_summary": wild_windows,
            "tame_dihedral_window_summary": tame_windows,
            "new_wild_orbit_partitions": [list(part) for part in new_parts],
            "interpretation": "At the F49/mu8 toy, enlarged Dickson symmetry gives invariant window strata not present in a tame dihedral subgroup lattice.",
        },
        "checks": {
            "pgl2_order": True,
            "pgl2_sharp_3_transitive_count": True,
            "subgroup_count_413": True,
            "invariant_subsets_are_orbit_unions": True,
            "wild_has_extra_partitions": True,
        },
        "non_claims": [
            "does not price every prize-scale Dickson window family",
            "does not close a wild-row adjacent upper certificate",
            "does not alter Papers A-D",
        ],
        "note": "experimental/notes/thresholds/wild_row_audit.md",
    }


def validate(payload: dict[str, object]) -> None:
    if payload.get("schema") != "wild-row-audit-v1":
        raise AssertionError("unexpected schema")
    if payload.get("node") != "wild_row_audit":
        raise AssertionError("node mismatch")
    if payload.get("status") != "PROVED_AUDIT":
        raise AssertionError("status mismatch")
    if payload.get("total_wild_rows") != 26:
        raise AssertionError("wild-row count mismatch")
    anchors = payload.get("anchor_checks")
    if not isinstance(anchors, dict) or not all(anchors.values()):
        raise AssertionError("anchor checks failed")
    pgl = payload.get("pgl2_f7")
    if not isinstance(pgl, dict):
        raise AssertionError("missing PGL2 block")
    if pgl.get("group_order") != 336 or pgl.get("subgroup_count") != 413:
        raise AssertionError("PGL2 summary mismatch")
    if pgl.get("dihedral_sylow2_subgroup_count") != 19:
        raise AssertionError("dihedral subgroup count mismatch")


def assert_same(expected: dict[str, object], actual: dict[str, object]) -> None:
    if expected != actual:
        raise AssertionError(
            "certificate mismatch\nexpected:\n"
            + json.dumps(expected, indent=2, sort_keys=True)
            + "\nactual:\n"
            + json.dumps(actual, indent=2, sort_keys=True)
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true")
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()

    payload = compute_payload()
    validate(payload)
    if args.emit:
        ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
        ARTIFACT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
        print(f"wrote {ARTIFACT.relative_to(REPO)}")
    if args.check:
        actual = json.loads(args.check.read_text(encoding="utf-8"))
        validate(actual)
        assert_same(payload, actual)
        print(f"checked {args.check}")
    if not args.emit and not args.check:
        print(f"{payload['status']}: {payload['node']} ({payload['total_wild_rows']} rows)")


if __name__ == "__main__":
    main()
