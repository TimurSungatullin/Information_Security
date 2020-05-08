# coding=utf-8

from t39 import get_keys, encrypt, invmod, get_random_p_q

m = 111111

# Первое шифрование
p, q = get_random_p_q()

public_key1, _ = get_keys(p, q)

e_m1 = encrypt(m, public_key1)

# Второе шифрование
p, q = get_random_p_q()

public_key2, _ = get_keys(p, q)

e_m2 = encrypt(m, public_key2)

# Третье шифрование
p, q = get_random_p_q()

public_key3, _ = get_keys(p, q)

e_m3 = encrypt(m, public_key3)

# Произведение всех 3
n_012 = public_key1[1] * public_key2[1] * public_key3[1]

# Произведение открытых ключей, кроме nj
m_s_0 = public_key2[1] * public_key3[1]
m_s_1 = public_key1[1] * public_key3[1]
m_s_2 = public_key2[1] * public_key1[1]

# Остатки от деления
c_0 = e_m1
c_1 = e_m2
c_2 = e_m3

# 3 зашифрованных сообщения
print c_0, c_1, c_2

r0 = (c_0 * m_s_0 * invmod(m_s_0, public_key1[1]))

r1 = (c_1 * m_s_1 * invmod(m_s_1, public_key2[1]))

r2 = (c_2 * m_s_2 * invmod(m_s_2, public_key3[1]))

r = (r0 + r1 + r2) % n_012

# Декодированное сообщение
print r ** (1. / 3)
# Если совпадут, получилось декодировать сообщение
print r ** (1. / 3) == m


"""
Вывод
1371737997260631 1371737997260631 1371737997260631
111111.0
True
"""
