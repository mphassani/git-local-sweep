#!/usr/bin/env python3
"""
Ensure package.json version matches VERSION in git-local-sweep.
"""

import json
import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
PACKAGE_JSON_PATH = REPO_ROOT / "package.json"
CLI_SCRIPT_PATH = REPO_ROOT / "git-local-sweep"
VERSION_LINE_PATTERN = re.compile(r'^VERSION = "(\d+\.\d+\.\d+)"$', re.MULTILINE)


def read_package_version():
    if not PACKAGE_JSON_PATH.exists():
        raise FileNotFoundError(f"Missing file: {PACKAGE_JSON_PATH}")

    with PACKAGE_JSON_PATH.open("r", encoding="utf-8") as file:
        data = json.load(file)

    version = data.get("version")
    if not version:
        raise RuntimeError("package.json is missing a version field.")
    return version


def read_script_version():
    if not CLI_SCRIPT_PATH.exists():
        raise FileNotFoundError(f"Missing file: {CLI_SCRIPT_PATH}")

    content = CLI_SCRIPT_PATH.read_text(encoding="utf-8")
    match = VERSION_LINE_PATTERN.search(content)
    if not match:
        raise RuntimeError(f"Could not find VERSION line in {CLI_SCRIPT_PATH}")
    return match.group(1)


def main():
    try:
        package_version = read_package_version()
        script_version = read_script_version()
    except (FileNotFoundError, RuntimeError) as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)

    if package_version != script_version:
        print(
            "Version mismatch detected: "
            f"package.json={package_version}, git-local-sweep={script_version}",
            file=sys.stderr
        )
        sys.exit(1)

    print(f"Versions are in sync: {package_version}")


if __name__ == "__main__":
    main()
