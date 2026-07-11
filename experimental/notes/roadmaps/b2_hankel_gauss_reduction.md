# Hankel–Gauss reduction of the max-fiber crux (ChatGPT-5.6-Pro, 2026-07-11) — reduction VERIFIED, gap = CHG

Source: a ChatGPT-5.6-Pro proposal. STATUS: the EXACT REDUCTION (steps 1–5 below) is rigorous and was
INDEPENDENTLY re-verified here from scratch (`verify_chatgpt_hankel.py`, `rankcheck.py`, + its own scanner
`hankel_gauss_dense_rank_scan.py`). The remaining GAP is one conjecture (CHG); UNPROVEN but not falsified on toys.

## The reduction (VERIFIED exact)
1. INTERPOLATION reformulation. H=mu_n, R=F_p[X]/(X^n-1). Subset S -> interpolation poly f, coeffs
   alpha_r=(1/n)sum_{a in S}a^{-r}. Weight+syndrome fix c=w+1 coeffs (alpha_0=m/n, alpha_{n-j}=v_j/n, j=1..w);
   free coeffs alpha_1..alpha_d, d=n-w-1. Then N(v)=#{u in F_p^d : f_u(a) in {0,1} for all a in H}. [VERIFIED
   matches direct N(v), p=7 n=6 & p=11 n=5.]
2. QUADRATIC-delta FOURIER. 1_{{0,1}}(z)=(1/p)sum_lambda e_p(lambda(z^2-z)). =>
   N(v)=p^{-n} sum_{lambda in F_p^H} G_v(lambda), G_v(lambda)=sum_{u in F_p^d} e_p(u^T A_lambda u + l^T u + gamma),
   with (A_lambda)_{ij}=sum_a lambda_a a^{i+j} (a d x d cyclic HANKEL/catalecticant). |G_v|=0 or p^{d-rank/2}.
3. SPARSE ANNIHILATION (the key gain). For every |T|<=d: sum_{supp lambda=T} G_v(lambda)=p^d, INDEPENDENT of v.
   [VERIFIED exactly: 7^4=2401, 11^3=1331.] Proof: eval map onto F_p^T is surjective (row rank t<=d) => G_v=
   p^{d-t} prod g(lambda_a); and sum_{lambda!=0} g(lambda)=p.
4. CENTERING removes the coherent term EXACTLY. N(v)-mu = p^{-n} sum_lambda (G_v(lambda)-Gbar_m(lambda)); by (3)
   every support<=d layer cancels after centering. This kills a syndrome-independent term of scale
   p^{-c} sum_{t<=d} C(n,t) ~ n^{299} at deployment -- the reason naive rank-by-rank bounds were off by n^{299}.
5. RANK WINDOW. rank A_lambda=|supp| if |supp|<=d [VERIFIED]; >= 2d-n if |supp|>d (Sylvester). So only ranks
   r>=r_*:=2d-n=n-2w-2 survive: N(v)-mu = p^{-n} sum_{r=r_*}^{d} T_r(v), T_r=centered rank-r sum.

## The gap: CHG conjecture (UNPROVEN)
   |T_r(v)| <= p^{n+2+(r_*-r)/2}  for all v, r_*<=r<=d.   (square-root scale = p^{n+(r_*-r)/2}; p^2 is allowed loss)
Sufficient: gives N_max < (p^2/(1-p^{-1/2})+mu)/n^3 * n^3 = 0.493 n^3 < n^3 at deployment (only ~2x room, but ANY
fixed p^C loss => fixed poly bound since p=1016n+1). Cleanest first target (Eq 29, full-rank case):
   |T_d(v)| <= p^{n+2-(w+1)/2}   (complementary Hankel nonsingular, honest Schur complement, no pseudodet).

## Algebraic route (ChatGPT, plausible)
Rank defect of the d x d Hankel A_lambda = nullity of an ORDINARY Hankel B_{Z,lambda} of order <= c=w+1
(rank duality via ker E_T^T = im W, W_{a,u}=a^{u-1}/L_T'(a); B=W^T D^{-1} W is Hankel, (B)_{uv}=sum_{a in T} y_a
a^{u+v}). Determinant reciprocity: chi(det A) chi(det B)=chi(prod_{a in T} lambda_a). So CHG becomes a Fourier
estimate for ordinary Hankel rank strata with a determinant-character twist chi(pdet B) and an inverse-quadratic
phase e_p(Q_v(B^dagger)). MISSING TOOL = a "twisted Elkies formula": the Hankel rank-stratum Fourier transform
with those twists, poly loss, uniform in order. Existing: Elkies untwisted Hankel Fourier (arXiv math/0105007);
Dwivedi-Grinberg exact Hankel rank counts (2109.05415); Garcia Armas-Ghorpade-Ram Bezoutian (1011.1760).
General resultant character-sum bounds lose 2^{2a+2b} (unusable at a,b~w) -- so the twisted formula is genuinely new.

## UPDATE (2026-07-11): TWISTED NONSINGULAR TRANSFORM NOW AVAILABLE

`b2_twisted_hankel_transform_v1.md` proves the exact Fourier transform of

```text
chi(det B) e_p(-z^T B^{-1}z)
```

on the nonsingular ordinary Hankel stratum.  It converts the transform into a
signed square-plus-form projective-divisor sum using Elkies's singular-locus
formula.  Thus the full-rank transform itself is no longer a missing algebraic
identity.

`b2_full_rank_chg_normalization_bridge_v1.md` now proves the exact bridge from
the centered full-rank CHG term to the standalone transform, including the
`-4` inverse variables, determinant sign, complete scalar phase, support-wise
centering, coefficient Fourier pairing, and Salie product.  It also proves the
zero-fiber endpoint identification on every surviving `q>=1` full-rank
stratum.  This still does not prove Eq. 29 or CHG: the signed Hankel--Salie
aggregate estimate remains open, and lower-rank pseudodeterminant strata are
not covered.

## Verification status (this repo)
- Reduction steps 1,3,5 INDEPENDENTLY VERIFIED (verify_chatgpt_hankel.py, rankcheck.py). Steps 2,4 follow +
  scanner confirms centering (sparse error ~1e-10). REDUCTION IS SOLID.
- CHG: holds on ALL toys (R_max = max_{v,r} |T_r|/p^{n+(r_*-r)/2}): 8.6 (7,6,1,3), 9.2 (11,5,1,2), 6.6
  (13,6,1,3), 39.0 (13,6,2,3) -- all < p^2. NOT falsified. Toys too small (n<=6) to confirm asymptotically.
  Scanner is a FALSIFIER: if R_max ~ C^n at larger n, CHG is false. (p^n cost limits to n<=6-7.)

## NEXT STEPS (this is the sharpest open lead of the session)
1. Prove the normalized full-rank signed Hankel--Salie estimate printed in the bridge note.
2. Extend the transform or find a separate payment for lower-rank pseudodeterminant strata.
3. Push the scanner to the largest feasible n (n=7,8 with careful memory) to stress-test CHG's n-scaling.
4. Check whether the normalized aggregate connects to finite-field decoupling / discrete Brascamp--Lieb literature.
