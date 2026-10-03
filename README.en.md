# 6.1 Sol Orch · 3 SET Fast

**Three teams start, but their results never merge. This skill gives them a shared contract and one chief responsible for the final result.**

A Codex skill for **three concurrent work packages**. The Sol chief assigns research questions, files and outputs before dispatch. Each SET runs a Sol leader, two Luna children and one Sol worker in parallel. Ready findings travel through shared JSON with source provenance; the same chief verifies and integrates them. Every role requires Fast, with optional Astra reviewers.

[한국어](README.md) · [Skill instructions](skills/6-1-sol-orch-3set-fast/SKILL.md) · [Example plan](examples/plan.json) · [Validation record](examples/validation-record.json) · [Apache-2.0](LICENSE)

![The same Sol chief starts three concurrent SETs, validates their shared evidence and integrates the final result](skills/6-1-sol-orch-3set-fast/assets/topology.png)

The large Sol cards at the top and bottom are **the same chief**. Repeated Sol cards inside a SET are stages of the same leader. Dashed edges represent optional Astra review. The illustration and model badges are custom explanatory artwork, not official logos. [Editable SVG](skills/6-1-sol-orch-3set-fast/assets/topology.svg) · [Attribution](skills/6-1-sol-orch-3set-fast/assets/ATTRIBUTION.md)

## Install and invoke

Ask Codex to install the skill:

```text
Install the Codex skill at the GitHub path below.
If an installed copy exists, preserve the original outside skill discovery
before replacing it.
https://github.com/Kimhyuntae9665/codex-skill-6-1-sol-orch-3set-fast/tree/main/skills/6-1-sol-orch-3set-fast
```

After checking the runtime, ask the chief in the current chat:

```text
$6-1-sol-orch-3set-fast
Build the account API, UI and user guide.
Create exactly three separate local SET chats with Sol 6.1/medium leaders.
Have all three use the same absolute workspace path and start concurrently:
SET1 owns the API, SET2 owns the UI and SET3 owns the guide.
The chief should first settle the shared schema and exclusive file ownership.
Each SET should immediately run two Luna/high children and one Sol/high worker
in parallel, publishing sources and checks through shared JSON.
Require Fast for every role. The chief should verify hashes, provenance and
integrated behavior, then deliver the final result.
```

This request explicitly authorizes **three SET chats**. Separate chats do not automatically share conversation history. To use only internal subagents, request that deployment and verify enough capacity and nesting support in one chat for the full hierarchy. Installing or inspecting the skill does not create SET chats.

## How results reach the chief

| Stage | Responsibility and output |
| --- | --- |
| Chief settles the contract | Shared inputs and interfaces, unique work keys, one writer per file, SET acceptance checks |
| Three SETs run concurrently | Leaders dispatch exploration, research and writing immediately; publish ready findings |
| Shared JSON carries evidence | Immutable SET revisions, atomic publication, facts and sources, uncertainty, receipts and SHA-256 |
| Chief integrates | Verify run ID, revision, hashes and provenance; resolve conflicting facts and check the complete result |

The workflow does not start one SET after another finishes. Settle shared contracts before launch so each package can start independently. Only operations that need an actual artifact wait for accepted evidence; other ready work continues. [Dispatch contracts](skills/6-1-sol-orch-3set-fast/references/dispatch-contracts.md) · [Information exchange](skills/6-1-sol-orch-3set-fast/references/information-exchange.md)

## Models and capacity

| Role | Count | Model / reasoning |
| --- | --- | --- |
| Chief | 1 | `gpt-6.1-sol` / medium |
| SET leader | 3 | `gpt-6.1-sol` / medium |
| Explorer | 1 per SET | `gpt-6-luna` / high |
| Researcher | 1 per SET | `gpt-6-luna` / high |
| Writer / implementation worker | 1 per SET | `gpt-6.1-sol` / high |
| Optional independent reviewer | Up to 1 per SET | `gpt-6-astra` / low |

**The basic hierarchy has 13 agents; adding all three Astra reviewers makes 16.** Each separate SET chat needs at least four local slots including its root, or five with a coexisting reviewer. Aggregate capacity cannot replace missing local capacity. All three leaders and basic child roles launch; children do not delegate further.

The host selects the main model and reasoning effort. Invoking the skill does not change the active chief's settings; handle mismatches through the [runtime preflight](skills/6-1-sol-orch-3set-fast/references/runtime.md).

The inspected test environment used this global configuration. Preserve existing settings and check authorization, profiles and project settings before applying individual keys:

```toml
service_tier = "priority"

[features]
fast_mode = true

[agents]
enabled = true
max_concurrent_threads_per_session = 16
```

