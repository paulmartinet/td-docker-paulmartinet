#!/bin/bash
set -e  #le script s'arrête immédiatement si une commande échoue

docker compose config
docker compose build
docker scan api || true
docker compose up -d
