# Security

Tiled employs modern web security standards to enforce access control with
minimum inconvenience to the user.

There are four use cases for the Tiled server.

1. Secure single-user server, analogous to how people use ``jupyter notebook``
2. Public data service
3. Private multi-user data service
4. Multi-user data service with some public and some private content

We address each in turn below.

## Secure single-user server

In this mode, a single user or small group of highly trusted users have access
to a Tiled server protected by a secret access token. This is the default mode.
For those familiar with Jupyter, this is very similar to how
``jupyter notebook`` works.

At startup, a secret token is generated and logged in the terminal.

```
$ tiled serve pyobject tiled.examples.generated_minimal:tree

    Use the following URL to connect to Tiled:

    "http://127.0.0.1:8000?api_key=a4062c3dd6ab2af0d28fdb7eb278dd985c462ecf08d39f33233554c7fdaa42e7"
```

where the token after ``api_key=`` will be different each time you start the
server. Once you have visited this URL with your web browser or the Tiled Python
client, a cookie will be set in your client and you won’t need to use the token
again. It is valid indefinitely.

For horizontally-scaled deployments where you need multiple instances of the
server to share the same secret, you can set it via an environment variable like
so.

```
TILED_SINGLE_USER_API_KEY=YOUR_SECRET tiled serve ...
```

or via the configuration parameter

```yaml
authentication:
  single_user_api_key: "..."
```

When the secret is set manually it this way, it is *not* logged in the terminal.

```{note}

When generating a secret, is important to produce a difficult-to-guess random
number, and make it different each time you start up a server.  Two equally good
ways to generate a secure secret...

With ``openssl``:

    openssl rand -hex 32

With ``python``:

    python -c "import secrets; print(secrets.token_hex(32))"

```

## Public data service

Tiled can serve a public data repository with no authentication required. To
launch it in this mode, use the ``--public`` flag as in

```
tiled serve {pyobject, directory, config} --public ...
```

When the server is started in this way, it will log a notice like
the following:

```
$ tiled serve pyobject --public tiled.examples.generated_minimal:tree

    Tiled server is running in "public" mode, permitting open, anonymous access.
    Any data that is not specifically controlled with an access policy
    will be visible to anyone who can connect to this server.

```

Alternatively, if using a configuration file as in

```
tiled serve config ...
```

include the configuration:

```yaml
authentication:
  allow_anonymous_access: true
```

This is a complete working example:

```yaml
# config.yml
authentication:
  allow_anonymous_access: true
trees:
  - path: /
    tree: tiled.examples.generated_minimal:tree
```

```
tiled serve config config.yml
```

As above, a notice will be logged that the server is public.

## Private multi-user data service

In this mode, users *must* log in to access anything other than the root ``GET /``
and documentation ``GET /docs`` routes.

Tiled is designed to integrate with external user-management systems via a pluggable
Authenticator interface. For those familiar with JupyterHub, these are very
similar to JupyterHub Authenticators. Authenticators fall into two groups:

* Authenticators that accept user credentials directly, following the OAuth2 and
  OpenAPI standards as shown below, and validate the credentials using some
  underlying authentication mechanism, such as PAM.
* Authenticators that use an external service such as Google or ORCID to validate
  the user identity, without directly handling credentials in Tiled.

This mode requires configuration files to be used, as in

```
tiled serve config path/to/config_file(s)
```


in order to specify the Authenticator and, when applicable, any parameters.
The shorthands ``tiled serve pyobject ...`` and ``tiled serve directory ...``
do not currently support this mode. See below for complete working examples.

The server implements "sliding sessions", meaning that the user provides their
login credentials once and the server keep their session alive for as long as
they are actively using it---up to some optional, configurable limit.

You may configure:

* The maximum time to keep an *inactive* session alive (default is one week)
* The maximum session lifetime (default is unlimited)
* Access token lifetime. This is internal from the user's point of view
  It should be short. (Default 15 minutes.)

See {doc}`../reference/authentication` for advanced customization options and
additional details.

### Authenticate with local system accounts

Tiled includes a `PAMAuthenticator` for logging in with local user accounts
using a username and password. It requires one additional dependency:

```
pip install pamela
```

The configuration file(s) should include:

```yaml
authentication:
  authenticator: tiled.authenticators:PAMAuthenticator
```

Here is a complete working example:

```yaml
# pam_config.yml
authentication:
  providers:
    - authenticator: tiled.authenticators:PAMAuthenticator
      # This 'provider' can be any string; it is used to differentiate
      # authentication providers when multiple ones are supported.
      provider: local
trees:
  - path: /
    tree: tiled.examples.generated_minimal:tree
```

```
tiled serve config pam_config.yml
```

Authenticate using a system user account and password.


### Authenticate with OpenID Connect Providers

Tiled includes an `OIDCAuthenticator` for logging in with third-party identity
providers including ORCID, Google, and many others using the web standard OpenID
Connect. In this mode, Tiled does not directly handle users' login credentials.
Instead, it provides a link to open in the browser, log in to the third-party
service, and obtain an access code that will be accepted by Tiled.

