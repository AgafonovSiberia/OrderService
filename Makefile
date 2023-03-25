run:
	docker compose up --build

stop:
	docker compose up stop

run_base:
	docker compose -f docker-compose.base.yaml up --build

stop_base:
	docker compose -f docker-compose.base.yaml stop


clear_data:
	docker compose -f docker-compose.base.yaml down -v
	docker compose -f docker-compose.app.yaml down -v