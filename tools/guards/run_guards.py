import pathlib
import sys
from typing import Callable, List, Tuple

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.guards import agents_guard, ascii_guard, docs_guard, roadmap_guard

Guard = Tuple[str, Callable[[], None]]


def run_guard(name: str, func: Callable[[], None]) -> bool:
    try:
        func()
        print(f"{name} guard: PASS")
        return True
    except SystemExit as exc:
        print(f"{name} guard: FAIL", file=sys.stderr)
        if exc.code not in (0, None):
            return False
        return False
    except Exception as exc:  # pragma: no cover - safety net
        print(f"{name} guard: ERROR - {exc}", file=sys.stderr)
        return False


def main() -> None:
    guards: List[Guard] = [
        ("ASCII", ascii_guard.main),
        ("Agents", agents_guard.main),
        ("Docs", docs_guard.main),
        ("Roadmap", roadmap_guard.main),
    ]

    failures = 0
    for name, func in guards:
        if not run_guard(name, func):
            failures += 1
    if failures:
        raise SystemExit(1)

    print("All guards passed.")


if __name__ == "__main__":
    main()
