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
    description = ("Django hit counter application that tracks the number of hits/views for chosen objects"),
    license = "GPLv3",
    keywords = "django health check monitoring",
    url = "https://github.com/KristianOellegaard/django-health-check",
    packages=find_packages(),
    long_description=read('README.md'),
    install_requires=[
        'Django>=1.4',
        'python-memcached-stats',#git+git://github.com/dlrust/python-memcached-stats.git
        'gargoyle',
        'django-celery',
        'python-memcached',
        'south'
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
