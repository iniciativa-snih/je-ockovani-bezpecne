brunette:
	brunette jeockovanibezpecne tests config.py setup.py

flake:
	flake8 jeockovanibezpecne tests config.py setup.py

test:
	pytest

check: brunette flake test

install-dev:
	python -m pip install virtualenv
	python -m virtualenv venv
	source venv/bin/activate && python -m pip install -e ".[dev]"
	source venv/bin/activate && pre-commit install
	source venv/bin/activate && python -m pip install ipykernel
	source venv/bin/activate && ipython kernel install --user --name=je-ockovani-bezpecne

install-test:
	python -m pip install -e ".[test]"

clean:
	rm -rf build __pycache__ jeockovanibezpecne/__pycache__ __pycache__ instance \
	tests/__pycache__ tests/jeockovanibezpecne/__pycache__ .pytest_cache *.egg-info .eggs tests/jeockovanibezpecne/__pycache__\
	tests/jeockovanibezpecne/toolkit/__pycache__ tests/jeockovanibezpecne/toolkit/testing/__pycache__ \
	jeockovanibezpecne/toolkit/__pycache__ jeockovanibezpecne/toolkit/testing/__pycache__ \
	jeockovanibezpecne/toolkit/testing/resources/__pycache__ jeockovanibezpecne/toolkit/testing/avast/__pycache__ \
	tests/jeockovanibezpecne/server/__pycache__ tests/jeockovanibezpecne/toolkit/__pycache__  tests/jeockovanibezpecne/toolkit/avast/__pycache__ \
	jeockovanibezpecne/toolkit/testing/avast/resources/__pycache__

locust:
	locust -f tests/locust.py --headless --host https://jeockovanibezpecne.herokuapp.com -u 100 -r 5
