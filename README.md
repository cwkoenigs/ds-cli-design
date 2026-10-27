# ds-cli-design

The terminal design system as a project: everything from the Claude Design export, a Python library that renders it, and the skills that let an agent build any CLI in this style. It is the terminal sibling of the HTML design system (`dashboard-style` / `ds-design-system`).

The design comes from ds-next ("ds-next terminal design system v1", 2026-10-23). The name `ds-cli-design` means "design for CLIs"; it is not the `ds-cli` tool.

## What's here

| Path | What it is |
|---|---|
| `design-system/` | The export, as delivered: `readme.md` (principles, content, visual foundations: start here), `ACCEPTED.md` (what was chosen), `tokens.json` (every value, machine-readable), `tokens/*.css`, `guidelines/` (specimen cards: colours, type, glyphs, grid, mascot), `components/terminal/` (React primitives with props contracts and usage notes), `ui_kits/terminal/` (a full session), `pages/` (the spec and screens, offline), `assets/mascot.txt`, `HANDOFF-terminal.md`, `SYNC.md`, `SKILL.upstream.md` |
| `src/ds_cli_design/` | The library. `ui_style.py`: roles, glyphs, grid, line builders, frames, banner, mascot. `widgets.py`: `pick` and `form`. `picker.py`: `browse`, a filterable list. `demo.py`: every component on one screen |
| `examples/ds-next/` | The export's `code/`: ds-next's own `ui.py`, `cli.py`, `widgets.py`, `ui_style.py`, a full REPL built on the system |
| `skills/ds-cli-design/` | Skill: build or restyle a CLI in this system (library use, rules, verification) |
| `skills/ds-cli-design-sync/` | Skill: bring a new export in and carry it to the CLIs that use it |
| `scripts/check.py` | The library agrees with `tokens.json`: every role in both themes and ANSI-16, every glyph, the grid, the mascot |
| `scripts/sync.py` | Replace `design-system/` from a new export zip and print the token diff |

## Use it in a CLI

```sh
uv add --editable ~/Developer/ds-cli-design                                  # on this Mac
uv add "ds-cli-design @ git+https://github.com/cwkoenigs/ds-cli-design"      # anywhere else
```

```python
import sys
from ds_cli_design import S, console
out = console(color=sys.stdout.isatty())
out.print(S.outcome("ok", "deploy", "3 files · 2 s"))
for line in S.error("canon not found at ~/Developer/canon", "set DS_CANON=<path>"):
    out.print(line)
```

The `ds-cli-design` skill has the table of which helper fits which moment and the rules. `~/Developer/atlas` is a complete CLI built on it.

## Commands

| Command | Does |
|---|---|
| `make demo` | Every component on one screen (banner, outcomes, a turn, an error, an approval frame) |
| `make demo-widgets` | The same, then `pick`, `form` and `browse` to try |
| `make check` | Fails if the library and `tokens.json` disagree |
| `make sync ZIP=~/Downloads/<export>.zip` | Bring in a new export from Claude Design, print what moved, check |
| `make install` | Link both skills into `~/.claude/skills`, `~/.codex/skills`, `~/.hermes/skills` (whichever exist) |

`DS_THEME=light` shows the light ramp; without `COLORTERM=truecolor` it falls back to ANSI-16.

## Changes from the export

The library started as the export's `code/ui_style.py` and `code/widgets.py`. Since 1.1.0 it also carries
what ds-next drew on its own, so ds-next imports the look from here instead of keeping a copy:

- `banner()` draws the brighter banner the owner chose: a visible edge, a bright title. It takes the
  product name and the art instead of always saying ds-next.
- `prompt_box`, `PromptEcho` and `session_rule` draw Cortex Code's rounded prompt box with the session
  tag in its top rule.
- `agent_lines()` prints its text; the export's copy printed `None`, because `Text.rstrip()` works in place (ds-next's live copy already had this fix).
- `agent_lines()` prints its text; the export's copy printed `None`, because `Text.rstrip()` works in place (ds-next's live copy already had this fix).
- `pick` and `form` frames keep their width in a terminal wider than 80 columns; in the export they overshoot.

`picker.browse` is new: a filterable picker for long lists, drawn like `pick`.

## Updating

Change the design in the Claude Design project, export the zip, then `make sync ZIP=...` (the `ds-cli-design-sync` skill walks through it, including mirroring moved tokens in `ui_style.py` and updating the CLIs that use the library).
