# Prove implementation review evidence

This log records scoped implementation acceptance. It does not establish whole-candidate or production readiness; see [the live readiness audit](../READINESS.md).

## Canonical JSON and Merkle primitives

Accepted commit:10344f3. Source: src/prove/canonical.py, errors.py, merkle.py. Evidence: tests/test_canonical.py and tests/test_merkle.py.

The first implementation was not accepted on its initial green suite. Main review and expanded fixed vectors exposed empty-tree rejection, incorrect largest-power-of-two splitting for odd tree sizes and an unnormalized deep-parser RecursionError. Regression-first fixes corrected these. The independent reviewer then demonstrated otherwise-valid uppercase/whitespace hash encodings being accepted by bytes.fromhex. New tests modified valid proof/root strings, and strict lowercase encodings were enforced.

The main session read the actual final source and reran the scoped tests in an isolated capped worker:33 passed. The independent reviewer rechecked the corrections and returned APPROVED. This acceptance covers primitives and their declared bounds, not receipt persistence, real anchoring or installation.

## Versioned contracts and direct bindings

Accepted commit:0771498. Source: src/prove/schema.py and data/schemas/protocol-v1.json. Evidence: tests/test_schema.py and tests/fixtures/contracts/.

The worker first wrote meaningful failing contract tests. Additional RED cycles exposed regex end-anchor behavior accepting final newlines, a missing closed root in the packaged schema and an incorrectly nullable trace call count. The corrections use portable ECMA-compatible patterns and a closed local-reference schema.

Independent review demonstrated a valid Merkle path for an attempt_end event positioned before the end of its declared tree. The schema had accepted that visible contradiction; it now requires the final position. Review also caught malformed embedded format types being classified as unsupported instead of malformed; nested validation now applies the intended precedence.

Main review added direct checks implied by the generic contract: generated artifact count and UTF8 inventory rank, fixture aggregate count bounds and a non-null digest for declared weight-digest evidence. Regression inputs include actual valid Merkle proofs so rejection is attributable to the contract contradiction rather than a broken hash.

Final main-session cumulative rerun:237 tests passed in0.31s on Python3.12 in the capped worker (204 contracts,33 primitives). Independent scoped re-review returned APPROVED. These validators deliberately do not authenticate cache/model/issuer claims, read artifacts, verify whole-trace history, recompute arbitrary scores or validate Bitcoin header hashes; later consumers must supply those checks.

## Descriptor-safe filesystem and writer locks

Source: src/prove/filesystem.py. Evidence: tests/test_filesystem.py and independently owned tests/test_filesystem_adversarial.py. Main-session cumulative rerun:343 passed in1.81s in the capped Python3.12 worker, including106 filesystem cases. Scoped independent re-review returned APPROVED after direct fault-injection probes.

The first green implementation was rejected. Root-ancestor replacements could evade reads and destination publication; lock acquisition repeated that mistake at .prove. The corrected implementation retains directory identities and checks reachability from the opened receipt root. Enumeration now applies path and prefix-collision rules. File and ancestor-publication fsync failures cannot report success. Lock acquisition is nonblocking, recovery binds the complete bounded file through EOF, and live-writer/empty-lock races have process-level regressions.

Repeated review exposed a systemic descriptor-ownership defect: close-after-release EIO could trigger a second close, mask the original failure and leak a sibling descriptor. A fresh implementer replaced scattered cleanup with one ownership mechanism that relinquishes descriptors before closing, drains all remaining cleanup and preserves primary exceptions. Meaningful RED cases preceded the fix. Direct reviewer probes for rewalk, enumeration, failed opening, stream and acquisition failures returned operational code5 with zero descriptor leaks and zero repeated closes. Minimal context reentry guards preserve existing ownership.

This covers the declared opened-root boundary and detectable replacements before its checks. It is not a sandbox against an actor with unrestricted same-user filesystem control after the last check, nor a hardware power-loss proof. Application-level receipt staging, interrupted-finalization recovery and durability repair for hash-identical reuse are later persistence requirements.

## Receipt persistence and later consumers

Receipt persistence acceptance is recorded below. Full verification, timestamp transport/evidence, installed CLI and handoff are still incomplete. Later review entries must record actual source/commit boundaries, reproduced findings, regression tests, main-session verification and remaining limits. Reviewer approval alone never establishes whole-candidate readiness.

## Pure normalized-record engine

Source: src/prove/records.py and the prepared event/inventory additions in schema.py. Evidence: tests/test_records.py, schema regressions and independently owned tests/test_records_adversarial.py. Main-session final cumulative run:391 passed in2.46s in the capped worker. Scoped independent review returned APPROVE after direct semantic probes.

