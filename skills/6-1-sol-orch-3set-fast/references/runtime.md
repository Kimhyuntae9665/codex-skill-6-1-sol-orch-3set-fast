# Runtime and scheduling

Read before dispatch and recheck each run. Skill text is not host configuration.

## Fast for every role

`service_tier = "fast"` is the documented Codex setting, mapped to request
value `priority`. Supported existing `priority` settings may already request
Fast. Inspect thread overrides, not just config defaults, and supported tiers
for the requested models. Reasoning effort is independent of speed tier.

Apply an explicit Fast option when the host exposes one. When the collaboration
schema has only model/effort fields, do not invent a `service_tier`, `fast`, or
`mode` argument. Use supported Fast configuration/inheritance and record
evidence. Saying "Fast" in a prompt cannot enable it.

Record each agent separately, for example:

```json
{"agent":"set1-worker","model":"gpt-6.1-sol","fast_required":true,
 "fast_request":"inherited configured priority; host advertises priority",
 "observed_tier":null}
```

`null` means unobservable, not Standard and not verified Fast. A known downgrade
or unsupported Fast role must be reported and further work held until a
supported Fast route exists; no silent Standard fallback. Continue other
independent available work. Root model/effort are selected in the host; report
a mismatch instead of claiming the pictured topology ran. The active tool
schema is authoritative for parameters/model IDs.

## Capacity

Normalize to `C`: total usable simultaneous/open threads INCLUDING the chief.
Account for existing threads and the host's counting rule. Modern Codex's
`agents.max_concurrent_threads_per_session` counts spawned threads EXCLUDING
the primary; its `max_threads` legacy alias has the same meaning in current
documentation. The host may enforce a lower cap than a config value.

| Total C | Execution mode |
| --- | --- |
| 13+ | Chief + 3 leaders + up to 3 workers each; only useful, ready roles. |
| 7–12 | Three leaders; bounded worker grants with at least one worker slot per active set. |
| 3–6 | Stagger sets, keeping one worker slot per active leader. At C=4: chief + one leader + at most two children. |
| 2 | Chief + one leader who works directly; not the full pictured hierarchy. |
| 1/no delegation | Chief-only reduced execution; retain decomposition and report it. |

Full basic fan-out uses 13 total. Three simultaneous additional reviewers would
use 16; normally reuse/release finished worker capacity before review.
Each SET has at most one explorer, one researcher and one worker live. The
13-thread figure is a ceiling for that composition, not permission to turn
all nine worker slots into Luna researchers. Leave unneeded roles unused.

The chief issues each leader a global slot grant: maximum children under the
host's counting rule, roles and release condition. Before each spawn, confirm
the grant. Only regrant after actual availability is confirmed. Finishing,
sleeping or interrupting may not close a thread. Use an actual host close tool
if provided; do not invent one. If none exists, reuse permitted agents/roles
or work within remaining capacity and disclose the limitation.

The exact tree needs chief → leader → child nesting support. If the host
rejects that depth, the chief can host workers directly under SET contracts,
but must announce the flattened tree. Do not claim the exact hierarchy or
repeatedly retry a known rejection.

## Optional host fragment; not auto-applied

This fragment expresses Fast and up to 15 spawned threads (16 total) on a
supported current Codex host. These settings belong in host config, NOT skill
`agents/openai.yaml`. Check host support and existing sections before an
authorized config change; never overwrite unrelated settings or add obsolete
depth keys from old examples.

```toml
service_tier = "fast"

[features]
fast_mode = true

[agents]
enabled = true
max_concurrent_threads_per_session = 15
```

This does not override a session's hard limit. Verify effective capacity after
any host restart/new session. Creating this skill does not apply this optional
global config change.

## Official sources checked 2026-10-03

- [Speed and supported Fast models](https://learn.chatgpt.com/docs/agent-configuration/speed)
- [Configuration: service tier and limits](https://learn.chatgpt.com/docs/config-file/config-reference)
- [Subagents and configuration inheritance](https://learn.chatgpt.com/docs/agent-configuration/subagents)

Documentation support alone does not establish this account's entitlement or
the serving tier of a particular request. Check runtime evidence.
