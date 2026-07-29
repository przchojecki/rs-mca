(* Independent exact Wolfram Language replay for the degree-60 outer
   primitive-subdegree route compiler.

   This file checks only the finite arithmetic and branch-cycle data in the
   companion JSON certificate.  It does not prove the imported primitive
   group classification, the geometric decomposition lemmas, an owner,
   ledger movement, or K3/row closure.
*)

ClearAll["Global`*"];

fail[message_] := (
  Print["status=FAIL"];
  Print["failure=", message];
  Exit[1]
);
require[condition_, message_] := If[!TrueQ[condition], fail[message]];

scriptDirectory = DirectoryName[AbsoluteFileName[$InputFileName]];
certificatePath = FileNameJoin[{
  scriptDirectory,
  "..",
  "data",
  "certificates",
  "kb-mca-v4-degree60-outer-primitive-route-compiler-v1",
  "kb_mca_v4_degree60_outer_primitive_route_compiler_v1.json"
}];
certificate = Quiet[Check[Import[certificatePath, "RawJSON"], $Failed]];
require[AssociationQ[certificate], "certificate import"];
require[
  Lookup[certificate, "schema", Missing["schema"]] ===
    "kb-mca-v4-degree60-outer-primitive-route-compiler-v1",
  "certificate schema"
];

