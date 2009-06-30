from setuptools import setup, find_packages
import os

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description = (
    read('README.txt')
    + '\n' +
    read('CHANGES.txt')
    )

setup(
    name='grokcore.annotation',
    version='1.0.1',
    author='Grok Team',
    author_email='grok-dev@zope.org',
    url='http://grok.zope.org',
    download_url='http://pypi.python.org/pypi/grokcore.annotation',
    description='Grok-like configuration for Zope annotations',
    long_description=long_description,
    license='ZPL',
    classifiers=['Environment :: Web Environment',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: Zope Public License',
                 'Programming Language :: Python',
                 'Framework :: Zope3',
                 ],

    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['grokcore'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['setuptools',
                      'martian',
                      'zope.component',
                      'zope.interface',
                      'zope.annotation',
                      'grokcore.component',
                      'ZODB3',
                      'zope.app.container',
                      'zope.configuration',
                      'zope.testing',
                      ],
    )
