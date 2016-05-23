""" General Functions """

def mul(a, b):
    p = 0
    while b:
        if b & 1:
            p = p ^ a
        if a & 0x80:
            a = (a << 1) ^ 0b100011011
        else:
            a <<= 1
        b >>= 1
    return p

""" AES Functions """
import numpy as np
from copy import deepcopy


sbox = [
    [0x63,0x7c,0x77,0x7b,0xf2,0x6b,0x6f,0xc5,0x30,0x01,0x67,0x2b,0xfe,0xd7,0xab,0x76],
    [0xca,0x82,0xc9,0x7d,0xfa,0x59,0x47,0xf0,0xad,0xd4,0xa2,0xaf,0x9c,0xa4,0x72,0xc0],
    [0xb7,0xfd,0x93,0x26,0x36,0x3f,0xf7,0xcc,0x34,0xa5,0xe5,0xf1,0x71,0xd8,0x31,0x15],
    [0x04,0xc7,0x23,0xc3,0x18,0x96,0x05,0x9a,0x07,0x12,0x80,0xe2,0xeb,0x27,0xb2,0x75],
    [0x09,0x83,0x2c,0x1a,0x1b,0x6e,0x5a,0xa0,0x52,0x3b,0xd6,0xb3,0x29,0xe3,0x2f,0x84],
    [0x53,0xd1,0x00,0xed,0x20,0xfc,0xb1,0x5b,0x6a,0xcb,0xbe,0x39,0x4a,0x4c,0x58,0xcf],
    [0xd0,0xef,0xaa,0xfb,0x43,0x4d,0x33,0x85,0x45,0xf9,0x02,0x7f,0x50,0x3c,0x9f,0xa8],
    [0x51,0xa3,0x40,0x8f,0x92,0x9d,0x38,0xf5,0xbc,0xb6,0xda,0x21,0x10,0xff,0xf3,0xd2],
    [0xcd,0x0c,0x13,0xec,0x5f,0x97,0x44,0x17,0xc4,0xa7,0x7e,0x3d,0x64,0x5d,0x19,0x73],
    [0x60,0x81,0x4f,0xdc,0x22,0x2a,0x90,0x88,0x46,0xee,0xb8,0x14,0xde,0x5e,0x0b,0xdb],
    [0xe0,0x32,0x3a,0x0a,0x49,0x06,0x24,0x5c,0xc2,0xd3,0xac,0x62,0x91,0x95,0xe4,0x79],
    [0xe7,0xc8,0x37,0x6d,0x8d,0xd5,0x4e,0xa9,0x6c,0x56,0xf4,0xea,0x65,0x7a,0xae,0x08],
    [0xba,0x78,0x25,0x2e,0x1c,0xa6,0xb4,0xc6,0xe8,0xdd,0x74,0x1f,0x4b,0xbd,0x8b,0x8a],
    [0x70,0x3e,0xb5,0x66,0x48,0x03,0xf6,0x0e,0x61,0x35,0x57,0xb9,0x86,0xc1,0x1d,0x9e],
    [0xe1,0xf8,0x98,0x11,0x69,0xd9,0x8e,0x94,0x9b,0x1e,0x87,0xe9,0xce,0x55,0x28,0xdf],
    [0x8c,0xa1,0x89,0x0d,0xbf,0xe6,0x42,0x68,0x41,0x99,0x2d,0x0f,0xb0,0x54,0xbb,0x16]]

