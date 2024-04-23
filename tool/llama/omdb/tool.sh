#! /bin/bash
end=$((SECONDS+3600))

while [ $SECONDS -lt $end ]; do
    python ../../../llamarest.py ../../../specs/swagger/omdb.yaml http://localhost:9006
done
