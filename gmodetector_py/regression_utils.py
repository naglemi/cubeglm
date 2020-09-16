import numpy as np

def regress(test_matrix, test_cube):
    """ Perform least squares (multiple) linear regression to regress hypercube onto design matrix and obtain weights for each spectral component in each pixel

    :param test_matrix: An object of class XMatrix (containing normalized spectra for each known component, and intercept if applicable)
    :param test_cube: An object of class Hypercube (containing spectra for each pixel)
    """

    MP_pseudoinverse = np.linalg.pinv(test_matrix.matrix)
    #b_vec = test_cube.hypercube.transpose(reshape(test_cube.hypercube.shape[2],
    #                                    test_cube.hypercube.shape[0] * test_cube.hypercube.shape[1])
    b_vec = test_cube.hypercube.transpose(2,0,1).reshape(test_cube.hypercube.shape[2], -1)
    m_vec = np.matmul(MP_pseudoinverse, b_vec)
    m_vec = m_vec.reshape((test_cube.hypercube.shape[0],
                          test_cube.hypercube.shape[1],
                          len(test_matrix.components)))
    return(m_vec)
