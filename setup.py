from __future__ import print_function
from setuptools import setup, find_packages
import codecs
import os
import re
import sys


def read(*parts):
    path = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(path, encoding='utf-8') as fobj:
        return fobj.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


# Get the long description from the relevant file
long_description = read('README.md')


install_requires = [
    'PyYAML >= 3.11'
]


tests_require = [
    'mock >= 1.0.1',
    'nose',
]


classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',

    'License :: OSI Approved :: Apache Software License',

    'Programming Language :: Python :: 2.7',
]


if sys.version_info < (2, 7):
    tests_require.append('unittest2')


setup(
    name='wharfrat',
    version=find_version("wharfrat", "__init__.py"),
    description='Convert config files into docker commands',
    long_description=long_description,
    author='Paul Becotte',
    author_email='pjbecotte@gmail.com',
    url='https://github.com/pbecotte/wharfrat',
    license='Apache License 2.0',
    packages=find_packages(exclude=['tests.*', 'tests']),
    include_package_data=True,
    test_suite='nose.collector',
    install_requires=install_requires,
    tests_require=tests_require,
    classifiers=classifiers,
    entry_points="""
    [console_scripts]
    wharfrat=wharfrat.command:main
    """,
    keywords='docker orchestration dev tools'
)
