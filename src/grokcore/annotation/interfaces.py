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
"""Grok interfaces
"""

from zope import interface


class IBaseClasses(interface.Interface):
    """grokcore.annotation base classes.
    """
    Annotation = interface.Attribute("Base class for persistent annotations.")


class IAnnotationFactory(interface.Interface):
    factory = interface.Attribute('Class to create a new annotation')
    name = interface.Attribute('Name of the annotation')

    def get(context):
        """Return the existing annotation or None if None exists.
        """

    def __call__(context):
        """Return the existing annotation or create a new one.
        """


class IGrokcoreAnnotationAPI(IBaseClasses):
    """grokcore.annotation API description.
    """
    queryAnnotation = interface.Attribute('Function to query an annotation')
