# Dispatch contracts

The chief writes and validates the plan BEFORE dispatch. Only the chief edits
this global file; leaders return scope changes as proposals.

## Plan example

```json
{
  "version": 1,
  "run_id": "example",
  "objective": "Deliver the requested account page",
  "chief_write_scope": ["work/three-set/example/shared/"],
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
      "state": "queued"
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
      "state": "queued"
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
      "state": "queued"
    }
  ]
}
```

This assumes the chief already settled the shared contract. If SET2/SET3
instead needs SET1's finished output, include `SET1` in `depends_on` and hold
dependent work until that artifact is accepted.

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
Capacity: chief-granted maximum N child slots; request changes before spawn.
Children: Luna explorer/high, Luna researcher/high, Sol worker/high as useful;
conditional Astra reviewer/low. All require Fast; none delegate further.
At most one live child per role; preserve the two-Luna/one-Sol composition.
Ownership: single live writer per file, including scratch outputs.
Dependencies: wait for required evidence; reuse completed other-set results.
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
`agent_id`, `role`, `write_scope`, `state`, `depends_on`, and `checks`.
Children return results, not competing ledger edits. The leader checks every
child scope is within its SET and does not overlap other live writers or its
own edits. The global helper checks SET declarations, not actual worker edits.

States: `queued → running → done`, plus `blocked` and `cancelled`. On handoff,
stop/confirm the previous writer, inspect partial output, update/recheck the
plan and then grant the new owner. Index returned results by work key for reuse.
Use internal collaboration tools, not new sidebar chats, for coordination.
