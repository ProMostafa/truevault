
# Approach one: using docker & docker compose
### Installing docker & docker compose
Please refer to this [link](https://support.netfoundry.io/hc/en-us/articles/360057865692-Installing-Docker-and-docker-compose-for-Ubuntu-20-04) to install docker and docker compose

### Clone truevault repository
```bash
 git clone https://github.com/ProMostafa/truevault.git
 cd truevault
```

### Build & run docker compose file 
for build images 
```bash
docker-compose build
```
for run images
```bash
docker-compose up
```
for stop containers and remove it
```bash
docker-compose down
```
## Create Admin user
make sure you run docker-compose up
```bash
docker exec -it <container_id> sh python manage.py createsuperuser
```

## Login to admin site and add Currencies for able to manipulate with APIs

### After run images can use truevault project
navigates to http://localhost:8000/

*******************************
# Approach two: using veritual env

### clone truevault repository
```bash
 git clone https://github.com/ProMostafa/truevault.git
 cd truevault
```

## Install Redis
```bash
sudo apt-get install redis-server
```
***Don't forget to change redis setting in setting.py and .env file***

### Installing python 3.10 (if it's installed already, skip this part)
Please refer to this [link](https://phoenixnap.com/kb/how-to-install-python-3-ubuntu) to install python

## Create virtualenv
```bash
python3.10 -m venv venv
```
Activate it
```bash
source venv/bin/activate
```
Install the requirements
```bash
pip install -r requirements.txt
```

# Installing the Database
### Installing pgAdmin and Postgresql
Please refer to this [link](https://www.tecmint.com/install-postgresql-and-pgadmin-in-ubuntu/) to Install postgresql and pgAdmin.

## creating the database for pgadmin
The database is gonna be named 'truevault' ***Don't forget to change postgesl setting in setting.py and .env file***

### Source Env variables before run project
```bash
source .env
```

## Create Admin user
make sure you inside root dir 
```bash
python manage.py createsuperuser
```

## Login to admin site and add Currncies for able to manipulate with APIs

## Run django server
```bash
python manage.py runserver
```

## Run celery server
```bash
celery -A configuration worker --loglevel=info
```

## Run flower server for monitoring background tasks
```bash
celery -A configuration flower
```