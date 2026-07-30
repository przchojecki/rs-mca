p = 2130706433;

e0 =
  36 c^6 d^4 - 180 c^6 d^3 - 172 c^5 d^4 + 297 c^6 d^2 +
  920 c^5 d^3 + 524 c^4 d^4 - 180 c^6 d - 1698 c^5 d^2 -
  2428 c^4 d^3 - 960 c^3 d^4 + 36 c^6 + 1256 c^5 d +
  4071 c^4 d^2 + 3648 c^3 d^3 + 860 c^2 d^4 - 328 c^5 -
  3052 c^4 d - 5364 c^3 d^2 - 3052 c^2 d^3 - 328 c d^4 +
  860 c^4 + 3648 c^3 d + 4071 c^2 d^2 + 1256 c d^3 + 36 d^4 -
  960 c^3 - 2428 c^2 d - 1698 c d^2 - 180 d^3 + 524 c^2 +
  920 c d + 297 d^2 - 172 c - 180 d + 36;

e1 =
  36 c^4 d^6 - 172 c^4 d^5 - 180 c^3 d^6 + 524 c^4 d^4 +
  920 c^3 d^5 + 297 c^2 d^6 - 960 c^4 d^3 - 2428 c^3 d^4 -
  1698 c^2 d^5 - 180 c d^6 + 860 c^4 d^2 + 3648 c^3 d^3 +
  4071 c^2 d^4 + 1256 c d^5 + 36 d^6 - 328 c^4 d -
  3052 c^3 d^2 - 5364 c^2 d^3 - 3052 c d^4 - 328 d^5 +
  36 c^4 + 1256 c^3 d + 4071 c^2 d^2 + 3648 c d^3 + 860 d^4 -
  180 c^3 - 1698 c^2 d - 2428 c d^2 - 960 d^3 + 297 c^2 +
  920 c d + 524 d^2 - 180 c - 172 d + 36;

f6 =
  9 c^6 - 82 c^5 + 119 c^4 - 156 c^3 + 119 c^2 - 82 c + 9;
f8 =
  324 c^8 - 5328 c^7 + 29617 c^6 - 77552 c^5 + 106134 c^4 -
  77552 c^3 + 29617 c^2 - 5328 c + 324;
f10 =
  36 c^10 - 352 c^9 + 1741 c^8 - 5266 c^7 + 9871 c^6 -
  12124 c^5 + 9871 c^4 - 5266 c^3 + 1741 c^2 - 352 c + 36;

expectedResultant =
  3486784401 (c - 2)^4 (2 c - 1)^4 (c - 1)^10 (c + 1)^10 *
    f6 * f8 * f10;
resultantFactorization =
  Cancel[Resultant[e0, e1, d]/expectedResultant] === 1;

f6Basis = GroebnerBasis[
  {e0, e1, f6}, {d, c},
  MonomialOrder -> Lexicographic,
  Modulus -> p
];
f10Basis = GroebnerBasis[
  {e0, e1, f10}, {d, c},
  MonomialOrder -> Lexicographic,
  Modulus -> p
];
wNum =
  3 c^2 d^2 - 4 c^2 d - 4 c d^2 + 2 c^2 + 9 c d + 2 d^2 -
  5 c - 5 d + 2;
wDen =
  2 c^2 d^2 - 5 c^2 d - 5 c d^2 + 2 c^2 + 9 c d + 2 d^2 -
  4 c - 4 d + 3;
f6Reciprocal =
  PolynomialReduce[c d - 1, f6Basis, {d, c}, Modulus -> p][[2]] === 0;
f6Fixed =
  PolynomialReduce[wNum - wDen, f6Basis, {d, c}, Modulus -> p][[2]] === 0;
f10Equal =
  PolynomialReduce[d - c, f10Basis, {d, c}, Modulus -> p][[2]] === 0;

mJ =
  9883900 c^7 + 763829210 c^6 + 1812515029 c^5 + 915891061 c^4 +
  913730111 c^3 + 47079281 c^2 + 1996723265 c + 482954018;
uJ =
  1606439928 c^6 + 1258221600 c^5 + 1415812154 c^4 +
  1301926167 c^3 + 1055326069 c^2 + 177769301 c + 1050548741;
vJ =
  29628355 c^7 + 885094218 c^6 + 1465118481 c^5 + 901744177 c^4 +
  1916788299 c^3 + 1095838264 c^2 + 343401622 c + 162121279;

mI =
  829611936 c^7 + 1359907050 c^6 + 1507080347 c^5 + 413622875 c^4 +
  795930408 c^3 + 1198218452 c^2 + 1278816008 c + 467867406;
uI =
  1820761540 c^6 + 227124627 c^5 + 986262926 c^4 +
  1339492114 c^3 + 1704323271 c^2 + 1711384843 c + 728891986;
vI =
  880556468 c^7 + 644748967 c^6 + 1809782485 c^5 + 338011691 c^4 +
  1768858959 c^3 + 2109338360 c^2 + 197424372 c + 1963273613;

bezoutJ = PolynomialMod[Expand[uJ f8 + vJ mJ], p] === 1;
bezoutI = PolynomialMod[Expand[uI f8 + vI mI], p] === 1;

result = <|
  "schema" ->
    "kb_mca_v4_m2_diagonal_112_fixed_positive_identity_wolfram_v1",
  "Prime" -> PrimeQ[p],
  "ResultantFactorization" -> resultantFactorization,
  "F6ReciprocalCollision" -> f6Reciprocal,
  "F6FixedCollision" -> f6Fixed,
  "F10EqualLabelCollision" -> f10Equal,
  "F8JBezout" -> bezoutJ,
  "F8IBezout" -> bezoutI
|>;

Print[result];
If[!And @@ Values[result][[2 ;;]], Exit[1]];
Print["PASS"];
