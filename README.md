# OSC Member Manager

## Getting Started

Install Docker & docker-compose, then:

```sh
cp sample.env .env
docker-compose up --build
```

After first build, you can just run:

```sh
docker-compose up
```

To run unit tests:

```sh
docker-compose run --rm app sh -c "python manage.py test"
```

### Other Commands

Create a new database migration file:

```sh
docker-compose run --rm app sh -c "python manage.py makemigrations"
```

Optionally, dry-run migration creation to see if models formatted correctly:

```sh
docker-compose run --rm app sh -c "python manage.py makemigrations --dry-run"
```

Apply the migration to the database:

```sh
docker-compose run --rm app sh -c "python manage.py migrate"
```

### Admin Dashboard

You can log into the admin dashboard by going to the route `/admin` and using the following credentials:

- Username: `admin@example.com`
- Password: `changeme`

These defaults are set via environment variables:

```txt
DJANGO_SUPERUSER_EMAIL="admin@example.com"
DJANGO_SUPERUSER_PASS="changeme"
```

If you want to change these values, copy the sample.env file to a new `.env` file and change the values. If you already created an admin with the other credentials, then another one won't be created automatically. To get another one to be created automatically, remove the database and restart the app with this command:

```sh
docker-compose down --remove-orphans -v
docker-compose up
```

If you want to create a new admin without removing the old database, run this command:

```sh
docker-compose run --rm app sh -c "python manage.py createsuperuser --no-input"
```
## Django Install

### Prerequisites
Make sure you have Python installed on your system. Run the following command in your cmd to make sure:
```sh
python --version
```
If Python is not installed, install it at the following link: https://www.python.org/downloads/

Django should already be included. For full functionality, first open a venv in your terminal.

(If you don't have a venv installed, install one such as Conda: https://docs.conda.io/projects/conda/en/latest/user-guide/install/windows.html)

Or, run in your IDE terminal:
```sh
python -m venv /py
```
```sh
.\.venv\Scripts\activate
```
Run in terminal:
```sh
pip install -r requirements.txt
```
```sh
pip install -r requirements.dev.txt
```

## Discussion

If the docker-compose commands get too tedious, we may want to consider these _task managers_:

- [just](https://github.com/casey/just?tab=readme-ov-file)
- [go-task](https://taskfile.dev/)
