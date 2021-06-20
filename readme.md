# Migration DB

A python script to migrate databases from a source database server to a destination database server

### Pre-requisites

- python3
- source database credentials set in the `.env` as `DB1_HOST`, `DB1_USER` and `DB1_PASSWORD`.
- destination database credentials set in the `.env` file as `DB2_HOST`, `DB2_USER` and `DB2_PASSWORD`.

### Setup

First, install the required packages.

```bash
pip install -r requirements.txt
```

### Running

```bash
python3 main.py
```