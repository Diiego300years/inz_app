#!/bin/bash

# here I used bash to check if folder migrations exists.
if [ ! -d "./migrations" ]; then
  echo "Folder 'migrations' doesn't exist, I'm starting init..."
  flask db init
  flask db migrate -m "docker test migrations"
  flask db upgrade
else
  echo "Folder called 'migrations' exist."
fi

# This mean finish and next step...
exec "$@"
