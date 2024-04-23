#! /bin/bash
end=$((SECONDS+3600))

while [ $SECONDS -lt $end ]; do
    python ../../../llamarest2.py ../../../specs/swagger/fdic.yaml http://localhost:9001/api
done
