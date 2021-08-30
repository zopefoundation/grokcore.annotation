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

import collections
import sys

import ZODB

from zope.configuration.config import ConfigurationMachine
from grokcore.component import zcml



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


_marker = object()


class ReferenceMap:
    """Builds a references/back-references map for the given database.
    Useful in tests, assuming small(!) datasets and a DemoStorage (or
    MappingStorage) database implementation, which (almost?) all of our
    testcases do use.
    Note: do not forget to transaction.commit() after modification to
    stored objects, before building the reference map.
    """

    def __init__(self, any_persisted_object):
        db = any_persisted_object._p_jar.db()
        self._c = db.open()
        self._s = self._c._storage
        self._outgoing = collections.defaultdict(set)
        self._incoming = collections.defaultdict(set)
        self.index()

    def index(self, current=_marker, seen=_marker):
        """Build the an index of outgoing and incoming object references.
        Indexing starts at the database root object (which is not the
        Zope root folder BTW).
        """
        if current is _marker:
            current = ZODB.utils.p64(0)  # 0 is oid for ZODB root.
        if seen is _marker:
            seen = set()
        if current in seen:
            return
        seen.add(current)
        refs = ZODB.serialize.referencesf(self._s.load(current)[0])
        for ref in refs:
            self._outgoing[current].add(ref)
            self._incoming[ref].add(current)
            self.index(current=ref, seen=seen)

    def __contains__(self, oid):
        """Check to see if the oid is refered to by an object closer to the
        root of the object graph.
        """
        return oid in self._outgoing

    def outgoing_refs(self, oid):
        return self._outgoing[oid]

    def incoming_refs(self, oid):
        return self._incoming[oid]

    def _recurse_paths(self, target_oid, depth, seen=None):
        if depth == 0:
            return
        if seen is None:
            seen = set()
        for source_oid in self._incoming[target_oid]:
            if (source_oid, target_oid, depth) in seen:
                continue
            yield depth, source_oid, target_oid
            yield from self._recurse_paths(source_oid, depth - 1, seen=seen)
            seen.add((source_oid, target_oid, depth))

    def path(self, from_oid, to_oid, max_depth=20):
        """Find shortest path from `from_oid` - the object being nearer to the
        root of the graph - to `to_oid` - the object deeper in the graph.
        Return None if no path can be found.
        """
        parents = {}
        steps = self._recurse_paths(to_oid, max_depth)
        for depth, source_oid, target_oid in steps:
            info = (max_depth - depth, target_oid)
            if info < parents.get(source_oid, (sys.maxsize, None)):
                parents[source_oid] = info
        path = []
        parent_oid = from_oid
        while parent_oid != to_oid:
            info = parents.get(parent_oid)
            if info is None:
                return None
            path.append(info[1])
            parent_oid = info[1]
        path.reverse()
        path.append(from_oid)
        return path

    def describe(self, oids):
        for oid in oids:
            obj = self._c.get(oid)
            yield obj.__class__, getattr(obj, '__name__', 'n/a')

    def realize(self, oids):
        for oid in oids:
            yield self._c.get(oid)
