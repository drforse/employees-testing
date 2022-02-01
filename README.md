# employees-testing
## Configuration  
### .env  
MONGO_INITDB_ROOT_USERNAME=mongo username  
MONGO_INITDB_ROOT_USERNAME=mongo password  
### config.ini  
```
[DEFAULT]  
motor_uri = mongo connection uri for motor, ex.: mongodb://root:root_password@mongo:27017/  
mongo_db = mongo database name  
get_entities_default_limit = default limit for entities in GET requests, for ex. GET /employees  
debug = debug value for fastapi application  
test_mongo_db = test mongo database name for pytest tests  
```
### Data upload  
Follow these steps to upload test data to prod :D :  
- get web service container_id: `docker ps --all`  
- copy upload_test_data_to_prod.py to container: `docker cp upload_test_data_to_prod.py <container_id>:upload_test_data_to_prod.py`  
- run `docker exec -it <container_id> /bin/bash` to enter shell  
- run `python upload_test_data_to_prod.py`  
- run `exit` to exit the container shell  
### Installation  
1. clone the repo  
2. configure everything you need (check Configuration)  
3. run `docker-compose up -d`  
4. upload test data to prod if you want to test it :D  
### Tests  
run `pytest` to run tests  
### Additional info  
You can check info about endpoints on /docs or /redoc  
