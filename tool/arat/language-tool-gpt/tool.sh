#! /bin/bash
end=$((SECONDS+3600))

while [ $SECONDS -lt $end ]; do
    python ../../../arat.py ../../../specs/gswagger/language-tool.yaml http://localhost:9003/v2
done
