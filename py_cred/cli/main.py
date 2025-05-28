import click
from rich.console import Console
from rich.table import Table
from ..core.storage import SecretStorage, Secret
from ..core.crypto import CryptoManager

console = Console()
storage = SecretStorage()
crypto = CryptoManager()

@click.group()
def cli():
    """Credential Manager CLI"""
    pass

@cli.command()
def init():
    """Initialize the credential manager"""
    master_key = crypto.generate_master_key()
    console.print(f"[green]Initialized with master key: {master_key}[/green]")

@cli.command()
@click.option("--name", required=True)
@click.option("--value", required=True)
@click.option("--type", required=True)
def add(name, value, type):
    """Add a new credential"""
    secret = Secret(name, value, type)
    storage.store(secret)
    console.print(f"[green]Added credential: {name}[/green]")

@cli.command()
@click.option("--name", required=True)
def get(name):
    """Get a credential"""
    console.print(f"[yellow]Getting credential: {name}[/yellow]")

if __name__ == "__main__":
    cli()
