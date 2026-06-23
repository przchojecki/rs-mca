# M1 Cycle116 Finite Chain Contract

Status: CONDITIONAL / AUDIT / FINITE-COMPUTATION-DEPENDENT.

Date: 2026-06-23.

This note records the finite proof chain that the Cycle120 ABF-facing audit
depends on. It is a reviewer contract, not a raw certificate bundle. It keeps
the chain split into:

```text
Cycle84 exact finite product occupancy
  -> fixed-jet locator-to-support-wise-MCA transfer
  -> smooth [512,256] field/domain lift
  -> ABF radius arithmetic from the Cycle120 contract.
```

The note imports the heavy Cycle84 finite census and the Cycle84 fixed-jet
instantiation as claims to be independently reviewed. It includes the abstract
fixed-jet transfer and the smooth padding lift because both are short enough to
audit directly.

## Finite Anchor

The Cycle84 finite certificate works over

```text
F0 = F_17[X] / (X^16 + X^8 + 3),
eta = 6 X^9,
beta = X + 2,
D0 = <eta>, |D0| = 256.
```

It asserts the exact product occupancy

```text
N = 52,747,567,092,
m_max(beta) = 2,
ordered off-diagonal energy D = 24,
12 double fibers,
no fibers of size >= 3.
```

The integrated repository note

```text
experimental/notes/m1/m1_cycle84_public_replay_audit.md
```

records the public replay metadata and keeps the result at status
`AUDIT / FINITE_MODEL_PROOF / PUBLIC_REPLAY`. The copied finite certificate in
the closed PR #96 branch should still be treated as an imported finite
computation until a reviewer reruns or independently checks it.

## Abstract Fixed-Jet Transfer

Let `D subset F`, `|D|=n`, let `beta notin D`, and let `J` range over a family
of `j`-subsets of `D`. Put

```text
P_J(X) = prod_{a in J}(X-a),
S_J = D \ J.
```

Assume all `P_J` have a common leading `sigma`-jet:

```text
deg(P_J - P_J') <= j - sigma
```

for all pairs in the family, and set

```text
k = n - j - sigma.
```

Then the complementary locators

```text
L_J(X) = prod_{a in S_J}(X-a)
```

have a common high-degree truncation in degrees strictly above `k`. Let `W` denote
that common truncation and put

```text
Q_J(X) = W(X) - L_J(X).
```

Then `deg Q_J <= k`. Define two received words on `D` by

```text
f(x) = W(x)/(x-beta),
g(x) = -1/(x-beta),
```

and for each `J` define

```text
z_J = Q_J(beta).
```

Since `Q_J(X)-Q_J(beta)` is divisible by `X-beta`, the polynomial

```text
c_J(X) = (Q_J(X)-z_J)/(X-beta)
```

has degree `< k`. On `S_J`, the locator `L_J` vanishes, so `Q_J=W` there, and

```text
c_J(x) = f(x) + z_J g(x)  for all x in S_J.
```

Thus the line point `f+z_J g` is explained by `RS[F,D,k]` on a support of size

```text
|S_J| = n-j = k+sigma.
```

The same support cannot simultaneously explain `f` and `g` by two codewords of
`RS[F,D,k]`: if `G` of degree `<k` agreed with `g` on `S_J`, then

```text
(X-beta)G(X) + 1
```

would be a nonzero polynomial of degree at most `k`, vanish on
`|S_J|=k+sigma>k` points, and take value `1` at `X=beta`, a contradiction.

Finally,

```text
z_J = W(beta) - L_J(beta)
    = W(beta) - V_D(beta)/P_J(beta),
```

where `V_D(X)=prod_{a in D}(X-a)`. Since `beta notin D`, `V_D(beta) != 0`.
Therefore distinct values of `P_J(beta)` give distinct bad line parameters
`z_J`.

Consequently, if the family has `M` distinct values `P_J(beta)`, then

