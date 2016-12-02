#!/usr/bin/env bash
# Use this if you want your data to be persisted across reboots. You can
# also version the data by changing the ID variable.
ID="a001"
DATASTORE_PATH="$HOME/.appengine/ingrid-application/Datastore/$ID"
BLOBSTORE_PATH="$HOME/.appengine/ingrid-application/Blobstore/$ID"
#APP_PATH="$HOME/Projects/api-inkit-io"
APP_PATH="$HOME/Documents/Development/GIT/ingrid-application/default"

mkdir -p "$DATASTORE_PATH"
mkdir -p "$BLOBSTORE_PATH"

DATASTORE_PATH="$DATASTORE_PATH/db"
BLOBSTORE_PATH="$BLOBSTORE_PATH/db"

dev_appserver.py "$APP_PATH/app.yaml" \
   --port 8080 \
   --host 127.0.0.1 \
   --datastore_path "$DATASTORE_PATH" \
   --storage_path "$BLOBSTORE_PATH" \
   --require_indexes --log_level debug \
   --enable_sendmail=yes

