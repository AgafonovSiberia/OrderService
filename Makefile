run_base:
	docker-compose -f docker-compose.base.yaml up --build

stop_base:
	docker-compose -f docker-compose.base.yaml stop


clear_data:
	docker-compose -f docker-compose.base.yaml down -v