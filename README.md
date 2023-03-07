# `CubeGLM` (formerly `gmodetector_py`)
CubeGLM is a Python package for analyzing fluorescent hyperspectral images. Key features include the abilities to quantify known spectral components (e.g. GFP and chlorophyll, in the context of plant biology) in each pixel of hyperspectral images (A.K.A. hypercubes) as well as producing false color images to allow visualization of each component's concentration in each pixel. This package was developed for use in the [GMOdetector workflow](https://github.com/naglemi/gmodetector_py/) to study plant transformation; however, it can be used to analyze any hyperspectral images in which the number of spectral components is low enough for them to be quantified by regression without high levels of noise.

## Installation
This package is not yet available on Conda or PyPi repositories. The GitHub repo can be cloned and the package can be installed as follows:
1. Install a GitHub interface ([command line](https://cli.github.com/) or [graphical](https://desktop.github.com/) and clone this repository (e.g. `git clone https://github.com/naglemi/gmodetector_py.git` if using the command line.
2. (Recommended): Install [Anaconda or Miniconda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html#regular-installation) to support installation of dependencies without conflicts.
3. Create an environment that already has most dependencies using this command: <br><code>conda create -y -c conda-forge -n test-environment python=3.7.4 pytest codecov numpy pandas matplotlib tzlocal h5py pytables rpy2 parallel</code>
4. Activate the new conda environment<br><code>conda activate test-environment`</code>
5. Install *Spectral Python* from the *pypi* repository<br><code>pip install spectral`</code>
6. Launch R and install *scales* from the R console via:<br><code>install.packages('scales', repos = 'http://cran.us.r-project.org')</code>
- Note: To launch R, just type `R` on the command line and press enter. Once you have completed installation and are ready to leave R and return to command line, enter `q()`. When prompted, enter `n` to indicate there is no need to save the workspace.
7. Install *gmodetector_py* and test dependencies. The below command should be run from inside the *gmodetector_py* directory that is created from step 1 of this section.<br><code>pip install ".[test]"</code>

## Sample data
We provide two sample hyperspectral images that can be used to test CubeGLM and make sure the package is working properly before running your own data. Since these hyperspectral files are too large for GitHub (~1.4GB each), they can be found on [Google Drive](https://drive.google.com/drive/folders/1v13ynHfrER5e81nbT05mmgc1GaiAev0Z?usp=sharing). This folder also includes example outputs for comparison to ensure test analysis runs properly.

## Basic use

### Preparing a design matrix with known spectral components
To quantify spectral components in our hypercube, we must have a design matrix with columns representing the spectra of each known component. This can be prepared using the `XMatrix` class.

``` python
test_matrix = XMatrix(fluorophore_ID_vector = ['GFP', 'Chl', 'Noise'],
                      spectral_library_path = spectral_library_path,
                      intercept = 1,
                      wavelengths = read_wavelengths(file_path = file_path),
                      spectra_noise_threshold = 0.01,
                      min_desired_wavelength = 500,
                      max_desired_wavelength = 900)
```
- `intercept` can be set to 0 if there is no background signal in your hyperspectral images. To be clear, this means there is not even a faint signal when images are taken with no light source and perfect darkness is expected. If there is background signal, a y-intercept should be included by setting `intercept` to 1 instead of 0.
- `spectral_library_path` should point to the path for the `spectral_library` folder in this GitHub repo, or alternatively your own spectral library with spectra in the same format. 
- `fluorophore_ID_vector` should be a list that matches file prefixes of spectra in this folder. 
- `file_path` should point to an ENVI-format `hdr` file that lists wavelengths for a sample hyperspectral image. Assuming the wavelengths for all of your images are the same, it can be any one of these images. The prefix to the `hdr` file (containing metadata) must match a `raw` file (containing the hypercube itself) in the same folder.

### Loading a hypercube
``` python
test_cube = Hypercube(file_path,
                      min_desired_wavelength = 500,
                      max_desired_wavelength = 900)
```
- See under "Preparing a design matrix..." for the description of `file_path`. When creating an object of `Hypercube` class, it should point to the `hdr` file for the desired hyperspectral image.

### Computing weights for spectral components
``` python
weight_array = WeightArray(test_matrix=test_matrix,
                           test_cube=test_cube,
                           relu = relu_before_plot)
```
- `test_matrix` and `test_cube` should point to objects of `XMatrix` and `Hypercube` classes, produced as described in the previos two steps.
- `relu_before_plot` can be set to `True` (recommended for standard use) or `False`. If `True`, negative weights will be replaced with zero. This helps us make sure the scales for false color are consistent across images with the same settings (as described below).

To save a `weight_array` object for downstream analysis with other tools, we can use the `save` method for the `WeightArray` class as follows:
weight_array.save(path = output_file_name_prefix,
                  format = weight_format,
                  output_dir = output_dir,
                  threshold = threshold)

- `path` points to where the file will be saved. If you wish for the path to match the file preix of the imported hypercube, this can be set to `ntpath.basename(weight_array.source)`. Note, `ntpath` must first be imported (`import ntpath`).
- `format` can be set to either `csv` or `hdf` (the latter for faster loading in downstream analysis with other tools).
- `threshold` refers to a significance threshold. Above this threshold, all cumulative signal will be counted to produce summary statistics. The units are arbitrary and depend on a given hyperspectral camera. In our research, we set this to 38 because this represents above which significant GFP or DsRed reporter protein signal can be clearly distinguished from background noise. This only affects the `_summary.csv` files discussed below.

When a weight array is saved, two outputs will be produced. The first is the weight array itself, which can be analyzed with downstream tools such as in our [GMOdetector workflow](https://github.com/naglemi/gmodetector_py/) to study plant transformation. The second output is a `_summary.csv` file that contains the cumulative signals for each fluorescent component (with thresholding according to the aforementioned `threshold` parameter). This latter file can be used for statistical analysis in other workflows that do not involve further examination of the weight array itself.

### Producing false color images for visualizing spectral component signals
We can produce false color images representing the intensities of up to three spectral components using the `FalseColor` and `ImageChannel` classes.
``` python
stacked_component_image = FalseColor([ImageChannel(weight_array = weight_array,
                                                   desired_component_or_wavelength = "GFP",
                                                   color = 'green',
                                                   cap = 400),
                                      ImageChannel(weight_array = weight_array,
                                                   desired_component_or_wavelength = "Chl",
                                                   color = 'red',
                                                   cap = 200),
                                      ImageChannel(weight_array = weight_array,
                                                   desired_component_or_wavelength = "Noise",
                                                   color = 'blue',
                                                   cap = 200)])
```

- `weight_array` can point to an object of class `WeightArray` if you wish to plot spectral component weights. Alternatively, this parameter can be replaced with `hypercube` and pointed to a `Hypercube` object if you wish to plot wavelength intensities.
- `Desired_component_or_wavelength` can be set to either a string value referring to a known spectral component in the spectral library, or to a numeric value for a given wavelength for which data is collected.
- `color` must be set to `red`, `green`, or `blue` for a given channel.
- `cap` indicates an upper limit of signal for each of these component. Any signal at or above these values will appear with maximum brightness; thus, these variables are comparable to exposure on an RGB camera. If caps are too high, not much signal at lower ranges will be seen. If cap for a given component is too low, the false color images will appear overexposed with respect to the component.

Saving false color images:
``` python
stacked_component_image.save(path_prefix = stacked_component_image.source,
                             output_dir = output_dir)
```
This will save a `png` file for the `FalseColor` image with the same file prefix as the input hypercube, in the user-defined `output_dir`.

## High-throughput deployment
In this repository, `analyze_sample.py` is provided in the `wrappers` folder. This provides a high-level Python function, as well as a command line interface, to run over the previously described functions for a given sample.

For details, run `python analyze_sample.py` from the command line to see command-line argument descriptions, or run `help(analyze_sample)` from Python after loading the function.

## Under the hood
See the notebook [`Designing_regression.ipynb`](https://github.com/naglemi/gmodetector_py/blob/master/notebooks/Designing_regression.ipynb) for a description of the mathematical approach.

## Acknowledgements
We thank the National Science Foundation Plant Genome Research Program for support (IOS #1546900, Analysis of genes affecting plant regeneration and transformation in poplar), and members of GREAT TREES Research Cooperative at OSU for its support of the Strauss laboratory.
