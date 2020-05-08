# coding=utf-8

# Для случайных больших чисел
import rsa


def get_random_p_q():
    # Большие случайные простые числа достанем из
    # пакета rsa, он создаёт открытй и закрытый ключ,
    # но берём только случайные числа p и q
    rsa_test = rsa.newkeys(1024)
    _, rsa_private_key = rsa_test
    p = rsa_private_key.p
    q = rsa_private_key.q
    return p, q


def invmod(a, n):
    t = 0
    newt = 1
    r = n
    newr = a
    # Пока остаток не равен 0
    while newr != 0:
        q = r // newr
        t, newt = newt, t - q * newt
        r, newr = newr, r - q * newr
    if t < 0:
        t += n
    return t


def get_keys(p, q):
    n = p * q
    t = (p - 1) * (q - 1)
    e = 3
    d = invmod(e, t)
    public_key = e, n
    private_key = d, n

    return public_key, private_key


def encrypt(msg, public_key):
    return pow(msg, public_key[0], public_key[1])


def decrypt(enc_msg, private_key):
    return pow(enc_msg, private_key[0], private_key[1])


p = 3557
q = 2579

# Пример с wikipedia (https://ru.wikipedia.org/wiki/RSA)
m = 111111

pub, priv = get_keys(p, q)

encr_msg = encrypt(m, pub)
# Должен вывести 4051753 (Из wikipedia)
print encr_msg

print decrypt(encr_msg, priv)

# Для больших p и q
p, q = get_random_p_q()

pub, priv = get_keys(p, q)

encr_msg = encrypt(m, pub)

print encr_msg

print decrypt(encr_msg, priv)

"""
Вывод
4051753 (Зашифрованное)
111111 (Расшифрованное)
1371737997260631 (Зашифрованное)
111111 (Расшифрованное)
"""