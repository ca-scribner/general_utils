import os
import sys

from setuptools import setup, find_packages

sys.path.append(os.path.abspath('./general_utils'))
from version import VERSION

setup(name='general_utils',
      version=VERSION,
      description='Collection of generic utilities',
      author='Andrew Scribner',
      install_requires=[
        'matplotlib>=2.1.2',
        'numpy>=1.14.0',
        'pandas>=0.22.0',
        'scikit-learn>=0.19.1',
      ],
      packages=find_packages(),
      python_requires='>3.6',
      )