```text
LD_sw(RS[F,D,k], k+sigma) >= M.
```

This is a support-wise line/MCA statement. It is not an ordinary list-decoding
lower bound.

## Cycle84 Native Instantiation

The Cycle116 packet claims that the Cycle84 family satisfies

```text
j = 113,
sigma = 6,
n = 256,
k = 256 - 113 - 6 = 137,
|S_T| = 143,
P_T(X) = X^113 - X^112 + O(X^107),
P_T(beta) = 4(beta - 1) Phi(T),
4(beta - 1) != 0.
```

Together with the Cycle84 occupancy `#{Phi(T)} = N`, the abstract transfer gives

```text
LD_sw(RS[F0,D0,137],143) >= N.
```

This native-row conclusion is conditional on the two Cycle116 import clauses:

```text
I1. the fixed six-jet identity for all Cycle84 locators P_T;
I2. the product-scalar identity P_T(beta)=4(beta-1)Phi(T).
```

The finite product census alone does not prove these identities.

## Slot-Block Bridge Reduction

The Cycle116 packet gives a more local form of the fixed-jet/product-scalar
instantiation. For each seven-state tuple `T=((i_t,a_t))_{t=1}^7`, the
co-support is

```text
J_T = {1} union union_{t=1}^7 eta^t Y_{i_t,a_t},
```

where each slot block has size `16` and the seven active cosets are disjoint.
Thus `|J_T|=1+7*16=113`. The imported finite slot identities are:

```text
R_{t,i,a}(X) = prod_{y in Y_{i,a}}(X - eta^t y)
             = X^16 + O(X^10),
R_{t,i,a}(beta) = 3^t u_t(i,a),
```

for all `t=1,...,7`, `i=1,2,3`, and `a=0,...,15`. Here
`X^16+O(X^10)` means that the coefficients of `X^15,...,X^11` vanish.

These 336 slot identities imply the two Cycle116 instantiation clauses without
any further finite search. Indeed,

```text
P_T(X) = (X-1) prod_{t=1}^7 R_{t,i_t,a_t}(X).
```

Let `Q_T=prod_t R_{t,i_t,a_t}`. Since every nonleading term in a block drops the
degree by at least `6`, one has

```text
Q_T(X) = X^112 + O(X^106).
```

Multiplying by `X-1` gives

```text
P_T(X) = X^113 - X^112 + O(X^107).
```

Likewise,

```text
P_T(beta)
= (beta-1) prod_{t=1}^7 R_{t,i_t,a_t}(beta)
= (beta-1) 3^(1+...+7) prod_{t=1}^7 u_t(i_t,a_t)
= 4(beta-1) Phi(T),
```

because `3^28=4` in `F_17`. Thus the current black-box part of the Cycle116
instantiation is narrower than the full fixed-jet/product-scalar statement:
it is exactly the 336 slot identities plus the Cycle84 occupancy certificate.

The companion verifier

```text
python3 experimental/scripts/verify_m1_cycle116_fixed_jet_bridge.py
```

checks this formal degree-support and scalar reduction. It does not verify the
336 slot identities themselves.

The 336 identities are replayed separately by

```text
python3 experimental/scripts/verify_m1_cycle116_slot_identities.py
```

That verifier works directly in `F_17[X]/(X^16+X^8+3)`. It recomputes the three
seed polynomials from

```text
E_1={0,1,2,3,5,11,12,13},
E_2={0,1,2,3,4,8,9,14},
E_3={0,1,2,4,5,7,11,14},
```

checks that their `Z^7` and `Z^6` coefficients vanish, forms all sets
`B_{i,a}=a+E_i mod 16`, and then checks all `7*3*16=336` block locators and
evaluations. It also emits a stable digest for the normalized slot table
`u_t(i,a)`:

```text
47ae84dc2df0fe0b4b43a7e0543b141fb940061fc48ccb80b40ce4e9483abc01
```

