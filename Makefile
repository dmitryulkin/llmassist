.PHONY: start
start:
	docker-compose.exe -f build/docker-compose.base.yml -f build/docker-compose.prod.yml up --force-recreate ${MODE}

.PHONY: stop
stop:
	docker-compose.exe down --remove-orphans ${MODE}
