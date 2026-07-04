#!/usr/bin/env python3
"""Verifier for xr_pencil_cascade (W1).

The proof packet says that two distinct aligned slopes whose agreement sets
share a core R with |R| >= A-1 force a codeword pencil (U,V) on R.  If
|R| >= A, every finite slope is already A-bad on R.  If |R| = A-1, every
additional off-core zero of the residual line e_u + z e_v contributes exactly
one finite slope, except for collisions where several off-core points give the
same slope.

Stdlib only; no Monte Carlo.
Run: python3 experimental/scripts/verify_xr_pencil_cascade.py
To refresh the pinned certificate:
  python3 experimental/scripts/verify_xr_pencil_cascade.py --write-certificate
"""

from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass


HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
CERT = os.path.join(
    REPO,
    "experimental",
    "data",
    "certificates",
    "xr-pencil-cascade",
    "toy_pencil_cascade.json",
)

FAILS: list[str] = []
NCHECK = 0


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


@dataclass(frozen=True)
class Fp:
    p: int

    def add(self, a: int, b: int) -> int:
        return (a + b) % self.p

    def sub(self, a: int, b: int) -> int:
        return (a - b) % self.p

    def mul(self, a: int, b: int) -> int:
        return (a * b) % self.p

    def div(self, a: int, b: int) -> int:
        return self.mul(a, self.inv(b))

    def neg(self, a: int) -> int:
        return (-a) % self.p

    def inv(self, a: int) -> int:
        if a % self.p == 0:
            raise ZeroDivisionError("0 has no inverse")
        return pow(a, self.p - 2, self.p)


def eval_poly(F: Fp, coeffs: list[int], domain: list[int]) -> list[int]:
    vals: list[int] = []
    for x in domain:
        acc = 0
        power = 1
        for c in coeffs:
            acc = F.add(acc, F.mul(c, power))
            power = F.mul(power, x)
        vals.append(acc)
    return vals


def vec_add(F: Fp, a: list[int], b: list[int]) -> list[int]:
    return [F.add(x, y) for x, y in zip(a, b)]


def vec_sub(F: Fp, a: list[int], b: list[int]) -> list[int]:
    return [F.sub(x, y) for x, y in zip(a, b)]


def scalar_vec(F: Fp, c: int, a: list[int]) -> list[int]:
    return [F.mul(c, x) for x in a]


def codeword_line(F: Fp, U: list[int], z: int, V: list[int]) -> list[int]:
    return vec_add(F, U, scalar_vec(F, z, V))


def agreement_set(a: list[int], b: list[int]) -> set[int]:
    return {i for i, (x, y) in enumerate(zip(a, b)) if x == y}


def residual_slopes(F: Fp, e_u: list[int], e_v: list[int], core: set[int]) -> dict[int, set[int]]:
    slopes: dict[int, set[int]] = {}
    for i, (a, b) in enumerate(zip(e_u, e_v)):
        if i in core:
            continue
        if b:
            z = F.div(F.neg(a), b)
            slopes.setdefault(z, set()).add(i)
    return slopes


def recover_pencil(
    F: Fp,
    c1: list[int],
    c2: list[int],
    z1: int,
    z2: int,
) -> tuple[list[int], list[int]]:
    denom = F.sub(z1, z2)
    V = scalar_vec(F, F.inv(denom), vec_sub(F, c1, c2))
    U_num = vec_sub(F, scalar_vec(F, z1, c2), scalar_vec(F, z2, c1))
    U = scalar_vec(F, F.inv(denom), U_num)
    return U, V


