#!/usr/bin/env bash

PACKAGE="boilerplate"

# Remove backup files
rm -f *~

# Remove Python cache
rm -rf "__pycache__"
rm -rf "src/${PACKAGE}/__pycache__"

# Display the cleaned directory structure
tree -I .venv
