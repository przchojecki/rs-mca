---
workboard_item: M1
row: Mersenne-31 list at 2^-100
object: LIST
target_epsilon: 2^-100
agreement: 1116023
B_star: 16777215
direct_statement: >-
  On the pinned c=2048, (u,v)=(0,1), p=2^31-1 quotient profile (punctured
  1022-label domain), the aligned depth-32 collision censuses enumerate only
  T16-aligned exchanges, raising the completeness question of whether every
  depth-32 collision of valid 479-supports is a union of intact T16 classes.
  The answer is negative. Two explicit valid 479-supports A, B collide through
  locator coefficient 39 and first differ at coefficient 40 (381197232 vs
  1671112725), with deficiency |A\B| = |B\A| = 192. In intact class T16(5) the
  anchor-only points are the eight-point half T8(5) and the neighbor-only
  points are the opposite half T8(251), so neither difference is a union of
  intact T16 classes and the collision is not T16-aligned. Independently, a
  union bound over supports fully partial in every intact class, pigeonhole
  over the p^32 depth-32 prefix targets, and a rational constant-intersection
  rank bound force a ragged collision with 34 <= e <= 479 without the explicit
  construction. Hence the aligned two-equation census is not a complete census
  of depth-32 collisions on this profile.
architecture: DIRECT_PINNED_C2048_U0_V1_QUOTIENT_PROFILE
partition_digest: N/A; support-level collision witness, no row atom banked
atom_or_cell: Q / PINNED_QUOTIENT_PREFIX_FIBER / T16_ALIGNMENT
quantifier: >-
  One explicit pair of valid 479-supports on the deployed 1022-label punctured
  quotient domain, plus an independent existence statement over the same
  domain.
projection_and_unit: >-
  Two 479-supports, their deficiency, the direct locator-prefix agreement
  depth, one partial intact T16 class, and the finite deployed class census.
  No received word, codeword, explanation, ray, slope, or row-list projection.
claimed_bound: >-
  deficiency = 192; exact prefix agreement depth = 39; coefficient-40 values
  381197232 and 1671112725; T16(5) difference intersections are the opposite
  eight-point halves T8(5), T8(251). Independent union bound G = C(1022,479) -
  62(C(1006,479)+C(1006,463)) with ceil(G/p^32) = 3,604,924 > 1,022, forcing a
  ragged collision with 34 <= e <= 479. New ragged floor: minimum ragged
  deficiency <= 192.
status: COUNTEREXAMPLE
impact: LOCAL_ONLY
falsifier: >-
  Either printed support has size other than 479, a duplicate, or a punctured
  label; deficiency other than 192; any of the first 39 locator coefficients
  differing between A and B; coefficient 40 agreeing; either class-5 difference
  intersection not equal to the printed opposite eight-point T8 half; or, on
  the counting side, an error in the deployed 62*16 + 30 = 1022 class census,
  a failure of the union-bound integers, more than p^32 depth-32 prefix
  targets, or more than 1022 rationally independent incidence vectors in
  Q^1022.
replay: >-
  Stdlib-only Lean kernel replay; no Python in the payload. Build target: cd
  experimental/lean/m31_t16_ragged_witness && lake build (requires the in-tree
  m31_quotient_t16_mixing_floor package). Kernel-checked: the explicit-witness
  conjunction (support validity, canonical order, both difference sets,
  deficiency 192, the printed depth-32 target, prefix equality at depth 39,
  inequality at depth 40, the two coefficient-40 values, and the partial
  T16(5) class), the signed opposite-half T8 relation, and the counting
  integer gates (the 62*16 + 30 class census, the three binomials, the union
  bound G, floor/mod/ceil of G by p^32, G > 1022 p^32, and the Gram boundary
  arithmetic). Proved in the note prose, not in Lean: the union bound itself,
  the pigeonhole step, the Newton exclusion of e <= 32, the rational
  constant-intersection rank bound, and the degree-439 construction mechanism.
  Tactic disclosure from the #print axioms census: of the ten theorems, nine
  reduce by native_decide and depth_and_rank_boundary_arithmetic uses ordinary
  decide; each native_decide theorem depends on its compiler-reduction axiom
  (theorem._native.native_decide.ax_1_1), two of them (signed_t8_relation_exact,
  explicit_ragged_collision) additionally on propext, and the decide theorem
  depends on no axioms. No sorry, admit, custom axiom, or
  Mathlib dependency.
