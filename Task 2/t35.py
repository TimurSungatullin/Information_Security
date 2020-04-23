# coding=utf-8

import hashlib

from Crypto.Cipher import AES

from swapKey import Client

p = ('ffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea6'
     '3b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245'
     'e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f2411'
     '7c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f'
     '83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08'
     'ca237327ffffffffffffffff')
g1 = 5
p = int(p, 16)


def update_g(g):
    A = Client(p, g1)
    B = Client(p, g)

    print u'A send: p: {}, g: {}, A: {}'.format(A.p, A.g, A.my_key)
    print u'B recv: p: {}, update g: {}, p: {}'.format(A.p, g, A.my_key)
    A.send(B, data=(A.p, g, A.p))
    print u'B send: B: {}'.format(B.my_key)
    print u'A recv: B: {}'.format(B.my_key)
    B.send(A, data=(B.my_key,))
    # Если True, клиенты получили одинаковые ключи
    print A.final_key == B.final_key
    msg = b'Message for Bob!'
    # Отправим сообщение B
    A.send(B, msg=msg)
    # Отправим расшифрованное сообщение A
    B.send(A, msg=bytes(B.decrypted_msg))


print 'g: 1'
update_g(1)
print 'g: p'
update_g(p)
print 'g: p - 1'
update_g(p - 1)

"""
Вывод
g: 1
Client get the message
�z��g��i�9�N
Client get the message
���p`'[�̬�F�
g: p
Client get the message
Message for Bob!
Client get the message
Message for Bob!
g: p - 1
Client get the message
B��A�����̴�(&
Client get the message
����R<1�ӥ�a_7f
"""
