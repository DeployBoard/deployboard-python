# Configuration

DeployBoard uses a simple config.yml file to provide default values. You can override these values by editing the file directly, or by passing the values as environment variables.

The recommended approach is to use the environment variables, this way you don't have to manage your own version of the config file, and you are not committing any potential secrets into source code.

## Core

| Key | Description | Default | Type | Required |
|---|---|---|---|---|
| MONGO_URI | The full path to the mongodb. | localhost:20710 | string | No |
| DPB_ENV | Used during testing to determine if a fake db should be used. | None | string | No |

## Okta Auth

| Key | Description | Default | Type | Required |
|---|---|---|---|---|
| OKTA_ENABLED | If you want to enable Okta Auth. | false | bool | No |
| OKTA_CLIENT_ID | Okta client id. | None | string | No |
| OKTA_CLIENT_SECRET | Okta client secret. | None | string | No |
| OKTA_SCOPES | Okta scopes. | None | string | No |
| OKTA_AUTH_URL | Okta auth url. | None | string | No |
| OKTA_TOKEN_URL | Okta token url. | None | string | No |
| OKTA_API_URL | Okta api url. | None | string | No |
| OKTA_AUDIENCE | Okta audience. | None | string | No |
| OKTA_ALLOWED_DOMAINS | Okta allowed domains. | None | string | No |
| OKTA_ALLOWED_GROUPS | Okta allowed groups. | None | string | No |
| OKTA_ROLE_ATTRIBUTE_PATH | Okta role attribute path in JMESPath. | None | string | No |
