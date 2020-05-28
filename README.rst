Qt Checker
==========

Authors: Jan Kotański <jan.kotanski at desy.de>

Introduction
------------

This is a simple helper module to perform PyQt GUI tests.


Installation
------------

QtChecker requires the following python packages: ``qt4`` or  ``qt5`` or ``pyqtgraph``.



From sources
""""""""""""

Download the latest QtChecker version from https://github.com/jkotan/qtchecker

Extract sources and run

.. code-block:: console

   $ python setup.py install

The ``setup.py`` script may need: ``setuptools  sphinx  numpy  pytest`` python packages as well as ``qtbase5-dev-tools`` or ``libqt4-dev-bin``.

Debian packages
"""""""""""""""

Debian `buster` and `stretch` or Ubuntu  `focal`, `eoan`, `bionic` packages can be found in the HDRI repository.

To install the debian packages, add the PGP repository key

.. code-block:: console

   $ sudo su
   $ wget -q -O - http://repos.pni-hdri.de/debian_repo.pub.gpg | apt-key add -

and then download the corresponding source list, e.g.

.. code-block:: console

   $ cd /etc/apt/sources.list.d

and

.. code-block:: console

   $ wget http://repos.pni-hdri.de/buster-pni-hdri.list

or

.. code-block:: console

   $ wget http://repos.pni-hdri.de/stretch-pni-hdri.list

or

.. code-block:: console

   $ wget http://repos.pni-hdri.de/focal-pni-hdri.list

respectively.

Finally,

.. code-block:: console

   $ apt-get update
   $ apt-get install python-qtchecker

.. code-block:: console

   $ apt-get update
   $ apt-get install python3-qtchecker

for python 3 version.

From pip
""""""""

To install it from pip you need to install pyqt5 in advance, e.g.

.. code-block:: console

   $ python3 -m venv myvenv
   $ . myvenv/bin/activate
   
   $ pip install pyqt5
   
   $ pip install qtchecker

