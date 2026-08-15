(* Exact Wolfram replay of the support-wise affine-span counterexample. *)

ClearAll[falling, rising, repairedCap];
falling[x_, j_] := Product[x - i, {i, 0, j - 1}];
rising[x_, j_] := Product[x + i, {i, 0, j - 1}];
repairedCap[n_, k_, m_, s_, theta_: 1] := Floor[Max[
  falling[n, s + 1]/(m theta rising[m - k + 1, s - 1]),
  falling[n - k + s, s + 1]/(theta rising[m - k + 1, s])
]];

p = 257; n = 256; k = 1; m = 86; w = 85;
points = Join[Table[{gamma, 0}, {gamma, 0, m - 1}], {{m, 1}}];
common = Table[{0, 0, "common"}, {w}];
connectors = Table[
  b = PowerMod[m - gamma, -1, p];
  {Mod[-gamma b, p], b, "connector"},
  {gamma, 0, m - 1}
];
connectorB = connectors[[All, 2]];
availableB = Select[Range[p - 1], ! MemberQ[connectorB, #] &];
unused = Table[
  b = availableB[[index]];
  forbidden = DeleteDuplicates[Mod[#[[2]] - #[[1]] b, p] & /@ points];
  a = First[Select[Range[0, p - 1], ! MemberQ[forbidden, #] &]];
  {a, b, "unused"},
  {index, w}
];
hyperplanes = Join[common, connectors, unused];
r0 = hyperplanes[[All, 1]];
r1 = hyperplanes[[All, 2]];
supports = Table[
  With[{gamma = point[[1]], lambda = point[[2]]},
    Flatten@Position[
      Mod[r0 + gamma r1 - lambda, p],
      0
    ]
  ],
  {point, points}
];
normalRanks = (MatrixRank[Mod[({r1[[#]], -1} & /@ #), p],
    Modulus -> p] &) /@ supports;
directionMax = Max[Values[Counts[r1]]];
nearDistances = Table[
  With[{gamma = point[[1]]},
    word = Mod[r0 + gamma r1, p];
    n - Max[Values[Counts[word]]]
  ],
  {point, points}
];
oldCap = Max[
  Floor[falling[n, 2]/(m w)],
  Floor[falling[n, 2]/(w (w + 1))]
];
fixedCap = repairedCap[n, k, m, 1];

kbN = 2097152; kbK = 1048576; kbM = 1116048;
kbW = kbM - kbK; budget = 274980728111395087;
kbCaps = Table[repairedCap[kbN, kbK, kbM, s], {s, 1, 9}];
thresholdCaps = Map[
  repairedCap[kbN, kbK, kbM, #[[1]], #[[2]]] &,
  {{9, 13}, {10, 388}, {11, 12050}}
];
previousTotals = Map[
  repairedCap[kbN, kbK, kbM, #[[1]], #[[2]] - 1] + 2 kbW &,
  {{9, 13}, {10, 388}, {11, 12050}}
];

checks = {
  Length[hyperplanes] == 256,
  Length[points] == 87,
  DeleteDuplicates[Length /@ supports] == {86},
  DeleteDuplicates[normalRanks] == {2},
  Intersection @@ supports == {},
  directionMax == 85,
  Min[nearDistances] == 170,
  oldCap == 8,
  fixedCap == 759,
  kbCaps[[8]] == 110390969172173096,
  kbCaps[[9]] == 3430729820133944932,
  kbCaps[[8]] + 2 kbW == 110390969172308040,
  budget - kbCaps[[8]] - 2 kbW == 164589758939087047,
  thresholdCaps == {263902293856457302, 274790124064526354,
    274970108028773601},
  previousTotals == {285894151677963688, 275500176064828033,
    274992929018868606}
};

If[! And @@ checks,
  Print["KB_MCA_SUPPORT_LOCAL_THETA_WOLFRAM_FAIL"];
  Exit[1]
];

Print["KB_MCA_SUPPORT_LOCAL_THETA_WOLFRAM_PASS ",
  <|"slopes" -> Length[points], "oldCap" -> oldCap,
    "repairedCap" -> fixedCap, "directionMax" -> directionMax,
    "minNearDistance" -> Min[nearDistances],
    "kbPaidTotal" -> kbCaps[[8]] + 2 kbW,
    "kbSlack" -> budget - kbCaps[[8]] - 2 kbW|>
];