invSbox = [
    [0x52,0x09,0x6A,0xD5,0x30,0x36,0xA5,0x38,0xBF,0x40,0xA3,0x9E,0x81,0xF3,0xD7,0xFB],
    [0x7C,0xE3,0x39,0x82,0x9B,0x2F,0xFF,0x87,0x34,0x8E,0x43,0x44,0xC4,0xDE,0xE9,0xCB],
    [0x54,0x7B,0x94,0x32,0xA6,0xC2,0x23,0x3D,0xEE,0x4C,0x95,0x0B,0x42,0xFA,0xC3,0x4E],
    [0x08,0x2E,0xA1,0x66,0x28,0xD9,0x24,0xB2,0x76,0x5B,0xA2,0x49,0x6D,0x8B,0xD1,0x25],
    [0x72,0xF8,0xF6,0x64,0x86,0x68,0x98,0x16,0xD4,0xA4,0x5C,0xCC,0x5D,0x65,0xB6,0x92],
    [0x6C,0x70,0x48,0x50,0xFD,0xED,0xB9,0xDA,0x5E,0x15,0x46,0x57,0xA7,0x8D,0x9D,0x84],
    [0x90,0xD8,0xAB,0x00,0x8C,0xBC,0xD3,0x0A,0xF7,0xE4,0x58,0x05,0xB8,0xB3,0x45,0x06],
    [0xD0,0x2C,0x1E,0x8F,0xCA,0x3F,0x0F,0x02,0xC1,0xAF,0xBD,0x03,0x01,0x13,0x8A,0x6B],
    [0x3A,0x91,0x11,0x41,0x4F,0x67,0xDC,0xEA,0x97,0xF2,0xCF,0xCE,0xF0,0xB4,0xE6,0x73],
    [0x96,0xAC,0x74,0x22,0xE7,0xAD,0x35,0x85,0xE2,0xF9,0x37,0xE8,0x1C,0x75,0xDF,0x6E],
    [0x47,0xF1,0x1A,0x71,0x1D,0x29,0xC5,0x89,0x6F,0xB7,0x62,0x0E,0xAA,0x18,0xBE,0x1B],
    [0xFC,0x56,0x3E,0x4B,0xC6,0xD2,0x79,0x20,0x9A,0xDB,0xC0,0xFE,0x78,0xCD,0x5A,0xF4],
    [0x1F,0xDD,0xA8,0x33,0x88,0x07,0xC7,0x31,0xB1,0x12,0x10,0x59,0x27,0x80,0xEC,0x5F],
    [0x60,0x51,0x7F,0xA9,0x19,0xB5,0x4A,0x0D,0x2D,0xE5,0x7A,0x9F,0x93,0xC9,0x9C,0xEF],
    [0xA0,0xE0,0x3B,0x4D,0xAE,0x2A,0xF5,0xB0,0xC8,0xEB,0xBB,0x3C,0x83,0x53,0x99,0x61],
    [0x17,0x2B,0x04,0x7E,0xBA,0x77,0xD6,0x26,0xE1,0x69,0x14,0x63,0x55,0x21,0x0C,0x7D]]

def subBytes(state, op):
    for row in range(4):
        for col in range(4):
            ncol = state[row][col] % 16
            nrow = state[row][col] // 16
            if op == "encrypt":
                state[row][col] = sbox[nrow][ncol]
            else:
                state[row][col] = invSbox[nrow][ncol]

def shiftRows(state):
    state[1] = np.array([state[1][1], state[1][2], state[1][3], state[1][0]]).tolist()
    state[2] = np.array([state[2][2], state[2][3], state[2][0], state[2][1]]).tolist()
    state[3] = np.array([state[3][3], state[3][0], state[3][1], state[3][2]]).tolist()

def invShiftRows(state):
    state[1] = np.array([state[1][3], state[1][0], state[1][1], state[1][2]]).tolist()
    state[2] = np.array([state[2][2], state[2][3], state[2][0], state[2][1]]).tolist()
    state[3] = np.array([state[3][1], state[3][2], state[3][3], state[3][0]]).tolist()

def mixColumns(state):
    _state = np.zeros((4, 4), dtype=np.int)
    for col in range(4):
        _state[0, col] = mul(state[0][col], 2) ^ mul(state[1][col], 3) ^ state[2][col] ^ state[3][col]
        _state[1, col] = state[0][col] ^ mul(state[1][col], 2) ^ mul(state[2][col], 3) ^ state[3][col]
        _state[2, col] = state[0][col] ^ state[1][col] ^ mul(state[2][col], 2) ^ mul(state[3][col], 3)
        _state[3, col] = mul(state[0][col], 3) ^ state[1][col] ^ state[2][col] ^ mul(state[3][col], 2)

    for row in range(4):
        for col in range(4):
            state[row][col] = _state[row, col]

