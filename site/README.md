# RS-MCA Frontier Site

Static site for the public RS-MCA frontier board.

## Vercel

Create a Vercel project from this repository and set:

```text
Root Directory: site
Framework Preset: Other
Build Command: empty / none
Output Directory: .
```

The deployed entry point is `index.html`.

## Data Files

- `data/frontier.json`: chart and leaderboard entries.
- `data/updates.json`: browsable result ledger entries for proof notes,
  audits, counterexamples, bridge results, and targets.
- `data/rate-leaderboards.json`: the four official-rate MCA/list boards,
  including row status and missing-piece metadata.
- `data/papers.json`: Paper A/B/D/C links, including GitHub PDF and TeX
  source URLs.

## Embedded Board Fallbacks

`index.html` embeds `frontier.json`, `updates.json`, and
`rate-leaderboards.json` so the board still works when JSON fetches fail or
the page is opened directly from disk.  The files under `data/` are
authoritative.  After changing any of those three files, refresh the embedded
copies and run the fail-closed semantic drift check from the repository root:

```sh
python3 site/sync_fallback_data.py --write
python3 site/sync_fallback_data.py
python3 site/sync_fallback_data.py --self-test
```

The checker ignores formatting and object-key order, while preserving
user-visible array order.

The four PDF files are copied into `papers/` because Vercel only serves files
inside the configured root directory.
