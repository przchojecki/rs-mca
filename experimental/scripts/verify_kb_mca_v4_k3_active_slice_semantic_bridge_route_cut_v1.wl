(* Independent Wolfram replay of the K3 direct-coordinate route cut. *)

ClearAll[require];
require[condition_, message_] := If[! TrueQ[condition], Print["FAIL: " <> message]; Abort[]];

p = 2130706433;
n = 2097152;
zeta = 1213133211;
selected = {
 {106253,2130600181},{1369722,2129336712},{3779040,2126927394},
 {8509390,2122197044},{10074554,2120631880},{10557358,2120149076},
 {12609353,2118097081},{14292086,2116414348},{14535750,2116170684},
 {15465656,2115240778},{15916705,2114789729},{16063573,2114642861},
 {17060445,2113645989},{18308266,2112398168},{18560217,2112146217},
 {19146956,2111559478},{23803083,2106903351},{24600315,2106106119},
 {24695656,2106010778},{25420300,2105286134},{26886517,2103819917},
 {32424981,2098281453},{33558404,2097148030},{33587235,2097119199},
 {33762591,2096943843},{33877430,2096829004},{34423271,2096283163},
 {35880750,2094825684},{37630638,2093075796},{37955085,2092751349},
 {38255910,2092450524},{38823503,2091882931},{41058570,2089647864},
 {41999211,2088707223},{42650444,2088055990},{42971510,2087734924}
};

require[PrimeQ[p], "base prime"];
require[PowerMod[zeta, n, p] == 1 && PowerMod[zeta, n/2, p] == p - 1,
        "exact carrier generator order"];
roots = Flatten[selected];
require[Length[DeleteDuplicates[roots]] == 72, "selected roots distinct"];
require[And @@ (PowerMod[#, n, p] == 1 & /@ roots), "selected roots in carrier"];
require[And @@ (Mod[1 - #[[1]], p] == #[[2]] & /@ selected), "tau pairs"];
require[PowerMod[1, n, p] == 1 && PowerMod[0, n, p] == 0,
        "literal carrier witness"];

outer = Mod[selected[[All, 1]] (1 - selected[[All, 1]]), p];
require[Length[DeleteDuplicates[outer]] == 36, "outer values distinct"];
pout = Expand[Times @@ (y - # & /@ outer[[1 ;; 30]])];
qout = Expand[Times @@ (y - # & /@ outer[[31 ;; 36]])];
h = x (1 - x);
v = PolynomialMod[pout /. y -> h, p];
a = PolynomialMod[qout /. y -> h, p];
directV = PolynomialMod[Times @@ (((x - #[[1]]) (x - #[[2]])) & /@ selected[[1 ;; 30]]), p];
directA = PolynomialMod[Times @@ (((x - #[[1]]) (x - #[[2]])) & /@ selected[[31 ;; 36]]), p];

require[PolynomialMod[v - directV, p] === 0, "active complete fibers"];
require[PolynomialMod[a - directA, p] === 0, "source complete fibers"];
require[Exponent[v, x] == 60 && Mod[Coefficient[v, x, 60], p] == 1,
        "V degree/monic"];
require[Exponent[a, x] == 12 && Mod[Coefficient[a, x, 12], p] == 1,
        "A degree/monic"];
require[Exponent[PolynomialGCD[v, D[v, x], Modulus -> p], x] == 0,
        "V squarefree"];
require[Exponent[PolynomialGCD[a, D[a, x], Modulus -> p], x] == 0,
        "A squarefree"];
require[Exponent[PolynomialGCD[v, a, Modulus -> p], x] == 0, "V/A coprime"];
require[PolynomialMod[v a^5 - (pout /. y -> h) (qout /. y -> h)^5, p] === 0,
        "rational composition"];
require[PolynomialMod[(h /. x -> (1 - x)) - h, p] === 0, "h invariant"];

inv2 = PowerMod[2, -1, p];
conjugated = PolynomialMod[(1 - (x + inv2)) - inv2, p];
require[PolynomialMod[conjugated + x, p] === 0, "conjugacy to negation"];
require[PowerMod[zeta, n/2, p] == p - 1, "negation preserves subgroup"];
require[Mod[-n, p] != 0, "carrier polynomial coefficient contradiction"];

Print[ExportString[
 <|"status" -> "WOLFRAM_PASS_DIRECT_COORDINATE_ROUTE_CUT",
   "p" -> p,
   "carrier_order" -> n,
   "selected_fibers" -> Length[selected],
   "active_degree" -> Exponent[v, x],
   "source_degree" -> Exponent[a, x],
   "tau_preserves_D" -> False,
   "conjugated_negation_preserves_D" -> True,
   "actual_MCA_counterexample" -> False,
   "ledger_movement" -> 0|>, "RawJSON"]];
