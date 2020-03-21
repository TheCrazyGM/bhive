bhive - Unofficial Python Library for Hive
===============================================

bhive is an unofficial python library for hive, which is created new from scratch from `python-bitshares`_
The library name is derived from a beam machine, similar to the analogy between hive and steam. bhive includes `python-graphenelib`_.

.. image:: https://img.shields.io/pypi/v/bhive.svg
    :target: https://pypi.python.org/pypi/bhive/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/pyversions/bhive.svg
    :target: https://pypi.python.org/pypi/bhive/
    :alt: Python Versions


.. image:: https://anaconda.org/conda-forge/bhive/badges/version.svg
    :target: https://anaconda.org/conda-forge/bhive


.. image:: https://anaconda.org/conda-forge/bhive/badges/downloads.svg
    :target: https://anaconda.org/conda-forge/bhive


Current build status
--------------------

.. image:: https://travis-ci.org/thecrazygmn/bhive.svg?branch=master
    :target: https://travis-ci.org/thecrazygmn/bhive

.. image:: https://ci.appveyor.com/api/projects/status/ig8oqp8bt2fmr09a?svg=true
    :target: https://ci.appveyor.com/project/thecrazygm/bhive

.. image:: https://circleci.com/gh/thecrazygmn/bhive.svg?style=svg
    :target: https://circleci.com/gh/thecrazygmn/bhive

.. image:: https://readthedocs.org/projects/bhive/badge/?version=latest
  :target: http://bhive.readthedocs.org/en/latest/?badge=latest

.. image:: https://api.codacy.com/project/badge/Grade/e5476faf97df4c658697b8e7a7efebd7
    :target: https://www.codacy.com/app/thecrazygmn/bhive?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=thecrazygmn/bhive&amp;utm_campaign=Badge_Grade

.. image:: https://pyup.io/repos/github/thecrazygmn/bhive/shield.svg
     :target: https://pyup.io/repos/github/thecrazygmn/bhive/
     :alt: Updates

.. image:: https://api.codeclimate.com/v1/badges/e7bdb5b4aa7ab160a780/test_coverage
   :target: https://codeclimate.com/github/thecrazygmn/bhive/test_coverage
   :alt: Test Coverage

Installation
============
The minimal working python version is 2.7.x. or 3.4.x

bhive can be installed parallel to python-hive.

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


Installing bhive with conda-forge
--------------------------------

Installing bhive from the conda-forge channel can be achieved by adding conda-forge to your channels with::

    conda config --add channels conda-forge

Once the conda-forge channel has been enabled, bhive can be installed with::

    conda install bhive

Signing and Verify can be fasten (200 %) by installing cryptography::

    conda install cryptography

bhive can be updated by::

    conda update bhive

CLI tool bhivepy
---------------
A command line tool is available. The help output shows the available commands::

    bhivepy --help

Stand alone version of CLI tool bhivepy
--------------------------------------
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
`beem`_ created by holgern80 `python-bitshares`_ and `python-graphenelib`_ were created by Fabian Schuh (xeroc).


.. _python-graphenelib: https://github.com/xeroc/python-graphenelib
.. _python-bitshares: https://github.com/xeroc/python-bitshares
.. _Python: http://python.org
.. _Anaconda: https://www.continuum.io
.. _bhive.readthedocs.io: http://bhive.readthedocs.io/en/latest/
.. _bhive-discord-channel: https://discord.gg/4HM592V
