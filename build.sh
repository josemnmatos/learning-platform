#!/usr/bin/env bash
# exit on error
set -o errexit

python plp_app/manage.py collectstatic --no-input
python plp_app/manage.py migrate