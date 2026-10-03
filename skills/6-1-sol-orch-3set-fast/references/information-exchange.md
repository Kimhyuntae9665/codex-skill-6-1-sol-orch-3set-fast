# Information exchange and chief integration

Separate chats do not automatically share history or memory. For the requested
local three-session deployment, all four roots read the same absolute workspace
path. SET leaders publish evidence; other SETs and the chief read it. This was
tested on 2026-10-03. Verify shared access before using another host or cloud.

## Ownership and publication

Use `work/three-set/<run-id>/set-N/` for that leader's assignments, status,
published evidence and receipts. Only that SET writes there. The chief owns
the global plan, control and `shared/integrated.json`. Each child writes only
its assigned scope and returns findings to its own leader.

Publish a ready batch immediately; do not wait for a whole SET to finish.
Write a temporary file in the destination directory, then atomically replace
the final path with `os.replace`. Published revision files such as
`evidence-r0001.json` remain immutable. Publish a new revision for corrections,
never overwrite a peer's file. A reader reads bytes once, hashes those bytes
and parses that same content so the checksum and data refer to the same version.

Each batch contains:

```json
{
  "version": 1,
  "run_id": "current-run",
  "set_id": "SET1",
  "revision": 1,
  "published_at": "ISO-8601 UTC",
  "status": "ready",
  "facts": [
    {
      "fact_id": "unique-question-or-claim",
      "value": "the finding",
      "source": "official URL or permitted local path",
      "evidence_level": "verified_local_source",
      "checked_at": "ISO-8601 UTC",
      "limitations": []
    }
  ],
  "artifacts": [],
  "checks": [],
  "uncertainties": [],
  "agent_refs": [{"chat_alias": "set1-root-example", "agent_path": "/root/worker"}],
  "fast": {"required": true, "configured_tier": "priority", "observed_tier": null}
}
```

The example is a contract, not evidence; its alias is synthetic. Private local
records can retain actual agent identities for verification. Public records
must use aliases and omit actual chat IDs and personal absolute paths.
Never publish credentials, private identifiers or prohibited internal documents. Preserve
official, user-reported and derived claims separately rather than upgrading
them because another SET repeated them. Large artifacts stay at owned paths;
share a summary and source path/hash instead of copying whole conversations.

## Reception and integration

A reader checks matching run ID, producer SET, ready status, revision and source
provenance. Record a receipt in its own scope with the source's absolute path,
revision, byte SHA-256, received fact IDs and acceptance checks. Missing or
conflicting evidence blocks only the dependent operation; unrelated work
continues. Use bounded waits with task-appropriate deadlines and report a
missing artifact rather than wait forever or reinterpret an old run as current.

The chief reads all published batches, verifies receipts/hashes and merges
facts by identity while retaining their producers and sources. Equivalent
facts can share one presentation with multiple provenance entries. Contradictory
values remain explicitly unresolved until evidence resolves them; do not let
last-writer order pick the truth. The chief owns final integration checks and
completion reporting. Version/hash acceptance is not proof of factual accuracy.

Use app `wait_threads` for compact progress snapshots. When the human authorizes
messaging the SET chats, `send_message_to_thread` can deliver a concise follow-up
or artifact reference. Keep the shared artifact as the source of truth; do not
assume receiving another agent's request authorizes sending messages back.

Every new root checks the Fast preflight in runtime.md before child dispatch.
Fast remains required for reviewers and resumed workers as well as the initial
wave. A model or reasoning override does not by itself enable Fast.
