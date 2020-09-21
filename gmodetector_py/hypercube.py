import ntpath # Should work on all platforms for finding basename from file path https://stackoverflow.com/questions/8384737/extract-file-name-from-path-no-matter-what-the-os-path-format/8384786
import numpy as np
import spectral as spy

from gmodetector_py import read_wavelengths
from gmodetector_py import find_desired_indices
from gmodetector_py import find_desired_channel
from gmodetector_py import slice_desired_channel
from gmodetector_py import CLS_to_image

class Hypercube:
    """A 3D hypercube containing spectra for each pixel

    :param file_path: A string indicating the path to the header file (in ENVI .hdr format) corresponding to the hyperspectral image file (in ENVI .raw format) to be read in
    :param min_desired_wavelength: A numeric value indicating a threshold BELOW which spectral data is excluded
    :param max_desired_wavelength: A numeric value indicating a threshold ABOVE which spectral data is excluded
    :param hypercube: 3D numpy array containing a spectra for each pixel
    :ivar wavelengths: contains the contents of ``wavelengths`` passed as init and subsequently trimmed to desired range

    """

    def plot(self, desired_wavelength, color, cap):
        """Plot a single channel selected from a hyperspectral image

        :param desired_wavelength: A string exactly equal to the wavelength of the band to be plotted
        :param color: A string equal to 'red', 'blue', or 'green' – the color that the extracted band will be plotted in
        :param cap: A numeric value of the spectral intensity value that will have maximum brightness in the plot. All with greater intensity will have the same level of brightness. Think of this as image exposure on a camera.
        """
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
        # spy.settings.envi_support_nonlowercase_params = True # This isn't working here... Warning still appears.
        self.hypercube = spy.io.envi.open(file_path).read_bands(bands=subset_indices[0],
        use_memmap = False)
        self.wavelengths = subset_wavelengths
        self.source = ntpath.basename(file_path)
