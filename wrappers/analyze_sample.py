def analyze_sample(file_path, test_matrix, min_desired_wavelength, max_desired_wavelength,
                   green_channel, red_channel, blue_channel,
                   green_cap, red_cap, blue_cap, weight_format,
                   plot = True):

    time_pre_read_partial = time.perf_counter()
    test_cube = Hypercube(file_path,
                          min_desired_wavelength = min_desired_wavelength,
                          max_desired_wavelength = max_desired_wavelength)

    weight_array = WeightArray(test_matrix=test_matrix,
                               test_cube=test_cube)

    weight_array.save(weight_array.source, format = weight_format)

    if plot == True:

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
