## Youtube Statistics

This application extracts data from YouTube Data API v3 that scraps videos of a channel with tags and statistics. This application also has a scheduler that tracks changes of video statistics (viewCount, likeCount, favoriteCount, commentCount) and tags every 3 mintues and store them into the postgreSQL database.

The scheduler also tracks the video performance by taking an initial performance score of viewCount of each video by diving viewCount of all the videos of a channel median and compares with the first hours viewCount of a video by diving viewCount of all the videos of a channel for first hour (60 minutes later) and update the initial score in the database.

The scheduler is programmed to run for 20 iterations of 3 minutes each (total 1 hour).


### Services:

1. Django Rest Framework
   
2. PostgreSQL Database
   
3. pgadmin4
   
4. React.js, Material-UI
   
5. Docker Containerization


### Installation:

1. Install [Docker Compose](https://docs.docker.com/compose/install/)

2. Clone this repository

`git clone https://github.com/moinul7002/Martailer.git`

3. Open Terminal and go to the directory

`cd Martailer`

4. Create virtualenv

`pip install virtualenv` or `pip3 install virtualenv`

`virtualenv py3env`

5. Activate the virtual environment

`source py3env/bin/activate`

### Backend

1. Go to app directory

`cd app`

2. Install python dependencies

`pip install -r requirements.txt`

3. Add superuser with login credentials

`docker-compose run --rm app sh -c "python manage.py createsuperuser"`

4. Migrate the DB

`docker-compose run --rm app sh -c "python manage.py migrate --run-syncdb"`

5. Execute Docker Compose file

`docker-compose up -d`

The docker-compose will run all the containerized services associated with the application and the Django development server will start at

`http://0.0.0.0:8000/`


### Frontend

1. In the terminal, go to frontend directory.

`cd frontend`

2. Create [React App](https://github.com/facebook/create-react-app)

`npx create-react-app .`

3. Go to the development server `http://127.0.0.1:3000`


### API

1. Get all the video data

`http://127.0.0.1:8000/api/list-of-videos/`

2. Search

`http://127.0.0.1:8000/api/search?q=2022&f=ASC`


### API Testing

In the terminal, run `docker-compose run --rm app sh -c 'python manage.py test'`


### Docker

1. Using docker compose, run

`docker-compose up -d`

2. Stop all the containers,

`docker-compose stop`

3. Remove all the containers,

`docker-compose down`


N.B: if you find any postgreSQL port 5432 issue, please remove all the containers and run them again.

Finally, `deactivate` the virtual environment.

Thanks.
