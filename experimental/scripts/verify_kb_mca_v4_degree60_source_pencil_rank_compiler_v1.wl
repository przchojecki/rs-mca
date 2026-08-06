(* Exact Wolfram Language arithmetic replay for the degree-60
   source-pencil rank controls.

   This independently checks the source-partition totals, deterministic
   matrix dimensions, the explicit degree-ten F_p root/fibre data, its
   finite-coordinate conjugation, and the degree-ten modular rank tests.
   It is a computation-only control: it does not assert exhaustion,
   same-record transport, an owner, a payment, or row closure.
*)

ClearAll["Global`*"];

fail[message_] := (
  Print["status=FAIL"];
  Print["failure=", message];
  Exit[1]
);
require[condition_, message_] := If[!TrueQ[condition], fail[message]];

p = 2130706433;
endpointDegree = 60;

profiles = {
  <|"m" -> 2, "n" -> 30, "a" -> 6, "b" -> 0,
    "partitions" -> 10395|>,
  <|"m" -> 3, "n" -> 20, "a" -> 4, "b" -> 0,
    "partitions" -> 15400|>,
  <|"m" -> 4, "n" -> 15, "a" -> 3, "b" -> 0,
    "partitions" -> 5775|>,
  <|"m" -> 6, "n" -> 10, "a" -> 2, "b" -> 0,
    "partitions" -> 462|>,
  <|"m" -> 10, "n" -> 6, "a" -> 1, "b" -> 1,
    "partitions" -> 66|>,
  <|"m" -> 12, "n" -> 5, "a" -> 1, "b" -> 0,
    "partitions" -> 1|>
};

partitionFormula[row_] :=
  12!/
    ((Lookup[row, "m"]!)^Lookup[row, "a"] Lookup[row, "a"]!
      If[
        Lookup[row, "b"] == 0,
        1,
        ((Lookup[row, "m"]/5)!)^Lookup[row, "b"]
          Lookup[row, "b"]!
      ]);