This uses the same technology that supports web-based flows like "Log in to
Website X with Google!" but it does so in a way that works from command-line
tools, scripts, Jupyter notebooks, and other applications. It works like this:

User: Hello, Tiled! Please let me in.
Tiled Server: Go to this URL and come back with an access code.
User (in web browser): Hello OIDC Provider {ORCID, Google, etc.}, Tiled sent me.
OIDC Provider: Do you authorize Tiled to see your account info?
User (in web browser): Yes.
OIDC Provider: _directs browser to Tiled Serer_
Tiled Server: The OIDC provider has vouched that you are {username}. Copy/paste
this access code.

The `OIDCAuthenticator` requires an additional dependency. (Depending on how you
installed Tiled, you may already have it because it is required by Tiled's
Python _client_.)

```
pip install httpx
```

1. Deploy Tiled with HTTPS.
2. Register your application with the OIDC Provider. You will be asked to
   provide a Redirect URI. Give `https://.../auth/code`. You will be given a
   Client ID and Client Secret.
3. It is recommended to set the Client Secret as an environment variable, such
   as `OIDC_CLIENT_SECRET`, and reference that from configuration file as shown
   below.
4. Obtain the OIDC provider's public key(s). These are published by the OIDC provider.
   Starting from a URL like:

   * [https://accounts.google.com/.well-known/openid-configuration](https://accounts.google.com/.well-known/openid-configuration)
   * [https://orcid.org/.well-known/openid-configuration](https://orcid.org/.well-known/openid-configuration)

   Navigate to the link under the key `jwks_uri`. These public key(s) are designed
   to prevent man-in-the-middle attacks. They may be rotated over time.

The configuration file(s) must include the following.

```yaml
authentication:
  providers:
  - provider: some-oidc-service
    authenticator: tiled.authenticators:OIDCAuthenticator
    args:
      # All of these are given by the OIDC provider you register
      # your application.
      client_id: ...
      client_secret: ${OIDC_CLIENT_SECRET}  # reference an environment variable
      token_uri: ...
      authorization_endpoint: ...
      redirect_uri: ...  # https://{YOUR_TILED_SERVER_ADDRESS}/provider/{some-oidc-service}/auth/code
      # These come from the OIDC provider as described above.
      public_keys:
        - kty: ...
          e: ...
          use: ...
          kid: ...
          n: ...
          alg: ...
      confirmation_message: "You have logged in with ... as {id}."
```

Here is an example for ORCID authentication running at
`https://tiled-demo.blueskyproject.io`.

```yaml
authentication:
  providers:
  - provider: orcid
    authenticator: tiled.authenticators:OIDCAuthenticator
    args:
      client_id: APP-0ROS9DU5F717F7XN  # obtained from ORCID for tiled-demo.blueskyproject.io; not secret
      client_secret: ${OIDC_CLIENT_SECRET}  # reference an environment variable
      redirect_uri: https://tiled-demo.blueskyproject.io/api/auth/provider/orcid/code
      token_uri: "https://orcid.org/oauth/token"
      authorization_endpoint: "https://orcid.org/oauth/authorize?client_id={client_id}&response_type=code&scope=openid&redirect_uri={redirect_uri}"
      # These values come from https://orcid.org/.well-known/openid-configuration.
      # Obtain them directly from ORCID. They may change over time.
      public_keys:
        - kty: ...
          e: ...
          use: ...
          kid: ...
          n: ...
          alg: RS256
      confirmation_message: "You have logged in with ORCID as {id}."
```

### Toy examples for testing and development

The ``DictionaryAuthenticator`` authenticates using usernames and passwords
specified directly in the configuration. The passwords may be extracted from
environment variables, as shown. This is not a robust user management system and
should only for used for development and demos.

```yaml
# dictionary_config.yml
authentication:
  providers:
  - provider: toy
    authenticator: tiled.authenticators:DictionaryAuthenticator
    args:
      users_to_passwords:
        alice: ${ALICE_PASSWORD}
        bob: ${BOB_PASSWORD}
        cara: ${CARA_PASSWORD}
trees:
  - path: /
    tree: tiled.examples.generated_minimal:tree
```

```
ALICE_PASSWORD=secret1 BOB_PASSWORD=secret2 CARA_PASSWORD=secret3 tiled serve config dictionary_config.yml
```

The ``DummyAuthenticator`` accepts *any* username and password combination.

```yaml
# dummy_config.yml
authentication:
  providers:
  - provider: toy
    authenticator: tiled.authenticators:DummyAuthenticator
trees:
  - path: /
    tree: tiled.examples.generated_minimal:tree
```

```
tiled serve config dummy_config.yml
```

To control which users can see which entries in the Trees, see
{doc}`access-control`.

## Multi-user data service with some public and some private content

When an Authenticator is used in conjunction with {doc}`access-control`,
certain entries may be designated as "public", visible to any user. By default,
visitors still need to be authenticated (as any user) to see these entries.
To make such entries visible to *anonymous*, unauthenticated users as well,
include the configuration:

```yaml
authentication:
  allow_anonymous_access: true
```

See also {doc}`../reference/service-configuration`.