The remaining imported finite computation is the Cycle84 product occupancy
census for that normalized table.

## Cycle84 Color Shell And Energy Saturation

The companion verifier

```text
python3 experimental/scripts/verify_m1_cycle84_color_collision_witnesses.py
```

checks two further finite clauses for the same normalized slot table.

First, it computes the exact seven-slot color shell:

```text
#{T: color(T)=4 mod 16} = 52,747,567,104.
```

Second, it verifies six explicit product-collision pairs and their images under
the Cycle84 tau involution. These give:

```text
verified tau collision orbits = 6,
verified double fibers        = 12,
ordered off-diagonal energy   >= 24.
```

Thus the remaining heavy Cycle84 census can be stated as a sharp energy upper
bound for this normalized table:

```text
D <= 24,
```

where `D=sum_v m(v)(m(v)-1)` is the ordered off-diagonal product energy on the
color shell. If this imported upper bound holds, the verified witnesses saturate
all possible off-diagonal energy. Hence every nontrivial fiber is one of the
twelve verified double fibers, no fiber has size at least `3`, and

```text
#{Phi(T)} = 52,747,567,104 - 12
          = 52,747,567,092.
```

This is the exact numerator used downstream.

The kernel-lift filtering stage is checked by

```text
python3 experimental/scripts/verify_m1_cycle84_projected_log_certificate.py
```

and

```text
python3 experimental/scripts/verify_m1_cycle84_kernel_lift_candidates.py
```

The projected-log verifier checks the compact fixture
`experimental/data/witnesses/m1-cycle84/slot_logs.json`: all `336` slot logs
exponentiate back to the normalized slot values, their residue vectors are
correct, colors agree, and the tau-pair log sums are constant in each slot.

The kernel-lift verifier then checks all `30` projected duplicate-bin
candidates against the same normalized slot table. For each of the `60`
normalized witnesses it checks the color-shell condition, exponentiates the
supplied full log back to the finite-field product, verifies congruence modulo
`M=(17^16-1)/3`, and confirms that kernel difference `0` is exactly the
true-collision case. Its output is:

```text
projected duplicate bins checked = 30,
normalized witnesses checked     = 60,
true tau collision orbits        = 6,
true double fibers after tau     = 12,
true ordered energy after tau    = 24.
```

Therefore the remaining heavy Cycle84 import is now only the projected
tau-folded census completeness statement over the certified projected-log
table: the `30` projected duplicate bins listed in the kernel-lift verifier are
the complete projected duplicate list, and each has projected count `2`.

## Abstract Smooth Padding Lift

Let `C0=RS[F0,D0,k0]` and suppose a native support-wise bad-slope theorem gives
one line `f+z g` and, for each parameter `z` in a set `Z`, a support
`S_z subset D0` such that:

```text
|S_z| = a0,
f+z g is explained by C0 on S_z,
(f,g) is not simultaneously explained by C0 on S_z.
```

Let `K/F0` be an extension field, let `B` be a set of new evaluation points
disjoint from `D0`, and let `A subset B` have size `r`. Put

```text
H = D0 disjoint_union B,
L_A(X) = prod_{a in A}(X-a),
k = k0 + r.
```

Define lifted received words on `H` by

```text
F(x) = L_A(x) f(x)   for x in D0,
G(x) = L_A(x) g(x)   for x in D0,
F(a) = G(a) = 0      for a in A,
```

with arbitrary values on `B \ A`.

If `c_z` of degree `<k0` explains `f+z g` on `S_z`, then

```text
C_z(X) = L_A(X)c_z(X)
```

has degree `<k0+r=k` and explains `F+z G` on `S_z union A`. Hence every `z in Z`
has agreement at least

```text
a0 + r.
```

The lifted same-support noncontainment is lossless. If `P,Q` of degree `<k`
simultaneously explained `F,G` on `S_z union A`, then both `P` and `Q` would
vanish on `A`, so

