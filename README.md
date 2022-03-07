# `tap-auth0`

`tap-auth0` is a Singer tap for Auth0.

Built with the [Meltano Tap SDK](https://sdk.meltano.com) for Singer Taps.

## Overview

`tap-auth0` extracts raw data from the [Auth0 Management API](https://auth0.com/docs/api/management/v2) for the following resources:
- [Users](https://auth0.com/docs/manage-users/user-migration/bulk-user-exports)
- [Clients](https://auth0.com/docs/api/management/v2#!/Clients/get_clients)

## Installation

```bash
# pip
pip install git+https://github.com/Matatika/tap-auth0

# pipx
pipx install git+https://github.com/Matatika/tap-auth0

# poetry
poetry add git+https://github.com/Matatika/tap-auth0
```

## Configuration

### Accepted Config Options

Name | Required | Description
--- | --- | ---
`client_id` | Yes | Your `tap-auth0` M2M application client ID
`client_secret` | Yes | Your `tap-auth0` M2M application client secret
`domain` | Yes | Your [Auth0 tenant](https://auth0.com/docs/get-started/auth0-overview/create-tenants) domain in the format `<TENANT_NAME>.<REGION_IDENTIFIER>.auth0.com`

A full list of supported settings and capabilities for this
tap is available by running:

```bash
tap-auth0 --about
```

### Source Authentication and Authorization

Before using `tap-auth0`, you will need to [create a M2M application](https://auth0.com/docs/get-started/auth0-overview/create-applications/machine-to-machine-apps) from your [Auth0 Dashboard](https://auth0.com/docs/get-started/auth0-overview/dashboard). We recommend restricting your use of this application to `tap-auth0` only.

Your `tap-auth0` M2M application will need authorized access to the [Auth0 Management API](https://auth0.com/docs/manage-users/user-accounts/manage-users-using-the-management-api) for your tenant, as well as a number of scopes.

#### Scopes
Your `tap-auth0` M2M application will need to have certain [scopes](https://auth0.com/docs/get-started/apis/scopes) set to allow `tap-auth0` to access specific Auth0 resource data.

> All non-`read:` scopes can be disregarded, as `tap-auth0` will only ever 'read' data

The available scopes differ depending on the type of Auth0 resource (relevant to `tap-auth0`):
- [Users](https://auth0.com/docs/manage-users/user-migration/bulk-user-exports)
- [Clients](https://auth0.com/docs/api/management/v2#!/Clients/get_clients)

If a required scope is not set for your `tap-auth0` M2M application, `tap-auth0` will encounter a `403 Forbidden` response from the Auth0 Management API and fail. You must set all required scopes for the resources listed above.

Some scopes are not required. Setting these will allow `tap-auth0` to read more specific and possibly sensitive resource data, so do this at your own risk.

## Usage

You can easily run `tap-auth0` by itself or in a pipeline using [Meltano](https://meltano.com/).

### Executing the Tap Directly

```bash
tap-auth0 --version
tap-auth0 --help
tap-auth0 --config CONFIG --discover > ./catalog.json
```

## Developer Resources

### Initialize your Development Environment

```bash
pipx install poetry
poetry install
```

### Create and Run Tests

Create tests within the `tap_auth0/tests` subfolder and
  then run:

```bash
poetry run pytest
```

You can also test the `tap-auth0` CLI interface directly using `poetry run`:

```bash
poetry run tap-auth0 --help
```

### Testing with [Meltano](https://www.meltano.com)

_**Note:** This tap will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._

Your project comes with a custom `meltano.yml` project file already created. Open the `meltano.yml` and follow any _"TODO"_ items listed in
the file.

Next, install Meltano (if you haven't already) and any needed plugins:

```bash
# Install meltano
pipx install meltano
# Initialize meltano within this directory
cd tap-auth0
meltano install
```

Now you can test and orchestrate using Meltano:

```bash
# Test invocation:
meltano invoke tap-auth0 --version
# OR run a test `elt` pipeline:
meltano elt tap-auth0 target-jsonl
```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to 
develop your own taps and targets.
