bhive - Unofficial Python Library for Hive
==========================================

bhive is an unofficial python library for hive, which is created new from beem
The library name is a play on word from beem and hive making a bee hive. bhive includes `python-graphenelib`_.

.. image:: https://img.shields.io/pypi/v/bhive.svg
    :target: https://pypi.python.org/pypi/bhive/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/pyversions/bhive.svg
    :target: https://pypi.python.org/pypi/bhive/
    :alt: Python Versions

Installation
============
The minimal working python version is 2.7.x. or 3.4.x
Tested on python versoin 3.7.5

bhive can be installed parallel to python-hive and beem.

For Debian and Ubuntu, please ensure that the following packages are installed:

.. code:: bash

    sudo apt-get install build-essential libssl-dev python-dev

For Fedora and RHEL-derivatives, please ensure that the following packages are installed:

.. code:: bash

    sudo yum install gcc openssl-devel python-devel

For OSX, please do the following::

    brew install openssl
    export CFLAGS="-I$(brew --prefix openssl)/include $CFLAGS"
    export LDFLAGS="-L$(brew --prefix openssl)/lib $LDFLAGS"

For Termux on Android, please install the following packages:

.. code:: bash

    pkg install clang openssl-dev python-dev

Signing and Verify can be fasten (200 %) by installing cryptography:

.. code:: bash

    pip install -U cryptography

or:

.. code:: bash

    pip install -U secp256k1prp

Install or update bhive by pip::

    pip install -U bhive

You can install bhive from this repository if you want the latest
but possibly non-compiling version::

    git clone https://github.com/thecrazygmn/bhive.git
    cd bhive
    python setup.py build

    python setup.py install --user

Run tests after install::

    pytest

CLI tool bhivepy
----------------
A command line tool is avail1able. The help output shows the available commands::

    bhivepy --help

Stand alone version of CLI tool bhivepy
---------------------------------------
With the help of pyinstaller, a stand alone version of bhivepy was created for Windows, OSX and linux.
Each version has just to be unpacked and can be used in any terminal. The packed directories
can be found under release. Each release has a hash sum, which is created directly in the build-server
before transmitting the packed file. Please check the hash-sum after downloading.

Changelog
=========
Can be found in CHANGELOG.rst.

License
=======
This library is licensed under the MIT License.

Acknowledgements
================
beem created by holger80 `python-bitshares`_ and `python-graphenelib`_ were created by Fabian Schuh (xeroc).


.. _python-graphenelib: https://github.com/xeroc/python-graphenelib
.. _python-bitshares: https://github.com/xeroc/python-bitshares
.. _Python: http://python.org