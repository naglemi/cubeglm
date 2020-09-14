from setuptools import setup

setup(name='gmodetector_py',
      version='0.0.1',
      description='Quantification of fluorescent proteins in hyperspectral images by regression',
      author='Michael Nagle',
      author_email='michael.nagle@oregonstate.edu',
      packages=['gmodetector_py'],
      install_requires=['numpy',
                        'pandas',
                        'spectral',
                        'rpy2',
                        'matplotlib'])