---
name: 6-1-sol-orch-3set-fast
description: Run substantial work through three simultaneous Sol/Luna agent sets in Fast mode, with one Sol chief and optional Astra reviews. Use for the complete three-set parallel hierarchy; never substitute staggered, sequential, or chief-only execution.
---

# 6.1 Sol Orch — 3 SET Fast, Parallel Only

Run one chief and THREE sets concurrently. The standard hierarchy has
**13 distinct agents**: one chief + three Sol leaders + six Luna children +
three Sol workers. Three optional Astra reviewers bring the total to 16 when
needed. See the [topology](assets/topology.png).

The sets are simultaneous teams, not three rounds of one team.
**No skill-imposed slot throttle, set queue, staggered schedule, sequential
fallback, or reduced execution mode.** A host limit cannot be erased by a
prompt: if the runtime cannot run the full hierarchy, report that the requested
parallel execution is unavailable. Do not label a smaller run as this skill.

The [three-session deployment](references/three-session.md) is the reference
architecture: each SET leader is a separate chat root, and all three dispatch
their children concurrently. Create those user-owned chats only when the human
explicitly requests new chats. Otherwise use a single nested agent tree when
its effective capacity and nesting support the full hierarchy. Never switch
to new chats after a capacity error without that explicit request.
Merely inspecting or editing this skill does not launch agents or chats.
Invoking the workflow does not authorize publication, submission, messages to
other chats, or host configuration changes.
Use this workflow for substantial work that supplies three independent packages.
Do not manufacture duplicate/busywork tasks to populate the graph.
For the user's requested separate-session workflow, shared versioned JSON
carries evidence between SETs and back to the chief. Read the
[exchange contract](references/information-exchange.md) before dispatch.

## Model roles — Fast required throughout

| Role | Count | Model | Reasoning | Work |
| --- | --- | --- | --- | --- |
| Chief | 1 | `gpt-6.1-sol` | medium | Set interfaces, dispatch, integrate and verify. |
| SET leaders | 3 | `gpt-6.1-sol` | medium | Dispatch each set's children and integrate its outputs. |
| Explorer | 1 per SET | `gpt-6-luna` | high | Explore a distinct source/code/domain slice; no production edits. |
| Researcher | 1 per SET | `gpt-6-luna` | high | Resolve distinct evidence questions with sources; no production edits. |
| Worker | 1 per SET | `gpt-6.1-sol` | high | Implement or verify artifacts in its exclusive scope. |
| Reviewer | Optional per SET | `gpt-6-astra` | low | Independently review completed outputs; no edits. |

The public contract requires Sol 6.1/medium for the chief and all SET leaders.
Pin leader effort through supported tool fields and record actual chief effort.
The host selects the active chief; see runtime.md for runtime mismatches.

Fast is the serving tier, not low reasoning. Inspect model availability, Fast
configuration/inheritance, nesting support and effective runtime capacity using
[runtime.md](references/runtime.md). Pin supported model/effort fields; use
no/small history forks where full-history forks forbid overrides. Never invent
a tier field. Record configured/requested and observed tier separately;
configuration without telemetry does not prove actual Fast serving.
Fast is mandatory for the chief, all three SET leaders and every Luna, Sol and
Astra child. Verify the configured Fast route and `features.fast_mode = true`
at each new root before spawning, inspect applicable overrides and preserve
Fast inheritance. Do not continue a known Standard/disabled-Fast run or claim
Fast merely because a prompt says so. Unknown server telemetry remains unknown.

Inspect host configuration following runtime.md. Its example allows 16 spawned
agents (17 including the chief), enough for the full topology and reviewers.
Change configuration only with the host owner's explicit authorization and
preserve higher existing values. Verify effective runtime limits separately;
writing a config does not hot-reload active chats.

## Launch the whole hierarchy without set-by-set waits

1. Inspect inputs, instructions and existing agents. Settle shared interfaces
   once. Divide the objective into three independent packages; partition
   company/domain pools and research questions as well as files.
2. Write `work/three-set/<run-id>/plan.json` using
   [dispatch-contracts.md](references/dispatch-contracts.md). Assign all sets
   distinct work keys, exclusive scopes, outputs and checks. Record
   `execution_mode: "parallel-only"`, actual `capacity_total`, and
   `concurrent_reviewers` (0 at initial dispatch). Record `deployment` as
   `three-session` for explicitly requested new SET chats, or `single-tree`
   for internal subagents. Initial execution needs
   13 total agents; this describes the architecture, not a skill-side throttle.
