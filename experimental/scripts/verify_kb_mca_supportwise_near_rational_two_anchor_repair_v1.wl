(* Independent Wolfram replay for the support-wise two-anchor repair. *)

n = 2^21;
K = 2^20;
m = 1116048;
w = m - K;
dmin = n - K + 1;
Bstar = 274980728111395087;

checks = {
  w == 67472,
  2 w == 134944,
  3 w == 202416,
  3 w < dmin,
  dmin - 3 w == 846161,
  n - w == 2029680,
  n - w >= m,
  m - 1 >= K,
  Bstar - 2 w == 274980728111260143,
  Expand[(eu + z ev) - eta] == eu + z ev - eta,
  Simplify[(eta1 - eta0)/(z1 - z0) == ev,
    Assumptions -> z1 != z0 && ev == (eta1 - eta0)/(z1 - z0)]
};

m31 = 1116024;
w31 = m31 - K;
B31 = 16777215;
checks = Join[checks, {
  w31 == 67448,
  2 w31 == 134896,
  3 w31 < dmin,
  B31 - 2 w31 == 16642319
}];

If[And @@ checks,
  Print["Wolfram support-wise two-anchor replay"];
  Print["  KoalaBear charge: ", 2 w];
  Print["  M31 charge: ", 2 w31];
  Print["RESULT: PASS"],
  Print["RESULT: FAIL"];
  Exit[1]
]
