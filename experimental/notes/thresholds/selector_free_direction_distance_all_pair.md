# Selector-free direction-distance compiler for all LineRay pairs

- **Status:** `PROVED` for the mathematical statements under the displayed weighted-Reed--Solomon chart hypotheses.
- **Object:** the full set of retained `(slope, witness)` pairs, including several witnesses at one slope.
- **Formal status:** `Lean UNPROVED STATEMENT TARGET`; the formalization section is a target map, not a Lean certificate.
- **Paper effect:** none. No stable TeX or PDF is changed.

The high-direction and minimum-lift predecessors selected one witness per retained slope. Their proofs admit a stronger interpretation. This note records it on the pair-count object required by the residual LineRay census, makes the realized punctured-word set explicit, and separates the proved rank implication from the conditional beyond-Johnson residual.

The direction-distance and minimum-lift arguments are due to Danny (DannyExperiments). The exact LineRay pair-count target and its distinction from slope count were calibrated by Latif Kasuli. The selector-free synthesis, affine-core comparison, and rational-host de-confliction were developed by holmbuar and the Codex team.

## 1. Weighted-RS setup and unconditional surjectivity

Let `F` be a finite field and let `U subseteq F` consist of `N=R+kappa` distinct points, where `R>=1` and `kappa>=1`. Fix nonzero weights `lambda_x` and parity columns

```text
h_x=lambda_x(1,x,...,x^(R-1))^T in F^R.
```

Define

```text
H:F^U -> F^R,       H(e)=sum_(x in U)e_x h_x,       K=ker H.
```

Every `R` columns form an invertible weighted Vandermonde matrix. Consequently

```text
H is surjective,
K is an [N,kappa,R+1] generalized Reed--Solomon code.       (1)
```

Thus every syndrome has an `R`-supported lift. No assumption about the number of realized slopes is needed to lift either line generator.

Fix `0<=t<R`, syndromes `y_0,y_1 in F^R`, and `y_1!=0`. Let `P` be any finite set of distinct pairs `(gamma,e) in F times F^U` satisfying

```text
H(e)=y_0+gamma y_1,                 wt(e)<=t.               (2)
```

For `S subseteq U` write `V_S=span_F{h_x:x in S}`. The low-direction theorem additionally assumes

```text
{y_0,y_1} not subseteq V_(supp(e))                         (3)
```

for every pair. First-match and ownership conditions may restrict `P` further; the proof never enlarges it to a generic image.

Define

```text
d=min{wt(v):H(v)=y_1}.                                    (4)
```

Surjectivity and `y_1!=0` give `1<=d<=R`.

## 2. High-direction all-pair theorem

Put

```text
D_H=(N-t)^2-N(N-d).                                       (5)
```

### Theorem 1 (one extension-code ball, with all multiplicities)

If `D_H>0`, then

```text
|P| <= floor(N(d-t)/D_H) <= N^2.                          (6)
```

This statement does not need transversality.

### Proof

Choose lifts `b_0,b_1` with `H(b_i)=y_i`. For `p=(gamma,e)`, write `e=b_0+gamma b_1+z_p` with `z_p in K`, and put

```text
c_p=-gamma b_1-z_p=b_0-e in L:=K+<b_1>.                  (7)
```

The map `p mapsto c_p` is injective. Equality first gives equal errors; applying (2) then gives `(gamma_p-gamma_q)y_1=0`, hence equal slopes. This replaces the predecessors' distinct-slope selector.

The code `L` has minimum distance exactly `d`: kernel words have weight at least `R+1>d`, nonkernel words rescale to `y_1`-lifts, and a minimum lift attains equality. Also `dist(c_p,b_0)=wt(e)<=t`.

Choose an `(N-t)`-subset `B_p` of the coordinates on which `c_p=b_0`. Distinct extension-code words give `|B_p intersect B_q|<=N-d`. The standard degree-square double count yields

```text
|P| <= N((N-t)-(N-d))/((N-t)^2-N(N-d)),
```

which is (6) after integer rounding.

## 3. Minimum-lift puncture on the realized pair set

Choose a minimum lift `v` and put

```text
J=supp(v),    |J|=d,    M=N-d,
Delta=R+1-d=M-kappa+1,    rho=min(t,M).                   (8)
```

