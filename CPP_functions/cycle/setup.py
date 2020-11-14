from distutils.core import setup, Extension

module = Extension('cycleModule', sources=['cpyConverter.cpp', 'cycles.cpp'], include_dirs=['.'], language='c++')

setup(name='PackageName',
      version='1.0',
      description='This is a package for cycleModule',
      ext_modules=[module])
