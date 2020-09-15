from gmodetector_py import regress

class WeightArray:
    """A 3D array containing weights for each spectral component, obtained by regression of hybercube onto design matrix

    :param test_matrix: An object of class XMatrix (containing normalized spectra for each known component, and intercept if applicable)
    :param test_cube: An object of class Hypercube (containing spectra for each pixel)
    :ivar wavelengths: contains the contents of ``wavelengths`` passed from ``test_matrix`` and ``test_cube`` (must be same, or will yield error)
    :ivar weights: 3D array containing weight values

    """

    def __init__(self, test_matrix, test_cube):

        if test_matrix.wavelengths.astype(np.float).all() != test_cube.wavelengths.astype(np.float).all():
            raise Exception("Design matrix and hypercube do not have the same ``wavelengths`` attribute. Make sure to set the same ``min_desired_wavelength`` and ``max_desired_wavelength`` when creating both objects.")

        self.wavelengths = test_matrix.wavelengths
        self.weights = regress(test_matrix = test_matrix,
                               test_cube = test_cube)