The [local subagent limit](https://learn.chatgpt.com/docs/agent-configuration/subagents) excludes the primary root. A configured limit of 16 allows 17 including the root; this differs from the 13 or 16 agents the topology needs. Changes may require a new runtime. Check actual capacity, Fast inheritance and overrides at every SET root. If the complete hierarchy cannot start, report the limit and partial results rather than label a reduced run as success.

[Codex's Fast documentation](https://learn.chatgpt.com/docs/agent-configuration/speed) shows `service_tier = "fast"` and `features.fast_mode = true`. The [API Fast guide](https://developers.openai.com/api/docs/guides/fast-mode) treats `fast` and `priority` as equivalent for supported API models; it does not establish that every Codex host accepts the same persisted alias. The local experiment verified configured `priority` and `fast_mode = true`; actual serving telemetry remained `observed_tier: null`. Reasoning effort, configured tier and observed serving tier are separate facts. [Runtime guidance](skills/6-1-sol-orch-3set-fast/references/runtime.md) · [Separate SET chats](skills/6-1-sol-orch-3set-fast/references/three-session.md)

## Check a dispatch plan

Python 3.9+ standard library only. Run from the repository root:

```sh
python skills/6-1-sol-orch-3set-fast/scripts/check_plan.py examples/plan.json --workspace .
python -m unittest discover -s tests -v
```

Plan checks return `0` on success and `2` on failure. Version 2 checks cover parallel execution declarations and required capacity, overlapping SET ownership or work keys, out-of-scope outputs and serial SET dependencies. The global plan path is reserved to the chief. Shared reads are allowed. The tool checks declarations; it does not query live capacity, lock files or automatically detect semantically identical research questions.

## What was verified

On 2026-10-03, three fresh local chats each launched four children: two Luna, one Sol and one Astra. **One chief + three SET root leaders + 12 children = 16 agents overlapped for about 35 seconds.** Each fresh chat advertised 17 slots including its root; the directly demonstrated per-SET run was one root plus four children, five agents. This was a bounded idle-hold capacity experiment.

A separate exchange experiment transferred and integrated **11 facts** through shared JSON. Generated nonces, receipts, byte SHA-256 and source provenance were cross-checked, then independently checked by the chief. This verifies shared-file transfer on the local host; it does not guarantee automatic history sharing or file access across hosts.

**Task speedup and token savings were not measured. Actual Fast serving was not observed.** Results and limitations are recorded in the [validation record](examples/validation-record.json).

## Manual installation

The [current skill documentation](https://learn.chatgpt.com/docs/build-skills) lists `~/.agents/skills` for user skills and `.agents/skills` for repository skills. These commands preserve an existing copy outside the active discovery directory before replacement; backup is this installation procedure, not an installer guarantee.

<details>
<summary>Windows PowerShell</summary>

```powershell
$ErrorActionPreference = 'Stop'
git clone https://github.com/Kimhyuntae9665/codex-skill-6-1-sol-orch-3set-fast.git
if ($LASTEXITCODE -ne 0) { throw 'Git clone failed.' }
$skillTarget = Join-Path $HOME '.agents/skills/6-1-sol-orch-3set-fast'
if (Test-Path -LiteralPath $skillTarget) {
    $backupRoot = Join-Path $HOME '.agents/skill-backups'
    New-Item -ItemType Directory -Path $backupRoot -Force | Out-Null
    $skillBackup = Join-Path $backupRoot ('6-1-sol-orch-3set-fast-' + (Get-Date -Format 'yyyyMMdd-HHmmss-fff'))
    Move-Item -LiteralPath $skillTarget -Destination $skillBackup
    Write-Output ('Preserved original: ' + $skillBackup)
}
New-Item -ItemType Directory -Path (Split-Path $skillTarget) -Force | Out-Null
Copy-Item -LiteralPath './codex-skill-6-1-sol-orch-3set-fast/skills/6-1-sol-orch-3set-fast' -Destination $skillTarget -Recurse
```

</details>

<details>
<summary>macOS / Linux</summary>

```sh
(
  set -eu
  git clone https://github.com/Kimhyuntae9665/codex-skill-6-1-sol-orch-3set-fast.git
  skill_target="$HOME/.agents/skills/6-1-sol-orch-3set-fast"
  if [ -e "$skill_target" ]; then
    backup_root="$HOME/.agents/skill-backups"
    mkdir -p "$backup_root"
    skill_backup="$backup_root/6-1-sol-orch-3set-fast-$(date -u +%Y%m%dT%H%M%SZ)"
    test ! -e "$skill_backup"
    mv "$skill_target" "$skill_backup"
    printf 'Preserved original: %s\n' "$skill_backup"
  fi
  mkdir -p "$HOME/.agents/skills"
  cp -R ./codex-skill-6-1-sol-orch-3set-fast/skills/6-1-sol-orch-3set-fast "$skill_target"
)
```

</details>

## License and attribution

[Apache License 2.0](LICENSE). Derived from [6-1-sol-orch](https://github.com/Kimhyuntae9665/codex-skill-6-1-sol-orch), adding three parallel SETs, required Fast, dispatch checks and shared-evidence integration. See [NOTICE](NOTICE) for upstream attribution. This community project is not affiliated with or endorsed by OpenAI.

Official references: [Skills](https://learn.chatgpt.com/docs/build-skills) · [Speed](https://learn.chatgpt.com/docs/agent-configuration/speed) · [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) · [Configuration](https://learn.chatgpt.com/docs/config-file/config-reference)
