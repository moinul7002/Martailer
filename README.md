## YouTube Statistics

Source: [YouTube Data API v3](https://developers.google.com/youtube/v3/)

This application extracts data from YouTube Data API v3 that scraps videos of a channel with tags and statistics. This application also has a scheduler that tracks changes of video statistics (viewCount, likeCount, favoriteCount, commentCount) and tags every 3 mintues and store and update them into the postgreSQL database.

The scheduler also tracks the video performance by taking an initial performance score of viewCount of each video by diving viewCount of all the videos of a channel median and compares with the first hours viewCount of a video by diving viewCount of all the videos of a channel for first hour (60 minutes later) and update the initial score in the database.

The scheduler is programmed to run for 20 iterations of 3 minutes each (total 1 hour).


### Services:

1. app - Django Rest Framework
   
2. local_pgdb - PostgreSQL Database
   
3. frontend - React.js, Material-UI


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

** Comment out the following line from `/app/core/api/views.py`

`from .main import FetchData`

This will allow you to run Django for the first time to migrate the DB and create superuser without causing `Django.db.utils.ProgrammingError: relation .. does not exist`. Because running migrations and creating superuser triggers the system checks to run, which causes the views to load. There isn't an option to disable this. We could call `@ratelimit` decorator that allows to pass a callable, but one disadvantage is that it will run SQL query every time the view runs that could affect performance.

In general, we want to avoid database queries when modules load as well as causing issues with migrations. It can cause issues when running tests while using try-catch exception in the decorator and queries go to the live DB before the test database has been created.

As this project is for development only and also has an API testing, I prefer commenting the line rather than using `@ratelimit` decorator.

3. Migrate the DB

`docker-compose run --rm app sh -c "python manage.py makemigrations"`

`docker-compose run --rm app sh -c "python manage.py migrate --run-syncdb"`

4. Add superuser with login credentials

`docker-compose run --rm app sh -c "python manage.py createsuperuser"`

** Now, uncomment the previous line from `/app/core/api/views.py`

5. Execute Docker Compose file

`docker-compose up -d`

The docker-compose will run all the containerized services associated with the application and the Django development server will start at

`http://0.0.0.0:8000/`

Please wait for the scheduler to complete its task. As it will run for 1 hour before exiting, I recommend to change the `time_count` and `wait_time_in_minutes` variables from `main.py` to your preference.


### Frontend

1. In the terminal, go to frontend directory.

`cd frontend`

2. Go to the development server `http://127.0.0.1:3000`


### API Endpoints

1. Get all the video data

`http://127.0.0.1:8000/api/list-of-videos/` #Working endpoint but not needed for frontend

2. Search by Tags & Filter by Performance

`http://127.0.0.1:8000/api/search?q=&f=` # Get all data

`http://127.0.0.1:8000/api/search?q=2022&f=` # Get data by tags

`http://127.0.0.1:8000/api/search?q=&f=ASC` # Sort performance in ascending order

`http://127.0.0.1:8000/api/search?q=&f=DESC` # Sort performance in descending order

`http://127.0.0.1:8000/api/search?q=2022&f=ASC` # Get data by searching tags and sort the searched data in ascending order

`http://127.0.0.1:8000/api/search?q=2022&f=DESC` # Get data by searching tags and sort the searched data in descending order


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
