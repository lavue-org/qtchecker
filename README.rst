Qt Checker
==========

Authors: Jan Kotański <jan.kotanski at desy.de>

Introduction
------------

This is a simple helper module to perform PyQt GUI tests.

In the qtchecker tests user

1. creates ```QtChecker``` object  with the global QApplication object and a given tested QWidget dialog parameters
2. defines a sequence of checks with ``setChecks()``` method and the following helper classes:
- ```AttrCheck```  - read a tested dialog attribute value
- ```CmdCheck``` - execute a tested dialog command and read its result value
- ```WrapAttrCheck``` - execute a wrapper command on a tested dialog attribute
- ```WrapCmdCheck``` - execute a wrapper command on a result value of a tested dialog command
- ```ExtAttrCheck``` - read an external attribute value defined outside the dialog 
- ```ExtCmdCheck``` - execute an external command defined outside the dialog and read its result value
classes
3. starts event loop and performs checkes with ```executeChecks()``` or  ```executeChecksAndClose()``` method
4. compare results by reading ```results``` attribute of executing

for example   

.. code-block:: python

    from PyQt5 import QtGui
    from PyQt5 import QtCore
    from PyQt5 import QtTest

    # QApplication object should be one for all tess
    app = QtGui.QApplication([])

    def test_run(self):

        # my tested MainWindow dialog
        dialog = MainWindow()
        dialog.show()

	# create QtChecker object
	qtck = qtchecker.QtChecker(app, dialog)

	# define a sequence of action of the dialog
        qtck.setChecks([
	    # read return value of execute isConnected command
            qtchecker.CmdCheck(
	        # a python path to a method executed in the first action 
	        "_MainWindow__lavue._LiveViewer__sourcewg.isConnected"
            ),
	    # click pushButton with the left-mouse-click
	    qtchecker.WrapAttrCheck(
	        # a python path to an pushButton object
	        "_MainWindow__lavue._LiveViewer__sourcewg._SourceTabWidget__sourcetabs[],0._ui.pushButton",
		# Wrapper command to be executed on the action object
		QtTest.QTest.mouseClick,
		# additional parameters of the wrapper command
		[QtCore.Qt.LeftButton]
	    ),
	    # click pushButton with the left-mouse-click
	    qtchecker.ExtCmdCheck(
                # parent object of an external method
		self,
		# external method name
		"getLavueState"
	    ),
	])

	# execute the check actions
	status = qtck.executeChecksAndClose()
	self.assertEqual(status, 0)

        # compare results returned by each action
	qtck.compareResults(self,
	    [
	        True,
		None,
		'{"connected": false}'
            ]
	)

More examples can be found at like `LavueTests
<https://github.com/jkotan/lavue/blob/develop/test/CommandLineArgument_test.py/>`_  `LavueStateTests
<https://github.com/jkotan/lavue/blob/develop/test/CommandLineLavueState_test.py/>`_.
	
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
