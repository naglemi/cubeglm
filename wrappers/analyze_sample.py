# Import classes
# Check version
from gmodetector_py import version
print('Running GMOdetector version ' + version.__version__)

from gmodetector_py import XMatrix
from gmodetector_py import Hypercube
from gmodetector_py import WeightArray
from gmodetector_py import ImageChannel
from gmodetector_py import FalseColor

# Import the one function we need to use before calling classes
from gmodetector_py import read_wavelengths

# The following are needed for this specific wrapper script only
import warnings
import argparse

import os # needed for basename

parser = argparse.ArgumentParser(description="""This script provides a wrapper
for analyzing a sample by a start-to-finish hyperspectral regression workflow,
including plotting and saving of weight arrays for each spectral component.""")

parser.add_argument('file_path', type = string, nargs = 1,
                    help = """Relative filepath to the metadata file (.hdr) for
                    a sample to be analyzed""")
parser.add_argument('--fluorophores', type=string, nargs = '+',
                    dest = 'fluorophore_ID_vector',
                    help = 'A list of spectral components in the spectral library')
parser.add_argument('--min_desired_wavelength', type = numeric, nargs = 1,
                    help = """A numeric value indicating a threshold BELOW
                    which spectral data is excluded""")
parser.add_argument('--max_desired_wavelength', type = numeric, nargs = 1,
                    help = """A numeric value indicating a threshold ABOVE
                    which spectral data is excluded""")
parser.add_argument('--green_channel', type = string, nargs = 1,
                    help = """A string matching the ID of the spectral component
                    for which weights will be plotted (e.g. 'GFP')
                    with GREEN false color""")
parser.add_argument('--red_channel', type = string, nargs = 1,
                    help = """A string matching the ID of the spectral component
                    for which weights will be plotted (e.g. 'GFP')
                    with RED false color""")
parser.add_argument('--blue_channel', type = string, nargs = 1,
                    help = """A string matching the ID of the spectral component
                    for which weights will be plotted (e.g. 'GFP')
                    with BLUE false color""")
parser.add_argument('--green_cap', type = string, nargs = 1,
                    help = """A numeric value of the spectral intensity value
                    of the GREEN channel (specified by `--green-channel` that
                    will have maximum brightness in the plot.
                    All with greater intensity will have the same level of
                    brightness. Think of this as image exposure on a camera.""")
parser.add_argument('--red_cap', type = string, nargs = 1,
                    help = """A numeric value of the spectral intensity value
                    of the RED channel (specified by `--red-channel` that
                    will have maximum brightness in the plot.
                    All with greater intensity will have the same level of
                    brightness. Think of this as image exposure on a camera.""")
parser.add_argument('--blue_cap', type = string, nargs = 1,
                    help = """A numeric value of the spectral intensity value
                    of the BLUE channel (specified by `--blue-channel` that
                    will have maximum brightness in the plot.
                    All with greater intensity will have the same level of
                    brightness. Think of this as image exposure on a camera.""")
parser.add_argument('--weight_format', type = string, nargs = 1, default = 'hdf',
                    help = """The format in which the weight array will be saved;
                    Currently supported are `csv` and `hdf` (h5py) formats.""")
parser.add_argument('--plot', type = bool, nargs = 1, default = False,
                    help = """Boolean (True or False) indicating whether to
                    create false color plots of spectral components. Note that
                    at the time of writing documentation, there is no support
                    for producing false color plots of hypercubes prior to
                    regression in `analyze_sample`; this must be done
                    independently for a given sample as described in
                    documentation for the `Hypercube` class.""")
parser.add_argument('--spectral_library_path', type = string, nargs = 1,
                    default = './spectral_library/',
                    help = """Path to a folder in which all spectra listed by the
                    `--fluorophores` flag are included in the appropriate format
                    (See documentation for `XMatrix` object, or examples for
                    format details""")
parser.add_argument('--intercept', type = numeric, nargs = 1, default = 1,
                    help = """If 0, no intercept is added to X. If 1, a vector
                    of 1's equal to # spectra is prepended to X during regression.
                    This value should be set to 1 if there is any significant
                    level of background noise in hypercubes (Y) being
                    analyzed""")
parser.add_argument('--spectra_noise_threshold', type = numeric, nargs = 1,
                    default = 0.01,
                    help = """A float indicating a threshold below which fitted
                    spectra values are set to zero (default value is 0.01,
                    an approximate noise threshold of the Andor hyperspectral
                    camera with settings used by Strauss Lab at the time of
                    writing documentation), passed to read_fit_spectra)""")
parser.add_argument('--normalize', type = bool, nargs = 1, default = False,
                    help = """Boolean (True or False) indicating whether
                    to normalize the experimental sample against
                    a user-provided chroma standard""")
parser.add_argument('--rescale', type = bool, nargs = 1, default = True,
                    help = """Boolean (True or False) indicating whether to
                    rescale the experimental sample's hypercube after
                    normalization to bring the normalized spectra
                    to approximately the sample mean intensity as prior to
                    normalization""")
parser.add_argument('--chroma_width', type = numeric, nargs = 1, default = 10,
                    help = """The number of pixels to be extracted from the
                    center of the chroma standard hypercube, over which the
                    mean for each row will be taken and used for normalizing
                    fluctuations in laser and/or signal intensity""")
