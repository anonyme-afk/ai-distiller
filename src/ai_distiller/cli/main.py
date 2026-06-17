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
    import yaml
    from pathlib import Path
    Path("config/domains").mkdir(parents=True, exist_ok=True)
    with open(f"config/domains/{domain}.yaml", "w") as f:
        yaml.dump({"domain": domain, "teacher": {"model": "claude-3-5-sonnet-20241022"}}, f)
    console.print("[bold green]Project initialized.[/bold green]")

@app.command()
def wizard():
    """Interactive configuration wizard."""
    from .wizard import run_wizard
    run_wizard()

@app.command()
def generate(examples: int = typer.Option(10, help="Number of examples to generate"), domain: str = typer.Option("support_client", help="Domain config to use")):
    """Generate training data."""
    console.print(f"[bold blue]Generating {examples} examples for {domain}...[/bold blue]")
    from ai_distiller.distillation.teacher import TeacherConnector
    from ai_distiller.distillation.data_generator import DataGenerator
    import json
    import os
    
    try:
        teacher = TeacherConnector()
        generator = DataGenerator(teacher)
        dataset = generator.generate(domain=domain, num_examples=examples)
        
        os.makedirs("outputs", exist_ok=True)
        with open("outputs/generated_dataset.json", "w") as f:
            json.dump(dataset, f, indent=2)
        console.print("[bold green]Generation complete. Saved to outputs/generated_dataset.json[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error during generation:[/bold red] {str(e)}")
        raise typer.Exit(code=1)

@app.command()
def clean(input_file: str = typer.Option("outputs/generated_dataset.json", help="File to clean")):
    """Clean generated data."""
    console.print(f"[bold blue]Cleaning dataset {input_file}...[/bold blue]")
    from ai_distiller.distillation.cleaner import DataCleaner
    import json
    import os
    
    if not os.path.exists(input_file):
        console.print(f"[bold red]Error:[/bold red] Input file '{input_file}' not found.")
        raise typer.Exit(code=1)
        
    try:
        with open(input_file, "r") as f:
            dataset = json.load(f)
            
        cleaner = DataCleaner()
        cleaned = cleaner.clean(dataset)
        
        with open("outputs/cleaned_dataset.json", "w") as f:
            json.dump(cleaned, f, indent=2)
        console.print("[bold green]Cleaning complete. Saved to outputs/cleaned_dataset.json[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error during cleaning:[/bold red] {str(e)}")
        raise typer.Exit(code=1)

@app.command()
def train(input_file: str = typer.Option("outputs/cleaned_dataset.json", help="File to train on")):
    """Start fine-tuning process."""
    console.print(f"[bold magenta]Starting distillation process using {input_file}...[/bold magenta]")
    from ai_distiller.distillation.trainer import Trainer
    import json
    import os
    
    if not os.path.exists(input_file):
        console.print(f"[bold red]Error:[/bold red] Input file '{input_file}' not found.")
        raise typer.Exit(code=1)
        
    try:
        with open(input_file, "r") as f:
            dataset = json.load(f)
            
        trainer = Trainer()
        result = trainer.train(dataset)
        console.print(f"[bold green]Training output saved at {result['model_path']}[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error during training:[/bold red] {str(e)}")
        raise typer.Exit(code=1)

@app.command()
def serve():
    """Start API server."""
    import uvicorn
    console.print("[bold green]Starting API Server on port 8000...[/bold green]")
    uvicorn.run("ai_distiller.api.server:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    app()
