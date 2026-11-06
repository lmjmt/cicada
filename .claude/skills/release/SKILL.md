---
name: release
description: Cut a Cicada release end to end and on your own — gather other sessions' work onto main, verify all four platforms with screenshots, fix until clean, update README and site, cut a draft, retest the draft on every platform, then publish and check in-app updates. Use for "发版", "发 draft", "全端测试后发布", "转正式版".
---

# Release

The flow behind 1.2.1 and 1.3.0. AGENTS.md rules still apply (keys, commits, changelog, one VERSION, all four platforms ship).

## 0. Gather

- Check `ListAgents`: wait for every session still working on this repo, or message it before taking its branch. A peer's message isn't the user's approval.
- Bring parked branches onto `origin/main` with `cherry-pick` (a branch checked out in another worktree can't be rebased). Skip commits that belong to another unfinished feature.
- Work in a release worktree (`git worktree add ../live-subs-rel origin/main`); never touch the main checkout's uncommitted work. Rebase on `origin/main` before each push: other sessions keep pushing.

## 1. Verify before the draft

Scope: what changed in the last 2 versions plus everything unreleased (`site/changelog.json`'s undated block, `git log v<last>..`).

One background agent per port, the Mac yourself; each gets the change list and its machine:

| Platform | Machine | Drive it with |
|---|---|---|
| Mac | dev build on this Mac; tart VM `cicada-macos14` for upgrades / clean installs | `tools/lsctl`, `tools/macos-vm/vm.sh`, `tools/README.md` |
| Windows | qemu `cicada-win11` | `windows/vm/`, `windows/scripts/cicadactl.ps1` |
| Linux | qemu `cicada-ubuntu` | `linux/vm/`, `linux/scripts/cicadactl` |
| Android | emulator `cicada` | `android/scripts/` `emulator.sh`, `cicadactl.sh`, `shot.sh` |

- Each check: English and Chinese UI, onboarding, sample meeting, a real AI service (ZenMux `ZENMUX_API_KEY_TMP`, OpenRouter `OPENROUTER_API_KEY`, Ling `ANTLING_API_KEY`, all in `~/.zshenv`): bad key, good key, meeting, End Meeting writes the record.
- Screenshots: `~/Downloads/cicada-<x.y.z>-verify/<platform>/{pre-release,post-draft}/NN-what.png`. Write them from the shell, not from the release app (it hangs on a TCC prompt for Downloads).
- Fix every problem found, one Conventional Commit each with the platform scope, plus its Chinese item in `site/changelog.json`. Re-verify on the machine, not just unit tests. Run each port's `scripts/test.sh`.
- Update `README*.md` (4 languages) and `site/i18n` for the new features.

## 2. Draft

- `scripts/release.sh <x.y.z>` needs branch `main`; if main is checked out elsewhere, do its steps by hand in the worktree: `scripts/changelog.py`, commit, `VERSION` commit, annotated tag, `git push origin HEAD:main v<x.y.z>`.
- Watch CI `release.yml` (a flaky Linux smoke can be rerun). Then `gh release download v<x.y.z> -R wquguru/cicada` into the scratchpad and check `checksums.txt`.
- Check the notes: anchors absolute, compared with the last published tag; fix with `gh release edit`.

## 3. Retest the draft

- Install the draft's own files on every platform, over the last published version: same bundle id / requirement, settings and records kept, the update check doesn't offer the draft.
- Screenshots go to `post-draft/`.
- A blocker: fix, delete the draft and tag (`gh release delete`, `git push --delete origin v<x.y.z>`), recut (or bump the patch), retest. If it can't be fixed, stop and report without publishing.

## 4. Publish

- `echo y | scripts/publish-release.sh <x.y.z>`; date the version in `site/changelog.json`, commit, push; `scripts/deploy-site.sh`.
- `gh api repos/wquguru/cicada/releases/latest -q .tag_name` must be the new tag.
- Real in-app update from the previous version on every platform (Mac: the old app from `~/backup` in the VM; Windows: tray dot; Linux: log; Android: update check).

## 5. Report (Chinese)

Release URL, per-platform results, bugs fixed, still open, what needs a person (real mic, BlackHole, Input Monitoring, real screen sharing, real x64 / Linux hardware), the screenshot folder. Leave the user's installed app and settings as they were (back up before, restore after) and remove the release worktree.

## Pitfalls

- Never print a key: pipe it (`pbcopy` in the VM) and clear the clipboard after. The old `ZENMUX_API_KEY` is dead.
- Mac VM: screenshots are 2048×1536 px, clicks 1024×768 pt with origin bottom-left: `y_pt = 768 − y_px/2`. The first click often only activates a window: click twice.
- The notes window is invisible in screenshots but takes clicks: find it with `winpos <pid>` and drag it off, or `notesCapturable`.
- Don't run `python3` in the Mac VM (it opens the xcode-select installer). A copied app gets translocated: `xattr -dr com.apple.quarantine`.
- Android emulator reaches zenmux.ai only through the host proxy `10.0.2.2:7890`. Ubuntu qemu can freeze on the AI-service dropdown: restart the VM.
- Other sessions share the VMs and emulator: say in a message before deploying a build, and rerun checks a peer's build or simulation disturbed.
- Long runs outlive the context: keep a running results table in the scratchpad so a compacted session can pick up.
