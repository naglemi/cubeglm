from gmodetector_py import regress
import numpy as np
import pandas as pd
from gmodetector_py import find_desired_channel
from gmodetector_py import slice_desired_channel
from gmodetector_py import CLS_to_image
import h5py

class WeightArray:
    """A 3D array containing weights for each spectral component, obtained by regression of hybercube onto design matrix

    :param test_matrix: An object of class XMatrix (containing normalized spectra for each known component, and intercept if applicable)
    :param test_cube: An object of class Hypercube (containing spectra for each pixel)
    :ivar wavelengths: contains the contents of ``wavelengths`` passed from ``test_matrix`` and ``test_cube`` (must be same, or will yield error)
    :ivar weights: 3D array containing weight values
    :ivar components: A list of spectral components (including intercept if applicable) – contains the contents of ``fluorophore_ID_vector`` passed through``test_matrix.components``

    """

    def _convert_3D_to_pseudotriplet(self, index_starting_at_one = True):
        I, J = np.indices(self.weights.shape[0:2])
        if index_starting_at_one == True:
            I = I + 1
            J = J + 1
        for i in range(0, len(self.components)):
            if i == 0:
                # Thank you 英文原文 for explaining conversion of matrix to triplet form with numpy http://www.javaear.com/question/30478758.html
                array_in_coordinate = pd.DataFrame(np.column_stack(ar.ravel() for ar in (I, J, self.weights[:, :, i])),
                columns = ['rows', 'cols', self.components[i]])
            if i > 0:
                matrix_slice_in_triplet = np.column_stack(ar.ravel() for ar in (I, J, self.weights[:, :, i]))
                array_in_coordinate = pd.concat([array_in_coordinate,
                pd.DataFrame(matrix_slice_in_triplet[:, 2], columns = [self.components[i]])], axis = 1)
                #print('array shape is...')
                #print(array_in_coordinate.shape)
                #print('head row of array is...')
                #print(array_in_coordinate[:1])
        # columns = ['rows', 'cols'] + self.components)
        self._weights_pseudotriplet = array_in_coordinate

    def save(self, path, index_starting_at_one = True, format = "hdf",
    output_dir = "./"):

        self._convert_3D_to_pseudotriplet(index_starting_at_one = index_starting_at_one)

        if format == "csv":
            # I suspect the conversion from np.ndarray to pd.DataFrame is superfluous
            #array_in_coordinate = pd.DataFrame(array_in_coordinate)
            for i in range(0, len(self.components)):
                output_path = output_dir + path + '_' + self.components[i] + '_weights.' + format
                self._weights_pseudotriplet.to_csv(output_path, index = False)

        if format == "hdf":
            output_path = output_dir + path + '_weights.' + format
            for i in range(0, len(self.components)):
                print('Saving layer ' + self.components[i] + ' to ' + output_path + ' with key ' + self.components[i])
                self._weights_pseudotriplet.to_hdf(output_path, key = self.components[i], format = 'table')

    def plot(self, desired_component, color, cap):
        """Plot a single channel selected from a weight array produced by regression

                :param desired_component: A string matching the ID of the component to be plotted (e.g. 'GFP')
                :param color: A string equal to 'red', 'blue', or 'green' – the color that the extracted band will be plotted in
                :param cap: A numeric value of the spectral intensity value that will have maximum brightness in the plot. All with greater intensity will have the same level of brightness. Think of this as image exposure on a camera.

        """
        index_of_desired_channel = find_desired_channel(self.components,
                                                        desired_component)
        Weights_desired_peak_channel = slice_desired_channel(self.weights,
                                                             index_of_desired_channel)
        plot_out = CLS_to_image(CLS_matrix = Weights_desired_peak_channel,
                                cap = cap, mode = 'opaque',
                                match_size=False, color=color)
        return(plot_out)

    def __init__(self, test_matrix, test_cube):

        if test_matrix.wavelengths.astype(np.float).all() != test_cube.wavelengths.astype(np.float).all():
            raise Exception("Design matrix and hypercube do not have the same ``wavelengths`` attribute. Make sure to set the same ``min_desired_wavelength`` and ``max_desired_wavelength`` when creating both objects.")

        self.wavelengths = test_matrix.wavelengths
        self.weights = regress(test_matrix = test_matrix,
                               test_cube = test_cube)
        self.components = test_matrix.components
        self.source = test_cube.source
