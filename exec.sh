#!/usr/bin/env bash
docker build -t backend-docker .
docker run --env-file .env -p 8000:8000 -it backend-docker
