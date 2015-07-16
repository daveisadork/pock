``pock`` is a library that aims to make interacting with Pacemaker as simple as possible.
It has Python bindings, as well as a command-line interface based on `click <https://github.com/mitsuhiko/click>`_.

Installation
============

The easiest way to install pock is to use ``pip``.

    pip install pock

To install without ``pip``, clone this repository like this.

    git clone https://github.com/mechaxl/pock.git

And install using setuptools.

    python setup.py install

Example Usage
=============

From the CLI
------------

.. code:: bash

    pock resources list

In Python
---------

.. code:: python

    import pock

    pock.resources.list()

Build Status
============
.. image:: https://travis-ci.org/mechaxl/pock.svg
    :target: https://travis-ci.org/mechaxl/pock