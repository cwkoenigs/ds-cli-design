# ds-cli-design: the terminal design system's exports from Claude Design. The code is the canon's.
#   make check            the canon's ui_style agrees with design-system/tokens.json
#                         (the canon at $DS_CANON, else ~/Developer/canon)
#   make sync ZIP=FILE    bring in a new export from Claude Design, print the token diff, check
#   make install          link the skill into ~/.claude/skills, ~/.codex/skills, ~/.hermes/skills
#   make uninstall        remove those links
ZIP ?=
RUN = uv run --quiet --no-project --with "rich>=13" --with "prompt-toolkit>=3.0.40" python

.PHONY: check sync install uninstall

check:
	$(RUN) scripts/check.py

sync:
	@test -n "$(ZIP)" || (echo "usage: make sync ZIP=~/Downloads/<export>.zip" && exit 2)
	python3 scripts/sync.py "$(ZIP)"

install:
	./install.sh

uninstall:
	./install.sh --uninstall
