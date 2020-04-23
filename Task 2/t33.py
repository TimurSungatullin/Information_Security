# coding=utf-8

from random import randint
import hashlib
from Crypto.Cipher import AES
from Crypto import Random

# Быстрое возведение в степень по модулю
def my_pow(x, y, n):
    z = 1
    while y > 0:
        if y % 2 == 1:
            z *= x
            z %= n
        x *= x
        x %= n
        y //= 2

    return z


p = ('ffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea6'
     '3b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245'
     'e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f2411'
     '7c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f'
     '83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08'
     'ca237327ffffffffffffffff')
g = 5
p = int(p, 16)
a = randint(1, p - 1)
b = randint(1, p - 1)

A = my_pow(g, a, p)
B = my_pow(g, b, p)
KA = my_pow(B, a, p)
KB = my_pow(A, b, p)
# Если True, значит оба клиента имеют одинаковые ключи
print KA == KB
# Встроенный метод возведения в степень по модулю
A = pow(g, a, p)
B = pow(g, b, p)
KA1 = pow(B, a, p)
KB = pow(A, b, p)
# Если True, значит функция my_pow реализована правильно
print KA1 == KA


class Client:
    def __init__(self, p=None, g=None):
        self.p = p
        self.g = g
        self.random_key = None
        self.final_key = None
        self.other_key = None
        self.my_key = None
        self.msg = None
        if all((self.p, self.g)):
            self.random_key = randint(1, p - 1)
            self.generate_key()

    def send(self, client, data=None, msg=None):
        if msg:
            iv = Random.new().read(AES.block_size)
            sha1_key = hashlib.sha1(hex(self.final_key)).hexdigest()[:16]
            aes = AES.new(sha1_key, mode=AES.MODE_CBC, IV=iv)
            msg = aes.encrypt(msg) + iv
        client.recv(data, msg)
        return msg

    def recv(self, data=None, msg=None):
        if data:
            if len(data) == 3:
                self.p = data[0]
                self.g = data[1]
                self.other_key = data[2]
                self.random_key = randint(1, p - 1)
                self.generate_key()
            elif len(data) == 1:
                self.other_key = data[0]
            self.update_key()

        if msg:
            iv = msg[-AES.block_size:]
            msg = msg[:-AES.block_size]
            sha1_key = hashlib.sha1(hex(self.final_key)).hexdigest()[:16]
            aes = AES.new(sha1_key, mode=AES.MODE_CBC, IV=iv)
            decrypted_msg = aes.decrypt(msg)
            print 'Client get the message'
            print decrypted_msg
            self.decrypted_msg = decrypted_msg

    def update_key(self):
        self.final_key = my_pow(self.other_key, self.random_key, self.p)

    def generate_key(self):
        self.my_key = my_pow(self.g, self.random_key, self.p)


print u'Тест реализации через класс Client'
A = Client(p, g)
B = Client()

A.send(B, data=(A.p, A.g, A.my_key))
B.send(A, data=(B.my_key,))
A.send(B, msg=b'Message for Bob!')
# Если True, клиенты получили одинаковые ключи
print A.final_key == B.final_key

"""
Вывод
True
True
Тест реализации черер класс Client
Client get the message
Message for Bob!
True
"""
