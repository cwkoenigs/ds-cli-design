---
name: ds-cli-design-sync
description: "Use when a new terminal design system export arrives."
---

# Bring a new terminal design system export into ds-cli-design and the canon

The design decisions are made in the Claude Design project (`design-system/tokens.json` names it under `source.designProject`). Each time Clark asks it for "the design system zip", it sends an export like `~/Downloads/CLI design system development prod.zip`. This skill carries that export into `~/Developer/ds-cli-design`, into the canon's code (canon-lib's `ui_style`, `widgets`, `picker`), and on to every CLI that uses it.

## Procedure

1. Find the zip (usually the newest `*design system*.zip` in `~/Downloads`). Confirm it with Clark if more than one fits.
2. `make -C ~/Developer/ds-cli-design sync ZIP="<path>"`. It replaces `design-system/` (the export's `code/` goes to `examples/ds-next/`, its `SKILL.md` to `design-system/SKILL.upstream.md`), prints every token added (+), removed (-) or changed (~), and runs the check against the canon (`$DS_CANON`, else `~/Developer/canon`).
3. If the check fails, the tokens moved. On a branch in the canon, mirror each change in `blocks/block-ui-style/code/ui_style.py`: colours in `PALETTE` (dark, light, ansi16), glyphs in `_Glyphs`, the grid constants, `MASCOT`. Then `make check` until it passes. That file and `tokens.json` are the only two places a value lives.
4. If the export's `code/ui_style.py` or `code/widgets.py` changed beyond tokens (new helpers, new widgets), port them into the canon's blocks (`block-ui-style`, `block-tui-widgets`, `block-tui-picker`, or a new block, status `proposed`), keeping the canon's departures from the export: the brighter banner with `banner(name=...)`, Cortex Code's rounded prompt box with the session tag, `agent_lines` printing its text, frames held at their width with `VSplit([Frame(..., width=w), Window()])`, every Application wrapped in `widgets.resize_safe`.
5. Release it from the canon: bump each changed block's `version` (with a line in its `BLOCK.md` saying what changed) and `lib/pyproject.toml`'s version; run `scripts/build_index.py`, `scripts/build_lib.py` and `scripts/test_blocks.py block-ui-style block-tui-widgets block-tui-picker`; open the PR. Once it is merged, tag the merge `canon-lib-v<version>` and push the tag.
6. Commit the export here with the token diff in the message, and push.
7. Carry it to the consumers by moving their pin to the new tag:
   - ds-next: the `canon-lib[tui] @ git+...@canon-lib-v<version>` line in `pyproject.toml`, then `uv lock` and the tests.
   - atlas: the tag under `[tool.uv.sources]`, then `uv tool install --editable ~/Developer/atlas --force`, and run `atlas` in a real terminal (tmux) to look: every component at 80 columns, both themes (`DS_THEME=light`).
   Tell Clark which repos moved.

## Pitfalls

- The export is not a git diff: it replaces the folder wholesale. Local notes belong in `design-system/SYNC.local.md`, which sync keeps.
- Never edit `design-system/` by hand to change a value; change it in the design project and re-export, or it will be overwritten on the next sync.
- Never put the code back here. There is one copy, in the canon's blocks; this repo only holds the design and checks the code against it.