Main rejected the initial minimal test set. Expanded tests cover honestly rehashed contradictory records, lifecycle/retry/reference errors, terminal and coverage rules, exact resources, overflow, usage unknowns and canonical JSONL limits. Main source review also exposed repeated manifest hashing during artifact generation; it is now computed once. Invalid attempt argument types produce structured errors, the one-shot validator keeps its prior error precedence, and stored-record verification reuses computed metadata rather than repeating the tree calculation.

Independent acceptance cases bind real canonical hashes and trees while contradicting a budget outcome: known token use above a ceiling must still reject completed when another call reports null usage. Explicit budget_exceeded retains a null full total and its known lower bound; below/equal-ceiling subtotals with unknown constrained usage remain unknown. Known call-count violations remain detectable with unknown token totals. Exact1MiB event and64MiB JSONL positive boundaries pass, with over-limit input rejected. Distinguishable code2/code4 cases exercise one-shot validation precedence.

This is pure supplied-record consistency. It does not authenticate execution/model identity, establish real-world call completeness, read artifacts, recompute scores, persist receipts, contact calendars or make an installed CLI available.

## Durable generic receipt snapshots

Source: store.py, paths.py and focused filesystem/schema additions. Evidence: tests/test_store.py, original filesystem/schema regressions and independently owned tests/test_store_adversarial.py. Main final cumulative run:475 passed,1 prerequisite skip in34.79s; the skipped bind-alias case separately passed in a disposable capped worker with the real second bind mount. Scoped independent re-review returned APPROVE. No privileged worker, host-mount or live-service changes were needed.

The reviewed persistence design was corrected before code: existing final-result conflicts must be checked before adding any candidate artifact; a journal binds one pending candidate; identical bytes must have their file/ancestor durability repaired after failed fsync; trusted storage prefixes must preserve the full1024-byte wire path allowance; and complete recorded-only traces can have no artifacts. Implementation tests cover these requirements plus immutable repeat/conflict behavior and selected attempts.

Main actual-source review and implementation fault injection exposed foreign recognized root adoption on first registration, skipped manifest-file persistence, a synthetic8MiB options wrapper rejecting valid larger traces, stale shared-description directory enumeration, empty-directory namespace conflicts and selected-prefix identity loss. Test-first corrections preserve original bytes, safe descriptors and the separate wire/storage limits.

Independent review then reproduced false success when a missing descendant caused an entire artifact listing to be treated as empty, a bind-mounted-descendant overlap gap and a raw recursion error on a deep internal tree. Separate main regressions failed on all three, including the actual bind mount. Absence is now optional only at the exact requested initial open; later failures propagate. Iterative enumeration preserves ownership/namespace checks, and bidirectional descendant inode scans supplement upward ancestry with cycle bounds.

An actual child process exits immediately after journal publication. Recovery is blocked by the stale writer lock until explicit observed-digest lock recovery, then completes the bound snapshot with the live source removed. Stages/journals remain local and retained; no automatic cleanup or claim of protection from unrestricted same-user tampering after final checks is introduced. This acceptance establishes local snapshot persistence, not Bitcoin anchoring, score correctness or a released CLI.

## Optional no-model fixture and deterministic scoring

Source: fixture.py, scoring.py and the closed fixture-payload schema/validator additions. Evidence: tests/test_fixture.py, tests/test_scoring.py and focused schema cases. Final main cumulative run:503 passed,1 bind-prerequisite skip in33.40s. Independent scoped review returned APPROVE after direct wrong-math, version/type, correct1/2, defensive-copy and unavailable/no-read probes. The bind case was exercised separately during persistence acceptance.

Main rejected the initial tests because an allegedly honest-rehash wrong-score case retained a stale byte count and therefore failed before testing the math. The corrected cases update every digest and byte-length binding, validate cores/records and then demonstrate false recomputation rejection, including through actual store sealing. Additional cases cover exact Unicode equality, complete unique sample membership, shuffled arrays, both aggregates, closed payload types/fields/versions and the8MiB raw payload limit.

The first implementation also imposed an unsupported exactly-one pinned-dataset-copy rule and classified future payload formats as malformed. It now deterministically selects the UTF8-first matching pinned entry and preserves unsupported4 versus malformed2. Declared aggregates are returned as defensive copies, and JSON errors use the existing typed boundary.

The fresh in-memory fixture uses two declared samples, one exact match and zero model-call events. Generic ingestion does not depend on it. Null scores are unavailable without reads; arbitrary recorded-only score bytes are not parsed or recomputed. Recomputed fixture agreement authenticates neither labels/observations nor execution/output provenance. Full verification/reference conformance, anchors, distribution and CLI remain outstanding.

