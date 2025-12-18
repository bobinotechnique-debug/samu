import argparse
import pathlib
import re
import sys
from typing import List

REQUIRED_INDEXES = [
    "docs/INDEX.md",
    "docs/roadmap/INDEX.md",
    "docs/roadmap/phase0/INDEX.md",
    "docs/specs/INDEX.md",
    "docs/api/INDEX.md",
    "docs/ux/INDEX.md",
    "docs/ops/INDEX.md",
    "specs/INDEX.md",
    "api/INDEX.md",
    "ux/INDEX.md",
    "ops/INDEX.md",
]

AGENT_ERRORS_PATH = "docs/ops/agent_errors.md"
REQUIRED_SECTIONS = ["## Summary", "## How to add an entry", "## Entry template", "## Known Failure Patterns"]
REQUIRED_FIELDS = [
    "Date:",
    "Context (step ref):",
    "Symptom:",
    "Root cause:",
    "Fix:",
    "Prevention:",
    "Files touched:",
]


def validate_indexes(repo_root: pathlib.Path) -> List[str]:
    missing: List[str] = []
    for relative in REQUIRED_INDEXES:
        if not (repo_root / relative).exists():
            missing.append(relative)
    return missing


def validate_index_references(repo_root: pathlib.Path) -> List[str]:
    reference_errors: List[str] = []
    pattern = re.compile(r"^-\s+([^\s]+)", re.MULTILINE)

    for relative in REQUIRED_INDEXES:
        path = repo_root / relative
        if not path.exists():
            continue
        content = path.read_text(encoding="utf-8")
        for match in pattern.finditer(content):
            target = match.group(1)
            if not target.endswith(".md"):
                continue
            target_path = repo_root / target
            if not target_path.exists():
                reference_errors.append(f"{target} referenced in {relative} is missing")
    return reference_errors


def find_orphan_docs(repo_root: pathlib.Path) -> List[str]:
    orphan_folders: List[str] = []
    docs_root = repo_root / "docs"
    if not docs_root.exists():
        return orphan_folders

    for directory in docs_root.rglob("*"):
        if not directory.is_dir():
            continue
        markdown_files = list(directory.glob("*.md"))
        if markdown_files:
            index_file = directory / "INDEX.md"
            if not index_file.exists():
                orphan_folders.append(str(directory.relative_to(repo_root)))
    return orphan_folders


def validate_agent_error_template(repo_root: pathlib.Path) -> List[str]:
    issues: List[str] = []
    template_path = repo_root / AGENT_ERRORS_PATH
    if not template_path.exists():
        issues.append(f"{AGENT_ERRORS_PATH} is missing")
        return issues

    content = template_path.read_text(encoding="utf-8")
    for section in REQUIRED_SECTIONS:
        if section not in content:
            issues.append(f"Missing section '{section}' in {AGENT_ERRORS_PATH}")
    for field in REQUIRED_FIELDS:
        if field not in content:
            issues.append(f"Missing field '{field}' in {AGENT_ERRORS_PATH}")
    return issues


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate documentation guardrails")
    parser.add_argument(
        "--repo-root",
        default=pathlib.Path(__file__).resolve().parents[2],
        type=pathlib.Path,
        help="Repository root path",
    )
    args = parser.parse_args()
    repo_root = args.repo_root

    missing = validate_indexes(repo_root)
    reference_errors = validate_index_references(repo_root)
    orphan_folders = find_orphan_docs(repo_root)
    template_issues = validate_agent_error_template(repo_root)

    if missing:
        print(f"Docs guard failed. Missing files: {', '.join(missing)}", file=sys.stderr)
    if reference_errors:
        print("Docs guard failed. Index files reference missing targets.", file=sys.stderr)
        for entry in reference_errors:
            print(entry, file=sys.stderr)
    if orphan_folders:
        print("Docs guard failed. Directories with markdown files are missing INDEX.md.", file=sys.stderr)
        for folder in orphan_folders:
            print(f"Missing INDEX.md in {folder}", file=sys.stderr)
    if template_issues:
        print("Docs guard failed. Agent error log template is incomplete.", file=sys.stderr)
        for issue in template_issues:
            print(issue, file=sys.stderr)

    if missing or reference_errors or orphan_folders or template_issues:
        raise SystemExit(1)

    print("Docs guard passed.")


if __name__ == "__main__":
    main()
