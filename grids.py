import os
import sys
import pathlib

import numpy as np
import matplotlib.pyplot as plt

from astropy.io import fits

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
            with fits.open(file_name) as hdul:
                hdul.info()
                arr = hdul[0].data[ :, :]
                header= hdul[0].header             
            #arr = read_fits(file_name, fixdtype=True)
            plot_image(arr)
        else:
            print('ERROR: %s does not exist' % p)
            sys.exit(1)



if __name__ == '__main__':
    main(sys.argv)
