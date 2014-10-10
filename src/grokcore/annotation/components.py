##############################################################################
#
# Copyright (c) 2006-2007 Zope Foundation and Contributors.
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
"""Base classes for Grok application components.

"""

from zope.annotation.interfaces import IAttributeAnnotatable
from zope.annotation.interfaces import IAnnotations
from zope.container import contained
from zope.interface import implements, providedBy
from grokcore.annotation.interfaces import IAnnotationFactory
import persistent
import grokcore.component
import zope.component


class Model(grokcore.component.Context):
    """Base class for an object which is able to handle annotations
    """
    grokcore.component.implements(IAttributeAnnotatable)


class Annotation(persistent.Persistent, contained.Contained):
    """The base class for annotation classes in Grok applications.

    Inherits from the :class:`persistent.Persistent` class.
    """


class AnnotationFactory(object):
    implements(IAnnotationFactory)

    def __init__(self, factory, name):
        self.factory = factory
        self.name = name

    def get(self, context):
        """Return None if the annotation doesn't exists.
        """
        annotations = IAnnotations(context)
        return annotations.get(self.name)

    def __call__(self, context):
        annotations = IAnnotations(context)
        try:
            result = annotations[self.name]
        except KeyError:
            result = self.factory()
            annotations[self.name] = result

        if result.__parent__ is None:
            result.__parent__ = context
            result.__name__ = self.name

        return result


def queryAnnotation(context, interface):
    manager = zope.component.getSiteManager()
    factory = manager.adapters.lookup((providedBy(context),), interface)
    if factory is None or not IAnnotationFactory.providedBy(factory):
        return None
    return factory.get(context)