consumers: >-
  M31 list-row census / floor work (the integrated band_mixing and
  t16_mixing_floor rooted-shell series and the aligned-collision census):
  supplies the first explicit non-aligned (ragged) depth-32 collision on the
  profile and an independent proof that the ragged sector is forced, delimiting
  the completeness of the aligned censuses and setting a ragged deficiency
  floor at e <= 192.
risk_limits: >-
  Support-level, pinned-profile scope only. The explicit witness facts are
  kernel-checked directly from the 479 roots; on the counting side only the
  finite census and the integer gates are kernel-checked, while the union
  bound, pigeonhole, Newton, and rational rank steps are elementary prose
  proofs. 192 is an upper bound on the minimum ragged deficiency, not claimed
  minimal; the minimum ragged deficiency, the census of signed opposite-half
  relations, and the non-aligned orbit structure remain open. No received-word,
  codeword, ray, or slope claim; no row-ledger movement and no M31 row closure.
---

# Explicit ragged depth-32 collision on the pinned M31 profile

## 1. The completeness question and its answer

On the pinned profile the aligned depth-32 collision censuses enumerate only
`T16`-aligned exchanges: exchanges whose two difference sets are unions of intact
`T16` classes.  They raise the natural completeness question.

> Is every depth-32 collision of valid 479-supports on the pinned profile
> `T16`-aligned?

The answer is negative.  Two explicit valid 479-supports `A`, `B` on the
deployed 1,022-label punctured quotient domain satisfy

```text
|A \ B| = |B \ A| = 192,
pref_39(A) = pref_39(B),
pref_40(A) != pref_40(B),
```

and inside intact class `T16(5)` the anchor-only points form the eight-point
half `T8(5)` while the neighbor-only points form the opposite half `T8(251)`, so
neither difference is a union of intact `T16` classes.  The pair is therefore a
depth-32 collision whose exact locator-prefix agreement depth is 39 and which is
not `T16`-aligned.

## 2. Frozen profile and notation

Put `p = 2^31 - 1 = 2147483647`.  Let `g = (1717986917, 1288490189)` be the
frozen norm-one generator in `F_p[i]`, and for odd `r`, `1 <= r <= 2047`, put
`q_r = 2^(-2047) Re(g^(r 2^19))` in `F_p`.  The pinned profile removes `q_1` and
`q_3`; its deployed domain is

```text
D = { q_r : r odd, 1 <= r <= 2047, r not in {1,3} },   |D| = 1022.
```

A support is printed by its odd representatives.  For a 479-support `S`, write
`V_S(Y) = prod (Y - q)` over `q in S` and let `pref_d(S)` be its first `d`
nonleading coefficients.  For two 479-supports `A`, `B`, write `X = A \ B`,
`Y = B \ A`, `e = |X| = |Y|`.  For odd `a`, the intact dyadic classes are

```text
T8(a)  = { q_r : r == a or -a (mod 512) },
T16(a) = { q_r : r == a or -a (mod 256) },
```

and every intact `T16` class splits as `T16(a) = T8(a) disjoint-union
T8(256 - a)`.  The depth-32 quotient-jet reduction `lem:newton-equivalence`
identifies equality of `pref_32` with equality of the first 32 power sums of `X`
and `Y`.

## 3. The two printed supports

### 3.1 Anchor support A

The SHA-256 of the comma-separated representative list with a trailing newline is
`228937e666705a41c9f20c8032e9b017f90af8060d8d19a4b5ea2dc28d1b4052`.

