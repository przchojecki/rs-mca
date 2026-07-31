#!/usr/bin/env wolframscript
(* Independent exact-rational replay of the 36-cell q-slice atlas. *)

ClearAll["Global`*"];

fail[message_] := (Print["FAIL: " <> message]; Exit[1]);
check[condition_, message_] := If[! TrueQ[condition], fail[message]];

experimentalRoot = DirectoryName[DirectoryName[$InputFileName]];
certificatePath = FileNameJoin[{
    experimentalRoot,
    "data", "certificates",
    "kb-mca-v4-m2-aligned-positive-qslice-atlas-v1",
    "kb_mca_v4_m2_aligned_positive_qslice_atlas_v1.json"
}];
data = Import[certificatePath, "RawJSON"];

edges = <|
    "E01" -> {"v0", "v1"}, "E02" -> {"v0", "v2"},
    "E03" -> {"v0", "v3"}, "E12" -> {"v1", "v2"},
    "E13" -> {"v1", "v3"}, "E23" -> {"v2", "v3"}
|>;
assignments = <|
    "F00" -> {"E01", "E02"}, "F01" -> {"E01", "E03"},
    "F02" -> {"E01", "E12"}, "F03" -> {"E01", "E13"},
    "F04" -> {"E02", "E23"}, "F05" -> {"E03", "E23"},
    "F06" -> {"E12", "E23"}, "F07" -> {"E13", "E23"},
    "M00" -> {"E02", "E03"}, "M01" -> {"E02", "E12"},
    "M02" -> {"E03", "E13"}, "M03" -> {"E12", "E13"}
|>;
bInversion = <|
    "F00" -> "F01", "F01" -> "F00",
    "F02" -> "F03", "F03" -> "F02",
    "F04" -> "F05", "F05" -> "F04",
    "F06" -> "F07", "F07" -> "F06",
    "M00" -> "M00", "M01" -> "M02",
    "M02" -> "M01", "M03" -> "M03"
|>;
targetIds = {"R02", "R11", "R20"};

check[data["schema"] ===
    "kb-mca-v4-m2-aligned-positive-qslice-atlas-v1", "schema"];
check[data["parent"]["commit"] ===
    "c2edcfa5cbfb8a41e7dea04ae1b34325c90ed5dc", "parent"];
check[Length[data["assignments"]] === 12, "assignment count"];
check[Length[data["cells"]] === 36, "cell count"];
check[Length[DeleteDuplicates[Lookup[data["cells"], "cell_id"]]] === 36,
    "duplicate cell"];

expectedCells = Flatten[
    Table[assignmentId <> "-" <> targetId,
        {assignmentId, Keys[assignments]}, {targetId, targetIds}]
];
check[Sort[Lookup[data["cells"], "cell_id"]] === Sort[expectedCells],
    "cell Cartesian product"];
