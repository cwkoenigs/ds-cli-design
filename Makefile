# ds-cli-design: the terminal design system as a project.
#   make check            the library agrees with design-system/tokens.json
#   make demo             every component on one screen (make demo-widgets for pick, form, browse)
#   make sync ZIP=FILE    bring in a new export from Claude Design, print the token diff, check
#   make install          link the skills into ~/.claude/skills, ~/.codex/skills, ~/.hermes/skills
#   make uninstall        remove those links
ZIP ?=

.PHONY: check demo demo-widgets sync install uninstall

check:
	uv run --quiet python scripts/check.py

demo:
	uv run --quiet ds-cli-design-demo

demo-widgets:
	uv run --quiet ds-cli-design-demo --widgets

sync:
	@test -n "$(ZIP)" || (echo "usage: make sync ZIP=~/Downloads/<export>.zip" && exit 2)
	python3 scripts/sync.py "$(ZIP)"

install:
	./install.sh

uninstall:
	./install.sh --uninstall
