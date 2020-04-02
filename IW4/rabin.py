from math import sqrt

from sympy import randprime


def adv_gcd(a, b):
    if not b:
        return 1, 0
    y, x = adv_gcd(b, a % b)
    return x, y - (a // b) * x


def phi(n):
    result = n
    bound = int(sqrt(n))
    for i in range(2, bound):
        if n % i == 0:
            while n % i == 0:
                n /= i
            result *= 1 - 1 / i
    if n > 1:
        result -= result / n
    return int(result)


class Rabin:
    def __init__(self):
        self.p = None
        self.q = None
        self.n = None
        self.get_keys()
        self.alphabet = ".abcdefghijklmnopqrstuvwxyz 1234"

    def get_keys(self):
        while True:
            self.p = randprime(3, 100)
            self.q = randprime(3, 100)
            self.n = self.p * self.q
            if self.p != self.q and len(bin(self.n)) == 12 and self.p % 4 == 3 and self.q % 4 == 3:
                break

    def get_public_key(self):
        return self.n

    def get_private_key(self):
        return self.p, self.q

    def encrypt_block(self, m):
        return pow(m, 2, self.n)

    def decrypt_block(self, c):
        y_p, y_q = adv_gcd(self.p, self.q)
        m_p = pow(c, (self.p + 1) // 4, self.p)
        m_q = pow(c, (self.q + 1) // 4, self.q)
        r1 = (y_p * self.p * m_q + y_q * self.q * m_p) % self.n
        r2 = self.n - r1
        r3 = (y_p * self.p * m_q - y_q * self.q * m_p) % self.n
        r4 = self.n - r3
        return r1, r2, r3, r4

    def encrypt(self, text):
        blocks, k = self.get_blocks(text)
        number_blocks = [int(
            format(self.alphabet.find(blk[0]), f'#0{7}b')[2:] + format(self.alphabet.find(blk[1]), f'#0{7}b')[2:], 2)
            for blk in blocks]
        if any([item > self.n for item in number_blocks]):
            # если какой-то из полученных элементов больше n, то нужно взять другие ключи
            self.get_keys()
            return self.encrypt(text)
        crypted = [self.encrypt_block(item) for item in number_blocks]
        print(f"Открытый ключ: {self.get_public_key()}")
        with open("private_key.txt", "w") as private_key:
            private_key.write(f"{self.get_private_key()}")
        return "".join([self.alphabet[number // 32] + self.alphabet[number % 32] for number in crypted])

    def decrypt(self, text):
        blocks, k = self.get_blocks(text)
        result = []
        for block in blocks:
            temp = []
            n1, n2 = self.alphabet.find(block[0]), self.alphabet.find(block[1])
            decrypted = self.decrypt_block(n1 * 32 + n2)
            for mb in decrypted:
                n = bin(mb)[2:]
                if len(n) < 6:
                    continue
                temp.append(self.alphabet[int(n[-10:-5], 2)] + self.alphabet[int(n[-5:], 2)])
            result.append(temp)
        return result

    @staticmethod
    def get_blocks(text):
        k = 2
        blocks = [text[i:i + k] for i in range(0, len(text), k)]
        if len(blocks[-1]) != k:
            blocks[-1] = blocks[-1] + " " * (k - len(blocks[-1]))
        return blocks, k


text = "source text"
print(f"Исходный текст: {text}")
rabin = Rabin()
ciphertext = rabin.encrypt(text)
print(f"Шифротекст: {ciphertext}")
decoded_text = rabin.decrypt(ciphertext)
print(f"Расшифрованный: {decoded_text}")
