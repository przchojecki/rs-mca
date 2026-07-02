# Hankel Rank-6 A385 Pair-Core Cauchy-Moment Normal Form

Status: PROVED / AUDIT.

This note unpacks the external-evaluation rows in the `A=385` pair-core rank
test.

Work in the separated boundary transfer with

```text
j = 127,        m = 128,        h = 5.
```

Let `X` be the base support, `|X|=128`, and write

```text
P_X(T) = prod_{x in X} (T-x),
W_x = Omega_x/a_x.
```

The weights `W_x` are nonzero.  For

```text
Q(T) = q_0 + q_1 T + q_2 T^2 + q_3 T^3 + q_4 T^4,
```

the transferred polynomial `L_Q` is the unique degree-`<128` polynomial with

```text
L_Q(x) = W_x Q(x)        for x in X.
```

Thus for an external point `s notin X`,

```text
L_Q(s)
  =
  sum_{x in X} W_x Q(x) P_X(s)/((s-x)P_X'(x)).
```

In the monomial basis `1,T,T^2,T^3,T^4`, the row `ev_s(Q)=L_Q(s)` therefore has
coordinates

```text
c_r(s) = P_X(s) sum_{x in X} W_x x^r/((s-x)P_X'(x)),
0 <= r <= 4.
```

Since `s` is external, `P_X(s) != 0`; removing this nonzero row factor does not
change matrix rank.  Define the reduced Cauchy-moment row

```text
d_r(s) = sum_{x in X} W_x x^r/((s-x)P_X'(x)).
```

For an external core `E`, the reduced matrix factors as

```text
D_E = C_{E,X} diag(W_x/P_X'(x)) V_X,
```

where

```text
C_{s,x} = 1/(s-x),
V_{x,r} = x^r,        0 <= r <= 4.
```

The rank-test packet says a pressure-forced pair-core survivor needs

```text
rank D_E <= 3
```

for some external set `E` of size at least `24`.  Equivalently, every `4 x 4`
minor of `D_E` vanishes.

By Cauchy-Binet, for rows `S={s_1,...,s_4}` and columns
`R={r_1<...<r_4} subset {0,1,2,3,4}`,

```text
det D_{S,R}
  =
  sum_{T subset X, |T|=4}
    det(1/(s_i-x))_{s_i in S, x in T}
    det(x^r)_{x in T, r in R}
    prod_{x in T} W_x/P_X'(x).
```

This is the concrete determinant target for the no-fixed-core pair-core
frontier.  The next proof attempt should attack these weighted Cauchy-moment
minor equations directly, or else construct a minimal rank-`<=3` witness and
route it through the split-locator and paid-ledger gates.

Replay:

```sh
python3 experimental/scripts/verify_f17_32_m3_rank6_a385_pair_core_cauchy_moment.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a385-pair-core-cauchy-moment/f17_32_n512_k256_m3_rank6_a385_pair_core_cauchy_moment.json
```

Nonclaims:

```text
no closure of the no-fixed-core A=385 frontier;
no proof that rank<=3 Cauchy-moment cores of size 24 are impossible;
no proof that rank<=3 Cauchy-moment cores of size 24 are paid;
no specialization of the arbitrary nonzero base weights W_x;
no split-locator witness from the matrix rank condition;
no overlapping-support rank-6 classification;
no row-level M3 safe-side bound.
```
