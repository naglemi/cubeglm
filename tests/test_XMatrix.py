from gmodetector_py import XMatrix
from gmodetector_py import read_wavelengths

def test_XMatrix():
    wavelengths = read_wavelengths('tests/example.hdr')
    test_matrix = XMatrix(fluorophore_ID_vector = ['DsRed', 'ZsYellow', 'Chl', 'Diffraction'],
                          spectral_library_path = 'spectral_library/',
                          intercept = 1,
                          wavelengths = wavelengths,
                          spectra_noise_threshold = 0.01,
                          min_desired_wavelength = 550,
                          max_desired_wavelength = 600)

    print("Shape of test matrix is... ")
    print(test_matrix.matrix.shape)
    assert len(test_matrix.wavelengths) == test_matrix.matrix.shape[0]
