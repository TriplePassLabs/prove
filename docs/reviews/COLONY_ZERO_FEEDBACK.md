# Colony Zero external feedback, candidate77c8d0e

Imported from the owner-provided public feedback on 2026-11-07 UTC. The reported candidate was `0.1.0a1`, commit `77c8d0e4cdaec67de44ec64c06a82d74854f3014`, with wheel SHA256 `b03ded47158e80800213661a91c7beb2197ca891df516ee66057697a627748cd`.

Colony Zero reported installed-CLI checks of generic offline receipt behavior. It retrospectively sealed seven public EXP-CZ-018 files totaling 6,572 bytes and reported unavailable scoring. Those observations describe frozen artifact and record integrity only. They do not establish original chronology, score computation, trace or ledger correctness, model identity, execution honesty, attempt completeness, or completed anchoring.

| Finding or request | Disposition |
| --- | --- |
| F-001: `python3 -m venv` failed on Ubuntu CPython 3.12 without `ensurepip` | Documentation corrected. The quickstart now requires the matching interpreter venv package for the standard path and provides an optional `uv` fallback when `uv` is already installed. Prove neither requires `uv` at runtime nor asks users to replace system Python or use `sudo pip`. |
| Explicit retrospective mode | Existing `manifest.metadata.evaluation_timing = "retrospective"` remains the structured, hashed self-declaration. It is non-normative and does not authenticate chronology. A dedicated CLI flag or report field remains open. |
| Narrow Colony Zero mapping example | Generic integration guidance now explains the boundary: artifacts preserve per-condition metrics, selection rules, ledger roots, and weight/model declarations unless a supported scorer recomputes them. No Colony-specific parser, adapter, imported research dependency, invented trace event, or fixture-exact mapping was added to Prove. |
| Independent live-chain gate | Still open. This feedback did not provide independently selected validated chain evidence, and no synthetic header or explorer response substitutes for it. |

The report's proxy-blocked offline control is useful test evidence, but it is not operating-system network isolation: `unshare -rn` was unavailable in the reported environment. The original report and evidence remain in the external-feedback import folder.

Main independently reproduced F-001 in a disposable Ubuntu 24.04.4 container with CPython 3.12.3: standard environment creation exited 1 while `ensurepip` was absent. Both documented routes then passed with the unchanged frozen wheel: installing `python3.12-venv` repaired the standard path, and existing `uv` 0.11.32 installed into a separate environment without system `ensurepip` or environment `pip`.

After disconnecting the container's network, both installed environments passed the generic CLI checks and all 103 conformance cases. An actual egress probe returned `ENETUNREACH`; no source checkout was mounted. A separate generic metrics example preserved opaque research declarations and reported the selected 3/4 aggregate as `recorded_only`, with identity and execution unverified. These checks resolve the setup documentation finding, not the independent live-chain gate.
