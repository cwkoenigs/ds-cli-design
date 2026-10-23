---
name: ds-cli-design-sync
description: "Use when a new terminal design system export arrives."
---

# Bring a new terminal design system export into ds-cli-design

The design decisions are made in the Claude Design project (`design-system/tokens.json` names it under `source.designProject`). Each time Clark asks it for "the design system zip" he gets an export like `~/Downloads/CLI design system development prod.zip`. This skill carries that export into `~/Developer/ds-cli-design` and on to every CLI that uses it.

## Procedure

1. Find the zip (usually the newest `*design system*.zip` in `~/Downloads`). Confirm it with Clark if more than one fits.
2. `make -C ~/Developer/ds-cli-design sync ZIP="<path>"`. It replaces `design-system/` (the export's `code/` goes to `examples/ds-next/`, its `SKILL.md` to `design-system/SKILL.upstream.md`), prints every token added (+), removed (-) or changed (~), and runs the check.
3. If the check fails, the tokens moved. Mirror each change in `src/ds_cli_design/ui_style.py`: colours in `PALETTE` (dark, light, ansi16), glyphs in `_Glyphs`, the grid constants, `MASCOT`. Then `make check` until it passes. That file and `tokens.json` are the only two places a value lives.
4. If the export's `code/ui_style.py` or `code/widgets.py` changed beyond tokens (new helpers, new widgets), port them into `src/ds_cli_design/`, keeping the local fixes: `banner(name=...)`, `agent_lines` printing its text, frames held at their width with `VSplit([Frame(..., width=w), Window()])`.
5. `make demo` and `make demo-widgets` in a real terminal (tmux): every component still renders at 80 columns, both themes (`DS_THEME=light`).
6. Bump `version` in `pyproject.toml` and `__version__` in `src/ds_cli_design/__init__.py`; update the skill `ds-cli-design` if a rule changed. Commit with the token diff in the message and push.
7. Carry it to the consumers:
   - `~/Developer/atlas` depends on it editable: `uv tool install --editable ~/Developer/atlas --force`, then run `atlas` in a terminal to look.
   - ds-next keeps its own live copy (`src/ds_next/ui_style.py`); tell Clark what changed rather than editing that repo uninvited.

## Pitfalls

- The export is not a git diff: it replaces the folder wholesale. Local notes belong in `design-system/SYNC.local.md`, which sync keeps.
- Never edit `design-system/` by hand to change a value; change it in the design project and re-export, or it will be overwritten on the next sync.
