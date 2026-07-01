# F17^32 M3 Rank-6 A386 Conic-Pair Safety

Status: PROVED / AUDIT.

This packet gives a projective-safety criterion for separated rank-6 boundary
buckets at

```text
A = 386.
```

The low-degree transfer has `h=3`, so the auxiliary `Q`-space is `P^2`.
Choose one direction node `y0` and two comparison nodes `y1,y2`.  The ratio
consistency equations give two plane conics

```text
F_i(Q) = Omega_{y_i} Q(y_i) b_{y0} L_Q(y0)
       - Omega_{y0} Q(y0) b_{y_i} L_Q(y_i),   i=1,2.
```

If these two conics have no common component over the algebraic closure, then
Bezout gives at most four `Q`-classes and hence at most four finite ambient
roots.  The split-locator gate cannot increase this count, and the
endpoint-uniform theorem contributes the single endpoint `[0:1]`, so the
support-wise projective total is at most

```text
4 + 1 = 5 <= 6.
```

Replay:

```sh
python3 experimental/scripts/verify_f17_32_m3_rank6_a386_conic_pair_safety.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a386-conic-pair-safety/f17_32_n512_k256_m3_rank6_a386_conic_pair_safety.json
```

Nonclaims:

```text
does not prove the no-common-component criterion for all A=386 weights;
does not cover A=385;
does not classify overlapping-support rank-6 pencils;
does not prove endpoint payment.
```