```text
A =
[
  5, 7, 15, 17, 19, 23, 25, 29, 31, 35, 39, 43, 47, 49, 51, 53,
  55, 59, 61, 65, 67, 69, 71, 73, 75, 77, 83, 85, 87, 89, 91, 93,
  95, 97, 99, 101, 103, 105, 107, 109, 111, 113, 115, 117, 119, 121, 123, 125,
  127, 129, 131, 133, 135, 137, 139, 141, 143, 145, 147, 151, 153, 155, 157, 163,
  165, 167, 169, 171, 173, 175, 177, 181, 183, 185, 187, 189, 193, 197, 199, 203,
  207, 209, 211, 213, 215, 217, 219, 221, 223, 227, 229, 231, 233, 235, 237, 241,
  243, 245, 247, 249, 253, 255, 257, 259, 263, 265, 267, 269, 271, 275, 277, 279,
  281, 283, 285, 289, 291, 293, 295, 297, 299, 301, 303, 305, 309, 313, 315, 319,
  323, 325, 327, 329, 331, 335, 337, 339, 341, 343, 345, 347, 349, 355, 357, 359,
  361, 365, 367, 369, 371, 373, 375, 377, 379, 381, 383, 385, 387, 389, 391, 393,
  395, 397, 399, 401, 403, 405, 407, 409, 411, 413, 415, 417, 419, 421, 423, 425,
  427, 429, 435, 437, 439, 441, 443, 445, 447, 451, 453, 457, 459, 461, 463, 465,
  469, 473, 477, 481, 483, 487, 489, 493, 495, 497, 505, 507, 509, 511, 513, 515,
  517, 519, 527, 529, 531, 535, 537, 541, 543, 547, 551, 555, 559, 561, 563, 565,
  567, 571, 573, 577, 579, 581, 583, 585, 587, 589, 595, 597, 599, 601, 603, 605,
  607, 609, 611, 613, 615, 617, 619, 621, 623, 625, 627, 629, 631, 633, 635, 637,
  639, 641, 643, 645, 647, 649, 651, 653, 655, 657, 659, 663, 665, 667, 669, 675,
  677, 679, 681, 683, 685, 687, 689, 693, 695, 697, 699, 701, 705, 709, 711, 715,
  719, 721, 723, 725, 727, 729, 731, 733, 735, 739, 741, 743, 745, 747, 749, 753,
  755, 757, 759, 761, 765, 767, 769, 771, 775, 777, 779, 781, 783, 787, 789, 791,
  793, 795, 797, 801, 803, 805, 807, 809, 811, 813, 815, 817, 821, 825, 827, 831,
  835, 837, 839, 841, 843, 847, 849, 851, 853, 855, 857, 859, 861, 867, 869, 871,
  873, 877, 879, 881, 883, 885, 887, 889, 891, 893, 895, 897, 899, 901, 903, 905,
  907, 909, 911, 913, 917, 927, 929, 947, 959, 963, 969, 973, 993, 1007, 1019, 1029,
  1041, 1055, 1075, 1079, 1085, 1089, 1101, 1119, 1121, 1131, 1199, 1201, 1217, 1223, 1235, 1239,
  1243, 1247, 1253, 1259, 1267, 1269, 1271, 1289, 1291, 1293, 1301, 1307, 1313, 1317, 1321, 1325,
  1337, 1343, 1359, 1361, 1429, 1439, 1441, 1459, 1471, 1475, 1481, 1485, 1505, 1519, 1531, 1541,
  1553, 1567, 1587, 1591, 1597, 1601, 1613, 1631, 1633, 1643, 1711, 1713, 1729, 1735, 1747, 1751,
  1755, 1759, 1765, 1771, 1779, 1781, 1783, 1801, 1803, 1805, 1813, 1819, 1825, 1829, 1833, 1837,
  1849, 1855, 1871, 1873, 1941, 1951, 1953, 1971, 1983, 1987, 1993, 1997, 2017, 2031, 2043
]
```

### 3.2 Neighbor support B

The corresponding representative-list SHA-256 is
`8c13ce7f1084e3e8f5b54ceeb560380c4c451196c9f6c0e84a5e1353c14147c7`.

