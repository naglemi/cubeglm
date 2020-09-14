from setuptools import setup
exec(open('gmodetector_py/version.py').read())

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
