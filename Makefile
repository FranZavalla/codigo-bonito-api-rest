ENV_VARIABLES = DATABASE_PATH=./test_db.sqlite ORM=sqlalchemy
KILL_BACKEND_COMMAND = kill `cat uvicorn.pid`; rm uvicorn.pid;
UNSET_ENV_VARIABLES = unset DATABASE_PATH; unset ORM;
WAIT_FOR_BACKEND_COMMAND = for i in $$(seq 1 10); do \
		curl -s http://localhost:8000; \
		if [ $$? -eq 0 ]; then break; fi; \
		echo "Esperando que el backend inicie..."; \
		sleep 1; \
	done; \

run_unit_tests:
	poetry run pytest testing/unit/

run_integration_tests:
	poetry run pytest testing/integration/

run_e2e_tests:
	$(ENV_VARIABLES) \
	poetry run uvicorn app.main:app > uvicorn.log 2>&1 & \
	echo $$! > uvicorn.pid; \
	$(WAIT_FOR_BACKEND_COMMAND) \
	poetry run pytest testing/e2e/test_endpoints.py; \
	TEST_EXIT_CODE=$$?; \
	$(KILL_BACKEND_COMMAND) \
	$(UNSET_ENV_VARIABLES) \
	exit $$TEST_EXIT_CODE

run_all_tests:
	poetry run pytest testing/unit/ || exit $$?; \
	poetry run pytest testing/integration/ || exit $$?; \
	$(ENV_VARIABLES) \
	poetry run uvicorn app.main:app > uvicorn.log 2>&1 & \
	echo $$! > uvicorn.pid; \
	$(WAIT_FOR_BACKEND_COMMAND) \
	poetry run pytest testing/e2e/test_endpoints.py; \
	TEST_EXIT_CODE=$$?; \
	$(KILL_BACKEND_COMMAND) \
	$(UNSET_ENV_VARIABLES) \
	exit $$TEST_EXIT_CODE


run_tests_with_coverage:
	DATABASE_PATH=./test_db.sqlite ORM=sqlalchemy poetry run pytest --cov=app

run_specific_test:
	DATABASE_PATH=./test_db.sqlite ORM=sqlalchemy poetry run pytest -k $(test)
