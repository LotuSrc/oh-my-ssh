# -*- encoding: UTF-8 -*-
from setuptools import setup, find_packages
import os

VERSION = '0.0.2'

setup(name='oms',
      version=VERSION,
      description='',
      long_description='',
      classifiers=[],
      keywords='',
      author='LotuSrc',
      author_email='451415738@qq.com',
      url='',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          'bullet==2.2.0',
          'pexpect',
          'fire'
      ],
      entry_points={
          'console_scripts': [
              'oms = main:main'
          ]
      },
      )
