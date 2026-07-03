#!/usr/bin/env python3
"""E20 KMS/KLLM loss-exponent statement arithmetic.

This verifier contains no experimental search.  It records the statement-level
quantitative information needed by the E20/QX.10 roadmap item and checks the
small amount of exponent arithmetic used in the note:

* raw Johnson/Grassmann small-set theorems are structural/asymptotic, so they
  do not by themselves emit a finite q-power loss at FM scale;
* the KLLM global-hypercontractive input has beta^(1/4) loss;
* for an indicator family of FM measure mu = q^(1-t), Holder turns the KLLM
  L4 estimate into an internal-stay exponent (g+t-1)/4 when the globalness
  parameter is beta <= q^(-g).
"""
from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any


OUTPUT = Path(
    "experimental/data/certificates/kms-kllm-loss-tables/"
    "kms_kllm_loss_tables.json"
)

RATES = ("1/2", "1/4", "1/8", "1/16")
SLACKS = (2, 3, 4, 5, 6, 8)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def frac_string(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def theorem_sources() -> list[dict[str, Any]]:
    return [
        {
            "id": "KMMS_Johnson_2025_ToC_Theorem_1_3",
            "title": "Small-Set Expansion in the Johnson Graph",
            "authors": ["Subhash Khot", "Dor Minzer", "Dana Moshkovitz", "Muli Safra"],
            "venue": "Theory of Computing 21(2), 2025",
            "url": "https://theoryofcomputing.org/articles/v021a002/",
            "extracted_statement_type": "qualitative structural small-set expansion",
            "usable_q_power_loss": None,
            "verdict": "NO_DIRECT_FM_SCALE_IMPORT",
            "reason": (
                "The statement has the form: for fixed alpha and eta there "
                "exist r and epsilon so pseudorandom Johnson sets have "
                "expansion above 1-eta.  It gives the right tangent/junta "
                "obstruction, but no explicit q-power exponent at mu=q^(1-t)."
            ),
        },
        {
            "id": "DKKMS_Grassmann_2021_IJM",
            "title": "On non-optimally expanding sets in Grassmann graphs",
            "authors": [
                "Irit Dinur",
                "Subhash Khot",
                "Guy Kindler",
                "Dor Minzer",
                "Muli Safra",
            ],
            "venue": "Israel Journal of Mathematics 243, 2021",
            "url": "https://doi.org/10.1007/s11856-021-2164-7",
            "extracted_statement_type": "constant-threshold partial Grassmann inverse theorem",
            "usable_q_power_loss": None,
            "verdict": "NO_DIRECT_FM_SCALE_IMPORT",
            "reason": (
                "The extracted quantitative threshold is constant-scale: "
                "expansion below 7/8 implies non-pseudorandomness.  This is "
                "too coarse to price FM-scale measure q^(1-t) without a "
                "separate q-power bridge."
            ),
        },
        {
            "id": "KMS_Grassmann_2023_Annals",
            "title": "Pseudorandom sets in Grassmann graph have near-perfect expansion",
            "authors": ["Subhash Khot", "Dor Minzer", "Muli Safra"],
            "venue": "Annals of Mathematics 198(1), 2023",
            "url": "https://doi.org/10.4007/annals.2023.198.1.1",
            "extracted_statement_type": "asymptotic near-perfect expansion for pseudorandom Grassmann sets",
            "usable_q_power_loss": None,
            "verdict": "NO_DIRECT_FM_SCALE_IMPORT_AS_STATED",
            "reason": (
                "The Annals theorem supplies the qualitative endpoint that "
                "pseudorandom Grassmann sets expand as 1-o(1).  The E20 "
                "arithmetic still needs explicit finite exponents before it "
                "can pay a q^(1-t) FM ledger directly."
            ),
        },
        {
            "id": "KLLM_Global_Hypercontractivity_2024_JAMS",
            "title": "Hypercontractivity for global functions and sharp thresholds",
            "authors": ["Peter Keevash", "Noam Lifshitz", "Eoin Long", "Dor Minzer"],
            "venue": "Journal of the AMS 37(1), 2024; arXiv:2103.04604",
            "url": "https://doi.org/10.1090/jams/1027",
            "extracted_statement_type": "global hypercontractivity",
            "usable_q_power_loss": "conditional",
            "verdict": "SURVIVES_CONDITIONALLY_ON_QX11_GLOBALNESS",
            "reason": (
                "The source theorem gives a p-independent noise rate and a "
                "beta^(1/4) loss for beta-small generalized influences.  "
                "Thus a q-power globalness certificate converts to an "
                "explicit q-power small-set-expansion loss."
            ),
            "loss_exponent_beta_to_L4": "1/4",
            "noise_parameter_recorded": "rho = 1/5 in the highlighted (4,2) cube statement",
        },
    ]


def kllm_row(slack: int, globalness_exponent: int) -> dict[str, Any]:
    if slack <= 1:
        raise ValueError("FM slack t must be at least 2")
    fm_measure_exponent = slack - 1
    stay = Fraction(globalness_exponent + fm_measure_exponent, 4)
    full_match_required_g = 3 * fm_measure_exponent
    return {
        "slack_t": slack,
        "fm_measure": f"mu = q^(-{fm_measure_exponent})",
        "globalness_beta": f"beta <= q^(-{globalness_exponent})",
        "kllm_internal_stay_exponent": frac_string(stay),
        "kllm_internal_stay_bound": f"Pr[one KLLM-noise step stays in A | A] <= q^(-{frac_string(stay)})",
        "full_fm_stay_exponent": fm_measure_exponent,
        "matches_full_fm_stay_exponent": stay >= fm_measure_exponent,
        "globalness_exponent_needed_to_match_full_fm": full_match_required_g,
    }


def rate_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for rate in RATES:
        rows.append(
            {
                "rate": rate,
                "direct_rate_dependency_in_extracted_theorems": "none",
                "interpretation": (
                    "The extracted KMS/DKKMS/KLLM loss exponents do not depend "
                    "on the Reed-Solomon rate directly.  Rate enters later "
                    "through which FM slack t and which paid tangent/globalness "
                    "ledgers the XR assembly must certify."
                ),
                "slack_rows": [
                    {
                        "slack_t": slack,
                        "fm_measure_exponent": slack - 1,
                        "kllm_stay_exponent_if_beta_le_1": frac_string(
                            Fraction(slack - 1, 4)
                        ),
                        "globalness_exponent_needed_to_match_full_fm": 3 * (slack - 1),
                    }
                    for slack in SLACKS
                ],
            }
        )
    return rows


def build_certificate() -> dict[str, Any]:
    sources = theorem_sources()
    kllm_no_extra_globalness = [kllm_row(slack, 0) for slack in SLACKS]
    kllm_full_match = [
        kllm_row(slack, 3 * (slack - 1)) for slack in SLACKS
    ]
    payload: dict[str, Any] = {
        "schema": "kms_kllm_loss_tables.v1",
        "roadmap_task": "E20 / QX.10 / xr_kms_parameter_matching",
        "status": "AUDIT_STATEMENT_ARITHMETIC",
        "sources": sources,
        "fm_scale_convention": {
            "measure": "mu ~= q^(1-t)",
            "slack_parameter": "t = A-k in the FM1 split-locator convention",
            "fm_measure_exponent": "t-1",
        },
        "kllm_conversion": {
            "assumption": "indicator family A has measure mu=q^(1-t) and beta-small generalized influences with beta<=q^(-g)",
            "source_loss": "||T_{1/5} f||_4 <= beta^(1/4) ||f||_2",
            "holder_step": "<f,Tf> <= ||f||_{4/3} ||Tf||_4",
            "internal_stay_exponent": "(g+t-1)/4",
            "globalness_needed_to_match_full_fm_stay": "g >= 3(t-1)",
        },
        "kllm_no_extra_globalness_table": kllm_no_extra_globalness,
        "kllm_full_fm_match_table": kllm_full_match,
        "rate_table": rate_rows(),
        "verdict": {
            "raw_kms_dkkms_direct_import": "FAILS_FOR_FM_SCALE_AS_STATED",
            "kllm_route": "CONDITIONALLY_CARRIES_IF_QX11_CERTIFIES_GLOBALNESS",
            "next_required_certificate": (
                "QX.11 must convert paid tangent ledgers into beta<=q^(-g) "
                "generalized-influence/globalness bounds.  QX.14 then decides "
                "whether the resulting (g+t-1)/4 exponent is enough for each "
                "rate/slack row."
            ),
        },
        "nonclaims": [
            "does not prove a KMS/DKKMS/KLLM import theorem",
            "does not verify the hypotheses of KLLM for RS alignment sets",
            "does not settle the final XR wall arithmetic",
            "does not extract hidden constants from the primary papers",
        ],
        "script_sha256": sha256_text(Path(__file__).read_text()),
    }
    normalized = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["payload_sha256"] = sha256_text(normalized)
    return payload


def print_summary(certificate: dict[str, Any]) -> None:
    print(certificate["schema"])
    print("raw KMS/DKKMS:", certificate["verdict"]["raw_kms_dkkms_direct_import"])
    print("KLLM:", certificate["verdict"]["kllm_route"])
    print("KLLM no-extra-globalness table:")
    for row in certificate["kllm_no_extra_globalness_table"]:
        print(
            f"  t={row['slack_t']} mu={row['fm_measure']} "
            f"stay_exp={row['kllm_internal_stay_exponent']} "
            f"need_g={row['globalness_exponent_needed_to_match_full_fm']}"
        )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit", action="store_true", help="write the certificate JSON")
    parser.add_argument("--check", type=Path, help="check an existing certificate JSON")
    args = parser.parse_args()

    certificate = build_certificate()
    if args.emit:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n")
    if args.check:
        existing = json.loads(args.check.read_text())
        if existing != certificate:
            raise SystemExit(f"certificate mismatch: {args.check}")
    if not args.emit and not args.check:
        print_summary(certificate)


if __name__ == "__main__":
    main()
