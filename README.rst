Qt Checker
==========

Authors: Jan Kotański <jan.kotanski at desy.de>

Introduction
------------

This is a simple helper module to perform PyQt GUI tests.
In the qtchecker tests the user
1. creates ```QtChecker``` object  with global QApplication object and tested QWidget object parameters
2. defines a sequence of checks with ``setChecks()``` method and ```CmdCheck```, ```AttrCheck```  ```WrapCmdCheck```, ```WrapAttrCheck``` classes
3. starts event loop and performs checkes with ```executeChecks()``` or  ```executeChecksAndClose()``` method
4. compare results by reading ```results``` attribute of executing 


.. code-block:: python
:emphasize-lines: 3,5


    from PyQt5 import QtGui
    from PyQt5 import QtCore
    from .Qt import QtTest
 		  
    # QApplication object should be one for all tess 		  
    app = QtGui.QApplication([])		  
		  
    def test_run(self):

        # my tested dialog
        dialog = MyMainWindow()
        dialog.show()
	qtck = qtchecker.QtChecker(app, dialog)

	# define a sequence of action of the dialog 
        qtck.setChecks([
            qtchecker.CmdCheck("_MainWindow__lavue._LiveViewer__sourcewg.isConnected"),
	    qtchecker.WrapAttrCheck(
	        "_MainWindow__lavue._LiveViewer__sourcewg._SourceTabWidget__sourcetabs[],0._ui.pushButton",
		QtTest.QTest.mouseClick, [QtCore.Qt.LeftButton]),
	])

	# execute the check actions
	status = qtck.executeChecksAndClose()
	self.assertEqual(status, 0)

        # compare results returned by each action
	qtck.compareResults(self, [True, None])

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