(* Reconstruct the certificate's live-row partition. *)
conclusion = Lookup[certificate, "conclusion", <||>];
liveRows = Lookup[certificate, "live_row_classification", {}];
deletedRows = Lookup[certificate, "parent_deleted_rows", {}];

rowTriple[row_] := Lookup[row, {"m", "r", "delta"}];
terminalRows[name_] := Select[
  liveRows,
  Lookup[#, "terminal", Missing["terminal"]] === name &
];

forcedRows = terminalRows["FORCED_STRICT_OUTER_DECOMPOSITION"];
contradictionRows = terminalRows["ACTUAL_PRODUCER_CONTRADICTION"];
survivorRows = terminalRows["PRIMITIVE_OUTER_COMPATIBLE_SURVIVOR"];

partitionCounts = {
  Lookup[conclusion, "original_transverse_type_count", -1],
  Lookup[conclusion, "parent_deleted_type_count", -1],
  Lookup[conclusion, "live_input_type_count", -1],
  Lookup[conclusion, "forced_strict_outer_decomposition_type_count", -1],
  Lookup[conclusion, "new_actual_producer_contradiction_type_count", -1],
  Lookup[conclusion, "primitive_outer_survivor_type_count", -1]
};
require[partitionCounts === {26, 2, 24, 18, 1, 5},
  "26/2/24/18/1/5 conclusion counts"];
require[
  {
    Length[deletedRows],
    Length[liveRows],
    Length[forcedRows],
    Length[contradictionRows],
    Length[survivorRows]
  } === {2, 24, 18, 1, 5},
  "classification row counts"
];
require[24 == 18 + 1 + 5, "live partition identity"];
require[
  Sort[rowTriple /@ deletedRows] === Sort[{{12, 1, 48}, {12, 3, 16}}],
  "parent-deleted rows"
];
require[
  rowTriple /@ contradictionRows === {{10, 4, 10}},
  "new contradiction row"
];
expectedSurvivors = {
  {6, 3, 8},
  {6, 6, 4},
  {10, 5, 8},
  {12, 2, 24},
  {12, 4, 12}
};
require[
  rowTriple /@ survivorRows === expectedSurvivors,
  "primitive-compatible survivor rows"
];
require[
  Lookup[conclusion, "primitive_outer_survivors", {}] ===
    expectedSurvivors,
  "conclusion survivor rows"
];

(* Exact challenge-field arithmetic for the deleted m=6 -> m=30 edge. *)
p = 2130706433;
extensionDegree = 6;
q = p^extensionDegree;
require[PrimeQ[p], "deployed characteristic primality"];
require[Mod[p, 5] == 3, "p modulo five"];
require[Mod[q, 5] == 4, "q modulo five"];
require[CoprimeQ[5, q - 1], "fifth-power permutation gcd"];

fieldArithmetic = Lookup[
  Lookup[
    certificate,
    "m6_degree_five_outer_right_factor_exclusion",
    <||>
  ],
  "field_arithmetic",
  <||>
];
require[
  Lookup[
    fieldArithmetic,
    {"p", "extension_degree", "gcd_5_q_minus_1"}
  ] === {p, extensionDegree, 1},
  "certificate challenge-field arithmetic"
];
require[
  TrueQ[Lookup[fieldArithmetic, "fifth_power_permutates_K", False]],
  "certificate fifth-power terminal"
];

(* The m=10,r=4 decomposition arithmetic has no viable right factor. *)
allowedSourceInnerDegrees = {2, 3, 4, 5, 6, 10, 12, 30};
m10 = 10;
r10 = 4;
e2 = 2;
e3 = 3;
rPrime = 1;
epsilon = e3*r10/rPrime;
require[
  !MemberQ[allowedSourceInnerDegrees, m10*e2],
  "m10 degree-two right factor source-profile gate"
];
require[
  r10 > e3 - 1,
  "m10 degree-three same-fibre inequality"
];
require[IntegerQ[epsilon] && epsilon == 12,
  "m10 transverse cover degree"];
require[epsilon > e3^2 && e3^2 == 9,
  "m10 transverse cover bound contradiction"];

(* Pure permutation arithmetic for the m=4,r=8 branch-cycle table. *)
cycleTypePermutation[cycleType_List] := Module[
  {permutation, offset, cycle, length, index},
  permutation = Range[Total[cycleType]];
  offset = 0;
  Do[
    cycle = Range[offset + 1, offset + length];
    Do[
      permutation[[cycle[[index]]]] =
        cycle[[Mod[index, length] + 1]],
      {index, 1, length}
    ];
    offset += length,
    {length, cycleType}
  ];
  permutation
];

cycleCount[permutation_List] := Module[
  {seen, cycles, point, start},
  seen = ConstantArray[False, Length[permutation]];
  cycles = 0;
  Do[
    If[!TrueQ[seen[[start]]],
      cycles++;
      point = start;
      While[!TrueQ[seen[[point]]],
        seen[[point]] = True;
        point = permutation[[point]]
      ]
    ],
    {start, 1, Length[permutation]}
  ];
  cycles
];

permutationIndex[permutation_List] :=
  Length[permutation] - cycleCount[permutation];

twoSubsets = Subsets[Range[6], {2}];
intersectionOneOrbital = Select[
  Tuples[Range[Length[twoSubsets]], 2],
  Length[
    Intersection[
      twoSubsets[[#[[1]]]],
      twoSubsets[[#[[2]]]]
    ]
  ] == 1 &
];
require[Length[twoSubsets] == 15, "degree-fifteen action size"];
require[Length[intersectionOneOrbital] == 120, "r8 orbital size"];

inducedTwoSubsetPermutation[permutation_List] := (
  FirstPosition[
    twoSubsets,
    Sort[permutation[[#]]]
  ][[1]] & /@ twoSubsets
);

inducedOrbitalPermutation[permutation_List] := Module[
  {subsetPermutation},
  subsetPermutation = inducedTwoSubsetPermutation[permutation];
  (
    FirstPosition[
      intersectionOneOrbital,
      subsetPermutation[[#]]
    ][[1]] & /@ intersectionOneOrbital
  )
];

computedClassTable = Table[
  Module[
    {permutation, naturalIndex, pointIndex, orbitalIndex},
    permutation = cycleTypePermutation[cycleType];
    naturalIndex = permutationIndex[permutation];
    pointIndex = permutationIndex[
      inducedTwoSubsetPermutation[permutation]
    ];
    orbitalIndex = permutationIndex[
      inducedOrbitalPermutation[permutation]
    ];
    {
      cycleType,
      If[OddQ[naturalIndex], -1, 1],
      pointIndex,
      orbitalIndex
    }
  ],
  {cycleType, IntegerPartitions[6]}
];

m4Ledger = Lookup[
  certificate,
  "m4_r8_primitive_branch_cycle_exclusion",
  <||>
];
certificateClassTable = (
  {
    Lookup[#, "natural_cycle_type"],
    Lookup[#, "natural_sign"],
    Lookup[#, "degree_fifteen_index"],
    Lookup[#, "r8_orbital_index"]
  } & /@ Lookup[m4Ledger, "class_index_table", {}]
);
require[
  computedClassTable === certificateClassTable,
  "m4 class-index table"
];
require[
  Lookup[
    m4Ledger,
    {
      "degree_fifteen_total_index",
      "r8_orbital_degree",
      "outer_component_genus_upper_bound"
    }
  ] === {28, 120, 2},
  "m4 Riemann-Hurwitz targets"
];
require[
  Lookup[m4Ledger, "allowed_r8_total_indices", {}] ===
    {238, 240, 242},
  "m4 orbital total-index range"
];

nonidentityClassTable = Select[computedClassTable, #[[3]] > 0 &];
poleClassIndex = First[
  FirstPosition[nonidentityClassTable[[All, 1]], {5, 1}]
];

enumerateBranchMultisets[allowedSigns_List] := Module[
  {solutions, search},
  solutions = {};
  search[
    position_Integer,
    pointRemaining_Integer,
    orbitalRemaining_Integer,
    counts_List
  ] := Module[
    {row, maximum, count},
    If[position > Length[nonidentityClassTable],
      If[
        pointRemaining == 0
          && orbitalRemaining == 0
          && counts[[poleClassIndex]] >= 1,
        AppendTo[solutions, counts]
      ];
      Return[Null]
    ];
    row = nonidentityClassTable[[position]];
    If[!MemberQ[allowedSigns, row[[2]]],
      search[
        position + 1,
        pointRemaining,
        orbitalRemaining,
        Append[counts, 0]
      ];
      Return[Null]
    ];
    maximum = Min[
      Quotient[pointRemaining, row[[3]]],
      Quotient[orbitalRemaining, row[[4]]]
    ];
    Do[
      search[
        position + 1,
        pointRemaining - count row[[3]],
        orbitalRemaining - count row[[4]],
        Append[counts, count]
      ],
      {count, 0, maximum}
    ]
  ];
  Do[
    search[1, 28, orbitalTotal, {}],
    {orbitalTotal, {238, 240, 242}}
  ];
  solutions
];

a6Solutions = enumerateBranchMultisets[{1}];
s6Solutions = enumerateBranchMultisets[{-1, 1}];
require[a6Solutions === {}, "A6 branch-class DP"];
require[Length[s6Solutions] == 1, "S6 branch-class DP uniqueness"];

uniqueS6Solution = First[s6Solutions];
uniqueS6Rows = MapThread[
  If[
    #2 > 0,
    {#1[[1]], #2},
    Nothing
  ] &,
  {nonidentityClassTable, uniqueS6Solution}
];
expectedUniqueS6Rows = {
  {{5, 1}, 2},
  {{2, 1, 1, 1, 1}, 1}
};
require[uniqueS6Rows === expectedUniqueS6Rows,
  "S6 unique branch-class multiset"];
uniqueProductSign = Times @@ MapThread[
  #1[[2]]^#2 &,
  {nonidentityClassTable, uniqueS6Solution}
];
require[uniqueProductSign == -1, "S6 unique product sign"];
certificateS6Multisets = Lookup[
  m4Ledger,
  "S6_necessary_class_multisets",
  Missing["S6"]
];
require[
  ListQ[certificateS6Multisets]
    && Length[certificateS6Multisets] == 1
    && ListQ[First[certificateS6Multisets]],
  "certificate S6 multiset shape"
];
certificateS6Rows = (
  {
    Lookup[#, "natural_cycle_type", Missing["cycle type"]],
    Lookup[#, "count", -1]
  } & /@
    First[certificateS6Multisets]
);
require[
  Lookup[m4Ledger, "A6_necessary_class_multisets", Missing["A6"]] === {}
    && certificateS6Rows === expectedUniqueS6Rows
    && Lookup[
      m4Ledger,
      "S6_unique_multiset_product_sign",
      0
    ] == -1
    && !TrueQ[Lookup[m4Ledger, "S6_product_one_possible", True]],
  "certificate m4 product-one contradiction"
];

(* Independent integer checks for the finite m=6,m=10 Nielsen ledger.
   Product-one, generation, conjugacy-class exhaustiveness, and orbit
   multiplicities are replayed by the companion Sage/GAP script. *)
nielsenLedger = Lookup[
  certificate,
  "primitive_survivor_low_genus_nielsen_ledger",
  <||>
];
m6Passports = Lookup[nielsenLedger, "m6_passports", {}];
m10Passports = Lookup[nielsenLedger, "m10_passports", {}];
allPassports = Join[m6Passports, m10Passports];
require[
  {Length[m6Passports], Length[m10Passports], Length[allPassports]}
    === {7, 9, 16},
  "Nielsen passport counts"
];
require[
  Lookup[nielsenLedger, "passport_count", -1] == 16,
  "certificate Nielsen passport count"
];
require[
  Total[
    Lookup[#, "simultaneous_conjugacy_orbit_count", -1] & /@
      allPassports
  ] == 18,
  "Nielsen simultaneous-conjugacy orbit count"
];
require[
  Lookup[nielsenLedger, "simultaneous_conjugacy_orbit_count", -1] == 18,
  "certificate Nielsen orbit count"
];

passportGenus[row_] := Module[
  {degree, subdegree, componentIndices},
  degree = Lookup[row, "outer_degree", -1];
  subdegree = Lookup[row, "subdegree", -1];
  componentIndices = Lookup[row, "component_indices", {}];
  (Total[componentIndices] - (2 degree subdegree - 2))/2
];

Do[
  require[
    Total[Lookup[row, "point_indices", {}]]
      == 2 Lookup[row, "outer_degree", -1] - 2,
    "Nielsen point-cover genus-zero identity"
  ];
  require[
    MemberQ[{0, 1}, passportGenus[row]]
      && passportGenus[row] == Lookup[row, "component_genus", -1],
    "Nielsen component-genus identity"
  ],
  {row, allPassports}
];
require[
  passportGenus /@ m6Passports === {0, 0, 0, 0, 1, 0, 1},
  "m6 component genera"
];
require[
  passportGenus /@ m10Passports === {0, 0, 1, 1, 1, 1, 1, 0, 1},
  "m10 component genera"
];
require[
  TrueQ[Lookup[nielsenLedger, "all_survivors_have_three_branch_values", False]],
  "three-branch Nielsen terminal"
];

(* Reconstruct the normalized route graph and prove it is acyclic. *)
terminalInnerDegrees = {2, 3, 4, 6, 10, 12};
properDivisors[value_Integer] := Select[
  Divisors[value],
  1 < # < value &
];
rawRouteEdges = Flatten[
  Table[
    {m, m e},
    {m, terminalInnerDegrees},
    {e, properDivisors[60/m]}
  ],
  1
];
sourceImpossibleEdges = Select[
  rawRouteEdges,
  !MemberQ[allowedSourceInnerDegrees, #[[2]]] &
];
admittedBeforeFieldCut = Select[
  rawRouteEdges,
  MemberQ[allowedSourceInnerDegrees, #[[2]]] &
];
fieldDeletedEdges = {{6, 30}};
admittedEdges = Sort[
  Append[
    Complement[admittedBeforeFieldCut, fieldDeletedEdges],
    {30, 6}
  ]
];

routeGraph = Lookup[certificate, "route_graph", <||>];
require[
  Sort[Lookup[routeGraph, "source_profile_impossible_targets", {}]] ===
    Sort[sourceImpossibleEdges],
  "source-profile-impossible route targets"
];
require[
  Sort[Lookup[routeGraph, "field_deleted_edges", {}]] ===
    fieldDeletedEdges,
  "field-deleted route edge"
];
require[
  Sort[Lookup[routeGraph, "admitted_edges", {}]] === admittedEdges,
  "admitted route edges"
];
directedRouteGraph = Graph[DirectedEdge @@@ admittedEdges];
require[AcyclicGraphQ[directedRouteGraph], "route DAG"];
require[
  Lookup[routeGraph, "nontrivial_strongly_connected_components", {}] === {}
    && TrueQ[Lookup[routeGraph, "route_graph_acyclic", False]],
  "certificate route DAG terminal"
];

Print[
  "status=PROVED_DEGREE60_OUTER_PRIMITIVE_ROUTE_FINITE_ARITHMETIC_REPLAY"
];
Print["partition=26_original_2_parent_deleted_24_live_18_routes_1_empty_5_survivors"];
Print["challenge_field_mod5=", Mod[q, 5]];
Print["fifth_power_gcd=", GCD[5, q - 1]];
Print["m10_r4_cover_degree=", epsilon];
Print["m10_r4_cover_bound=", e3^2];
Print["m4_A6_multisets=", Length[a6Solutions]];
Print["m4_S6_multisets=", Length[s6Solutions]];
Print["m4_S6_unique_product_sign=", uniqueProductSign];
Print["nielsen_passports=", Length[allPassports]];
Print[
  "nielsen_simultaneous_conjugacy_orbits=",
  Lookup[nielsenLedger, "simultaneous_conjugacy_orbit_count"]
];
Print["route_edges=", admittedEdges];
Print["route_dag=True"];
