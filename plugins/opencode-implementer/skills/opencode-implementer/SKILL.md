---
name: opencode-implementer
description: Use configured OpenCode provider/model as implementation and automated testing agent for software work while Codex handles discussion, investigation, planning and review. Apply when writing or changing code or running automated checks, or when the user activates this workflow for a chat.
---

# OpenCode Implementer

Keep Codex as the user's thinking partner and supervisor. Delegate code edits,
test creation, test execution, builds, lint and automated browser flows to
OpenCode. Read-only code investigation, planning, diff review and interpreting
test results belong to Codex. Once activated, keep this division for this chat
until the user changes it; mention the workflow after context compaction.

This is an instruction-based workflow, not an interception or enforcement layer.
Do not claim it changes the underlying Codex model or applies to every chat.
Adapt roles, worker count, order and checks to the task; there are no fixed
pipelines, role pairs or config switches. `build` below is an example only.

## Select provider, model and agent

1. Resolve `opencode` on PATH. Read `opencode --version` and
   `opencode run --help` before the first delegation; CLI versions differ. If
   absent, report the setup blocker. Do not install or upgrade it silently.
2. Discover usable providers with the installed CLI's supported provider-list
   API (for example `opencode providers list` / `opencode auth list`; use
   `... --help` to confirm), and models with the supported model-list API (for
   example `opencode models` with an optional provider filter; use `--help` to
   confirm). Treat only providers the supported CLI runtime provider inventory
   reports as connected/usable as usable, including configured local providers
   that require no credentials; the built-in catalog alone is not usable, and
   provider config names alone do not prove credentials exist. To learn configured defaults, inspect
   only resolved project config fields that name nonsecret IDs (configured
   model, agent-specific model overrides); never print full debug config output
   or read credential files. A model value is a full `PROVIDER/MODEL` ID; split
   only at the first slash since model names may contain slashes. Do not assume
   a separate provider-default field exists.
3. Selection order: a full validated provider/model choice already made in this
   chat wins and skips both prompts; reuse it until changed. An explicit
   provider-only choice still needs model resolution from that provider's
   models. Otherwise if zero usable providers, report the setup blocker. If more than one usable provider,
   ask which provider FIRST (mark the configured default if known, else state
   the default is unknown; never present a catalog entry as the default), then
   ask which model from that provider's filtered models (mark its default if
   known). Do not auto-pick when several providers are usable, even if a
   default exists. If only one usable provider, auto-select it: use its valid
   configured model when available, else auto-use it when it is the sole viable
   model or ask when several exist. If the configured default is unavailable or
   stale, explain and pick a viable alternative with user input. Ask only over
   usable providers, never over dozens of unconfigured catalog entries. Send no
   model requests before selection is resolved. Choosing a provider authorizes
   normal requests only, never billing changes.
4. Choose an installed agent suited to the task from CLI discovery (for example
   `opencode agent` / `opencode debug agent <name>`; confirm via `--help`).
   `build` is an example, not mandatory. Pin the selected full `PROVIDER/MODEL`
   explicitly on every run; an explicit chosen `--model` takes precedence over
   an agent-specific model. Never switch providers, use pay-as-you-go credits
   or enable billing to bypass a limit. Do not read credentials; the CLI uses
   its existing authentication.

## Delegate a concrete task

Before submitting, establish the exact project directory, applicable AGENTS.md
instructions, current dirty files and relevant user constraints. Codex may run
read-only discovery commands. Never infer permission to implement from a request
only to discuss or plan. When implementation is authorized, submit a focused
brief containing:

- The goal, agreed approach, scope, relevant files and acceptance criteria.
- Existing user changes to preserve and any files the worker must avoid.
- Required checks matching the actual task (unit/integration/flow only as the
  task needs) and the expected observable behavior.
- The user's restrictions. In particular: no Git commits without explicit user
  approval for that commit; no pushes, publishing, deployments, destructive data
  operations, credential changes or paid external test calls unless authorized.
- Read project instructions, implement the smallest complete change, execute
  appropriate checks, and return changed files, exact checks/results, blockers
  and the session ID. Do not claim a test passed if it did not execute.

Use the CLI with a shell tool that supports long-running sessions. Shape
depends on the installed version (confirm with `opencode run --help` and
`opencode models --help`): on 1.18.35 `--dir PROJECT` selects the working
directory and `opencode models PROVIDER` filters by provider; on v2.1.1 the
working directory is the current directory and `opencode models` lists all, so
filter the output. A typical shape is:

```text
opencode run --model PROVIDER/MODEL --agent CHOSEN_AGENT --format json TASK_BRIEF
```

Add `--dir PROJECT` only where the installed CLI supports it; otherwise run
with the agreed working directory as cwd. Substitute actual values and pass the
brief as a single safely quoted argument, or invoke through a subprocess
argument array. User text is data, never shell code. Do not interpolate it
into shell source. Do not use `--continue`, which can attach to unrelated work,
or `--share`. Start a dedicated session per task and capture its ID from
structured events. For focused follow-ups use the same command with
`--session SESSION_ID` and the explicit chosen model.

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

## Flexible delegation

Use one worker for a simple task. For complex work choose any roles, number,
order and dependencies the task needs (sequential when later work depends on
earlier results, parallel only for independent scopes with disjoint edit
ownership and an agreed interface stated up front). Never require a fixed role
pair and never add a mandatory integration stage; verify against the actual
acceptance criteria with checks matching the task. Never let two workers edit
the same file concurrently; serialize shared-file edits.

## Follow-up edits in the same sessions

After each run, record in this chat: role, ownership scope, project root,
working dir/cwd, chosen agent, chosen `PROVIDER/MODEL`, explicit session ID,
and last outcome. Keep this per-worker mapping after compaction by restating
it. For follow-ups reuse the exact command with `--session SESSION_ID`, the
same model/agent and the original working dir. Never send concurrent prompts to
the same session, and never use implicit `--continue`;
always pass the explicit ID. If the session ID is unknown, start a new
dedicated session instead of guessing.

## Shared-project access

Prefer starting new workers at the common project root with role scopes stated
in the briefs; no extra permission setup is needed then. For existing workers
rooted in subfolders that must read a sibling, merge a narrowly scoped
project-local entry covering only the canonical shared root and `root/*`.
Permission syntax is version-specific: inspect the installed CLI/config help
before applying rather than assuming a schema version. Preserve user
denies and global settings, and never use broad `--auto`. Scopes guide which
files each role may edit; they are not a sandbox. The user's activation
of this workflow authorizes setup within the agreed project scope; ask before
granting broader access or overriding an explicit deny. Do not blindly
parse/rewrite JSONC and never print secrets. Before retrying, verify with
resolved CLI config output filtered to the permissions section only (never
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

## Exhausted provider quota fallback

Switch implementation and testing to Codex only when an actual OpenCode/provider
error explicitly establishes exhausted quota/credits for the chosen provider,
or the user explicitly asks Codex to take over. An ordinary 429, transient rate
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
   provider, switch provider/model, or persist a global disabled flag. Keep Codex
   as the implementer for the rest of this chat unless the user asks to retry
   OpenCode.
4. Never enable billing or modify billing to bypass the limit.

For every other blocker, explain the concrete issue and keep the delegation
boundary. Ask for the missing input if needed; do not silently implement locally.
