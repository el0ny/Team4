from distutils.core import setup, Extension

module = Extension('graphModule',
                   sources=['cpyConverter.cpp', 'cycle/cycles.cpp', 'fragm_alwdFaces/func.cpp', 'alpha_path/alpha_path.cpp'],
                   include_dirs=['cycle', 'fragm_alwdFaces', 'alpha_path'], language='c++')

setup(name='PackageName',
      version='1.0',
      description='This is a package for graphModule',
      ext_modules=[module])
