from setuptools import setup, find_packages
import codecs
import os

from ramby import __version__, __author__

with open("requirements.txt", 'r') as fp:
    install_requires = [x.strip() for x in fp.readlines()]

with open("README.md", "r") as fp:
    readmefile = fp.read()

# Setting up
setup(
    name="ramby",
    version=__version__,
    author=__author__,
    author_email="kennethgabriel78@gmail.com",
    description='Ramby is a simple way to setup a webscraper',
    long_description=readmefile,
    long_description_content_type="text/markdown",
    url="https://github.com/keosariel/ramby",
    packages=find_packages(),
    license="MIT",
    install_requires=install_requires,
    keywords=['python', 'crawler', 'scraper', 'bs4', 'beautifulsoup'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)