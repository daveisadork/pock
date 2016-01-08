Introduction
============

``pock`` is a library that aims to make interacting with Pacemaker as simple as possible.
It has Python bindings, as well as a command-line interface based on
`click <https://github.com/mitsuhiko/click>`_. It's in an early stage of development, so
don't rely on it for anything critical.

Installation
============

Clone this repository:

    git clone https://github.com/mechaxl/pock.git && cd pock/

And install using setuptools:

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