3. Validate once with Python 3.9+:
   `python <skill-dir>/scripts/check_plan.py <plan> --workspace <root>`.
   Correct collisions, unowned outputs and set-to-set dependencies. The checker
   does not prove semantic independence or query live capacity.
4. Dispatch SET 1, SET 2 and SET 3 immediately in the same dispatch wave.
   For explicitly requested `three-session` execution, create exactly three
   local chats through the supported app tool and follow three-session.md.
   Calls may be issued one after another, but **do not await one set's completion
   before starting the next**. Each leader immediately starts its Explorer,
   Researcher and Worker with ready, distinct initial tasks. The chief must not
   do a whole package itself while leaving its SET queued.
5. Inspect the live agent tree after dispatch. Record identities, parent links,
   ownership, launch times and states. Claim full parallel operation only with
   evidence that all three sets and their basic children launched and overlapped;
   a plan or diagram alone is insufficient.
6. Publish ready findings as versioned SET-owned files and read relevant peer
   findings while other independent work continues. The chief validates run ID,
   revision, hashes and provenance, then integrates results in its own output.
   Peer artifact dependencies do not turn the three SETs into a completion chain.

If spawning fails or effective capacity is too small, report the concrete
blocker and partial tree. Do not claim success, drain SET 1 then start SET 2,
retry a known limit repeatedly, or create unrequested chats/CLI processes.
A three-session deployment is the reference separate-root
architecture; its capacity must be verified separately for every new SET chat.
Preserve partial results. Explain that supported host configuration/new runtime
is needed before the requested parallel execution can proceed.
After a partial launch failure, stop further dispatch and tell launched agents
to stop new work and return a safe checkpoint. Confirm each writer and pending
background tool has stopped or completed, record final states and preserve
outputs before ending the blocked run. Do not leave orphaned writers running.

## Each SET runs its children in parallel

A leader is not another chief: do not recursively create three more sets.
Children do not delegate further. Preserve the defined roles and models.
Each standard set runs one Explorer, one Researcher and one Worker concurrently;
the role composition is the requested topology, not a low-capacity fallback.

- Give each child one objective, exclusions, read inputs, exclusive write paths,
  checks, model, reasoning and Fast requirement. Keep prompts concise; do not
  copy irrelevant history or repeat completed work.
- Only the leader writes `set-N/assignments.json`: work keys, agent identities,
  parent links, scopes, launch/state evidence and results.
- Give the Worker useful ready work from dispatch: implementation against an
  agreed contract, an independent artifact, or verification of existing evidence.
  Forward findings as they arrive; do not make it wait for both Luna roles to
  finish their entire package before starting.
- Real artifact dependencies still apply: dependent operations use accepted
  evidence while unrelated branches continue immediately. Redesign a SET that
  depends entirely on another SET before launching. Do not create a serial SET
  chain or race missing data merely to claim concurrency.
- Request Astra only for consequential risk or concrete unresolved concerns.
  Reviews use completed artifacts; independent ready reviews can run together.
  All basic children and three added reviewers need 16 total live threads if
  they coexist. Check actual capacity; never throttle other SETs for a review.
- Return outputs, changes, checks, sources, uncertainty, model/tier evidence
  and child states. Confirm writers finished before ownership handoff.

## Parallel efficiency and ownership

Each research question and output has one owner. Shared reading is allowed;
duplicate implementation/research is not. Canonicalize paths, use set-local
scratch and keep one live writer per file/resource. Shared configs, forms,
databases and services also need an owner. Serialize only an actual shared
mutation; never serialize entire sets because of it.

Keep all ready independent work active. The chief integrates outputs as they
arrive, reuses results by work key and gives cross-set fixes to one owner.
Before reassigning ownership, confirm the previous writer/background operation
stopped and update the plan. Interrupted turns alone do not prove tools stopped.

Inspect artifacts/diffs and run proportionate integration checks. Report the
result, actual simultaneous counts, launch/overlap evidence and Fast/model
uncertainty. Do not infer measured speedup from the number of agents.
