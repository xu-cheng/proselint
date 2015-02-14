#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Command line utility for proselint."""

import click
import os
from proselint.tools import line_and_column
import proselint.checks as pl
import pkgutil
import codecs
import subprocess
import ntpath


base_url = "prose.lifelinter.com/"
proselint_path = os.path.dirname(os.path.realpath(__file__))


def log_error(filename, line, column, error_code, msg):
    """Print the error to the command line."""
    click.echo(ntpath.basename(filename) + ":" +
               str(1 + line) + ":" +
               str(1 + column) + ": " +
               error_code + " " +
               msg + " " + base_url + error_code)


def run_initialization():
    """Run the initialization method for each check."""
    for loader, module_name, is_pkg in pkgutil.walk_packages(pl.__path__):
        module = loader.find_module(module_name).load_module(module_name)

        # Run the initialization.
        try:
            assert(hasattr(module.initialize, '__call__'))
            module.initialize()
        except Exception:
            pass


def lint(path):
    """Run the linter on the file with the given path."""
    # Extract functions from the checks folder.
    checks = []
    for loader, module_name, is_pkg in pkgutil.walk_packages(pl.__path__):
        module = loader.find_module(module_name).load_module(module_name)

        # Add the check to the list of checks.
        try:
            assert(hasattr(module.check, '__call__'))
            checks.append(module.check)
        except Exception:
            pass

    # Apply all the checks.
    with codecs.open(path, "r", encoding='utf-8') as f:
        text = f.read()
        errors = []
        for check in checks:
            errors += check(text)

        # Sort the errors by line and column number.
        errors = sorted(errors)

        # Display the errors.
        for error in errors:
            (start, end, error_code, msg) = error
            (line, column) = line_and_column(text, start)
            log_error(path, line, column, error_code, msg)

    return errors


@click.command()
@click.option('--version/--whatever', default=None)
@click.option('--initialize/--i', default=None)
@click.option('--debug/--d', default=False)
@click.argument('file', default=False)
def proselint(file=None, version=None, initialize=None, debug=None):
    """Define the linter command line API."""
    # Return the version number.
    if version:
        print "v0.0.1"
        return

    # Run the intialization.
    if initialize:
        run_initialization()
        return

    # In debug mode, delete the cache and *.pyc files before running.
    if debug:
        subprocess.call("find . -name '*.pyc' -delete", shell=True)
        subprocess.call("find . -name '*.check' -delete", shell=True)

    # Use the demo file by default.
    if not file:
        file = os.path.join(os.path.dirname(proselint_path), "demo.md")

    return lint(file)


if __name__ == '__main__':
    proselint()
