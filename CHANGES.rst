Changes
=======

3.1 (2020-10-27)
----------------

- Add support for `FieldUpdatedEvent` in `LazyPropertyAnnotation` to
  mirror the behavior of zope.schema.


3.0.1 (2018-01-17)
------------------

- Replace the use of `grok.implements()` with the `@grok.implementer()`
  directive throughout.

3.0.0 (2018-01-12)
------------------

- Rearrange tests such that Travis CI can pick up all functional tests too.

1.6 (2017-05-30)
----------------

- Add LazyAnnotation and LazyAnnotationProperty.

- Drop support of Python 2.6 and claim support for Python 3.4, 3.5, 3.6 and PyPy.

1.5.1 (2016-01-29)
------------------

- Update tests.

1.5 (2014-10-20)
----------------

- Updating MANIFEST.in, fixing a brown paper bag release.

1.4 (2014-10-17)
----------------

- Add ``queryAnnotation()`` to return an annotation. Return None if it
  doesn't exists. This helper will never do any write operation in the
  database.

- Add ``deleteAnnotation()`` to delete an annotation (if it exists).

1.3 (2012-05-01)
----------------

- Use ``provideAdapter()`` from grokcore.component.util.

- Made package comply to zope.org repository policy.

1.2 (2009-12-13)
----------------

* Use zope.container instead of zope.app.container.

1.1 (2009-09-18)
----------------

* The annotation object become really a contained object to be aware
  of its context, and name.

* Use 1.0b1 versions.cfg in Grok's release info instead of a local
  copy; a local copy for all grokcore packages is just too hard to
  maintain.

1.0.1 (2009-06-30)
------------------

* Reupload to pypi with a correct version of Python which doesn't
  have a distutils bug.

1.0 (2009-06-29)
----------------

* Created ``grokcore.Annotation`` by factoring annotation components,
  grokkers and directives out of Grok.
