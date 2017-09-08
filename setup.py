# coding=utf-8
from setuptools import setup, find_packages

setup(
    name="Gamma-Free ordering",
    version="0.1",
    author="Francois Brucker, Célia Châtel",
    author_email="francois.brucker@gmail.com, celia.chatel@lif.univ-mrs.fr",
    description="Tools for classification and data analysis",
    keywords="classification dissimilarity lattice",
    packages=find_packages(),
    long_description=open('README.txt').read(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: ",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    requires=['pillow', 'PIL', 'matplotlib'],
)
