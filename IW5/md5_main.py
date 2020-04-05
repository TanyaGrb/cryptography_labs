import math
import struct


def prepare_message(message):
    """Prepare message for hashing."""

    # append terminator byte, padding and original length in bits modulo 2 ** 64; the new length
    # will be a multiple of 64 bytes
    paddingSize = (64 - 1 - 8 - len(message) % 64) % 64
    lengthInBits = (len(message) * 8) % 2 ** 64
    return message + b"\x80" + paddingSize * b"\x00" + struct.pack("<Q", lengthInBits)


def rotate_left(n, amount):
    """Rotate a 32-bit integer left."""

    return ((n << amount) & 0xffff_ffff) | (n >> (32 - amount))


def hash_chunk(state, chunk):
    """Hash one chunk.
    state: 4 unsigned 32-bit integers
    chunk: 16 unsigned 32-bit integers
    return: 4 unsigned 32-bit integers"""

    a, b, c, d = state

    for i in range(64):
        if i < 16:  # F
            F = (b & c) | (~b & d)
            g = i
            shift = (7, 12, 17, 22)[i % 4]
        elif i < 32:  # G
            F = (d & b) | (c & ~d)
            g = (5 * i + 1) % 16
            shift = (5, 9, 14, 20)[i % 4]
        elif i < 48:  # H
            F = b ^ c ^ d
            g = (3 * i + 5) % 16
            shift = (4, 11, 16, 23)[i % 4]
        else:  # I
            F = c ^ (b | ~d)
            g = 7 * i % 16
            shift = (6, 10, 15, 21)[i % 4]

        k_i = math.floor(abs(math.sin(i + 1)) * 2 ** 32)
        bAdd = (k_i + a + F + chunk[g]) & 0xffff_ffff  # 2**32 - 1
        bAdd = rotate_left(bAdd, shift)

        (a, b, c, d) = (d, (b + bAdd) & 0xffff_ffff, b, c)

    return a, b, c, d


def md5(message):
    """Hash a bytestring. Return the hash as 16 bytes. See references."""

    # set initial state
    state = [0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476]  # a0, b0, c0, d0
    # prepare message and process it in chunks of 64 bytes (16 32-bit integers)
    for chunk in struct.iter_unpack("<16I", prepare_message(message)):
        # hash the chunk; add each 32-bit integer to the corresponding integer in the state
        hash_ = hash_chunk(state, chunk)
        state = [(s + h) & 0xffff_ffff for (s, h) in zip(state, hash_)]  # сложение state + hash_ по модулю 2**32
    # the final state is the hash
    return b"".join(struct.pack("<I", number) for number in state)


def main():
    """The main function."""

    message = b"000111"
    print(md5(message).hex())


if __name__ == "__main__":
    main()
