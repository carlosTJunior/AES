import aes
import numpy as np


np.set_printoptions(formatter={'int': hex})

if __name__ == '__main__':
    c = aes.encryptBlock(aes.block.tolist(), aes.key.tolist())
    cm = np.asmatrix(c)

    print "\n\nOriginal Block: \n\n{}".format(aes.block)
    print "\n\nEncrypted Block: \n\n{}".format(cm)

    p = aes.decryptBlock(cm.tolist(), aes.key.tolist())
    pm = np.asmatrix(p)

    print "\n\nDecrypted Block: \n\n{}\n".format(pm)
