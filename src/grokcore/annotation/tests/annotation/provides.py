"""
  >>> grok.testing.grok(__name__)
  >>> from zope import component
  >>> from zope.annotation.attribute import AttributeAnnotations
  >>> component.provideAdapter(AttributeAnnotations)

If an annotation class implements more than one interface, it has to
declare which one it should be registered for using ``grok.provides``.

  >>> manfred = Mammoth()
  >>> ann = IOneInterface(manfred)

It can then be looked up only using that one interface:

  >>> IAnotherOne(manfred)
  Traceback (most recent call last):
  TypeError: ('Could not adapt', <grokcore.annotation.tests.annotation.provides.Mammoth object at ...>, <InterfaceClass grokcore.annotation.tests.annotation.provides.IAnotherOne>)


"""

import grokcore.annotation as grok
from zope import interface


class Mammoth(grok.Model):
    pass


class IOneInterface(interface.Interface):
    pass


class IAnotherOne(interface.Interface):
    pass


@grok.implementer(IOneInterface, IAnotherOne)
class MammothAnnotation(grok.Annotation):
    grok.provides(IOneInterface)
