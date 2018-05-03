========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |coveralls| |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

.. |docs| image:: https://readthedocs.org/projects/dupuis/badge/?style=flat
    :target: https://readthedocs.org/projects/dupuis
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/redapple/dupuis.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/redapple/dupuis

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/redapple/dupuis?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/redapple/dupuis

.. |requires| image:: https://requires.io/github/redapple/dupuis/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/redapple/dupuis/requirements/?branch=master

.. |coveralls| image:: https://coveralls.io/repos/redapple/dupuis/badge.svg?branch=master&service=github
    :alt: Coverage Status
    :target: https://coveralls.io/r/redapple/dupuis

.. |codecov| image:: https://codecov.io/github/redapple/dupuis/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/redapple/dupuis

.. |version| image:: https://img.shields.io/pypi/v/dupuis.svg
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/dupuis

.. |commits-since| image:: https://img.shields.io/github/commits-since/redapple/dupuis/v0.1.0.svg
    :alt: Commits since latest release
    :target: https://github.com/redapple/dupuis/compare/v0.1.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/dupuis.svg
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/dupuis

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/dupuis.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/dupuis

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/dupuis.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/dupuis


.. end-badges

UI tools for record deduplication and linkage

* Free software: MIT license

Installation
============

::

    pip install dupuis

Documentation
=============

https://dupuis.readthedocs.io/

Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
