# Ember Nexus: Action Attest

This GitHub action is used within the Ember Nexus organization to handle attestation and provenance tasks, including:
- Generating merkle trees
- Initiating Originstamp certificates using the merkle tree's root hash

## Usage



## Available commands inside the container

```bash
pip install .
python -m src run ember-nexus app-plugin-experimental v0.0.3

ruff check
ruff check --fix
ruff format
```

## Available commands outside the container

```bash
docker build -t action:test -f docker/Dockerfile .
docker run -e GITHUB_TOKEN=github_pat_... -e ORIGINSTAMP_TOKEN=... action:test run ember-nexus app-plugin-experimental v0.0.3
```