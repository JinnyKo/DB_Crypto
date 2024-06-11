#AES-256:
# 대칭 키 암호화 알고리즘, 동일한 키를 사용해서 데이터를 암호화, 복호화 시킴
# AES 는 128,192,256 비트  키 길이를 지원 (256 가장 높은 수중 보안)

# Cipher: 다양한 암호화 모드 지원(CBC,ECB,CTR ...) => 여기서 AES 알고리즘이랑, "암호화 모드" 는 다른 거임
#  
# 1.
from Crypto.Cipher import AES
# 암호화에 필요한 임의의 바이트 데이터를 생성하는 함수 'get_random_bytes'
from Crypto.Random import get_random_bytes
# pad: 데이터를 블록 크기에 맞게 패딩함 'unpd': 복호화된 데이터에서 패딩을 제거함 
from Crypto.Util.Padding import pad, unpad

# AES-256 키 생성 (256비트 = 32바이트)
key = get_random_bytes(32)

def encrypt(data, key):
    # Initialization Vector (IV) 생성/IV는 AES 블록 암호화 알고리즘 블록 크기와 동일한 길이여야 함. 
    # AES의 블록 크기는 128비트 이기 때문에 무조건 항상 IV는 16바이트 길이로 생성되어야함
    iv = get_random_bytes(16)
    # AES cipher 객체 생성 (CBC 모드)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # 데이터 패딩 및 암호화 => 패딩을 사용해서 데이터를 블록 크기로 맞춤 
    # padding: AES같은 블록 암호화 알고리즘은 고정된 크기의 블록 단위로 데이터를 처리 하는데, AES의 경우 블록크기가 16바이트 임 
    # 즉, 암호화 하려는 데이터의 길이가 16바이트의 배수가 아니면, 이 데이터의 길이를 16바이트의 배수로 맞춰야함. 그게 padding
    
    ct_bytes = cipher.encrypt(pad(data.encode(), AES.block_size))
    return iv + ct_bytes

def decrypt(ct, key):
    # IV 분리
    iv = ct[:16]
    ct = ct[16:]
    # AES cipher 객체 생성 (CBC 모드)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # 데이터 복호화 및 패딩 제거
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    return pt.decode()

# 예시 데이터
data = "Hello, AES-256 Encryption!"
# 데이터 암호화
encrypted_data = encrypt(data, key)
print(f"Encrypted: {encrypted_data.hex()}")

# 데이터 복호화
decrypted_data = decrypt(encrypted_data, key)
print(f"Decrypted: {decrypted_data}")
