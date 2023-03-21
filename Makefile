run_base:
	docker-compose -f docker-compose.base.yaml up --build


clear_data:
	docker-compose -f docker-compose.base.yaml down -v