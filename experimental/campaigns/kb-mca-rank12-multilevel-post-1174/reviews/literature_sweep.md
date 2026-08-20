# External literature and public-code sweep

Date: 2026-08-20

## Search coverage

The external lane screened 376 candidates across more than eight distinct
query families spanning Reed--Solomon MCA, list recovery, higher-order MDS,
support-constrained parity checks, finite-field incidence geometry, and
public Proximity Prize work.  The coordinator independently ran five Exa
queries with ten returned hits each and fetched the primary sources below.
Search hits were treated as discovery only; statements recorded here were
checked against the linked paper or exact Git commit.

## Strongest importable public chain

The most relevant outside work is the `SYZ21`--`SYZ25` chain at exact
`SlopDotCash/proximityprize` commit
[`acfa4f072d0c7fe8e706c80d8e21cb5b083f73a6`](https://github.com/SlopDotCash/proximityprize/tree/acfa4f072d0c7fe8e706c80d8e21cb5b083f73a6):

- [SYZ21 shortening dimension](https://github.com/SlopDotCash/proximityprize/blob/acfa4f072d0c7fe8e706c80d8e21cb5b083f73a6/docs/kb/deltastar-466-syz21-shortening-coverage-2026-07-11.md)
  proves that the dual annihilator supported on (U) has dimension
  \(\max(0,|U|-k)\).
- [SYZ22 syndrome-pair bridge](https://github.com/SlopDotCash/proximityprize/blob/acfa4f072d0c7fe8e706c80d8e21cb5b083f73a6/docs/kb/deltastar-466-syz22-strip-bridge-2026-07-11.md)
  identifies the witness-function source with that shortening space and
  proves the doubled dimension (2(|U|-k)), while leaving realizability
  explicit.
- [SYZ24 cross-core compatibility](https://github.com/SlopDotCash/proximityprize/blob/acfa4f072d0c7fe8e706c80d8e21cb5b083f73a6/docs/kb/deltastar-466-syz24-cross-core-compat-2026-07-11.md)
  reduces the missing lower-rank statement to generation of the union
  shortened dual by the core-supported shortened duals.
- [SYZ25 exact generation criterion](https://github.com/SlopDotCash/proximityprize/blob/acfa4f072d0c7fe8e706c80d8e21cb5b083f73a6/docs/kb/deltastar-466-syz25-mds-generation-2026-07-11.md)
  proves that generation is equivalent to local-to-global gluing of
  degree-(<k) polynomials on the cores.  It also gives the mandatory
  negative control

  \[
  n=6,\quad k=3,\quad
  C_1=\{0,1,4,5\},
  C_2=\{0,2,3,5\},
  C_3=\{1,2,3,4\},
  \]

  for which the total nominal excess is \(3=|U|-k\), but the joint span has
  rank two.  Thus over-budget core counting does not imply generation.
- [SYZ42 realizability audit](https://github.com/SlopDotCash/proximityprize/blob/acfa4f072d0c7fe8e706c80d8e21cb5b083f73a6/docs/kb/deltastar-466-syz42-realizability-2026-07-11.md)
  distinguishes rigidity/generation from existence of the actual syndrome
  configuration; neither quantifier can silently replace the other.

This chain is not a rank-twelve payment.  It supplies the correct linear
algebra object, exact negative controls, and the most promising classifier
interface.

## Primary literature

- Brakensiek--Dhar--Gopi,
  [Generalized GM-MDS: Polynomial Codes are Higher Order MDS](https://arxiv.org/html/2310.12888v3),
  gives the appropriate higher-order MDS/intersection language for generic
  polynomial codes.
- Brakensiek--Dhar--Gopi,
  [Improved Field Size Bounds for Higher Order MDS Codes](https://arxiv.org/html/2212.11262),
  proves an exponential-scale lower bound already for unrestricted
  MDS(3).  Therefore the fixed KoalaBear field cannot support the naive
  theorem that every abstract core family is in generic higher-order-MDS
  position.
- Han--Yildiz--Hassibi,
  [On Codes with Support-Constrained Parity Checks](https://arxiv.org/html/2605.08644),
  supplies further exact support-mask obstructions to generalized
  Reed--Solomon realizability.
- Tamo,
  [Points-Polynomials Incidence Theorem with Applications to Coding Theory](https://arxiv.org/html/2312.12962),
  provides a spectral incidence method, but its dominant Johnson-scale term
  is too large in the deployed post-Johnson row.
- Jo,
  [Reed--Solomon Mutual Correlated Agreement Beyond the Johnson Radius](https://eprint.iacr.org/2026/1432),
  proves polynomial bad-parameter bounds for a fixed number of integer steps
  beyond Johnson.  The deployed KoalaBear gap is not in that fixed-step
  regime.
- Chojecki,
  [Conjectures and Barriers for RS-MCA](https://eprint.iacr.org/2026/1479),
  confirms that primitive-fiber, residual-projection, algebraic-routing, and
  add-back payments remain open in the unrestricted smooth problem.

## Research conclusion

The maximal nonduplicate attack is not another scalar cutoff and not an
unrestricted MDS(3) assertion.  It is an actual-received-line,
source-restricted higher-order circuit compiler:

1. attach to every minimizing pair core its supported dual annihilator;
2. classify every failure of their joint span through the exact
   local-to-global polynomial-gluing obstruction;
3. preserve the same line, slope, support, explanation, and owner;
4. route every source-realizable circuit to shortening, a proved earlier
   owner, a budget-fitting collision family, or `UNPAID_PRIMITIVE`;
5. keep the (n=6,k=3) coplanar triple as a mandatory hostile regression.

The theorem must exploit the actual received-line equations.  The external
field-size and support-mask results rule out replacing that work by an
abstract all-core generation claim.
