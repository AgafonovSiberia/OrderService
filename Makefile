run:
	docker compose -f docker-compose.app.yaml up --build

stop:
	docker compose -f docker-compose.app.yaml up --build

run_base:
	docker compose -f docker-compose.base.yaml up --build

stop_base:
	docker compose -f docker-compose.base.yaml stop


clear_data:
	docker compose -f docker-compose.base.yaml down -v
	docker compose -f docker-compose.app.yaml down -v