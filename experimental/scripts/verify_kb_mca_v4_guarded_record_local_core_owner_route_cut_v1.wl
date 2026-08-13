(* Independent Wolfram replay of the guarded core-owner route cut. *)
p = 11; dom = Range[10]; k = 5; m = 7; w = m - k;
slopes = {0, 2, 3, 5, 6, 8, 9};
u = {0, 1, 4, 10, 9, 6, 9, 4, 3, 0};
v = {7, 2, 10, 7, 9, 5, 2, 2, 9, 3};
coeffs = {{4, 6, 8, 8, 2}, {10, 6, 10, 9, 1}, {7, 9, 1, 8, 7},
  {0, 10, 2, 0, 1}, {8, 2, 3, 5, 3}, {10, 2, 2, 3, 6},
  {4, 8, 0, 10, 8}};
supports = {{2, 5, 6, 7, 8, 9, 10}, {1, 3, 5, 6, 7, 8, 10},
  {1, 2, 3, 4, 8, 9, 10}, {1, 2, 5, 6, 8, 9, 10},
  {2, 4, 5, 6, 8, 9, 10}, {1, 3, 5, 7, 8, 9, 10},
  {1, 2, 4, 5, 6, 7, 10}};
peval[c_, x_] := Mod[Sum[c[[j + 1]] x^j, {j, 0, Length[c] - 1}], p];
words = Table[Mod[u + slopes[[i]] v, p], {i, Length[slopes]}];
actualSupports = Table[Pick[dom, MapThread[Equal,
    {Map[peval[coeffs[[i]], #] &, dom], words[[i]]}]], {i, Length[slopes]}];
indices = Subsets[Range[7], {6}];
cores = (Intersection @@ supports[[#]]) & /@ indices;
shiftRank[i_, s_] := MatrixRank[Mod[Table[
    Join[Table[words[[i, j]] dom[[j]]^a, {a, 0, s}],
      Table[-dom[[j]]^a, {a, 0, s + k - 1}]], {j, 1, Length[dom]}], p],
    Modulus -> p];
d1 = Table[First @ Select[Range[0, 5], shiftRank[i, #] < (2 # + k + 1) &],
   {i, 1, 7}];
global = Intersection @@ supports;
compiler[ss_, kk_, affine_, separated_] := Module[{core, s},
  core = Intersection @@ ss;
  If[affine, Return["GLOBAL_AFFINE_PAID"]];
  If[core === {}, Return["EMPTY_GLOBAL_CORE_WITH_LOCAL_CRITICAL_CORES"]];
  s = kk - Length[core];
  Which[s <= 2, "FIXED_CORE_GENERIC_PAID_s_LE_2",
    s <= 13 && separated, "DIRECTION_SEPARATED_PAID_3_LE_s_LE_13",
    s <= 13, "DIRECTION_LIST_SHORTENED_" <> ToString[s],
    True, "COMMON_CORE_SHORTENED_s_GE_14"]];
compilerControls = {
  compiler[supports, k, False, False],
  compiler[{{1, 2, 3, 4}, {1, 2, 3, 5}}, 4, False, False],
  compiler[{{1, 2}, {1, 3}}, 6, False, True],
  compiler[{{1, 2}, {2, 3}}, 20, False, False],
  compiler[{{1}, {2}}, 5, False, False],
  compiler[{{1}, {2}}, 5, True, False]};
sharpSupports = (Complement[Range[0, 3], {#}] &) /@ Range[0, 3];
sharpErrors = Table[Product[z - j, {j, DeleteCases[Range[0, 3], i]}],
  {i, Range[0, 3]}];
sharpFence = <|
  "globalCore" -> Intersection @@ sharpSupports,
  "threeWiseCores" -> (Intersection @@ # & /@ Subsets[sharpSupports, {3}]),
  "degrees" -> (Exponent[#, z] & /@ sharpErrors),
  "offDiagonalZero" -> And @@ Flatten@Table[
    Mod[sharpErrors[[i + 1]] /. z -> j, 5] == 0,
    {i, 0, 3}, {j, DeleteCases[Range[0, 3], i]}],
  "diagonalNonzero" -> And @@ Table[
    Mod[sharpErrors[[i + 1]] /. z -> i, 5] != 0, {i, 0, 3}]|>;
overlapLocator = Expand[Product[z-j, {j, {0, 1, 2}}]];
overlapBase = {1 + 4 z + 2 z^3, 3 + z + 6 z^2};
overlapDirection = {2, 5};
overlapChanged = Expand[overlapBase + overlapDirection overlapLocator];
overlapRay = <|
  "sharedEqual" -> And @@ Flatten@Table[
    Mod[overlapChanged[[i]] /. z -> j, 7] ==
      Mod[overlapBase[[i]] /. z -> j, 7], {i, 1, 2}, {j, 0, 2}],
  "newScalar" -> Mod[overlapLocator /. z -> 3, 7],
  "newDifference" -> Mod[(overlapChanged-overlapBase) /. z -> 3, 7],
  "primitiveNoCommonRayBound" -> 1963173|>;
xi[m_, cap_] := Module[{u = Quotient[m, cap], r = Mod[m, cap]},
  Binomial[m, 2]-u Binomial[cap, 2]-Binomial[r, 2]];
guardedRay[q_] := Floor[(1048576+q)/q] 981105 +
  Floor[31 Binomial[1048576+q, 2]/xi[67472+q, q-1]];
guardedRayValues = Table[guardedRay[q], {q, 3, 1048576}];
guardedRayMaximum = Max[guardedRayValues];
guardedRayArgmax = First@FirstPosition[guardedRayValues, guardedRayMaximum]+2;
linerayCaps = Table[Binomial[981104+a, a], {a, 0, 4}];
linerayGate = <|"caps" -> linerayCaps,
  "lastPaidRank" -> Max@Select[Range[0, 4], linerayCaps[[#+1]] <= 274980728111395087 &],
  "earlierAddback" -> 134975,
  "rank3SlackAfterAddback" -> 274980728111395087-134975-linerayCaps[[4]],
  "firstUnpaidRank" -> 4|>;
affinePred = Table[Mod[coeffs[[1]] + (slopes[[i]] - slopes[[1]])
      PowerMod[slopes[[2]] - slopes[[1]], -1, p]
      (coeffs[[2]] - coeffs[[1]]), p], {i, 1, 7}];
result = <|"supportsMatch" -> (actualSupports === supports), "d1" -> d1,
   "criticalCores" -> cores, "coreHistogram" -> Counts[cores],
   "globalCore" -> global, "globalAffine" -> (affinePred === coeffs),
   "globalCoreCompiler" -> compilerControls,
   "coherentFenceSharpControl" -> sharpFence,
   "overlapRayControl" -> overlapRay,
   "guardedRay" -> <|"maximum" -> guardedRayMaximum,
     "argmaxQ" -> guardedRayArgmax,
     "slack" -> 274980728111395087-guardedRayMaximum|>,
   "allLineRayGate" -> linerayGate,
   "nearRationalCharge" -> 2*67472, "exceptionReserve" -> 31,
   "jointReserve" -> (2*67472 + 31),
   "signedRemaining" -> (274980728111395087 - (2*67472 + 31))|>;
If[result =!= <|"supportsMatch" -> True, "d1" -> ConstantArray[3, 7],
    "criticalCores" -> {{8, 10}, {10}, {10}, {10}, {5, 10}, {10}, {10}},
    "coreHistogram" -> <|{8, 10} -> 1, {10} -> 5, {5, 10} -> 1|>,
    "globalCore" -> {10}, "globalAffine" -> False,
    "globalCoreCompiler" -> {"DIRECTION_LIST_SHORTENED_4",
      "FIXED_CORE_GENERIC_PAID_s_LE_2",
      "DIRECTION_SEPARATED_PAID_3_LE_s_LE_13",
      "COMMON_CORE_SHORTENED_s_GE_14",
      "EMPTY_GLOBAL_CORE_WITH_LOCAL_CRITICAL_CORES", "GLOBAL_AFFINE_PAID"},
    "coherentFenceSharpControl" -> <|"globalCore" -> {},
      "threeWiseCores" -> {{3}, {2}, {1}, {0}},
      "degrees" -> {3, 3, 3, 3}, "offDiagonalZero" -> True,
      "diagonalNonzero" -> True|>,
    "overlapRayControl" -> <|"sharedEqual" -> True, "newScalar" -> 6,
      "newDifference" -> {5, 2}, "primitiveNoCommonRayBound" -> 1963173|>,
    "guardedRay" -> <|"maximum" -> 342921713716, "argmaxQ" -> 3,
      "slack" -> 274980385189681371|>,
    "allLineRayGate" -> <|"caps" -> {1, 981105, 481284001065,
      157397034144292985, 38605872343809750481845},
      "lastPaidRank" -> 3, "earlierAddback" -> 134975,
      "rank3SlackAfterAddback" -> 117583693966967127,
      "firstUnpaidRank" -> 4|>,
    "nearRationalCharge" -> 134944, "exceptionReserve" -> 31,
    "jointReserve" -> 134975, "signedRemaining" -> 274980728111260112|>,
  Print["FAIL ", result]; Exit[1]];
Print["KB_MCA_V4_GUARDED_CORE_OWNER_WOLFRAM_PASS ", result];
