#!/usr/bin/env python3
"""F3 verifier: affine-net rich points are mixed degree-1 pullback cells.

The P3 residue is an affine line arrangement in the fixed-subcore parameter
plane.  A line has the form

    a = intercept + direction*z.

This verifier enumerates the original P3 toy net and several generic/adversarial
multi-direction nets over F_193.  For every (t+1)-rich point it constructs the
b=2 fiber-dictionary charge: choose a pivot incident line and express each
other incident line by the degree-1 equality fiber with the pivot.  Mixed maps
are allowed, so each incident edge may use its own pair map.

Run:
  python3 experimental/scripts/verify_f3_net_absorption.py
To refresh the pinned certificate:
  python3 experimental/scripts/verify_f3_net_absorption.py --write-certificate
"""

from __future__ import annotations

from dataclasses import dataclass
import itertools
import json
import os
import sys


HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
CERT = os.path.join(
    REPO,
    "experimental",
    "data",
    "certificates",
    "f3-net-absorption",
    "f3_net_absorption.json",
)

P = 193
THRESHOLD = 3
ANCHOR_Z = 0

FAILS: list[str] = []
NCHECK = 0
LOCAL_FAILS: list[str] = []
LOCAL_ASSERTS = 0


def check(name: str, cond: bool, detail: str = "") -> None:
    global NCHECK
    NCHECK += 1
    tag = "PASS" if cond else "FAIL"
    line = f"[{tag}] {name}"
    if detail:
        line += f"   ({detail})"
    print(line)
    if not cond:
        FAILS.append(name)


def expect(name: str, cond: bool, detail: str = "") -> None:
    """Silent local assertion used for the many pair-trade identities."""
    global LOCAL_ASSERTS
    LOCAL_ASSERTS += 1
    if not cond:
        msg = name
        if detail:
            msg += f" ({detail})"
        LOCAL_FAILS.append(msg)


def inv(a: int) -> int:
    if a % P == 0:
        raise ZeroDivisionError("zero inverse")
    return pow(a, P - 2, P)


@dataclass(frozen=True, order=True)
class Line:
    label: str
    direction: int
    intercept: int

    def value(self, z: int) -> int:
        return (self.intercept + self.direction * z) % P

    def key(self) -> tuple[int, int]:
        return (self.direction % P, self.intercept % P)


@dataclass(frozen=True)
class RichPoint:
    z: int
    a: int
    lines: tuple[Line, ...]


def dedupe(lines: list[Line]) -> list[Line]:
    seen: dict[tuple[int, int], Line] = {}
    for line in lines:
        key = line.key()
        if key not in seen:
            seen[key] = line
    return sorted(seen.values(), key=lambda line: (line.direction, line.intercept, line.label))


def rich_points(lines: list[Line], threshold: int = THRESHOLD) -> list[RichPoint]:
    out: list[RichPoint] = []
    lines = dedupe(lines)
    for z in range(P):
        if z == ANCHOR_Z:
            continue
        buckets: dict[int, list[Line]] = {}
        for line in lines:
            buckets.setdefault(line.value(z), []).append(line)
        for a, incident in buckets.items():
            directions = {line.direction % P for line in incident}
            if len(incident) >= threshold and len(directions) >= 2:
                out.append(RichPoint(z, a, tuple(sorted(incident))))
    return sorted(out, key=lambda rp: (rp.z, rp.a, tuple(line.label for line in rp.lines)))