parser.add_argument('--chroma_path', nargs = 1, default = None,
                    help = """The filepath to a chroma standard against which
                    experimental samples will be normalized. Please note the
                    `--normalize` flag must be set to `True` if normalizing.""")
parser.add_argument('--relu' , type = bool, nargs = 1, default = True,
                    help = """Whether to replace values below zero in the weight
                    array with zero before making plots; needed for scales to be
                    consistent across images with the same color/cap settings""")

args = parser.parse_args()
print args.accumulate(args.integers)

def analyze_sample(file_path,fluorophore_ID_vector,
min_desired_wavelength, max_desired_wavelength,
green_channel, red_channel, blue_channel,
green_cap, red_cap, blue_cap, weight_format = 'hdf', plot = True,
spectral_library_path = './spectral_library/', intercept = 1,
spectra_noise_threshold = 0.01, normalize = False, rescale = True,
chroma_width = 10, chroma_hypercube = None, chroma_path = None,
relu_before_plot = True):
    """This function provides a wrapper for analyzing a sample by a
    start-to-finish hyperspectral regression workflow, including plotting
    and saving of weight arrays for each spectral component. At the time of
    writing documentation, this function is intended to be accessed from the
    command line. To see further documentation, including for each argument
    passed from the command line to this function, run
    `analyze_sample.py --help` from the command line.

    All arguments to this function are accesible from command line at the time
    of documentation except for `chroma_hypercube`, an preloaded alternative to
    `chroma_path` that allows for a common chroma standard to be stored in shared
    memory when parallelization in Python (rather than just command line) is
    used."""

    if chroma_hypercube is not None and chroma_path is not None:
        raise Exception("""Chroma standard was submitted both as a pre-loaded
                        hypercube (`chroma_hypercube`) and
                        a filepath (`chroma_path`). Please choose one.""")

    if normalize == True and (chroma_path is None and chroma_hypercube is None):
        raise Exception("""Normalization is on (via `normalize` option) but
                        no chroma standard has been provided for normalization
                        (via either `chroma_path` or `chroma_hypercube`).""")

    if normalize == False and (chroma_path is not None or chroma_hypercube is not None):
        raise Exception("""Normalization is off (via `normalize` option) but
                        a chroma standard has been provided. Set `normalize` to
                        True if you wish to perform normalization of the sample.""")

    if chroma_hypercube is None and chroma_path is None:
        warnings.warn('Sample is not being normalized with a chroma standard.')

    if chroma_hypercube is None and chroma_path is not None:
        chroma_hypercube = Hypercube(file_path,
        min_desired_wavelength = min_desired_wavelength,
        max_desired_wavelength = max_desired_wavelength)

    if normalize == True:
        normalize(self, chroma_hypercube, chroma_width, rescale = rescale)

    wavelengths = read_wavelengths(file_path = file_path)

    test_matrix = XMatrix(fluorophore_ID_vector = fluorophore_ID_vector,
                      spectral_library_path = spectral_library_path,
                      intercept = intercept,
                      wavelengths = wavelengths,
                      spectra_noise_threshold = spectra_noise_threshold,
                      min_desired_wavelength = min_desired_wavelength,
                      max_desired_wavelength = max_desired_wavelength)

    time_pre_read_partial = time.perf_counter()
    test_cube = Hypercube(file_path,
                          min_desired_wavelength = min_desired_wavelength,
                          max_desired_wavelength = max_desired_wavelength)

    weight_array = WeightArray(test_matrix=test_matrix,
                               test_cube=test_cube,
                               relu = relu)

    weight_array.save(os.path.basename(weight_array.source), format = weight_format)

    if plot == True:

        if relu_before_plot == True:
            weight_array.relu()

        stacked_component_image = FalseColor([ImageChannel(weight_array = weight_array,
                                                           desired_component_or_wavelength = green_channel,
                                                           color = 'green',
                                                           cap = green_cap),
                                              ImageChannel(weight_array = weight_array,
                                                           desired_component_or_wavelength = red_channel,
                                                           color = 'red',
                                                           cap = red_cap),
                                              ImageChannel(weight_array = weight_array,
                                                           desired_component_or_wavelength = blue_channel,
                                                           color = 'blue',
                                                           cap = blue_cap)])

        stacked_component_image.save(stacked_component_image.source)

    time_post_read_partial = time.perf_counter() - time_pre_read_partial

    return('Finished running sample ' + file_path + ' in ' + str(time_post_read_partial) + 's')

if __name__ == "__main__":
    analyze_sample(file_path = args.file_path,
    fluorophore_ID_vector = args.fluorophore_ID_vector,
    min_desired_wavelength = args.min_desired_wavelength,
    max_desired_wavelength = args.max_desired_wavelength,
    green_channel = args.green_channel,
    red_channel = args.red_channel,
    blue_channel = args.blue_channel,
    green_cap = args.green_channel,
    red_cap = args.red_cap,
    blue_cap = args.blue_cap,
    weight_format = args.weight_format,
    plot = args.plot,
    spectral_library_path = args.spectral_library_path,
    intercept = args.intercept,
    spectra_noise_threshold = args.spectra_noise_threshold,
    normalize = args.normalize,
    rescale = args.rescale,
    chroma_width = args.chroma_width,
    #chroma_hypercube = None,
    chroma_path = args.chroma_path,
    relu_before_plot = args.relu_before_plot)
