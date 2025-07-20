compose:
	docker compose -f deploy/docker-compose.yml up --build -d
down:
	docker compose -f deploy/docker-compose.yml down