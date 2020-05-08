# CircENVent

Tool to populate environment variables to a context on CircleCI. Uses the CircleCI CLI tool under the hood and simplifies the process of getting all your secrets populated.

## Requirements

Requires you to have installed and configured the [CircleCI CLI tool](https://circleci.com/docs/2.0/local-cli/). You'll also need to [create a personal](https://app.circleci.com/settings/user/tokens) token on a user with admin access to the organization you are wanting to add the variables to.

```zsh
circleci setup
```

## Usage

### Guided Flow

```zsh
circenv
```

### Use in other scripts

You can pass in all the required prompts as commandline arguments, including the variables themselves if you don't want to use a `.env` file.

```zsh
circenv -t T0k3N1234 -o MyOrg -c context-name -e VAR_1=SECRET123 -e VAR_2=ANOTHERSECRET -e VAR_3
```

#### Token

Uses your token from `~/.circleci/cli.yml` by default. This is the preferred option as it allows you to also use the CircleCI CLI tool for other purposes. If you don't want to store your token in a file, you can pass it in as seen above whenever you run the command.

#### Organization

The name of your Github organization. The tool currently doesn't support Bithbucket, but it would be fairly simple to implement if you needed to.

#### Context

Context name can be an already existing context, or it will create a new one.

#### Environment Variables

The easiest way is to specify all your variables as a [dotenv file](https://pypi.org/project/python-dotenv/). The script will parse the file and add all variables to your context. You can also pass them in completely via the cli, either in the format `KEY=VALUE` or just pull one of your already set variables by passing in just the `KEY`.
