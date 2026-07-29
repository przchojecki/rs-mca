# Rejected base-field reciprocal-\(P_6\) candidate

Status: **REJECTED / PRESERVED FAILED ATTEMPT**

The first elimination pass for the pole-\([6]\), endpoint-\(\{0,2\}\),
reciprocal \(P_6\) chart produced the apparent base-field candidate

```text
alpha =
[711525961, 963394751, 1475394420,
 29417033, 2067032599, 490298432]

factor sequence =
[277779454, 0, 1269030692, 861675741,
 215343436, 1915362997, 1107093278]
```

It is not a solution of the full source equations.  Its six \(S\)-interpolation
residuals vanish, but the three nonanchor \(P\)-interpolation residuals are

```text
[1604374407, 1718964514, 179487170]
```

modulo \(p=2130706433\).

The error was a sign in the projected discovery equation.  For path
\([0,1,3,4,5,2]\) and factor sequence
\([x_0,0,a,-a,-b,b,x_6]\), the \(P\)-values are
\[
 (0,0,bx_6,-a^2,ab,-b^2).
\]
The rejected projection used
\[
 -a^2(t-r)(t-s)+bx_6P_{\rm base}=0
\]
where the full determinant equation requires the opposite sign on the
\(bx_6P_{\rm base}\) term.  Resultant roots were then accepted without a
substitution check against all six original interpolation equations.

The committed local-survivor packet corrects the sign, substitutes every
candidate into the unsimplified equations, and finds a valid solution only
after passing to \(\mathbf F_{p^2}\subset\mathbf F_{p^6}\).  This failed
attempt is retained to prevent the base-field integers or the projected
resultant from being reused as proof evidence.
