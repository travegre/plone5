# Plone 5 Docker helpers
# Run 'make up' instead of 'docker compose up' to ensure correct directory ownership.

UID := $(shell id -u)
GID := $(shell id -g)

# Plone container runs as UID 1000 (plone user baked into the image).
PLONE_UID := 1000
PLONE_GID := 1000

DATA_DIRS := data/var data/eggs data/parts data/downloads

.PHONY: init up build buildout down clean

## Create data directories with correct ownership before starting containers.
init:
	@echo "Creating data directories owned by $(PLONE_UID):$(PLONE_GID)..."
	@mkdir -p $(DATA_DIRS)
	@sudo chown -R $(PLONE_UID):$(PLONE_GID) $(DATA_DIRS)
	@echo "Done."

## Build the Docker image.
build:
	docker compose build

## Run buildout (first time or after adding eggs).
buildout: init
	RUN_BUILDOUT=1 docker compose up

## Normal start (skips buildout if already done).
up: init
	docker compose up

## Stop containers.
down:
	docker compose down

## Full reset: stop, wipe data dirs, re-init, rebuild image (no cache), and run buildout.
clean: down
	@echo "Wiping data directories..."
	@sudo rm -rf $(DATA_DIRS)
	$(MAKE) init
	docker compose build --no-cache
	$(MAKE) buildout
