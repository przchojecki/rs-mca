# Row-sharp Q prefix atom route experiments v1

Status: `EXPERIMENTAL_EVIDENCE_NOT_A_PROOF`.

These are exact small-model experiments.  They do not prove the deployed
row-sharp Q theorem.

## Summary

- `bc_to_q_observation`: toy chart counts are controlled by multiplicity-weighted sums of ordinary prefix fibers; non-injective theta curves require multiplicity accounting
- `cases_with_nonretained_exact_lift_mass`: [{'case': {'j': 8, 'n': 16, 'p': 17, 'w': 1}, 'fiber_size': 758, 'nonretained': 688}, {'case': {'j': 8, 'n': 16, 'p': 17, 'w': 2}, 'fiber_size': 54, 'nonretained': 48}, {'case': {'j': 8, 'n': 16, 'p': 17, 'w': 3}, 'fiber_size': 7, 'nonretained': 5}, {'case': {'j': 5, 'n': 32, 'p': 97, 'w': 2}, 'fiber_size': 33, 'nonretained': 32}, {'case': {'j': 4, 'n': 64, 'p': 193, 'w': 2}, 'fiber_size': 32, 'nonretained': 31}, {'case': {'j': 3, 'n': 128, 'p': 257, 'w': 2}, 'fiber_size': 21, 'nonretained': 20}]
- `composite_descent_failures`: 0
- `composite_descent_observation`: gcd(e,N) fiber-factorization passed all checked finite regressions
- `generated_prefix_support_observation`: top finite fibers often split into multiple exact lift classes; support payment cannot be inferred from image labels
- `route_d_observation`: top fibers frequently have large nonzero signed folding defect; zero-defect descent alone is insufficient
- `top_seam_constant_diff_violations`: 0
- `top_seam_free_core_warning`: some unmarked side-pair keys have multiple common cores/mates, so marked incidence is the right object
- `top_seam_observation`: minimal Q1 collisions satisfy the constant side-polynomial condition in all checked cases

## Route D folding / primitive orbit diagnostics

- `F_17, n=16, j=8, w=1`: max=758, max primitive=757, max stabilized=758, nonempty fibers=17.
  top defect histogram: `{'0': 70, '4': 480, '6': 192, '8': 16}`
  top exact-lift diagnostic: `{'exact_lift_classes': 193, 'exact_prefix_depth_used': 1, 'fiber_size': 758, 'largest_exact_lift_class': 70, 'nonretained_after_largest': 688}`
- `F_17, n=16, j=8, w=2`: max=54, max primitive=49, max stabilized=54, nonempty fibers=289.
  top defect histogram: `{'0': 6, '4': 32, '8': 16}`
  top exact-lift diagnostic: `{'exact_lift_classes': 49, 'exact_prefix_depth_used': 2, 'fiber_size': 54, 'largest_exact_lift_class': 6, 'nonretained_after_largest': 48}`
- `F_17, n=16, j=8, w=3`: max=7, max primitive=5, max stabilized=7, nonempty fibers=4881.
  top defect histogram: `{'0': 3, '6': 4}`
  top exact-lift diagnostic: `{'exact_lift_classes': 6, 'exact_prefix_depth_used': 3, 'fiber_size': 7, 'largest_exact_lift_class': 2, 'nonretained_after_largest': 5}`
- `F_97, n=16, j=8, w=3`: max=6, max primitive=2, max stabilized=6, nonempty fibers=12457.
  top defect histogram: `{'0': 6}`
  top exact-lift diagnostic: `{'exact_lift_classes': 1, 'exact_prefix_depth_used': 3, 'fiber_size': 6, 'largest_exact_lift_class': 6, 'nonretained_after_largest': 0}`
- `F_97, n=32, j=5, w=2`: max=33, max primitive=33, max stabilized=26, nonempty fibers=9408.
  top defect histogram: `{'3': 6, '5': 27}`
  top exact-lift diagnostic: `{'exact_lift_classes': 33, 'exact_prefix_depth_used': 2, 'fiber_size': 33, 'largest_exact_lift_class': 1, 'nonretained_after_largest': 32}`
