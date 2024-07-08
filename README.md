# `tap-auth0`

`tap-auth0` is a Singer tap for Auth0.

Built with the [Meltano Tap SDK](https://sdk.meltano.com) for Singer Taps.

[![Python version](https://img.shields.io/badge/dynamic/toml?url=https%3A%2F%2Fraw.githubusercontent.com%2FMatatika%2Ftap-auth0%2Fmaster%2Fpyproject.toml&query=tool.poetry.dependencies.python&label=python)](https://docs.python.org/3/)
[![Singer SDK version](https://img.shields.io/badge/dynamic/toml?url=https%3A%2F%2Fraw.githubusercontent.com%2FMatatika%2Ftap-auth0%2Fmaster%2Fpoetry.lock&query=package%5B%3F(%40.name%3D%3D'singer-sdk')%5D.version&label=singer-sdk)](https://sdk.meltano.com/en/latest/)
[![License](https://img.shields.io/github/license/Matatika/tap-auth0)](https://github.com/Matatika/tap-auth0/blob/main/LICENSE)
[![Code style](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fastral-sh%2Fruff%2Fmain%2Fassets%2Fbadge%2Fformat.json)](https://docs.astral.sh/ruff/)

## Overview

`tap-auth0` extracts raw data from the [Auth0 Management API](https://auth0.com/docs/api/management/v2) for the following resources:
- [Users](https://auth0.com/docs/manage-users/user-migration/bulk-user-exports)
- [Clients](https://auth0.com/docs/api/management/v2#!/Clients/get_clients)
- [Logs](https://auth0.com/docs/api/management/v2#!/Logs/get_logs)

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

Name | Required | Default | Description
--- | --- | --- | ---
`client_id` | Yes |  | Your `tap-auth0` M2M application client ID
`client_secret` | Yes | | Your `tap-auth0` M2M application client secret
`domain` | Yes | | Your [Auth0 tenant](https://auth0.com/docs/get-started/auth0-overview/create-tenants) domain in the format `<TENANT_NAME>.<REGION_IDENTIFIER>.auth0.com`
`job_poll_interval_ms` | No | `2000` | The interval in milliseconds between requests made to [get a job](https://auth0.com/docs/api/management/v2#!/Jobs/get_jobs_by_id) when polling for a non-`pending` `status`
`job_poll_max_count` | No | `10` | The number of requests made to [get a job](https://auth0.com/docs/api/management/v2#!/Jobs/get_jobs_by_id) when polling for a non-`pending` `status`

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
- [Logs](https://auth0.com/docs/api/management/v2#!/Logs/get_logs)

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
make init
```

### Lint your Code

Identify lint issues by running:

```bash
make lint
```

> If `make init` has been run, this command will execute automatically before a commit

You can also fix lint issues automatically with:

```bash
make lint-fix
```

### Create and Run Tests

Create tests within the `tap_auth0/tests` subfolder and
  then run:

```bash
make test
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