def invMixColumns(state):
    _state = np.zeros((4, 4), dtype=np.int)
    for col in range(4):
        _state[0, col] = mul(state[0][col], 14) ^ mul(state[1][col], 11) ^ mul(state[2][col], 13) ^ mul(state[3][col], 9)
        _state[1, col] = mul(state[0][col], 9) ^ mul(state[1][col], 14) ^ mul(state[2][col], 11) ^ mul(state[3][col], 13)
        _state[2, col] = mul(state[0][col], 13) ^ mul(state[1][col], 9) ^ mul(state[2][col], 14) ^ mul(state[3][col], 11)
        _state[3, col] = mul(state[0][col], 11) ^ mul(state[1][col], 13) ^ mul(state[2][col], 9) ^ mul(state[3][col], 14)

    for row in range(4):
        for col in range(4):
            state[row][col] = _state[row, col]

def addRoundKey(state, roundKey):
    for row in range(4):
        for col in range(4):
            state[row][col] = state[row][col] ^ int(roundKey[row][col])

rcon = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36]

def column(matrix, i):
    return [row[i] for row in matrix]

def keyExpansion(key, rounds):
    expanded = deepcopy(key)

    for i in range(4, rounds * 4):
        expanded = [row + [0] for row in expanded] #add a 0 right column
        temp = column(expanded, i - 1)
        temp1 = column(expanded, i - 4)
        if i % 4 == 0:
            rotWord(temp)
            subWord(temp)
            currentRound = i // 4
            temp[0] = temp[0] ^ rcon[currentRound - 1]

        for row in range(4):
            expanded[row][i] = temp[row] ^ temp1[row]

    return expanded

def rotWord(word):
    _word = word[:]
    for i in range(3):
        _word[i] = word[i + 1]
    _word[3] = word[0]
    #copy lists and modify the reference
    for i in range(4):
        word[i] = _word[i]

def subWord(word):
    for i in range(4):
        ncol = word[i] % 16
        nrow = word[i] // 16
        word[i] = sbox[nrow][ncol]

def getRoundkey(expanded, _round):
    roundkey = np.zeros((4, 4), dtype=np.int)
    _expanded = np.asmatrix(expanded)
    for i in range (4):
        roundkey[:, i] = _expanded[:, 4 * (_round - 1) + i].reshape(4,)

    return roundkey.tolist()

block = np.matrix([[0x01, 0x89, 0xfe, 0x76],
                   [0x23, 0xab, 0xdc, 0x54],
                   [0x45, 0xcd, 0xba, 0x32],
                   [0x67, 0xef, 0x98, 0x10]])

key = np.matrix([[0x0f, 0x47, 0x0c, 0xaf],
                 [0x15, 0xd9, 0xb7, 0x7f],
                 [0x71, 0xe8, 0xad, 0x67],
                 [0xc9, 0x59, 0xd6, 0x98]])

def encryptBlock(block, key):
    state = deepcopy(block)
    expandedKey = keyExpansion(key, 11)

    roundkey = getRoundkey(expandedKey, 1)
    addRoundKey(state, roundkey)
    #print "round11:\n{}".format(np.asmatrix(state))

    for _round in range(2, 12):
        subBytes(state, "encrypt")
        shiftRows(state)
        if _round != 11:
            mixColumns(state)
        roundkey = getRoundkey(expandedKey, _round)
        addRoundKey(state, roundkey)
        #print "round{}:\n{}".format(_round, np.asmatrix(state))

    return state   

def decryptBlock(block, key):
    state = deepcopy(block)
    expandedKey = keyExpansion(key, 11)

    roundkey = getRoundkey(expandedKey, 11)
    #print "roundkey:\n{}".format(np.asmatrix(roundkey))
    addRoundKey(state, roundkey)
    #print "round11:\n{}".format(np.asmatrix(state))

    for _round in reversed(range(1, 11)):
        invShiftRows(state)
        subBytes(state, "decrypt")
        roundkey = getRoundkey(expandedKey, _round)
        addRoundKey(state, roundkey)
        if _round != 1:
            invMixColumns(state)
        #print "round{}:\n{}".format(_round, np.asmatrix(state))

    return state   
