#!make

# Set up any vars we might need before our env file
SHELL := /bin/bash

# Some variables we always set
BASEDIR=$(CURDIR)

.PHONY: test
test: lint
	./test

.PHONY: clean
clean:
	rm -fr README.rst dist/ datasimple.egg-info/

.PHONY: lint
lint:
	./lint

.PHONY: readme
readme: README.rst
README.rst: README.md
	pandoc -s README.md -o README.rst

.PHONY: dist
dist: readme
	@echo "TODO: distribute with twine"
