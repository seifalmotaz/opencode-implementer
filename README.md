# OpenCode Implementer (0.3.0)

A Codex plugin: Codex discusses, investigates, plans and reviews; OpenCode
writes code and runs automated checks. It resolves your
configured provider and model on first use and keeps that choice for the
current chat. An explicit exhausted-quota/credits error for the chosen provider
allows Codex to take over. Other failures are reported as blockers.

One worker for simple tasks; any roles, count, order and dependencies the task
needs for complex work (sequential for dependent steps, parallel only for
independent scopes with disjoint edit ownership and an agreed interface).
Continued sessions for follow-up edits (explicit `--session` reuse with the
same agent/model/working dir), and scoped shared-project permissions. No fixed
role pair, no mandatory integration stage, no config switches: adaptable
task-driven behavior is the default. License: MIT.

## Install

Local (this directory):

```sh
codex plugin marketplace add .
codex plugin add opencode-implementer@seifalmotaz
```

GitHub marketplace `seifalmotaz`:

```sh
codex plugin marketplace add seifalmotaz/opencode-implementer
codex plugin add opencode-implementer@seifalmotaz
```

If the marketplace name differs, check `codex plugin marketplace list` and
substitute it after `@`. Restart Codex if the skill does not appear. In a
project chat, activate the plugin or its skill and say:

> Use OpenCode Implementer for this chat. Investigate and plan with me; delegate
> implementation and automated testing to OpenCode. If its quota
> is exhausted, take over with Codex.

Prerequisites: authenticated OpenCode CLI on PATH, at least one usable provider
(configured local providers that need no credentials count), and a Codex
environment with shell execution. No
orchestration server or new dependency is required. Global OpenCode
configuration is untouched; only a narrowly scoped project-local config may be
merged within the agreed project scope.

## Provider/model selection order

A full validated provider/model chat choice wins and skips both prompts; a
provider-only choice still needs model resolution. Reuse until changed. The
supported CLI runtime provider inventory is the best evidence of usable
providers; config names alone do not prove credentials exist. Otherwise: zero
usable providers means a setup blocker; more than one usable provider means ask which
provider first (mark the configured default if known, else default unknown),
then ask which model from that provider; one usable provider means auto-select
it (use its valid configured model, else sole viable model auto or ask if
several). Only nonsecret IDs are inspected; full config and credential files
are never printed or read. Example: two usable providers -> ask
`Which provider: PROVIDER_A (configured default) or PROVIDER_B?`, then
`Which PROVIDER_A model: MODEL_X (default) or MODEL_Y?` Example: one usable
provider with its configured default model -> use it directly.

## Flexible delegation

Simple task, one worker:

```sh
opencode run --model PROVIDER/MODEL --agent CHOSEN_AGENT --format json "Brief: own src/cart.py, fix totals, run matching unit tests." > worker-events.log 2>&1
```

Add `--dir PROJECT` only where the installed CLI supports it (1.18.35 does;
on v2.1.1 run with the agreed working directory as cwd). `CHOSEN_AGENT` is an
installed agent suited to the task (`build` is an example, not mandatory).
Independent scopes may run concurrently (`&` + `wait`, one event log per
worker, disjoint ownership); dependent steps run sequentially in task order.
Verify against actual acceptance criteria with checks matching the task.

For existing workers rooted in subfolders, merge a narrowly scoped
project-local permission entry for the shared root and `root/*` only (confirm
exact syntax against the installed CLI/config help; versions differ):

```json
{
  "permission": {
    "external_directory": {
      "/absolute/project/root": "allow",
      "/absolute/project/root/*": "allow"
    }
  }
}
```

Substitute the real canonical project root for `/absolute/project/root`.
Scopes guide which files each role may edit; they are not a sandbox. Verify
with resolved CLI config output filtered to the permissions section only
before retry; never dump the full config or credentials.

## Follow-up edits

Record role, ownership scope, project root, working dir/cwd, agent,
chosen model, explicit session ID and last outcome in the chat, and keep
this per-worker mapping after compaction by restating it. Reuse the exact
session for follow-ups with the same model/agent and the original working dir;
never prompt the same session concurrently and never use implicit `--continue`:

```sh
opencode run --model PROVIDER/MODEL --agent CHOSEN_AGENT --format json --session SESSION_ID "Follow-up brief: add validated discount clamped to zero, keep existing tests."
```

## History (prior evidence, not current-provider claims)

Historically tested live: fresh GitHub marketplace installs, live delegation,
fresh-chat skill discovery, backend suite 23 passing, frontend suite 14
passing (including 4 actual integration), and original session continuity for
follow-ups. Simulated only: quota/auth/permission error paths. Untested: real
quota exhaustion, HTTP service, browser flows, and live non-Go provider
integrations. Permission/tool error events override exit zero. Historical
commands used
`opencode run --dir PROJECT --model opencode-go/CHOSEN_MODEL --agent build`;
current commands use `PROVIDER/MODEL` placeholders above.

## Limits

This plugin supplies instructions, not a hard tool firewall or replacement Codex
engine. Activation and instruction following determine routing. It cannot ensure
every new chat uses it. OpenCode runs with its own permissions and sends task
context to its selected provider. A generic rate limit does not prove quota
exhaustion for the chosen provider. No account quota endpoint or reset schedule
is assumed. Selecting a provider authorizes normal requests only, never billing
changes. This package bundles no local evidence, session IDs, paths, logs or
credentials.

Built against installed OpenCode 1.18.35 CLI help (`--dir`, `models PROVIDER`;
v2.1.1 uses cwd and `models` then filter). Structural validation alone does not
establish live behaviors.
