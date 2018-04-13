---
title: datasimple README
author: Craig Kelly
---

# Introduction

*Source Note:* The authoritative version of this file is the Markdown version.
The RST version is automatically created from the Markdown by `pandoc`.

This is an Apache licensed library and set of command-line tools for simple
data processing tasks and pipelines. It is assumed that it will be used with
tools like [dmk](https://github.com/CraigKely/dmk) and that serious work will
be done with serious tools (like jupyterlab and scipy).

If it feels like a mishmash of functionality, that's because it is. This is
mainly a collection of odds and ends that keeps getting used in projects in a
very specific analytics and data science team.

# Installing

The normal way:

```
$ pip install datasimple
```

However, we use Python 3 and prefer user installs, so on a system like Ubuntu
you probably want:

```
$ pip3 install --user --upgrade datasimple
```

HOWEVER, The CORRECT usage is a Pipfile controlled by pipenv.

See below (in [Hacking](#hacking)) for installing in development mode if you
need to make source code changes.

# What you get

The datasimple library and some handy scripts (see `./bin`). Of note is a class
designed to help you write scripts to convert anything to Excel spreadsheets.
(Once again, this is functionality we need for a particular business
environment. It is expressly NOT an endorsement of Excel for data science.)

# Requirements

This is Python 3. Don't submit requests for Python 2 compatibility.

See setup.py for dependencies (which will get installed automatically when you
install this package with `pip`)

# Hacking

You should be developing in a virtualenv. Since you are probably forced to work
in a Vagrant Ubuntu VM on a Windows machine, and you'll want to use the shared
`/vagrant` folder, you might want to consider using pipenv and pyenv with the
virtualenv plugin.

Use `make test` for testing (which will also handle linting). In fact, see
the `Makefile` for what we automate with this project.

# Contributing

The following guidelines are used when accepting external contributions:

* `./lint` should not find any issues
* There should be appropriate tests add to the appropriate module in `./tests`
* There should be an existing *and* compelling use case.

The `./lint` script in the root of this repo uses pylama which you must
install. Currently it also expects a pylama linter plugin called "quotes". See
Craig (the maintainer) for this plugin. NOTE: if even ONE PERSON contacts me
I'll make that plugin public :)

If you don't currently have pylama installed, you can get the latest installed
for your user with `pip3 install --user --upgrade pylama`.

You should also test using the `./test` script in the root of this repo. It
runs tests using nosetests. Our setup also requires the package nose-exclude.
However, the test script delegates via `setup.py` so you shouldn't need to
worry about this.

Note that both pylama and nosetests have configuration specified in
`setup.cfg`.
