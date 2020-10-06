# Import classes
from gmodetector_py import XMatrix
from gmodetector_py import Hypercube
from gmodetector_py import WeightArray

from gmodetector_py import ImageChannel
from gmodetector_py import FalseColor

# Import the one function we need to use before calling classes
from gmodetector_py import read_wavelengths

# Need pandas to read weight array from hdf
import pandas as pd

# Need numpy for unit testing with allclose
import numpy as np

from PIL import Image

test_hypercube_path = "./tests/test_hypercube.hdr"

wavelengths = read_wavelengths(file_path = test_hypercube_path)

min_desired_wavelength = 500
max_desired_wavelength = 900

hypercube_de_novo = Hypercube(test_hypercube_path,
                              min_desired_wavelength = min_desired_wavelength,
                              max_desired_wavelength = max_desired_wavelength)

test_matrix = XMatrix(fluorophore_ID_vector = ['DsRed', 'ZsYellow', 'Chl', 'Diffraction'],
                      spectral_library_path = "./spectral_library/",
                      intercept = 1,
                      wavelengths = wavelengths,
                      spectra_noise_threshold = 0.01,
                      min_desired_wavelength = min_desired_wavelength,
                      max_desired_wavelength = max_desired_wavelength)

weight_array_de_novo = WeightArray(test_matrix=test_matrix,
                                   test_cube=hypercube_de_novo)

weight_array_de_novo.relu()

reloaded_weight_array = pd.read_hdf('./tests/test_array_weights.hdf',
                                    key = 'weights')

weight_array_de_novo._convert_3D_to_pseudotriplet()

print("Minimum value for both existing and de novo weight arrays for unit test:")
print(weight_array_de_novo.weights.min())
print(reloaded_weight_array.min())

np.testing.assert_allclose(reloaded_weight_array,
                           weight_array_de_novo._weights_pseudotriplet,
                           equal_nan=False)

reloaded_test_weights_img = Image.open("./tests/test_weights_FalseColor.png")

unit_test_weights_img = FalseColor([ImageChannel(weight_array = weight_array_de_novo,
                                                 desired_component_or_wavelength = 'DsRed',
                                                 color = 'green',
                                                 cap = 400),
                                    ImageChannel(weight_array = weight_array_de_novo,
                                                 desired_component_or_wavelength = 'Chl',
                                                 color = 'red',
                                                 cap = 200),
                                    ImageChannel(weight_array = weight_array_de_novo,
                                                 desired_component_or_wavelength = 'Diffraction',
                                                 color = 'blue',
                                                 cap = 50)])


unit_test_weights_img = np.array(unit_test_weights_img.image, dtype = 'uint8')
reloaded_test_weights_img = np.array(reloaded_test_weights_img, dtype = 'uint8')

np.testing.assert_allclose(unit_test_weights_img, reloaded_test_weights_img)