Let `pi_J` puncture `J`. It is injective on `K`: a killed kernel word would have support at most `d<=R`, contradicting distance `R+1`. Hence `C_J=pi_J(K)` is an `[M,kappa,Delta]` GRS code. Puncturing also maps `S_0={u:H(u)=y_0}` injectively onto an affine coset `A` of `C_J`.

For `p=(gamma,e)` define

```text
u_p=e-gamma v in S_0,        w_p=pi_J(u_p)=pi_J(e),
W_P={w_p:p in P}.                                             (9)
```

Every realized word lies in `A` and has weight at most `rho`, but `W_P` need not equal the whole low-weight coset list. For `w in W_P` put

```text
P_w={p in P:w_p=w},       h(w)=max(1,d+wt(w)-t).           (10)
```

### Theorem 2 (exact realized-cluster reduction)

```text
|P_w| <= floor(d/h(w)),                                    (11)

|P| = sum_(w in W_P)|P_w|
    <= sum_(w in W_P) floor(d/max(1,d+wt(w)-t)).           (12)
```

Consequently the larger affine-coset sum is also valid:

```text
|P| <= sum_(w in A, wt(w)<=rho)
         floor(d/max(1,d+wt(w)-t)).                        (13)
```

### Proof

Fix `w in W_P`. Injectivity of `pi_J` on `S_0` gives one lift `u_w`, so every cluster pair has `e=u_w+gamma v`. Distinct pairs in the same cluster have distinct slopes. Thus same-slope multiplicity is retained: distinct errors at one slope necessarily have different realized words.

Write `j=wt(w)`. Outside `J` the error has exactly `j` nonzeros, so its weight bound forces at least `d+j-t` zeros on `J` when positive. Even otherwise there is one zero: if not, both `u_w` and `v` are supported inside `supp(e)`, contradicting (3).

For each `x in J`, the equation `u_w(x)+gamma v(x)=0` has at most one solution since `v(x)!=0`. The cluster has at most `d` zero incidences and every pair consumes at least `h(w)`. This proves (11)--(13).

## 4. Realized parallel-pencil rank

Assume `P` is nonempty, fix `p_*=(gamma_*,e_*)`, and define

```text
sigma(P)=dim span_F{e-e_*:(gamma,e) in P}.                 (14)

alpha(W_P)=dim span_F{w-w_*:w in W_P},
```

where `w_*` is the realized word of `p_*`; equivalently,
`alpha(W_P)` is the affine dimension of the realized-word set.

### Theorem 3 (rank uses realized words only)

```text
sigma(P)<=alpha(W_P)+1<=|W_P|.                             (15)
```

Indeed, after choosing one lift `u_w` for each realized word,

```text
e-e_*=(u_w-u_(w_*))+(gamma-gamma_*)v.
```

The differences `u_w-u_(w_*)` lie in `K`, and puncturing maps their span
isomorphically to the span of the differences `w-w_*`. Thus that lift-difference
span has dimension `alpha(W_P)`. All error differences lie in its sum with
`<v>`, proving the first inequality; the second is the elementary affine bound
`alpha(W_P)<=|W_P|-1`. The structural theorem uses the realized set, not the
full coset list.

## 5. Punctured Johnson corollary

Let

```text
A_(<=rho)={w in A:wt(w)<=rho},
D_J=Delta M-2rho M+rho^2=(M-rho)^2-M(kappa-1).             (16)
```

### Theorem 4 (field-independent polynomial payment)

If `D_J>0`, then

```text
|W_P| <= |A_(<=rho)| <= floor(M(Delta-rho)/D_J),           (17)
|P| <= d floor(M(Delta-rho)/D_J) <= N^3,                  (18)
sigma(P) <= floor(M(Delta-rho)/D_J).                       (19)
```

### Proof

Each low-weight coset word has at least `M-rho` zeros. Distinct words differ by a codeword of weight at least `Delta`, so their zero masks intersect in at most `M-Delta=kappa-1` coordinates. The elementary Johnson count gives

```text
|A_(<=rho)|
 <= M((M-rho)-(kappa-1))/((M-rho)^2-M(kappa-1))
 = M(Delta-rho)/D_J.
```

Equations (11) and (15) give the remaining claims.

## 6. Exact residual contract

The two polynomial branches leave only

