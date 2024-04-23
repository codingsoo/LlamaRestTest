#! /bin/bash
end=$((SECONDS+3600))

while [ $SECONDS -lt $end ]; do
    python ../../../llamarest3.py ../../../specs/swagger/ocvn.yaml http://localhost:9004
done