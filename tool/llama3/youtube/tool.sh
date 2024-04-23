#! /bin/bash
end=$((SECONDS+3600))

while [ $SECONDS -lt $end ]; do
    python ../../../llamarest3.py ../../../specs/swagger/youtube.yaml http://localhost:9009/api
done
