from setuptools import setup


def read(name):
    """Read a file."""
    with open(name) as f:
        return f.read()


long_description = (
    read('README.rst')
    + '\n' +
    read('CHANGES.rst')
)

tests_require = [
    'zope.configuration',
    'zope.schema',
    'zope.testing > 4.6',
    'zope.testrunner >= 6.4',
]


setup(
    name='grokcore.annotation',
    version='5.1.dev0',
    author='Grok Team',
    author_email='zope-dev@zope.dev',
    url='https://github.com/zopefoundation/grokcore.annotation',
    description='Grok-like configuration for Zope annotations',
    long_description=long_description,
    license='ZPL-2.1',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Framework :: Zope :: 3',
    ],
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.9',
    install_requires=[
        'grokcore.component >= 2.5',
        'martian',
        'setuptools',
        'zope.annotation',
        'zope.cachedescriptors',
        'zope.component',
        'zope.container',
        'zope.event',
        'zope.interface',
        'zope.location',
        'zope.schema',
    ],
    extras_require={'test': tests_require},
)