```text
D_H<=0,                 D_J<=0.                            (20)
```

The packet does **not** assert that a chart in (20) has linear or non-sublinear affine rank. It proves only

```text
|P|<=d|W_P|,            sigma(P)<=|W_P|.                  (21)
```

Thus an exponential pair family forces an exponential realized punctured list. If a separate theorem proves that `sigma(P)` is not `o(N)`, then (15) conditionally forces a non-sublinear realized list; under a separate `sigma(P)=Omega(N)` hypothesis, the coset contains `Omega(N)` realized low-weight words. These are conditional implications, not conclusions about every unpaid chart.

## 7. Exact fixtures

### 7.1 An F_5 same-slope collision

Take `U={0,1,2,3,4} subset F_5`, `R=3`, `kappa=2`, `t=2`, and `h_x=(1,x,x^2)^T`. Let

```text
e =(0,4,3,0,0),       e'=(0,0,0,3,4).
```

Then

```text
H(e)=H(e')=(2,0,1),      e-e'=(0,4,3,2,1) in K.
```

Set `y_0=(2,0,1)` and `y_1=h_0=(1,0,0)`. The pairs `(0,e)` and `(0,e')` have one slope but two witnesses. Both are transverse because any three parity columns are independent. Puncturing the minimum lift at coordinate zero gives distinct realized words `(4,3,0,0)` and `(0,0,3,4)`. This rejects a hidden one-witness-per-slope selector. Here `D_J=0`, so the fixture tests (12), not the strict Johnson corollary.

### 7.2 A complete hosted F_11 puncture fixture

Take `U={0,...,8} subset F_11`, `N=9`, `R=8`, `kappa=1`, `t=4`, and `h_x=(1,x,...,x^7)^T`. A kernel generator is

```text
omega=(9,5,10,2,3,2,10,5,9).
```

Choose

```text
v=(0,0,0,0,0,0,0,10,1),
u=(0,0,0,0,0,0,0,0,10).
```

Then

```text
d=2, J={7,8},
y_0=H(u)=(10,3,2,5,7,1,8,9),
y_1=H(v)=(0,1,4,4,1,0,10,7).
```

Exhausting `u+gamma v+a omega` over `gamma,a in F_11` shows that the complete transverse weight-at-most-four pair set is

```text
(0,u),
(1,u+v)=(1,(0,0,0,0,0,0,0,10,0)).
```

Both puncture to zero on the seven outside coordinates. Hence `W_P={0}`, the cluster has size two, and (11) is sharp:

```text
floor(2/max(1,2+0-4))=2.
```

Here

```text
M=7, Delta=7, rho=4, D_H=-38, D_J=9,
|A_(<=rho)|<=floor(7*3/9)=2.
```

The high branch fails, the realized bound is exact, the coarse bound is `|P|<=4`, and `sigma(P)=1<=|W_P|=1`.

### 7.3 A positive-rate RS family

For every `m>=5` take

```text
N=9m, R=8m, kappa=m, t=4m, d=2m,
M=7m, Delta=6m+1, rho=4m.                                 (22)
```

Then

```text
D_H<0,       D_J=m(2m+7)>0,
|W_P|<=floor(7(2m+1)/(2m+7))<=6,
|P|<=12m,    sigma(P)<=6.                                 (23)
```

These parameters occur in weighted-RS geometry. In the representation

```text
K={(omega_x p(x))_(x in U):deg p<m},
```

choose a `7m`-set `T_0` and put `v(x)=omega_x product_(a in T_0)(x-a)`. Its support `J` has size `2m`, and its degree proves `d=2m`. Assign distinct `gamma_x` on `J` and choose `u` to vanish on `T_0` with `u(x)=-gamma_xv(x)` on `J`. At slope `gamma_x`, the witness is supported on `J minus {x}`. The representation `y_1=H(v)` on `J` uses all `2m` nonzero coefficients; since `2m<=R` and every at-most-`R` set of parity columns is independent, that representation is unique and `y_1` is not in `V_(J minus {x})`. Hence all `2m` witnesses are transverse. They have `W_P={0}`, and the exact realized bound (12) is `2m` and is attained.

At `m=5`, the uniform bound reads

```text
N=45, R=40, kappa=5, t=20, d=10,
|W_P|<=4, |P|<=40, sigma(P)<=4,
```

