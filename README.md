Grab airport information and store in a PostGIS repository.

This project primarily uses Python and Django, with PostgreSQL (PostGIS extension) as the backend.


## Setup

It is recommended to use a Python virtualenv (or equivalent) to manage Python dependencies
for this project.

```
sudo pip install virtualenv
sudo pip install virtualenvwrapper
```

Create the virtual environment and activate it.
```
virtualenv venv
source venv/bin/activate
```

Install the Python dependencies for this project.
```
pip install -r requirements.txt
```

Change to the "aeroproject" Django site/project directory, and run the database migrations.
By default, this will create a SQLite database, and install your schema objects (tables).
```
cd aeroproject
python manage.py migrate
```

## Running

Activate the virtual environment.
```
source venv/bin/activate
```

Change to the "aeroproject" Django site/project directory, and run the server.
```
cd aeroproject
python manage.py runserver
```
