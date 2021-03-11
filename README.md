# Simple REST service

The Flask based simple REST service with two endpoints



## Requirements

- python 3.8
- Postgresql



## How to install?
- Install Docker (https://docs.docker.com/get-docker/)
- Download folder Docker from this repo
- Build image
```
	..SimpleREST/Docker/build
```	
```	

## How to run?

### Edit run.sh
Set 
- Set the actual credentials for Postgresql:  -e SQLALCHEMY_DATABASE_URI='postgresql://postgres:xxxxxxxxxx@localhost:5432/marakas' 

Create tables and load data:
../SimpleREST/create_table.sql 

### Run service
```
run.sh  
```
Enpoints:
- GET ​/product/{id}/{page}/{limit}
- PUT /reviews/{id}
      json_data = {'title': '...',  'review': '...'}

