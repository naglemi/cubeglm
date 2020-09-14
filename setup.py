from setuptools import setup
from ._version import __version__

setup(name='gmodetector_py',
      version=__version__,
      description='Quantification of fluorescent proteins in hyperspectral images by regression',
      author='Michael Nagle',
      author_email='michael.nagle@oregonstate.edu',
      packages=['gmodetector_py'],
      install_requires=['numpy',
                        'pandas',
                        'spectral',
                        'rpy2',
                        'matplotlib'])
