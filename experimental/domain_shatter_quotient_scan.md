# Domain-Shattering Quotient-Core Residual Scan

**Status:** EXPERIMENTAL / AUDIT, with a proved finite lower-bound predicate.

This note accompanies `experimental/domain_shatter_quotient_scan.py`.  It
targets the X3 direction in `agents.md`: treat the quotient profile as a
degeneracy measure and test whether small changes to a smooth domain destroy
the quotient-core obstruction while preserving much of the domain.

Represent the original smooth cyclic domain by exponents `Z/nZ`.  For a dyadic
quotient scale `M`, the order-`M` subgroup cosets are the residue classes
modulo `N=n/M`:

```text
C_r = {r + tN : 0 <= t < M}.
```

After puncturing the domain, the quotient-core construction still survives at
scale `M` if:

```text
sigma < M,
M divides k,
some anchor M-coset contains at least sigma retained points,
and at least k/M intact M-cosets remain outside that anchor.
```

If these conditions hold, the same polynomial construction as the quotient-core
lower bound gives at least

```text
binom(full_cosets - indicator(anchor is full), k/M)
```

nearby codewords at agreement `k+sigma`, maximized over possible anchor cosets.
The script reports the logarithm of this residual lower bound at every surviving
scale.

Proof sketch: choose a retained `sigma`-subset `T` of the anchor coset and let
`L_T` be its locator.  For every choice `A` of `k/M` intact `M`-cosets outside
the anchor, the union locator has the quotient form

```text
L_A(X) = X^k + c_1 X^{k-M} + c_2 X^{k-2M} + ...
```

so `P_A=L_T(X)(X^k-L_A(X))` has degree `< k` when `sigma<M`.  The received word
`Y=X^k L_T(X)` agrees with `P_A` on `T` and on every retained point of the
intact cosets in `A`, giving agreement `k+sigma`.  Distinct choices of `A` give
distinct quotient locators and hence distinct codewords.

The default comparison includes:

```text
none
hit-cosets:8
hit-cosets:16
hit-cosets:32
```

Here `hit-cosets:M` deletes one representative from every order-`M` coset.  This
is a small deterministic hitting set for that quotient scale: it removes
`n/M` points and destroys every intact `M`-coset, while leaving other quotient
scales to be checked rather than assumed safe.

Example commands:

```bash
python3 experimental/domain_shatter_quotient_scan.py --m-min 8 --m-max 10
python3 experimental/domain_shatter_quotient_scan.py --pattern none --pattern hit-cosets:16
python3 experimental/domain_shatter_quotient_scan.py --dimension-source retained --format json
```

This is not a positive theorem for punctured domains.  It is an obstruction
audit: passing the scan only means that the explicit quotient-core lower bound
represented by these intact-coset conditions is absent or reduced for the
specified puncturing pattern.
