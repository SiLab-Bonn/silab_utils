#!/usr/bin/env python

from setuptools import setup, Extension, find_packages
from distutils.command.build_ext import build_ext
from Cython.Build import cythonize
import numpy as np
import os

copt = {'msvc': ['-Isilab_utils/cpp/external', '/EHsc']}  # Set additional include path and EHsc exception handling for VS
lopt = {}


class build_ext_opt(build_ext):
    def initialize_options(self):
        build_ext.initialize_options(self)
        self.compiler = 'msvc' if os.name == 'nt' else None  # in Anaconda the libpython package includes the MinGW import libraries and a file (Lib/distutils/distutils.cfg) which sets the default compiler to mingw32. Alternatively try conda remove libpython.

    def build_extensions(self):
        c = self.compiler.compiler_type
        if c in copt:
            for e in self.extensions:
                e.extra_compile_args = copt[c]
        if c in lopt:
            for e in self.extensions:
                e.extra_link_args = lopt[c]
        build_ext.build_extensions(self)


extensions = [
    Extension('silab_utils.compiled_analysis_functions', ['silab_utils/cpp/compiled_analysis_functions.pyx'])   # Fast analysis functions written in C++
]


f = open('VERSION', 'r')
version = f.readline().strip()
f.close()

author = 'David-Leon Pohl'
author_email = 'pohl@physik.uni-bonn.de'

# Requirements from requirements.txt
with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

setup(
    name='silab_utils',
    version=version,
    description='silab_utils - Often used and usefull data analysis utils for the Silicon Laboratory Bonn are collected in this package',
    url='https://github.com/SiLab-Bonn/silab_utils',
    license='MIT License',
    long_description='This package is a collecting tank for analysis functions that are often needed. It provides e.g. fast functions where python + numpy is still too slow or simple to use function for special use cases.',
    author=author,
    maintainer=author,
    author_email=author_email,
    maintainer_email=author_email,
    install_requires=install_requires,
    packages=find_packages(),  # exclude=['*.tests', '*.test']),
    include_package_data=True,  # accept all data files and directories matched by MANIFEST.in or found in source control
    package_data={'': ['README.*', 'VERSION'], 'docs': ['*'], 'examples': ['*']},
    ext_modules=cythonize(extensions),
    include_dirs=[np.get_include()],
    cmdclass={'build_ext': build_ext_opt},
    platforms='any'
)
