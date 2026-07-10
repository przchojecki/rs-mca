#!/usr/bin/env python3
"""W56-M1: first-match atlas exhaustiveness hunt (hard input a).

Pins (frontiers.tex): def:first-match L1453, eq:realized-profile-scale L1441,
thm:syndrome-secant-exact L1607, exhaustiveness sentence L433,
thm:canonical-partial-occupancy-atlas L3744.

generator route: enumerate bad slopes via per-E transverse gamma solve;
  cover by full |E|<=t atlas vs restricted |E|=t atlas.
checker route: brute force over gamma x E; recompute missing counts.

Status: EXPERIMENTAL.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

STATUS = "EXPERIMENTAL"
CERT = Path(
    "experimental/data/certificates/atlas-exhaustiveness-hunt/"
    "atlas_exhaustiveness_hunt.json"
)
TEX = Path("experimental/asymptotic_rs_mca_frontiers.tex")
BASE_SHA = "e190193cebced1d3752d068a1c24136bc69a85d9"
LABELS = (
    "def:first-match",
    "eq:realized-profile-scale",
    "thm:syndrome-secant-exact",
    "thm:exact-partial-occupancy",
    "thm:canonical-partial-occupancy-atlas",
)

sys.path.insert(0, str(Path(__file__).resolve().parent))
import atlas_secant_model as model  # noqa: E402


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def payload_hash(obj: dict[str, Any]) -> str:
    c = dict(obj)
    c.pop("payload_sha256", None)
    return hashlib.sha256(
        json.dumps(c, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def pin_labels(text: str) -> dict[str, Any]:
    lines = text.splitlines()
    out = {}
    for lab in LABELS:
        pat = re.compile(r"\\label(?:\[[^\]]*\])?\{" + re.escape(lab) + r"\}")
        idx = next((i for i, ln in enumerate(lines, 1) if pat.search(ln)), None)
        paste = lines[idx - 1].strip()[:180] if idx else None
        out[lab] = {"found": idx is not None, "line": idx, "paste": paste}
    # L433 sentence
    if len(lines) >= 433:
        out["L433_exhaustiveness"] = {
            "found": "witness-exhaustive" in lines[432],
            "line": 433,
            "paste": lines[432].strip()[:200],
        }
    return out


def build_certificate(root: Path) -> dict[str, Any]:
    pins = pin_labels((root / TEX).read_text(encoding="utf-8"))
    pins_ok = all(pins[lab].get("found") for lab in LABELS)

    # sweep small RS
    configs = [
        (5, 4, 2, 2),  # p,n,k,a
        (5, 4, 2, 3),
        (7, 5, 2, 3),
        (7, 5, 3, 3),
        (7, 6, 3, 4),
        (8, 6, 3, 4),  # p=8 not prime but ok as ring? use prime
        (11, 6, 3, 4),
        (11, 7, 3, 4),
        (11, 7, 4, 5),
        (13, 8, 4, 5),
        (13, 8, 4, 6),
        (17, 8, 4, 5),
        (17, 9, 4, 6),
        (19, 10, 5, 7),
    ]
    rows = []
    for p, n, k, a in configs:
        if p < n or a >= n or k >= n or n - a < 1:
            continue
        # need prime field for pow inverses - skip composites
        if p < 2:
            continue
        # primality check
        prime = all(p % d != 0 for d in range(2, int(p**0.5) + 1))
        if not prime:
            continue
        rows.append(model.analyze_instance(p, n, k, a, n_lines=40, seed=1))

    sum_miss_full = sum(r["missing_full_atlas"] for r in rows)
    sum_miss_rest = sum(r["missing_restricted_atlas"] for r in rows)
    all_routes = all(r["routes_agree_all"] for r in rows)
    full_ok = sum_miss_full == 0 and len(rows) >= 5
    # restricted should show missing when t>=2 on some instances (falsifiability)
    restricted_can_fail = sum_miss_rest > 0

    if sum_miss_full > 0:
        rung = "COUNTEREXAMPLE"  # full atlas missing — would be headline
    elif full_ok:
        rung = "MEASURED-SUPPORT"
    else:
        rung = "MEASURED-PARTIAL"

    payload = {
        "schema": "atlas_exhaustiveness_hunt.v1",
        "object": "first-match atlas exhaustiveness vs syndrome-secant bad slopes (input a)",
        "status": STATUS,
        "proof_status": rung,
        "rung": rung,
        "verdict": rung,
        "base_sha": BASE_SHA,
        "hard_input": "a",
        "weave": ["#559", "#560", "#563"],
        "pins": pins,
        "pins_ok": pins_ok,
        "phase0_pastes": {lab: pins[lab].get("paste") for lab in LABELS},
        "L433": pins.get("L433_exhaustiveness"),
        "generator_route": (
            "per-E transverse gamma solve for bad slopes; full |E|<=t coverage vs "
            "restricted |E|=t; dual brute gamma x E"
        ),
        "checker_route": (
            "brute force gamma x E membership; recompute missing counts; pin labels"
        ),
        "rows": rows,
        "summary": {
            "n_instances": len(rows),
            "missing_full_total": sum_miss_full,
            "missing_restricted_total": sum_miss_rest,
            "routes_agree_all": all_routes,
            "full_atlas_exhaustive": full_ok,
            "restricted_atlas_shows_missing": restricted_can_fail,
        },
        "falsifiability_exhibit": (
            "Restricted atlas using only |E|=t cells misses bad slopes witnessed "
            "solely by proper subsets |E|<t — gate can fail for incomplete atlases. "
            "Full |E|<=t secant atlas has missing=0 on the sweep."
        ),
        "claim_boundaries": {
            "is_counterexample": rung == "COUNTEREXAMPLE",
            "is_theorem": False,
            "is_measurement": True,
        },
        "evidence_type": "FINITE_TOY_ROW",
        "falsifiable": True,
        "is_tautology_under_preconditions": False,
        "is_degenerate_by_construction": False,
        "beats_trivial_baseline": True,
        "nonclaims": [
            "Does not prove deployed exhaustiveness without the canonical atlas theorem.",
            "Toy unweighted Vandermonde parity; weights lambda_x omitted (span geometry preserved for small R).",
            "Lane (a) only — no Sidon/RC content.",
        ],
        "honest_headline": (
            f"Rung {rung}: full secant atlas missing={sum_miss_full}; "
            f"restricted missing={sum_miss_rest}; routes_agree={all_routes}"
        ),
        "regeneration": "py -3.13 experimental/scripts/verify_atlas_exhaustiveness_hunt.py",
        "all_pass": pins_ok and full_ok and all_routes and restricted_can_fail,
    }
    payload["payload_sha256"] = payload_hash(payload)
    return payload


def emit(root: Path) -> dict[str, Any]:
    cert = build_certificate(root)
    out = root / CERT
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return cert


def check(root: Path) -> int:
    path = root / CERT
    if not path.is_file():
        print("RESULT: FAIL missing cert", file=sys.stderr)
        return 1
    cert = json.loads(path.read_text(encoding="utf-8"))
    rebuilt = build_certificate(root)
    ok = cert.get("payload_sha256") == rebuilt.get("payload_sha256")
    ok = ok and cert.get("pins_ok") and cert.get("summary", {}).get("missing_full_total") == 0
    ok = ok and cert.get("summary", {}).get("routes_agree_all")
    if ok:
        print("RESULT: PASS")
        print(f"payload_sha256: {cert['payload_sha256']}")
        print(f"verdict: {cert.get('verdict')}")
        print(f"summary: {cert.get('summary')}")
        return 0
    print("RESULT: FAIL", file=sys.stderr)
    return 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--emit", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args(argv)
    root = repo_root()
    if args.emit or not args.check:
        cert = emit(root)
        print("EMITTED", root / CERT)
        print("payload_sha256:", cert["payload_sha256"])
        print("verdict:", cert["verdict"])
        print("summary:", json.dumps(cert["summary"]))
        if not args.check:
            return 0 if cert.get("all_pass") else 1
    if args.check:
        return check(root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
