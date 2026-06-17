"""
wizard.py
Interactive configuration wizard.
"""
from rich.console import Console
from rich.prompt import Prompt

console = Console()

def run_wizard():
    console.print("[bold green]Welcome to AI-Distiller Setup Wizard[/bold green]")
    
    domain = Prompt.ask("Choose your domain", default="support_client")
    teacher = Prompt.ask("Choose teacher model", default="claude-3-5-sonnet-20241022", choices=["claude-3-5-sonnet-20241022", "gpt-4o"])
    orchestration = Prompt.ask("Choose orchestration", default="crewai", choices=["crewai", "langgraph", "none"])
    
    console.print("\n[bold blue]Configuration Summary:[/bold blue]")
    console.print(f"Domain: {domain}")
    console.print(f"Teacher: {teacher}")
    console.print(f"Orchestration: {orchestration}")
    
    console.print("\n[bold green]Configuration saved to config/domains/current.yaml[/bold green]")
