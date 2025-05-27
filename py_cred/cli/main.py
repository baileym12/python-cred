import click
from rich.console import Console

console = Console()

@click.group()
def cli():
    """Credential Manager CLI"""
    pass

@cli.command()
def init():
    """Initialize the credential manager"""
    console.print("[green]Initializing credential manager...[/green]")

if __name__ == "__main__":
    cli()
