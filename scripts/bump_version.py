#!/usr/bin/env python3
"""
Bump semantic version in package.json and git-local-sweep script in one step.
"""

import argparse
import json
import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
PACKAGE_JSON_PATH = REPO_ROOT / "package.json"
CLI_SCRIPT_PATH = REPO_ROOT / "git-local-sweep"
VERSION_LINE_PATTERN = re.compile(r'^VERSION = "(\d+\.\d+\.\d+)"$', re.MULTILINE)


def parse_semver(version):
    match = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)", version)
    if not match:
        raise ValueError(f"Invalid semantic version: {version}")
    return tuple(int(part) for part in match.groups())


def bump_semver(version, bump_type):
    major, minor, patch = parse_semver(version)

    if bump_type == "major":
        return f"{major + 1}.0.0"
    if bump_type == "minor":
        return f"{major}.{minor + 1}.0"
    if bump_type == "patch":
        return f"{major}.{minor}.{patch + 1}"

    raise ValueError(f"Unsupported bump type: {bump_type}")


def load_package_json():
    if not PACKAGE_JSON_PATH.exists():
        raise FileNotFoundError(f"Missing file: {PACKAGE_JSON_PATH}")

    with PACKAGE_JSON_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_package_json(data):
    with PACKAGE_JSON_PATH.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)
        file.write("\n")


def update_cli_script(new_version):
    if not CLI_SCRIPT_PATH.exists():
        raise FileNotFoundError(f"Missing file: {CLI_SCRIPT_PATH}")

    content = CLI_SCRIPT_PATH.read_text(encoding="utf-8")
    if not VERSION_LINE_PATTERN.search(content):
        raise RuntimeError(
            f"Could not find VERSION line in {CLI_SCRIPT_PATH}"
        )

    updated = VERSION_LINE_PATTERN.sub(
        f'VERSION = "{new_version}"',
        content,
        count=1
    )
    CLI_SCRIPT_PATH.write_text(updated, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(
        description="Bump semantic version in package.json and git-local-sweep."
    )
    parser.add_argument(
        "bump_type",
        choices=["major", "minor", "patch"],
        help="Version bump type."
    )
    args = parser.parse_args()

    package_data = load_package_json()
    current_version = package_data.get("version")
    if not current_version:
        print("package.json is missing a version field.", file=sys.stderr)
        sys.exit(1)

    try:
        new_version = bump_semver(current_version, args.bump_type)
    except ValueError as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)

    package_data["version"] = new_version
    save_package_json(package_data)
    update_cli_script(new_version)

    print(f"Bumped version: {current_version} -> {new_version}")


if __name__ == "__main__":
    main()
