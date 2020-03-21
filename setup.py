# -*- coding: utf-8 -*-
"""Packaging logic for bhive."""
import codecs
import io
import os

from setuptools import setup

# Work around mbcs bug in distutils.
# http://bugs.python.org/issue10945

try:
    codecs.lookup('mbcs')
except LookupError:
    ascii = codecs.lookup('ascii')
    codecs.register(lambda name, enc=ascii: {True: enc}.get(name == 'mbcs'))

VERSION = '0.23.0'

tests_require = ['mock >= 2.0.0', 'pytest', 'pytest-mock', 'parameterized']

requires = [
    "future",
    "ecdsa",
    "requests",
    "websocket-client",
    "appdirs",
    "Events",
    "scrypt",
    "pylibscrypt",
    "pycryptodomex",
    "pytz",
    "Click",
    "prettytable",
    "pyyaml"
]


def write_version_py(filename):
    """Write version."""
    cnt = """\"""THIS FILE IS GENERATED FROM bhive SETUP.PY.\"""
version = '%(version)s'
"""
    with open(filename, 'w') as a:
        a.write(cnt % {'version': VERSION})


def get_long_description():
    """Generate a long description from the README file."""
    descr = []
    for fname in ('README.rst',):
        with io.open(fname, encoding='utf-8') as f:
            descr.append(f.read())
    return '\n\n'.join(descr)


if __name__ == '__main__':

    # Rewrite the version file everytime
    write_version_py('bhive/version.py')
    write_version_py('bhivebase/version.py')
    write_version_py('bhiveapi/version.py')
    write_version_py('bhivegraphenebase/version.py')

    setup(
        name='bhive',
        version=VERSION,
        description='Unofficial Python library for HIVE',
        long_description=get_long_description(),
        download_url='https://github.com/thecrazygmn/bhive/tarball/' + VERSION,
        author='Holger Nahrstaedt',
        author_email='thecrazygm@gmail.com',
        maintainer='Holger Nahrstaedt',
        maintainer_email='thecrazygm@gmail.com',
        url='http://www.github.com/thecrazygmn/bhive',
        keywords=['hive', 'library', 'api', 'rpc'],
        packages=[
            "bhive",
            "bhiveapi",
            "bhivebase",
            "bhivegraphenebase",
            "bhivegrapheneapi"
        ],
        classifiers=[
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'Intended Audience :: Financial and Insurance Industry',
            'Topic :: Office/Business :: Financial',
        ],
        install_requires=requires,
        entry_points={
            'console_scripts': [
                'bhivepy=bhive.cli:cli',
            ],
        },
        setup_requires=['pytest-runner'],
        tests_require=tests_require,
        include_package_data=True,
    )
