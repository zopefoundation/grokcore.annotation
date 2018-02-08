"""
  >>> grok.testing.grok(__name__)
  >>> from zope import component
  >>> from zope.annotation.attribute import AttributeAnnotations
  >>> component.provideAdapter(AttributeAnnotations)

If an annotation class doesn't specify anything else, its dotted name
will be used as an annotation key:

  >>> manfred = Mammoth()
  >>> ann = IImplicitName(manfred)

  >>> from zope.annotation.interfaces import IAnnotations
  >>> availables_ann = IAnnotations(manfred)
  >>> 'grokcore.annotation.tests.annotation.name.ImplicitName' in availables_ann
  True

Of course, annotation classes can explicity specify the name of the
annotation key that they will be stored under.  That's useful if you
want a meaningful key that's accessible from other applications and if
you want to be able to move the class around during refactorings (then
the dotted name will obviously change)

  >>> ann = IExplicitName(manfred)
  >>> availables_ann = IAnnotations(manfred)
  >>> 'grokcore.annotation.tests.annotation.name.ExplicitName' in availables_ann
  False
  >>> 'mammoth.branding' in IAnnotations(manfred)
  True

And the name is stored in __name__:

  >>> ann.__name__
  'mammoth.branding'


"""

import grokcore.annotation as grok
from zope import interface


class Mammoth(grok.Model):
    pass


class IExplicitName(interface.Interface):
    pass


class IImplicitName(interface.Interface):
    pass


@grok.implementer(IExplicitName)
class ExplicitName(grok.Annotation):
    grok.name('mammoth.branding')


@grok.implementer(IImplicitName)
class ImplicitName(grok.Annotation):
    pass
