import random
import numpy as np
from constants import SBOX, RCON

class AES():

    def __init__(self):
        self.security = 128
        self.key = self.generatekey()
        self.roundkeys = self.generateroundkeys(self.key)

    def generatekey(self):
        bits = np.random.randint(0, 2, self.security)
        bits = bits.reshape(-1, 16)
        key = np.packbits(bits, axis=1).reshape(4,4)
        return key

    def generateroundkeys(self, key):
        keys = [key]
        for round in range(10):
            prev = keys[-1]
            transformed_col = self.rcon(self.subbytes(self.rotword(prev[:,-1])), 0)
            col1 = key[:,0] ^ transformed_col
            col2 = key[:,1] ^ col1
            col3 = key[:,2] ^ col2
            col4 = key[:,3] ^ col3
            keys.append(np.array([col1, col2, col3, col4]))
        return keys


    def encrypt(self, data):
        blocks = self.toblocks(data)
        blocks = blocks ^ self.roundkeys[0]
        for round in range(10):
            blocks = self.subbytes(blocks)
            blocks = self.shiftrows(blocks)
            blocks = self.mixcolumns(blocks)

    def subbytes(self, blocks):
        lookup = np.vectorize(lambda x: int(SBOX.get(x)))
        return lookup(blocks)
    
    def shiftrows(self, blocks):

        for block in blocks:
            block[1] = np.roll(block[1], -1)
            block[2] = np.roll(block[2], -2)
            block[3] = np.roll(block[3], -3)

        return blocks

    def mixcolumns(self, blocks):

        A = np.array([
            [2,3,1,1],
            [1,2,3,1],
            [1,1,2,3],
            [3,1,1,2]
            ])

        for block in blocks:


        return blocks

    def rotword(self, x):
        return np.roll(x, -1)

    def rcon(self, x, round):
        x[0] = int(x[0] ^ RCON[round])
        return x

    def toblocks(self, data):
        hex_data = data.encode().hex()
        n_pad = 16 - int(abs((len(hex_data) / 2) % 16 ))
        if n_pad:
            hex_data += format(n_pad, '02x') * n_pad
        bytes_ = list(int(hex_data[i:i+2], 16) for i in range(0, len(hex_data), 2))
        blocks = np.array(bytes_).reshape(-1, 4, 4)
        return blocks
