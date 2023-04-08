# python3 setup.py build_ext --inplace
from distutils.core import setup, Extension
from Cython.Build import cythonize
import numpy

package = Extension('core', ['modules/strategies/zigzag/core.pyx'], include_dirs=[numpy.get_include()])
setup(ext_modules=cythonize([package]))