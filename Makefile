.PHONY: clean venv docker-rm docker-build docker test test-rebuild test-env build upload

TESTS = "tests/"
N = 1

clean:
	@rm -rf dist/*
	@rm -rf build/*
	@find . -path '*/.*' -prune -o -name '__pycache__' -exec rm -fr {} +
	@find . -path '*/.*' -prune -o -name '*.egg-info' -exec rm -fr {} +
	@find . -path '*/.*' -prune -o -name '*.py[co]' -exec rm -fr {} +
	@find . -path '*/.*' -prune -o -name '*.build' -exec rm -fr {} +
	@find . -path '*/.*' -prune -o -name '*.so' -exec rm -fr {} +
	@find . -path '*/.*' -prune -o -name '*.c' -exec rm -fr {} +
	@find . -path '*/.*' -prune -o -name '*~' -exec rm -fr {} +

venv:
	@rm -rf ~/venv/engin
	@python3 -m venv ~/venv/engin

docker-rm:
	@cd docker && docker-compose -f dev.compose.yaml rm -s -v -f;

docker-build: docker-rm
	@cd docker && docker-compose -f dev.compose.yaml build --no-cache;

docker:
	@cd docker && docker-compose -f dev.compose.yaml run engin-dev;

test: clean
	python3 -m tox --skip-missing-interpreters -- ${TESTS} -n ${N}
	@make clean

test-rebuild: clean
	rm -rf .tox
	python3 -m tox --skip-missing-interpreters --recreate --notest
	@make clean

test-env: clean
	python3 -m tox -e ${ENV} -- ${TESTS} -n ${N}

build: clean
	@python3 -m build

upload: build
	@twine upload dist/*
