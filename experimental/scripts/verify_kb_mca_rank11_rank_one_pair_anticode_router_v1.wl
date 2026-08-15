(* Independent exact-integer replay. *)
n = 2097152;
k = 1048576;
m = 1116048;
budget = 274980728111395087;

affineRay[u_Integer] := Module[{nu, mu, q, large},
  nu = n - u;
  mu = m - u;
  q = Min[k - 1, mu - 1];
  large = If[mu > k - 1, Quotient[nu, k], 0];
  large (n - m + 1) +
   Quotient[nu (nu - 1), 2 q (mu - q)]
  ];

bestValue = -1;
bestCore = -1;
Do[
 value = affineRay[u];
 If[value > bestValue || (value == bestValue && u > bestCore),
  bestValue = value;
  bestCore = u
  ],
 {u, 0, k - 1}
 ];

proper = Table[
   Floor[Binomial[n, r + 1]/Binomial[m, r + 1]],
   {r, 0, 10}
   ];

If[
 {bestValue, bestCore} =!= {8147918, 1048575} ||
 affineRay[0] =!= 1962241 ||
 affineRay[67472] =!= 2945484 ||
 affineRay[67473] =!= 1964379 ||
 proper =!= {1, 3, 6, 12, 23, 44, 82, 155, 292, 548, 1031} ||
 budget - bestValue =!= 274980728103247169 ||
 budget - Last[proper] =!= 274980728111394056,
 Print["KB_MCA_RANK11_RANK_ONE_ROUTER_WOLFRAM_FAIL"];
 Exit[1]
 ];

Print[
 "KB_MCA_RANK11_RANK_ONE_ROUTER_WOLFRAM_PASS ",
 "affine_ray=", bestValue, " core=", bestCore,
 " proper_r10=", Last[proper]
 ];
