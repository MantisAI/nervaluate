
import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

# Load data from the__versions__.py module. Change version, etc in
# that module, and it will be automatically populated here.

about = {}
version_path = os.path.join(here, 'nervaluate', '__version__.py')
with open(version_path, 'r') as f:
    exec(f.read(), about)

setup(
    name=about["__name__"],
    version=about["__version__"],
    description=about["__description__"],
    url=about["__url__"],
    author=about["__author__"],
    author_email=about["__author_email__"],
    license=["__license__"],
    packages=["nervaluate"],
    install_requires=[
        "scikit-learn==0.21.2",
        "sklearn-crfsuite==0.3.6"
    ],
    tests_require=["pytest"],
    include_package_data=True,
    zip_safe=True,
)
