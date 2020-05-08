#!/usr/bin/env python3

import os
import subprocess

import click
import yaml
from pathlib import Path
from dotenv import dotenv_values, load_dotenv

def check_cirleci_cli():
    print("Checking for CircleCI CLI...   ", end="")
    check = subprocess.Popen(["which", "circleci"],
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT)
    stdout,stderr = check.communicate()

    if stderr:
        print("""Please install CircleCI CLI tool:
    https://circleci.com/docs/2.0/local-cli/""")
        exit(1)
    
    print(u'\u2713')


def get_cli_token():
    print("Getting CircleCI Token...   ", end="")
    home = str(Path.home())
    with open(home + "/.circleci/cli.yml", "r") as circleci_config:
        try:
            c = yaml.safe_load(circleci_config)
            if c["token"]:
                print(u'\u2713')
                return c["token"]
        except yaml.YAMLError as e:
            print(e)

    print("""You will need a token to access CircleCI.
You can create a token by logging in to your CircleCI account and then going to:
    https://app.circleci.com/settings/user/tokens

This token is tied to your user, so if you are setting it up for an organization you may want to use a service account instead.
    """)
    return False


def get_env_vars(env):
    print("Getting Environment Variables...   ", end="")

    env_vars = []

    # Load the environment variables from .env
    load_dotenv()
    for e in env:
        if "=" in e:
            var = e.split("=", 1)
        else:
            var = (e, os.getenv(e))
        env_vars.append(var)
    
    if env_vars == []:
        print(u'\u274c')
        print("No variables found. Exiting...")
        exit(1)

    print(u'\u2713')
    return env_vars


def add_context(ctx, org):
    print("Creating Context on CircleCI...   ", end="")
    check = subprocess.Popen(["circleci", "context", "create", "github", org, ctx],
        stdout=subprocess.PIPE, 
        stderr=subprocess.STDOUT)
    stdout,stderr = check.communicate()

    print(u'\u2713')


def add_environment_variable(ctx, org, var):
    print("Adding", var[0], "...   ", end="")
    check = subprocess.Popen(["circleci", "context", "store-secret", "github", org, ctx, var[0]],
        shell=False,
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE,
        stderr=subprocess.STDOUT)

    check.stdin.write(str.encode(var[1]))
    stdout,stderr = check.communicate()

    print(u'\u2713')


@click.command()
@click.option("-t", "--token", default=lambda: get_cli_token(), help="Personal Token for CircleCI.")
@click.option("-e", "--env", multiple=True, default=lambda: dotenv_values())
@click.option("-o", "--org", prompt="Enter Github organization", help="Github organization that your project is under.")
@click.option("-c", "--context", prompt="Enter context name", help="Shared context to store variables under in CircleCI.")
def main(token, env, org, context):
    """=== CircENVent ===

Use CircleCI CLI tool to populate environment variables to your projects."""
    
    check_cirleci_cli()
    env_vars = get_env_vars(env)
    add_context(context, org)

    for var in env_vars:
        add_environment_variable(context, org, var)
