#! /bin/bash
end=$((SECONDS+3600))

while [ $SECONDS -lt $end ]; do
    python ../../../llamarest3.py ../../../specs/swagger/genome-nexus.yaml http://localhost:9002
done
