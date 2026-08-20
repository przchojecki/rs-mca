# Certificate and custody review

Verdict: **GREEN**.

- Parent commit is fixed to
  `193b7bf99a5cc7ccea042f25677e698d9f988eee`.
- Primary and independent verifiers share no imports.
- Both pass in normal and optimized Python modes.
- Primary hostile mutations: `6/6` rejected.
- Primary finite matroid configurations: `2,077`.
- Independent finite matroid configurations: `1,286`.
- Selected result, adjacent failure, and global cutoff scan are exact integers.
- Canonical result JSON is regenerated from the primary verifier.
- The manifest hashes every shipped load-bearing file and is sealed only after
  all file bytes are final.

No PDF, external binary, floating-point gate, network response, or mutable
third-party artifact is required to verify the result.
