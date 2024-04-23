#! /bin/bash
end=$((SECONDS+3600))

while [ $SECONDS -lt $end ]; do
    python ../../../llamarest2.py ../../../specs/swagger/ohsome.yaml http://localhost:9005/v1
done
