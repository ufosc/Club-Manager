# OSC Member Manager

## Getting Started

Install Docker & docker-compose, then:

```sh
docker-compose up --build
```

After first build, you can just run:

```sh
docker-compose up
```

To run unit tests:

```sh
docker-compose run --rm api sh -c "python manage.py test"
```

## Discussion

If the docker-compose commands get too tedious, we may want to consider these _task managers_:

- [just](https://github.com/casey/just?tab=readme-ov-file)
- [go-task](https://taskfile.dev/)
