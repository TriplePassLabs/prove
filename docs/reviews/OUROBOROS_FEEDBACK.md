# Ouroboros external feedback, candidate77c8d0e

Imported from the owner-provided Drive feedback on2026-11-07 UTC. The tested runtime was0.1.0a1, commit `77c8d0e4cdaec67de44ec64c06a82d74854f3014`, wheel SHA256 `b03ded47158e80800213661a91c7beb2197ca891df516ee66057697a627748cd`.

Ouroboros reported fresh installed-CLI success on CPython3.12.3 and3.13.14. Eight of nine feedback checks passed; live anchoring was explicitly not run. Six public producer files totaling20942 bytes were retrospectively sealed with unchanged source/copy hashes. These observations establish the external generic workflow, not original chronology, score computation, private-ledger completeness, model identity or honest execution.

| Finding | Disposition | Evidence and correction |
| --- | --- | --- |
| FT-001: protocol missing from outer review ZIP | Confirmed packaging defect; corrected packet revision2 | Main reproduced the omission. The source archive already contained the protocol, but the independently usable outer packet did not. Packet assembly now includes `docs/PROTOCOL.md`; verification requires the named document and checks its declared hash. The original packet is preserved with its original checksum. |
| FR-001: explicit retrospective mode | Dedicated CLI/report mode remains an open usability request | Main verified that existing `manifest.metadata.evaluation_timing = "retrospective"` is accepted and frozen. The integration guide now documents that self-declaration. It is non-normative metadata and does not authenticate chronology. No new CLI flag, report field or wire-schema meaning is introduced by this correction. |
| FT-003: original outputs are not checked in place | Intended snapshot behavior; documentation clarified | Main reproduced exit0 after changing the original output and exit2 after changing the receipt's copied artifact. Full verification checks the frozen receipt copy. An external-directory comparison command is not part of v1. |
| FT-004: staging retained after successful seal | Intended durable producer state; documentation clarified | Main reproduced three retained stage files and verified an unchanged portable receipt after omitting only root `.prove` from a sharing copy. The guide now explains recovery, possible duplicate disk usage, and portable contents. No automatic cleanup or producer-state deletion was added. |

The correction also fixes a stale CLI spelling in the protocol prose: preregistration uses `--receipt`, as implemented and shown in the quickstart. Receipt formats and algorithms are unchanged.

The external feedback JSON validates against the shipped feedback schema. Main's bounded-worker recheck exercised the unchanged runtime and reproduced the packet omission, structured metadata acceptance, source-versus-snapshot distinction, retained stage files and private-state-free sharing. The new packet documentation check fails against the original ZIP before the packaging fix.

No Ouroboros-specific behavior, model dependency or research-project import was added to Prove. Original reports and evidence remain preserved in the external-test folder. Revised delivery identifies its documentation commit separately from runtime77c8d0e and keeps both original distribution hashes. Independently sourced real chain evidence and the fresh locally gated launch test remain open. Other downstream feedback remains pending.
