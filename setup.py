from setuptools import setup, find_packages

from util.version import VERSION

"""
Setup module for Fuse
"""

setup(
    name='Fuse-Con',
    description='Fuse is a content aggregation CLI tool written in Python',
    version=VERSION,
    license='MIT',
    author="Eliran Turgeman",
    author_email='email@example.com',
    python_requires=">=3.7",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/Eliran-Turgeman/Fuse',
    keywords='Fuse aggregation',
    install_requires=[
        'feedparser==6.0.8',
        'praw==6.4.0',
        'colorama==0.4.4',
        'pytest',
        'pytest-mock==3.7.0',
        'requests'
    ],

)
