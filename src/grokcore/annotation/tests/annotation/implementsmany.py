"""
An annotations class must implement either exactly one interface, or
it should cspecify which of the many implemented interfaces it should
be registered for.  Ambiguities lead to errors:

  >>> grok.testing.grok(__name__)
  Traceback (most recent call last):
  ...
  martian.error.GrokError: <class 'grokcore.annotation.tests.annotation.implementsmany.MammothAnnotations'> is implementing more than one interface (use grok.provides to specify which one to use).
"""

import grokcore.annotation as grok
from zope import interface

class Mammoth(grok.Model):
    pass

class IOneInterface(interface.Interface):
    pass

class IAnotherInterface(interface.Interface):
    pass

@grok.implementer(IOneInterface, IAnotherInterface)
class MammothAnnotations(grok.Annotation):
    pass