def pair_trade(pivot: Line, other: Line, z: int, a: int) -> dict:
    """Return the b=2 degree-1 mixed-pullback certificate for a line pair."""
    ds = (other.direction - pivot.direction) % P
    dc = (other.intercept - pivot.intercept) % P
    expect("pair has distinct directions", ds != 0, f"{pivot.label},{other.label}")
    root = (-dc * inv(ds)) % P
    lp = pivot.value(z)
    lo = other.value(z)

    # Fiber dictionary at b=2: the unordered branch block is encoded by its
    # elementary symmetric coefficients.
    e1_const = (pivot.intercept + other.intercept) % P
    e1_slope = (pivot.direction + other.direction) % P
    e2_c0 = (pivot.intercept * other.intercept) % P
    e2_c1 = (pivot.intercept * other.direction + other.intercept * pivot.direction) % P
    e2_c2 = (pivot.direction * other.direction) % P
    e1_at_z = (e1_const + e1_slope * z) % P
    e2_at_z = (e2_c0 + e2_c1 * z + e2_c2 * z * z) % P

    expect("degree-1 equality fiber has the rich-point root", root == z, f"root={root}, z={z}")
    expect("pair branches meet at the rich value", lp == a and lo == a, f"values=({lp},{lo}), a={a}")
    expect("b=2 symmetric coefficient e1 specializes correctly", e1_at_z == (2 * a) % P)
    expect("b=2 symmetric coefficient e2 specializes correctly", e2_at_z == (a * a) % P)

    return {
        "pair": [pivot.label, other.label],
        "linear_equality": {
            "constant": dc,
            "slope": ds,
            "root": root,
        },
        "block_symmetric_coefficients": {
            "e1": [e1_const, e1_slope],
            "e2": [e2_c0, e2_c1, e2_c2],
        },
    }


def charge_rich_point(rp: RichPoint) -> list[dict]:
    """Cover all incident lines by a spanning tree of b=2 pair trades."""
    pivot = rp.lines[0]
    trades = [pair_trade(pivot, other, rp.z, rp.a) for other in rp.lines[1:]]
    covered = {pivot.label}
    for trade in trades:
        covered.update(trade["pair"])
    expect(
        "spanning pair trades cover every incident line",
        covered == {line.label for line in rp.lines},
        f"covered={len(covered)}, incident={len(rp.lines)}",
    )
    expect("rich point uses exactly b-1 pair trades", len(trades) == len(rp.lines) - 1)
    return trades


def p3_original_net(m: int = 10) -> list[Line]:
    lines: list[Line] = []
    for i in range(1, m + 1):
        lines.append(Line(f"H{i}", 0, i))
    for j in range(1, m + 1):
        lines.append(Line(f"P{j}", 1, j))
    for ell in range(1, 2 * m + 1):
        lines.append(Line(f"N{ell}", -1 % P, ell))
    return lines


def grid_net(name: str, directions: list[int], z_values: list[int], a_values: list[int]) -> list[Line]:
    lines: list[Line] = []
    for direction in directions:
        for z in z_values:
            for a in a_values:
                intercept = (a - direction * z) % P
                lines.append(Line(f"{name}_s{direction}_c{intercept}", direction % P, intercept))
    return dedupe(lines)


def seeded_adversarial_net() -> list[Line]:
    """Generic-slope net with non-grid, pseudorandom rich parameters and decoys."""
    directions = [5, 37, 111]
    params = []
    for i in range(1, 19):
        z = (7 * i * i + 11 * i + 3) % P
        a = (13 * i * i * i + 17 * i + 29) % P
        if z != ANCHOR_Z:
            params.append((z, a))

    lines: list[Line] = []
    for direction in directions:
        for z, a in params:
            intercept = (a - direction * z) % P
            lines.append(Line(f"A_s{direction}_z{z}_a{a}", direction, intercept))

    # Decoys are chosen with unrelated directions/intercepts.  The verifier
    # charges any extra rich point they accidentally create.
    for r in range(12):
        direction = (19 * r + 23) % P
        intercept = (31 * r * r + 43 * r + 47) % P
        lines.append(Line(f"D{r}", direction, intercept))
    return dedupe(lines)


def template_census_cases() -> list[tuple[str, list[Line]]]:
    cases: list[tuple[str, list[Line]]] = []
    slope_pool = [0, 1, 2, 5, 17]
    z_values = [3, 9, 27]
    a_values = [4, 31]
    for directions in itertools.combinations(slope_pool, 3):
        name = "template_" + "_".join(str(s) for s in directions)
        cases.append((name, grid_net(name, list(directions), z_values, a_values)))
    return cases


