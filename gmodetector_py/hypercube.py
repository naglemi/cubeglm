class Hypercube:
    """A 3D hypercube containing spectra for each pixel
    
    :param file_path: A string indicating the path to the header file (in ENVI .hdr format) corresponding to the hyperspectral image file (in ENVI .raw format) to be read in
    :param min_desired_wavelength: A numeric value indicating a threshold BELOW which spectral data is excluded
    :param max_desired_wavelength: A numeric value indicating a threshold ABOVE which spectral data is excluded
    :param hypercube: 3D numpy array containing a spectra for each pixel
    :ivar wavelengths: contains the contents of ``wavelengths`` passed as init and subsequently trimmed to desired range
    
    """
    
    def __init__(self, file_path, min_desired_wavelength, max_desired_wavelength):
        # Define attribute with contents of the value param
        
        all_wavelengths = read_wavelengths(file_path)
        subset_indices = find_desired_indices(all_wavelengths, min_desired_wavelength, max_desired_wavelength)
        subset_wavelengths = np.array(all_wavelengths)[subset_indices[0]]
        
        self.hypercube = test_cube.hypercube.read_bands(bands=subset_indices[0])
        self.wavelengths = subset_wavelengths