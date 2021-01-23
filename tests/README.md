# DeployBoard Tests

Tests are run within a Docker container.

Run the following commands from the root of the repository.

First build the test docker container.  
Then run the container passing in the entire repo.

```
docker build --no-cache -t deployboard-pytest:latest -f tests/Dockerfile .
docker run --rm -it -v ${PWD}:/app -e PYTHONPATH=/app/:/app/src/:/app/src/api/ -e MONGO_URI=localhost:27017 -e APP_SECRET=changeme --network="host" deployboard-pytest
```
