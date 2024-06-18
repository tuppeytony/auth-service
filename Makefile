local:
	docker-compose -p auth-service -f ./ci/local/docker-compose.yaml up -d

migrate:
	cd ./src && alembic upgrade head
