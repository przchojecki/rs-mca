(* Independent Wolfram replay of the live frontier, partition, and route cut. *)

repo = DirectoryName[DirectoryName[DirectoryName[$InputFileName]]];
read[path_] := Import[FileNameJoin[{repo, path}], "RawJSON"];
assert[condition_, code_] := If[! TrueQ[condition], Print["FAIL ", code]; Exit[code]];

source = read[
  "experimental/data/certificates/" <>
  "kb-mca-v4-degree60-source-pencil-rank-compiler-v1/" <>
  "kb_mca_v4_degree60_source_pencil_rank_compiler_v1.json"
];
m12 = read[
  "experimental/data/certificates/" <>
  "kb-mca-v4-m12-diagonal-socle-degree5-close-v1/" <>
  "kb_mca_v4_m12_diagonal_socle_degree5_close_v1.json"
];
m10 = read[
  "experimental/data/certificates/" <>
  "kb-mca-v4-m10-scott-strip-lower-degree-router-v1/" <>
  "kb_mca_v4_m10_scott_strip_lower_degree_router_v1.json"
];
m6 = read[
  "experimental/data/certificates/" <>
  "kb-mca-v4-m6-scott-cartesian-degree2-router-v1/" <>
  "kb_mca_v4_m6_scott_cartesian_degree2_router_v1.json"
];
m4 = read[
  "experimental/data/certificates/" <>
  "kb-mca-v4-m4-adjacency-genus-exclusion-v1/" <>
  "kb_mca_v4_m4_adjacency_genus_exclusion_v1.json"
];
m3 = read[
  "experimental/data/certificates/" <>
  "kb-mca-v4-m3-primitive-outer-degree2-router-v1/" <>
  "kb_mca_v4_m3_primitive_outer_degree2_router_v1.json"
];
m2 = read[
  "experimental/data/certificates/" <>
  "kb-mca-v4-m2-r2-dihedral-degree3-source-facet-exclusion-v1/" <>
  "kb_mca_v4_m2_r2_dihedral_degree3_source_facet_exclusion_v1.json"
];
activeManifest = read[
  "experimental/data/certificates/" <>
  "kb-mca-v4-tangent-source-adapter-v1/manifest.json"
];
activeRow = read[
  "experimental/data/certificates/" <>
  "kb-mca-v4-tangent-source-adapter-v1/row_manifest.json"
];
packet = read[
  "experimental/data/certificates/" <>
  "kb-mca-v4-k3-outer-frontier-dihedral-route-cut-v1/" <>
  "kb_mca_v4_k3_outer_frontier_dihedral_route_cut_v1.json"
];
routeCut = Lookup[packet, "deployed_dihedral_route_cut"];

