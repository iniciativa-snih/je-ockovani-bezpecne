install-dev:
	python -m pip install virtualenv
	python -m virtualenv venv
	source venv/bin/activate && python -m pip install -e ".[dev]"
	source venv/bin/activate && pre-commit install
	source venv/bin/activate && python -m pip install ipykernel
	source venv/bin/activate && ipython kernel install --user --name=jsou-vakciny-bezpecne

clean:
	rm -rf build __pycache__ jsouvakcinybezpecne/__pycache__ __pycache__ \
	tests/__pycache__ tests/jsouvakcinybezpecne/__pycache__ .pytest_cache *.egg-info .eggs tests/jsouvakcinybezpecne/__pycache__\
	tests/jsouvakcinybezpecne/toolkit/__pycache__ tests/jsouvakcinybezpecne/toolkit/testing/__pycache__ \
	jsouvakcinybezpecne/toolkit/__pycache__ jsouvakcinybezpecne/toolkit/testing/__pycache__ \
	jsouvakcinybezpecne/toolkit/testing/resources/__pycache__ jsouvakcinybezpecne/toolkit/testing/avast/__pycache__ \
	tests/jsouvakcinybezpecne/server/__pycache__ tests/jsouvakcinybezpecne/toolkit/__pycache__  tests/jsouvakcinybezpecne/toolkit/avast/__pycache__ \
	jsouvakcinybezpecne/toolkit/testing/avast/resources/__pycache__
