# Quick Start

!!! note
    This guide gets DeployBoard up and running, but not necessarily production ready.
    Read the full [Deployment](index.md) guide to make your install production ready.

## Install

The quickest way to get an instance of DeployBoard up and running is using docker-compose.

```
git clone https://github.com/DeployBoard/deployboard
cd deployboard
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements-dev.txt
docker-compose up -d --build
python3 ./scripts/first_user.py
```

## Details

In case you don't know what any of the commands above do.

We clone the git repo.
`git clone https://github.com/DeployBoard/deployboard`

Change directory into the repo.
`cd deployboard`

Create a virtual environment so our install dependencies are isolated in a temporary workspace.
`python3 -m venv venv`

Activate our virtual environment.
`source venv/bin/activate`

Install our requirements. These will get installed within your virtual environment, so you don't have to worry about conflicts.
`pip3 install -r requirements-dev.txt`

Start the docker containers using docker-compose. The --build flag will force building the containers from scratch.
`docker-compose up -d --build`

Once the MongoDB container is running, you can run the first_user script to create the account and first admin user.
`python3 ./scripts/first_user.py`
