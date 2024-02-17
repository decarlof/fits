import os
import sys
import pathlib

import numpy as np
import matplotlib.pyplot as plt

from astropy.io import fits



def _getDataType(path):
    bitpix = _readBITPIX(path)
    if bitpix > 0:
        dtype = 'uint%s' % bitpix
    elif bitpix <= -32:
        dtype = 'float%s' % -bitpix
    else:
        dtype = 'int%s' % -bitpix
    return dtype

def _readBITPIX(path):
    # astropy fits reader has a problem
    # have to read BITPIX from the fits file directly
    stream = open(path, 'rb')
    while True:
        line = stream.read(80).decode("utf-8")
        if line.startswith('BITPIX'):
            value = line.split('/')[0].split('=')[1].strip()
            value = int(value)
            break
        continue
    stream.close()
    return value


def read_fits(fname, fixdtype=True):
    """
    Read data from fits file.

    Parameters
    ----------
    fname : str
        String defining the path of file or file name.

    Returns
    -------
    ndarray
        Data.
    """

    # NOTE:
    # at astropy 1.0.5, it is necessary to fix the dtype
    # but at 1.1.1, it seems unnecessary
    f = fits.open(fname)
    arr = f[0].data
    f.close()
    if fixdtype:
        dtype = _getDataType(fname)
        if dtype:
            arr = np.array(arr, dtype=dtype)
    return arr

def plot_image(arr):

    plt.figure()
    plt.imshow(arr, cmap='gray')
    plt.title(f"Image")
    plt.axis("off")    
    plt.show()    

def main(args):

    if len(sys.argv) == 1:
        print ('ERROR: Must provide the path to a run-file folder as the argument')
        print ('Example:')
        print ('        python %s /data/file.fits'% sys.argv[0])
        sys.exit(1)
    else:

        file_name   = sys.argv[1]
        p = pathlib.Path(file_name)
        if p.is_file():
            arr = read_fits(file_name, fixdtype=True)
            plot_image(arr)
        else:
            print('ERROR: %s does not exist' % p)
            sys.exit(1)



if __name__ == '__main__':
    main(sys.argv)