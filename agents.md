# Agents Guide

Quick orientation for AI agents working in this repo.

## What this is

A Home Assistant **app** (formerly add-on) called **Code Editor**: a
browser-based [code-server](https://github.com/coder/code-server) instance
exposed through Home Assistant's ingress, scoped to editing `/config`.

- Repo: `gollyjer/home-assistant-code-editor`
- Slug: `code_editor` (was `vscode` upstream)
- Ingress port: `1337` (nginx) → code-server bound to localhost
- Distribution: **local-build** via HA Supervisor. No prebuilt images are
  published; users build on their device when they install/update.

## Fork lineage

Forked from `hassio-addons/addon-vscode` (Studio Code Server, by Franck
Nijhof / HA Community Add-ons). Baseline fork commit:
`776ef9119524ff489345a6a60e13333264e67b1c`.

Major rebrand + modernization landed in `1.118.0`. See
`code-editor/CHANGELOG.md` for the full reshape (slug change, new layout,
trimmed mounts, nginx ingress proxy, extension list overhaul, etc.).

## Repo layout

```
repository.yaml              # HA repo metadata (points Supervisor at code-editor/)
README.md                    # User-facing repo readme
CHANGELOG.md                 # Repo-level changelog
LICENSE.md
assets/                      # screenshots etc.
code-editor/                 # the app itself (was vscode/ upstream)
  config.yaml                # HA app manifest (version, slug, ingress, schema)
  Dockerfile                 # builds the image
  vscode.extensions          # pinned VSIX list: vendor.slug#version, one per line
  patch-ha-schemas.py        # build-time JSON-schema patcher (see below)
  vendor/                    # vendored VSIX files preferred over marketplace download
  requirements.txt           # Python deps installed into image (e.g. ESPHome)
  apparmor.txt               # AppArmor profile
  translations/en.yaml       # app metadata & options
  rootfs/                    # overlaid into / at build (s6-overlay init, etc.)
  DOCS.md                    # user-facing config docs
  CHANGELOG.md               # app changelog (this is the one HA shows)
  README.md
  icon.png / logo.png
```

## Versioning

4-component scheme: **`{code-server major}.{code-server minor}.{code-server patch}.{our patch}`**.

- Currently `1.118.0.2` — tracks code-server `v4.118.0`, our patch counter `2`.
- Bump the trailing `.N` for our-only changes (schema patch, extension
  add/remove, default tweak). Reset to `.0` when code-server upstream moves
  (e.g. next release is `1.119.0.0`).
- Bump it in `code-editor/config.yaml` **and** add a `code-editor/CHANGELOG.md`
  entry. HA Supervisor reads version from `config.yaml`.

## Build pipeline (Dockerfile)

Builds on `ghcr.io/hassio-addons/debian-base:9.3.0` (pinned in Dockerfile,
no `build.yaml` anymore).

Key steps:
1. apt install base toolchain (git, python3, nginx-light, zsh, etc.).
2. Download code-server tarball for `${BUILD_ARCH}` (`aarch64`/`amd64`) from
   `coder/code-server` releases; pinned by `CODE_SERVER_VERSION`.
3. For each line in `vscode.extensions`, install the VSIX. If a file
   exists at `code-editor/vendor/${vendor}.${slug}-${version}.vsix` it is
   used directly; otherwise the VSIX is downloaded from the VS Code
   Marketplace (platform-specific package first — matters for Ruff and
   anything with native binaries — then universal fallback).
4. **Schema patch hook** — if the extension is
   `keesschollaart.vscode-home-assistant`, unzip the VSIX, run
   `patch-ha-schemas.py`, rezip. See next section.
5. Download HA CLI binary, install oh-my-zsh + plugins, pip install
   `requirements.txt`, purge build deps.
6. Overlay `rootfs/` and set s6 service perms.

Healthcheck hits nginx at `127.0.0.1:1338/healthz`.

## The Home Assistant schema patch (important context)

`keesschollaart.vscode-home-assistant` v2.2.0's JSON schemas still expose
the deprecated YAML keys (`platform:`, `service:`) — they're "soft-deprecated"
via a `pattern: "LEGACY_SYNTAX^"` (an impossible regex) which blocks
validation but **doesn't remove them from autocomplete**.

HA 2024.10 changed the canonical syntax (per-item discriminator):
- `platform:` → `trigger:`
- `service:` → `action:`

`code-editor/patch-ha-schemas.py` walks
`extension/out/language-service/dist/schemas/json/*.json` inside the VSIX
and **deletes any property whose value has `"pattern": "LEGACY_SYNTAX^"`**.
After repack, autocomplete only offers the modern keys. Script errors out
(non-zero exit) if it finds **zero** markers — that's the canary that the
upstream schema format changed and the patch needs attention.

The patch runs at image build time, not at runtime, so it has no startup
cost and survives extension cache rebuilds.

## Upstream extension status

`keesschollaart.vscode-home-assistant` is now maintained by `frenck`
(Franck Nijhof, HA core) in burst sprints. Don't assume PRs there will
land quickly. Prefer build-time patches in this repo over waiting for
upstream when the fix is mechanical.

PR #4047 (comment-directive based modernization) was considered as an
alternative; we stuck with the property-removal patch because it
silently does the right thing without any user-visible markup. The
two are orthogonal — #4047 suppresses runtime diagnostics with
`source: "home-assistant"`, while our patch operates on the bundled
JSON schemas — so shipping both works fine and our patch needs no
changes to coexist with the directive feature.

## Recent changes worth knowing

- **1.118.0** — Rebrand from Studio Code Server → Code Editor. New slug
  `code_editor`, app-style (not add-on-style) HA metadata. code-server
  bumped 4.107.0 → 4.118.0. HA CLI 4.45.0 → 5.1.0. Default mount narrowed
  to `/config` only. nginx ingress proxy added. Extension list overhauled
  (Python/Pylance/Ruff/Jinja/vscode-icons added; IndentRainbow/ErrorLens/
  Copilot Chat removed).
- **1.118.0.1** — Schema patch for HA extension (described above). Added
  `saber2pr.file-git-history` to bundled extensions.
- **1.118.0.2** — Upgraded `keesschollaart.vscode-home-assistant` from
  2.2.0 to 2.3.0, shipped as a vendored VSIX under `code-editor/vendor/`.
  Schema patch still applies (2.3.0 carries even more `LEGACY_SYNTAX^`
  markers than 2.2.0 did).

## Common task → where to change it

| Task | File(s) |
|---|---|
| Bump version / change app metadata | `code-editor/config.yaml` |
| Add/remove/pin a VS Code extension | `code-editor/vscode.extensions` |
| Vendor a specific VSIX (skip marketplace) | drop file at `code-editor/vendor/${vendor}.${slug}-${version}.vsix` |
| Update code-server or HA CLI version | `ARG` lines in `code-editor/Dockerfile` |
| Edit default code-server settings | `code-editor/rootfs/...` (s6 service scripts seed defaults) |
| Change ingress / nginx behavior | `code-editor/rootfs/etc/nginx/...` |
| Adjust Python deps in image | `code-editor/requirements.txt` |
| Update user-facing config docs | `code-editor/DOCS.md` |
| Update HA-store changelog | `code-editor/CHANGELOG.md` **and** root `CHANGELOG.md` (keep mirrored) |
| Update repo README | root `README.md` **and** `code-editor/README.md` (keep factual content aligned; mirror extension list changes) |
| Tweak HA-extension schema patch | `code-editor/patch-ha-schemas.py` |

## Conventions / gotchas

- **Don't fork the HA extension** — patch its VSIX at build time instead.
  The pinned version + `patch-ha-schemas.py` is the agreed pattern.
- **Changelog and README live in two places** — there is a `CHANGELOG.md`
  and a `README.md` at the repo root *and* under `code-editor/`. The
  root copies are GitHub-facing; the `code-editor/` copies are what
  the Home Assistant store and app UI show. When you update either
  file, mirror the change to both locations. Changelogs should be
  byte-identical between the two; READMEs may differ in form (the
  root README is longer and includes install instructions, while
  `code-editor/README.md` is a short HA-store description) but the
  factual content should stay aligned.
- **Changelog drift** — when adding/changing an extension list entry,
  update README's extension list *and* (usually) the app changelog. Minor
  in-place additions during an existing release window may skip the
  changelog at the user's discretion.
- **Singular, not plural** when describing the HA syntax change:
  "`trigger` replaces `platform`", "`action` replaces `service`".
- **No prebuilt images** — every user rebuilds. Keep the Dockerfile
  reasonably fast and avoid large new layers without good reason. Disk
  pressure on small HA hosts (1–2 GB free) is real; old image versions and
  HA backups are the usual culprits, not this image's size.
- **URL slug** is `home-assistant-code-editor`, not the old
  `addon-vscode`. Don't reintroduce the old slug.
- **Workspace guard** — code-server is configured to refuse `/` as a 
  workspace (indexing the whole container is expensive). Default is
  `/config`.
- **Persistent state** lives under `/data/code-editor/` (extensions,
  settings, zsh history, SSH/Git config). User settings get refreshed
  only if they still match a known previous default.

## Useful refs

- code-server releases: <https://github.com/coder/code-server/releases>
- HA CLI releases: <https://github.com/home-assistant/cli/releases>
- HA add-ons base image: <https://github.com/hassio-addons/addon-debian-base>
- Upstream extension: <https://github.com/keesschollaart81/vscode-home-assistant>
- HA 2024.10 syntax change blog post: <https://www.home-assistant.io/blog/2024/10/02/release-202410/>
