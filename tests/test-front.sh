#!/bin/bash

echo "Running test on frontend..."
url=localhost:3000
code=`curl -s -I ${url} | grep HTTP | awk '{print $2}'`
if [ code -eq 200 ]; then
    echo "Test passed!"
else
    echo "Test failed with status code: ${code}" >&2
    exit 1
fi