from distutils.core import setup, Extension

module = Extension('graphModule', sources=['cpyConverter.cpp', 'cycle/cycles.cpp'],
                   include_dirs=['cycle'], language='c++')

setup(name='PackageName',
      version='1.0',
      description='This is a package for graphModule',
      ext_modules=[module])
