from setuptools import setup, find_packages

setup(
    name = "WENDI_dev",
    version = "0.13",
    packages = find_packages(),
    install_requires = ["numpy", "setuptools","future"],
    author = "NuGrid collaboration",
    author_email = "fherwig@uvic.ca")
