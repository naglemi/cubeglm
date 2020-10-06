# Import classes
from gmodetector_py import Hypercube
from gmodetector_py import ImageChannel
from gmodetector_py import FalseColor
from PIL import Image

# Import the one function we need to use before calling classes
from gmodetector_py import read_wavelengths

# Need numpy for unit testing with allclose
import numpy as np

test_hypercube_path = "./tests/test_hypercube.hdr"

wavelengths = read_wavelengths(file_path = test_hypercube_path)

hypercube_de_novo = Hypercube(test_hypercube_path,
                              min_desired_wavelength = 500,
                              max_desired_wavelength = 900)

hypercube_img_de_novo = FalseColor([ImageChannel(hypercube = hypercube_de_novo,
                                                 desired_component_or_wavelength = '582.6952',
                                                 color = 'green',
                                                 cap = 1500),
                                    ImageChannel(hypercube = hypercube_de_novo,
                                                 desired_component_or_wavelength = '672.6443',
                                                 color = 'red',
                                                 cap = 800),
                                    ImageChannel(hypercube = hypercube_de_novo,
                                                 desired_component_or_wavelength = '501.2859',
                                                 color = 'blue',
                                                 cap = 650)])

reloaded_test_hypercube_img = Image.open("./tests/test_hypercube.png")

# Need to convert images to numpy arrays so we can use np.allclose() for unit test
unit_test_hypercube_img = np.array(hypercube_img_de_novo.image, dtype = 'uint8')
reloaded_test_hypercube_img = np.array(reloaded_test_hypercube_img, dtype = 'uint8')

np.testing.assert_allclose(unit_test_hypercube_img, reloaded_test_hypercube_img)