## Offline OTS parser and explicitly trusted cached headers

Source: anchors.py and chain.py. Evidence: tests/test_anchors.py, tests/test_chain.py and attributed upstream historical header bytes under tests/fixtures/ots/. Main read both modules and final cumulative run returned579 passed,1 prerequisite skip and3 upstream OpReverse pending-deprecation warnings in32.55s. Independent scoped proof/cache review returned APPROVE after direct framing, substitution, extra-invalid-witness, unused-cache-header and mutation probes.

The parser uses standard pinned upstream operations and attestation deserializers. The initial structural preflight enforced16MiB/depth64/work100000 and EOF before any operation evaluation, followed by the upstream timestamp evaluator with the same depth bound. Later live interoperability testing raised the timestamp depth policy to256, as recorded below. Tests include exact boundaries and traps proving rejected framing never reaches operation calls. Unsupported major versions/file hash algorithms remain distinct from malformed/substituted proofs.

The cache boundary validates closed metadata and every cached80-byte header hash, including unused entries, then exposes immutable block records and defensive summaries. It reports external_explicit trust and cached_only freshness. Witness policy selects an actual checked qualifying Bitcoin path; bad extras are counted, no valid cached witness plus a contradiction fails, and missing cache remains insufficient_chain. Synthetic caches and historical published bytes establish implementation behavior, not independently acquired live node evidence.

No real calendar submission, fresh completed anchor, RPC export or current-chain observation was performed by this phase. Those remain explicit acceptance gaps. This module cannot obtain network authority from pending proof URLs or local receipt state.

## Calendar transport and durable proof actions

Source: _http.py, transport.py, timestamping.py and the bounded raw-Timestamp parser addition in anchors.py. Evidence: tests/test_http.py, test_transport.py, test_timestamping.py and parser regressions. Final main cumulative run:677 passed,1 prerequisite skip,3 upstream warnings in78.24s. Scoped independent re-review returned APPROVE after reproducing and rechecking three defects. No actual public-calendar call was made during implementation.

Actual loopback tests exercise hung/dribbling bodies, TLS and framing failures, stdin/-c callers, bounded IPC and real owned-child cleanup. The final launcher runs a fixed Python module, with data in bounded pipes and no caller main-guard requirement. Non-200 bodies stay remote; scrubbed bounded status/retry metadata crosses IPC. Standard verified TLS and no redirects remain mandatory.

Independent review reproduced close-after-release failure skipping child cleanup, large discarded error pages suppressing Retry-After, and repeated capped commands starving later origins. Test-first fixes drain cleanup without masking primary errors, retain scheduling metadata without reading discarded bodies, and prioritize never-attempted/oldest-due work within each target before round-robin selection. A two-command case now reaches all12 origins while retaining the eight-request cap.

Durable nonces and request reservations precede I/O. Tests cover cooldown/deferral, partial successes, imported proofs, manifest-only registration promoted to a sealed result, fresh upgrade insufficiency, core mutation, no-clobber history and interruption recovery. Unsupported-only replies fail5; unsupported-only imported proofs fail4; no such reply can become a fake pending proof. Malformed local format types fail2 while future strings retain4.

Online attestation presence is unverified until independent cached headers pass offline witness checking. Real submission, fresh completed proofs, independent node export, installed CLI and external feedback remain separate unfulfilled gates.

## Explicit Bitcoin Core snapshot export

Source: evidence.py. Evidence: tests/test_evidence.py. Main read the complete implementation, reran117 focused tests, then794 cumulative passes/1 prerequisite skip/3 existing upstream warnings in89.67s in the capped Python3.12 worker. Independent scoped review returned APPROVE after direct decimal, response-status, input-type and diagnostic-scrubbing probes.

The exporter accepts explicit local config/cookie paths and only the three read-only RPC methods. Actual loopback tests check header authentication without credential-bearing argv, redirects/TLS/network failures, bounded retries and the shared deadline. Strict JSON preserves exact decimal progress without context rounding or unbounded exponent expansion. Stable-tip acquisition rechecks every selected active height, validates raw headers and the complete cache, and returns no partial output. All credentials in these tests are synthetic. No actual node or credential file was accessed.

Separately, the main session submitted a generic no-model manifest and finalized result to the four public OpenTimestamps calendars. Each received pending proofs; one bounded upgrade retained those valid pending proofs without changing either core. This establishes the actual submission path, not a completed Bitcoin anchor. Independently acquired real chain evidence remains unresolved. Full verifier/reference, installed CLI and external feedback are still incomplete.

