run:
	python sp500.py

test:
	pytest test_sp500.py

setup-prod:
	pip install --trusted-host pypi.python.org -r requirements/prod.txt

setup-test:
	pip install --trusted-host pypi.python.org -r requirements/test.txt

lint:
	pylint *.py