```text
B =
[
  7, 9, 11, 13, 15, 19, 21, 23, 25, 27, 29, 33, 35, 37, 39, 41,
  43, 45, 47, 49, 53, 57, 59, 63, 67, 69, 71, 73, 75, 79, 81, 83,
  85, 87, 89, 91, 93, 99, 101, 103, 105, 109, 111, 113, 115, 117, 119, 121,
  123, 125, 127, 129, 131, 133, 135, 137, 139, 141, 143, 145, 147, 149, 151, 153,
  155, 157, 159, 161, 163, 165, 167, 169, 171, 173, 179, 181, 183, 185, 187, 189,
  191, 195, 197, 201, 203, 205, 207, 209, 213, 217, 221, 225, 227, 231, 233, 237,
  239, 241, 249, 251, 253, 255, 257, 259, 261, 263, 271, 273, 275, 279, 281, 285,
  287, 291, 295, 299, 303, 305, 307, 309, 311, 315, 317, 321, 323, 325, 327, 329,
  331, 333, 339, 341, 343, 345, 347, 349, 351, 353, 355, 357, 359, 361, 363, 365,
  367, 369, 371, 373, 375, 377, 379, 381, 383, 385, 387, 389, 391, 393, 395, 397,
  399, 401, 403, 407, 409, 411, 413, 419, 421, 423, 425, 427, 429, 431, 433, 437,
  439, 441, 443, 445, 449, 453, 455, 459, 463, 465, 467, 469, 471, 473, 475, 477,
  479, 483, 485, 487, 489, 491, 493, 497, 499, 501, 503, 505, 509, 511, 513, 515,
  519, 521, 523, 525, 527, 531, 533, 535, 537, 539, 541, 545, 547, 549, 551, 553,
  555, 557, 559, 561, 565, 569, 571, 575, 579, 581, 583, 585, 587, 591, 593, 595,
  597, 599, 601, 603, 605, 611, 613, 615, 617, 621, 623, 625, 627, 629, 631, 633,
  635, 637, 639, 641, 643, 645, 647, 649, 651, 653, 655, 657, 659, 661, 663, 665,
  667, 669, 671, 673, 675, 677, 679, 681, 683, 685, 691, 693, 695, 697, 699, 701,
  703, 707, 709, 713, 715, 717, 719, 721, 725, 729, 733, 737, 739, 743, 745, 749,
  751, 753, 761, 763, 765, 767, 769, 771, 773, 775, 783, 785, 787, 791, 793, 797,
  799, 803, 807, 811, 815, 817, 819, 821, 823, 827, 829, 833, 835, 837, 839, 841,
  843, 845, 851, 853, 855, 857, 859, 861, 863, 865, 867, 869, 871, 873, 875, 877,
  879, 881, 883, 885, 887, 889, 891, 893, 895, 897, 899, 901, 903, 905, 907, 909,
  911, 913, 943, 945, 961, 967, 979, 983, 987, 991, 997, 1003, 1011, 1013, 1015, 1033,
  1035, 1037, 1045, 1051, 1057, 1061, 1065, 1069, 1081, 1087, 1103, 1105, 1173, 1183, 1185, 1203,
  1215, 1219, 1225, 1229, 1249, 1263, 1275, 1285, 1297, 1311, 1331, 1335, 1341, 1345, 1357, 1375,
  1377, 1387, 1455, 1457, 1473, 1479, 1491, 1495, 1499, 1503, 1509, 1515, 1523, 1525, 1527, 1545,
  1547, 1549, 1557, 1563, 1569, 1573, 1577, 1581, 1593, 1599, 1615, 1617, 1685, 1695, 1697, 1715,
  1727, 1731, 1737, 1741, 1761, 1775, 1787, 1797, 1809, 1823, 1843, 1847, 1853, 1857, 1869, 1887,
  1889, 1899, 1967, 1969, 1985, 1991, 2003, 2007, 2011, 2015, 2021, 2027, 2035, 2037, 2039
]
```

Both lists are strictly increasing, avoid representatives 1 and 3, and contain
479 entries.  Their intersection is the 287-point common core; their two
differences are the 192-point exchanges.

## 4. Common depth-32 target and the partial class

The common first 32 nonleading coefficients are

```text
1855844193, 1473516259, 1180855483, 1278472540, 19420661, 1326549671, 185963244, 549194916, 1782472388, 540362367, 1873064133, 1262538111, 1676789978, 1180247279, 705606729, 896635126, 1579828831, 624675746, 1809833968, 679266634, 777394799, 1302213418, 902807383, 658621866, 543253585, 517492700, 226469049, 919947861, 1715697364, 1176419888, 1774114675, 433908075
```

The target-list SHA-256 is
`80f449b6060ecf884866bef71d58c94ce43a3028d19787a2ffca09644cf370bb`.

Direct multiplication of all 479 linear factors gives equality through
coefficient 39.  At coefficient 40 the values are

```text
A:  381197232,
B: 1671112725,
```

so the exact locator-prefix agreement depth is 39.

The printed ragged class is

```text
(A\B) intersect T16(5)
  = T8(5)
  = [5, 507, 517, 1019, 1029, 1531, 1541, 2043],

(B\A) intersect T16(5)
  = T8(251)
  = [251, 261, 763, 773, 1275, 1285, 1787, 1797].
```

Each list is a strict eight-point subset of the 16-point intact class `T16(5)`,
which is itself the disjoint union of these two opposite halves.  Neither
difference is a union of intact `T16` classes.

## 5. Construction mechanism

The exchange is generated by twenty-four paired `T8` half-classes:

```text
X8 = [5,247,245,243,17,235,229,31,223,219,215,211,
      51,55,199,61,193,65,77,177,175,95,97,107]

Y8 = [251,9,11,13,239,21,27,225,33,37,41,45,
      205,201,57,195,63,191,179,79,81,161,159,149].
```