## Read-only full and inclusion verification

Source: verify.py and focused Directory.digest expected-size support. Evidence: tests/test_verify.py and main-owned test_verify_adversarial.py. Main read the complete source and filesystem diff. Initial cumulative847 passes did not establish acceptance: independent review constructed five genuine membership proofs with visibly impossible trace positions/counts that returned success. The finite trace-only plausibility fix had actual10-case RED before source changes and positive full-log controls. Main's final affected-suite rerun passed578 checks with3 existing upstream warnings in7.45s. Independent scoped re-review returned APPROVE.

The full consumer streams every artifact, checks all supplied records/resources/budget consistency, recomputes only the reviewed fixture rule and independently checks both proof commitments against explicit cached headers. Invalid local evidence cannot disappear behind pending anchors, per-file I/O failures or the error-presentation cap. Reports preserve selected policy/confirmation threshold, partial dimensions and unverified identity/execution. Cache provenance presentation is bounded without altering the actual checked cache. Verification performs no writes, locks, producer calls, implicit cache discovery or network operations.

Inclusion verifies only the selected membership plus direct bindings and finite necessary position/count bounds. Correct-hash false scores remain detectable only in full scope. Coverage, actual resources, budget compliance, scoring and unseen history remain unchecked in inclusion output. The reference verifier, installed process-level offline tests and real independently acquired chain acceptance remain separate gates.

A separate main-owned regression reproduced HTTP child imports from unrelated CWD/PYTHONPATH shadow packages. That launcher issue is tracked as Task6d and remains outside this verifier approval; whole-candidate readiness is not established.

## Installed HTTP child isolation

Task6d changes the fixed child argv to `[sys.executable, '-I', '-m', 'prove._http']`, retaining bounded pipes, timeouts, TLS and cleanup. Main's benign-marker regressions actually failed for CWD, PYTHONPATH and sitecustomize shadow imports before this change. The corrected tests require both marker absence and a successful real loopback response. Exact-argv authentication tests retain no request/authentication data in argv.

Main read the four-line production/assertion diff, then reran the full suite in the capped worker with an editable-installed package:869 passed,1 explicit bind prerequisite skip and3 existing upstream warnings in90.44s. Independent scoped review returned APPROVE. The worker's intermediate partial-output counts were not used as the acceptance verdict. No unsafe import fallback was introduced; the selected interpreter must have Prove installed, consistent with the public contributor setup. Clean wheel/sdist installation and CLI acceptance still remain outstanding.

## Independent materialized-wire reference and fixed corpus

Source: tools/reference_verify.py; static data: src/prove/data/conformance/. Independent authoring worksheet and comparison tests are retained under tests/. The second author used the public protocol/static schema and did not read or import production algorithm bodies. Reference JCS writing, ordered-tree/path validation, supplied-record semantics and fixture math are separate implementations. Fixed expected bytes/roots were authored independently; ordinary tests never regenerate them. Corpus subprocesses isolate imports, deny Prove/rfc8785 imports and trap socket connections. All materialized paths remain data inside the reference.

Main rejected the initial109 passing checks after reading source and reproducing eight additional failures with correctly rebound commitments. Fixes cover completed reasons, unique score roles, fixture dataset bindings in inclusion, known-subtotal overflow with null totals, and unsupported discriminator classification. Independent review then reproduced included-event-size and malformed-format precedence failures. Exact1MiB positive/over-limit genuine-path controls and sequential full-core prerequisite fixes close those findings while retaining inclusion's distinct grouped format preflight. Main inspected final changed sections and actual index SHA256c3dd535124b4822f864d3c4f4c5e7719606784a9ffd20d4b1f9dc2a48e43aa49.

Main full-suite observation before the final reference-order correction:1006 passed,1 bind prerequisite skip,3 upstream warnings in114.42s. Final affected reference/corpus/adversarial rerun:142 passed in22.15s. Independent scoped re-review returned APPROVE. The final103-case corpus includes94 production comparisons, four canonical byte vectors and eight roots/all35 paths. This reference is a scoped data consumer, not an alternate filesystem verifier or Bitcoin implementation. Installed CLI, independent live chain evidence and whole-candidate acceptance remain outstanding.

## Generic CLI and passive package entrypoints

Source: cli.py, passive package/version/module entrypoints and focused static package-data configuration. Evidence: test_cli.py, test_resources.py and main-owned test_cli_adversarial.py. The primary workflow uses generic manifests and external output directories, with no model, research checkout or private service. Public quickstart/integration instructions use the installed command. The package remains an unreleased alpha candidate; editable tests do not establish clean-distribution acceptance.

