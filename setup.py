#! /usr/bin/env python

"""Installer script."""
import setuptools

with open("README.md") as f:
    long_description = f.read()

setuptools.setup(
    name="cmccdb-tools",
    version="0.0.1",
    description="Tools for working with the CMCC Database",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Center-for-Mechanical-Control-of-Chem/cmccdb-tools",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "rdkit",
        "ipykernel",
        "torch",
        "opencv-python-headless",
        "pillow",
        "mccoygroup-mcutils>=1.4.0",
        "huggingface-hub",
        # "git+https://github.com/b3m2a1/MolScribe.git"
    ]
)
