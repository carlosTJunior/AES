import unittest
import numpy as np
import aes1

class TestAES(unittest.TestCase):

    def setUp(self):
        pass

    def testSubBytes(self):
        state = np.matrix([[0xea, 0x04, 0x65, 0x85],
                           [0x83, 0x45, 0x5d, 0x96],
                           [0x5c, 0x33, 0x98, 0xb0],
                           [0xf0, 0x2d, 0xad, 0xc5]])

        expected = np.matrix([[135, 242,  77, 151],
                              [236, 110,  76, 144],
                              [ 74, 195,  70, 231],
                              [140, 216, 149, 166]])

        aes1.subBytes(state)
        areEqual = (state == expected).all()
        self.assertTrue(areEqual)

    def testShiftRows(self):
        state = [[0x87, 0xf2, 0x4d, 0x97],
                 [0xec, 0x6e, 0x4c, 0x90],
                 [0x4a, 0xc3, 0x46, 0xe7],
                 [0x8c, 0xd8, 0x95, 0xa6]]

        expected = [[0x87, 0xf2, 0x4d, 0x97],
                    [0x6e, 0x4c, 0x90, 0xec],
                    [0x46, 0xe7, 0x4a, 0xc3],
                    [0xa6, 0x8c, 0xd8, 0x95]]

        aes.shiftRows(state)
        self.assertEqual(state, expected)

    def testMixColumns(self):
        state = [[0x87, 0xf2, 0x4d, 0x97],
                 [0x6e, 0x4c, 0x90, 0xec],
                 [0x46, 0xe7, 0x4a, 0xc3],
                 [0xa6, 0x8c, 0xd8, 0x95]]

        expected = [[0x47, 0x40, 0xa3, 0x4c],
                    [0x37, 0xd4, 0x70, 0x9f],
                    [0x94, 0xe4, 0x3a, 0x42],
                    [0xed, 0xa5, 0xa6, 0xbc]]

        aes.mixColumns(state)
        self.assertEqual(state, expected)

    def testAddRoundKey(self):
        state = [[0x47, 0x40, 0xa3, 0x4c],
                 [0x37, 0xd4, 0x70, 0x9f],
                 [0x94, 0xe4, 0x3a, 0x42],
                 [0xed, 0xa5, 0xa6, 0xbc]]

        key = [[0x0f, 0x47, 0x0c, 0xaf],
               [0x15, 0xd9, 0xb7, 0x7f],
               [0x71, 0xe8, 0xad, 0x67],
               [0xc9, 0x59, 0xd6, 0x98]]

        expected = [[0x48L, 0x7L, 0xafL, 0xe3L],
                    [0x22L, 0xdL, 0xc7L, 0xe0L],
                    [0xe5L, 0xcL, 0x97L, 0x25L],
                    [0x24L, 0xfcL, 0x70L, 0x24L]]

        aes.addRoundKey(state, key)
        self.assertEqual(state, expected)

    def testRotWord(self):
        word = [1, 2, 3, 4]

        expected = [2, 3, 4, 1]

        aes.rotWord(word)
        self.assertEqual(word, expected)

    def testSubWord(self):
        word = [0x1, 0x23, 0x45, 0x67]

        expected = [0x7c, 0x26L, 0x6eL, 0x85L]

        aes.subWord(word)
        self.assertEqual(word, expected)

    def testKeyExpansion(self):
        pass

    def testGetRoundKey(self):
        pass

if __name__ == '__main__':
    unittest.main()
