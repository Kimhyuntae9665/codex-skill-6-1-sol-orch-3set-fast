---
name: 6-1-sol-orch-3set-fast
description: Coordinate substantial work with one GPT-6.1 Sol chief and three non-overlapping Sol/Luna sets, all requiring Fast mode, with optional Astra reviews. Use when the user requests this three-set hierarchy or authorizes parallel sets for independent work; do not add teams to a trivial task.
---

# 6.1 Sol Orch — 3 SET Fast

One chief owns global decomposition and integration. Three set leaders own
distinct work packages. Preserve the approved [topology](assets/topology.png):
chief → three parallel sets → same chief for final integration. Repeated Sol
cards are stages of the same leader, not extra agents. Astra is conditional.

Invocation authorizes this agent workflow within the user's task. It does not
authorize new sidebar chats, publication, submission, or unrelated configuration
changes. Small tasks stay with the chief; do not invent three packages just to
fill the diagram.

## Roles: Fast required for every model

| Role | Model | Reasoning | Responsibility |
| --- | --- | --- | --- |
| Chief, one | `gpt-6.1-sol` | medium | Decompose, grant ownership and slots, resolve cross-set decisions, integrate and verify. |
| SET 1–3 leader | `gpt-6.1-sol` | medium | Allocate bounded children, integrate its package and report evidence. |
| Explorer, per set as useful | `gpt-6-luna` | high | Investigate a bounded code path; no production edits. |
| Researcher, per set as useful | `gpt-6-luna` | high | Answer assigned questions with sources; no production edits. |
| Worker, per set as useful | `gpt-6.1-sol` | high | Implement in owned files and run focused checks. |
| Reviewer, only when needed | `gpt-6-astra` | low | Independently review completed work; report without editing. |

Fast is the service tier, not low reasoning or Ultrafast. Before spawning,
inspect the active model, effective Fast setting, available models, nesting
support, tool schema and remaining capacity. Read
[runtime.md](references/runtime.md) for tier checks and scheduling. A skill
cannot change the active chief model or raise a host-imposed capacity.

Require Fast for EVERY role. Apply a supported explicit Fast/priority option
when exposed; otherwise use verified Fast parent/runtime configuration and
host-supported inheritance. Never invent a spawn parameter. Track required,
configured/requested, and observed tier separately. A request without telemetry
does not prove the actual serving tier; disclose that uncertainty. If Fast is
known disabled/unsupported, report the blocker before launching that role;
do not silently substitute Standard or a different model.

## Chief: allocate before anyone starts

1. Inspect relevant instructions, inputs, current work and existing agents.
   Identify independent units. Settle critical shared interfaces first.
2. Write `work/three-set/<run-id>/plan.json` using
   [dispatch-contracts.md](references/dispatch-contracts.md). Use exactly three
   set records for a genuine three-set task; blocked/unnecessary packages can
   remain queued or be cancelled with reasons.
3. Assign each set a distinct objective, work keys, read inputs, exclusive write
   scopes, outputs, acceptance checks and dependencies. Partition search
   questions/domain pools as well as code. Shared input reading is allowed;
   repeated research or implementation objectives are not.
4. Run `python <skill-dir>/scripts/check_plan.py <plan> --workspace <root>`.
   Use an actually available Python 3.9+ interpreter; the helper uses only the
   standard library. Resolve a host/bundled runtime if `python` is unavailable.
   Correct conflicting declared paths, duplicate work keys, unowned outputs
   and dependency cycles before dispatch. Review objective wording too: the
   checker cannot detect semantic duplicates with different keys.
5. Choose the honest execution mode from actual capacity. Give each leader
   only its contract, necessary shared decisions, this role table, runtime
   rules and exact slot grant. Briefly explain each set's ownership and whether
   the three sets can actually run concurrently.

Only the chief writes the global plan or reassigns work between sets. Leaders
request changes; they do not silently absorb another set's tasks.

## Each SET: work inside its grant

A leader MUST NOT run the chief procedure again or recursively create three
more sets. It may spawn only its bounded explorer, researcher, worker and
conditional reviewer. These children do not delegate further.
Keep at most one live agent in each role per SET: two Luna roles, one Sol
worker, and one conditional Astra. Do not replace the Sol worker with a third
Luna or multiply researchers to fill spare slots. Split successive work units
inside these role limits and reuse the assigned agents where supported.

- Give each child one objective, exclusions, exact files/read-only scope,
  necessary inputs, expected evidence, checks, model, reasoning and Fast
  requirement. Pin model/effort through supported tool fields. If full-history
  forks forbid overrides, use a scoped contract with no fork or a supported
  small fork. Do not copy irrelevant history.
- The leader alone maintains
  `work/three-set/<run-id>/set-N/assignments.json`. Record child task keys,
  agent identities, scopes, dependencies and state. One live writer per file,
  including scratch outputs. Leaders do not edit worker-owned files while
  those workers own them. Validate child scopes stay inside this SET's scope
  and do not overlap other live writers; the global helper checks SET scopes.
- Explorer and researcher may work concurrently on distinct questions.
  Implementation dependent on their evidence waits for that evidence; diagram
  branches do not justify racing dependent work.
- Reuse completed results by work key before searching or implementing again.
  Independent review intentionally rechecks a result, not its implementation.
- Request scope/slot changes before spawning or touching other SET files.
  Report unmet dependencies; do not redo the supplying set's work.
- Request Astra only for consequential security, integrity, concurrency,
  compatibility or cross-component risk, or concrete unresolved concerns.
  Finish worker edits and obtain a review slot first. Address material findings
  and verify fixes. No standing tester role.
- Return outputs, changed files, checks/results, sources, uncertainty, actual
  model/tier evidence and child completion status. Confirm children no longer
  write before handing ownership to the chief.

## Global ownership and capacity

All sets share a workspace. Canonicalize paths; case/alias differences are not
different ownership. Serialize shared files instead of assigning simultaneous
writers different line ranges. Use distinct set-local scratch directories.
Shared configs, schemas, browser forms, databases, environments and services
also need one explicit owner; a path checker does not lock external resources.

Before reassigning: stop the previous writer, wait for acknowledgement, check
partial work/background tools, update and recheck the plan, then grant the new
owner. An interrupted turn alone does not prove a background tool stopped.
Do not repeat completed work without new evidence.

The chief grants slots centrally. Leaders cannot independently consume all
capacity. Never fill every slot with waiting leaders and leave none for their
workers. Regrant only after the host confirms available capacity. Idle/done
threads may occupy open-thread limits; reuse permitted agents where possible.
If closing/releasing is unavailable, use actual remaining capacity and report
the reduced mode. Do not loop on rejected spawns or bypass limits with new
chats/CLI processes.

## Integrate and finish

The chief joins returned outputs and checks dependency contracts. Cross-set
repairs go to one owner or to the chief after acknowledged handoff; do not
make all three sets repair the same issue. Run meaningful integration checks
proportional to the changes, reusing valid focused results.

Confirm required agents/writers are finished and inspect final artifacts or
diffs. Report outcome, checks, concerns, actual concurrency mode and material
Fast/model uncertainty. Three sets do not prove a threefold speedup; only
measured elapsed time can support that claim.
