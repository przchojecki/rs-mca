(* Independent Wolfram exact-integer replay of the common-core staircase. *)

n = 2097152; k = 1048576; m = 1116048;
d = m - k; r = n - k; b = 274980728111395087;

rfloor[c_] := Ceiling[32 (m - c)/(n - c)];
j[s_] := Floor[Product[(r + i)/(d + i), {i, 0, s}]];
cell[s_] := Min[Binomial[r + s, d + s], Binomial[r + s, s + 1]];

c = 4131;
num = Binomial[n, c]; den = Binomial[m, c]; jo = Ceiling[num/den];

tests = {
  d == 67472,
  r == 1048576,
  n - m == 981104,
  32 d - 2 r == 61952,
  rfloor[4130] == 18,
  rfloor[4131] == 17,
  rfloor[k - 1] == 3,
  cell[1] == 549756338176,
  cell[2] == 192154133857304576,
  cell[3] == 50372197381489643749376,
  j[13] == 47876303026096432,
  j[14] == 743896698428332665,
  b - j[13] == 227104425085298655,
  b - j[14] == -468915970316937578,
  num > b den,
  IntegerLength[jo, 2] == 3765,
  IntegerLength[jo, 10] == 1134
};

If[And @@ tests,
  Print[<|
    "status" -> "PASS",
    "checks" -> Length[tests],
    "J13" -> j[13],
    "J14" -> j[14],
    "JoBits" -> IntegerLength[jo, 2],
    "LedgerMovement" -> 0
  |>],
  Print[<|"status" -> "FAIL", "tests" -> tests|>]; Exit[1]
];
