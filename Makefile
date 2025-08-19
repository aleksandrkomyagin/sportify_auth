PROJECT_NAME=sportify-auth
DOCKER=docker
COMPOSE=docker compose
COMPOSE_NAME=docker-compose.yml
CONTAINER=sportify_auth_service_app

build:
	$(COMPOSE) -f $(COMPOSE_NAME) up --build

logs:
	$(DOCKER) logs -f $(CONTAINER)

lint:
	@echo "Running ruff..."
	ruff check src/ --fix
	ruff check src/ --select I --fix
	ruff format src/

test:
	@echo "Running pytest..."
	$(DOCKER) exec sportify_auth_service_app pytest -v
