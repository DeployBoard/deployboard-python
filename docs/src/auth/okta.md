# Okta OAuth2 authentication

The Okta authentication allows your DeployBoard users to log in by using an external Okta authorization server.

## Create an Okta application

Before you can sign a user in, you need to create an Okta application from the Okta Developer Console.

1. Log in to the [Okta portal](https://login.okta.com/).

1. Go to Admin and then select **Developer Console**.

1. Select **Applications**, then **Add Application**.

1. Pick **Web** as the platform.

1. Enter a name for your application (or leave the default value).

1. Add the **Base URI** of your application, such as https://deployboard.example.com.

1. Enter values for the **Login redirect URI**. Use **Base URI** and append it with `/login/okta`, for example: https://deployboard.example.com/login/okta.

1. Click **Done** to finish creating the Okta application.

## Enable Okta OAuth in DeployBoard

1. Add the following environment variables. See [Configuration](../../deployment/configuration/#okta-auth) for more information.

```ini
OKTA_ENABLED = true
OKTA_CLIENT_ID = "your_client_id"
OKTA_CLIENT_SECRET = "your_client_secret"
OKTA_SCOPES = openid profile email groups
OKTA_AUTH_URL = "https://<tenant-id>.okta.com/oauth2/v1/authorize"
OKTA_TOKEN_URL = "https://<tenant-id>.okta.com/oauth2/v1/token"
OKTA_API_URL = "https://<tenant-id>.okta.com/oauth2/v1/userinfo"
OKTA_AUDIENCE = "api://default"
OKTA_ALLOWED_DOMAINS =
OKTA_ALLOWED_GROUPS =
OKTA_ROLE_MAPPING =
```

### Configure allowed groups and domains

!!! Note
    TODO: This needs to be implemented.

To limit access to authenticated users that are members of one or more groups, set `allowed_groups` to a comma-separated list of Okta groups.

```ini
allowed_groups = "Developers, Admins"
```

The `allowed_domains` option limits access to the users belonging to the specific domains. Domains should be separated by comma.

```ini
allowed_domains = "mycompany.com, mycompany.org"
```

### Map roles

TODO: Correct this

DeployBoard can attempt to do role mapping through Okta OAuth. In order to achieve this, DeployBoard checks for the presence of a role using the [JMESPath](http://jmespath.org/examples.html) specified via the `role_attribute_path` configuration option.

DeployBoard uses JSON obtained from querying the `/userinfo` endpoint for the path lookup. The result after evaluating the `role_attribute_path` JMESPath expression needs to be a valid DeployBoard role, i.e. `Viewer`, `Editor` or `Admin`. Refer to [Organization roles]({{< relref "../permissions/organization_roles.md" >}}) for more information about roles and permissions in DeployBoard.

Read about how to [add custom claims](https://developer.okta.com/docs/guides/customize-tokens-returned-from-okta/add-custom-claim/) to the user info in Okta. Also, check Generic OAuth page for [JMESPath examples]({{< relref "generic-oauth.md/#jmespath-examples" >}}).
