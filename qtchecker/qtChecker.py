# Copyright (C) 2017  DESY, Notkestr. 85, D-22607 Hamburg
#
# qtchecker is a helper python module for PyQt gui test.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation in  version 2
# of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA  02110-1301, USA.
#
# Authors:
#     Jan Kotanski <jan.kotanski@desy.de>
#

import os

qt_api = os.getenv("QT_API", os.getenv('DEFAULT_QT_API', 'pyqt5'))
if qt_api != 'pyqt4':
    try:
        from PyQt5 import QtGui
        from PyQt5 import QtCore
        from PyQt5 import QtTest
    except Exception:
        from PyQt4 import QtGui
        from PyQt4 import QtCore
        from PyQt4 import QtTest
else:
    from PyQt4 import QtGui
    from PyQt4 import QtCore
    from PyQt4 import QtTest


""" qt checker for testing gui """


class Check(object):
    """ abstract check class
    """

    def __init__(self, path):
        """ constructor

        :param path: check item path
        :type path: :obj:`str`
        """

        #: (:obj:`str`) checker path
        self._path = path or ""
        spath = path.split(".")
        self._lpath = spath[:-1]
        self._item = spath[-1]

    def path(self):
        """ provides the widget path

        :returns: widget path
        :rtype: :obj:`str`
        """
        return self._path

    def execute(self, dialog):
        """ abstract execute

        :param dialog: qt dialog
        :type dialog: :obj:`any`
        """

    def _getparent(self, dialog):
        """ abstract execute

        :param dialog: qt dialog
        :type dialog: :obj:`any`
        """
        parent = dialog
        for itm in self._lpath:
            if "[]," in itm:
                sitm = itm.split(",")
                itm = sitm[0][:-2]
                try:
                    parent = getattr(parent, itm)[int(sitm[1])]
                except Exception:
                    parent = getattr(parent, itm)[sitm[1]]
            else:
                parent = getattr(parent, itm)
        return parent


class CmdCheck(Check):

    def __init__(self, path, params=None):
        Check.__init__(self, path)
        """ constructor

        :param path: check item path
        :type path: :obj:`str`
        :param params: a list of wrapper parameters
        :type params: :obj:`dict` <:obj:`str`, :obj:`any`>
        """
        self._params = params

    def execute(self, dialog):
        """ execute command

        :param dialog: qt dialog
        :type dialog: :obj:`any`
        """
        parent = self._getparent(dialog)
        cmd = getattr(parent, self._item)
        if self._params:
            return cmd(**self._params)
        else:
            return cmd()


class WrapCmdCheck(Check):

    def __init__(self, path, params,
                 wcmd, wparams=None, wpos=0):
        CmdCheck.__init__(self, path, params)
        Check.__init__(self, path)
        """ constructor

        :param path: check item path
        :type path: :obj:`str`
        :param params: a list of wrapper parameters or None
        :type params: :obj:`dict` <:obj:`str`, :obj:`any`>
        :param wcmd: wcmd command
        :type wcmd: :obj:`func`
        :param wparams: a list of wrapper parameters
        :type wparams: :obj:`list`
        :param wpos: position of wrapping object
        :type wpos: :obj:`int`
        """
        self._wcmd = wcmd
        self._wparams = wparams
        self._wpos = wpos

    def execute(self, dialog):
        """ execute command

        :param dialog: qt dialog
        :type dialog: :obj:`any`
        """
        cmdres = CmdCheck.execute(self, dialog)
        if not self._wparams:
            wp = [cmdres]
        else:
            wp = list(self._wparams)
            wp.insert(self._wpos, cmdres)
        return self._wcmd(*wp)


class AttrCheck(Check):

    def __init__(self, path):
        Check.__init__(self, path)
        """ constructor

        :param path: check item path
        :type path: :obj:`str`
        """

    def execute(self, dialog):
        """ execute command

        :param dialog: qt dialog
        :type dialog: :obj:`any`
        """
        parent = self._getparent(dialog)
        return getattr(parent, self._item)


class ExtAttrCheck(Check):

    def __init__(self, parent, atname):
        Check.__init__(self, "")
        """ constructor

        :param parent: parent object
        :type parent: :obj:`any`
        :param atname: attribute name
        :type atname: :obj:`str`
        """
        self._parent = parent
        self._atname = atname

    def execute(self, _):
        """ execute command
        """
        return getattr(self._parent, self._atname)


class ExtCmdCheck(Check):

    def __init__(self, parent, cmdname, cmdparams=None):
        Check.__init__(self, "")
        """ constructor

        :param parent: parent object
        :type parent: :obj:`any`
        :param atname: command name
        :type atname: :obj:`str`
        """
        self._parent = parent
        self._cmdname = cmdname
        self._cmdparams = cmdparams

    def execute(self, _):
        """ execute command
        """
        cmd = getattr(self._parent, self._cmdname)
        if not self._cmdparams:
            return cmd()
        else:
            return cmd(*self._cmdparams)


