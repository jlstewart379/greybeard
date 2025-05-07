import json
from pathlib import Path
from greybeard.models.change_model import Suggestion, ChangeBlock, DiffBlock
from dataclasses import asdict
from typing import List
from rich.console import Console
from rich.syntax import Syntax
from rich.prompt import Prompt
from greybeard.diff_engine import apply_diff

SUGGESTION_DIR = Path(".greybeard/suggestions")
SUGGESTION_DIR.mkdir(parents=True, exist_ok=True)
console = Console()

def save_suggestion(suggestion: Suggestion, slug: str):
    with open(SUGGESTION_DIR / f"{slug}.json", "w") as f:
        json.dump(asdict(suggestion), f, indent=2)

def load_suggestions() -> List[Suggestion]:
    suggestions = []
    for file in SUGGESTION_DIR.glob("*.json"):
        with open(file) as f:
            data = json.load(f)
            blocks = [
                ChangeBlock(
                    label=b["label"],
                    reason=b["reason"],
                    diff=DiffBlock(**b["diff"]),
                    status=b.get("status", "saved"),
                    timestamp=b.get("timestamp", "")
                ) for b in data["change_blocks"]
            ]
            suggestions.append(Suggestion(path=data["path"], change_blocks=blocks))
    return suggestions

def update_suggestion_status(slug: str, status: str):
    path = SUGGESTION_DIR / f"{slug}.json"
    if not path.exists():
        return
    with open(path) as f:
        data = json.load(f)
    for block in data["change_blocks"]:
        block["status"] = status
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def preview_suggestion(suggestion: Suggestion):
    console.print(f"[bold underline]Previewing suggestion for:[/] {suggestion.path}\n")
    for i, block in enumerate(suggestion.change_blocks):
        console.print(f"[bold yellow]Change {i+1}: {block.label}[/] – {block.reason}")
        original = "".join(block.diff.original)
        replacement = "".join(block.diff.replacement)
        diff_display = f"--- ORIGINAL ---\n{original}\n--- REPLACEMENT ---\n{replacement}\n"
        syntax = Syntax(diff_display, "diff", theme="ansi_dark", line_numbers=False)
        console.print(syntax)
        console.print("\n")

def review_and_apply(suggestion: Suggestion, slug: str):
    preview_suggestion(suggestion)
    action = Prompt.ask("What would you like to do?", choices=["apply", "skip", "save"], default="save")

    if action == "apply":
        file_path = Path(suggestion.path)
        if not file_path.exists():
            console.print(f"[red]Error: File {file_path} not found.[/red]")
            return
        new_content = "\n".join(suggestion.change_blocks[0].diff.replacement) + "\n"
        apply_diff(file_path, new_content)
        update_suggestion_status(slug, "applied")
        console.print(f"[green]Change applied to {file_path}[/green]")

    elif action == "skip":
        update_suggestion_status(slug, "skipped")
        console.print("[yellow]Suggestion skipped.[/yellow]")

    elif action == "save":
        update_suggestion_status(slug, "saved")
        console.print("[cyan]Suggestion saved for later.[/cyan]")

