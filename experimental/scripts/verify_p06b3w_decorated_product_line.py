#!/usr/bin/env python3
"""Symbolically verify the P06b3w decorated product-line theorem."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


OUTPUT = (
    Path(__file__).resolve().parent.parent
    / "data/certificates/paper-d-cubic-product-line/"
    "p06b3w_decorated_product_line.json"
)


def main() -> None:
    r, a, t, w, W = sp.symbols("r a t w W")
    difference = (W - w) / (r - 1)
    pair_product_left = w / a
    pair_sum_left = sp.factor(
        (difference - pair_product_left + a - 1) / (a - 1)
    )
    u_left = sp.factor(a + pair_sum_left)
    v_left = sp.factor(a * pair_sum_left + pair_product_left)
    u_right = sp.factor(u_left + r - 1)
    pair_sum_right = sp.factor(u_right - t)
    pair_product_right = W / t
    compatibility = sp.factor(
        t * pair_sum_right
        + pair_product_right
        - (v_left + (r - 1) * (u_left - 1))
    )
    numerator, denominator = sp.together(compatibility).as_numer_denom()
    numerator = sp.factor(numerator)
    denominator = sp.factor(denominator)

    left_factor = sp.factor(
        -a * r + a * t + a + r * t + r - t**2 - t - 1
    )
    right_factor = sp.factor(
        a**2 + a * r - a * t - a + r**2 - r * t - r + t
    )
    constant = sp.factor(a * t * (t - a) * (a - 1) * (r - 1) * (r - t))
    expected_numerator = sp.factor(-a * left_factor * W + t * right_factor * w + constant)

    if sp.expand(numerator - expected_numerator) != 0:
        raise AssertionError("product-line numerator identity failed")
    if denominator != a * t * (a - 1) * (r - 1):
        raise AssertionError("clearing denominator drift")

    resultant = sp.factor(sp.resultant(left_factor, right_factor, a))
    expected_resultant = (r - 1) ** 2 * (r - t) ** 2
    if sp.expand(resultant - expected_resultant) != 0:
        raise AssertionError("degeneracy resultant identity failed")

    payload = {
        "schema": "p06b3w-decorated-product-line-symbolic-verification/v1",
        "claim_id": "P06B3W_DECORATED_PRODUCT_LINE_REDUCTION",
        "status": "PASS_EXACT_SYMBOLIC_IDENTITIES",
        "clearing_denominator": "a*t*(a-1)*(r-1)",
        "left_factor": str(left_factor),
        "right_factor": str(right_factor),
        "constant_factor": str(constant),
        "degeneracy_resultant_in_a": str(resultant),
        "record_currency": "decorated_records=9*sum_r(C_r)=288*T_sm",
        "scope_guard": (
            "This theorem reduces valid records to nonzero product lines. It does "
            "not bound their aggregate over subgroup parameters."
        ),
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="ascii")
    print("PASS P06b3w decorated product-line symbolic verification")
    print(f"resultant={resultant}")


if __name__ == "__main__":
    main()
