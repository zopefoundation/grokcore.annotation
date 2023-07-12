from setuptools import find_packages
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
    'zope.testrunner',
]


setup(
    name='grokcore.annotation',
    version='4.0',
    author='Grok Team',
    author_email='zope-dev@zope.dev',
    url='https://github.com/zopefoundation/grokcore.annotation',
    description='Grok-like configuration for Zope annotations',
    long_description=long_description,
    license='ZPL 2.1',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Framework :: Zope :: 3',
    ],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['grokcore'],
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.7',
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
