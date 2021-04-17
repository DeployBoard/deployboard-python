# Contributing

## Process

DeployBoard works on a [Fork & Pull](https://reflectoring.io/github-fork-and-pull/){:target="_blank"} based system.

If you want to implement a new feature, or fix an existing bug, first search our [open issues](https://github.com/DeployBoard/deployboard/issues){:target="_blank"} to see if an issue already exists.

If you find an existing issue, please first comment on the issue that you are going to work on. This helps reduce duplicated work.

If you do not find an existing issue, please [open a new issue](https://github.com/DeployBoard/deployboard/issues/new/choose){:target="_blank"} filling out the provided issue templates before starting work.

## Development

Of course, you are free to use whatever editor and environment you like.

A runtime is provided via Docker.

!!! Note
    The following commands are run from the project root.

### Virtual Environment

To ensure everyone has a similar environment, we create a virtual environment using the following commands.

```
# Create the virual environment.
python3 -m venv venv

# Activate the virtual environment.
source venv/bin/activate
```

To leave the virtual environment, simply run `deactivate`.

### Build Bootstrap

The UI requires bootstrap. We use some custom scss variables which requires building bootstrap.

You can build bootstrap using the provided script located in the `/scripts/` directory.

```
bash ./scripts/build_bootstrap.sh
```

### Start the App

After building bootstrap, you will want to start the application. You can do this with Docker.

```
docker-compose up -d --build
```

The application should be running now at `localhost:80`, but you still need to seed the database before you can log in.

### Seed the DB

Once the application is up, you can seed the database using the provided script in the `/scripts/` directory.

```
python3 ./scripts/db_seed.py
```

### Usage

Once you have the database seeded, you will be able to log in.

The usernames created as part of the seed script are:

- admin@example.com (role: Admin)
- editor@example.com (role: Editor)
- viewer@example.com (role: Viewer)

The password provided for all development users is the string `secret`.

!!! Note
    Disabled users are also created for each role. The disabled users were created for testing access controls.

API Keys are also created, you can find them at `localhost/settings/apikeys`.

## Testing

Tests are run using pyteset on Docker.

We currently build our own docker image locally to use for pytest. To build the deployboard-pytest docker image run the following command.

```
docker build --no-cache -t deployboard-pytest:latest -f tests/Dockerfile .
```

Now that we have the image built, we can run the container passing in our code.

```
docker run --rm -it -v ${PWD}:/app deployboard-pytest
```

This will run all of our tests and generate a coverage report at the root of the project `/htmlcov/index.html`

## Docs

Docs are hosted via Docker, and can be started as part of the docker-compose script mentioned in the above section.

!!! Note
    If you have already started the application with `docker-compose` the Docs will be available at: `localhost:8000`.

The Docs source code is found in `/src/docs/` of the project root.

If you only want to run the Docs, and not the rest of the application, you can do so by running this command

```
docker run --rm -it -p 8000:8000 -v ${PWD}/docs:/docs squidfunk/mkdocs-material
```

Just like running via `docker-compose`, the Docs will be available at `localhost:8000`.

## Committing

We use pre-commit hooks to verify some things prior to committing to source control.

To enable this, you need to run the following commands.

!!! Note
    Make sure to set up your [Virtual Environment](contributing.md#virtual-environment).

```
# Install pre-commit and any other dev dependencies.
pip3 install -r requirements-dev.txt

# Install git hooks in the .git directory.
pre-commit install
```
