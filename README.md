# ds-cli-design

The terminal design system's exports from Claude Design, and the check that keeps the canon's code equal to them. It is the terminal sibling of the HTML design system (`dashboard-style` / `ds-design-system`). The name means "design for CLIs"; it is not the `ds-cli` tool.

The code that draws the design is the canon's, not this repo's: canon-lib's `ui_style`, `widgets` and `picker`, built from the blocks `block-ui-style`, `block-tui-widgets` and `block-tui-picker` (the canon standard `terminal-design`). ds-next and atlas import it from there. Until 1.1.0 this repo was also a Python library, `ds_cli_design`; the tag `v1.1.0` still installs it for anything pinned to it, but nothing new should.

## What's here

| Path | What it is |
|---|---|
| `design-system/` | The export, as delivered: `readme.md` (principles, content, visual foundations: start here), `ACCEPTED.md` (what was chosen), `tokens.json` (every value, machine-readable), `tokens/*.css`, `guidelines/` (specimen cards: colours, type, glyphs, grid, mascot), `components/terminal/` (React primitives with props contracts and usage notes), `ui_kits/terminal/` (a full session), `pages/` (the spec and screens, offline), `assets/mascot.txt`, `HANDOFF-terminal.md`, `SYNC.md`, `SKILL.upstream.md` |
| `examples/ds-next/` | The export's `code/`: ds-next's own `ui.py`, `cli.py`, `widgets.py`, `ui_style.py`, a full REPL built on the system |
| `skills/ds-cli-design-sync/` | Skill: bring a new export in and carry it to the canon's code and the CLIs that use it |
| `scripts/check.py` | The canon's `ui_style` agrees with `tokens.json`: every role in both themes and ANSI-16, every glyph, the grid, the mascot, frames exact at 80 and 60 |
| `scripts/sync.py` | Replace `design-system/` from a new export zip and print the token diff |

## Use the design in a CLI

```sh
uv add "canon-lib[tui] @ git+https://github.com/cwkoenigs/canon@canon-lib-v0.2.0#subdirectory=lib"
```

```python
import sys
from canon_lib import ui_style as S
out = S.console(color=sys.stdout.isatty())
out.print(S.outcome("ok", "deploy", "3 files · 2 s"))
```

The `ds-terminal-design` skill (installed by `ds-next setup`) has which helper fits which moment, and the rules. `~/Developer/atlas` is a complete CLI built on it.

## Commands

| Command | Does |
|---|---|
| `make check` | Fails if the canon's `ui_style` and `tokens.json` disagree (the canon at `$DS_CANON`, else `~/Developer/canon`) |
| `make sync ZIP=~/Downloads/<export>.zip` | Bring in a new export from Claude Design, print what moved, check |
| `make install` | Link the sync skill into `~/.claude/skills`, `~/.codex/skills`, `~/.hermes/skills` (whichever exist) |

## Updating

Change the design in the Claude Design project, export the zip, then `make sync ZIP=...`. The `ds-cli-design-sync` skill walks through the rest: mirroring moved tokens in the canon's `block-ui-style`, releasing canon-lib under a new tag, and moving the pins in ds-next and atlas.

## History

The library started as the export's `code/ui_style.py` and `code/widgets.py`; 1.1.0 took ds-next's banner and prompt box so ds-next could import it. On 2026-10-28 the code went back to the canon, where the look had been released on 2026-10-20: canon-lib 0.2.0 took the two things only this library had, `banner(name=...)` and `browse`, so there is one copy of the code.
