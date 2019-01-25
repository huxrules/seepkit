from distutils.core import setup, Extension

module1 = Extension('astros', sources = ['astrosmodule.c'])

setup(name = 'PackageName', version = '1.0', description = 'demo packag', ext_modules = [module1])


