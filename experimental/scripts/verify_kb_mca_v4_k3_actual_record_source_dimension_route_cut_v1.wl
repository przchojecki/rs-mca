(* Independent Wolfram replay of the actual-record dimension-sensitivity audit. *)

ClearAll[require];
require[condition_, message_] :=
  If[! TrueQ[condition], Print["FAIL: " <> message]; Abort[]];

p = 2130706433;
n = 2097152;
k = 1048576;
m = 1116048;
e = 67473;
zeta = 1213133211;
q = p^6;
bStar = Floor[q/2^128];

require[PrimeQ[p], "base prime"];
require[PowerMod[3, (p - 1)/2, p] != 1 &&
        PowerMod[3, (p - 1)/127, p] != 1, "primitive power base"];
require[PowerMod[zeta, n, p] == 1, "zeta^n"];
require[PowerMod[zeta, n/2, p] == p - 1, "exact carrier order"];
require[e + m == 1183521 < n, "support intervals disjoint"];
require[IrreduciblePolynomialQ[x^6 + x + 6, Modulus -> p],
        "degree-six challenge modulus"];

offE = n - e;
actualMaxN = k + e - 2;
effectiveMaxN = k + e - 1;
require[{offE, actualMaxN, effectiveMaxN} ==
        {2029679, 1116047, 1116048}, "root-count values"];
require[offE > effectiveMaxN, "root-count minimum under both shifts"];
require[e == (m - k) + 1, "code-dimension Q boundary"];
require[e == (m - (k + 1)) + 2, "effective first BC interior"];

codeProfile = {e, n - k + 1 - e, k - 1 + e, n - m - (n - k + 1 - e)};
effectiveProfile =
  {e, n - (k + 1) + 1 - e, (k + 1) - 1 + e,
   n - m - (n - (k + 1) + 1 - e)};
require[codeProfile == {67473, 981104, 1116048, 0}, "code profile"];
require[effectiveProfile == {67473, 981103, 1116049, 1},
        "effective profile"];

supports = Binomial[n - e, m];
supportBytes = IntegerDigits[supports, 256];
supportHash = IntegerString[Hash[ByteArray[supportBytes], "SHA256"], 16, 64];
require[IntegerLength[supports, 2] == 2015083, "support bit length"];
require[Length[supportBytes] == 251886, "support byte length"];
require[supportHash ==
        "4d11045a6ab54a207e0c6ed148104a40f426f2ab4e5ef5e65453f1eca4710678",
        "support SHA-256"];
require[Mod[supports, p] == 864013898, "support residue p"];
require[Mod[supports, 1000000007] == 180951258, "support residue 1e9+7"];
require[Mod[supports, 4294967291] == 633477545, "support residue 2^32-5"];

require[bStar == 274980728111395087, "frozen B_star"];
require[bStar - (n - m) == 274980728110413983, "joint reserve"];

Print[ExportString[
 <|"status" -> "WOLFRAM_PASS_ACTUAL_RECORD_DIMENSION_SENSITIVITY_AUDIT",
   "p" -> p,
   "carrier_order" -> n,
   "extension_modulus_irreducible" -> True,
   "code_profile" -> "BOUNDARY_NUMERICAL_PROFILE",
   "effective_profile" -> "FIRST_INTERIOR_NUMERICAL_PROFILE",
   "actual_owner" -> "NOT_ESTABLISHED_BY_PINNED_SOURCES",
   "support_fingerprint_sha256" -> supportHash,
   "B_star" -> bStar,
   "pure_ray_scope" -> True,
   "ledger_movement" -> 0|>, "RawJSON"]];