require[
  And @@ (
    partitionFormula[#] == Lookup[#, "partitions"] & /@ profiles
  ),
  "source partition formulas"
];
partitionTotal = Total[Lookup[profiles, "partitions"]];
require[partitionTotal == 32099, "source partition total"];

dimensionTable = <|
  2 -> <|"Source" -> {{3, 6}, 2},
    "Symmetric" -> {{61, 31}, 31},
    "Augmented" -> {{61, 32}, 31}|>,
  3 -> <|"Source" -> {{4, 4}, 2},
    "Symmetric" -> {{61, 21}, 21},
    "Augmented" -> {{61, 22}, 21}|>,
  4 -> <|"Source" -> {{5, 3}, 2},
    "Symmetric" -> {{61, 16}, 16},
    "Augmented" -> {{61, 17}, 16}|>,
  6 -> <|"Source" -> {{7, 2}, 2},
    "Symmetric" -> {{61, 11}, 11},
    "Augmented" -> {{61, 12}, 11}|>,
  10 -> <|"Source" -> {{11, 2}, 2},
    "Symmetric" -> {{61, 7}, 7},
    "Augmented" -> {{61, 8}, 7}|>,
  12 -> <|"Source" -> {{13, 2}, 2},
    "RawSource" -> {{13, 1}, 1},
    "Symmetric" -> {{61, 6}, 6},
    "Augmented" -> {{61, 7}, 6}|>
|>;

Do[
  m = Lookup[row, "m"];
  n = Lookup[row, "n"];
  forcedColumns = Lookup[row, "a"] + Lookup[row, "b"];
  If[m == 12,
    require[
      Lookup[dimensionTable[m], "RawSource"] ==
        {{m + 1, forcedColumns}, 1},
      "m12 raw-source dimensions"
    ];
    require[
      Lookup[dimensionTable[m], "Source"] == {{m + 1, 2}, 2},
      "m12 canonical-source dimensions"
    ],
    require[
      Lookup[dimensionTable[m], "Source"] ==
        {{m + 1, forcedColumns}, 2},
      "source dimensions"
    ]
  ];
  require[
    Lookup[dimensionTable[m], "Symmetric"] ==
      {{endpointDegree + 1, n + 1}, n + 1},
    "symmetric-power dimensions"
  ];
  require[
    Lookup[dimensionTable[m], "Augmented"] ==
      {{endpointDegree + 1, n + 2}, n + 1},
    "augmented dimensions"
  ],
  {row, profiles}
];

recursiveRoutes = <|
  2 -> {}, 3 -> {}, 4 -> {2}, 6 -> {2, 3},
  10 -> {2}, 12 -> {2, 3, 4, 6}
|>;
primeDegreeSurvivors = Select[
  {2, 3},
  PrimeQ[#] && Lookup[recursiveRoutes, #] == {} &
];
require[primeDegreeSurvivors == {2, 3},
  "prime-degree survivor controls"];

m10Data = <|
  243 -> <|
    "x" -> {
      441863510, 709682263, 710497174, 796172940, 1603196979
    },
    "z" -> {
      74267057, 635415206, 824563947, 1188339233, 1311122138,
      1530081469, 1604873909, 1738540140, 1748005996, 2129029503
    }
  |>,
  3459 -> <|
    "x" -> {
      85973857, 872107610, 1750292172, 1822723048, 1861022612
    },
    "z" -> {
      524247488, 669066773, 704716532, 738015176, 962409336,
      1012276996, 1153656275, 1336775124, 1511963758, 2040404707
    }
  |>,
  3574 -> <|
    "x" -> {
      292496322, 598963494, 682863060, 937365616, 1749724374
    },
    "z" -> {
      714150458, 1005685328, 1258341041, 1471328886, 1514082436,
      1553989613, 1709052297, 1807884165, 1825444399, 2054986408
    }
  |>,
  8607 -> <|
    "x" -> {
      301169065, 393923145, 587925168, 1160295361, 1818100127
    },
    "z" -> {
      168034917, 419890251, 448555045, 534454304, 711740316,
      1066041149, 1202773742, 1229101756, 1283645823, 1458588429
    }
  |>,
  19677 -> <|
    "x" -> {
      133423276, 197786794, 426255696, 1635032333, 1868914767
    },
    "z" -> {
      10557685, 122865591, 223329671, 358247568, 574517956,
      1192307416, 1364654713, 1411702662, 1510667199, 1753975271
    }
  |>,
  30437 -> <|
    "x" -> {
      114235151, 491570846, 570012245, 1308462057, 1777132567
    },
    "z" -> {
      215919938, 315566246, 407523600, 583041545, 725871186,
      992895811, 1561212629, 1837417984, 1974847492, 2039235734
    }
  |>,
  43384 -> <|
    "x" -> {
      1052806569, 1180717393, 1312828491, 1366977764, 1478789082
    },
    "z" -> {
      133148234, 280420086, 668377073, 772386483, 810412009,
      1047569159, 1324342231, 1567326038, 1930358159, 2119192693
    }
  |>
|>;

s5[x_] := Mod[x^5 + x^2 + x, p];
rFromZ[z_] := Mod[z + 2 PowerMod[z, -1, p], p];
tFromZ[z_] := PowerMod[Mod[z - 1, p], -1, p];
zFromT[t_] := Mod[(t + 1) PowerMod[t, -1, p], p];

zz = Unique["z"];
ww = Unique["w"];
tt = Unique["t"];
ss = Unique["s"];

oldNumerator =
  (zz^2 + 2 ww^2)^5
  + (zz^2 + 2 ww^2)^2 (zz ww)^3
  + (zz^2 + 2 ww^2) (zz ww)^4;
oldDenominator = (zz ww)^5;
newNumerator = Expand[
  oldNumerator /. {zz -> tt + ss, ww -> tt}
];
newDenominator = Expand[
  oldDenominator /. {zz -> tt + ss, ww -> tt}
];
rightNumerator = (tt + ss)^2 + 2 tt^2;
rightDenominator = tt (tt + ss);

require[
  Expand[
    newNumerator -
      (
        rightNumerator^5
        + rightNumerator^2 rightDenominator^3
        + rightNumerator rightDenominator^4
      )
  ] === 0,
  "degree-ten conjugated composition numerator"
];
require[
  Expand[newDenominator - rightDenominator^5] === 0,
  "degree-ten conjugated composition denominator"
];
require[
  Coefficient[newNumerator, tt, 10] ==
    255 Coefficient[newDenominator, tt, 10],
  "conjugated infinity value"
];
require[!KeyExistsQ[m10Data, 255], "selected y=255"];

newNumeratorAffine = Expand[newNumerator /. ss -> 1];
newDenominatorAffine = Expand[newDenominator /. ss -> 1];
modCoefficientList[polynomial_, degree_] := PadRight[
  Mod[CoefficientList[Expand[polynomial], tt], p],
  degree + 1
];
normalizedCoefficientList[polynomial_, degree_] := Module[
  {coefficients, leading},
  coefficients = modCoefficientList[polynomial, degree];
  leading = Last[coefficients];
  require[leading != 0, "polynomial leading coefficient"];
  Mod[PowerMod[leading, -1, p] coefficients, p]
];

transformedByY = Association[];
fibreChecks = KeyValueMap[
  Function[{y, data},
    Module[
      {xs, zs, recoveredXs, transformed, fibrePolynomial, rootPolynomial},
      xs = Lookup[data, "x"];
      zs = Lookup[data, "z"];
      require[Length[xs] == 5 && DuplicateFreeQ[xs],
        "degree-ten x-root count"];
      require[Length[zs] == 10 && DuplicateFreeQ[zs],
        "degree-ten z-root count"];
      require[And @@ (s5[#] == y & /@ xs),
        "outer quintic fibre"];
      require[And @@ (# != 0 && # != 1 & /@ zs),
        "conjugation pole in selected fibre"];
      recoveredXs = rFromZ /@ zs;
      require[
        Sort[recoveredXs] ==
          Sort[Flatten[(ConstantArray[#, 2] &) /@ xs]],
        "quadratic fibre identities"
      ];
      transformed = tFromZ /@ zs;
      require[DuplicateFreeQ[transformed],
        "transformed fibre repeats"];
      require[And @@ MapThread[
        zFromT[#1] == #2 &,
        {transformed, zs}
      ], "inverse conjugation"];
      require[
        And @@ (
          Mod[
            (newNumeratorAffine /. tt -> #)
            - y (newDenominatorAffine /. tt -> #),
            p
          ] == 0 & /@ transformed
        ),
        "transformed fibre evaluation"
      ];
      fibrePolynomial =
        newNumeratorAffine - y newDenominatorAffine;
      rootPolynomial = Expand[Times @@ (tt - # & /@ transformed)];
      require[
        normalizedCoefficientList[fibrePolynomial, 10] ==
          normalizedCoefficientList[rootPolynomial, 10],
        "transformed split fibre polynomial"
      ];
      AssociateTo[transformedByY, y -> transformed];
      True
    ]
  ],
  m10Data
];
require[And @@ fibreChecks, "degree-ten fibre checks"];

allOldRoots = Flatten[Lookup[Values[m10Data], "z"]];
allTransformedRoots = Flatten[Values[transformedByY]];
require[Length[DeleteDuplicates[allOldRoots]] == 70,
  "old fibre collision"];
require[Length[DeleteDuplicates[allTransformedRoots]] == 70,
  "transformed fibre collision"];

sourceY = 243;
activeYs = {3459, 3574, 8607, 19677, 30437, 43384};
exceptionalFinitePoints = {0, p - 1};
sourcePoints = Join[
  Lookup[transformedByY, sourceY],
  exceptionalFinitePoints
];
activePoints = Flatten[Lookup[transformedByY, activeYs]];
require[Length[sourcePoints] == 12 && DuplicateFreeQ[sourcePoints],
  "finite source split"];
require[Length[activePoints] == 60 && DuplicateFreeQ[activePoints],
  "active split"];
require[Intersection[sourcePoints, activePoints] == {},
  "source/active overlap"];
require[
  Mod[newDenominatorAffine /. tt -> 0, p] == 0
    && Mod[newDenominatorAffine /. tt -> (p - 1), p] == 0,
  "exceptional finite denominator points"
];

(* Independent modular rank replay for the degree-ten control. *)
sourceForms = {
  newNumeratorAffine - sourceY newDenominatorAffine,
  newDenominatorAffine
};
sourceMatrix = Transpose[
  modCoefficientList[#, 10] & /@ sourceForms
];
require[Dimensions[sourceMatrix] == {11, 2},
  "degree-ten source matrix dimensions"];
require[MatrixRank[sourceMatrix, Modulus -> p] == 2,
  "degree-ten source matrix rank"];

symmetricForms = Table[
  PolynomialMod[
    newNumeratorAffine^(6 - j) newDenominatorAffine^j,
    p
  ],
  {j, 0, 6}
];
symmetricMatrix = Transpose[
  modCoefficientList[#, 60] & /@ symmetricForms
];
activeForm = PolynomialMod[
  Times @@ (
    newNumeratorAffine - # newDenominatorAffine & /@ activeYs
  ),
  p
];
augmentedMatrix = Transpose[
  Join[
    modCoefficientList[#, 60] & /@ symmetricForms,
    {modCoefficientList[activeForm, 60]}
  ]
];
require[Dimensions[symmetricMatrix] == {61, 7},
  "degree-ten symmetric matrix dimensions"];
require[Dimensions[augmentedMatrix] == {61, 8},
  "degree-ten augmented matrix dimensions"];
require[MatrixRank[symmetricMatrix, Modulus -> p] == 7,
  "degree-ten symmetric matrix rank"];
require[MatrixRank[augmentedMatrix, Modulus -> p] == 7,
  "degree-ten active membership rank"];

Print["status=PASS_EXACT_WOLFRAM_SOURCE_PENCIL_CONTROLS"];
Print["partition_total=", partitionTotal];
Print["rows=", Lookup[profiles, "m"]];
Print["dimension_table=", dimensionTable];
Print["recursive_right_degrees=", recursiveRoutes];
Print["prime_degree_survivors=", primeDegreeSurvivors];
Print["m10_source_y=", sourceY];
Print["m10_active_ys=", activeYs];
Print["m10_exceptional_finite_points={0,-1}"];
Print["m10_all_70_selected_roots_finite_and_distinct=True"];
Print["m10_y255_absent=True"];
Print["scope=EXACT_ARITHMETIC_CONTROL_NOT_EXHAUSTION_OR_PAYMENT"];
