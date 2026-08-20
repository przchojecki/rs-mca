#!/usr/bin/env sage
"""Independent exact replay of the SYZ25 overbudget-generation counterexample."""

F = GF(7)
points = [F(i) for i in range(6)]
k = 3
cores = [
    [0, 1, 4, 5],
    [0, 2, 3, 5],
    [1, 2, 3, 4],
]

G = matrix(F, [[x**j for x in points] for j in range(k)])


def supported_dual_basis(core):
    restricted = G.matrix_from_columns(core)
    rows = []
    for local in restricted.right_kernel().basis():
        row = vector(F, 6)
        for index, value in zip(core, local):
            row[index] = value
        rows.append(row)
    return rows


blocks = [supported_dual_basis(core) for core in cores]
assert [len(block) for block in blocks] == [1, 1, 1]

joint = matrix(F, [row for block in blocks for row in block])
full_dual = G.right_kernel()

assert G.rank() == k
assert full_dual.dimension() == 6 - k == 3
assert joint.rank() == 2
assert sum(len(core) - k for core in cores) == 3
assert len(set().union(*[set(core) for core in cores])) - k == 3

# The orthogonal complement of the two-dimensional joint span inside F^6
# has dimension four, one larger than the global degree-<k evaluation code.
# This is the local polynomial patching obstruction dual to the span defect.
assert joint.right_kernel().dimension() == 4
assert G.row_space().dimension() == 3
assert G.row_space().is_subspace(joint.right_kernel())

print(
    "KB_MCA_SYZ25_COPLANAR_CORE_CONTROL_PASS "
    "nominal=3 full=3 joint=2 deficiency=1 local_poly_dim=4"
)

# Positive incremental-overlap control.  Each new size-four core meets the
# running union in k=3 points, and the three one-dimensional supported-dual
# blocks generate the full shortened dual of their six-point union.
positive_cores = [
    [0, 1, 2, 3],
    [1, 2, 3, 4],
    [2, 3, 4, 5],
]
positive_rows = [
    row
    for core in positive_cores
    for row in supported_dual_basis(core)
]
positive_joint = matrix(F, positive_rows)
assert positive_joint.rank() == 3
assert len(set().union(*[set(core) for core in positive_cores])) - k == 3
print("KB_MCA_INCREMENTAL_OVERLAP_GENERATION_PASS joint=full=3")
