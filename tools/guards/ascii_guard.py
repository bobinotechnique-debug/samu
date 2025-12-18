import argparse
import pathlib
import subprocess
import sys
from typing import Iterable, List, Tuple

BINARY_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".bmp",
    ".svg",
    ".ico",
    ".pdf",
    ".zip",
    ".gz",
    ".tgz",
    ".xz",
    ".7z",
    ".tar",
    ".jar",
    ".exe",
    ".dll",
    ".pdb",
    ".so",
    ".dylib",
    ".mp3",
    ".mp4",
}


def list_tracked_files(repo_root: pathlib.Path) -> Iterable[pathlib.Path]:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_root), "ls-files"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        raise SystemExit(f"ASCII guard failed. Unable to list tracked files via git. {exc}") from exc

    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        yield repo_root / line.strip()


def find_non_ascii(path: pathlib.Path) -> Tuple[int, int]:
    line_number = 1
    try:
        data = path.read_bytes()
    except OSError as exc:
        raise SystemExit(f"ASCII guard failed. Unable to read {path}: {exc}") from exc

    for byte in data:
        if byte == 10:
            line_number += 1
            continue
        if byte > 127:
            return line_number, byte
    return 0, 0


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate ASCII-only tracked files")
    parser.add_argument(
        "--repo-root",
        default=pathlib.Path(__file__).resolve().parents[2],
        type=pathlib.Path,
        help="Repository root path",
    )
    args = parser.parse_args()
    repo_root = args.repo_root

    violations: List[str] = []

    for tracked_file in list_tracked_files(repo_root):
        extension = tracked_file.suffix.lower()
        if extension in BINARY_EXTENSIONS:
            continue
        if not tracked_file.exists():
            continue
        line_number, byte_value = find_non_ascii(tracked_file)
        if line_number:
            relative_path = tracked_file.relative_to(repo_root)
            violations.append(
                f"Non-ASCII byte {byte_value} detected in {relative_path} at line {line_number}."
            )

    if violations:
        print("ASCII guard failed. Non-ASCII content detected.", file=sys.stderr)
        for violation in violations:
            print(violation, file=sys.stderr)
        raise SystemExit(1)

    print("ASCII guard passed.")


if __name__ == "__main__":
    main()
