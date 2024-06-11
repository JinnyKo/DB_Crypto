from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

# AES-256 키 생성 (보통은 환경 변수나 안전한 키 관리 시스템을 통해 관리)
KEY = get_random_bytes(32)

def encrypt(data):
    iv = get_random_bytes(16)
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    ct_bytes = cipher.encrypt(pad(data.encode(), AES.block_size))
    return iv + ct_bytes

def decrypt(ct):
    iv = ct[:16]
    ct = ct[16:]
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    return pt.decode()
