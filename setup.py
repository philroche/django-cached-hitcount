import os
from setuptools import setup, find_packages
from cached_hitcount import __version__

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "django-cached-hitcount",
    version = __version__,
    author = "Philip Roche",
    author_email = "phil@philroche,net",
    description = ("Basic app that allows you to track the number of hits/views for a particular object."),
    license = "GPLv3",
    keywords = "django hit count",
    url = "https://github.com/philroche/django-cached-hitcount",
    packages=find_packages(),
    long_description=read('README.md'),
    install_requires=[
        'Django>=1.4,<1.6',
        'python-memcached-stats==0.1',#git+git://github.com/dlrust/python-memcached-stats.git
        'nexus',
        'django-jsonfield<0.9.4',
        'billiard',
        'python-dateutil',
        'gargoyle',
        'django-celery',
        'python-memcached',
        'south',
        'pyyaml',
        'ua-parser',
        'user-agents'
    ],
    dependency_links=[
        "https://github.com/dlrust/python-memcached-stats/tarball/master#egg=python-memcached-stats-0.1"
    ],
    include_package_data=True,
    zip_safe = False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Plugins',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
