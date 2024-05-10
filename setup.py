#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


if sys.argv[-1] == "publish":
    os.system("python setup.py sdist upload")
    sys.exit()


with open("README.md", "r", encoding="UTF-8") as f:
    readme = f.read()

with open("requirements.txt", "r", encoding="UTF-8") as f:
    requirements = f.read().splitlines()

setup(
    name="jobsubmit",
    version="0.1.0",
    description="An automated way to mutliplex commands for slurm job submission",
    long_description=readme,
    long_description_content_type="test/markdown",
    author="Joe Yesselman",
    author_email="jyesselm@unl.edu",
    url="https://github.com/jyesselm/jobsubmit",
    packages=[
        "jobsubmit",
    ],
    package_dir={"jobsubmit": "jobsubmit"},
    py_modules=["jobsubmit / jobsubmit"],
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords="jobsubmit",
    classifiers=[
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    entry_points={
        "console_scripts": [
            "jobsubmit = jobsubmit.cli:main",
        ]
    },
)
