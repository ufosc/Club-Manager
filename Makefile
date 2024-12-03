build: ./Dockerfile
	docker-compose build

dev: build
	docker-compose up

test: build
	docker-compose run --rm app sh -c "python manage.py test"

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
	
down:
	docker-compose down --remove-orphans

clean:
	docker-compose down --remove-orphans -v
