import typer
from greybeard.chat_engine import run_chat

app = typer.Typer()

@app.command()
def chat(path: str = "."):
    run_chat(path)

if __name__ == "__main__":
    app()
