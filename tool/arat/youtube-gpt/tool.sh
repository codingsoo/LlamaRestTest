#! /bin/bash
end=$((SECONDS+3600))

while [ $SECONDS -lt $end ]; do
    python ../../../arat.py ../../../specs/gswagger/youtube.yaml http://localhost:9009/api
done
