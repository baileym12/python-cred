import click
import json
from pathlib import Path
from datetime import datetime
from ..core.storage import SecretStorage, Secret
from ..core.audit import AuditLogger

@click.group()
def cli():
    """Python Credential Manager - Secure Secrets Management CLI"""
    pass

@cli.command()
def init():
    """Initialize the credential manager."""
    storage = SecretStorage()
    audit = AuditLogger()
    audit.log("system", "init", "Initialized credential manager")
    click.echo("Credential manager initialized successfully!")

@cli.command()
@click.argument('name')
@click.argument('value')
@click.option('--type', 'secret_type', default='api_key', help='Type of secret (api_key, token, password)')
@click.option('--env', 'environment', default='default', help='Environment (e.g., dev, prod)')
@click.option('--rotation', 'rotation_days', type=int, help='Days until rotation is required')
def store(name, value, secret_type, environment, rotation_days):
    """Store a new secret."""
    try:
        storage = SecretStorage()
        audit = AuditLogger()

        # Create rotation policy if specified
        rotation_policy = None
        if rotation_days:
            rotation_policy = {
                "days_until_rotation": rotation_days,
                "last_rotated": datetime.utcnow().isoformat()
            }

        # Create and store the secret
        secret = Secret(
            name=name,
            value=value,
            secret_type=secret_type,
            environment=environment,
            rotation_policy=rotation_policy
        )
        storage.store(secret)
        
        audit.log("store", name, f"Stored {secret_type} for {environment}")
        click.echo(f"Secret '{name}' stored successfully!")
    except Exception as e:
        click.echo(f"Error storing secret: {str(e)}", err=True)

@cli.command()
@click.argument('name')
def get(name):
    """Retrieve a secret."""
    try:
        storage = SecretStorage()
        audit = AuditLogger()
        
        secret = storage.retrieve(name)
        if not secret:
            click.echo(f"Secret '{name}' not found!", err=True)
            return

        # Check if rotation is needed
        if secret.rotation_policy:
            last_rotated = datetime.fromisoformat(secret.rotation_policy["last_rotated"])
            days_until_rotation = secret.rotation_policy["days_until_rotation"]
            days_since_rotation = (datetime.utcnow() - last_rotated).days
            
            if days_since_rotation >= days_until_rotation:
                click.echo(f"Warning: Secret '{name}' is due for rotation!", err=True)

        audit.log("retrieve", name, f"Retrieved {secret.secret_type}")
        click.echo(secret.value)
    except Exception as e:
        click.echo(f"Error retrieving secret: {str(e)}", err=True)

@cli.command()
@click.argument('name')
def delete(name):
    """Delete a secret."""
    try:
        storage = SecretStorage()
        audit = AuditLogger()
        
        if storage.delete(name):
            audit.log("delete", name, "Secret deleted")
            click.echo(f"Secret '{name}' deleted successfully!")
        else:
            click.echo(f"Secret '{name}' not found!", err=True)
    except Exception as e:
        click.echo(f"Error deleting secret: {str(e)}", err=True)

@cli.command()
@click.argument('name')
@click.argument('new_value')
def rotate(name, new_value):
    """Rotate a secret's value."""
    try:
        storage = SecretStorage()
        audit = AuditLogger()
        
        if storage.rotate(name, new_value):
            audit.log("rotate", name, "Secret rotated")
            click.echo(f"Secret '{name}' rotated successfully!")
        else:
            click.echo(f"Secret '{name}' not found!", err=True)
    except Exception as e:
        click.echo(f"Error rotating secret: {str(e)}", err=True)

@cli.command()
@click.option('--env', 'environment', help='Filter by environment')
@click.option('--type', 'secret_type', help='Filter by secret type')
def list(environment, secret_type):
    """List all secrets."""
    try:
        storage = SecretStorage()
        secrets = storage.list_secrets()
        
        # Apply filters
        if environment:
            secrets = [s for s in secrets if s["environment"] == environment]
        if secret_type:
            secrets = [s for s in secrets if s["secret_type"] == secret_type]

        if not secrets:
            click.echo("No secrets found.")
            return

        # Format output
        for secret in secrets:
            click.echo(f"\nName: {secret['name']}")
            click.echo(f"Type: {secret['secret_type']}")
            click.echo(f"Environment: {secret['environment']}")
            click.echo(f"Created: {secret['created_at']}")
            click.echo(f"Last Updated: {secret['updated_at']}")
            if secret.get('last_rotated'):
                click.echo(f"Last Rotated: {secret['last_rotated']}")
            if secret.get('rotation_policy'):
                click.echo(f"Rotation Policy: Every {secret['rotation_policy']['days_until_rotation']} days")
            click.echo("-" * 40)
    except Exception as e:
        click.echo(f"Error listing secrets: {str(e)}", err=True)

@cli.command()
def audit_log():
    """View the audit log."""
    try:
        audit = AuditLogger()
        logs = audit.get_logs()
        
        if not logs:
            click.echo("No audit logs found.")
            return

        for log in logs:
            click.echo(f"\nTimestamp: {log['timestamp']}")
            click.echo(f"Action: {log['action']}")
            click.echo(f"Target: {log['target']}")
            click.echo(f"Details: {log['details']}")
            click.echo("-" * 40)
    except Exception as e:
        click.echo(f"Error viewing audit log: {str(e)}", err=True)

if __name__ == '__main__':
    cli()
