#!/bin/bash

# login
docker login container.cs.vt.edu

# Build the image
docker build --platform linux/amd64 -t container.cs.vt.edu/saketh/aginsurancellm/frontend .

# Push the image
docker push container.cs.vt.edu/saketh/aginsurancellm/frontend