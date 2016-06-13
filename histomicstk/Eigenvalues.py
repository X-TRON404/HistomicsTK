import numpy as np


def Eigenvalues(H):
    """
    Calculates the eigenvectors of the hessian volumes 'H'
    generated by Hessian.py

    Parameters
    ----------
    H : array_like
        M x N x 4 hessian matrix - H[:,:,0] = dxx,
        H[:,:,1] = H[:,:,2] = dxy, H[:,:,3] = dyy.

    Returns
    -------
    Lambda : array_like
        M x N x 2 image of eigenvalues.
    V1 : array_like
        M x N x 2 eigenvector for Lambda(:,:,0)
    V2 :
        M x N x 2 eigenvector for Lambda(:,:,1)
    """

    # get size of H
    sizeX = H.shape[0]
    sizeY = H.shape[1]

    # initialize Lambda, V1 and V2
    Lambda = np.zeros((sizeX, sizeY, 2))
    V1 = np.zeros((sizeX, sizeY, 2))
    V2 = np.zeros((sizeX, sizeY, 2))

    # compute eigenvalues of H
    radical = np.sqrt((H[:, :, 0]-H[:, :, 3])**2 + 4*H[:, :, 1]**2)
    Lambda[:, :, 0] = (H[:, :, 0]+H[:, :, 3]+radical) / 2
    Lambda[:, :, 1] = (H[:, :, 0]+H[:, :, 3]-radical) / 2

    # compute eigenvectors of H
    V1[:, :, 0] = 2*H[:, :, 1]
    V1[:, :, 1] = H[:, :, 3] - H[:, :, 0] + radical
    norms = np.sqrt(V1[:, :, 0]**2 + V1[:, :, 1]**2)

    # normalize eigenvectors of H
    with np.errstate(divide='ignore', invalid='ignore'):
        V1[:, :, 0] = np.true_divide(V1[:, :, 0], norms)
        V1[:, :, 1] = np.true_divide(V1[:, :, 1], norms)
        # check -inf inf NaN
        V1[:, :, 0][ ~ np.isfinite(V1[:, :, 0])] = 0
        V1[:, :, 1][ ~ np.isfinite(V1[:, :, 1])] = 0
    V2[:, :, 0] = -V1[:, :, 1]
    V2[:, :, 1] = V1[:, :, 0]

    # order by magnitude
    swap = np.where(abs(Lambda[:, :, 0]) > abs(Lambda[:, :, 1]))

    # swap between Lambda[:, :, 0] and Lambda[:, :, 1]
    Lambda[:, :, 0][swap], Lambda[:, :, 1][swap] = \
        Lambda[:, :, 1][swap], Lambda[:, :, 0][swap]

    # swap between V1 and V2
    V1[:, :, 0][swap], V2[:, :, 0][swap] = V2[:, :, 0][swap], V1[:, :, 0][swap]
    V1[:, :, 1][swap], V2[:, :, 1][swap] = V2[:, :, 1][swap], V1[:, :, 1][swap]

    return Lambda, V1, V2
