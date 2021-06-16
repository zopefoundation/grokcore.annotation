##############################################################################
#
# Copyright (c) 2007 Zope Foundation and Contributors.
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
"""Grok test helpers
"""
from __future__ import print_function
import sys
from zope.configuration.config import ConfigurationMachine
from grokcore.component import zcml
# Provide this import here for BBB reasons:


def grok(module_name):
    config = ConfigurationMachine()
    zcml.do_grok('grokcore.component.meta', config)
    zcml.do_grok('grokcore.annotation.meta', config)
    zcml.do_grok(module_name, config)
    config.execute_actions()


def warn(message, category=None, stacklevel=1):
    """Intended to replace warnings.warn in tests.

    Modified copy from zope.deprecation.tests to:

      * make the signature identical to warnings.warn
      * to check for *.pyc and *.pyo files.

    When zope.deprecation is fixed, this warn function can be removed again.
    """
    print("From grok.testing's warn():")

    frame = sys._getframe(stacklevel)
    path = frame.f_globals['__file__']
    if path.endswith('.pyc') or path.endswith('.pyo'):
        path = path[:-1]

    file = open(path)
    lineno = frame.f_lineno
    for i in range(lineno):
        line = file.readline()

    print("{}:{}: {}: {}\n  {}".format(
        path,
        frame.f_lineno,
        category.__name__,
        message,
        line.strip(),
    ))