- `F_97, n=32, j=5, w=3`: max=7, max primitive=7, max stabilized=2, nonempty fibers=183936.
  top defect histogram: `{'1': 7}`
  top exact-lift diagnostic: `{'exact_lift_classes': 1, 'exact_prefix_depth_used': 3, 'fiber_size': 7, 'largest_exact_lift_class': 7, 'nonretained_after_largest': 0}`
- `F_193, n=64, j=4, w=2`: max=32, max primitive=32, max stabilized=27, nonempty fibers=37249.
  top defect histogram: `{'2': 3, '4': 29}`
  top exact-lift diagnostic: `{'exact_lift_classes': 32, 'exact_prefix_depth_used': 2, 'fiber_size': 32, 'largest_exact_lift_class': 1, 'nonretained_after_largest': 31}`
- `F_257, n=128, j=3, w=2`: max=21, max primitive=21, max stabilized=6, nonempty fibers=65792.
  top defect histogram: `{'1': 1, '3': 20}`
  top exact-lift diagnostic: `{'exact_lift_classes': 21, 'exact_prefix_depth_used': 2, 'fiber_size': 21, 'largest_exact_lift_class': 1, 'nonretained_after_largest': 20}`

## Top-seam marked incidence

- `F_17, n=16, j=8, w=1` skipped: pair budget `4865239`.
- `F_17, n=16, j=8, w=2`: minimal marked pairs=88704, max mates/support=20, constant-diff violations=0, max cores/unmarked sidepair=252.
- `F_17, n=16, j=8, w=3`: minimal marked pairs=8820, max mates/support=6, constant-diff violations=0, max cores/unmarked sidepair=70.
- `F_97, n=32, j=5, w=2`: minimal marked pairs=312000, max mates/support=10, constant-diff violations=0, max cores/unmarked sidepair=325.
- `F_97, n=32, j=5, w=3`: minimal marked pairs=9504, max mates/support=6, constant-diff violations=0, max cores/unmarked sidepair=24.
- `F_193, n=64, j=4, w=2` skipped: pair budget `5333720`.

## BC-to-Q toy chart checks

- `F_17, n=16, j=8, w=2`, `linear_first_coordinate`: sum=742, union=742, weighted=742, theta collisions=0.
- `F_17, n=16, j=8, w=2`, `moment_curve`: sum=742, union=742, weighted=742, theta collisions=0.
- `F_17, n=16, j=8, w=2`, `shifted_moment_curve`: sum=759, union=759, weighted=759, theta collisions=0.
- `F_97, n=32, j=5, w=3`, `linear_first_coordinate`: sum=256, union=256, weighted=256, theta collisions=0.
- `F_97, n=32, j=5, w=3`, `moment_curve`: sum=0, union=0, weighted=0, theta collisions=0.
- `F_97, n=32, j=5, w=3`, `shifted_moment_curve`: sum=19, union=19, weighted=19, theta collisions=0.
- `F_193, n=64, j=4, w=2`, `linear_first_coordinate`: sum=3408, union=3408, weighted=3408, theta collisions=0.
- `F_193, n=64, j=4, w=2`, `moment_curve`: sum=3408, union=3408, weighted=3408, theta collisions=0.
- `F_193, n=64, j=4, w=2`, `shifted_moment_curve`: sum=3315, union=3315, weighted=3315, theta collisions=0.

## Composite-prefix gcd descent regressions

- `F_17, n=16`: 6/6 gcd-descent factorizations passed.
- `F_97, n=32`: 7/7 gcd-descent factorizations passed.
- `F_193, n=64`: 8/8 gcd-descent factorizations passed.

## Interpretation

The experiments support Route D as the right next route, but also show
why it must be a large-defect transfer theorem rather than a zero-defect
or image-cell argument.  Top-seam collisions obey the expected side
normal form, but marked incidence is necessary.  Composite descent
behaves exactly with `gcd(e,N)`, matching the repaired theorem shape.
