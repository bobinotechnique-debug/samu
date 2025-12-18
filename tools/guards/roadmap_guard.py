import argparse
import pathlib
import sys
from typing import List

ROOT_STEP = "roadmap/phase0/step-00-bootstrap.md"
DOCS_STEP = "docs/roadmap/phase0/step-01-harden-bootstrap.md"
DOCS_ROADMAP_INDEX = "docs/roadmap/INDEX.md"
REQUIRED_SECTIONS = ["## Goal", "## Deliverables", "## Acceptance Criteria", "## Tests", "## Risks"]


def validate_path_exists(repo_root: pathlib.Path, relative: str, message: str) -> None:
    target = repo_root / relative
    if not target.exists():
        print(message, file=sys.stderr)
        raise SystemExit(1)


def ensure_content_includes(path: pathlib.Path, required: List[str]) -> None:
    content = path.read_text(encoding="utf-8")
    missing_sections = [section for section in required if section not in content]
    if missing_sections:
        print(
            f"Roadmap guard failed. {path} missing sections: {', '.join(missing_sections)}",
            file=sys.stderr,
        )
        raise SystemExit(1)


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate roadmap guardrails")
    parser.add_argument(
        "--repo-root",
        default=pathlib.Path(__file__).resolve().parents[2],
        type=pathlib.Path,
        help="Repository root path",
    )
    args = parser.parse_args()
    repo_root = args.repo_root

    root_step_path = repo_root / ROOT_STEP
    docs_step_path = repo_root / DOCS_STEP
    docs_roadmap_index = repo_root / DOCS_ROADMAP_INDEX

    validate_path_exists(repo_root, ROOT_STEP, "Roadmap guard failed. Missing roadmap/phase0/step-00-bootstrap.md.")
    root_content = root_step_path.read_text(encoding="utf-8")
    if "## Status" not in root_content or "Done" not in root_content:
        print("Roadmap guard failed. Phase 0 bootstrap status must be marked Done.", file=sys.stderr)
        raise SystemExit(1)

    validate_path_exists(repo_root, DOCS_STEP, "Roadmap guard failed. Missing docs/roadmap/phase0/step-01-harden-bootstrap.md.")
    validate_path_exists(repo_root, DOCS_ROADMAP_INDEX, "Roadmap guard failed. Missing docs/roadmap/INDEX.md.")

    index_content = docs_roadmap_index.read_text(encoding="utf-8")
    if DOCS_STEP not in index_content:
        print(
            "Roadmap guard failed. docs/roadmap/INDEX.md must reference docs/roadmap/phase0/step-01-harden-bootstrap.md.",
            file=sys.stderr,
        )
        raise SystemExit(1)

    ensure_content_includes(docs_step_path, REQUIRED_SECTIONS)

    print("Roadmap guard passed.")


if __name__ == "__main__":
    main()
