(* Independent Wolfram Engine replay of the near-aligned negative q-slice. *)

ClearAll["Global`*"];

edge[left_, right_] := {left right, -(left + right), 1};
evaluation[x_] := {
  {1, x, x^2, 0},
  {0, 0, 0, 1 - x^2},
  {-x^2, -x, -1, 0}
};
zeroQ[value_] := Numerator[Together[value]] === 0;

w = 1/c;
a = 2;
q0 = c d;
q1 = -(c + d);
f = q0 + w;
g = -1 - w q0;
m = q1 (1 + w);
z = Together[-(f + m a - g a^2)/(g - m a - f a^2)];
vAtZ = {f + g z, m (1 - z), -(g + f z)};
linear1 = vAtZ[[3]];
linear0 = vAtZ[[2]] + a vAtZ[[3]];
If[!zeroQ[vAtZ[[1]] + a linear0], Print["FAIL incidence"]; Exit[1]];

reconstruct[template_] := Module[
  {first, second, right, left, target, atW, atZ, matrix, rhs, solution,
   consistency, u, v, residuals, uRoot, vRoot, norm, quotient},
  If[template === "fixed-moving",
    first = edge[a, 1/a]; second = edge[a, b]; right = 1/a; left = b,
    first = edge[a, b]; second = edge[a, 1/b]; right = b; left = 1/b
  ];
  target = Together[
    ((linear0 + left linear1) first + (linear0 + right linear1) second)/
      (left - right)
  ];
  atW = evaluation[w];
  atZ = evaluation[z];
  matrix = Join[
    {atW[[1]] - q0 atW[[3]], atW[[2]] - q1 atW[[3]]},
    atZ
  ];
  rhs = Join[{0, 0}, target];
  solution = Together[LinearSolve[Take[matrix, 4], Take[rhs, 4]]];
  consistency = Together[(matrix.solution - rhs)[[5]]];
  u = {
    solution[[1]] + solution[[2]] W + solution[[3]] W^2,
    solution[[4]] (1 - W^2),
    -solution[[3]] - solution[[2]] W - solution[[1]] W^2
  };
  v = {
    f + g W,
    m (1 - W),
    -(g + f W)
  };
  residuals = Table[
    uRoot = Sum[u[[index]] root^(index - 1), {index, 1, 3}];
    vRoot = Sum[v[[index]] root^(index - 1), {index, 1, 3}];
    norm = Together[uRoot^2 - W vRoot^2];
    quotient = Cancel[norm/(W - w)^2];
    If[!zeroQ[norm - (W - w)^2 quotient],
      Print["FAIL exact division"]; Exit[1]
    ];
    quotient,
    {root, {c, d}}
  ];
  {consistency, Together[Times @@ residuals]}
];

pFactor = c d - 2 c - 2 d + 1;
qFactor = 2 c d - c - d + 2;
loci = {
  {"fixed-moving:B", "fixed-moving", b -> -qFactor/pFactor},
  {"moving-moving:B", "moving-moving", b -> -qFactor/pFactor},
  {"moving-moving:C", "moving-moving", b -> -pFactor/qFactor}
};

rawResiduals = Table[
  reconstructed = reconstruct[locus[[2]]];
  consistency = Together[reconstructed[[1]] /. locus[[3]]];
  If[!zeroQ[consistency], Print["FAIL consistency ", locus[[1]]]; Exit[1]];
  Together[reconstructed[[2]] /. locus[[3]]],
  {locus, loci}
];

lambda =
  4 c^2 d - 2 c^2 - c d - c - 2 d + 4;
aFactor = 5 c d - 4 c - 4 d + 5;
incidenceE =
  c d w + 4 c d - 2 c w - 2 c - 2 d w - 2 d + 4 w + 1;
If[!zeroQ[lambda - c incidenceE],
  Print["FAIL Lambda parent relation"]; Exit[1]
];
expectedLeading =
  (c - 1)^2 (d - 1)^2 (d + 1)^2 (c d - 1)^4 lambda^4/
    ((c + 1)^2 aFactor^4);
