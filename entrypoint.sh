#!/bin/sh

set -o errexit
set -o pipefail
set -o nounset

echo "Running migrations..."
alembic -c sportify_auth/setup/alembic.ini upgrade head
echo "Migrations successful"

echo "Running server..."
python sportify_auth/main.py
