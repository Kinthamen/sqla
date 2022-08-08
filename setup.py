from os.path import splitext
from os.path import basename
from setuptools import setup
from setuptools import find_packages
from glob import glob

with open('README.md', 'r') as f:
    long_description = f.read()

with open('LICENSE', 'r') as f:
    license = f.read()

setup(
    name='sqla',
    version = '0.0.1',
    description = 'A small set of inheritable bases for SQLAlchemy to get any project started quickly',
    url='https://github.com/Kinthamen/sqla.git',
    author='Abinadi Cordova',
    author_email='abinadi.cordova1@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    long_description=long_description,
    long_description_content_type='text/markdown',
    license=license,
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires = [
        'SQLAlchemy>=1.4.31',
    ]
)