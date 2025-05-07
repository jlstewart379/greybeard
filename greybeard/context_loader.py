import os
from pathlib import Path

IGNORED_DIRS = {".git", ".greybeard", "__pycache__", "node_modules"}
ALLOWED_EXTENSIONS = {".py", ".tf", ".sh", ".md"}

def parse_greybeardignore(path: Path):
    ignore_file = path / ".greybeardignore"
    patterns = set()
    if ignore_file.exists():
        with open(ignore_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    patterns.add(line)
    return patterns

def load_repo_context(path: str, max_files: int = 20, max_lines: int = 40) -> str:
    context = []
    root = Path(path)
    ignore_patterns = parse_greybeardignore(root)

    file_count = 0
    for file_path in sorted(root.rglob("*")):
        if file_count >= max_files:
            break
        if not file_path.is_file():
            continue
        if file_path.suffix not in ALLOWED_EXTENSIONS:
            continue
        if any(part in IGNORED_DIRS for part in file_path.parts):
            continue
        if any(str(file_path).startswith(str(root / pattern)) for pattern in ignore_patterns):
            continue

        try:
            with open(file_path, "r") as f:
                lines = f.readlines()
                snippet = ''.join(lines[:max_lines])
                rel_path = file_path.relative_to(root)
                context.append(f"# {rel_path}\n{snippet}\n")
                file_count += 1
        except Exception:
            continue

    return "\n".join(context)

