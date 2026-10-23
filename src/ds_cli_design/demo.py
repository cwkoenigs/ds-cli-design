"""Every piece of the design system on one screen, built only with the library.

    uv run ds-cli-design-demo            (or: make demo)   colour on a terminal, plain glyphs when piped
    DS_THEME=light uv run ds-cli-design-demo               the light ramp
    uv run ds-cli-design-demo --widgets                    then try pick, form and browse

Read it as the reference for how each helper is meant to be used.
"""
from __future__ import annotations

import asyncio
import sys
import time

from rich.markdown import Markdown
from rich.text import Text

from . import ui_style as S
from .picker import Item, browse
from .ui_style import G
from .widgets import Field, form, pick


def main() -> None:
    out = S.console(color=sys.stdout.isatty())
    w = S.width(out)

    # 1. the banner: shown once, at the start of a session
    for line in S.banner("1.0", [("project", "ds-cli-design"), ("theme", "dark" if S.is_dark() else "light"),
                                 ("width", f"{w} cols")],
                         ["/help lists commands", "Esc cancels a widget"], "~/Developer/ds-cli-design",
                         "terminal design", w=w, name="ds-cli"):
        out.print(line)
    out.print()

    # 2. a flat command: outcomes, labelled rows, a hint. No rail; local commands are instant.
    out.print(S.outcome("ok", "check", "13 roles · 14 glyphs · grid · mascot"))
    out.print(S.outcome("warn", "tokens.json", "updated 2026-10-23 · newer than the last sync"))
    out.print(S.labelled("project", "ds-cli-design"))
    out.print(S.labelled("theme", "DS_THEME=light|dark"))
    out.print(S.hint("make sync ZIP=<export.zip> brings in a new export"))
    out.print()

    # 3. an agent's turn: you, the agent on one rail, a tool call, its folded result, the footer
    out.print(S.you("which repo serves the billing site?"))
    S.agent_lines(out, Markdown("Two Vercel projects build from **one repo**; checking which root each uses."))
    out.print(S.run("vercel", "project inspect ringneck-billing"))
    out.print(S.result("Root Directory  site/ringneck-billing", more=14))
    with out.status(S.status_label("reading deployments", 0), spinner=S.SPINNER, spinner_style="accent") as live:
        for s in range(1, 3):
            time.sleep(0.4)
            live.update(S.status_label("reading deployments", s))
    out.print(S.run("gh", "api repos/…/deployments"))
    out.print(S.result("Production – ringneck-billing  db61b32"))
    S.agent_lines(out, Markdown("`ringneck-billing` deploys on every push to main; the checkout links the other project."))
    out.print(S.footer("2 tools", "4 s", "turn 3"))
    out.print()

    # 4. an error: what failed, then the fix. Red only on the line that failed.
    for line in S.error("canon not found at ~/Developer/canon", "set DS_CANON=<path> or run ds-next init"):
        out.print(line)
    out.print(S.fold("3 lines folded · ctrl-o opens"))
    out.print()

    # 5. a frame: only for something that needs you. kind="approval" draws the warn edge.
    keys = Text.assemble(("y", "key"), (" approve · n deny", "dim"))
    for line in S.frame(Text.assemble(("approve", "bold"), (f"{G.sep}git push", "muted")),
                        [Text("push 3 commits to origin/main?"), None,
                         S.labelled("branch", "main", indent=0), S.labelled("commits", "3", indent=0)],
                        kind="approval", keys=keys, w=w):
        out.print(line)

    if "--widgets" in sys.argv and sys.stdin.isatty():
        out.print()
        choice = asyncio.run(pick("pick a theme", [("dark", "dark", "the default"), ("light", "light", "DS_THEME=light")]))
        out.print(S.outcome("ok", "pick", str(choice)))
        values = asyncio.run(form("new project", [
            Field("name", "name", required=True, example="feed-model"),
            Field("kind", "kind", "python-cli", choices=[("python-cli", "python cli"), ("notebook", "notebook")]),
            Field("owner", "owner", hint="who answers questions about it"),
        ], footer=lambda v: f"creates ~/Developer/{v['name'] or '<name>'}", validate=lambda v: None, width=w))
        out.print(S.outcome("ok", "form", str(values)))
        items = [Item(f"g{n}", name, f"glyph {ch}", outcome=oc, number=n)
                 for n, (name, ch, oc) in enumerate([("ok", G.ok, "ok"), ("warn", G.warn, "warn"), ("err", G.err, "err"),
                                                      ("prompt", G.prompt, ""), ("agent", G.agent, ""), ("run", G.run, ""),
                                                      ("result", G.result, ""), ("rail", G.rail, ""), ("close", G.close, ""),
                                                      ("select", G.select, ""), ("fold", G.fold, ""), ("sep", G.sep.strip(), "")], 1)]
        out.print(S.outcome("ok", "browse", str(asyncio.run(browse("glyphs", items, width=w)))))


if __name__ == "__main__":
    main()
