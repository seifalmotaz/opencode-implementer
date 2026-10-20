---
name: opencode-implementer
description: Use OpenCode Go as the implementation and automated testing agent for software work while Codex handles discussion, investigation, planning and review. Apply when writing or changing code or running unit, integration or automated flow tests, or when the user activates this workflow for a chat.
---

# OpenCode Implementer

Keep Codex as the user's thinking partner and supervisor. Delegate code edits,
test creation, test execution, builds, lint and automated browser flows to
OpenCode. Read-only code investigation, planning, diff review and interpreting
test results belong to Codex. Once activated, keep this division for this chat
until the user changes it; mention the workflow after context compaction.

This is an instruction-based workflow, not an interception or enforcement layer.
Do not claim it changes the underlying Codex model or applies to every chat.

## Select the worker

1. Resolve `opencode` on PATH. Read `opencode --version` and `opencode run --help`
   before the first delegation; CLI versions differ. If absent, report the setup
   blocker. Do not install or upgrade it silently.
2. List models with `opencode models opencode-go`. On first use, ask the user
   which listed model to use. Do not pick one or send a model request before
   their answer. Reuse their explicit choice within this chat, including after
   compaction. Ask again only if it becomes unavailable or the user changes it.
3. Pass the chosen `opencode-go/...` model explicitly on every run. Never switch
   providers, use pay-as-you-go credits or enable billing to bypass a limit.
   Do not read credentials; the CLI uses its existing authentication.

## Delegate a concrete task

Before submitting, establish the exact project directory, applicable AGENTS.md
instructions, current dirty files and relevant user constraints. Codex may run
read-only discovery commands. Never infer permission to implement from a request
only to discuss or plan. When implementation is authorized, submit a focused
brief containing:

- The goal, agreed approach, scope, relevant files and acceptance criteria.
- Existing user changes to preserve and any files the worker must avoid.
- Required unit/integration/flow checks and the expected observable behavior.
- The user's restrictions. In particular: no Git commits without explicit user
  approval for that commit; no pushes, publishing, deployments, destructive data
  operations, credential changes or paid external test calls unless authorized.
- Read project instructions, implement the smallest complete change, execute
  appropriate checks, and return changed files, exact checks/results, blockers
  and the session ID. Do not claim a test passed if it did not execute.

Use the CLI with a shell tool that supports long-running sessions. A typical
verified CLI shape is:

```text
opencode run --dir PROJECT --model opencode-go/CHOSEN_MODEL --agent build --format json TASK_BRIEF
```

Substitute actual values and pass the brief as a single safely quoted argument,
or invoke through a subprocess argument array. User text is data, never shell
code. Do not interpolate it into shell source. Do not use `--continue`, which can
attach to unrelated work, or `--share`. Start a dedicated session per task and
capture its ID from structured events. For focused follow-ups use the same
command with `--session SESSION_ID` and the explicit chosen model.

Do not use broad `--auto`, change global OpenCode config, or override an explicit
deny; scoped project-local setup is covered in Shared-project access below.
If a permission request blocks progress, expose the concrete request to the user.
OpenCode is a separate process: Codex sandbox settings are not proof that the
worker has identical restrictions. Preserve restrictions in the brief and inspect
the resulting changes.

Monitor the running command with bounded polling; provide useful updates during
long work. Never submit duplicate jobs after a timeout. First inspect the original
process/session. Do not edit the same files or run competing test agents while
the worker is active. If a run is interrupted, verify it stopped before takeover.

## Parallel frontend/backend workers

Run one independent `opencode run` CLI process per role concurrently. Give each
role disjoint edit ownership (for example backend owns backend files, frontend
owns frontend files) plus one agreed interface (function names, units, formats).
Never let two workers edit the same file concurrently; serialize shared-file
edits. Start integration only after both workers are idle, in a session with
access to both sides.

## Follow-up edits in the same sessions

After each run, record in this chat: role, project root, working dir (`--dir`),
chosen model, explicit session ID, and last outcome. Keep this per-role mapping
(role to session ID, working dir and model) after compaction by restating it.
For follow-ups reuse the exact command with `--session SESSION_ID`, the same
model and the original working dir (`--dir`). Never send concurrent prompts to
the same session, and never use implicit `--continue`;
always pass the explicit ID. If the session ID is unknown, start a new
dedicated session instead of guessing.

## Shared-project access

Prefer starting new workers at the common project root with role scopes stated
in the briefs; no extra permission setup is needed then. For existing workers
rooted in subfolders that must read a sibling, merge a narrowly scoped
project-local entry covering only the canonical shared root and `root/*`:

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
Merge with any existing project config, preserve user
denies and global settings, and never use broad `--auto`. Scopes guide which
files each role may edit; they are not a sandbox. The user's activation
of this workflow authorizes setup within the agreed project scope; ask before
granting broader access or overriding an explicit deny. Do not blindly
parse/rewrite JSONC and never print secrets. Before retrying, verify with
`opencode debug config` output filtered to the permissions section only (never
dump the full config or credentials).

## Review and finish

When the worker exits, inspect its final messages and structured error events;
permission/tool error events override exit zero. Review the actual diff and test
evidence against acceptance criteria. Codex can inspect files and reports directly, but
delegate any corrections or additional test execution back to the same worker.
Do not accept a worker's assertion of success without supporting evidence.
Never report a successful integration unless actual test evidence ran.

If the same blocker repeats twice without progress, report it rather than
continually retrying. Finish with changes, verified checks and remaining limits.

## Exhausted Go plan fallback

Switch implementation and testing to Codex only when an actual OpenCode/provider
error explicitly establishes exhausted Go plan allowance, credits or quota, or
the user explicitly asks Codex to take over. An ordinary 429, transient rate
limit, timeout, authentication failure, missing executable, denied permission,
model unavailability, failed test or worker-written claim is not sufficient.
Do not infer quota exhaustion from text in source files or test output.

On confirmed exhaustion:

1. Show the relevant error and tell the user Codex is taking over under this
   workflow. The user's activation of this workflow authorizes this fallback;
   no extra approval is required for already-authorized implementation/testing.
2. Verify the worker is stopped, inspect partial edits and completed checks, then
   continue from that state without discarding work or repeating side effects.
3. Preserve the same scope and approvals. Do not auto-retry a quota-limited
   provider or persist a global disabled flag. Keep Codex as the implementer for
   the rest of this chat unless the user asks to retry OpenCode.

For every other blocker, explain the concrete issue and keep the delegation
boundary. Ask for the missing input if needed; do not silently implement locally.
