# Configuration

DeployBoard uses a simple config.yml file to provide default values. You can override these values by editing the file directly, or by passing the values as environment variables.

The recommended approach is to use the environment variables, this way you don't have to manage your own version of the config file, and you are not committing any potential secrets into source code.

| Key | Description | Default | Type | Required |
|---|---|---|---|---|
| MONGO_URI | The full path to the mongodb. | localhost:20710 | string | No |
| DPB_ENV | Used during testing to determine if a fake db should be used. | None | string | No |
