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
      exit "$test_status"
    }

    trap cleanup EXIT

    printf '%s\n' '--- Removing previous test database ---'
    "${compose[@]}" down --volumes --remove-orphans

    printf '%s\n' '--- Starting test stack ---'
    "${compose[@]}" up -d --build --wait

    printf '\n%s\n' '--- Running tests ---'
    uv run pytest -ra -v --color=yes
