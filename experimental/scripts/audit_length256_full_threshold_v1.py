"""Independent Pascal-row audit for the DIRECT Lane L length-256 packet.

Contract: notes/list/length256_full_threshold_v1.md. No primary-verifier import.
This is a finite arithmetic audit, not independent external proof review.
"""

from copy import deepcopy
from functools import lru_cache
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "data/certificates/length256-full-threshold-v1/packet.json"


@lru_cache(maxsize=16)
def row(n):
    result = [1]
    for size in range(1, n+1):
        result.append(1)
        for j in range(size-1, 0, -1):
            result[j] += result[j-1]
    return tuple(result)


def ceiling(numerator, denominator):
    quotient, remainder = divmod(numerator, denominator)
    return quotient + bool(remainder)


def audit(data):
    assert (data["n"], data["k"], data["shifted_dimension"], data["target_bits"]) == (256, 32, 33, 128)
    assert data["schema"] == "length256-full-threshold-v1"
    assert data["status"] == "PROVED_FINITE_FAMILY" and data["architecture"] == "DIRECT"
    assert data["workboard_item"] == "L"
    assert data["upstream_main"] == "93fba1be3f3299b0ba4708d88715377bbb656e45"
    assert data["pr_1151_parent"] == "f7edd54f889c970825c271c626347dc92f878cdb"
    n, k, scale = 256, 32, 1 << 128
    near = data["near_cap"]
    low, high = int(near["q_lower_inclusive"]), int(near["q_upper_exclusive"])
    assert (low, high) == (1 << 255, 1 << 256)
    assert int(near["budget_min"]) == low//scale
    assert int(near["budget_max"]) == (high-1)//scale
    assert near["list_unsafe_agreement"] == 33 and near["list_first_safe_agreement"] == 34
    assert int(near["list_unsafe_lower"]) == ceiling(row(n)[33], n) > (high-1)//scale
    assert int(near["list_safe_upper"]) == row(n)[32]//row(34)[32] <= low//scale
    assert near["list_common_support_arities"] == "all"
    assert near["largest_safe_grid_radius"] == [111, 128]
    assert near["real_safe_right_endpoint"] == [223, 256]
    assert near["real_right_endpoint_included"] is False
    assert near["johnson_squared_agreement"] == n*(k-1) > 34*34
    assert 111*256 == (n-34)*128 and 223 == n-34+1
    assert near["mca_unsafe_agreement"] == 34 and near["mca_safe_agreement"] == 36
    assert near["mca_first_safe_options"] == [35, 36]
    assert int(near["mca_safe_upper"]) == row(n)[33]//row(35)[32] <= low//scale
    size = int(near["pole_selected_list"])
    assert size == 1 << 129
    assert int(near["shifted_list_lower"]) == ceiling(row(n)[34], n) >= size
    numerator, denominator = size*(low-n), low-n+k*(size-1)
    assert low-n > k*(size-1)
    assert int(near["mca_unsafe_lower"]) == scale+1 <= ceiling(numerator, denominator)

    tower = data["tower"]
    assert (tower["coefficient_field"], tower["extension_degree"]) == (257, 31)
    assert all(257 % divisor for divisor in range(2, 17))
    field, budget = int(tower["q"]), int(tower["budget"])
    assert field == 257**31 and budget == field//scale
    assert (1 << 248) < field < (1 << 249) < low
    assert tower["list_unsafe_agreement"] == 34 and tower["list_safe_agreement"] == 36
    assert tower["list_first_safe_options"] == [35, 36]
    assert tower["list_common_support_arities"] == "all"
    assert int(tower["list_unsafe_lower"]) == ceiling(row(n)[34], 257**2) > budget
    assert int(tower["list_safe_upper"]) == row(n)[32]//row(36)[32] <= budget
    assert tower["mca_unsafe_agreement"] == 36 and tower["mca_safe_agreement"] == 38
    assert tower["mca_first_safe_options"] == [37, 38]
    count = int(tower["pole_selected_list"])
    assert count == budget+1
    assert int(tower["shifted_list_lower"]) == ceiling(row(n)[36], 257**3) >= count
    assert int(tower["mca_safe_upper"]) == row(n)[33]//row(37)[32] <= budget
    assert int(tower["pole_pair_root_upper"]) == k*count*(count-1)//2 < field-n
    paths = {"notes/list/length256_full_threshold_v1.md",
             "scripts/verify_length256_full_threshold_v1.py", "scripts/audit_length256_full_threshold_v1.py"}
    assert set(data["source_sha256"]) == paths
    for ref, checksum in data["source_sha256"].items():
        assert hashlib.sha256((ROOT/ref).read_bytes()).hexdigest() == checksum
    assert set(data["nonclaims"]) == {"KoalaBear closure", "FPC5 aggregation", "near-cap MCA 35 safety",
                                      "tower LIST 35 safety", "tower MCA 37 safety", "grand prize resolution"}


def main():
    if not PACKET.exists():
        raise FileNotFoundError("INCOMPLETE: canonical packet is missing")
    data = json.loads(PACKET.read_text())
    audit(data)
    changes = [
        ((), "n", 255), ((), "k", 33), ((), "shifted_dimension", 34),
        (("near_cap",), "list_first_safe_agreement", 33),
        (("near_cap",), "budget_min", str((1 << 127)-1)),
        (("near_cap",), "real_right_endpoint_included", True),
        (("near_cap",), "mca_first_safe_options", [35]),
        (("tower",), "budget", "0"), (("tower",), "extension_degree", 32),
        (("tower",), "mca_safe_agreement", 37),
        (("tower",), "pole_selected_list", data["tower"]["budget"]),
        (("source_sha256",), "notes/list/length256_full_threshold_v1.md", "0"*64),
    ]
    for path, key, value in changes:
        bad = deepcopy(data)
        target = bad
        for component in path:
            target = target[component]
        target[key] = value
        try:
            audit(bad)
        except AssertionError:
            continue
        raise AssertionError(f"FAIL: mutation accepted: {path}/{key}")
    print(f"PASS: independent Pascal replay and {len(changes)} hostile mutations; no primary import or field enumeration")


if __name__ == "__main__":
    main()