If[!And @@ (zeroQ[Coefficient[#, W, 4] - expectedLeading] & /@ rawResiduals),
  Print["FAIL leading coefficient identity"]; Exit[1]
];
residuals = Together[#/Coefficient[#, W, 4]] & /@ rawResiduals;
If[!And @@ (zeroQ[# - First[residuals]] & /@ Rest[residuals]),
  Print["FAIL common residual"]; Exit[1]
];
r = First[residuals];

(* Certify the chosen rows 1,2,3,4: only c+d is not a parent unit. *)
q0Default = c d;
q1Default = -(c + d);
fDefault = q0Default + w;
gDefault = -1 - w q0Default;
mDefault = q1Default (1 + w);
zDefault = Together[
  -(fDefault + mDefault a - gDefault a^2)/
    (gDefault - mDefault a - fDefault a^2)
];
matrixDefault = Join[
  {
    evaluation[w][[1]] - q0Default evaluation[w][[3]],
    evaluation[w][[2]] - q1Default evaluation[w][[3]]
  },
  evaluation[zDefault]
];
defaultMinor = Together[Det[matrixDefault[[{1, 2, 3, 4}]]]];
expectedDefaultMinor = Together[
  3 (d - 2) (2 d - 1) (c - 2) (c + d) (2 c - 1)
    (c - 1)^4 (c + 1)^4 (c d - 1) aFactor/
    (c^4 lambda^4)
];
If[!zeroQ[defaultMinor - expectedDefaultMinor],
  Print["FAIL default minor factorization"]; Exit[1]
];

(* The default solver minor has a removable c+d factor. On d=-c,
   rows 1,2,3,5 in one-based indexing cover the divisor. *)
dAlt = -c;
q0Alt = c dAlt;
q1Alt = -(c + dAlt);
fAlt = q0Alt + w;
gAlt = -1 - w q0Alt;
mAlt = q1Alt (1 + w);
zAlt = Together[
  -(fAlt + mAlt a - gAlt a^2)/(gAlt - mAlt a - fAlt a^2)
];
matrixAlt = Join[
  {
    evaluation[w][[1]] - q0Alt evaluation[w][[3]],
    evaluation[w][[2]] - q1Alt evaluation[w][[3]]
  },
  evaluation[zAlt]
];
alternateMinor = Together[Det[matrixAlt[[{1, 2, 3, 5}]]]];
expectedAlternateMinor = Together[
  15 (c - 2) (c - 1)^2 (c + 1)^6 (c + 2)
    (2 c - 1) (2 c + 1) (c^2 + 1)/
    (c^4 (4 c^2 + 5 c + 4)^4)
];
If[!zeroQ[alternateMinor - expectedAlternateMinor],
  Print["FAIL removable minor coverage"]; Exit[1]
];
If[!zeroQ[(lambda /. d -> -c) + (c - 1) (4 c^2 + 5 c + 4)],
  Print["FAIL Lambda d=-c relation"]; Exit[1]
];

phi = (
  16 c^4 d^4 - 9 c^4 d^3 - 8 c^3 d^4 + 28 c^4 d^2
  - 30 c^3 d^3 - 15 c^2 d^4 - 24 c^4 d - 14 c^3 d^2
  + 51 c^2 d^3 + 4 c d^4 + 4 c^4 + 12 c^3 d - 30 c^2 d^2
  + 12 c d^3 + 4 d^4 + 4 c^3 + 51 c^2 d - 14 c d^2 - 24 d^3
  - 15 c^2 - 30 c d + 28 d^2 - 8 c - 9 d + 16
);
psi = (
  16 c^4 d^4 - 23 c^4 d^3 - 8 c^3 d^4 + 12 c^4 d^2
  + 22 c^3 d^3 - 15 c^2 d^4 - 8 c^4 d + 6 c^3 d^2
  + 33 c^2 d^3 + 4 c d^4 + 4 c^4 - 20 c^3 d - 30 c^2 d^2
  - 20 c d^3 + 4 d^4 + 4 c^3 + 33 c^2 d + 6 c d^2 - 8 d^3
  - 15 c^2 + 22 c d + 12 d^2 - 8 c - 23 d + 16
);
target = ((W - 1/d) (W - d))^2;
claimed = (
  2 phi/(d lambda^2) (W + W^3)
  - phi psi/(d^2 lambda^4) W^2
);

If[!zeroQ[r - target - claimed],
  Print["FAIL difference identity"]; Exit[1]
];
If[!zeroQ[(r /. W -> 1/d) - phi^2/(d^4 lambda^4)],
  Print["FAIL evaluation identity"]; Exit[1]
];

Print[<|
  "schema" -> "kb-mca-v4-m2-diagonal-112-near-negative-qslice-wolfram-v1",
  "loci" -> loci[[All, 1]],
  "common_monic_residual" -> True,
  "lambda_is_c_times_parent_E" -> True,
  "leading_coefficient_identity" -> True,
  "default_minor_factorization" -> True,
  "removable_minor_coverage" -> True,
  "difference_identity" -> True,
  "evaluation_identity" -> True,
  "terminal" -> "DELETED_BY_FORBIDDEN_XI_TAU_ELL_COLLISION"
|>];
Exit[0];
