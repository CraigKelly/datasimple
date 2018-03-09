# pal-utils

AMS IM PAL common utilities

## Installing

This is for internal use only, so it is NOT on PyPI. However, you can install
it from our local git. On an Ubuntu VM, you can install it (and dependencies)
with:

```
$ git clone git@github.build.ge.com:221019831/palutils.git
$ pip3 install --user palutils
```

You'll note the use of pip3 because as of this writing (August 2017), `python`
and `pip` are Python 2 links on Ubuntu. (According to the Python BDFL that's
actually correct for now.)

See below (in [Hacking](#hacking)) for installing in development mode if you
need to make source code changes.

## What you get

The palutils library (see `./palutils`) and lots of handy scripts (see `./bin`).

## Requirements

This is Python 3. Don't submit requests for Python 2 compatibility.

See setup.py for dependencies (which will get installed automatically when you
install this package with `pip`)

## Hacking

You should be developing in a virtualenv. Since you are probably forced to
work in a Vagrant Ubuntu VM on a Windows machine, and you'll want to use the
shared `/vagrant` folder, you might want to consider using pyenv with the
virtualenv plugin. That way you can do a one time setup. For example, since I
have a Python 3.6.1 environment, I use that for development:


```
$ cd palutils
$ pyenv virtualenv 3.6.1 palutils-dev
$ pyenv local palutils-dev
$ pip install -e .
```

Now when I am my development directory, the virtualenv is automatically active.

See also Contributing below for dev patterns

## Contributing

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
However, the test script delegates via `setup.py` so you shouldn't need to worry
about this.

Note that both pylama and nosetests have configuration specified in
`setup.cfg`.
