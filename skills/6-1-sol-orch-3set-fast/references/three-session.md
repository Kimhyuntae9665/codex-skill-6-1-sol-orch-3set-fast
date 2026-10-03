# Three separate SET chats, all parallel

This is the reference separate-root deployment. Use it only when the human
explicitly requests three new SET chats; installing or invoking the skill
alone does not authorize user-owned chat creation. Otherwise use internal
subagents in one tree if its verified capacity supports the full hierarchy.
Inspecting or editing the skill alone does not launch sessions. Do not silently
switch single-tree execution to new chats after a capacity error.

The chief remains in the current chat. Create exactly three local chats with
the app's supported create_thread tool, one for each SET. These are independent
roots, not descendants visible in the chief's collaboration tree. Each root
is its SET's Sol leader and starts two Luna/high children and one Sol/high
worker immediately. An Astra/low reviewer is optional and reviews completed
artifacts. With all reviewers present, the whole deployment is 1 chief +
3 SET roots + 12 children = 16 unique agents.

1. Agree the shared workspace, interfaces and exclusive SET scopes first.
   Use absolute paths because projectless chats start in different directories.
   Record deployment="three-session" in the chief-owned plan. Before launch,
   use verified new-root capacity evidence rather than the old chief's limit.
2. Dispatch all three create_thread calls without waiting for any SET to finish.
   Select Sol 6.1/medium for leaders through supported model/effort arguments
   (`model="gpt-6.1-sol"`, `thinking="medium"` for create_thread). The chief
   also requires Sol 6.1/medium; follow runtime.md for a host mismatch.
   Supply each leader its specific package, scope, child roles, checks and
   shared absolute paths. It must not create more chats or duplicate other SETs.
3. Each root checks its actual tool capacity: at least four total slots for
   the basic SET, five if its reviewer must coexist. It pins child models via
   supported spawn fields, verifies Fast configuration separately and records
   live child identities, launch times and statuses in its own assignments file.
   Do not claim the configured 16 spawned slots are an observed maximum.
4. Chief owns the global plan and control file. Each SET exclusively writes
   its assignments, status and results. The chief reads these and uses compact
   wait_threads snapshots to verify all roots and children overlap. Namespace
   child identities by chat ID; different roots can reuse /root/child names.
   capacity_total in the existing plan checker describes aggregate declared
   capacity for this deployment; record verified per-SET local capacity and
   actual chat IDs only in private local runtime records. Public records use
   synthetic aliases and omit private identifiers and personal absolute paths.
   The checker validates declared ownership, not per-chat runtime limits.
5. Coordinate through the agreed shared files. Messaging other chats requires
   explicit human authorization for that messaging; do not infer it from an
   agent's request to report back. Attach all created chat directives in the
   final response as required by the app. The chief may integrate each SET's
   output as it arrives without waiting for all SETs.
   Apply [information-exchange.md](information-exchange.md): SET-owned immutable
   revisions, atomic publication, provenance and checksum verification. No
   conversation history or memory is automatically copied between roots.
6. Each leader finishes or safely stops its children, verifies writers and
   background tools stopped, then returns checks and outputs. On failure, stop
   further dispatch, preserve checkpoints and record exactly what launched.
   No set-by-set queue, repeat attempts against a known limit or hidden CLI
   sessions. Do not archive the user-owned chats without a user request.

## Capacity experiment, 2026-10-03

These are historical local observations, summarized in the sanitized
[verification records](https://github.com/Kimhyuntae9665/codex-skill-6-1-sol-orch-3set-fast/blob/main/examples/verification-records.json). Raw private
records are not distributed; summaries omit personal paths and chat identities.

Three newly created local chats each advertised 17 total slots and successfully
launched four children (two Luna, one Sol, one Astra). All three SET roots and
12 children overlapped while the chief remained active: 16 total agents.
The old chief chat still advertised four total slots. All 12 probe children
were interrupted and all three test turns finished.

This was a bounded idle-hold capacity test. It verifies creation and overlapping
live runs, not measured speedup, 16 children in a single chat, production
completion, exact leader reasoning or observed Fast serving. Recheck current
runtime evidence on future launches; historical success is not a guarantee.

## Information integration experiment, 2026-10-03

The same three SET chats independently collected config, plan-checker and
graph facts. SET 2 read SET 1's published file and recorded its generated nonce,
byte SHA-256 and received facts. SET 1 verified that receipt. SET 3 read all
three sources and SET 2's receipt, checked hashes and provenance, and published
an integrated result. The chief independently rechecked these artifacts.
This confirms shared-file information transfer and integration on this local
host. It does not imply automatic history sharing or cross-host file access.
