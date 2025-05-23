run_unit_tests:
	poetry run pytest testing/unit/

run_integration_tests:
	poetry run pytest testing/integration/

run_e2e_tests:
	DATABASE_PATH=./test_db.sqlite ORM=sqlalchemy poetry run pytest testing/e2e/test_endpoints.py
	unset DATABASE_PATH
	unset ORM

run_all_tests:
	DATABASE_PATH=./test_db.sqlite ORM=sqlalchemy poetry run pytest

run_tests_with_coverage:
	DATABASE_PATH=./test_db.sqlite ORM=sqlalchemy poetry run pytest --cov=app

run_specific_test:
	DATABASE_PATH=./test_db.sqlite ORM=sqlalchemy poetry run pytest -k $(test)