check[And @@ (Lookup[#, "classification"] ===
        "UNCLASSIFIED_QSLICE_GENERATED" & /@ data["cells"]),
    "cell classifications"];
check[And @@ (Lookup[#, "ledger_movement"] === 0 & /@ data["cells"]),
    "cell ledger movement"];
check[data["rejected_globalizations"] === {
    "ENDPOINT_ONLY_MOBIUS_ORBIT",
    "DIAGONAL_W_MOBIUS_ORBIT",
    "FULL_SOURCE_SYSTEM_COVARIANCE"
}, "rejected covariance"];
check[data["external_provenance_policy"]["external_scopes_imported"] ===
    False, "external scope import"];
check[And @@ (
    If[Lookup[#, "external_provenance"] === Null, True,
        Lookup[Lookup[#, "external_provenance"], "scope_imported"] === False]
    & /@ data["cells"]), "per-cell external scope"];
check[MemberQ[data["nonclaims"],
    "no Mobius or diagonal-W covariance"], "covariance nonclaim"];
check[MemberQ[data["nonclaims"],
    "no owner or charge"], "owner nonclaim"];
check[MemberQ[data["nonclaims"],
    "no K3 or KoalaBear row closure"], "K3 nonclaim"];

vertexValues[bValue_] := <|
    "v0" -> 2, "v1" -> 1/2, "v2" -> bValue, "v3" -> 1/bValue
|>;

edgeVector[edgeId_, values_] := Module[{ids, left, right},
    ids = edges[edgeId];
    left = values[ids[[1]]];
    right = values[ids[[2]]];
    {left right, -(left + right), 1}
];

targetCoefficients[targetId_, side_, cValue_, dValue_] :=
    Which[
        targetId === "R02",
            With[{root = If[side === "c", dValue, cValue]},
                {1/root^2, -2/root, 1}],
        targetId === "R11",
            {1/(cValue dValue), -(cValue + dValue)/(cValue dValue), 1},
        targetId === "R20",
            With[{root = If[side === "c", cValue, dValue]},
                {1/root^2, -2/root, 1}],
        True, fail["unknown target"]
    ];

exactCellValues[assignmentId_, targetId_, fixture_] := Module[
    {
        bValue, cValue, dValue, wValue, values, pair, firstVertices,
        secondVertices, commonId, rightId, leftId, common, right, left,
        first, second, q0, q1, f, g, m, v, vCommon, incidenceN,
        incidenceD, z, vz, linear1, linear0, internalTarget,
        swappedTarget, p0, p1, p2, difference, rhsSum, rhsSource,
        blockDet, sumOuter, x0, x1, x2, x3, x4, atW2, u,
        residualAt, result, observed, target, sideRoot, side, root
    },
    bValue = fixture["b"]; cValue = fixture["c"];
    dValue = fixture["d"]; wValue = fixture["w"];
    values = vertexValues[bValue];
    pair = assignments[assignmentId];
    firstVertices = edges[pair[[1]]];
    secondVertices = edges[pair[[2]]];
    commonId = First[Intersection[firstVertices, secondVertices]];
    rightId = First[Complement[firstVertices, {commonId}]];
    leftId = First[Complement[secondVertices, {commonId}]];
    common = values[commonId]; right = values[rightId]; left = values[leftId];
    first = edgeVector[pair[[1]], values];
    second = edgeVector[pair[[2]], values];

    q0 = cValue dValue; q1 = -(cValue + dValue);
    f = q0 - wValue; g = 1 - wValue q0; m = q1 (1 - wValue);
    v = {f + g X, m (1 + X), g + f X};
    vCommon = Sum[common^(index - 1) v[[index]], {index, 1, 3}];
    incidenceN = Coefficient[vCommon, X, 0];
    incidenceD = Coefficient[vCommon, X, 1];
    check[incidenceD =!= 0, assignmentId <> " incidence denominator"];
    z = -incidenceN/incidenceD;
    vz = (Expand[# /. X -> z] &) /@ v;
    check[Together[vz[[1]] + common vz[[2]] + common^2 vz[[3]]] === 0,
        assignmentId <> " incidence"];
    linear1 = vz[[3]];
    linear0 = vz[[2]] + common vz[[3]];
    internalTarget = Together[
        ((linear0 + left linear1) first +
         (linear0 + right linear1) second)/(left - right)
    ];
    swappedTarget = Together[
        ((linear0 + right linear1) second +
         (linear0 + left linear1) first)/(right - left)
    ];
    check[And @@ Thread[Together[swappedTarget + internalTarget] == 0],
        assignmentId <> " star-swap sign"];

    {p0, p1, p2} = internalTarget;
    difference = (p0 - p2)/(1 - z^2);
    rhsSum = p0 + p2;
    rhsSource = -(1 + q0) (1 - wValue^2) difference/(2 (1 - q0));
    blockDet = (wValue - z) (1 - wValue z);
    check[blockDet =!= 0, assignmentId <> " reconstruction block"];
    sumOuter = (rhsSum wValue - 2 z rhsSource)/blockDet;
    x1 = ((1 + z^2) rhsSource - (1 + wValue^2) rhsSum/2)/blockDet;
    x0 = (sumOuter + difference)/2;
    x2 = (sumOuter - difference)/2;
    atW2 = x2 + x1 wValue + x0 wValue^2;
    x3 = (p1 wValue - z q1 atW2)/blockDet;
    x4 = ((1 + z^2) q1 atW2 - (1 + wValue^2) p1)/blockDet;
    u = {x0 + x1 X + x2 X^2, x3 (1 + X^2) + x4 X,
         x2 + x1 X + x0 X^2};

    residualAt[root_] := Module[{uRoot, vRoot, norm, divisor, remainder},
        uRoot = Sum[root^(index - 1) u[[index]], {index, 1, 3}];
        vRoot = Sum[root^(index - 1) v[[index]], {index, 1, 3}];
        norm = Together[Expand[uRoot^2 - X vRoot^2]];
        divisor = (X - wValue)^2;
        remainder = Together[PolynomialRemainder[norm, divisor, X]];
        check[remainder === 0, assignmentId <> " forced-square remainder"];
        Expand[PolynomialQuotient[norm, divisor, X]]
    ];

    result = {};
    Do[
        side = sideRoot[[1]];
        root = sideRoot[[2]];
        observed = CoefficientList[residualAt[root], X];
        check[Length[observed] === 3, assignmentId <> " residual degree"];
        target = targetCoefficients[targetId, side, cValue, dValue];
        result = Join[result, Together /@ {
            observed[[1]] - observed[[3]] target[[1]],
            observed[[2]] - observed[[3]] target[[2]]
        }],
        {sideRoot, {{"c", cValue}, {"d", dValue}}}
    ];
    result
];

cellsById = AssociationThread[
    Lookup[data["cells"], "cell_id"] -> data["cells"]
];
fixtures = data["exact_rational_fixtures"];
replays = 0;
Do[
    cellId = assignmentId <> "-" <> targetId;
    cell = cellsById[cellId];
    stored = AssociationThread[
        Lookup[cell["exact_rational_fixture_values"], "fixture_id"] ->
        Lookup[cell["exact_rational_fixture_values"], "values"]
    ];
    Do[
        values = exactCellValues[assignmentId, targetId, fixture];
        expected = ToExpression /@ stored[fixture["id"]];
        check[values === expected, cellId <> " fixture " <> fixture["id"]];
        replays++,
        {fixture, fixtures}
    ],
    {assignmentId, Keys[assignments]}, {targetId, targetIds}
];

(* Literal c<->d and b->b^-1 checks from the formulas, never from a claimed
   orbit action.  These are controls at both exact QQ fixtures. *)
symmetryChecks = 0;
Do[
    Do[
        original = exactCellValues[assignmentId, targetId, fixture];
        swappedFixture = Association[fixture];
        swappedFixture["c"] = fixture["d"];
        swappedFixture["d"] = fixture["c"];
        swapped = exactCellValues[assignmentId, targetId, swappedFixture];
        check[swapped === original[[{3, 4, 1, 2}]],
            assignmentId <> "-" <> targetId <> " c-d companion"];

        invertedFixture = Association[fixture];
        invertedFixture["b"] = 1/fixture["b"];
        inverted = exactCellValues[assignmentId, targetId, invertedFixture];
        partner = exactCellValues[bInversion[assignmentId], targetId, fixture];
        check[inverted === partner,
            assignmentId <> "-" <> targetId <> " b inversion"];
        symmetryChecks += 2,
        {fixture, fixtures}
    ],
    {assignmentId, Keys[assignments]}, {targetId, targetIds}
];

Print[
    "PASS: Wolfram exact aligned-positive atlas cells=36 fixture_replays=",
    replays, " symmetry_checks=", symmetryChecks,
    " payload=", data["payload_sha256"]
];
Exit[0];
