# Runtime — complete parallel hierarchy only

## Required topology and runtime evidence

Standard launch: chief 1 + leaders 3 + Luna children 6 + Sol workers 3 =
**13 total threads / 12 spawned threads**. With three optional Astra reviewers
coexisting, it is 16 total / 15 spawned. The skill imposes no lower concurrency
cap and never limits ready work to one SET at a time.

Inspect effective capacity, existing agents, the counting rule and
chief → leader → child nesting support before launch. Normalize evidence to
`capacity_total`, including the chief. A configured number is a request, not
proof of runtime capacity. Some hosts count open idle/finished threads too.

There is **no reduced-capacity execution table**. If fewer than 13 total threads
are available, nesting is unavailable, or required models/Fast cannot run,
report that this hierarchy cannot start. Do not choose sequential/staggered/
chief-only operation or a flattened topology on the user's behalf. Record
partial failures honestly; do not create unrequested chats or CLI processes.
For explicitly requested three-session deployment, follow
[three-session.md](three-session.md). Each SET needs four total local slots
for its leader and basic children, or five with its reviewer. This is independent
of the chief's old chat limit. Never substitute aggregate slots for a SET's
actual local capacity.

Calls need not be literally simultaneous. Dispatch them without completion
waits between SETs so all three teams overlap. Confirm with the live tree,
child records and timestamps. Thirteen planned agents do not prove 13 active
agents, nor do agents launched in unrelated waves.

## Fast for every role

`service_tier = "fast"` is the documented Codex Fast setting; request value
`priority` is also supported. Inspect effective thread overrides and parent
inheritance. Reasoning effort is independent of the tier.
Require `[features].fast_mode = true` explicitly for this workflow.
Check every separate SET root's global/project/profile/session settings before
child dispatch. New chats are independent roots; the chief's current tier is
not proof of their tier. Child model overrides must preserve the root's Fast
route; inspect selected custom-agent files for tier overrides where applicable.

Use explicit tier options only if the tool schema supports them. Where
collaboration exposes model/effort only, use verified configured inheritance;
never invent `service_tier`, `fast` or `mode` spawn fields. A prompt cannot
enable Fast. Known unavailable Fast is a blocker; unknown actual serving tier
must be disclosed rather than invented.

Record each agent separately, for example:

```json
{"agent":"set1-worker","model":"gpt-6.1-sol","fast_required":true,
 "fast_request":"inherited configured priority; host advertises priority",
 "observed_tier":null}
```

The host selects the chief model/effort; a skill cannot change the active
chief. This public contract requires Sol 6.1/medium for the chief and every
SET leader. Report a chief model/effort mismatch before dispatch and use a
supported host selection/new runtime. No installation-specific exception or
past user's approval transfers to another host owner.
All basic roles require the same Fast policy.

## Host configuration for the complete topology

The supported setting counts spawned threads EXCLUDING the primary:

```toml
service_tier = "priority"

[features]
fast_mode = true

[agents]
enabled = true
max_concurrent_threads_per_session = 16
```

This user-global default allows up to 16 spawned agents plus the primary
(17 total). The three-set topology uses 12 basic spawned agents, or 15 with
three optional reviewers; the remaining capacity is headroom, not a required
extra role. This provides room for the full topology and reviewers. It is
not a skill-side dispatch throttle or proof of unlimited capacity. Preserve
existing higher values. Do not invent zero, negative, infinity or undocumented
depth settings as an unlimited mode.

Modify host configuration only when authorized and preserve unrelated keys.
Changes may need a new runtime/app restart; already-running chats can retain
earlier hard limits. Recheck tool-advertised capacity after reload. Do not
interrupt or restart other active chats automatically.

Read the applicable global/project/profile/session settings. The sample
above is an opt-in configuration, not permission to edit or automatically
restore global defaults. Any host change requires that owner's explicit
authorization; preserve larger values and unrelated keys and validate the TOML.
Inspect project/profile/session overrides where applicable and report any
lower effective limit. Do not substitute the configured 17 total for an
actually advertised lower runtime limit.

## Official references checked 2026-10-03

- [Configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference)
- [Subagents and inheritance](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Fast speed setting](https://learn.chatgpt.com/docs/agent-configuration/speed)

Configuration/documentation does not establish a running session's actual
serving tier or effective capacity.
