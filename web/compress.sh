#!/bin/sh

if [ ! -d "static" ]; then
        exit 1
fi

ROOT=$(pwd)

cd $ROOT/static/css
cat bootstrap.css \
  custom.css \
  | python -m rcssmin > main.min.css

cd $ROOT/static/js
cat jquery.min.js \
  highstock.js \
  moment.min.js \
  tether.min.js \
  bootstrap.min.js \
  custom.js \
  | python -m rjsmin > main.min.js
