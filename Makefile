CB := $(shell git branch --show-current)

all:
	@echo "no default make rule defined"

help:
	cat Makefile

requirements:
	python3 -m pip install --upgrade -r requirements.txt

requirements-dev:
	python3 -m pip install --upgrade -r requirements-dev.txt

build: clean
	python3 setup.py build install

test:
	pytest -v

buildtest: clean build test

cleantest: clean requirements requirements-dev build test

clean:
	rm -fr build dist __pycache__ *.egg-info/
