# coding=utf-8

import hashlib

from Crypto.Cipher import AES

from t33 import Client

p = ('ffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea6'
     '3b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245'
     'e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f2411'
     '7c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f'
     '83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08'
     'ca237327ffffffffffffffff')
g1 = 5
p = int(p, 16)


def update_g(g):

    A = Client(p, g)
    B = Client(p, g)
    print u'A send: p: {}, g: {}, A: {}'.format(A.p, A.g, A.my_key)
    print u'B recv: p: {}, update g: {}, p: {}'.format(A.p, A.g, A.my_key)
    A.send(B, data=(A.p, A.g, A.my_key))
    print u'B send: B: {}'.format(B.my_key)
    print u'A recv: B: {}'.format(B.my_key)
    B.send(A, data=(B.my_key,))
    # Если True, клиенты получили одинаковые ключи
    print A.final_key == B.final_key
    msg = b'Message for Bob!'
    # Отправим сообщение B
    decr_msg = A.send(B, msg=msg)
    # Если g == 1, то ключ будет равен 1 ^ (ab) % p, то есть 1
    if g == 1:
        iv = decr_msg[-AES.block_size:]
        decr_msg = decr_msg[:-AES.block_size]
        sha1_key = hashlib.sha1(hex(1L)).hexdigest()[:16]
        aes = AES.new(sha1_key, mode=AES.MODE_CBC, IV=iv)
        decrypted_msg = aes.decrypt(decr_msg)
        print 'Успешно подобрали ключ'
        print msg == decrypted_msg
    # Если g == p, то ключ будет равен p ^ (ab) % p, то есть 0 (Из прошлого задания)
    if g == p:
        iv = decr_msg[-AES.block_size:]
        decr_msg = decr_msg[:-AES.block_size]
        sha1_key = hashlib.sha1(hex(0L)).hexdigest()[:16]
        aes = AES.new(sha1_key, mode=AES.MODE_CBC, IV=iv)
        decrypted_msg = aes.decrypt(decr_msg)
        print 'Успешно подобрали ключ'
        print msg == decrypted_msg
    # Если g == p, то ключ будет равен (-1) ^ (ab) % p, то есть 1 или p - 1 (Рассмотрим оба)
    if g == p - 1:
        iv = decr_msg[-AES.block_size:]
        decr_msg = decr_msg[:-AES.block_size]
        sha1_key = hashlib.sha1(hex(1L)).hexdigest()[:16]
        aes = AES.new(sha1_key, mode=AES.MODE_CBC, IV=iv)
        decrypted_msg1 = aes.decrypt(decr_msg)
        sha1_key = hashlib.sha1(hex(p - 1)).hexdigest()[:16]
        aes = AES.new(sha1_key, mode=AES.MODE_CBC, IV=iv)
        decrypted_msg2 = aes.decrypt(decr_msg)
        print 'Успешно подобрали ключ'
        print msg in (decrypted_msg1, decrypted_msg2)
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
Message for Bob!
Успешно подобрали ключ
True
g: p
Client get the message
Message for Bob!
Успешно подобрали ключ
True
g: p - 1
Client get the message
Message for Bob!
Успешно подобрали ключ
True
"""
