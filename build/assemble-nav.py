#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2024-present Deepstaging
# SPDX-License-Identifier: RPL-1.5

"""
Assembles the site nav by importing nav sections from each repo's mkdocs.yml.

Each repo defines its own nav with relative paths. This script reads those,
prefixes all paths with the repo's docs directory name, and writes the merged
nav into the site's mkdocs.yml — replacing everything after the `nav:` line.

This prevents the site nav from going stale when repos add new pages.
"""

import sys
from pathlib import Path

import yaml


# (repo directory name, nav section title, docs prefix in assembled site)
REPOS = [
    ("deepstaging", "Deepstaging", "deepstaging"),
    ("roslyn", "Roslyn", "roslyn"),
    ("deepstaging-web", "Web", "web"),
]


def prefix_paths(nav: list, prefix: str) -> list:
    """Recursively prefix all path values in a nav tree."""
    result = []
    for item in nav:
        if isinstance(item, str):
            result.append(f"{prefix}/{item}")
        elif isinstance(item, dict):
            new_item = {}
            for key, value in item.items():
                if isinstance(value, str):
                    new_item[key] = f"{prefix}/{value}"
                elif isinstance(value, list):
                    new_item[key] = prefix_paths(value, prefix)
                else:
                    new_item[key] = value
            result.append(new_item)
        else:
            result.append(item)
    return result


def extract_nav_section(content: str) -> str | None:
    """Extract the nav section from mkdocs.yml content as raw YAML text."""
    lines = content.split("\n")
    nav_start = None
    nav_end = None

    for i, line in enumerate(lines):
        if line.rstrip() == "nav:":
            nav_start = i
        elif nav_start is not None and line and not line[0].isspace() and line[0] != "#":
            nav_end = i
            break

    if nav_start is None:
        return None

    nav_lines = lines[nav_start:nav_end]
    return "\n".join(nav_lines)


def load_repo_nav(repos_dir: Path, repo_dir: str, docs_prefix: str) -> list | None:
    """Load and prefix the nav from a repo's mkdocs.yml."""
    mkdocs_path = repos_dir / repo_dir / "mkdocs.yml"
    if not mkdocs_path.exists():
        print(f"  ⚠ {mkdocs_path} not found, skipping", file=sys.stderr)
        return None

    with open(mkdocs_path) as f:
        nav_yaml = extract_nav_section(f.read())

    if not nav_yaml:
        print(f"  ⚠ No nav in {mkdocs_path}, skipping", file=sys.stderr)
        return None

    nav = yaml.safe_load(nav_yaml).get("nav")
    if not nav:
        return None

    return prefix_paths(nav, docs_prefix)


def count_pages(nav: list) -> int:
    """Count leaf pages in a nav tree."""
    count = 0
    for item in nav:
        if isinstance(item, str):
            count += 1
        elif isinstance(item, dict):
            for value in item.values():
                if isinstance(value, str):
                    count += 1
                elif isinstance(value, list):
                    count += count_pages(value)
    return count


def nav_to_yaml(nav: list, indent: int = 2) -> str:
    """Render a nav list to YAML string with proper indentation."""
    lines = []
    prefix = " " * indent

    for item in nav:
        if isinstance(item, str):
            lines.append(f"{prefix}- {item}")
        elif isinstance(item, dict):
            for key, value in item.items():
                if isinstance(value, str):
                    lines.append(f"{prefix}- {key}: {value}")
                elif isinstance(value, list):
                    lines.append(f"{prefix}- {key}:")
                    lines.append(nav_to_yaml(value, indent + 4))

    return "\n".join(lines)


def main():
    site_dir = Path(__file__).resolve().parent.parent
    mkdocs_path = site_dir / "mkdocs.yml"

    # Determine repos directory
    if len(sys.argv) > 1:
        repos_dir = Path(sys.argv[1]).resolve()
    else:
        repos_dir = site_dir.parent

    print(f"Assembling nav from repos in {repos_dir}")

    # Read existing mkdocs.yml and find the nav: line
    with open(mkdocs_path) as f:
        content = f.read()

    lines = content.split("\n")
    nav_line_idx = None
    for i, line in enumerate(lines):
        if line.rstrip() == "nav:":
            nav_line_idx = i
            break

    if nav_line_idx is None:
        print("ERROR: No 'nav:' line found in mkdocs.yml", file=sys.stderr)
        sys.exit(1)

    # Build the merged nav
    full_nav = [{"Home": "index.md"}]

    for repo_dir, section_title, docs_prefix in REPOS:
        repo_nav = load_repo_nav(repos_dir, repo_dir, docs_prefix)
        if repo_nav:
            full_nav.append({section_title: repo_nav})
            print(f"  ✓ {section_title}: {count_pages(repo_nav)} pages")

    # Render nav YAML
    nav_yaml = "nav:\n" + nav_to_yaml(full_nav)

    # Replace everything from nav: onwards
    header = "\n".join(lines[:nav_line_idx])
    new_content = header + "\n" + nav_yaml + "\n"

    with open(mkdocs_path, "w") as f:
        f.write(new_content)

    total = count_pages(full_nav)
    print(f"Nav assembled: {total} total pages written to {mkdocs_path}")


if __name__ == "__main__":
    main()
