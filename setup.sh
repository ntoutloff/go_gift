#!/bin/bash
export FLASK_APP=project
export FLASK_DEBUG=1
echo "FLASK_APP=$FLASK_APP"
echo "FLASK_DEBUG=$FLASK_DEBUG"
source /home/nathan/Documents/my_projects/go_gift/.venv/bin/activate
flask run