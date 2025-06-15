# Python Credential Manager

A secure command-line tool for managing API keys, tokens, and secrets with encryption, rotation policies, and audit logging.

## Features

- 🔐 **Secure Storage**: All secrets are encrypted using Fernet (symmetric encryption)
- 🔄 **Rotation Policies**: Set up automatic rotation reminders for your secrets
- 📝 **Audit Logging**: Track all operations with detailed audit logs
- 🌍 **Environment Support**: Organize secrets by environment (dev, prod, etc.)
- 🔍 **Secret Types**: Categorize secrets by type (api_key, token, password)
- 📊 **Filtering & Search**: List and filter secrets by environment and type
- 🔑 **Master Key Management**: Secure master key storage with rotation support

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/python-cred.git
cd python-cred

# Install the package
pip install -e .
```

## Usage

### Initialization

First, initialize the credential manager:

```bash
python -m py_cred init
```

This will create the necessary storage structure and generate a master key.

### Storing Secrets

Store a new secret with various options:

```bash
# Basic usage
python -m py_cred store my-api-key "secret-value"

# With type and environment
python -m py_cred store my-api-key "secret-value" --type api_key --env prod

# With rotation policy (30 days)
python -m py_cred store my-api-key "secret-value" --type api_key --env prod --rotation 30
```

Options:
- `--type`: Secret type (api_key, token, password) [default: api_key]
- `--env`: Environment (dev, prod, etc.) [default: default]
- `--rotation`: Days until rotation is required

### Retrieving Secrets

Get a secret's value:

```bash
python -m py_cred get my-api-key
```

If the secret has a rotation policy and is due for rotation, you'll see a warning message.

### Listing Secrets

List all stored secrets:

```bash
# List all secrets
python -m py_cred list

# Filter by environment
python -m py_cred list --env prod

# Filter by type
python -m py_cred list --type api_key
```

The output includes:
- Secret name
- Type
- Environment
- Creation date
- Last update date
- Last rotation date (if applicable)
- Rotation policy (if set)

### Rotating Secrets

Rotate a secret's value:

```bash
python -m py_cred rotate my-api-key "new-secret-value"
```

This will:
1. Update the secret's value
2. Update the last rotation timestamp
3. Log the rotation in the audit log

### Deleting Secrets

Remove a secret:

```bash
python -m py_cred delete my-api-key
```

### Viewing Audit Logs

View the audit log:

```bash
python -m py_cred audit_log
```

The audit log includes:
- Timestamp
- Action performed
- Target secret
- Additional details

## Security Features

### Encryption

- All secrets are encrypted using Fernet (symmetric encryption)
- Master key is stored securely
- Support for master key rotation

### Rotation Policies

- Set mandatory rotation periods for secrets
- Automatic warnings when rotation is due
- Tracking of last rotation date

### Audit Logging

- All operations are logged with timestamps
- Includes action type, target, and details
- Helps with compliance and security monitoring

## Best Practices

1. **Regular Rotation**
   - Set up rotation policies for sensitive secrets
   - Rotate secrets before they expire
   - Use the `--rotation` flag when storing secrets

2. **Environment Separation**
   - Use different environments for dev/prod
   - Keep production secrets separate
   - Use the `--env` flag to organize secrets

3. **Secret Types**
   - Categorize secrets by type
   - Use appropriate types for different secrets
   - Helps with organization and filtering

4. **Audit Logging**
   - Regularly review audit logs
   - Monitor for suspicious activity
   - Use logs for compliance purposes

## Development

### Project Structure

```
python-cred/
├── py_cred/
│   ├── cli/
│   │   └── main.py
│   ├── core/
│   │   ├── crypto.py
│   │   ├── storage.py
│   │   └── audit.py
│   └── __init__.py
├── tests/
├── setup.py
└── README.md
```

### Running Tests

```bash
pytest
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.