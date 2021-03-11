#!/usr/bin/env bash
docker stop rest_service
docker rm rest_service
sudo docker run -d  --name rest_service  --net=host -p 8888:8888  -e SQLALCHEMY_DATABASE_URI='postgresql://postgres:xxxxxxxxxx@localhost:5432/marakas' service:rest
