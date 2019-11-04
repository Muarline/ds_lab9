#!/usr/bin/env bash

while ! mongo --host 'mongo1' --eval 'rs.status()' &&
      ! mongo --host 'mongo2' --eval 'rs.status()' &&
      ! mongo --host 'mongo0' --eval 'rs.status()'; do
    sleep 10
done

mongo --host "mongo0" --eval 'rs.initiate({"_id":"rs","members":[{"_id":0,"host":"mongo0:27017"},{"_id":1,"host":"mongo1:27017"},{"_id":2,"host":"mongo2:27017"}]})'
