def find_desired_channel(data, desired_label):
    import numpy as np
    """ A high-level wrapper that finds to the index method of a list (after converting array to list if appropriate)

    :param data: A list (or numpy array) of values
    :param desired_label: A string indicating the element for which the user wishes to find the index in the list
    ...
    return: A numeric value indicating the index of the desired element

    >>> find_desired_channel([1, 2, 3, 4, 5], 3)
    2

    """
    ### Identifies the index  corresponding to the desired spectral component
    if isinstance(data, np.ndarray):
        data = data.tolist()
    desired_index = data.index(desired_label)
    return(desired_index)
    ###

def slice_desired_channel(array, desired_channel):
    slice = array[:,:,desired_channel]
    return(slice)

def CLS_to_image(CLS_matrix, cap, mode = 'opaque', match_size=False, color='white', relu = False):
    from PIL import Image
    import numpy as np
    # Usage:
    # image_out = CLS_to_image(CLS_matrix = load_CLS_layer(CLS_path = samples['CLS_data'][15],
    #                                                 layer = 'DsRed'),
    #                     cap = 10)
    if relu == True:
        CLS_matrix[CLS_matrix < 0] = 0

    CLS_matrix = np.interp(CLS_matrix,
                             (0,
                              #CLS_matrix.max()),
                              cap),
                             (0,
                              255)).astype(int)
    CLS_matrix_expanded = np.rot90(np.expand_dims(CLS_matrix, axis=2))
    if mode == 'opaque':
        empty_channel =  np.zeros((CLS_matrix_expanded.shape[0], CLS_matrix_expanded.shape[1], 1), dtype=np.uint8)
        if color=='white':
            CLS_matrix_expanded_filled = np.concatenate((CLS_matrix_expanded,
                                                         CLS_matrix_expanded,
                                                         CLS_matrix_expanded), axis=2).astype(np.uint8)
        if color=='red':
            CLS_matrix_expanded_filled = np.concatenate((CLS_matrix_expanded,
                                                         empty_channel,
                                                         empty_channel), axis=2).astype(np.uint8)
        if color=='green':
            CLS_matrix_expanded_filled = np.concatenate((empty_channel,
                                                         CLS_matrix_expanded,
                                                         empty_channel), axis=2).astype(np.uint8)
        if color=='blue':
            CLS_matrix_expanded_filled = np.concatenate((empty_channel,
                                                         empty_channel,
                                                         CLS_matrix_expanded), axis=2).astype(np.uint8)
        img = Image.fromarray(CLS_matrix_expanded_filled, 'RGB')
    if mode == 'transparent': # Don't think this mode is working yet
        blue_red_transparency =  np.zeros((CLS_matrix_expanded.shape[0], CLS_matrix_expanded.shape[1], 3), dtype=np.uint8)
        CLS_matrix_expanded_filled = np.concatenate((CLS_matrix_expanded, blue_red_transparency), axis=2).astype(np.uint8)
    #if match_size==True:
    #    img = img.crop((0, 0, rgb.size[0], rgb.size[1]))

    return(img)

def images_to_arrays(images):
    from numpy import asarray
    images_as_arrays = (asarray(image) for image in images)
    return(images_as_arrays)

def stack_images(images):
    from PIL import Image
    images_as_arrays = images_to_arrays(images)
    stacked_image = sum(images_as_arrays)
    stacked_image = Image.fromarray(stacked_image)
    return(stacked_image)

def checkIfDuplicates_l(listOfElems):
    ''' Check if given list contains any duplicates '''
    # Thank you Varun for this function
    # https://thispointer.com/python-3-ways-to-check-if-there-are-duplicates-in-a-list/
    if len(listOfElems) == len(set(listOfElems)):
        return False
    else:
        return True

import doctest
doctest.testmod()
