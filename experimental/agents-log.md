# Agents Log

This file is the working ledger for agent-created material in `experimental/`.
Use it to record every new note, script, scan, formalization stub, or audit before
the material is promoted into `tex/` or `scripts/`.

The log is not a proof-status authority. It is a coordination record: what was
added, why it might matter, and what a human or later agent should check next.
Keep entries concise and link to the relevant files.

## Entry Format

```markdown
### YYYY-MM-DD - Short title

- **Agent/model:** Name the agent or model, for example `GPT-5.5 Pro`,
  `Claude Fable 5`, or `Codex`.
- **Files added or changed:** List paths under `experimental/`, `tex/`,
  or `scripts/`.
- **Status:** PROVED / CONDITIONAL / CONJECTURAL / EXPERIMENTAL / AUDIT /
  COUNTEREXAMPLE.
- **What is being added:** State the claim, note, scan, script, or certificate
  in one or two sentences.
- **How it is useful:** Say which paper, theorem, problem, ledger, or toy case
  the material supports.
- **What to do next:** Give the next verification, cleanup, proof step,
  experiment, or promotion decision.
```

## Entries

### 2026-06-18 - L2 layered Johnson certificate

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:**
  `experimental/l2_interleaved_support_bridge.md`,
  `experimental/interleaved_list_enum.py`,
  `experimental/interleaved_list_enum_certificate.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED.
- **What is being added:** Adds a support-size-layer Johnson bound for
  interleaved support profiles.  The certificate uses the exact layer counts
  `B_i(s)` and the kernel `K_{n,a}(r,s)` for `s`-subsets meeting a fixed
  `r`-set in at least `a` points.
- **How it is useful:** This improves the max-excess Johnson bound by showing
  that high-excess supports are only dangerous when their layers are numerous;
  sparse high-excess layers, including repeated codeword rows, are certified
  without paying a Cartesian interleaving exponent.
- **What to do next:** Feed layer histograms from larger L2 scans into this
  certificate and compare the layered bound with exact codegrees and quotient
  packet counts.

### 2026-06-18 - L2 near-exact Johnson certificate

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:**
  `experimental/l2_interleaved_support_bridge.md`,
  `experimental/interleaved_list_enum.py`,
  `experimental/interleaved_list_enum_certificate.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED.
- **What is being added:** Adds an explicit Johnson-neighborhood bound for L2
  support profiles whose full agreement supports all have size at most `a+c`.
  The enumerator now reports the corresponding theorem-backed certificate from
  its observed support-size histograms.
- **How it is useful:** This turns the support-profile formula into a general
  near-capacity completion bound: after one row support is fixed, every other
  row support lies in a polynomial-size neighborhood for fixed excess `c`,
  avoiding the full Cartesian product except when large support excess remains.
- **What to do next:** Use the printed excess `c` and Johnson bound in larger
  L2 certificate scans, and separate high-excess support packets from the
  near-exact regime before applying Paper C list-over-field budgets.

### 2026-06-18 - L2 quotient-core threshold spectrum

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:**
  `experimental/l2_interleaved_support_bridge.md`,
  `experimental/quotient_core_interleaving.py`,
  `experimental/quotient_core_interleaving_certificate.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED.
- **What is being added:** Computes the exact common-intersection spectrum for
  interleaved quotient-core packets at arbitrary agreement threshold `a`.  With
  slack intersection `tau`, the required common quotient intersection is
  `ceil((a-tau)/M)`, and the packet count is the corresponding
  inclusion-exclusion tail for ordered quotient subsets.
- **How it is useful:** This sharpens the L2 quotient-core obstruction from a
  single endpoint statement into a full threshold profile.  It shows exactly
  when the aligned lower-bound packet is diagonal, when it becomes Cartesian,
  and how it transitions between those extremes.
- **What to do next:** Compare this spectrum against active interleaved
  agreement-support certificates and use it to separate genuinely dangerous L2
  packets from product bounds that are only artifacts of coarse counting.

### 2026-06-17 - L2 full-agreement support profile

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:**
  `experimental/l2_interleaved_support_bridge.md`,
  `experimental/interleaved_list_enum.py`,
  `experimental/interleaved_list_enum_certificate.md`,
  `experimental/quotient_core_interleaving.py`,
  `experimental/quotient_core_interleaving_certificate.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED.
- **What is being added:** Strengthens the L2 support-fiber bridge with an
  exact full-agreement support formula: an interleaved list is counted by
  tuples of row-wise full agreement supports whose intersection has size at
  least the agreement threshold. Adds the exact raw-to-full fiber
  decomposition and updates the tiny interleaved enumerator to print raw
  base-fiber and simultaneous-fiber counts. Adds a common-intersection
  codegree certificate and has the enumerator print the corresponding
  intersection histogram and two-row max codegrees.
- **How it is useful:** Replaces raw feasible `a`-subset fibers, which can
  overcount contained supports badly, by the repaired support object that is
  in bijection with row codewords and composes exactly under column-distance
  interleaving. This gives L2 certificate emitters the right intersection
  profile to bound rather than paying the Cartesian-product exponent, and a
  precise diagnostic for how much a raw support-fiber certificate overcounts.
  The codegree form gives a compact proof target for ruling out product-size
  interleaved lists from near-exact support packets. The random-received
  baseline proves that independent random rows pay the support-selection
  entropy only once, giving a benchmark for what a worst-case L2 certificate
  should recover after structured packets are separated. The quotient-core
  packet calculation shows that the standard aligned quotient lower-bound
  source is diagonal under column interleaving: its L2 packet count is `L`, not
  `L^mu`. The threshold-spectrum refinement computes exactly how this packet
  grows below `k+sigma` from the diagonal count toward the Cartesian count via
  a common quotient-intersection tail. The extension-coordinate support formula
  turns the manuscript's extension-list identity into the same
  common-intersection support certificate after choosing a base-field basis.
- **What to do next:** Have interleaved certificate tooling print row full
  agreement-support histograms, the common-intersection tuple count, and the
  random baseline next to the conservative product bound. Feed active quotient
  rows into the quotient-core interleaving calculator to display the aligned
  packet count separately from the Cartesian packet size. For extension-code
  list ledgers, print the chosen base-field basis and coordinate support
  profile before applying the L2 certificate.

### 2026-06-17 - Open PR triage integration

- **Agent/model:** Codex.
- **Files added or changed:** Integrated experimental material from PRs #1,
  #2, #3, and #46 through #66; added
  `experimental/pr-triage-2026-06-17.md`; renamed PR #55's dither scanner to
  `experimental/quotient_profile_dither.py` with matching `.md` note.
- **Status:** AUDIT / EXPERIMENTAL.
- **What is being added:** One-by-one triage of the open PR queue and local
  integration of accepted experimental notes, scanners, certificates, and
  audit bundles.
- **How it is useful:** Preserves useful agent contributions while enforcing
  the repository rule that new material starts in `experimental/` and Papers
  A-D remain unchanged.
- **What to do next:** Run verifiers and audits on the integrated material,
  review mathematical notes before promotion, and close the original PRs as
  manually integrated once the integration commit is pushed.
