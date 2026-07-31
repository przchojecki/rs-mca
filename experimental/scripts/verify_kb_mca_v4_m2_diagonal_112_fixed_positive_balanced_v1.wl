(* Independent Wolfram replay for the balanced fixed-positive packet.

   The exact integer polynomials are parsed from the checked-in Singular
   replay so that the two engines consume byte-identical inputs.  Wolfram
   independently recomputes both Groebner certificates modulo the deployed
   prime.  No Sage output is imported.
*)

p0 = 2130706433;
here = DirectoryName[$InputFileName];
singularPath = FileNameJoin[{
  here,
  "verify_kb_mca_v4_m2_diagonal_112_fixed_positive_balanced_v1.sing"
}];
source = Import[singularPath, "Text"];

ClearAll[extractPolynomial];
extractPolynomial[name_String] := Module[{matches},
  matches = StringCases[
    source,
    RegularExpression[
      "poly[[:space:]]+" <> name <>
      "[[:space:]]*=[[:space:]]*([\\s\\S]*?);"
    ] :> "$1"
  ];
  If[Length[matches] =!= 1,
    Print["POLYNOMIAL_PARSE_FAIL:" <> name];
    Exit[1]
  ];
  ToExpression[
    StringReplace[First[matches], WhitespaceCharacter -> ""],
    InputForm
  ]
];

(* Abbreviations used only to keep the explicit Singular source compact. *)
c2 = c^2; c3 = c^3; c4 = c^4;
w2 = w^2; w3 = w^3; w4 = w^4; w5 = w^5;
qc = extractPolynomial["qc"];
qd = extractPolynomial["qd"];
ell = extractPolynomial["ell"];
e1 = extractPolynomial["e1"];
e2 = extractPolynomial["e2"];
arec = extractPolynomial["arec"];
hmiss = extractPolynomial["hmiss"];

gbMissing = GroebnerBasis[
  {qc, qd, t*hmiss - 1},
  {t, b, c, w},
  Modulus -> p0,
  MonomialOrder -> DegreeReverseLexicographic
];
If[gbMissing =!= {1},
  Print["INCIDENCE_CD_EQ_W2_WOLFRAM_FAIL"];
  Exit[1]
];
Print["INCIDENCE_CD_EQ_W2_WOLFRAM_PASS"];

Clear[c2, c3, c4, w2, w3, w4, w5];
s2 = s^2; s3 = s^3; s4 = s^4; s5 = s^5;
p2 = p^2; p3 = p^3; p4 = p^4; p5 = p^5; p6 = p^6;
w2 = w^2; w3 = w^3; w4 = w^4;
qSym = extractPolynomial["Q"];
aSym = extractPolynomial["A"];
bSym = extractPolynomial["B"];
hSym = extractPolynomial["H"];

gbSupport = GroebnerBasis[
  {qSym, aSym, bSym, t*hSym - 1},
  {t, s, p, w},
  Modulus -> p0,
  MonomialOrder -> DegreeReverseLexicographic
];
remainderP = Last@PolynomialReduce[
  (p + w)^2, gbSupport, {t, s, p, w}, Modulus -> p0
];
remainderS = Last@PolynomialReduce[
  (5*s + 4*w - 4)^2,
  gbSupport, {t, s, p, w}, Modulus -> p0
];
If[remainderP =!= 0 || remainderS =!= 0,
  Print["SYMMETRIC_SUPPORT_WOLFRAM_FAIL"];
  Exit[1]
];
Print["SYMMETRIC_SUPPORT_WOLFRAM_PASS"];
Print["BALANCED_WOLFRAM_PASS"];
