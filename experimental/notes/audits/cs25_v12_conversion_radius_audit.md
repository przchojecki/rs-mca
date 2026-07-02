# Paper D v12 Deep-Point Conversion Radius Audit

- **Status:** AUDIT / proof-logic and integer-radius check.
- **Source:** `tex/cs25_cap_v12.tex`, Theorem A
  `deep-point list-to-CA conversion`, `rem:import`, and the adjacent
  quantitative floor propositions.
- **Verifier:** `experimental/scripts/verify_cs25_v12_conversion_radius.py`.

This audit checks the first item in the current `agents.md` Paper D v12 audit
priority: the direct deep-point conversion and its integer-radius condition.
The main Paper D cap no longer imports the Crites--Stewart conversion as a
black box; Theorem A gives the simple-pole proof directly and isolates the
condition

```text
floor(delta*n) <= n-k-1.
```

The official ePrint metadata pages for ABF 2026/680 and Crites--Stewart
2025/2046 are reachable from this environment, but their PDF endpoints returned
HTTP 403/Cloudflare during this audit.  Consequently, this note is a local audit
of the v12 formulation and its stated ABF/CS conventions, not a full external
line-by-line comparison with those PDFs.

## Integer-Radius Gate

Let `f=floor(delta*n)`.  A closed Hamming ball of relative radius `delta`
allows at most `f` errors, hence gives agreement at least `n-f`.

Theorem A needs every listed `C^+=RS[F,D,k+1]` codeword to agree with the
received word on more than `k` points, so that the simple-pole far-condition
argument for `g_alpha=-1/(X-alpha)` applies.  This is exactly

```text
n-f >= k+1    <=>    f <= n-k-1.
```

Equivalently, a radius with `floor(delta*n)=f` can occur below the sub-capacity
threshold `delta < 1-k/n` exactly when `f < n-k`, i.e. again
`f <= n-k-1`.

The verifier exhausts all triples `(n,k,f)` with `n<=80` and confirms both
equivalences.

## Simple-Pole Far Condition

For `alpha in F\\D`, define

```text
f_alpha(x)=U(x)/(x-alpha),   g_alpha(x)=-1/(x-alpha).
```

If some `G in F[X]_<k` agreed with `g_alpha` on more than `k` domain points,
then `(X-alpha)G(X)+1` would have degree at most `k`, more than `k` roots, and
value `1` at `alpha`, a contradiction.  Thus any common pair explanation on
`>=k+1` points is impossible.  This is precisely where the integer-radius gate
is used.

No off-by-one issue was found: at the endpoint
`delta=1-rho-1/n`, one has `floor(delta*n)=n-k-1`, so the CA conversion still
applies.  At `delta>=1-rho`, the condition fails, and Paper D correctly uses
MCA monotonicity from an admissible endpoint rather than claiming CA conversion
past capacity.

## Conversion Algebra

The proof obtains, for some pole `alpha`,

```text
epsilon >= L(q-n)/(q(q-n+kL)).
```

The denominator condition is safe because the hypothesis

```text
epsilon <= eta*(q-n)/(kq),   eta<1
```

implies `q-n-k*epsilon*q >= (1-eta)(q-n)>0`.  Solving gives

```text
L <= q*epsilon/(1-eta).
```

The verifier checks this implication with exact rational arithmetic on a finite
grid of small parameters and several `eta` values.  It also checks the
quantitative trigger from the adjacent deep-list floor:

```text
L(q-n)/(q(q-n+kL)) > (1/(2k))(1-n/q)
    <=> kL > q-n.
```

## Result

The current verifier reports:

```text
implemented PASS: 3   FAIL: 0
```

No radius-convention or algebra discrepancy was found.  The remaining external
source task is to repeat the comparison against the ABF and Crites--Stewart PDFs
in an environment where those PDF endpoints are accessible.
