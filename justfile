dev:
    docker compose -f compose.yml -f compose.dev.yml up --watch

dev-down:
    docker compose -f compose.yml -f compose.dev.yml down

dev-build:
    docker compose -f compose.yml -f compose.dev.yml build