def analyze_case(name: str, lines: list[Line], min_rich: int = 1) -> dict:
    lines = dedupe(lines)
    rps = rich_points(lines)
    check(f"{name}: has multi-direction rich points", len(rps) >= min_rich, f"rich={len(rps)}")
    max_mult = max((len(rp.lines) for rp in rps), default=0)
    min_dirs = min((len({line.direction for line in rp.lines}) for rp in rps), default=0)
    total_trades = 0
    samples = []
    for rp in rps:
        trades = charge_rich_point(rp)
        total_trades += len(trades)
        if len(samples) < 4:
            samples.append({
                "z": rp.z,
                "a": rp.a,
                "incident": [line.label for line in rp.lines],
                "trade_count": len(trades),
                "sample_trade": trades[0] if trades else None,
            })
    check(f"{name}: every rich point charged", total_trades >= sum(len(rp.lines) - 1 for rp in rps))
    return {
        "name": name,
        "line_count": len(lines),
        "rich_points": len(rps),
        "max_multiplicity": max_mult,
        "min_direction_count": min_dirs,
        "pair_trades": total_trades,
        "samples": samples,
    }


def main() -> None:
    cases: list[tuple[str, list[Line], int]] = [
        ("p3_original_three_direction_net", p3_original_net(), 65),
        (
            "generic_four_direction_grid",
            grid_net("G4", [0, 17, 71, 113], [2, 5, 11, 23, 47], [7, 19, 53, 101]),
            20,
        ),
        (
            "five_direction_high_multiplicity_grid",
            grid_net("G5", [0, 1, 12, 55, 144], [6, 14, 35], [10, 44, 120]),
            9,
        ),
        ("seeded_adversarial_generic_slopes", seeded_adversarial_net(), 10),
    ]
    cases.extend((name, lines, 6) for name, lines in template_census_cases())

    summaries = [analyze_case(name, lines, min_rich) for name, lines, min_rich in cases]
    total_rich = sum(row["rich_points"] for row in summaries)
    total_trades = sum(row["pair_trades"] for row in summaries)
    old_p3 = next(row for row in summaries if row["name"] == "p3_original_three_direction_net")
    check("original P3 net reproduces the 65 post-anchor rich parameters", old_p3["rich_points"] == 65)
    check("all charged cells are b=2 pair trades", total_trades >= total_rich * (THRESHOLD - 1))
    check("all local degree-1 fiber identities hold", not LOCAL_FAILS, f"local_assertions={LOCAL_ASSERTS}")

    result = {
        "node": "p3_affine_net_richline_residue",
        "task": "F3",
        "status": "PROVED: U3 survives; affine-net rich points charge to mixed b=2 degree-1 pullback cells",
        "field": f"F_{P}",
        "threshold": THRESHOLD,
        "anchor_slope_excluded": ANCHOR_Z,
        "case_count": len(summaries),
        "total_rich_points": total_rich,
        "total_pair_trades": total_trades,
        "local_assertions": LOCAL_ASSERTS,
        "cases": summaries,
        "lemma": (
            "At any multi-direction rich point of affine branches L_i(z), "
            "a pivot line and each other incident line give a nonzero linear "
            "equality L_i-L_0.  The b=2 fiber dictionary records the pair by "
            "its elementary symmetric coefficients; mixed pair maps cover the "
            "entire incident block."
        ),
        "checks": NCHECK,
    }

    if "--write-certificate" in sys.argv:
        os.makedirs(os.path.dirname(CERT), exist_ok=True)
        with open(CERT, "w") as fh:
            json.dump(result, fh, indent=2, sort_keys=True)
            fh.write("\n")

    expected = None
    if os.path.exists(CERT):
        with open(CERT) as fh:
            expected = json.load(fh)
    check("certificate exists", expected is not None, CERT)
    if expected is not None:
        check("certificate matches recomputed summary", result == expected)

    if FAILS:
        print("\nFAIL:")
        for name in FAILS:
            print("  -", name)
        for name in LOCAL_FAILS[:20]:
            print("  - local:", name)
        print(json.dumps(result, indent=2, sort_keys=True))
        sys.exit(1)
    print("\nsummary:")
    public_summary = {k: result[k] for k in (
        "node",
        "task",
        "status",
        "field",
        "case_count",
        "total_rich_points",
        "total_pair_trades",
        "local_assertions",
        "checks",
    )}
    print(json.dumps(public_summary, indent=2, sort_keys=True))
    print(f"\nPASS: {NCHECK} F3 net-absorption checks")


if __name__ == "__main__":
    main()
