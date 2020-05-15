# coding=utf-8
import hashlib
import re

from t39 import encrypt
from t39 import rsa_test
from t39 import decrypt

# ASN.1 для md5 (17 Байт)
ASN1 = b'\x30\x20\x30\x0c\x06\x08\x2a\x8b\x48\x86\xf7\x0d\x02\x05\x00\x04\x10'


def get_signature(priv, message):
    md5 = hashlib.md5()
    md5.update(message)
    digest = md5.digest()
    block = (
            b'\x00\x01' + (b'\xff' * (128 - len(digest) - len(ASN1) - 2))
            + b'\x00' + ASN1 + digest
    )
    # Шифруем закрытым ключом
    # Подпись использует обратный алгоритм (Шифр закрытыам ключом)
    # Поэтому названия методов такие, из прошлого задания взяты
    sign = decrypt(int.from_bytes(block, byteorder='big'), priv)
    return sign.to_bytes((sign.bit_length() + 7) // 8, byteorder='big')


def check_signature(pub, message, signature):
    # Расшифруем открытым ключом
    encrypt_sign = encrypt(int.from_bytes(signature, byteorder='big'), pub)
    encrypt_sign = encrypt_sign.to_bytes((encrypt_sign.bit_length() + 7) // 8, byteorder='big')
    block = b'\x00' + encrypt_sign
    # 17 байт ASN.1 и 16 байт сообщение его и достаём из подписи
    r = re.compile(b'\x00\x01\xff+?\x00.{17}(.{16})', re.DOTALL)
    m = r.match(block)
    # Если шаблон неправильный, значит подпись невалидна
    if not m:
        return False
    digest = m.group(1)
    md5 = hashlib.md5()
    md5.update(message)
    # Проверяем совпадение с исходным сообщением
    return digest == md5.digest()


def fake_sign(m):
    md5 = hashlib.md5()
    md5.update(m)
    digest = md5.digest()
    block = b'\x00\x01\xff\x00' + ASN1 + digest + (
            b'\x00' * (128 - len(digest) - len(ASN1) - 4)
    )
    block_int = int.from_bytes(block, byteorder='big')
    sign_int = int_cube_root(block_int) + 1
    sign = sign_int.to_bytes((sign_int.bit_length() + 7) // 8, byteorder='big')
    return sign


def int_cube_root(x):
    """Получение целового кубического корня"""
    a = 2
    # Находим верхнюю границу
    while a * a * a <= x:
        a *= 2
    # Нижняя граница
    b = a // 2

    while a - b > 1:
        mid = (a + b) // 2
        if mid * mid * mid <= x:
            b = mid
        elif mid * mid * mid > x:
            a = mid

    return b


message = b'hi mom'
pub_key, priv_key = rsa_test()
# Обычная подпись
signature = get_signature(priv_key, message)
# В случае ошибки подписи
if not check_signature(pub_key, message, signature):
    print('Signature is not valid')
# Подделанная подпись
fake_signature = fake_sign(message)
if not check_signature(pub_key, message, fake_signature):
    print('Signature is not valid')


"""
Вывод:

_________________
Ничего, потому что подписи валидны
"""