def build_X(fluorophore_ID_vector, intercept, wavelengths,
            min_desired_wavelength, max_desired_wavelength):  
    
    for i in range(0, (len(fluorophore_ID_vector))):
        print(i)
        path = (spectral_library_path + str(fluorophore_ID_vector[i]) + ".csv")
        if(os.path.isfile(path) == False):
            raise NameError("Error: Spectrum for " + fluorophore_ID_vector[i] + " not found in spectra_library folder")

        spectra = read_fit_spectra(spectra_path = path,
                                   wavelengths = wavelengths,
                                   plot = False,
                                   spectra_noise_threshold = 0.01)

        if(i==0 and intercept==1):
            intercept_vector = [1] * len(wavelengths)
            mm = np.c_[(intercept_vector, np.asarray(spectra['intensity']))] # https://stackoverflow.com/questions/43961585/cbind-r-function-equivalent-in-numpy

        if(i==0 and intercept==0):
            mm = np.array(spectra['intensity'])

        if(i>0):
            mm = np.c_[mm, np.array(spectra['intensity'])] # https://stackoverflow.com/questions/43961585/cbind-r-function-equivalent-in-numpy

    wavelengths = np.asarray(wavelengths)
    
    # https://stackoverflow.com/questions/13869173/numpy-find-index-of-the-elements-within-range
    wavelength_indices_desired = np.where(np.logical_and(wavelengths.astype(float)>=min_desired_wavelength,
                                                         wavelengths.astype(float)<=max_desired_wavelength))

    return(mm[wavelength_indices_desired,])
    
    
