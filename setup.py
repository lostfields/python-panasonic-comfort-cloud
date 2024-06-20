""" Setup for python-panasonic-comfort-cloud """

from setuptools import setup
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pcomfortcloud',
    version=os.getenv('VERSION', default='0.0.1'),
    description='Read and change status of Panasonic Comfort Cloud devices',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='http://github.com/lostfields/python-panasonic-comfort-cloud',
    author='Lostfields',
    license='MIT',
    classifiers=[
        'Topic :: Home Automation',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='home automation panasonic climate',
    install_requires=[
        'requests>=2.20.0',
        'beautifulsoup4>=4.12.3',
        'bs4>=0.0.2',
        'certifi>=2024.6.2',
        'charset-normalizer>=3.3.2',
        'idna>=3.7',
        'requests>=2.32.3',
        'soupsieve>=2.5',
        'urllib3>=2.2.2',
    ],
    packages=['pcomfortcloud'],
    zip_safe=False,
)
