#!/usr/bin/env python3
"""Verifier for the asymptotic B1 image-normalization repair.

The check is intentionally lightweight and stdlib-only. It verifies that
experimental/asymptotic_rs_mca.tex prints the image-normalized C9 interface,
the two ambient/image bookkeeping lemmas, and a data packet in which every
reported moment explicitly declares its normalization.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
TEX_PATH = ROOT / "experimental" / "asymptotic_rs_mca.tex"
DATA_PATH = ROOT / "experimental" / "data" / "asymptotic_b1_image_normalization_repair.json"
NOTE_PATH = ROOT / "experimental" / "notes" / "audits" / "asymptotic_b1_image_scale_repair.md"

EXPECTED_STATUS = "AUDIT / CONDITIONAL"


def normalize_tex(text: str) -> str:
    return re.sub(r"\s+", " ", text)


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise TypeError(f"{path} did not contain a JSON object")
    return data


def check_tex(tex: str, data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    flat = normalize_tex(tex)

    for label in data.get("required_tex_labels", []):
        require(f"\\label{{{label}}}" in tex, f"missing TeX label: {label}", errors)

    required_phrases = [
        "Image-normalized C9 Fourier/Sidon input",
        "\\begin{assumption}[Image-normalized C9 Fourier/Sidon input]",
        "Conditional closed ledger package",
        "Conditional first-match add-back",
        "Current audit status",
        "Max-fiber ambient-to-image transfer",
        "Moment normalization identity",
        "This is an image-normalized statement",
        "no unprinted bridge \\(A/L=\\exp(o(N))\\) is used",
        "The present note does not prove the missing moduli ledger",
        "Ambient moment estimates can be consumed here only through",
        "An ambient Fourier estimate does not imply this image-scale statement",
        "does not supply the missing C9 moduli/Fourier--Sidon source theorem",
        "does not supply the missing C9 moduli/Fourier--Sidon source theorem, the B3 window-uniformity theorem, the add-back profile decomposition, or the lower-side pole-reservoir collision-loss proof",
        "The lower side consumed by \\cref{thm:frontier} assumes either a subexponential collision loss",
    ]
    for phrase in required_phrases:
        require(phrase in tex, f"missing phrase in TeX: {phrase}", errors)

    compact_checks = [
        r"\Scal=\operatorname{im}\Phi",
        r"\barN=M/L",
        r"\Gsid_{q,\sigma} =L^{-1}\sum_{\Delta(F_s)\le \exp(-\sigma N)} \left(\frac{|F_s|}{\barN}\right)^q \le \exp(o(Nq))",
        r"\Gamma_{\rm amb}(q) =\left(\frac{A}{L}\right)^{q-1}\Gamma_{\rm img}(q)",
        r"\Gamma_{\rm img}(q) =\left(\frac{L}{A}\right)^{q-1}\Gamma_{\rm amb}(q) \le \Gamma_{\rm amb}(q)",
        r"The reverse direction is unsafe without a printed bound on \(A/L\)",
    ]
    for needle in compact_checks:
        require(needle in flat, f"missing normalized TeX fragment: {needle}", errors)

    forbidden_tex_phrases = [
        "thm:image-normalized-sidon-input",
        "def:image-normalized-sidon-input",
        "not an additional conjectural input",
        "The rest of the paper proves \\cref{thm:frontier}.  The proof is self-contained",
        "Fourier inversion on \\(\\Scal\\)",
        "Fourier inversion on \\Scal",
        "Fourier inversion gives \\(L\\mu",
        "image group",
    ]
    for phrase in forbidden_tex_phrases:
        require(phrase not in tex, f"forbidden ambiguous TeX phrase remains: {phrase}", errors)

    c9_index = tex.find("\\item \\emph{Fourier/Sidon cells.}")
    require(c9_index >= 0, "missing C9 Fourier/Sidon item", errors)
    if c9_index >= 0:
        c9_window = tex[c9_index : c9_index + 1000]
        require("image-normalized" in c9_window, "C9 item does not say image-normalized", errors)
        require("not an ambient" in c9_window, "C9 item does not reject ambient normalization", errors)

    return errors


def check_data(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    require(data.get("status") == EXPECTED_STATUS, f"status must be {EXPECTED_STATUS}", errors)
    require(data.get("audit_note") == "experimental/notes/audits/asymptotic_b1_image_scale_repair.md", "missing audit_note path", errors)
    require("lem:ambient-image-max" in data.get("proved_locally", []), "missing local proof: lem:ambient-image-max", errors)
    require("lem:moment-normalization" in data.get("proved_locally", []), "missing local proof: lem:moment-normalization", errors)
    require(
        "ass:image-normalized-sidon-input" in data.get("conditional_inputs", []),
        "missing conditional input: ass:image-normalized-sidon-input",
        errors,
    )
    for expected_nonclaim in [
        "does not prove the C9 moduli/Fourier-Sidon source theorem",
        "does not close the full asymptotic theorem by itself",
        "does not prove B3 window uniformity",
        "does not prove the add-back profile decomposition",
        "does not prove the lower-side pole-reservoir collision-loss input",
        "does not close any finite deployed adjacent row",
    ]:
        require(expected_nonclaim in data.get("nonclaims", []), f"missing nonclaim: {expected_nonclaim}", errors)

    moments = data.get("reported_moments")
    require(isinstance(moments, list) and len(moments) >= 4, "reported_moments must list at least four entries", errors)
    if isinstance(moments, list):
        seen = set()
        for i, moment in enumerate(moments):
            require(isinstance(moment, dict), f"moment {i} is not an object", errors)
            if not isinstance(moment, dict):
                continue
            name = moment.get("name", f"moment {i}")
            normalization = moment.get("normalization")
            require(normalization in {"image", "ambient"}, f"{name}: invalid or missing normalization", errors)
            for key in ["symbol", "denominator", "average_fiber", "source_label"]:
                require(bool(moment.get(key)), f"{name}: missing {key}", errors)
            symbol = moment.get("symbol")
            require(symbol not in seen, f"duplicate symbol entry: {symbol}", errors)
            seen.add(symbol)

        require("Gsid_{q,sigma}" in seen, "missing Gsid reported moment", errors)
        require("Gamma_amb(q)" in seen, "missing ambient comparison moment", errors)
        require("Gamma_img(q)" in seen, "missing image comparison moment", errors)

    return errors


def check_note(note: str) -> list[str]:
    errors: list[str] = []
    for phrase in [
        "Status: AUDIT / CONDITIONAL",
        "ass:image-normalized-sidon-input",
        "The C9 Fourier/Sidon payment is not proved here",
        "This packet does not prove",
        "lower-side pole-reservoir collision loss",
    ]:
        require(phrase in note, f"missing phrase in audit note: {phrase}", errors)
    return errors


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="run checks")
    args = parser.parse_args(argv)

    if not args.check:
        parser.error("nothing to do; pass --check")

    data = load_json(DATA_PATH)
    tex = TEX_PATH.read_text(encoding="utf-8")
    note = NOTE_PATH.read_text(encoding="utf-8")
    errors = check_data(data) + check_tex(tex, data) + check_note(note)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"RESULT: FAIL ({len(errors)} error(s))")
        return 1
    print("RESULT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
