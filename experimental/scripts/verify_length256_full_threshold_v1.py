"""Lane L, DIRECT LIST/MCA length-256 packet; integer arithmetic only.

Full bankability contract and analytic proofs: notes/list/length256_full_threshold_v1.md.
This checks their arithmetic, not a finite-field enumeration or the four-row compiler.
"""

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "data/certificates/length256-full-threshold-v1/packet.json"
SOURCES = (
    "notes/list/length256_full_threshold_v1.md",
    "scripts/verify_length256_full_threshold_v1.py",
    "scripts/audit_length256_full_threshold_v1.py",
)


def choose(n, k):
    if k < 0 or k > n:
        return 0
    result = 1
    for j in range(1, min(k, n-k) + 1):
        numerator = result * (n-j+1)
        assert numerator % j == 0
        result = numerator // j
    return result


def ceil_div(n, d):
    return (n+d-1)//d


def build():
    n, k = 256, 32
    low, high = 2**255, 2**256
    b_min, b_max = low//2**128, (high-1)//2**128
    list_upper = choose(n, k)//choose(34, k)
    list_lower = ceil_div(choose(n, k+1), n)
    mca_upper = choose(n, k+1)//choose(35, k)
    shifted_lower = ceil_div(choose(n, k+2), n)
    selected = 2**129
    assert list_lower > b_max and list_upper <= b_min
    assert mca_upper <= b_min and shifted_lower >= selected
    assert low-n > k*(selected-1)
    assert 34**2 < n*(k-1)

    q = 257**31
    b = q//2**128
    assert 2**248 < q < 2**249 < low
    assert all(257 % prime for prime in (2, 3, 5, 7, 11, 13))
    ordinary_lower = ceil_div(choose(n, 34), 257**2)
    ordinary_upper = choose(n, k)//choose(36, k)
    pole_lower = ceil_div(choose(n, 36), 257**3)
    pole_upper = choose(n, k+1)//choose(37, k)
    pole_selected = b+1
    assert ordinary_lower > b >= ordinary_upper
    assert pole_lower >= pole_selected and pole_upper <= b
    assert k*choose(pole_selected, 2) < q-n
    return {
        "schema": "length256-full-threshold-v1",
        "status": "PROVED_FINITE_FAMILY",
        "architecture": "DIRECT",
        "workboard_item": "L",
        "upstream_main": "93fba1be3f3299b0ba4708d88715377bbb656e45",
        "pr_1151_parent": "f7edd54f889c970825c271c626347dc92f878cdb",
        "n": n, "k": k, "shifted_dimension": k+1, "target_bits": 128,
        "near_cap": {
            "q_lower_inclusive": str(low), "q_upper_exclusive": str(high),
            "budget_min": str(b_min), "budget_max": str(b_max),
            "list_unsafe_agreement": 33, "list_first_safe_agreement": 34,
            "list_unsafe_lower": str(list_lower), "list_safe_upper": str(list_upper),
            "list_common_support_arities": "all",
            "largest_safe_grid_radius": [111, 128],
            "real_safe_right_endpoint": [223, 256], "real_right_endpoint_included": False,
            "johnson_squared_agreement": n*(k-1),
            "mca_unsafe_agreement": 34, "mca_safe_agreement": 36,
            "mca_first_safe_options": [35, 36],
            "mca_safe_upper": str(mca_upper),
            "shifted_list_lower": str(shifted_lower),
            "pole_selected_list": str(selected),
            "mca_unsafe_lower": str(2**128+1),
        },
        "tower": {
            "coefficient_field": 257, "extension_degree": 31,
            "q": str(q), "budget": str(b),
            "list_unsafe_agreement": 34, "list_safe_agreement": 36,
            "list_first_safe_options": [35, 36],
            "list_unsafe_lower": str(ordinary_lower), "list_safe_upper": str(ordinary_upper),
            "list_common_support_arities": "all",
            "mca_unsafe_agreement": 36, "mca_safe_agreement": 38,
            "mca_first_safe_options": [37, 38],
            "shifted_list_lower": str(pole_lower), "mca_safe_upper": str(pole_upper),
            "pole_selected_list": str(pole_selected),
            "pole_pair_root_upper": str(k*choose(pole_selected, 2)),
        },
        "source_sha256": {ref: hashlib.sha256((ROOT/ref).read_bytes()).hexdigest() for ref in SOURCES},
        "nonclaims": ["KoalaBear closure", "FPC5 aggregation", "near-cap MCA 35 safety",
                      "tower LIST 35 safety", "tower MCA 37 safety", "grand prize resolution"],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit", action="store_true", help="print the reproducible certificate")
    args = parser.parse_args()
    result = build()
    if args.emit:
        print(json.dumps(result, indent=2, sort_keys=True))
        return
    if not PACKET.exists():
        raise FileNotFoundError("INCOMPLETE: canonical packet is missing")
    assert json.loads(PACKET.read_text()) == result, "FAIL: canonical packet differs"
    print("PASS: exact near-cap all-arity LIST crossing 34; near-cap MCA {35,36}; tower LIST {35,36}, MCA {37,38}; source hashes match")


if __name__ == "__main__":
    main()
