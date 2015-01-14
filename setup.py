#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(name='pybitcoin',
      version='0.5',
      description='Python Bitcoin Tools',
      author='sillygod',
      author_email='sillygod@livemail.tw',
      url='https://github.com/sillygod/pybitcointool-plus',
      install_requires='six==1.8.0',
      packages=['bitcoin'],
      scripts=['pybtctool'],
      include_package_data=True,
      data_files=[("", ["LICENSE"])],
      )
