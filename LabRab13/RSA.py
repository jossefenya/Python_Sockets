import math, random
from fractions import gcd

distance = 100


def isSimple(a):
    for i in range(2, int(math.sqrt(a))):
        if a % i == 0:
            return False

    return True


class rsa:


    def generateKeys():
        p = random.randint(1, distance)
        while not isSimple(p):
            p = random.randint(1, distance)

        q = random.randint(1, distance)
        while not isSimple(p):
            q = random.randint(1, distance)

        n = p * q
        p_and_q = (p - 1) * (q - 1)

        e = random.randint(1, distance)

        while gcd(e, p_and_q) != 1:
            e = random.randint(1, distance)

        d = random.randint(1, 1000)

        while (d * e) % p_and_q != 1:
            d = random.randint(1, 1000)

        print('Server started work\n')

        open_key = (e, n)
        close_key = (d, n)

        return  (open_key, close_key)


    def encrypt(public, message):
        e, n = public
        secret_message = [((ord(i) ** e) % n) for i in message]
        return secret_message


    def decrypt(private, secret_message):
        d, n = private
        message = [chr((char ** d) % n) for char in secret_message]

        return ''.join(message)
