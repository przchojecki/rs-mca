#!/usr/bin/env python3
"""Re-checker for the WCL first-installment theorem packet.

This does NOT re-run the five censuses (they are large). It re-validates the
packet the way a reviewer would want: the recorded certificate summaries are
internally consistent, every admissibility gate is respected with margin, and
-- the point of the packet -- the LEVEL SCOPE of each theorem is exactly the
level at which the register's completeness derivation consumes it.

The last check is the load-bearing one. The weight-3/4 ambient exclusions are
`ell = 1` theorems; the derivation must use them only as {(1,3), (1,4)}, and
every other (ell, w) with w in {3,4} must be excluded by the Newton floor
instead. A mutation control asserts that dropping the Newton floor would make
the packet's scope claim false -- i.e. that the claim has content.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data/certificates/wcl-first-installment-v1/wcl_first_installment_v1.json"

ADMISSIBLE_V2 = 41          # official rows need v_2(q-1) >= 41
TOWER_DIMS = (1, 2, 4)      # level dimensions carrying open cells
WINDOW_LO, WINDOW_HI = 1, 7 # window [ell+1, ell+7]


def newton_floor(ell: int) -> int:
    """Newton short-window theorem (T5): reduced vanishers need w >= 2*ell+1."""
    return 2 * ell + 1


def main() -> None:
    data = json.loads(CERT.read_text())
    assert data["schema"] == "wcl-first-installment-v1"
    cells = data["theorems"]
    assert len(cells) == 5, "packet must carry exactly five theorems"

    # 1. every census respects the admissibility gate, with margin
    for t in cells:
        v2 = t.get("max_v2_observed")
        if v2 is None:
            continue
        assert v2 < ADMISSIBLE_V2, f"{t['id']}: observed v_2 {v2} reaches the gate"
        assert t["events"] == 0, f"{t['id']}: a census recorded an EVENT"

    # 2. internal consistency of the two ambient censuses
    w4 = next(t for t in cells if t["id"] == "weight4_ambient")
    assert w4["classes"] == 24979 and w4["section_keys"] == 1014080
    assert w4["factor_roots"] == 44599 and w4["prime_graph_nodes"] == 154086
    w3 = next(t for t in cells if t["id"] == "weight3_ambient")
    assert w3["classes"] == 254 and w3["factor_roots"] == 439

    # 3. the ell=2 closures are proved AT order 1024, not lifted from ell=1
    for cid in ("ell2_weight5", "ell2_weight6"):
        t = next(x for x in cells if x["id"] == cid)
        assert t["root_order"] == 1024, f"{cid}: wrong root order"
        assert t["window"] == [0, 512], f"{cid}: wrong support window"
    for cid in ("weight3_ambient", "weight4_ambient"):
        t = next(x for x in cells if x["id"] == cid)
        assert t["root_order"] == 512, f"{cid}: wrong root order"
        assert t["window"] == [0, 256], f"{cid}: wrong support window"

    # 4. THE SCOPE CLAIM: weights 3 and 4 are ambient-excluded only at ell = 1;
    #    at every deeper level the Newton floor already removes them.
    ambient_scope = {(1, 3), (1, 4)}
    assert set(map(tuple, data["ambient_excluded"])) == ambient_scope
    for ell in TOWER_DIMS:
        for w in (3, 4):
            if (ell, w) in ambient_scope:
                continue
            assert w < newton_floor(ell), (
                f"({ell},{w}) is neither ambient-excluded nor below the Newton floor"
                " -- an order-1024/2048 weight-3/4 result would be required"
            )

    # 5. mutation control: without the Newton floor the scope claim has content
    holes = [(ell, w) for ell in TOWER_DIMS for w in (3, 4)
             if (ell, w) not in ambient_scope and w >= 1]  # floor disabled
    assert holes, "scope claim is vacuous -- the Newton floor is doing no work"

    # 6. the declared window is the register's, unchanged
    assert data["window_bounds"] == [WINDOW_LO, WINDOW_HI]

    print(
        "WCL_FIRST_INSTALLMENT_PASS theorems=5 "
        f"max_v2={max(t['max_v2_observed'] for t in cells if t.get('max_v2_observed'))} "
        f"gate={ADMISSIBLE_V2} events=0 "
        f"ambient_scope={sorted(ambient_scope)} newton_covers={sorted(holes)}"
    )


if __name__ == "__main__":
    main()
