dev:
    docker compose -f compose.yml -f compose.dev.yml up --watch

dev-down:
    docker compose -f compose.yml -f compose.dev.yml down

dev-build:
    docker compose -f compose.yml -f compose.dev.yml build

test:
    #!/usr/bin/env bash
    set -Eeuo pipefail

    compose=(docker compose -p nothub-test -f compose.yml -f compose.dev.yml -f compose.test.yml)
    generated_env=0

    cleanup() {
      test_status=$?
      trap - EXIT
      printf '\n%s\n' '--- Stopping test stack ---'
      if ! "${compose[@]}" down --volumes --remove-orphans; then
        printf '%s\n' 'Failed to stop the test stack.' >&2
        if [ "$test_status" -eq 0 ]; then
          test_status=1
        fi
      fi
      if [ "$generated_env" -eq 1 ]; then
        rm -f .env
      fi
      exit "$test_status"
    }

    trap cleanup EXIT

    if [ ! -f .env ]; then
      cp .env.example .env
      generated_env=1
    fi

    printf '%s\n' '--- Removing previous test database ---'
    "${compose[@]}" down --volumes --remove-orphans

    printf '%s\n' '--- Starting test stack ---'
    "${compose[@]}" up -d --build --wait

    printf '\n%s\n' '--- Running tests ---'
    DATABASE_URL=postgresql+asyncpg://postgres:postgres@127.0.0.1:5432/nothub_test \
      uv run coverage run -m pytest -ra -v --color=yes