Positionwise every pair sums to 256, so the two `T8` classes are the opposite
halves of one intact `T16` class.  Put `X` equal to the union of `T8(a)` over
`a in X8` and `Y` the union of `T8(b)` over `b in Y8`; these are disjoint
192-point sets.

Let `rho(a) = T_8(2 q_a)`.  Opposite halves have `rho(256 - a) = -rho(a)`.  The
selected parameters obey

```text
sum rho(a)   over X8  =  sum rho(b)   over Y8  =  0,
sum rho(a)^3 over X8  =  sum rho(b)^3 over Y8  =  0.
```

Even parameter moments agree automatically under negation, so the first four
power sums, hence the first four elementary symmetric functions, of the two
24-element parameter selectors agree.  Each complete `T8` locator is a monic
factor `H_8(Y) - lambda(a)`, where `lambda(a) = 2^(-15) rho(a)` is the common
nonzero scalar multiple of `rho(a)` fixed by monic normalization.  The
convention is

```text
prod (Y - q) over T8(a)  =  2^(-15) (T_8(2Y) - rho(a))  =  H_8(Y) - lambda(a),
```

with `H_8 = 2^(-15) T_8(2 . )` the monic degree-8 single-cosine polynomial.  The
products of 24 such factors therefore differ by a polynomial of degree at most
19 in `H_8`, hence degree at most `19 * 8 = 152` in `Y`.  The common core has
degree 287, so

```text
deg(V_A - V_B) <= 287 + 152 = 439.
```

Since both full locators are monic of degree 479, their first
`479 - 439 - 1 = 39` nonleading coefficients agree and coefficient 40 is the
first allowed to differ.  The direct computation shows that it does.  The signed
odd-moment relation was a search heuristic only; the certificate multiplies all
479 linear factors for both supports and checks the locator boundary directly
rather than trusting the mechanism.

## 6. Independent counting refutation

Independently of the explicit pair, a union-bound and constant-intersection
argument forces a ragged collision.  Let `Omega` be the family of 479-supports
whose occupancy in each of the 62 intact `T16` classes lies in `1,...,15`.  The
deployed domain is `62 * 16 + 30 = 1022`: 62 intact `T16` classes of size 16 and
two punctured classes contributing 30 labels.  A union bound over supports that
avoid or fill one intact class gives

```text
|Omega| >= G,
G = C(1022,479) - 62 (C(1006,479) + C(1006,463)),
```

whose exact value is

```text
150886973635117460711666662582071823255426867483739460042949200876631463792057929927793782975191438676548263027051602244578457442497949895482320221835127957642611301275002567366220049664612169911127650003991391433564620249245172975828229613540553529329728488495433266471149105032726785842900884268401364000.
```

There are at most `p^32` depth-32 prefix targets, and

```text
floor(G / p^32) = 3,604,923,   G mod p^32 != 0,   ceil(G / p^32) = 3,604,924 > 1,022,
```

so one depth-32 prefix fiber `F` inside `Omega` has at least 3,604,924 members.
If every distinct pair in `F` had deficiency 33, their incidence vectors
`v_i` in `Q^1022` would have `<v_i, v_i> = 479` and `<v_i, v_j> = 446`, i.e. Gram
matrix `33 I + 446 J`.  From a dependence with coefficients `c_i` summing to `S`,
pairing with `v_j` gives `33 c_j + 446 S = 0`, so all `c_i` equal a common `t`
with `(33 + 446 m) t = 0` and hence `t = 0`; the vectors are independent and
`|F| <= 1022`, contradicting `|F| >= 3,604,924`.  Therefore some pair has
deficiency other than 33.  The depth-32 Newton equivalence excludes deficiency at
most 32 (for `e <= 32` the first `e` power sums determine the exchange locator
and force the two difference sets to coincide), so the surviving pair has
`34 <= e <= 479`.  Each support in `Omega` is partial in every intact class and
only 30 deployed labels lie in the two punctured classes, so each difference set
meets an intact `T16` class partially: the collision is ragged.

## 7. Reconciliation with the aligned censuses

The witness does not contradict the aligned computations; it delimits their
scope.

- `experimental/notes/thresholds/m31_aligned_collision_census_v1.md` is an
  exhaustive census of the dyadic-fiber-aligned depth-32 exchanges rooted at one
  fixed 479-point band anchor: 49 collisions at `e = 64`, all whole-`T64`-block
  swaps, and none at the `T16` `e = 48` or `T8` `e = 40, 48, 56` slices.  It is
  per-anchor and per-aligned-slice, and it explicitly leaves the unrestricted
  non-aligned sector open.
