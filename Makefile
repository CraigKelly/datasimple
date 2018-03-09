#!make

# Set up any vars we might need before our env file
SHELL := /bin/bash

# Some variables we always set
BASEDIR=$(CURDIR)
SCRIPTS=$(BASEDIR)/scripts

.PHONY: test
test: lint
	$(SCRIPTS)/test

.PHONY: clean
clean:
	rm -fr README.rst dist/ datasimple.egg-info/

.PHONY: lint
lint: readme
	$(SCRIPTS)/lint

.PHONY: readme
readme: README.rst
README.rst: README.md
	pandoc -s README.md -o README.rst

.PHONY: dist
dist: readme
	$(SCRIPTS)/dist
