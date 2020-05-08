import setuptools
from setuptools import find_packages, setup, Command

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="trajprocess", # Replace with your own username
    version="0.0.1",
    author="Aoyong",
    author_email="aoyong.lee@outlook.com",
    description="Process the trajecotry data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages= find_packages(exclude = ('tests')),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)