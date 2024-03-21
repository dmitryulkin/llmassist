.PHONY: start
start:
	docker-compose.exe -f build/docker-compose.base.yml -f build/docker-compose.prod.yml up --force-recreate ${MODE}

.PHONY: stop
stop:
	docker-compose.exe -f build/docker-compose.base.yml -f build/docker-compose.prod.yml down --remove-orphans ${MODE}

# rebuild and start only app
.PHONY: reapp
reapp:
	docker-compose.exe -f build/docker-compose.base.yml -f build/docker-compose.prod.yml up --no-deps --build ${MODE} app

# open tty to app while it works
.PHONY: ttyapp
ttyapp:
	docker exec -ti app /bin/bash
