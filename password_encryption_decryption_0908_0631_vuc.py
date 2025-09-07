# 代码生成时间: 2025-09-08 06:31:26
import bcrypt
from celery import Celery
from celery.task import task

# 配置Celery
app = Celery('password_encryption_decryption', broker='pyamqp://guest@localhost//')

# 加密密码的任务
@task(name='encrypt_password')
def encrypt_password(password):
    """
    使用bcrypt加密密码

    参数:
    password (str): 待加密的密码

    返回:
    str: 加密后的密码
    """
    if not password:
        raise ValueError("Password cannot be empty")

    try:
        # 使用bcrypt生成加密后的密码
        encrypted_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return encrypted_password.decode('utf-8')
    except Exception as e:
        # 处理加密过程中的错误
        raise Exception(f"Error encrypting password: {str(e)}")

# 解密密码的任务
@task(name='decrypt_password')
def decrypt_password(encrypted_password):
    """
    使用bcrypt解密密码

    参数:
    encrypted_password (str): 待解密的密码

    返回:
    bool: 解密成功返回True，否则返回False
    """
    if not encrypted_password:
        raise ValueError("Encrypted password cannot be empty")

    try:
        # 使用bcrypt验证密码是否匹配
        return bcrypt.checkpw(encrypted_password.encode('utf-8'), encrypted_password.encode('utf-8'))
    except Exception as e:
        # 处理解密过程中的错误
        raise Exception(f"Error decrypting password: {str(e)}")

# 测试
if __name__ == '__main__':
    # 加密密码
    plain_password = 'my_secret_password'
    encrypted = encrypt_password.delay(plain_password)
    print(f"Encrypted Password: {encrypted.get()}")

    # 解密密码
    decrypted = decrypt_password.delay(encrypted.get())
    print(f"Password Matches: {decrypted.get()}")