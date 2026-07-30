p = 2130706433;

(* H8: the surviving localized equation forces d=-c and then w=c. *)
wNum = -7 c^2 d + 3 c d^2 + 2 c^2 + 10 c d - 2 d^2 - 2 c - 2 d;
wDen = 2 c^2 d + 2 c d^2 + 2 c^2 - 10 c d - 2 d^2 - 3 c + 7 d;
h8First =
  36 c^6 d^6 + 72 c^5 d^7 + 36 c^4 d^8 - 1080 c^6 d^5 -
  1032 c^5 d^6 - 424 c^4 d^7 - 72 c^3 d^8 + 1737 c^6 d^4 +
  9282 c^5 d^5 + 4029 c^4 d^6 + 520 c^3 d^7 + 36 c^2 d^8 -
  756 c^6 d^3 - 14130 c^5 d^4 - 28092 c^4 d^5 -
  4818 c^3 d^6 - 100 c^2 d^7 + 36 c^6 d^2 + 6078 c^5 d^3 +
  44701 c^4 d^4 + 36600 c^3 d^5 + 1869 c^2 d^6 - 72 c d^7 -
  96 c^5 d^2 - 22044 c^4 d^3 - 64696 c^3 d^4 -
  22044 c^2 d^5 - 96 c d^6 - 72 c^5 d + 1869 c^4 d^2 +
  36600 c^3 d^3 + 44701 c^2 d^4 + 6078 c d^5 + 36 d^6 -
  100 c^4 d - 4818 c^3 d^2 - 28092 c^2 d^3 - 14130 c d^4 -
  756 d^5 + 36 c^4 + 520 c^3 d + 4029 c^2 d^2 + 9282 c d^3 +
  1737 d^4 - 72 c^3 - 424 c^2 d - 1032 c d^2 - 1080 d^3 +
  36 c^2 + 72 c d + 36 d^2;

h8 = {
  Factor[wNum /. d -> -c] === 10 c^2 (c - 1),
  Factor[wDen /. d -> -c] === 10 c (c - 1),
  Expand[(wNum - c wDen) /. d -> -c] === 0,
  Factor[h8First /. d -> -c] ===
    400 c^3 (c - 1)^2 (c + 1)^2 (c^2 - 5 c + 1)^2
};

(* H9: exact deployed-field terminal and full-quotient witnesses. *)
h = 100 c^4 - 504 c^3 + 817 c^2 - 504 c + 100;
mJ = 1153095255 c^3 + 44715398 c^2 + 2079603121 c + 1265012543;
uJ = 481856514 c^2 + 161871344 c + 1378984398;
vJ = 2108730127 c^3 + 1092963338 c^2 + 577218842 c + 1355798505;
mI = 1777964224 c^3 + 1373289511 c^2 + 1474392606 c + 1474202438;
uI = 134274715 c^2 + 1582407299 c + 450536384;
vI = 1452206296 c^3 + 1366419164 c^2 + 264697898 c + 1149576513;

bezoutJ = PolynomialMod[Expand[uJ h + vJ mJ], p] === 1;
bezoutI = PolynomialMod[Expand[uI h + vI mI], p] === 1;
hFactor = Factor[h, Modulus -> p];
expectedFactor =
  PolynomialMod[
    100 (c^2 + 272520209 c + 1210481498)
        (c^2 + 1602501447 c + 1516822740),
    p
  ];

q2Collision =
  PolynomialRemainder[c (14 - c) - 1, c^2 - 14 c + 1, c] === 0;

e0 =
  4 c^2 d^4 - 120 c^2 d^3 + 8 c d^4 + 193 c^2 d^2 +
  120 c d^3 + 4 d^4 - 84 c^2 d - 262 c d^2 - 84 d^3 +
  4 c^2 + 120 c d + 193 d^2 + 8 c - 120 d + 4;
e1 =
  4 c^4 d^2 + 8 c^4 d - 120 c^3 d^2 + 4 c^4 + 120 c^3 d +
  193 c^2 d^2 - 84 c^3 - 262 c^2 d - 84 c d^2 + 193 c^2 +
  120 c d + 4 d^2 - 120 c + 8 d + 4;
q6 = 4 c^6 - 112 c^5 + 317 c^4 - 430 c^3 + 317 c^2 - 112 c + 4;
gb = GroebnerBasis[
  {e0, e1}, {d, c},
  MonomialOrder -> Lexicographic, Modulus -> p
];
pureC = Select[gb, Exponent[#, d] == 0 &];
expectedEliminant =
  (2 c - 1)^3 * (c - 2)^3 * (c^2 - 14 c + 1) *
  (4 c^6 - 112 c^5 + 317 c^4 - 430 c^3 + 317 c^2 - 112 c + 4) *
  h;
gbComplete =
  Length[gb] == 3 && Length[pureC] == 1 &&
  PolynomialMod[
    Coefficient[expectedEliminant, c, 18] First[pureC] -
      expectedEliminant,
    p
  ] === 0;
q6Basis = GroebnerBasis[{e0, e1, q6}, {d, c},
  MonomialOrder -> Lexicographic, Modulus -> p];
hBasis = GroebnerBasis[{e0, e1, h}, {d, c},
  MonomialOrder -> Lexicographic, Modulus -> p];
q6Collision =
  PolynomialReduce[d - c, q6Basis, {d, c}, Modulus -> p][[2]] === 0;
hRelation =
  PolynomialReduce[
    375 d - 1600 c^3 + 6664 c^2 - 7241 c + 1400,
    hBasis, {d, c}, Modulus -> p
  ][[2]] === 0;

result = <|
  "schema" -> "kb_mca_v4_m2_diagonal_112_fixed_positive_crossed_wolfram_v1",
  "prime" -> PrimeQ[p],
  "H8" -> h8,
  "H9GroebnerCompleteness" -> gbComplete,
  "H9QuarticFactor" -> (PolynomialMod[hFactor - expectedFactor, p] === 0),
  "H9JBezout" -> bezoutJ,
  "H9IBezout" -> bezoutI,
  "H9Q2Collision" -> q2Collision,
  "H9Q6Collision" -> q6Collision,
  "H9HRelation" -> hRelation
|>;

Print[result];
If[!And @@ Flatten[Values[result][[3 ;;]]], Exit[1]];
Print["PASS"];
