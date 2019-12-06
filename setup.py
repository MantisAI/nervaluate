
import os
# read the contents of your README file
from os import path

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

# Load data from the__versions__.py module. Change version, etc in
# that module, and it will be automatically populated here.

about = {}
version_path = os.path.join(here, 'nervaluate', '__version__.py')
with open(version_path, 'r') as f:
    exec(f.read(), about)

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name=about["__name__"],
    version=about["__version__"],
    description=about["__description__"],
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=about["__url__"],
    author=about["__author__"],
    author_email=about["__author_email__"],
    license=["__license__"],
    packages=["nervaluate"],
    install_requires=[],
    tests_require=["pytest"],
    include_package_data=True,
    zip_safe=True,
)
