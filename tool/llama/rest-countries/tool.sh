#! /bin/bash
end=$((SECONDS+3600))

while [ $SECONDS -lt $end ]; do
    python ../../../llamarest.py ../../../specs/swagger/rest-countries.yaml http://localhost:9007
done