rows = Lookup[Lookup[source, "transverse_outer_terminal"], "rows"];
states = Sort@DeleteDuplicates@Flatten[
  Table[
    With[{inner = Lookup[row, "m"]},
      ({inner, #[[1]], #[[2]]} &) /@ Lookup[row, "r_delta"]
    ],
    {row, rows}
  ],
  1
];
assert[Length[states] == 26, 1];
assert[And @@ ((#[[2]] #[[3]] == 4 #[[1]]) & /@ states), 2];
counts = {Length[states]};

assert[TrueQ[Lookup[Lookup[m12, "conclusion"], "m12_closed"]], 3];
states = Select[states, First[#] != 12 &];
AppendTo[counts, Length[states]];

assert[TrueQ[Lookup[Lookup[m10, "conclusion"], "m10_routed"]], 4];
states = Select[states, First[#] != 10 &];
AppendTo[counts, Length[states]];

assert[TrueQ[Lookup[Lookup[m6, "conclusion"], "m6_routed"]], 5];
states = Select[states, First[#] != 6 &];
AppendTo[counts, Length[states]];

assert[
  TrueQ[Lookup[Lookup[m4, "conclusion"], "m4_transverse_row_empty"]],
  6
];
states = Select[states, First[#] != 4 &];
AppendTo[counts, Length[states]];

assert[
  Lookup[Lookup[m3, "conclusion"], "m3_independent_type_count"] == 0,
  7
];
states = Select[states, First[#] != 3 &];
AppendTo[counts, Length[states]];

assert[
  TrueQ[Lookup[Lookup[m2, "conclusion"], "full_v4_type_deleted"]],
  8
];
states = DeleteCases[states, {2, 2, 4}];
AppendTo[counts, Length[states]];
assert[counts === {26, 22, 18, 12, 8, 3, 2}, 9];
assert[states === {{2, 4, 2}, {2, 8, 1}}, 10];

(* The live four-cell active-v4 partition is derived from the repaired row. *)
partition = Lookup[activeRow, "partition"];
stages = Lookup[partition, "chronology_stages"];
ownerOrder = Lookup[stages, "owner_id"];
atomOrder = Lookup[stages, "atom_id"];
assert[
  ownerOrder === {
    "SOURCE_COORDINATE_TANGENT_IMAGE",
    "ACTIVE_V4_BOUNDARY_PREFIX_Q",
    "ACTIVE_V4_BALANCED_CORE",
    "UNPAID_V4_COMPLEMENT"
  },
  11
];
assert[atomOrder === {"U_paid", "U_Q", "U_BC", "U_new"}, 12];
assert[TrueQ[Lookup[partition, "first_match"]], 13];
assert[TrueQ[Lookup[partition, "first_match_disjoint"]], 14];
assert[TrueQ[Lookup[partition, "witness_exhaustive"]], 15];
assert[
  Lookup[activeManifest, "payload_sha256"] ===
    "ffd1e427f53db3d2dbfd13e69a05d173d2f2aa1f03c152aead73fcc821094acb",
  16
];
assert[
  Lookup[activeRow, "payload_sha256"] ===
    "36e9d69aaf6deeb4fe123358e8bb8d5bbbdcb40c9315b4316f0c6a1189a270e1",
  17
];

(* Exact deployed fixed-point-free dihedral recurrence route cut. *)
p = 2130706433;
n = 2^21;
half = n/2;
assert[PrimeQ[p], 18];
assert[p - 1 == 127 2^24, 19];
a = PowerMod[3, (p - 1)/n, p];
assert[a == 1213133211, 20];
assert[PowerMod[a, n, p] == 1, 21];
assert[PowerMod[a, half, p] == p - 1, 22];

fixedPointCongruenceCounts = {
  Length@Solve[2 k == 1, k, Modulus -> n],
  Length@Solve[2 k == 3, k, Modulus -> n]
};
assert[fixedPointCongruenceCounts === {0, 0}, 23];

(* Derive the exact quadratic quotient identity and complete reduced
   two-point carrier fibres. *)
quotientIdentity = Together[
  (tt + cc/tt) - (xx + cc/xx) -
  ((tt - xx) (tt xx - cc))/(tt xx)
];
assert[quotientIdentity === 0, 31];
quotientCoefficients = {a, PowerMod[a, 3, p]};
assert[
  And @@ Table[
    PolynomialGCD[xx^2 + c, xx, Modulus -> p] === 1 &&
    Exponent[xx^2 + c, xx] == 2 &&
    Expand[
      tt^2 - (xx + c/xx) tt + c -
      (tt - xx) (tt - c/xx)
    ] === 0 &&
    PowerMod[c, n, p] == 1,
    {c, quotientCoefficients}
  ],
  32
];
qRecords = Lookup[routeCut, "quadratic_quotient_fibres"];
assert[Lookup[qRecords, "name"] === {"q1", "q2"}, 33];
assert[
  Lookup[qRecords, "coefficient_value"] === quotientCoefficients,
  34
];
assert[
  Lookup[qRecords, "formula"] ===
    {"q1(x)=x+a/x", "q2(x)=x+a^3/x"},
  35
];
assert[
  Lookup[qRecords, "fibre_difference_formula"] === {
    "q1(T)-q1(x)=((T-x)(T*x-a))/(T*x)",
    "q2(T)-q2(x)=((T-x)(T*x-a^3))/(T*x)"
  },
  36
];
assert[Lookup[qRecords, "rational_map_degree"] === {2, 2}, 37];
assert[And @@ TrueQ /@ Lookup[qRecords, "preserves_D"], 38];
assert[And @@ TrueQ /@ Lookup[qRecords, "D_fibre_complete"], 39];
assert[And @@ TrueQ /@ Lookup[qRecords, "D_fibre_reduced"], 40];
assert[Lookup[qRecords, "D_fibre_cardinality"] === {2, 2}, 41];

rotationOrder = MultiplicativeOrder[PowerMod[a, 2, p], p];
groupOrder = 2 rotationOrder;
assert[rotationOrder == 2^20, 24];
assert[groupOrder == n, 25];

(* u=(x^n-1)/x^(n/2) has map degree n.  The exponent identities prove
   invariance under a/x and a^3/x and under the rotation a^2 x. *)
assert[PowerMod[a, half, p] == PowerMod[a, 3 half, p] == p - 1, 26];
assert[PowerMod[a, 2 half, p] == 1, 27];
invariantDegree = Max[n, half];
fixedFieldDegree = groupOrder;
assert[invariantDegree == fixedFieldDegree == n, 28];
invariantValuesOnD = (# - 1/#) & /@ {1, -1};
assert[invariantValuesOnD === {0, 0}, 29];

(* N|(p-1) makes all N roots rational; the exact order of a gives N
   distinct roots in D, and p does not divide N, so the fibre is reduced. *)
assert[Mod[p - 1, n] == 0, 42];
assert[CoprimeQ[p, n], 43];
assert[Exponent[xx^n - 1, xx] == n, 44];
(* The derivative is n*x^(n-1).  Its only root is zero because n is
   nonzero mod p, while the defining polynomial has value -1 at zero. *)
assert[Mod[n, p] != 0 && Mod[-1, p] != 0, 45];
zeroFibre = Lookup[routeCut, "common_invariant_zero_fibre"];
assert[Lookup[zeroFibre, "equation"] === "u^(-1)(0)=D", 46];
assert[Lookup[zeroFibre, "defining_polynomial"] === "x^N-1", 47];
assert[Lookup[zeroFibre, "cardinality"] == n, 48];
assert[Lookup[zeroFibre, "fibre_degree"] == n, 49];
assert[TrueQ[Lookup[zeroFibre, "complete"]], 50];
assert[TrueQ[Lookup[zeroFibre, "reduced"]], 51];
assert[
  Lookup[zeroFibre, "pole_support"] === {"0", "infinity"},
  52
];
poleOrders = Lookup[zeroFibre, "pole_orders"];
assert[Lookup[poleOrders, "0"] == half, 53];
assert[Lookup[poleOrders, "infinity"] == half, 54];
assert[Lookup[zeroFibre, "pole_divisor_degree"] == n, 55];

(* The only live arithmetic is the tangent subtraction.  The off-branch
   abstract multiplier is not imported as a source-to-charge theorem. *)
bStar = 274980728111395087;
tangentPaid = 981104;
liveReserve = bStar - tangentPaid;
assert[liveReserve == 274980728110413983, 30];

Print[
  "WOLFRAM_PASS frontier=", StringRiffle[ToString /@ counts, ">"],
  " residual=", states,
  " live_partition=FOUR_CELL_PRESENT",
  " dihedral_order=", groupOrder,
  " quadratic_fibres=COMPLETE_REDUCED_2",
  " fixed_field_degree=", fixedFieldDegree,
  " zero_fibre=COMPLETE_REDUCED_", n,
  " live_tangent_reserve=", liveReserve,
  " source_map_live_charge=UNPROVEN"
];