Main read the full CLI source, namespace bridge, reports and resource configuration. Initial source was not accepted on its green suite. Main reproduced hidden rejected filenames/schema fields and explicit anchor failures losing known local state. Safe bounded actionable diagnostics and registered/sealed state retention corrected those cases. Scoped review reproduced stdout ENOSPC exiting120 with a traceback after durable local work. Additional actual probes covered closed OS descriptor ownership, absent startup stdout and closed TextIO. Terminal reporting failures now return5 without retrying a failed sink or undoing completed output.

Receipt mutations/proof publication hold the selected root and recheck its original namespace; a single-command descriptor-selected cwd bridge restores the prior cwd while preserving primary exceptions. Verification retains its original absolute root and imports no producer/online modules. A separately mounted read-only alias inside a disposable capped worker exercised source overlap and proof-output rejection against an actually valid sealed receipt:2 checks passed in1.14s, cores and receipt validity preserved.

Main baseline cumulative observation:1095 passed,3 explicit bind prerequisite skips,3 upstream warnings in193.44s. Final affected stdout cases passed after the narrow closed-stream guard, and independent scoped review returned APPROVE. Clean wheel/sdist installs, OS-level disconnected verification, supported-version matrix, real independently acquired chain evidence and whole-candidate review remain separate acceptance gates.

## Distribution closure and whole-candidate critique

Initial clean wheel/source installs completed a generic receipt workflow without a source checkout or external network. The source archive audit then rejected missing public documentation, test fixtures and contributor tools. An explicit source manifest repaired that closure; rebuilt wheel/source assets passed byte comparisons against the public source inputs, excluding private planning/worker state. Installed checks exercise packaged resources, ordinary external outputs, full versus inclusion scope, no-clobber, tamper detection and synthetic completed OTS/header consistency. Those synthetic bytes are never described as real node evidence.

The packaging, dependency-notice, public CI and handoff review requested assessed-feedback completion rules. The corrected schema retains a valid unfinished template while requiring exact candidate identifiers, every required observation once, and explanations for checks not run. Main validated positive draft/completed forms and six incomplete negative forms; scoped re-review approved. Actual hosted CI and the final distribution matrix remain separate gates.

A fresh independent whole-runtime review established one recovery blocker: process loss after creation of a private temporary file, or between immutable link/unlink, leaves residue in the normative receipt namespace. Strict unknown-root/unlisted-artifact checks then reject registration retry or checkpoint recovery after proper explicit stale-lock recovery. The reviewer reproduced registration, final core and final artifact windows; main independently reproduced the final-core failure. Fixing this requires durable exact temporary-file ownership or equivalent safe staging, without prefix-based cleanup, ignored unknown files, or source mutation. The finding remains open until real process-exit regressions and scoped re-review pass.

Main's review of the proposed exact-owner recovery fix added actual link/unlink and pre-parent-creation process exits plus identical-registration durability probes. Two further failures were reproduced: recovery with an uncreated nested parent, and a retry that skipped file durability repair. Narrow corrections now pass22 affected checks, including the original critic's three process-loss reproductions and preservation of legitimate temporary-looking artifact names. Whole-candidate scoped re-review and final full suites are still required.

Live calendar testing separately exposed a real interoperability defect. Four HTTP200 replies of1001 bytes each were valid under pinned OpenTimestamps0.5.0 but exceeded Prove's64-node policy. Their measured timestamp depth was69. The bound now matches upstream's256-node default, while preflight still enforces byte/work/depth/EOF limits before evaluating operations. The affected batch passed129 checks; four frozen real replies and two depth/preflight checks passed6 more. A real upgrade then obtained Bitcoin-attestation-present proofs at height974785 for both original frozen cores, with no warnings and unchanged core IDs. Without independently selected chain evidence, verification correctly remains insufficient-chain. This does not establish completed independently verified anchoring or the separate locally gated fresh-launch requirement.

Final scoped re-review approved both runtime fixes and independently reran the original three crash reproductions plus six OTS interop/boundary cases:9 passed. Main matched the reviewed runtime blobs to the committed source. Recovery is committed at `fc789c4`; OTS interoperability at `bccf318`. Main's final supported-version observations passed1121 tests each on Python3.11.16/3.12.13/3.13.13, with3 explicit bind prerequisites skipped and3 upstream OpReverse warnings each. A separate actual second-bind run passed both source and CLI cases. Wheel and source installations completed the generic offline/synthetic-anchor workflows on all three runtimes with no source checkout mounted and no external network. Hosted CI and independently acquired real chain evidence remain distinct gates.
