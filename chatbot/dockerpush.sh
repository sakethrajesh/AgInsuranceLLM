#!/bin/bash

# Build the image
docker build --platform linux/amd64 -t container.cs.vt.edu/saketh/aginsurancellm .
# Push the image
docker push container.cs.vt.edu/saketh/aginsurancellm