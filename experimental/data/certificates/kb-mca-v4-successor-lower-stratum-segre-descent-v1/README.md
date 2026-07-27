# KoalaBear successor lower-stratum Segre payment

This packet treats the lower reduced-degree stratum at the first currently
open slack:

```text
r = 67,473
|Sigma| = 134,946
e = 67,473
|Sigma| = 2e.
```

The forced-gcd branch is directly paid. In the one-extra-gcd branch, the
degree-`e+1` source space is the tensor product of the two-dimensional
source pencil with linear polynomials, and every actual complement locator
lies on its smooth Segre quadric.

Base span at most three and non-descended full base span are paid below the
current reserve. In the remaining descent case, the lower multiplier pencil
is intrinsically recovered inside the enlarged source space by the
`q, Xq` gate. Coefficient Frobenius preserves that gate and therefore
preserves the linear-multiplier ruling. The source quadric is necessarily
split, so this final branch is paid as well.

The largest conservative cap is

```text
267,576,636,738,137,856
```

with exact reserve margin

```text
3,203,576,222,438,024.
```

The complete lower stratum is paid with zero additional owner charge. The
row remains open only because the upper reduced-degree stratum still needs
its occupied-dimension-three spread-or-petal or occupied-dimension-four
rank-two collective-syzygy payment.

```bash
python3 experimental/scripts/verify_kb_mca_v4_successor_lower_stratum_segre_descent_v1.py --check
python3 experimental/scripts/verify_kb_mca_v4_successor_lower_stratum_segre_descent_v1.py --tamper-selftest
```

```text
payload            c0a5ea4569c6eddd72a1e43d88b8267b6cbfcb35f9af08a04fa1713a4d004017
partition digest   7a57fa877417920862ed2fe2e5c569852555f78b73b046d320d5e7a65d98ebaa
additional charge  0
nonsplit possible  false
lower paid         true
```
