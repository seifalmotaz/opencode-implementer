"""Stdlib-only package check for the opencode-implementer plugin (no installs)."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PLUGIN = ROOT / "plugins/opencode-implementer/.codex-plugin/plugin.json"
MARKET = ROOT / ".agents/plugins/marketplace.json"
LIC = ROOT / "LICENSE"

errors = []


def fail(msg):
    errors.append(msg)


def assert_under_root(root, rel):
    """Resolve rel against root; raise ValueError if it escapes root."""
    target = (root / rel).resolve()
    try:
        target.relative_to(root.resolve())
    except ValueError:
        raise ValueError(f"path escapes package root: {rel}")
    return target


def check_frontmatter(path):
    try:
        lines = path.read_text().splitlines()
    except OSError:
        return False
    if not lines or lines[0].strip() != "---":
        return False
    try:
        end = lines.index("---", 1)
    except ValueError:
        return False
    name = descr = ""
    for line in lines[1:end]:
        if line.startswith("name:"):
            name = line.split(":", 1)[1].strip()
        elif line.startswith("description:"):
            descr = line.split(":", 1)[1].strip()
    return bool(name and descr)


def main():
    try:
        manifest = json.loads(PLUGIN.read_text())
    except Exception as e:  # noqa: BLE001 - report as validation failure
        fail(f"plugin.json invalid: {e}")
        manifest = None
    try:
        market = json.loads(MARKET.read_text())
    except Exception as e:  # noqa: BLE001 - report as validation failure
        fail(f"marketplace.json invalid: {e}")
        market = None

    if manifest is not None:
        for key in ("name", "version", "description", "skills"):
            if not manifest.get(key):
                fail(f"plugin.json missing {key}")
        try:
            skills = assert_under_root(PLUGIN.parent.parent, manifest.get("skills") or "skills")
            if not skills.is_dir():
                fail("manifest skills directory missing")
            elif not check_frontmatter(skills / manifest["name"] / "SKILL.md"):
                fail("SKILL.md frontmatter name/description missing")
        except ValueError as e:
            fail(str(e))

    if market is not None:
        try:
            src = market["plugins"][0]["source"]["path"]
            target = assert_under_root(ROOT, src)
            if not target.is_dir():
                fail(f"marketplace source path missing: {src}")
        except (KeyError, IndexError, TypeError):
            fail("marketplace.json plugin source entry malformed")
        except ValueError as e:
            fail(str(e))

    if not LIC.is_file() or "MIT License" not in LIC.read_text():
        fail("LICENSE missing MIT text")
    elif "2026 Seif Almotaz" not in LIC.read_text():
        fail("LICENSE missing copyright 2026 Seif Almotaz")

    if errors:
        print("FAIL:")
        for e in errors:
            print(f" - {e}")
        sys.exit(1)
    print("OK: manifest/marketplace structure, skill frontmatter, LICENSE.")


if __name__ == "__main__":
    main()
