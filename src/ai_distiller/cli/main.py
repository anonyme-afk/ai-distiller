"""
main.py
Main CLI entry point using Typer.
"""
import typer
from rich.console import Console

app = typer.Typer(help="AI-Distiller CLI: Build specialized AI assistants via model distillation.")
console = Console()

@app.command()
def init(domain: str = typer.Option("general", help="Domain for the new project")):
    """Initialize a new distillation project."""
    console.print(f"[bold green]Initializing new project for domain: {domain}[/bold green]")
    # Stub

@app.command()
def wizard():
    """Interactive configuration wizard."""
    from .wizard import run_wizard
    run_wizard()

@app.command()
def generate(examples: int = typer.Option(1000, help="Number of examples to generate")):
    """Generate training data."""
    console.print(f"[bold blue]Generating {examples} examples...[/bold blue]")
    # Stub

@app.command()
def clean():
    """Clean generated data."""
    console.print("[bold blue]Cleaning dataset...[/bold blue]")
    # Stub

@app.command()
def train():
    """Start fine-tuning process."""
    console.print("[bold magenta]Starting distillation/fine-tuning process...[/bold magenta]")
    # Stub

@app.command()
def serve():
    """Start API server."""
    import uvicorn
    console.print("[bold green]Starting API Server on port 8000...[/bold green]")
    uvicorn.run("ai_distiller.api.server:app", host="0.0.0.0", port=8000, reload=True)

@app.command()
def test():
    """Test the generated model."""
    console.print("[bold cyan]Testing model...[/bold cyan]")
    # Stub

if __name__ == "__main__":
    app()
