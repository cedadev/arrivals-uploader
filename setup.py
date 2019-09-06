""" A setuptools based setup module. """

__author__ = "Sam Pepler"
__date__ = "2017-07-28"
__copyright__ = "Copyright 2019 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level directory"


from setuptools import setup, find_packages


with open("README.md") as readme_file:
    long_description = readme_file.read()


setup(
    name = "arrivals_uploader",
    version = "1.0.0",
    description = "Django application which provides upload functionality.",
    author = "Sam Pepler",
    author_email = "sam.pepler@stfc.ac.uk",
    maintainer = "William Tucker",
    maintainer_email = "william.tucker@stfc.ac.uk",
    url = "https://github.com/cedadev/arrivals-uploader",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    license = "BSD - See LICENSE file for details",
    include_package_data=True,
    packages = find_packages(),
    install_requires = [
        "django",
        "django-sizefield",
        "django-extensions",
        "django-multiselectfield",
        "python-dateutil",
        "pytz",
        "Unidecode",
        "PyYAML",
        "pexpect",
    ],
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    zip_safe = False,
)
