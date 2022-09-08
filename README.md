# `CubeGLM` (formerly `gmodetector_py`)
CubeGLM is a Python package for analyzing fluorescent hyperspectral images. Key features include the abilities to quantify known spectral components (e.g. GFP and chlorophyll, in the context of plant biology) in each pixel of hyperspectral images (A.K.A. hypercubes) as well as producing false color images to allow visualization of each component's concentration in each pixel. This package was developed for use in the [GMOdetector workflow](https://github.com/naglemi/gmodetector_py/) to study plant transformation; however, it can be used to analyze any hyperspectral images in which the number of spectral components is low enough for them to be quantified by regression without high levels of noise.

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
`spectral_library_path` should point to the path for the `spectral_library` folder in this GitHub repo, or alternatively your own spectral library with spectra in the same format. 
`fluorophore_ID_vector` should be a list that matches file prefixes of spectra in this folder. 
`file_path` should point to an ENVI-format `hdr` file that lists wavelengths for a sample hyperspectral image. Assuming the wavelengths for all of your images are the same, it can be any one of these images.


## High-throughput deployment

## Under the hood

Main Readme and vignettes are forthcoming. Each individual function is documented using `docstring`.
