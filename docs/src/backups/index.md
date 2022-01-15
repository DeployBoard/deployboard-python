# Backups - Intro

## MongoDB

DeployBoard uses MongoDB to store all data.

You have a few options that depend on how you choose to run MongoDB.

For more information on backing up MongoDB, see the [backup docs](https://docs.mongodb.com/manual/core/backups/).

### Container

By default, MongoDB runs in a container.

1. You can perform a `mongodump` on a cron schedule, and run `mongorestore` when needed to recover the data.
2. You can perform a block level backup of the filesystem that the Docker container is running on. _(requires some additional configuration)_

### Atlas

MongoDB offers a cloud based solution [Atlas](https://www.mongodb.com/atlas/database) which does offer a free tier that should satisfy most deployments.

[Atlas](https://www.mongodb.com/atlas/database) provides [on-demand snapshots](https://docs.atlas.mongodb.com/backup/cloud-backup/overview/#on-demand-snapshots) and [continuous cloud backups](https://docs.atlas.mongodb.com/backup/cloud-backup/overview/#continuous-cloud-backups).

If using [Atlas](https://www.mongodb.com/atlas/database), you can still perform `mongodump` and `mongorestore`, but it will be much easier to just have Atlas do the backups automatically for you.

## Secrets

When running a production level instance of DeployBoard, you should be changing some default variables.

You will want to make sure to back these up, and there are plenty of options out there for secrets management.

Since managing secrets depends a lot on the type of environment that you are running your DeployBoard instance in, it is not realistic for us to be able to provide every method.

To get you started we will provide some links to popular solutions.

- [ECS](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/specifying-sensitive-data.html)
- [Kubernetes](https://kubernetes.io/docs/concepts/configuration/secret/)

Just know that you should be storing these secrets encrypted somewhere. In case of server disaster, that should not cause you to lose your secrets.
