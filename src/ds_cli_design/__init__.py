"""ds-cli-design: the terminal design system as a Python library.

    from ds_cli_design import S, G, console, browse, Item, pick, form, Field
    out = console(color=sys.stdout.isatty())
    out.print(S.outcome("ok", "deploy", "3 files · 2 s"))

S is the ui_style module (roles, glyphs, grid, line builders, frames, banner). The rules for using it
are in design-system/readme.md and the ds-cli-design skill.
"""
from . import ui_style as S
from .picker import Item, browse
from .ui_style import G, console
from .widgets import Field, form, pick

__version__ = "1.0.0"
__all__ = ["S", "G", "console", "browse", "Item", "pick", "form", "Field", "__version__"]
