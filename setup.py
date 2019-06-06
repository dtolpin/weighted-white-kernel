"""Weighted white kernel for scikit-learn Gaussian process.
"""

from setuptools import setup, find_packages
from os import path
import dtolpin.gaussian_process

# Get the long description from the README file
here = path.abspath(path.dirname(__file__))
with open(path.join(here, "README.md")) as f:
    long_description = f.read()


setup(
    name="weighted-white-kernel",
    version=dtolpin.gaussian_process.__version__,

    description="Weighted white kernel for Gaussian process",
    long_description=long_description,
    url="https://github.com/dtolpin/weighted-white-kernel",

    packages=find_packages(exclude=["doc"]),

    # source code layout
    namespace_packages=["dtolpin"],

    # author and license
    author="David Tolpin",
    author_email="david.tolpin@gmail.com",
    license="MIT",

    # dependencies, a list of rules
    install_requires=["scikit-learn"],
    # add links to repositories if modules are not on pypi
    dependency_links=[
    ],

    #  PyTest integration
    setup_requires=["pytest-runner"],
    tests_require=["pytest"]
)
