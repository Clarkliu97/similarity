## Setup

# The first thing to do is to clone the repository:

> git clone https://github.com/epochsgithub/similarity.git

> cd <project_name>


# Create a virtual environment to install dependencies in and activate it:
```
python>=3.10.2
pip install virtualenv
virtualenv <project_name>
source/path/to/venv/bin/activate

 Then install the dependencies:
(env)$ pip install -r requirements.txt
```

# Run Migrations
```
python manage.py makemigrations
python manage.py migrate
```
```
python manage.py migrate --run-syncdb
```
--run-syncdb - Creates tables for apps without migrations.

# Install Redis
https://github.com/MicrosoftArchive/redis/releases


# Run the django project locally

```
python manage.py runserver 0.0.0.0:8000
```

# Run Celery Purge
```
celery -A similarity purge -l info --pool=solo
```

# Run Celery Worker
```
celery -A similarity.worker -l info --pool=solo
```

# sqlite3 JSON_VALID for windows
check out https://github.com/heartexlabs/label-studio/issues/679


# Check out your site!

Visit localhost:8000 on your browser to see your application running. Try adding `/admin/` to the end of the URL, and you'll be taken to the admin site.
