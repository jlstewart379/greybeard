from pathlib import Path
import difflib

def generate_diff(original: str, modified: str, filename: str = "file") -> str:
    original_lines = original.splitlines(keepends=True)
    modified_lines = modified.splitlines(keepends=True)
    diff = difflib.unified_diff(
        original_lines, modified_lines,
        fromfile=f"a/{filename}",
        tofile=f"b/{filename}"
    )
    return ''.join(diff)

def apply_diff(filepath: Path, new_content: str):
    with open(filepath, 'w') as f:
        f.write(new_content)
