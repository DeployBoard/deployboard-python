# DeployBoard Tests

Tests are run within a Docker container.

Run the following commands from the root of the repository.

First build the test docker container.  

```
docker build --no-cache -t deployboard-pytest:latest -f tests/Dockerfile .
```

Then run the container volume mounting the entire repo.

```
docker run --rm -it -v ${PWD}:/app deployboard-pytest
```

If you want to run your tests against a real db, set the `MONGO_URI` environment variable, and add the `--network="host"` flag.

```
docker run --rm -it -v ${PWD}:/app -e MONGO_URI=localhost:27017 --network="host" deployboard-pytest
```
