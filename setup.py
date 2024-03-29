import os

from setuptools import setup


def read(filename):
    path = os.path.join(os.path.dirname(__file__), filename)
    with open(path, 'r') as f:
        return f.read()


setup(
    name="shibari",
    version="0.0.2",
    description="Bind functions to run only once inside a desired scope.",
    long_description=read('README.rst'),
    author="Joshua Fehler",
    author_email="jsfehler@gmail.com",
    license="MIT",
    url="https://github.com/jsfehler/shibari",
    py_modules=['shibari'],
    classifiers=(
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
    ),
)
