# coding=utf-8

from t39 import get_keys, encrypt, invmod, get_random_p_q, decrypt
from Crypto.Random import random


m = 111111

p, q = get_random_p_q()

public_key, private_key = get_keys(p, q)

# Шифрованный текст
c = encrypt(m, public_key)

# Модуль и экспонента
e, n = public_key

# Случайное число
s = random.randint(2, n - 1)

# Получаем новый шифрованный текст
c2 = (pow(s, e, n) * c) % n

# Даём серверу и получаем расшифруемое значение
m2 = decrypt(c2, private_key)

# Дешифруем
P = (m2 * invmod(s, n)) % n

print P
# Если совпадают, значит правильно расшифровали
print P == m

"""
Вывод
111111
True
"""
