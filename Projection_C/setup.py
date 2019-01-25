from distutils.core import setup, Extension

module1 = Extension('HLProjector', sources = ['WCDProjectorModule.c'])

setup(name = 'PackageName', version = '1.0', description = 'demo packag', ext_modules = [module1])


