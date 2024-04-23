#! /bin/bash
end=$((SECONDS+3600))

while [ $SECONDS -lt $end ]; do
    python ../../../llamarest2.py ../../../specs/swagger/spotify.yaml http://localhost:9008/v1
done
