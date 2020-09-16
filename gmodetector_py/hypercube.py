import numpy as np
import spectral.io.envi as envi
from gmodetector_py import read_wavelengths
from gmodetector_py import find_desired_indices

class Hypercube:
    """A 3D hypercube containing spectra for each pixel

    :param file_path: A string indicating the path to the header file (in ENVI .hdr format) corresponding to the hyperspectral image file (in ENVI .raw format) to be read in
    :param min_desired_wavelength: A numeric value indicating a threshold BELOW which spectral data is excluded
    :param max_desired_wavelength: A numeric value indicating a threshold ABOVE which spectral data is excluded
    :param hypercube: 3D numpy array containing a spectra for each pixel
    :ivar wavelengths: contains the contents of ``wavelengths`` passed as init and subsequently trimmed to desired range

    """

    def plot(self, desired_wavelength, color, cap):
        index_of_desired_channel = find_desired_channel(self.wavelengths,
                                                        desired_wavelength)
        Hypercube_desired_peak_channel = slice_desired_channel(self.hypercube,
                                                               index_of_desired_channel)
        plot_out = CLS_to_image(CLS_matrix = Hypercube_desired_peak_channel,
                            cap = cap, mode = 'opaque',
                            match_size=False, color=color)
        return(plot_out)

    def __init__(self, file_path, min_desired_wavelength, max_desired_wavelength):
        # Define attribute with contents of the value param

        all_wavelengths = read_wavelengths(file_path)
        subset_indices = find_desired_indices(all_wavelengths, min_desired_wavelength, max_desired_wavelength)
        subset_wavelengths = np.array(all_wavelengths)[subset_indices[0]]

        self.hypercube = envi.open(file_path).read_bands(bands=subset_indices[0])
        self.wavelengths = subset_wavelengths
