# Agent-Reach evaluation — 2026-11-17

**Repo:** https://github.com/Panniantong/Agent-Reach — cloned to `~/workspace/tools/agent-reach/`
(commit `c70ae6da5d39bc90e09ad2ae0575ccc89f31e284`, 2026-11-08, branch `main`; package version **1.6.1**)
**Sent by:** the user, Telegram msg 565 (2026-11-17 ~01:51 EST) — "this one is for your x issues"
**Question:** does it fix our impaired X access (Xitter down since 2026-11-15; direct x.com reads unreliable from this VM)?

## VERDICT: PASS — for X, on this VM, as things stand

Agent-Reach does not solve our X problem today. It contains **no API route, no cookie-file route, and no unauthenticated route to X at all**: its Twitter channel drives a real logged-in browser session, and it stops at two hard gates on this VM — (1) no usable browser kernel, and (2) no X login, which by the tool's own design only the user can create, in person, in its browser window. Both gates are documented below with live evidence. Revival conditions are spelled out at the end; if the user ever completes an X login in the tool's dedicated browser (ideally a burner account), the channel should be re-tested before any further verdict.

Side observation (out of scope for this eval, noted for completeness): the tool's no-login channels work fine from this VM — `agent-reach web search` (Exa backend) returned full results in ~4.5 s, and GitHub/YouTube/Bilibili/V2EX channels need no login. They don't fix X, so they don't change the verdict.

## What it is

- **Stack:** Python ≥3.10 CLI (`agent-reach`), MIT license. One CLI, JSON output, one "channel" per platform (GitHub, YouTube, Bilibili, V2EX, web by default; Xiaohongshu, Reddit, LinkedIn, Xueqiu, BOSS optional; **Twitter, Facebook, Instagram marked "experimental"**).
- **Design:** each channel action has an ordered list of upstream tools; Agent Reach installs/pins them and normalizes output. State lives in `~/.agent-reach/`. Read-only by design (no posting/commenting/liking).
- **Install method used here:** deliberately NOT the repo docs' remote-installer path (a release-zip download / shell installer script). Installed from the local clone into an isolated venv: `python3 -m venv .venv && .venv/bin/pip install .` inside `~/workspace/tools/agent-reach/`. Verified: `agent-reach version` → `{"ok": true, "result": {"version": "1.6.1", "install_method": "other"}}`. Repo unit tests run: `tests/test_channels.py` + `tests/test_channel_contracts.py` → **13 passed**. (PyPI carries an unrelated package also named `agent-reach` — do not install that one; the repo itself warns about this.)

## How it reaches X (the important part)

From `agent_reach/channels/twitter.py` and `agent_reach/backends/opencli.py` (read directly):

- The Twitter channel's **only** backend is **OpenCLI** (`@jackwener/opencli`, npm), which drives Chrome via a browser-bridge extension + local daemon, in a single Agent-Reach-owned "dedicated browser" profile (`~/.agent-reach/browser/profile`).
- Actions: `search`, `profile`, `tweets`, `thread` — all OpenCLI-only. Only `search` has a fallback: a public-web search scoped to `site:x.com` (Exa/Jina), which is search-engine results about X pages, not X data.
- Prerequisites declared in code: `node`, `chrome`. Node is present here (v24.22.1); OpenCLI itself installed fine (`~/.agent-reach/tools/npm-global/bin/opencli`).
- **Auth:** a live, logged-in x.com session inside that dedicated browser. No API key option, no cookie import by hand, no credential config. The tool **never logs in for you and never asks for a password** — its login hint, verbatim from the source: *"Ask the user to log in to x.com in the Agent Reach dedicated browser. Never log in on their behalf."* `agent-reach login twitter` opens a visible browser window for the user to log in personally. It can also copy a site's cookies one time from the user's own Chrome **if** that Chrome has the OpenCLI bridge extension connected — not the case on this VM (no user Chrome here). The docs recommend a burner/secondary account, since X may restrict accounts used for automated access.

## Live tests (2026-11-17, from this VM, all read-only)

