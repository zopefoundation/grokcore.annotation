
This package provides a support to simplify the use of annotations in
Zope.

.. contents::


Setting up ``grokcore.annotation``
==================================

This package is essentially set up like the `grokcore.component`_
package, please refer to its documentation for details.  The only
additional ZCML line you will need is::

  <include package="grokcore.annotation" />

Put this somewhere near the top of your root ZCML file but below the
line where you include ``grokcore.component``'s configuration.


Example
=======

Here a simple example of use of an annotation::

    import grokcore.annotation
    from zope import interface

    # Create a model and an interface you want to adapt it to
    # and an annotation class to implement the persistent adapter.
    class Mammoth(grokcore.annotation.Model):
        pass

    class ISerialBrand(interface.Interface):
        unique = interface.Attribute("Brands")

    class Branding(grokcore.annotation.Annotation):
        grokcore.annotation.implements(ISerialBrand)
        unique = 0

    # Grok the above code, then create some mammoths
    manfred = Mammoth()
    mumbles = Mammoth()

    # creating Annotations work just like Adapters
    livestock1 = ISerialBrand(manfred)
    livestock2 = ISerialBrand(mumbles)

    # except you can store data in them, this data will transparently persist
    # in the database for as long as the object exists
    livestock1.unique = 101
    livestock2.unique = 102

    # attributes not listed in the interface will also be persisted
    # on the annotation
    livestock2.foo = "something"



API Overview
============

Base classes
------------

``Annotation``
   Base class for an Annotation. Inherits from the
   persistent.Persistent class.

``Model``
   Base class for a Model on which you want to use an annotation.


In addition, the ``grokcore.annotation`` package exposes the
`grokcore.component`_ API.

.. _grokcore.component: http://pypi.python.org/pypi/grokcore.component