def threshold_fixture(*, collision: bool = False) -> dict:
    F = Fp(17)
    domain = list(range(9))
    k = 3
    t = 2
    A = k + t
    core = set(range(A - 1))
    U = eval_poly(F, [2, 1, 4], domain)
    V = eval_poly(F, [5, 3, 2], domain)
    e_u = [0, 0, 0, 0, 1, 1 if collision else 2, 3, 4, 5]
    e_v = [0, 0, 0, 0, 1, 1, 1, 1, 1]
    u = vec_add(F, U, e_u)
    v = vec_add(F, V, e_v)
    slopes = residual_slopes(F, e_u, e_v, core)
    for z, points in sorted(slopes.items()):
        w_z = codeword_line(F, u, z, v)
        c_z = codeword_line(F, U, z, V)
        support = agreement_set(w_z, c_z)
        check(
            f"threshold slope {z} contains forced core",
            core <= support,
            f"support={sorted(support)}",
        )
        check(
            f"threshold slope {z} off-core zeros match residual ratios",
            support - core == points,
            f"expected={sorted(points)}, got={sorted(support - core)}",
        )
        check(
            f"threshold slope {z} is A-bad",
            len(support) >= A,
            f"|support|={len(support)}, A={A}",
        )

    off_core = len(domain) - len(core)
    check(
        "threshold anchored slopes bounded by off-core size",
        len(slopes) <= off_core,
        f"slopes={len(slopes)}, off_core={off_core}",
    )

    z_values = sorted(slopes)
    z1, z2 = z_values[:2]
    c1 = codeword_line(F, U, z1, V)
    c2 = codeword_line(F, U, z2, V)
    U_rec, V_rec = recover_pencil(F, c1, c2, z1, z2)
    check("two-slope formula recovers U", U_rec == U)
    check("two-slope formula recovers V", V_rec == V)

    return {
        "field": "F_17",
        "n": len(domain),
        "k": k,
        "A": A,
        "t": t,
        "core_size": len(core),
        "off_core": off_core,
        "collision_fixture": collision,
        "anchored_slopes": len(slopes),
        "largest_off_core_fiber": max(len(points) for points in slopes.values()),
    }


def core_at_A_fixture() -> dict:
    F = Fp(17)
    domain = list(range(9))
    k = 3
    t = 2
    A = k + t
    core = set(range(A))
    U = eval_poly(F, [1, 6, 2], domain)
    V = eval_poly(F, [4, 0, 3], domain)
    e_u = [0, 0, 0, 0, 0, 7, 8, 9, 10]
    e_v = [0, 0, 0, 0, 0, 1, 2, 3, 4]
    u = vec_add(F, U, e_u)
    v = vec_add(F, V, e_v)
    for z in range(F.p):
        w_z = codeword_line(F, u, z, v)
        c_z = codeword_line(F, U, z, V)
        support = agreement_set(w_z, c_z)
        check(
            f"core-A slope {z} contains A-core",
            core <= support,
            f"support={sorted(support)}",
        )
        check(
            f"core-A slope {z} is A-bad",
            len(support) >= A,
            f"|support|={len(support)}, A={A}",
        )
    return {
        "field": "F_17",
        "n": len(domain),
        "k": k,
        "A": A,
        "t": t,
        "core_size": len(core),
        "all_finite_slopes_bad": F.p,
    }


def blocked_point_fixture() -> dict:
    F = Fp(17)
    domain = list(range(9))
    k = 3
    t = 2
    A = k + t
    core = set(range(A - 1))
    e_u = [0, 0, 0, 0, 1, 2, 3, 4, 5]
    e_v = [0, 0, 0, 0, 0, 1, 1, 1, 1]
    slopes = residual_slopes(F, e_u, e_v, core)
    check(
        "off-core point with e_v=0 and e_u!=0 contributes no slope",
        all(4 not in points for points in slopes.values()),
    )
    return {
        "field": "F_17",
        "n": len(domain),
        "k": k,
        "A": A,
        "t": t,
        "core_size": len(core),
        "blocked_points": 1,
        "anchored_slopes": len(slopes),
    }


def main() -> None:
    rows = [
        threshold_fixture(collision=False),
        threshold_fixture(collision=True),
        core_at_A_fixture(),
        blocked_point_fixture(),
    ]
    result = {
        "node": "xr_pencil_cascade",
        "task": "W1",
        "checks": NCHECK,
        "rows": rows,
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
        print("\nrecomputed summary:")
        print(json.dumps(result, indent=2, sort_keys=True))
        print("\nFAIL:")
        for name in FAILS:
            print("  -", name)
        sys.exit(1)

    print("\nsummary:")
    print(json.dumps(result, indent=2, sort_keys=True))
    print(f"\nPASS: {NCHECK} W1 pencil-cascade checks")


if __name__ == "__main__":
    main()
