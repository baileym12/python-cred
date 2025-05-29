# Python Credential Manager

A CLI tool for managing credentials securely.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python -m py_cred init
python -m py_cred add --name "github-token" --type "api-key" --value "your-secret"
python -m py_cred get --name "github-token"
```
