##############################################################################
#
# Copyright (c) 2006 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Bootstrap a buildout-based project

Simply run this script in a directory containing a buildout.cfg.
"""

import os
import shutil
import subprocess
import sys
import tempfile


tmpeggs = tempfile.mkdtemp()
ZCBUILDOUT = '2.11.3'


######################################################################
# load/install setuptools

try:
    import pkg_resources
    import setuptools  # NOQA
except ImportError:
    ez = {}

    try:
        from urllib.request import urlopen
    except ImportError:
        from urllib2 import urlopen

    exec(urlopen('https://bootstrap.pypa.io/ez_setup.py').read(), ez)
    # Do not update setuptools version that is the latest working version evar.
    setup_args = dict(
        to_dir=tmpeggs,
        version='33.1.1',
        download_delay=0)
    ez['use_setuptools'](**setup_args)

    import pkg_resources
    # This does not (always?) update the default working set.  We will
    # do it.
    for path in sys.path:
        if path not in pkg_resources.working_set.entries:
            pkg_resources.working_set.add_entry(path)

######################################################################
# Install buildout

ws = pkg_resources.working_set
requirement = '=='.join(('zc.buildout', ZCBUILDOUT))
cmd = [sys.executable, '-c',
       'from setuptools.command.easy_install import main; main()',
       '-mZqNxd', tmpeggs, requirement]

setuptools_path = ws.find(
    pkg_resources.Requirement.parse('setuptools')).location

if subprocess.call(cmd, env=dict(os.environ, PYTHONPATH=setuptools_path)) != 0:
    raise Exception(
        "Failed to execute command:\n%s",
        repr(cmd)[1:-1])

######################################################################
# Import and run buildout

ws.add_entry(tmpeggs)
ws.require(requirement)
import zc.buildout.buildout

zc.buildout.buildout.main(['bootstrap'])
shutil.rmtree(tmpeggs)