class WrapAttrCheck(AttrCheck):

    def __init__(self, path, wcmd, wparams=None, wpos=0):
        AttrCheck.__init__(self, path)
        """ constructor

        :param path: check item path
        :type path: :obj:`str`
        :param wcmd: wcmd command
        :type wcmd: :obj:`func`
        :param wparams: a list of wrapper parameters
        :type wparams: :obj:`list`
        :param wpos: position of wrapping object
        :type wpos: :obj:`int`

        """
        self._wcmd = wcmd
        self._wparams = wparams
        self._wpos = wpos

    def execute(self, dialog):
        """ execute command

        :param dialog: qt dialog
        :type dialog: :obj:`any`
        """
        attr = AttrCheck.execute(self, dialog)
        if not self._wparams:
            wp = [attr]
        else:
            wp = list(self._wparams)
            wp.insert(self._wpos, attr)
        return self._wcmd(*wp)


class QtChecker(object):

    def __init__(self, app=None, dialog=None, verbose=False,
                 qtgui=None, qtcore=None, qttest=None, sleep=0):
        """ constructor

        :param app:  application object
        :type app: :class:`PyQt5.QtGui.QApplication`
        :param dialog: qt dialog
        :type dialog: :obj:`any`
        :param verbose: verbose flag
        :type verbose: :obj:`bool`
        :param qtgui: QtGui module
        :type qtgui:  :obj:`any`
        :param qtcore: QtCore module
        :type qtcore:  :obj:`any`
        :param qttest: QtTest module
        :type qttest:  :obj:`any`
        :param sleep: sleep time in ms
        :type sleep: :obj:`int`
        """
        self.QtGui = qtgui or QtGui
        self.QtCore = qtcore or QtCore
        self.QtTest = qttest or QtTest
        self.__app = app
        if app is None:
            self.__app = self.QtGui.QApplication([])

        self.__dialog = dialog
        self.__checks = []
        self.__results = []
        self.__verbose = verbose
        self.__sleep = sleep

    def setDialog(self, dialog):
        """ sets dialog

        :param dialog: qt dialog
        :type dialog: :obj:`any`
        """
        self.__dialog = dialog

    def setChecks(self, checks):
        """ sets check items

        :param checks: a list of Check items
        :type checks: :obj:`list` <:class:`Check`>
        """
        self.__checks = checks

    def results(self):
        """ provides a list of result objects

        :returns: a list of result objects
        :rtype: :obj:`list` <:class:`any`>
        """
        return self.__results

    def executeChecksAndClose(self, delay=1000):
        """ executes check items and close the dialog in a separate thread

        :param delay: delay time in ms
        :type delay: :obj:`int`
        """
        self.__results = []
        self.QtCore.QTimer.singleShot(1000, self._executeChecksAndClose)
        status = self.__app.exec_()
        if self.__verbose:
            print("Status %s" % status)
        return status

    def executeChecks(self, delay=1000):
        """ executes check items

        :param delay: delay time in ms in a separate thread
        :type delay: :obj:`int`
        """
        self.__results = []
        self.QtCore.QTimer.singleShot(1000, self._executeChecks)
        status = self.__app.exec_()
        if self.__verbose:
            print("Status %s" % status)
        return status

    def _executeChecksAndClose(self):
        """ executes check items and close the dialog
        """
        self._executeChecks()
        if self.__dialog:
            self.__dialog.close()
            if self.__verbose:
                print("Close Dialog")
            self.__dialog = None

    def _executeChecks(self):
        """ executes check items
        """
        for i, ch in enumerate(self.__checks):
            if self.__verbose:
                print("Execute %s: %s" % (i, ch.path()))
            self.__results.append(ch.execute(self.__dialog))
            self.QtCore.QCoreApplication.processEvents()
            if self.__sleep:
                QtTest.QTest.qWait(self.__sleep)

    def compareResults(self, testcase, results, mask=None):
        """ compare results with use of testcase.assertEqual

        :param testcase: test case object
        :type testcase: :class:`unittest.TestCase`
        :param results: a list of template result objects
        :type results: :obj:`list` <:class:`any`>
        :param mask: a list of flags
        :type mask: :obj:`list` <:obj:`bool`>
        """
        mask = mask or []
        testcase.assertEqual(len(self.__results), len(results))
        for i, rs in enumerate(self.__results):
            if len(mask) <= i or not mask[i]:
                if self.__verbose and rs != results[i]:
                    print("Difference at %s: %s <> %s" % (i, rs, results[i]))
                testcase.assertEqual(rs, results[i])