```text
P = L_A p,   Q = L_A q
```

with `deg p, deg q < k0`. On `S_z`, the points avoid `A`, so `L_A` is nonzero
and `p,q` would simultaneously explain `f,g` on `S_z`, contradicting the
native noncontainment.

Therefore

```text
LD_sw(RS[K,H,k], a0+r) >= |Z|
```

with the same bad parameters `Z`.

## Smooth [512,256] Lift Contract

The Cycle116 lift uses the padding lemma after adjoining a square root of
`eta`:

```text
K = F0(theta), theta^2 = eta.
```

The companion verifier

```text
python3 experimental/scripts/verify_m1_cycle116_field_lift_contract.py
```

checks the field/lift envelope:

```text
X^16 + X^8 + 3 is irreducible over F_17;
eta has exact order 256 in F0^*;
eta is nonsquare in F0;
therefore K has size 17^32;
theta has exact order 512;
H=<theta> has size 512 and even powers recover D0=<eta>.
```

The field/lift setup is:

```text
H = D0 disjoint_union theta D0,
choose 119 fixed padding points in theta D0,
lift the native support of size 143 to a support of size 262,
raise the degree bound from <137 to <256,
preserve the same N bad line parameters and same-support noncontainment.
```

This is exactly the abstract padding lemma with:

```text
D0 = <eta>,          |D0| = 256,
B = theta D0,        |B| = 256,
A subset theta D0,   |A| = 119,
k0 = 137,
r = 119,
k = 256,
a0 = 143.
```

This gives the smooth row

```text
C = RS[F_17^32,H,256], |H| = 512,
LD_sw(C,262) >= N.
```

The support arithmetic is exact:

```text
143 + 119 = 262,
512 - 262 = 250,
256/512 = 1/2.
```

At `delta=125/256`,

```text
(1-delta)512 = 262.
```

Thus this is exactly the closed support threshold consumed in the Cycle120
ABF-facing contract.

## What Remains To Review

The chain is only as strong as the following imported clauses:

1. The Cycle84 finite product census really has
   projected tau-folded duplicate-bin completeness for the normalized slot
   table emitted by `verify_m1_cycle116_slot_identities.py`. The projected-log
   certificate, color shell, kernel-lift filtering, and twelve true
   double-fiber witnesses are now independently replayed by
   `verify_m1_cycle84_projected_log_certificate.py`,
   `verify_m1_cycle84_color_collision_witnesses.py`, and
   `verify_m1_cycle84_kernel_lift_candidates.py`.
2. The slot-block assembly really uses the co-support
   `{1} union union_t eta^t Y_{i_t,a_t}` with disjoint active cosets; the
   current slot-identity verifier checks the disjoint active-coset envelope.
3. The 336 Cycle116 slot identities continue to pass independent replay:
   `R_{t,i,a}(X)=X^16+O(X^10)` and
   `R_{t,i,a}(beta)=3^t u_t(i,a)`.
4. The field/lift envelope is correct: `F0(theta)` has size `17^32`, `theta`
   has order `512`, and `H=<theta>` decomposes as
   `D0 disjoint_union theta D0`.
5. The source-gate audit remains faithful to the official ABF text.

Failure of any clause should downgrade or revise the Cycle120 negative
certificate. If the first four clauses survive review, then the remaining
source question is whether the official challenge text admits the extension
field row and samples `gamma` from `F_17^32`, as recorded in
`m1_cycle120_abf_source_gate_audit.md`.

## Nonclaims

This note does not claim:

```text
ordinary list decoding;
protocol soundness failure;
an asymptotic theorem;
an accepted Proximity Prize solution;
a prime-field or deployed-row result;
independent replay of the Cycle84 heavy census;
independent proof of the Cycle84 fixed-jet instantiation.
```

It is the finite-chain contract that the next human or agent review should
either verify, repair, or falsify.
