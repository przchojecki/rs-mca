#!/usr/bin/env python3
"""Independent python-flint replay of exact integers and root bounds."""

from flint import fmpz, fmpz_poly


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


n = fmpz(2) ** 21
K = fmpz(2) ** 20
m = fmpz(1116048)
w = m - K
dmin = n - K + 1
B = fmpz(274980728111395087)

require(w == 67472, "w")
require(2*w == 134944, "two-anchor charge")
require(3*w == 202416 and 3*w < dmin, "minimum-distance guard")
require(dmin - 3*w == 846161, "minimum-distance margin")
require(B - 2*w == 274980728111260143, "budget remainder")
require(n-w == 2029680 and n-w >= m, "common support size")

# Root-count controls used twice in the proof.  A nonzero degree <K
# polynomial cannot vanish at K distinct formal integer points.
x = fmpz_poly([0, 1])
root_poly = fmpz_poly([1])
for a in range(8):
    root_poly *= x - a
require(root_poly.degree() == 8, "root polynomial degree")
require(all(root_poly(a) == 0 for a in range(8)), "root polynomial roots")

# A codeword supported on at most 3w coordinates is below RS minimum distance.
require(3*w <= n-K, "integer minimum-distance form")

# Mersenne-31 control.
m31 = fmpz(1116024)
w31 = m31-K
B31 = fmpz(16777215)
require(w31 == 67448 and 2*w31 == 134896, "M31 charge")
require(B31-2*w31 == 16642319, "M31 remainder")

print("FLINT support-wise two-anchor replay")
print("  KoalaBear charge:", 2*w)
print("  M31 charge:", 2*w31)
print("  root-count and distance guards: exact")
print("RESULT: PASS")
