import webpage

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


requires = ['requests', 'lxml', ]

with open('README.md') as f:
    readme = f.read()
with open('RELEASES.md') as f:
    history = f.read()

setup(
    name='webpage',
    version=webpage.__version__,
    description='The collection of tools for making webpage archive',
    long_description=readme + '\n\n' + history,
    author='Andrey Usov',
    author_email='ownport@gmail.com',
    url='https://github.com/ownport/webpage',
    packages=['webpage'],
    package_dir={'webpage': 'webpage'},
    install_requires=requires,
    zip_safe=False,
    classifiers=( # from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ),
)