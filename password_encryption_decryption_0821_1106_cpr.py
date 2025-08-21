# 代码生成时间: 2025-08-21 11:06:05
# -*- coding: utf-8 -*-

import hashlib
cryptography as crypt
import os
from celery import Celery
from celery import shared_task
from cryptography.fernet import Fernet

# 配置Celery
app = Celery('password_encryption_decryption',
             broker='pyamqp://guest@localhost//')

def get_key():
    # 生成密钥（32字节URL安全base64编码）
    key = Fernet.generate_key()
    return key

# 保存密钥到文件
def save_key_to_file(key):
    with open('secret.key', 'wb') as key_file:
        key_file.write(key)

# 从文件读取密钥
def load_key_from_file():
    return open('secret.key', 'rb').read()

# 加密函数
@shared_task
def encrypt_password(password, key=None):
    if key is None:
        key = load_key_from_file()
    f = Fernet(key)
    encrypted_password = f.encrypt(password.encode())
    return encrypted_password

# 解密函数
@shared_task
def decrypt_password(encrypted_password, key=None):
    if key is None:
        key = load_key_from_file()
    f = Fernet(key)
    decrypted_password = f.decrypt(encrypted_password)
    return decrypted_password

# 生成密钥并保存
def setup_encryption_key():
    key = get_key()
    save_key_to_file(key)
    print('Encryption key has been generated and saved.')

# 示例使用
if __name__ == '__main__':
    setup_encryption_key()  # 首次运行时生成并保存密钥
    password = 'my_secret_password'
    encrypted = encrypt_password(password)
    print('Encrypted:', encrypted)
    decrypted = decrypt_password(encrypted)
    print('Decrypted:', decrypted)
