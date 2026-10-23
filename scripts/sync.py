#!/usr/bin/env python3
"""Bring a new export of the design system in from Claude Design.

    python3 scripts/sync.py ~/Downloads/"CLI design system development prod.zip"   (or: make sync ZIP=...)

1. Unzips the export (it holds a `final/` folder, or the files at the top level).
2. Replaces design-system/ with it (code/ goes to examples/ds-next/, SKILL.md to SKILL.upstream.md).
3. Prints every token that was added, removed or changed since the last sync.
4. Runs the check. When it fails, the tokens moved: update src/ds_cli_design/ui_style.py by hand
   (PALETTE, G, grid constants, MASCOT) until `make check` passes. That file mirrors tokens.json;
   nothing else holds a value.
"""
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
DS = ROOT / "design-system"
KEEP_LOCAL = {"SYNC.local.md"}


def flat(obj, prefix=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from flat(v, f"{prefix}{k}.")
    else:
        yield prefix.rstrip("."), obj


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    zpath = pathlib.Path(sys.argv[1]).expanduser()
    old = dict(flat(json.loads((DS / "tokens.json").read_text()))) if (DS / "tokens.json").is_file() else {}
    with tempfile.TemporaryDirectory() as tmp:
        with zipfile.ZipFile(zpath) as z:
            z.extractall(tmp)
        hits = [p.parent for p in pathlib.Path(tmp).rglob("tokens.json") if "__MACOSX" not in p.parts]
        if not hits:
            sys.exit(f"{zpath}: no tokens.json inside; is this the design system export?")
        src = min(hits, key=lambda p: len(p.parts))
        keep = {n: (DS / n).read_bytes() for n in KEEP_LOCAL if (DS / n).is_file()}
        shutil.rmtree(DS)
        shutil.copytree(src, DS, ignore=shutil.ignore_patterns("__MACOSX", ".DS_Store", "code", "SKILL.md"))
        for n, b in keep.items():
            (DS / n).write_bytes(b)
        if (src / "SKILL.md").is_file():
            shutil.copy(src / "SKILL.md", DS / "SKILL.upstream.md")
        if (src / "code").is_dir():
            ex = ROOT / "examples" / "ds-next"
            shutil.rmtree(ex, ignore_errors=True)
            shutil.copytree(src / "code", ex, ignore=shutil.ignore_patterns("__pycache__"))
    new = dict(flat(json.loads((DS / "tokens.json").read_text())))
    print(f"synced design-system/ from {zpath.name}")
    changed = [(k, old.get(k), new.get(k)) for k in sorted(set(old) | set(new)) if old.get(k) != new.get(k)]
    for k, a, b in changed:
        print(f"  {'+' if a is None else '-' if b is None else '~'} {k}: {a!r} -> {b!r}")
    if not changed:
        print("  tokens unchanged")
    r = subprocess.run(["uv", "run", "--quiet", "python", str(ROOT / "scripts" / "check.py")], cwd=ROOT)
    if r.returncode:
        print("\nthe tokens moved: mirror them in src/ds_cli_design/ui_style.py, then `make check`")
    sys.exit(r.returncode)


if __name__ == "__main__":
    main()
