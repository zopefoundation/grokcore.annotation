"""
  >>> grok.testing.grok(__name__)
  >>> from zope import component
  >>> from zope.annotation.attribute import AttributeAnnotations
  >>> component.provideAdapter(AttributeAnnotations)
  >>> manfred = Mammoth()

We can adapt a model to an annotation interface and obtain a value for
its attributes:

  >>> lazyannotation = ILazy(manfred)
  >>> lazyannotation.lazy_attribute
  u'lazily waiting for a value.'

Note how just "getting" the annotation attribute's default value (as no
explicit value has been set before for this attribute), does not create
a new annotation objects:

  >>> print manfred.__dict__
  {}

If nothing was explicitly set before, we still can query for the annotation
and indeed get None for it and it won't create an object:

  >>> grok.queryAnnotation(manfred, ILazy) is None
  True

When setting an explicit value for the attribute on the annotations, we
actually do store a new annotation object:

  >>> lazyannotation.lazy_attribute = u'We have a value!'
  >>> print manfred.__dict__
  {'__annotations__': <...OOBTree object at ...>}

  >>> print list(manfred.__dict__['__annotations__'].keys())
  ['lazy.annotation.custom.name']

Now the queryAnnotation will indeed return the annotations object:

  >>> grok.queryAnnotation(manfred, ILazy)
  <...Lazy object at ...>

  >>> grok.queryAnnotation(manfred, ILazy).lazy_attribute
  u'We have a value!'

We can also delete the lazy annotation and the previously stored annotation
now is gone:

  >>> grok.deleteAnnotation(manfred, ILazy)
  True

  >>> print manfred.__dict__
  {'__annotations__': <...OOBTree object at ...>}

  >>> print list(manfred.__dict__['__annotations__'].keys())
  []

Note how the default schema value for the lazy attribute still "responds":

  >>> lazyannotation = ILazy(manfred)
  >>> lazyannotation.lazy_attribute
  u'lazily waiting for a value.'

"""

import grokcore.annotation as grok

from zope import interface
from zope import schema


class Mammoth(grok.Model):
    pass


class ILazy(interface.Interface):

    lazy_attribute = schema.TextLine(
        title=u'So, so lazy', default=u'lazily waiting for a value.')


class Lazy(grok.LazyAnnotation):
    grok.implements(ILazy)
    grok.name('lazy.annotation.custom.name')
    grok.provides(ILazy)

    lazy_attribute = grok.LazyAnnotationProperty(
        ILazy['lazy_attribute'])
