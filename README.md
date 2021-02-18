# DeployBoard

[![codecov](https://codecov.io/gh/DeployBoard/deployboard/branch/main/graph/badge.svg)](https://codecov.io/gh/DeployBoard/deployboard)

DeployBoard is a simple deployment tracking tool. Easily plugs in to any deployment tool or pipeline. Tracks DORA metrics, compliance, and more.

## Deployment

Build bootstrap with our custom scss from the root of this repository.

`bash scripts/build_bootstrap.sh`

Start the app.

`docker-compose up -d`

## Development

Virtual Environment

`python3 -m venv venv`

`source venv/bin/activate`

Start the app via docker.

`docker-compose up -d`