| Test | Command | Result |
|---|---|---|
| Web channel sanity | `agent-reach web search "agent reach" --limit 1` | ✅ OK — Exa backend, full text result, 4,450 ms |
| Twitter search (public-web fallback) | `agent-reach twitter search "xiaoying_eth" --limit 2` | ❌ No output at all within 120 s (killed by timeout) — appears to stall in browser provisioning before the fallback can answer |
| Tweet thread — @xiaoying_eth `2122233771764449497` | `agent-reach twitter thread 2122233771764449497` | ❌ `UPSTREAM_BROKEN` — "the Agent Reach browser did not open: browser closed" (8.2 s) |
| Tweet thread — @xiaoying_eth `2122233774251618732` | same | ❌ `UPSTREAM_BROKEN` (backend then auto-paused ~114 s) |
| Tweet thread — @xiaoying_eth `2122233776361410684` | same | ❌ `UPSTREAM_BROKEN`, 0 items |
| Tweet — @shinshin86 `2122281474301030886` | same | ❌ `UPSTREAM_BROKEN`, 0 items |
| Profile — @xiaoying_eth | `agent-reach twitter profile xiaoying_eth` | ❌ `UPSTREAM_BROKEN` — "browser did not open: browser closed" (7.0 s) |
| Timeline — @gossip_goblin | `agent-reach twitter tweets gossip_goblin --limit 3` | ❌ `UPSTREAM_BROKEN` — same (5.6 s) |

**Zero X content of any kind was retrieved: no post text, no expanded links, no media, no replies.** No 429s were hit — the requests never reached X.

## The two gates, evidenced

**Gate 1 — no working browser kernel on this VM.**
- `agent-reach add twitter` → `UPSTREAM_BROKEN`: *"CloakBrowser could not be installed: cloakbrowser exited 1: ModuleNotFoundError: No module named 'playwright._impl._js_handle'"* — the preferred CloakBrowser kernel's installer is broken in this environment (its bundled Playwright is internally inconsistent). `agent-reach browser setup` fails the same way.
- Fallback is a system Chrome: Agent Reach looks for `google-chrome` / `google-chrome-stable` / `chromium` on PATH. The VM had none. The only Chromium present, `/opt/meta-chromium/chrome` (the Muse browser build), was symlinked in as `chromium` and accepted as the backend (extension v1.0.27 prepared) — but it **refuses to start standalone**: `Hatch WebGL domain policy is required for browser startup`, and under Agent Reach: *"the Agent Reach browser did not open: browser closed"*. It is a policy-locked build, not a general-purpose Chrome.

**Gate 2 — no X login, and none can be created agent-side.**
Even with a working browser, every Twitter action needs a logged-in x.com session in the dedicated profile. None exists on this VM; the tool takes no password/API key/cookie file, and its login flow is a visible window for the user personally. Per the eval rules, this is a stop gate: no credentials were invented, borrowed, or reused.

## Failure modes (for future reference)

- Browser-kernel failure surfaces as `UPSTREAM_BROKEN` "browser did not open: browser closed" on every browser-channel action, and the backend auto-pauses (~2 min backoff) after a failure.
- First-ever Twitter call can hang silently for minutes (provisioning attempts) instead of erroring — always run it with an external timeout.
- The VM's egress proxy is flaky for package downloads (PyPI/npm wheels needed repeated retries during this install) — installs here are slow but do complete.
- X-side risks if it ever runs: channel is self-declared "experimental" (platform anti-automation is stricter; may break at any time); account-restriction risk is real enough that the docs recommend a burner account; built-in etiquette is max 2 concurrent reads per site and ≥10 s between same-site searches.

## Revival conditions (what would change the verdict)

1. A working browser for the dedicated profile: either CloakBrowser's installer fixed upstream (or its Playwright env repaired), or a real Chrome/Chromium installed on the VM that Agent Reach can launch (not the policy-locked Muse build).
2. **The user personally logs in to x.com** in the Agent Reach dedicated browser (`agent-reach login twitter`) — ideally a burner/secondary account, per the tool's own safety guidance and the account-risk note above.
3. Then re-run the same live-test table (threads/profile/timeline above) before adopting; if those return full text + expanded links, the verdict becomes ADOPT-PARTIAL/ADOPT and a usage section for the creator-study workflow gets written then.

Until both conditions hold, creator studies keep using the standing route: cross-platform triangulation (YouTube/objkt/other profiles) with X findings marked lead-level, per the 2026-11-15 user correction.

## Housekeeping

- Left installed (harmless, disk ~300 MB): `~/workspace/tools/agent-reach/` (clone + venv) and `~/.agent-reach/` (OpenCLI + state). The `/usr/local/bin/chromium` symlink to the policy-locked build was left in place; it is inert (that binary won't start outside its harness) — remove it if a real Chromium is ever installed to avoid confusion.
- No credentials were used, printed, or stored. No X account actions of any kind were taken. No SOURCES.md workflow note was added — per the eval plan that note is written only on ADOPT/ADOPT-PARTIAL; this file is the record instead.
