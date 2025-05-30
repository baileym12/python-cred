# Python Credential Manager

A self-hosted, developer-friendly CLI tool for managing, rotating, and auditing API keys, tokens, and credentials across environments.

## Features

- 🔐 Secure encryption of credentials using modern cryptographic methods
- 🔄 Automatic credential rotation based on configurable policies
- 📝 Comprehensive audit logging
- 🛡️ Environment-based credential management
- 🔑 Multiple credential types support (API keys, tokens, passwords)
- 📊 Rich CLI interface with clear feedback

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

1. Initialize the credential manager:
```bash
python -m py_cred init
```

2. Add a new credential:
```bash
python -m py_cred add --name "github-token" --type "api-key" --value "your-secret-value"
```

3. Retrieve a credential:
```bash
python -m py_cred get --name "github-token"
```

## Security Features

- Credentials are encrypted at rest using AES-256-GCM
- Master key is never stored in plaintext
- Audit logging for all operations
- Automatic credential rotation policies
- Environment isolation

## Development

This project uses:
- `cryptography` for secure encryption
- `click` for CLI interface
- `rich` for beautiful terminal output
- `pydantic` for data validation
- `python-dotenv` for configuration management

## License

MIT License