while the planted family has ten pairs and one realized word. The old high-direction condition and `3t<=R` both fail.

## 8. Comparison with neighboring packets

`direction_distance_large_kernel_ray_compiler.md` proves the high-direction inequality after choosing one witness per slope; Theorem 1 replaces the selector with (7). `low_direction_minimum_lift_puncture.md` proves the puncture charge for selected slopes; Theorem 2 counts every pair because same-puncture pairs have distinct slopes and same-slope pairs have distinct punctures.

Latif Kasuli's LineRay census re-recording identifies the with-multiplicity `(slope,witness)` count as the residual target. This note pays two regions of that object, not the complete census target.

The all-LineRay affine-core set-pair packet proves global and nested Bollobas-type charges using actual ranks and supports. It pays small global rank, or small selector and same-slope fiber ranks. The present theorem is complementary: it pays direction-Johnson regions independently of those ranks, and (15) connects its realized decomposition back to the affine core. Neither subsumes the other.

The section-nonpositive rational-host packet proves that general lines need not admit its reduced host presentation. There is no conflict: this theorem assumes an actual weighted-RS chart and neither extracts a host nor asserts atlas coverage.

## 9. Reproducibility and formalization contract

The predecessor checks are

```bash
python3 experimental/scripts/verify_direction_distance_ray_compiler.py
python3 experimental/scripts/verify_low_direction_minimum_lift_puncture.py
```

The companion all-pair verifier and certificate are intended at

```text
experimental/scripts/verify_selector_free_direction_distance_all_pair.py
experimental/data/certificates/selector-free-direction-distance-all-pair/
  selector_free_direction_distance_all_pair.json
```

Required commands are

```bash
python3 experimental/scripts/verify_selector_free_direction_distance_all_pair.py --check
python3 -O experimental/scripts/verify_selector_free_direction_distance_all_pair.py --check
python3 experimental/scripts/verify_selector_free_direction_distance_all_pair.py --tamper-selftest
python3 -O experimental/scripts/verify_selector_free_direction_distance_all_pair.py --tamper-selftest
python3 -m json.tool experimental/data/certificates/selector-free-direction-distance-all-pair/selector_free_direction_distance_all_pair.json
PYTHONPYCACHEPREFIX=/tmp/selector-free-direction-pycache python3 -m py_compile experimental/scripts/verify_selector_free_direction_distance_all_pair.py
```

The verifier must retain every witness, construct `W_P`, check every cluster,
(12), (15), its three pinned finite fixtures, exhaustive sweep coverage of the
displayed `F_5` collision, and the positive-rate arithmetic in (22)--(23). The
construction proof in Section 7.3 remains mathematical rather than an exhaustive
finite computation. The verifier also rejects all eighteen pinned tamper classes.
It supports the proof but does not replace it.

The Lean statement target is present at

```text
experimental/lean/grande_finale/GrandeFinale/DirectionDistanceAllPairs.lean
```

with the direct check, from that package,

```bash
lake env lean GrandeFinale/DirectionDistanceAllPairs.lean
```

The target should state the extension-word injection, realized fibers, same-fiber slope injection, zero-incidence inequality, parallel-pencil dimension bound, and Johnson arithmetic. It remains `Lean UNPROVED STATEMENT TARGET`: definitions or a successful statement check do not formalize the field-linear, MDS, transversality, or Johnson proofs here.

## 10. Ledger effect and nonclaims

For one fixed actual chart, Theorem 1 or 4 gives a field-independent polynomial payment on the full LineRay pair count. This is a local result only.

This note does **not**:

- prove a witness-exhaustive first-match atlas or aggregate chart count;
- prove rational-host extraction or coverage of the non-host stratum;
- pay every chart satisfying (20);
- assert that an unpaid chart has non-sublinear or linear affine rank;
- prove a beyond-Johnson affine-GRS list theorem;
- prove the complete LineRay census target;
- prove a profile-envelope, lower-reserve, or target comparison;
- alter a finite M31 or KoalaBear deployed row;
- transfer a count between generated, line, challenge, or list fields;
- change any stable paper TeX or PDF;
- claim Lean certification for the statement target.

The exact next local problem is to control the realized weighted sum (12) on the double-nonpositive locus (20), or route those charts to separately proved owners without losing witnesses.
