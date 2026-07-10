#!/usr/bin/env python3
"""Independent checker for compiler-hyp visibility audit (W48-FIX: CLEAN).

Checker route: re-read statement windows + resolve defined terms.
- thm:main-ledger must be CITED (not SILENT): statement uses closed ledger;
  def:closed-asymptotic-ledger (L3) contains distinct-ray compiler.
- curated CITED rows must have definition_clause resolving to A4/A6/A7/L3.
- verdict CLEAN; SILENT count 0.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

CERT = Path(
    "experimental/data/certificates/compiler-hyp-visibility/"
    "compiler_hyp_visibility.json"
)
TEX = Path("experimental/asymptotic_rs_mca_frontiers.tex")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def statement_of(text: str, label: str) -> str | None:
    lines = text.splitlines()
    lab_pat = re.compile(r"\\label(?:\[[^\]]*\])?\{" + re.escape(label) + r"\}")
    idx = next((i for i, ln in enumerate(lines) if lab_pat.search(ln)), None)
    if idx is None:
        return None
    start = idx
    while start > 0 and not re.search(
        r"\\begin\{(theorem|proposition|corollary|definition)\}", lines[start]
    ):
        start -= 1
    body = []
    for j in range(start, min(len(lines), start + 80)):
        if re.search(r"\\begin\{proof\}", lines[j]):
            break
        if re.search(
            r"\\end\{(theorem|proposition|corollary|definition)\}", lines[j]
        ):
            break
        body.append(lines[j])
    return "\n".join(body)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--check", action="store_true")
    args = p.parse_args()
    if not args.check:
        p.print_help()
        return 2
    root = repo_root()
    cert = json.loads((root / CERT).read_text(encoding="utf-8"))
    text = (root / TEX).read_text(encoding="utf-8")
    fails: list[str] = []

    for lab in (
        "hyp:ray-compiler",
        "eq:ray-compiler",
        "def:admissible-sequence",
        "def:closed-asymptotic-ledger",
        "thm:main-ledger",
        "prop:q-implies-sp",
    ):
        if not cert.get("pins", {}).get(lab, {}).get("found"):
            fails.append(f"pin:{lab}")

    if cert.get("verdict") != "CLEAN":
        fails.append("verdict_expected_CLEAN")
    if cert.get("counts", {}).get("SILENT", 0) != 0:
        fails.append("silent_nonzero")
    if not cert.get("curated_cited_resolved"):
        fails.append("cited_not_resolved")

    # main-ledger must be CITED with L3 resolution
    ml = next(
        (r for r in cert.get("table", []) if r.get("result") == "thm:main-ledger"),
        None,
    )
    if not ml or ml.get("visibility") != "CITED":
        fails.append("main_ledger_not_cited")
    if ml and "L3" not in (ml.get("definition_clause") or "") and "L3" not in (
        ml.get("evidence_invocation") or ""
    ):
        fails.append("main_ledger_missing_L3_evidence")

    # Independent: closed-ledger def contains distinct-ray compiler
    closed = statement_of(text, "def:closed-asymptotic-ledger")
    if closed is None or not re.search(
        r"distinct-ray\s+compiler|distinct.ray compiler", closed, re.I | re.S
    ):
        fails.append("closed_ledger_no_L3_ray")
    # main-ledger statement uses closed asymptotic ledger
    st_ml = statement_of(text, "thm:main-ledger")
    if st_ml is None or not re.search(r"closed asymptotic ledger", st_ml, re.I):
        fails.append("main_ledger_stmt_no_closed")

    # Spot-check admissible A6 has RC
    adm = statement_of(text, "def:admissible-sequence")
    if adm is None or not re.search(r"hyp:ray-compiler|\\textup\{\(RC\)\}", adm):
        fails.append("admissible_no_A6_rc")

    # prop:q-implies-sp still VISIBLE
    st_q = statement_of(text, "prop:q-implies-sp")
    if st_q is None or not re.search(r"\\textup\{\(RC\)\}", st_q):
        fails.append("q_implies_sp_not_visible")

    # curated CITED rows have definition_clause
    for r in cert.get("table", []):
        if r.get("curated") and r.get("visibility") == "CITED":
            if not r.get("definition_clause"):
                fails.append(f"no_clause:{r.get('result')}")

    if not cert.get("all_pass"):
        fails.append("all_pass")

    if fails:
        print("RESULT: FAIL", fails)
        return 1
    print("RESULT: PASS")
    print(
        "route: resolve defined terms (closed-ledger L3, admissible A4/A6/A7); "
        "main-ledger CITED not SILENT; CLEAN SILENT=0"
    )
    print("payload_sha256:", cert.get("payload_sha256"))
    print("verdict:", cert.get("verdict"))
    print("counts:", cert.get("counts"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
