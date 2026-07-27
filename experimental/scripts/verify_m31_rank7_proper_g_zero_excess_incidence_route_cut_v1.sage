"""Independent Sage replay for the proper-G zero-excess route cut.

The deployed arithmetic is replayed with Sage exact integers.  A separate
GF(31) census checks the source-compatible counterfixture polynomial by
polynomial.  The toy family is not an M31 counterexample.
"""

from itertools import combinations


def need(condition, label):
    if not condition:
        raise AssertionError(label)


# Deployed exact-integer arithmetic.
K = ZZ(1_048_576)
RADIUS = ZZ(981_129)
W = ZZ(67_447)
G_MASTER = ZZ(354_972)
SIGMA = ZZ(282_544)
K_RESIDUAL = ZZ(4_981)

A5 = binomial(K + 5, 5) // binomial(W + 5, 5)
A5_PLUS = binomial(K + 5, 5) // binomial(W + 6, 5)
need(A5 == 908_021, "rank-five cap")
need(A5_PLUS == 907_953, "rank-five excess-one fallback")

full_num = binomial(693_610, 6)
full_den = binomial(67_453, 6)
need(full_num // full_den == 1_182_419, "full-P cap")

proper_num = binomial(698_589, 5)
proper_den = binomial(67_452, 5)
need(proper_num // proper_den == 119_177, "proper fixed-G cap")

proper_needed = ZZ(9_806_394 - 6_466_046 - 1_182_419)
need(proper_needed == 2_157_929, "proper mass")
need(ceil(proper_needed / ZZ(119_177)) == 19, "occupied slices")

pair_count = binomial(7, 2)
intersection_budget = pair_count * (K_RESIDUAL - 1)
union_sum = 6 * G_MASTER + 5 * intersection_budget
union_floor = union_sum // pair_count
overlap = G_MASTER - union_floor
need(intersection_budget == 104_580, "intersection budget")
need(union_sum == 2_652_732, "union sum")
need(union_floor == 126_320, "union floor")
need(overlap == 228_652, "forced overlap")


# Exact source-compatible GF(31) counterfixture.
F = GF(31)
PR.<X> = PolynomialRing(F)


def locator(roots):
    return prod((X - F(root) for root in roots), PR.one())


P_ROOTS = tuple(range(8))
L_ROOTS = tuple(range(8, 31))
S_ROOTS = (8,)
P = locator(P_ROOTS)
L = locator(L_ROOTS)
M = P * L

rows = []
records = []
proper_count = 0
full_count = 0
g_slices = set()

for m in range(2, 9):
    for g_roots in combinations(P_ROOTS, m):
        G = locator(g_roots)
        q_roots = tuple(sorted(set(P_ROOTS) - set(g_roots)))
        Q = locator(q_roots)
        extras = tuple(root for root in L_ROOTS if root != 8)
        for extra_h in combinations(extras, m - 1):
            h_roots = tuple(sorted(S_ROOTS + extra_h))
            if sum(g_roots) % 31 != sum(h_roots) % 31:
                continue
            H = locator(h_roots)
            b = G - H
            f = Q * b

            need(b.degree() < m - 1, "toy degree b")
            need(f.degree() < 7, "toy degree f")
            need(gcd(P, f).monic() == Q.monic(), "toy planted Q")
            need(gcd(L, P - f).monic() == H, "toy H")
            need(gcd(M, P - f).monic() == (Q * H).monic(), "toy full gcd")
            need(gcd(G, b) == 1, "toy canonical G-b")
            need(gcd(b, H) == 1, "toy b-H coprime")
            need(f(F(8)) == P(F(8)) != 0, "toy nonzero label")

            row = tuple(f[index] for index in range(7))
            rows.append(row)
            records.append((row, g_roots, q_roots, h_roots))
            g_slices.add(g_roots)
            if m == 8:
                full_count += 1
            else:
                proper_count += 1

need(len(rows) == 65_671, "toy total")
need(len(set(rows)) == len(rows), "toy distinct")
need(proper_count == 60_166, "toy proper count")
need(full_count == 5_505, "toy full count")
need(len(g_slices) == 235, "toy occupied G")
need(matrix(F, rows).rank() == 7, "toy linear rank")

anchor = vector(F, rows[0])
directions = [vector(F, row) - anchor for row in rows[1:]]
need(matrix(F, directions).rank() == 6, "toy direction rank")
direction_polys = [
    sum(direction[index] * X**index for index in range(7))
    for direction in directions
]
divided_directions = [
    polynomial // (X - F(8)) for polynomial in direction_polys
]
need(
    matrix(
        F,
        [[polynomial[index] for index in range(6)]
         for polynomial in divided_directions],
    ).rank() == 6,
    "toy divided direction is full",
)
need(
    all(
        any(polynomial(F(point)) != 0 for polynomial in divided_directions)
        for point in P_ROOTS + tuple(root for root in L_ROOTS if root != 8)
    ),
    "toy no common direction zero",
)
evaluation_columns = {
    tuple(F(point)**power for power in range(7))
    for point in L_ROOTS
}
need(len(evaluation_columns) == len(L_ROOTS), "toy complete singleton line")
need(set().union(*(set(roots) for roots in g_slices)) == set(P_ROOTS),
     "toy lcm restoration")

# Find an actual all-proper source basis greedily.
basis_indices = []
basis_rows = []
old_rank = 0
for index, record in enumerate(records):
    if len(record[1]) == len(P_ROOTS):
        continue
    trial = basis_rows + [record[0]]
    new_rank = matrix(F, trial).rank()
    if new_rank > old_rank:
        basis_indices.append(index)
        basis_rows.append(record[0])
        old_rank = new_rank
    if old_rank == 7:
        break

need(len(basis_indices) == 7, "toy proper source basis")
need(
    set().union(*(set(records[index][1]) for index in basis_indices))
    == set(P_ROOTS),
    "toy proper basis lcm",
)

# A pure-proper subfamily strictly below p-1 retains that actual basis.
subfamily_indices = list(basis_indices)
for index, record in enumerate(records):
    if len(subfamily_indices) == 29:
        break
    if index not in subfamily_indices and len(record[1]) < len(P_ROOTS):
        subfamily_indices.append(index)

need(len(subfamily_indices) == 29 < 30, "toy CRT-sized subfamily")
sub_rows = [vector(F, records[index][0]) for index in subfamily_indices]
sub_anchor = sub_rows[0]
need(matrix(F, sub_rows).rank() == 7, "toy subfamily linear rank")
need(
    matrix(F, [row - sub_anchor for row in sub_rows[1:]]).rank() == 6,
    "toy subfamily direction rank",
)
need(
    set().union(*(set(records[index][1]) for index in subfamily_indices))
    == set(P_ROOTS),
    "toy subfamily lcm",
)

# Every residual support has size seven.  If two supports intersected in
# six points, one six-subset would have two owners.
owners = {}
for index, (_, _, q_roots, h_roots) in enumerate(records):
    support = tuple(
        sorted(set(q_roots) | (set(h_roots) - set(S_ROOTS)))
    )
    need(len(support) == 7, "toy residual support size")
    for subset in combinations(support, 6):
        need(subset not in owners, "toy pair intersection above k-1")
        owners[subset] = index

print({
    "schema": "m31-rank7-proper-g-zero-excess-incidence-sage-v1",
    "deployed": {
        "rank_five_cap": int(A5),
        "rank_five_excess_one_fallback": int(A5_PLUS),
        "full_p_cap": int(full_num // full_den),
        "proper_fixed_g_cap": int(proper_num // proper_den),
        "proper_mass_needed": int(proper_needed),
        "occupied_slice_minimum": 19,
        "forced_pair_overlap": int(overlap),
    },
    "toy": {
        "field": 31,
        "total": len(rows),
        "proper_g": proper_count,
        "full_p": full_count,
        "distinct_g": len(g_slices),
        "linear_rank": 7,
        "direction_rank": 6,
        "z_zero": True,
        "complete_line_size": 1,
        "common_V": 1,
        "zero_excess": True,
        "lcm_restored": True,
        "pair_residual_intersection_at_most": 5,
        "pure_proper_crt_sized_subfamily": 29,
    },
})
