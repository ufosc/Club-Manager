build: ./Dockerfile
	docker-compose build

dev: build
	docker-compose up

test: build
	docker-compose run --rm app sh -c "python manage.py test"
	
format: ./app
	docker-compose run --rm app sh -c "black --check . && \
	  autoflake --in-place --remove-all-unused-imports --remove-unused-variables --check --quiet --recursive --exclude "migrations" . && \
	  isort --check ."

format-fix: ./app
	docker-compose run --rm app sh -c "black . && \
	  autoflake --in-place --remove-all-unused-imports --remove-unused-variables --quiet --recursive --exclude "migrations" . && \
	  isort ."

lint: ./app
	docker-compose run --rm app sh -c "flake8"

network-build: ./Dockerfile
	docker-compose -f docker-compose.network.yml build

network-run:
	docker-compose -f docker-compose.network.yml up
	
network: network-build network-run

debug-build: ./Dockerfile
	docker-compose -f docker-compose.debug.yml build
	
debug-run:
	docker-compose -f docker-compose.debug.yml up

debug-test:
	docker-compose -f docker-compose.debug.yml run --rm app sh -c "pip install debugpy -t /tmp && \
		python manage.py wait_for_db && \
		python manage.py migrate && \
		python manage.py init_superuser && \
		python /tmp/debugpy --listen 0.0.0.0:5678 manage.py test"

debug: debug-build debug-run

docker-push-clubs:
	docker buildx build --platform=linux/amd64,linux/arm64 -t ikehunter5/club-manager:latest -f ./Dockerfile . --push

docker-push-proxy:
	docker buildx build --platform=linux/amd64,linux/arm64 -t ikehunter5/club-manager-proxy:latest ./deploy/proxy --push
	
down:
	docker-compose down --remove-orphans

clean:
	docker-compose down --remove-orphans -v