- `experimental/notes/thresholds/m31_quotient_t16_mixing_floor.md` is a
  per-anchor deficiency-192 rooted shell: 1,225 whole-`T64` neighbours and 8
  `T16`-mixed neighbours, rooted degree 1,233.

Both remain correct in their stated slice and anchor.  The present witness has a
different anchor, deficiency 192, and non-aligned differences, so it shows that
the alignment restriction of those censuses is mathematically substantive rather
than incidental.

## 8. New floor

The explicit witness gives a new upper bound on the smallest non-aligned
deficiency:

```text
minimum ragged deficiency <= 192.
```

The counting argument places any forced ragged collision in `34 <= e <= 479`;
the Newton lower context is `e >= 33`.  The minimum ragged deficiency is not
determined, nor is the census of signed opposite-half relations or the
non-aligned orbit structure under quotient-domain symmetries.

## 9. Routes killed

1. **Universal `T16`-alignment completeness is false.**  The class-5 half swap
   is a direct falsifier.
2. **The aligned two-equation census is not an unrestricted census.**  It omits
   the signed `T8` odd-moment sector exhibited here.
3. **Fixed-anchor low-deficiency `T8` sweeps do not imply global `T8` absence.**
   This witness has a different anchor and `e = 192`.

## 10. Kernel-checked evidence and replay boundary

The stdlib-only Lean package is `experimental/lean/m31_t16_ragged_witness/`
(namespace `M31T16RaggedWitness`); build it with `cd
experimental/lean/m31_t16_ragged_witness && lake build`, which requires the
in-tree `experimental/lean/m31_quotient_t16_mixing_floor/` package.  The explicit
witness is checked by

```text
M31T16RaggedWitness.RaggedWitness.signed_t8_relation_exact
M31T16RaggedWitness.RaggedWitness.explicit_ragged_collision
M31T16RaggedWitness.RaggedWitness.t16_class_five_is_partial_on_both_sides
```

where `explicit_ragged_collision` checks support validity, canonical order, both
difference sets, deficiency 192, the printed depth-32 target, prefix equality at
depth 39, inequality at depth 40, the two coefficient-40 values, and the partial
`T16(5)` class, computing both locators directly from the 479 deployed roots.
The counting integers are checked by

```text
M31T16RaggedWitness.CountingRefutation.deployed_t16_partition_census
M31T16RaggedWitness.CountingRefutation.support_count_inputs_exact
M31T16RaggedWitness.CountingRefutation.fully_partial_lower_bound_exact
M31T16RaggedWitness.CountingRefutation.deployed_prefix_target_count_exact
M31T16RaggedWitness.CountingRefutation.fully_partial_prefix_pigeonhole_arithmetic
M31T16RaggedWitness.CountingRefutation.fully_partial_exceeds_constant_intersection_cap
M31T16RaggedWitness.CountingRefutation.depth_and_rank_boundary_arithmetic
```

Kernel-checked in Lean: the explicit-witness conjunction, the signed
opposite-half `T8` relation, and the counting integer gates (the class census,
the three binomials, the union bound `G`, its floor/remainder/ceiling by `p^32`,
`G > 1022 p^32`, and the Gram boundary arithmetic).  Proved in the prose above,
not in Lean: the union bound itself, the pigeonhole step, the Newton exclusion of
`e <= 32`, the rational constant-intersection rank bound, and the degree-439
construction mechanism.  From the `#print axioms` census: of the ten theorems,
nine reduce by `native_decide` and `depth_and_rank_boundary_arithmetic` uses
ordinary `decide`; each `native_decide` theorem depends on its compiler-reduction
axiom (`theorem._native.native_decide.ax_1_1`), two of them
(`signed_t8_relation_exact`, `explicit_ragged_collision`) additionally on
`propext`, and the `decide` theorem depends on no axioms.  There is no `sorry`,
`admit`, custom axiom, or Mathlib dependency.

## 11. Scope

- Pinned profile and support level only.
- No received-word, codeword, ray, slope, list-size, or row-ledger claim, and no
  M31 row-ledger movement.
- 192 is an upper bound on the minimum ragged deficiency, not claimed minimal.
- No assertion about how many ragged collisions exist at a fixed anchor.

# COUNTEREXAMPLE end
