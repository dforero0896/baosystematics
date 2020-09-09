from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize("fast_line_count.pyx", language_level=3)
)

