import numpy as np
from gmodetector_py import build_X
from gmodetector_py import find_desired_indices

class XMatrix:
    """A design matrix for multiple linear regression, with effect and observation labels

    :param fluorophore_ID_vector: A list of spectral components in the spectral library
    :param spectral_library_path: A string indicating the directory where spectra can be found
    :param intercept: If 0, no intercept is added to X. If 1, a vector of 1s equal to # spectra is prepended to X.
    :param wavelengths: A list of precise wavelengths to be passed to read_fit spectra, which will fit the published spectra
    :param spectra_noise_threshold: A float indicating a threshold below which fitted spectra values are set to zero (default value is 0.01, an approximate noise threshold of the Andor hyperspectral camera), passed to read_fit_spectra
    :param min_desired_wavelength: A numeric value indicating a threshold BELOW which spectral data is excluded
    :param max_desired_wavelength: A numeric value indicating a threshold ABOVE which spectral data is excluded

    :ivar components: contains the contents of ``fluorophore_ID_vector`` passed as init
    :ivar wavelengths: contains the contents of ``wavelengths`` passed as init and subsequently trimmed to desired range
    :ivar matrix: contains the X matrix itself, trimmed to wavelengths for desired range, with one column for each component (and another for the intercept, if applicable)
    """

    def _nan_to_zero(self):
        return(np.nan_to_num(self.matrix))

    def _plot(self, tick_step = np.int(50)):
        # style
        plt.style.use('seaborn-darkgrid')

        # create a color palette
        palette = plt.get_cmap('Set1')

        # multiple line plot
        num=0

        XMatrix_plottable = pd.DataFrame(self.matrix)

        for column in XMatrix_plottable:
            num+=1
            plt.plot(self.wavelengths,
                     XMatrix_plottable[column],
                     marker='',
                     color=palette(num),
                     linewidth=1, alpha=0.9,
                     label=column)

        # Add legend
        plt.legend(loc=2, ncol=2)
        print("HEY")
        print(self.wavelengths.shape[0]-1)
        print(len(self.wavelengths))

        # Change tick marks
        #plt.xticks(np.arange(start = float(min(self.wavelengths)),
        #                     stop = float(max(self.wavelengths)),
        #                     step = tick_step))


        # Add titles
        plt.title("Design matrix of spectral components", loc='left', fontsize=12, fontweight=0, color='orange')
        plt.xlabel("Wavelength (nm)")
        plt.ylabel("Signal intensity (normalized)")

    def __init__(self, fluorophore_ID_vector, spectral_library_path,
                 intercept, wavelengths, spectra_noise_threshold,
                 min_desired_wavelength, max_desired_wavelength):
        # Define attribute with contents of the value param

        if intercept == 1:
            components = fluorophore_ID_vector.copy()
            components.insert(0, "Intercept")

        self.matrix = build_X(fluorophore_ID_vector = fluorophore_ID_vector,
                                             spectral_library_path = spectral_library_path,
                                             intercept = intercept,
                                             wavelengths = wavelengths,
                                             spectra_noise_threshold = spectra_noise_threshold,
                                             min_desired_wavelength = min_desired_wavelength,
                                             max_desired_wavelength = max_desired_wavelength)
        self.wavelengths = np.asarray(wavelengths)[find_desired_indices(wavelengths,
                                                            min_desired_wavelength,
                                                            max_desired_wavelength)]
        self.components = components
