# Dispatch contracts

The chief writes and validates the plan BEFORE dispatch. Only the chief edits
this global file; leaders return scope changes as proposals.

## Plan example

```json
{
  "version": 2,
  "run_id": "example",
  "objective": "Deliver the requested account page",
  "execution_mode": "parallel-only",
  "deployment": "three-session",
  "capacity_total": 16,
  "concurrent_reviewers": 0,
  "chief_write_scope": ["work/three-set/example/plan.json", "work/three-set/example/shared/"],
  "shared_inputs": ["The agreed account API schema"],
  "sets": [
    {
      "id": "SET1",
      "objective": "Implement the account API",
      "work_keys": ["implementation:account-api", "research:account-auth"],
      "read_inputs": ["src/shared/account-schema.json"],
      "write_scope": ["src/api/account/", "work/three-set/example/set-1/"],
      "outputs": ["src/api/account/handler.py"],
      "checks": ["API matches the agreed schema"],
      "depends_on": [],
      "state": "ready"
    },
    {
      "id": "SET2",
      "objective": "Implement the account UI against the agreed schema",
      "work_keys": ["implementation:account-ui"],
      "read_inputs": ["src/shared/account-schema.json"],
      "write_scope": ["src/ui/account/", "work/three-set/example/set-2/"],
      "outputs": ["src/ui/account/page.tsx"],
      "checks": ["Page handles agreed success and error states"],
      "depends_on": [],
      "state": "ready"
    },
    {
      "id": "SET3",
      "objective": "Write the user guide from the agreed behavior",
      "work_keys": ["documentation:account-guide"],
      "read_inputs": ["src/shared/account-schema.json"],
      "write_scope": ["docs/account/", "work/three-set/example/set-3/"],
      "outputs": ["docs/account/guide.md"],
      "checks": ["Guide matches agreed behavior"],
      "depends_on": [],
      "state": "ready"
    }
  ]
}
```

All three SET `depends_on` arrays must be empty: teams start together, not in
a completion chain. Settle interfaces or redesign dependent packages before
launch. Artifact dependencies inside a SET belong in child assignments;
unrelated work continues.

`capacity_total` is available effective runtime capacity including the chief,
not only a configured number. `concurrent_reviewers` is 0..3 and counts added
Astra agents coexisting with the 13 basic agents. The checker rejects old
plans, insufficient capacity and serial SET dependencies; it does not query
the host. Record live launch/overlap evidence separately.

The global `work/three-set/<run-id>/plan.json` is always reserved to the chief
by the checker, even if omitted from the declared chief paths. Include it
explicitly in the plan for clarity. Leaders only own their local assignments.

Paths are literal workspace-relative files/directories, not globs. A scope
reserves the path and descendants. The checker resolves aliases/symlinks and
compares case conservatively; cross-owner parent/child scopes conflict. Use
exact files when directory reservations would overlap unnecessarily.
Cancelled records retain ownership until the chief removes/reassigns it after
acknowledged handoff; cancellation alone does not release a writer.

Work keys name atomic activities such as `research:official-auth-contract`,
not broad labels like `python`. The chief checks different keys for semantic
overlap. For company research, partition explicit company/domain pools and
questions; do not give all sets the same search phrase. Shared sources are
allowed; each research question has one owner.

## Leader contract

Send the SET record, necessary shared decisions, relevant skill sections and:

```text
Role: SET2 leader, not chief; do not create three more sets.
Model: gpt-6.1-sol; reasoning: medium; Fast required.
Scope: SET2 contract only; exclude SET1/SET3 production files.
Launch: start Luna explorer/high, Luna researcher/high and Sol worker/high
immediately on distinct ready tasks; do not await another SET or a whole
child package before launching the others. All require Fast; none delegate.
Preserve two Luna children and one Sol worker; optional Astra reviewer/low.
The standard hierarchy has 13 agents; no set-by-set slot grants/throttle.
Ownership: single live writer per file, including scratch outputs.
Dependencies: accepted evidence for dependent operations; keep other ready
branches active. Reuse results; do not serialize the whole package.
Return: artifacts, changed files, checks/results, sources/uncertainty,
actual model/tier evidence and confirmation children stopped writing.
Unexpected overlap/dependency: report before expanding scope.
```

Pin model/effort through supported spawn fields; prose alone does not select
a model. If no tier parameter exists, follow runtime.md.

## Child contracts and local ownership

Each child receives one task, exclusions, paths, read/write permissions,
model/effort/Fast requirement, evidence, output and acceptance checks. Only
the leader writes its assignments file. Entries record `task_id`, `work_key`,
`agent_id`, `parent_agent`, `role`, `write_scope`, `launched_at`, `state`,
`depends_on`, and `checks`. Keep live snapshots/timestamps for overlap evidence.
Children return results, not competing ledger edits. The leader checks every
child scope is within its SET and does not overlap other live writers or its
own edits. The global helper checks SET declarations, not actual worker edits.

States: `ready → running → done`, plus `blocked` and `cancelled`. Ready means
prepared for the same dispatch wave, never awaiting another SET's completion.
On handoff,
stop/confirm the previous writer, inspect partial output, update/recheck the
plan and then grant the new owner. Index returned results by work key for reuse.
Within each SET use internal collaboration tools. For explicitly requested
three-session deployment, use the separate-root contracts in
[three-session.md](three-session.md), absolute shared workspace paths and
compact app wait snapshots. Chat identities are distinct from child agent paths.
