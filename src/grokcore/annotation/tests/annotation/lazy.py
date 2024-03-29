"""
  >>> grok.testing.grok(__name__)
  >>> from zope import component
  >>> from zope.annotation.attribute import AttributeAnnotations
  >>> component.provideAdapter(AttributeAnnotations)
  >>> manfred = Mammoth()

We can adapt a model to an annotation interface and obtain a value for
its attributes:

  >>> lazyannotation = ILazy(manfred)
  >>> str(lazyannotation.lazy_attribute)
  'lazily waiting for a value.'

Note how just "getting" the annotation attribute's default value (as no
explicit value has been set before for this attribute), does not create
a new annotation objects:

  >>> print(manfred.__dict__)
  {}

If nothing was explicitly set before, we still can query for the annotation
and indeed get None for it and it won't create an object:

  >>> grok.queryAnnotation(manfred, ILazy) is None
  True

When setting an explicit value for the attribute on the annotations, we
actually do store a new annotation object:

  >>> lazyannotation.lazy_attribute = u'We have a value!'
  >>> print(manfred.__dict__)
  {'__annotations__': <...OOBTree object at ...>}

  >>> print(list(manfred.__dict__['__annotations__'].keys()))
  ['lazy.annotation.custom.name']

Now the queryAnnotation will indeed return the annotations object:

  >>> grok.queryAnnotation(manfred, ILazy)
  <...Lazy object at ...>

  >>> str(grok.queryAnnotation(manfred, ILazy).lazy_attribute)
  'We have a value!'

One might expect to be able to explicitely mark the annotation as modified
(for example when the property is a sequence or mapping that is modified).
Flagging the annotation as modiffied should be properly delegated to the
underlying persistent storage object:

  >>> annotation_object = ILazy(manfred)
  >>> annotation_object.storage is not None
  True

  >>> from persistent.tests.utils import TrivialJar
  >>> annotation_object.storage._p_jar = TrivialJar()
  >>> annotation_object._p_changed
  False

  >>> annotation_object.storage._p_changed
  False

  >>> annotation_object._p_changed = True
  >>> annotation_object.storage._p_changed
  True

To increase test coverage we test some edge cases:

   >>> moomoo = Mammoth()
   >>> lazy_anno = ILazy(moomoo)
   >>> lazy_anno._p_changed
   False

  >>> lazy_anno._p_changed = True
  >>> lazy_anno._p_changed
  False

  >>> lazy_anno.lazy_attribute = u'foobar'
  >>> str(lazy_anno.lazy_attribute)
  'foobar'

  >>> lazy_anno.lazy_attribute = u'bazqux'
  >>> str(lazy_anno.lazy_attribute)
  'bazqux'

We can also delete the lazy annotation and the previously stored annotation
now is gone:

  >>> grok.deleteAnnotation(manfred, ILazy)
  True

  >>> print(manfred.__dict__)
  {'__annotations__': <...OOBTree object at ...>}

  >>> print(list(manfred.__dict__['__annotations__'].keys()))
  []

Note how the default schema value for the lazy attribute still "responds":

  >>> lazyannotation = ILazy(manfred)
  >>> str(lazyannotation.lazy_attribute)
  'lazily waiting for a value.'

Now we do some testing for internal details to get all lines covered:

  >>> try:
  ...     lazyannotation.lazy_readonly_attribute = u'foo'
  ... except ValueError as e:
  ...     str(e)
  "('lazy_readonly_attribute', 'field is readonly')"

  >>> Lazy.lazy_attribute
  <...LazyAnnotationProperty object at ...>

  >>> str(Lazy.lazy_attribute.title)
  'So, so lazy'

  >>> ellie = Mammoth()
  >>> ellie_annotation = _IFauxLazy(ellie)
  >>> try:
  ...     ellie_annotation.testing
  ... except AttributeError as e:
  ...     str(e)
  'testing'

  >>> peaches = Mammoth()
  >>> peaches_annotation = IIncorrect(peaches)
  >>> try:
  ...     peaches_annotation.testing = 'foo'
  ... except ValueError as e:
  ...     str(e)
  "('testing', 'invalid context')"

  >>> grok.deleteAnnotation(ellie, ILazy)
  False

  >>> from zope.event import subscribers
  >>> from zope.schema.fieldproperty import FieldUpdatedEvent
  >>> event_log = []
  >>> subscribers.append(event_log.append)
  >>> lazyannotation.lazy_attribute = u"new value"
  >>> len(event_log)
  1
  >>> (str(event_log[0].old_value), str(event_log[0].new_value))
  ('lazily waiting for a value.', 'new value')
  >>> event_log[0].inst is lazyannotation
  True
  >>> event_log[0].field.__name__
  'lazy_attribute'

"""

from zope import interface
from zope import schema

import grokcore.annotation as grok


class Mammoth(grok.Model):
    pass


class ILazy(interface.Interface):

    lazy_attribute = schema.TextLine(
        title='So, so lazy',
        default='lazily waiting for a value.')

    lazy_readonly_attribute = schema.TextLine(
        title='So, so lazy, but readonly',
        default='no writing here',
        readonly=True)


@grok.implementer(ILazy)
class Lazy(grok.LazyAnnotation):
    grok.name('lazy.annotation.custom.name')
    grok.provides(ILazy)

    lazy_attribute = grok.LazyAnnotationProperty(
        ILazy['lazy_attribute'])

    lazy_readonly_attribute = grok.LazyAnnotationProperty(
        ILazy['lazy_readonly_attribute'])


# Fixtures for tests for internal details

class _FauxField:

    def bind(self, other):
        return self


class _IFauxLazy(interface.Interface):
    pass


@grok.implementer(_IFauxLazy)
class FauxLazy(grok.LazyAnnotation):
    grok.provides(_IFauxLazy)

    testing = grok.LazyAnnotationProperty(_FauxField(), 'testing')


class IIncorrect(interface.Interface):

    testing = schema.TextLine(title='testing')


@grok.implementer(IIncorrect)
class IncorrectAnnotation(grok.Annotation):
    grok.provides(IIncorrect)

    testing = grok.LazyAnnotationProperty(IIncorrect['testing'])
