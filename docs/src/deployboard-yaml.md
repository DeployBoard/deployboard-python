# deployboard.yaml

## File

DeployBoard can manage dependencies and automatically build a service network map all from a yaml file in each git repository.

An example file might look like this.

TODO: What about multiple applications/services in the same repo?

```
name: my-example-service
domain:
  - name: example.com
  - paths:
      - /test
      - /v2/test
  - methods:
      - GET
      - PUT
      - POST
      - OPTIONS
depends:
  - service1
  - service2
  - service4
  - service12
  - api.dropboxapi.com
```


Admin -> Checkout -> Card
                -> Thing2

## Development

Of course, you are free to use whatever editor and environment you like.

A runtime is provided via Docker.

!!! Note
    The following commands are run from the project root.

### Virtual Environment

To ensure everyone has a similar environment, we create a virtual environment using the following commands.


To leave the virtual environment, simply run `deactivate`.

After leaving, you can delete the virtual environment by simply running `rm -rf venv` from the project root.

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
