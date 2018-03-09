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
	rm -fr dist/ datasimple.egg-info/

.PHONY: lint
lint:
	./lint

.PHONY: dist
dist:
	@echo "TODO: distribute with twine"
