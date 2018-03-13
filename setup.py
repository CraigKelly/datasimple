#!/usr/bin/env python3

"""Main setup script for datasimple."""

from glob import glob
from os import path
from setuptools import setup

here = path.abspath(path.dirname(__file__))


def _files(subdir):
    return sorted(set(
        path.join(subdir, path.split(fp)[-1])
        for fp in glob(path.join(here, subdir, '*'))
        if path.isfile(fp)
    ))


def _readme():
    with open(path.join(here, 'README.rst')) as fh:
        return fh.read()


if __name__ == '__main__':
    setup(
        name='datasimple',
        version='1.0.2',
        description='Utility library and scripts for simpler data-processing tasks',
        long_description=_readme(),
        url='https://github.com/CraigKelly/datasimple',
        author='Craig Kelly',
        author_email='craig.n.kelly@gmail.com',
        license='Apache Version 2.0',

        keywords='analytics data',
        classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'Programming Language :: Python :: 3',
        ],

        packages=['datasimple'],
        scripts=_files('bin'),

        python_requires='>=3.4',
        install_requires=[
            'colorclass>=2.2.0',
            'openpyxl>=2.4.8',
            'lxml>=3.5.0',
            'requests>=2.18.4',
            'terminaltables>=3.1.0',
        ],

        test_suite='nose.collector',
        tests_require=[
            'nose>=1.3.7',
            'nose-exclude>=0.5.0',
        ],

        package_data={},
        data_files=[],
        entry_points={},
    )
