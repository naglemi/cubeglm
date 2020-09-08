from gmodetector_py import read_wavelengths

# Test normal case, in which we read a certain number of wavelengths, in this case from the included example.hdr
def test_read_wavelengths():
    wavelengths = read_wavelengths('tests/example.hdr')
    assert len(wavelengths) == 318