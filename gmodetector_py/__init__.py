from .version import __version__
from .x_import_utils import read_fit_spectra
from .x_import_utils import build_X
from .misc_utils import read_wavelengths
from .misc_utils import find_desired_indices
from .regression_utils import regress
from .plot_utils import find_desired_channel
from .plot_utils import slice_desired_channel
from .plot_utils import CLS_to_image
from .hypercube import Hypercube
from .xmatrix import XMatrix
from .weight_array import WeightArray
from .image_channel import ImageChannel
from .false_color import FalseColor
from .plot_utils import checkIfDuplicates_l
from .plot_utils import stack_images

# By importing these in __init__.py we make them available to the user
# If we import these functions in the __init__ file, all the user
# has to do is ```import package``` to access all these functions such as by
# gmodetector_py.read_fit_spectra(...)
