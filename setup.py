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

""" setup.py for setting qtchecker"""

import codecs
import os
from setuptools import setup, find_packages

try:
    from sphinx.setup_command import BuildDoc
except Exception:
    BuildDoc = None


def read(fname):
    """ read the file

    :param fname: readme file name
    :type fname: :obj:`str`
    """
    with codecs.open(os.path.join('.', fname), encoding='utf-8') as f:
        long_description = f.read()
    return long_description

# from sphinx.setup_command import BuildDoc


#: (:obj:`str`) package name
NAME = 'qtchecker'
#: (:obj:`module`) package name
qtcheckerpackage = __import__(NAME)
#: (:obj:`str`) full release version
release = qtcheckerpackage.__version__
#: (:obj:`str`) package version
version = ".".join(release.split(".")[:2])


install_requires = [
    # 'pyqt5',
    # 'pyqtgraph>=0.10.0',
]

#: (:obj:`dict` <:obj:`str`, `any`>) metadata for distutils
SETUPDATA = dict(
    name=NAME,
    version=release,
    description='Live image viewer application for photon science detectors.',
    long_description=read('README.rst'),
    # long_description_content_type='text/x-rst',
    install_requires=install_requires,
    url='https://github.com/jkotan/qtchecker',
    author='J.Kotanski',
    author_email='jan.kotanski@desy.de',
    license='GPLv2',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='pyqt gui test checker helper',
    packages=find_packages(),
    zip_safe=False,
    cmdclass={
        "build_sphinx": BuildDoc
    },
    command_options={
        'build_sphinx': {
            'project': ('setup.py', NAME),
            'version': ('setup.py', version),
            'release': ('setup.py', release)}},
)


def main():
    """ the main function
    """
    setup(**SETUPDATA)


if __name__ == '__main__':
    main()
