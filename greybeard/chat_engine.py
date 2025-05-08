import os
import json
import re
from uuid import uuid4
from openai import OpenAI
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from greybeard.context_loader import load_repo_context
from greybeard.models.change_model import DiffBlock, ChangeBlock, Suggestion
from greybeard.storage.suggestion_store import save_suggestion, review_and_apply

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
console = Console()

def parse_suggestion_from_reply(reply: str):
    match = re.search(r'```json(.*?)```', reply, re.DOTALL)
    if not match:
        return None

    try:
        raw_json = match.group(1).strip()
        data = json.loads(raw_json)
        block = ChangeBlock(
            label=data["label"],
            reason=data["reason"],
            diff=DiffBlock(**data["diff"])
        )
        suggestion = Suggestion(path=data["path"], change_blocks=[block])
        slug = f"{data['path'].replace('/', '_').replace('.', '-')}-{block.label.replace(' ', '_').lower()}-{uuid4().hex[:6]}"
        return slug, suggestion
    except Exception as e:
        raise ValueError(f"Invalid suggestion format: {e}")

def run_chat(path: str):
    console.print(Panel(f"[bold green]Greybeard Assistant Started[/bold green]\nLoaded path: {path}", title="greybeard"))

    context_summary = load_repo_context(path)
    system_message = f"You are Greybeard, an expert infrastructure advisor. The user is working in a codebase with the following context:\n\n{context_summary}"

    console.print("\n[bold]Type your question below. Type 'exit' to quit.[/bold]\n")

    while True:
        user_input = Prompt.ask("[bold blue]You[/bold blue]")

        if user_input.strip().lower() in ["exit", "quit"]:
            console.print("[italic grey]Session ended.[/italic grey]")
            break

        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_input},
                ]
            )
            reply = response.choices[0].message.content.strip()
        except Exception as e:
            reply = f"[Error communicating with OpenAI API: {e}]"

        console.print(Panel(reply, title="[bold magenta]Greybeard[/bold magenta]"))

        try:
            parsed = parse_suggestion_from_reply(reply)
            if parsed:
                slug, suggestion = parsed
                save_suggestion(suggestion, slug)
                review_and_apply(suggestion, slug)
        except Exception as e:
            console.print(f"[red]Failed to parse suggestion: {e}[/red]")

