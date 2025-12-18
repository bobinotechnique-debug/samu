import argparse
import pathlib
import sys
from typing import List

REQUIRED_AGENTS = [
    "agents/backend.md",
    "agents/frontend.md",
    "agents/devops.md",
    "agents/docs.md",
]


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate agent contracts")
    parser.add_argument(
        "--repo-root",
        default=pathlib.Path(__file__).resolve().parents[2],
        type=pathlib.Path,
        help="Repository root path",
    )
    args = parser.parse_args()
    repo_root = args.repo_root

    missing: List[str] = []
    precedence: List[str] = []
    headers: List[str] = []

    for agent in REQUIRED_AGENTS:
        path = repo_root / agent
        if not path.exists():
            missing.append(agent)
            continue
        content = path.read_text(encoding="utf-8")
        if "Root agent (AGENT.md) overrides" not in content:
            precedence.append(agent)
        first_line = content.splitlines()[0] if content.splitlines() else ""
        if not first_line.strip().startswith("#"):
            headers.append(agent)

    if missing:
        print(f"Agents guard failed. Missing agents: {', '.join(missing)}", file=sys.stderr)
    if precedence:
        print(
            f"Agents guard failed. Precedence not declared in: {', '.join(precedence)}",
            file=sys.stderr,
        )
    if headers:
        print(
            f"Agents guard failed. Missing agent header lines in: {', '.join(headers)}",
            file=sys.stderr,
        )

    if missing or precedence or headers:
        raise SystemExit(1)

    print("Agents guard passed.")


if __name__ == "__main__":
    main()
