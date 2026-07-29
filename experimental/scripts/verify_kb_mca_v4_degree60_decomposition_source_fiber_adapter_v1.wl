(* Exact Wolfram Language replay of the degree-60 decomposition
   source-fiber adapter.

   For f = F o h with inner degree m and outer degree n=60/m, a pole of
   f having order five can only arise from:

     outer order 5, ramification index 1; or
     outer order 1, ramification index 5.

   The latter consumes four units of Riemann--Hurwitz ramification at
   each point of the fibre.
*)

endpointDegree = 60;
poleOrder = 5;
sourcePointCount = 12;
fullDomainSize = 2^21;
deployedCharacteristic = 2130706433;
challengeFieldSize = deployedCharacteristic^6;

profiles = Reap[
  Do[
    outerDegree = endpointDegree/innerDegree;
    Do[
      remainder = outerDegree - simpleOuterPoles;
      If[
        Mod[remainder, poleOrder] == 0
          && (simpleOuterPoles == 0
            || Mod[innerDegree, poleOrder] == 0),
        orderFiveOuterPoles = remainder/poleOrder;
        forcedRamification =
          simpleOuterPoles*(poleOrder - 1)*innerDegree/poleOrder;
        riemannHurwitzBudget = 2*innerDegree - 2;
        If[
          forcedRamification <= riemannHurwitzBudget,
          Sow[<|
            "InnerDegree" -> innerDegree,
            "OuterDegree" -> outerDegree,
            "OrderFiveOuterPoles" -> orderFiveOuterPoles,
            "SimpleOuterPoles" -> simpleOuterPoles,
            "ActiveOuterZeros" -> outerDegree,
            "ActiveCompletePoints" -> outerDegree*innerDegree,
            "CompleteSourcePoints" ->
              orderFiveOuterPoles*innerDegree,
            "ExceptionalSourcePoints" ->
              simpleOuterPoles*innerDegree/poleOrder,
            "ForcedRamification" -> forcedRamification,
            "RiemannHurwitzBudget" -> riemannHurwitzBudget,
            "RiemannHurwitzSlack" ->
              riemannHurwitzBudget - forcedRamification,
            "SourcePartitionCount" ->
              sourcePointCount!/
                (innerDegree!^orderFiveOuterPoles
                  orderFiveOuterPoles!
                  If[simpleOuterPoles == 0, 1,
                    (innerDegree/poleOrder)!^simpleOuterPoles
                      simpleOuterPoles!]),
            "FullDomainDivides2Power21" ->
              (Mod[fullDomainSize, innerDegree] == 0)
          |>]
        ]
      ],
      {simpleOuterPoles, 0, outerDegree}
    ],
    {innerDegree,
      Select[Divisors[endpointDegree], 1 < # < endpointDegree &]}
  ]
][[2, 1]];

profiles = SortBy[profiles, Lookup[#, "InnerDegree"] &];

expected = {
  <|"InnerDegree" -> 2, "OuterDegree" -> 30,
    "OrderFiveOuterPoles" -> 6, "SimpleOuterPoles" -> 0,
    "ActiveOuterZeros" -> 30, "ActiveCompletePoints" -> 60,
    "CompleteSourcePoints" -> 12, "ExceptionalSourcePoints" -> 0,
    "ForcedRamification" -> 0, "RiemannHurwitzBudget" -> 2,
    "RiemannHurwitzSlack" -> 2,
    "SourcePartitionCount" -> 10395,
    "FullDomainDivides2Power21" -> True|>,
  <|"InnerDegree" -> 3, "OuterDegree" -> 20,
    "OrderFiveOuterPoles" -> 4, "SimpleOuterPoles" -> 0,
    "ActiveOuterZeros" -> 20, "ActiveCompletePoints" -> 60,
    "CompleteSourcePoints" -> 12, "ExceptionalSourcePoints" -> 0,
    "ForcedRamification" -> 0, "RiemannHurwitzBudget" -> 4,
    "RiemannHurwitzSlack" -> 4,
    "SourcePartitionCount" -> 15400,
    "FullDomainDivides2Power21" -> False|>,
  <|"InnerDegree" -> 4, "OuterDegree" -> 15,
    "OrderFiveOuterPoles" -> 3, "SimpleOuterPoles" -> 0,
    "ActiveOuterZeros" -> 15, "ActiveCompletePoints" -> 60,
    "CompleteSourcePoints" -> 12, "ExceptionalSourcePoints" -> 0,
    "ForcedRamification" -> 0, "RiemannHurwitzBudget" -> 6,
    "RiemannHurwitzSlack" -> 6,
    "SourcePartitionCount" -> 5775,
    "FullDomainDivides2Power21" -> True|>,
  <|"InnerDegree" -> 5, "OuterDegree" -> 12,
    "OrderFiveOuterPoles" -> 2, "SimpleOuterPoles" -> 2,
    "ActiveOuterZeros" -> 12, "ActiveCompletePoints" -> 60,
    "CompleteSourcePoints" -> 10, "ExceptionalSourcePoints" -> 2,
    "ForcedRamification" -> 8, "RiemannHurwitzBudget" -> 8,
    "RiemannHurwitzSlack" -> 0,
    "SourcePartitionCount" -> 8316,
    "FullDomainDivides2Power21" -> False|>,
  <|"InnerDegree" -> 6, "OuterDegree" -> 10,
    "OrderFiveOuterPoles" -> 2, "SimpleOuterPoles" -> 0,
    "ActiveOuterZeros" -> 10, "ActiveCompletePoints" -> 60,
    "CompleteSourcePoints" -> 12, "ExceptionalSourcePoints" -> 0,
    "ForcedRamification" -> 0, "RiemannHurwitzBudget" -> 10,
    "RiemannHurwitzSlack" -> 10,
    "SourcePartitionCount" -> 462,
    "FullDomainDivides2Power21" -> False|>,
  <|"InnerDegree" -> 10, "OuterDegree" -> 6,
    "OrderFiveOuterPoles" -> 1, "SimpleOuterPoles" -> 1,
    "ActiveOuterZeros" -> 6, "ActiveCompletePoints" -> 60,
    "CompleteSourcePoints" -> 10, "ExceptionalSourcePoints" -> 2,
    "ForcedRamification" -> 8, "RiemannHurwitzBudget" -> 18,
    "RiemannHurwitzSlack" -> 10,
    "SourcePartitionCount" -> 66,
    "FullDomainDivides2Power21" -> False|>,
  <|"InnerDegree" -> 12, "OuterDegree" -> 5,
    "OrderFiveOuterPoles" -> 1, "SimpleOuterPoles" -> 0,
    "ActiveOuterZeros" -> 5, "ActiveCompletePoints" -> 60,
    "CompleteSourcePoints" -> 12, "ExceptionalSourcePoints" -> 0,
    "ForcedRamification" -> 0, "RiemannHurwitzBudget" -> 22,
    "RiemannHurwitzSlack" -> 22,
    "SourcePartitionCount" -> 1,
    "FullDomainDivides2Power21" -> False|>,
  <|"InnerDegree" -> 30, "OuterDegree" -> 2,
    "OrderFiveOuterPoles" -> 0, "SimpleOuterPoles" -> 2,
    "ActiveOuterZeros" -> 2, "ActiveCompletePoints" -> 60,
    "CompleteSourcePoints" -> 0, "ExceptionalSourcePoints" -> 12,
    "ForcedRamification" -> 48, "RiemannHurwitzBudget" -> 58,
    "RiemannHurwitzSlack" -> 10,
    "SourcePartitionCount" -> 462,
    "FullDomainDivides2Power21" -> False|>
};

If[profiles =!= expected,
  Print["status=FAIL_PROFILE_ENUMERATION"];
  Print[profiles];
  Exit[1];
];

accountingChecks = Map[
  Function[row,
    Lookup[row, "ActiveCompletePoints"] == endpointDegree
      && Lookup[row, "CompleteSourcePoints"]
        + Lookup[row, "ExceptionalSourcePoints"] == sourcePointCount
      && Lookup[row, "ForcedRamification"]
        + Lookup[row, "RiemannHurwitzSlack"]
        == Lookup[row, "RiemannHurwitzBudget"]
  ],
  profiles
];
If[
  !TrueQ[And @@ accountingChecks],
  Print["status=FAIL_DIVISOR_ACCOUNTING"];
  Exit[1];
];

eligibleDegrees = Lookup[
  Select[profiles, TrueQ[Lookup[#, "FullDomainDivides2Power21"]] &],
  "InnerDegree"
];
If[eligibleDegrees =!= {2, 4},
  Print["status=FAIL_FULL_DOMAIN_DIVISIBILITY"];
  Exit[1];
];

degreeFive = First[
  Select[profiles, Lookup[#, "InnerDegree"] == 5 &]
];

If[
  !(PrimeQ[deployedCharacteristic]
    && Mod[deployedCharacteristic, 5] == 3
    && Mod[challengeFieldSize, 5] == 4
    && Lookup[degreeFive, "SimpleOuterPoles"] == 2
    && Lookup[degreeFive, "ExceptionalSourcePoints"] == 2
    && Lookup[degreeFive, "ForcedRamification"] == 8
    && Lookup[degreeFive, "RiemannHurwitzBudget"] == 8
    && Lookup[degreeFive, "RiemannHurwitzSlack"] == 0
    && CoprimeQ[5, challengeFieldSize - 1]),
  Print["status=FAIL_DEGREE5_CHALLENGE_FIELD_GATE"];
  Exit[1];
];

degreeThirty = First[
  Select[profiles, Lookup[#, "InnerDegree"] == 30 &]
];
If[
  !(Lookup[degreeThirty, "SimpleOuterPoles"] == 2
    && Lookup[degreeThirty, "CompleteSourcePoints"] == 0
    && Lookup[degreeThirty, "ExceptionalSourcePoints"] == 12
    && Lookup[degreeThirty, "InnerDegree"]/5 == 6),
  Print["status=FAIL_DEGREE30_REFINEMENT"];
  Exit[1];
];

degreeTwelve = First[
  Select[profiles, Lookup[#, "InnerDegree"] == 12 &]
];
If[Lookup[degreeTwelve, "SourcePartitionCount"] =!= 1,
  Print["status=FAIL_DEGREE12_CANONICAL_PARTITION"];
  Exit[1];
];

Print["status=PROVED_DEGREE60_DECOMPOSITION_SOURCE_FIBER_ADAPTER"];
Print["inner_degrees=", Lookup[profiles, "InnerDegree"]];
Print["conditional_same_degree_carrier_eligible_degrees=", eligibleDegrees];
Print["source_splits=", (
  {
    Lookup[#, "InnerDegree"],
    Lookup[#, "CompleteSourcePoints"],
    Lookup[#, "ExceptionalSourcePoints"]
  } & /@ profiles
)];
Print["degree5_rh_saturated=True"];
Print["source_partition_counts=",
  Lookup[profiles, "SourcePartitionCount"]];
Print["challenge_field_cardinality_mod5=",
  Mod[challengeFieldSize, 5]];
Print["fifth_power_on_challenge_field_bijective=True"];
Print["degree30_refined_inner_degree=6"];
Print["degree12_canonical_source_partition_count=1"];
