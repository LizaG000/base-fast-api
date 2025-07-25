compose:
	docker compose -f deploy/docker-compose.yml up --build -d
down:
	docker compose -f deploy/docker-compose.yml down
migrations_init:
	 uv run alembic revision --autogenerate -m "init"