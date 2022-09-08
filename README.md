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

```
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

### Computing weights for spectral components

### Producing false color images for visualizing spectral component signals

## High-throughput deployment

## Under the hood

Main Readme and vignettes are forthcoming. Each individual function is documented using `docstring`.
