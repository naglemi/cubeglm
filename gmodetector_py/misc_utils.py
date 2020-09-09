import numpy as np
import spectral.io.envi as envi

def read_wavelengths(file_path):
    """ Obtain a list of wavelengths for which hyperspectral data has been collected and stored in the input header file 
    
    :param file_path: A string indicating the path to an ENVI header (.hdr) file which contains wavelength information. This should be the same for all images taken with a given set of hyperspectral camera settings (specifically, the same wavelengths collected).
    ...
    return: A list of precise wavelengths
    
    
    """
    h = envi.read_envi_header(file_path)
    wavelengths = h['wavelength']
    return(wavelengths)
    
def find_desired_indices(wavelengths, min_desired_wavelength, max_desired_wavelength):
    """ Determine indices, in a wavelength list, for which wavelengths are within the desired range specified by the user
    
    :param wavelengths: A list of precise wavelengths, for which indices of interest will be determined.
    :param min_desired_wavelength: A numeric value indicating a threshold BELOW which spectral data is excluded
    :param max_desired_wavelength: A numeric value indicating a threshold ABOVE which spectral data is excluded
    ...
    return: A list of indices corresponding to desired wavelengths
    
    >>> find_desired_indices([1, 2, 3, 4, 5], 1.5, 4.5)
    [2, 3, 4]
    
    """
    wavelengths = np.asarray(wavelengths)
    # https://stackoverflow.com/questions/13869173/numpy-find-index-of-the-elements-within-range
    wavelength_indices_desired = np.where(np.logical_and(wavelengths.astype(float)>=min_desired_wavelength,
                                                          wavelengths.astype(float)<=max_desired_wavelength))
    return(wavelength_indices_desired)

import doctest
doctest.testmod()
