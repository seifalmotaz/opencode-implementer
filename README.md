# OpenCode Implementer (0.2.1)

A Codex plugin: Codex discusses, investigates, plans and reviews; OpenCode
Go writes code and runs automated checks. It asks for your Go model on first use
and keeps that choice for the current chat. An explicit exhausted-plan error
allows Codex to take over. Other failures are reported as blockers.

Supports parallel frontend/backend workers (independent CLI runs, disjoint edit
ownership, agreed interface), continued sessions for follow-up edits (explicit
`--session` reuse), and scoped shared-project permissions. License: MIT.

## Install

Local (this directory):

```sh
codex plugin marketplace add .
codex plugin add opencode-implementer@seif-local-plugins
```

Public GitHub marketplace (planned public repo `seifalmotaz/opencode-implementer`;
available after publication):

```sh
codex plugin marketplace add seifalmotaz/opencode-implementer
codex plugin add opencode-implementer@seif-local-plugins
```

If the marketplace name differs after publication, check
`codex plugin marketplace list` and substitute it after `@`. Restart Codex if
the skill does not appear. In a project chat, activate the plugin or its skill
and say:

> Use OpenCode Implementer for this chat. Investigate and plan with me; delegate
> implementation and automated testing to OpenCode Go. If its plan is exhausted,
> take over with Codex.

Prerequisites: authenticated OpenCode CLI on PATH, an OpenCode Go subscription,
and a Codex environment with shell execution. No orchestration server or new
dependency is required. Global OpenCode configuration is untouched; only a
narrowly scoped project-local config may be merged within the agreed project
scope.

## Parallel workers

Run one CLI process per role concurrently, each with disjoint file ownership
and a shared interface agreed up front. Serialize shared-file edits; integrate
only after both workers are idle. Launch with `&` and `wait` so both run at the
same time, keeping a separate event log per role:

```sh
opencode run --dir PROJECT --model opencode-go/CHOSEN_MODEL --agent build --format json "Backend brief: own backend/, implement cart totals in integer cents, agreed API: cart_total(items, discount)." > backend-events.log 2>&1 &
opencode run --dir PROJECT --model opencode-go/CHOSEN_MODEL --agent build --format json "Frontend brief: own frontend/, implement currency formatter, consumes cart_total cents, displays EGP." > frontend-events.log 2>&1 &
wait
```

Prefer starting both at the common project root with role scopes in the briefs.
For existing workers rooted in subfolders, merge a narrowly scoped
project-local `permission.external_directory` entry for the shared root and
`root/*` only:

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
with `opencode debug config` output filtered to the permissions section only
before retry; never dump the full config or credentials.

## Follow-up edits

Record role, project root, `--dir`, model, explicit session ID and last outcome
in the chat, and keep this per-role mapping after compaction by restating it.
Reuse the exact session for follow-ups with the same model and the original
working dir; never prompt the same session concurrently and never use implicit
`--continue`:

```sh
opencode run --dir PROJECT --model opencode-go/CHOSEN_MODEL --agent build --format json --session SESSION_ID "Follow-up brief: add validated discount clamped to zero, keep existing tests."
```

## Tested

Backend unit suite 7 -> 11 passing; frontend unit suite 5 -> 8 passing, then 10
passing (8 unit + 2 integration) after scoped permission retry. The 2
integration tests invoke the actual Python backend `cart_total` from Node via
`execFileSync` and format the result: 2499 cents displays EGP 24.99; excessive
discount displays EGP 0.00. Permission/tool error events override exit zero.

Not tested: HTTP service, browser flows, quota/plan exhaustion, fresh-chat
skill discovery, concurrent edits to shared files.

## Limits

This plugin supplies instructions, not a hard tool firewall or replacement Codex
engine. Activation and instruction following determine routing. It cannot ensure
every new chat uses it. OpenCode runs with its own permissions and sends task
context to its selected provider. A generic rate limit does not prove Go plan
exhaustion. No account quota endpoint or reset schedule is assumed. This package
bundles no local evidence, session IDs, paths, logs or credentials.

Built against installed OpenCode 1.18.35 CLI help. Live model execution was
verified above; billing exhaustion and desktop activation still require an
end-to-end check. Structural validation alone does not establish those
behaviors.
