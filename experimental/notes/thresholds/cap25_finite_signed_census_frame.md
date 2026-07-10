# The signed census frame: sign quantization, exact identities, and
# the L-function diagonalization

- **Status:** PROVED (four theorems + exact identities; one-paragraph
  proofs included; machine verifiers).
- **Track:** the FINITE prize. Safe to park until the finite pivot.
- **Source:** the fork's finite-track campaign (satellites 16-21 of
  the F2 program); full record with 30+ verifiers at
  https://github.com/AllenGrahamHart/rs-mca-prize-dag
- **Verifier:** `python3 experimental/scripts/verify_finite_signed_census_frame.py`

## Setting

q an odd prime (theorem 4 lifts to q = p^k), N a 2-power with
N | q - 1, D = mu_N <= F_q^x. For c in F_q^j and x in D put
s_x(c) = sum_i c_i x^i mod q (representatives in [0, q)),
psi(s) = e^{2 pi i s / q}. The census N_b^{(j)} counts size-b
subsets with vanishing p_1..p_j; N^{(j)} the all-sizes total.

## Theorem 1 (census-Fourier split + SIGN QUANTIZATION)

prod_{x in D}(1 + psi(s_x(c))) = eps_c * e^{S_c} is a SIGNED REAL:
S_c = sum_x log|1 + psi(s_x)|, and the phase is pi-quantized with
  eps_c = (-1)^{K_c + U_c},
  K_c = (sum_x s_x)/q  (an integer: power sums of D vanish below
  index N),  U_c = #{x : s_x > q/2}.
PROOF. arg(1 + e^{i theta}) = theta/2 on (-pi, pi) and psi never
equals -1 at odd q; summing, the total phase is pi((sum s_x)/q -
U_c + U_c ... ) = pi(K_c) modulo the U_c half-turns — i.e. an
integer multiple of pi with parity K_c + U_c. QED.

## Theorem 2 (the exact census identity)

  sum_{c != 0} eps_c e^{S_c} = q^j N^{(j)} - 2^N.
PROOF. Orthogonality on prod(1 + psi) = sum_T psi(c . m(T)). QED.

## Theorem 3 (the ladder identity — the variance is an integer)

  sum_{c != 0} e^{2 S_c} = q^j C'' - 4^N,
where C'' = sum over delta in {0,+1,-1}^N with vanishing moments
p_1..p_j of 2^{#zeros(delta)} (the weighted signed-trade census,
an integer computable by exact DP). PROOF. |1+psi|^2 =
2 + psi + conj(psi); expand and apply orthogonality. QED.
REMARK. At N = 64 the two sides agree to 62+ significant bits
(their difference IS the census deviation): float verification is
categorically impossible; exact integers are mandatory.

## Theorem 4 (tower transfer)

With psi_c(y) = e_p(Tr(c y)) at q = p^k, Theorems 1-3 hold
verbatim: the quantization proof needs only Tr(0) = 0 and
vanishing power sums. (Verified at F_49 in the script; also at
F_25, F_81 in the fork.)

## Theorem 5 (L-function diagonalization of the shift field)

For G <= (Z/q)^x of even order f and index m, the deviation field
T(t) = sum_{g in G} log|1 + zeta_q^{tg}| satisfies, pointwise,
  T(t) = (f q/(q-1)) sum_{chi != 1, chi trivial on G}
         (1 - chi(2)) (L(1, chi)/tau(chi)) chi(t),
with tau the Gauss sum. COROLLARIES: (a) sum_t T(t)^2 =
(f^2 q/(q-1)) sum_chi |1-chi(2)|^2 |L(1,chi)|^2 — the field's
energy is a mean square of Dirichlet L-values over the quotient
characters; (b) DOUBLING LAW: 2 in G implies T == 0 identically
(2G = G). PROOF: multiplicative Fourier + 1+x = (1-x^2)/(1-x) +
the classical even-character evaluation sum_a conj(chi)(a)
log|1 - zeta^a| = -q L(1,chi)/tau(chi). QED.
CONTEXT: this independently reconstructs and extends the
L(1,chi)-over-subgroups bridge of Borda-Munsch-Shparlinski
(Res. Number Theory, 2024), who bound SIZES of subgroup Dedekind
sums; the diagonalization gives the exact pointwise law.

## Why this frame matters for the finite prize

In these coordinates the finite census problem's remaining content
is exactly the cancellation of the parity field eps against the
Gaussian weight e^S — with the variance side an exact integer
(Theorem 3) and the whole frame valid at extension fields
(Theorem 4). The fork's measured record: the alignment matches the
per-orbit random-sign model with constant ~1 across six decades of
population, every axis tested.
