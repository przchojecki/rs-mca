# M1 Smooth-Padding LDsw Transfer Theorem

Status: PROVED / AUDIT / SMOOTH-PADDING-LDSW-THEOREM.

Date: 2026-06-24.

This note isolates the generic theorem behind the Cycle116-to-Cycle120 smooth
padding step. It is independent of the special `F_17^32` arithmetic: once a
native support-wise bad line is known, padding by a fixed vanishing locator
preserves the same bad parameters and increases the agreement support.

The companion verifier is:

```text
python3 experimental/scripts/verify_m1_smooth_padding_ldsw_theorem.py
```

It constructs exact finite-field toy bad lines, pads them, and checks agreement
and noncontainment directly.

## Theorem

Let `D` be a code domain and let `C=RS[F,D,k]`. Suppose a fixed line `f+z g`
has a set `Z` of support-wise bad parameters, where each `z in Z` has an
agreement support `S_z subset D` of size at least `a`.

Let `A` and `R` be disjoint from `D` and from each other, and put

```text
H = D union A union R,
k_plus = k + |A|,
L_A(X)=prod_{x in A}(X-x).
```

Define lifted words on `H` by

```text
f_plus(x)=L_A(x) f(x),   g_plus(x)=L_A(x) g(x)  for x in D,
f_plus(x)=g_plus(x)=0                         for x in A,
```

with arbitrary values on `R`. Then the same parameters `Z` are support-wise bad
for `RS[F,H,k_plus]` on the supports

```text
S_z_plus = S_z union A.
```

Thus

```text
LD_sw(RS[F,H,k_plus], a+|A|) >= |Z|.
```

## Proof

For a bad native parameter `z`, let `c_z` be a degree-`<k` codeword explaining
`f+z g` on `S_z`. Then

```text
L_A c_z
```

has degree `<k+|A|` and explains `f_plus+z g_plus` on `S_z union A`. On `D`
this is multiplication by `L_A`; on `A` both sides vanish.

For noncontainment, suppose degree-`<k+|A|` polynomials explain both lifted
words on `S_z union A`. Both polynomials vanish on every point of `A`, so each
is divisible by `L_A`. Dividing by `L_A` gives degree-`<k` polynomials
explaining the native pair `(f,g)` on `S_z`, contradicting native
support-wise noncontainment.

The points in `R` are deliberately unused by the agreement support; they only
increase the co-support and domain size. This is exactly the role of the odd
coset block `R` in the Cycle120 row.

## Cycle116/Cycle120 Instantiation

The concrete M1 padding has:

```text
native: n=256, k=137, agreement=143, co-support=113,
A size: 119,
R size: 137,
lifted: n=512, k=256, agreement=262, co-support=250.
```

The size identities are:

```text
143 + 119 = 262,
137 + 119 = 256,
113 + 137 = 250.
```

The concrete field/domain facts, including

```text
H=<theta>=D0 disjoint_union theta D0,
A={theta eta^i:0<=i<=118},
R={theta eta^i:119<=i<=255},
P_A(beta) != 0,
P_R(beta) != 0,
```

are still checked by:

```text
python3 experimental/scripts/verify_m1_cycle116_smooth_padding_transfer.py
```

The generic theorem here explains why those concrete checks preserve the
native bad parameters in the ABF-facing `[512,256]` row.

## Remaining Imports

This theorem does not prove the native Cycle116 bad-line theorem or the
Cycle84 count. It consumes those upstream results and proves that the smooth
padding step loses no bad parameters.
