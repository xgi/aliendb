#!/bin/sh

until netcat -z $POSTGRES_HOST $POSTGRES_PORT
do
  sleep 0.5
done