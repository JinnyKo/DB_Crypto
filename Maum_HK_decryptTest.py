#!/usr/bin/python
# -*- coding:utf-8 -*-

"""program"""
__author__ = "MINDsLAB"
__date__ = "creation: 2020-05-11, modification: 0000-00-00"

###########
# imports #
###########
import sys
import base64
import hashlib
import subprocess
from Crypto import Random
from Crypto.Cipher import AES

###########
# options #
###########

## Jinny ## 
## reload, sys.setdefaultencoding => python2 인코딩 설정/ python3 지원 안함
## python3 에서는 기본적으로 UTF-8 사용해서 근데 인코딩 설정 할 필요 없긴 함/ reload -> imoirtlib.reload 
## python3 에서는 문자열이랑 바이트 명확히 구분 해야해서, decode encode 적절히 잘 사용 ㄱㄱ 
# reload(sys)
#sys.setdefaultencoding("utf-8")  # => importlib.reload(sys) 


#########
# class #
#########
class AESCipher(object):
    def __init__(self, conf):
        self.bs = 16  # Jinny: 블록크기 설정 16byte 
        self.conf = conf
        # Jinny: OpenSSL명령어로 복호화된 값 설정 => openssl enc -seed -d -a -in {0} -pass file:{1} AES암호화 해제 명령 
        self.key = self.openssl_dec()

        # jinny: self.salt는 해시 생성할때 사용되는 솔트 값, 솔트값이 뭐냐면 관련된 키를 생성할 때 사용되는 추가 데이터인데 salt는 암호화나 해시 함수에 추가 해서
        #       같은 입력값이 주어지더라도 서로 다른 출력을 생성하도록 함, 그래서 동일한 비밀번호에 대해 항상 동일한 해시값이 생성되는 것을 방지
        self.salt = 'anySaltYouCanUse0f0n'  # 왜 랜덤이 아닌지 모르겠네 

        # self.private_key = self.get_private_key(self.key, self.salt)
        self.private_key = self.key

    
    # Jinny: 문자열 AES 블록 크기 맞게 패딩, AES 알고리즘은 입력 데이터가 블록 크기 배수가 아니면 작동 안해서, 패딩 크기 맞춰서 추가 데이터 삽입 해줘야함 
    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)
    # 패딩 전 데이터 길이: 20바이트
    # 블록 크기: 16바이트
    # 패딩 길이: 16 - (20 % 16) = 12바이트
    # 패딩 문자 값: 12 (0x0C)
    # ex데이터: "Hello World 1234"
    # 패딩된 데이터: "Hello World 1234\x0C\x0C\x0C\x0C\x0C\x0C\x0C\x0C\x0C\x0C\x0C\x0C"

    @staticmethod
    def _unpad(s):
        return s[0:-ord(s[-1:])]

    # Jinny: 실제 AES 생성 부분
    @staticmethod
    def get_private_key(secret_key, salt):
        return hashlib.pbkdf2_hmac('SHA256', secret_key.encode(), salt.encode(), 65536, 32)

    # Jinny: AES암호화: 패딩추가 -> 초기화 백터 생성 -> AES CBC 모드로 암호화 -> base64 인코딩 -> return
    def encrypt(self, message):
        message = self._pad(message)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.private_key, AES.MODE_CBC, iv)
        cipher_bytes = base64.b64encode(iv + cipher.encrypt(message.encode('utf-8')))
        return cipher_bytes.decode('utf-8')

    def decrypt(self, encoded):
        cipher_text = base64.b64decode(encoded)
        iv = cipher_text[:AES.block_size]
        cipher = AES.new(self.private_key, AES.MODE_CBC, iv)
        plain_bytes = self._unpad(cipher.decrypt(cipher_text[self.bs:]))
        return plain_bytes.decode('utf-8')

    # Jinny: 고정된 초기화 백터 사용해서 복호화 시키기 (보통은 각 암호화 작업마다 다른 IV 사용함, 보안성 안좋음)
    def decrypt_hk(self, encoded):
        cipher_text = base64.b64decode(encoded)
        iv = self.private_key[:AES.block_size]
        cipher = AES.new(self.private_key, AES.MODE_CBC, iv)
        decrypted_text = self._unpad(cipher.decrypt(cipher_text))
        return decrypted_text.decode('utf-8')

    def is_encrypt(self, message):
        try:
            self.decrypt(message)
            return True
        except Exception:
            return False

    @staticmethod
    def sub_process(cmd):
        sub_pro = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        response_out, response_err = sub_pro.communicate()
        return response_out, response_err

    def openssl_dec(self):
        cmd = "openssl enc -seed -d -a -in {0} -pass file:{1}".format(self.conf.pd, self.conf.ps_path)
        std_out, std_err = self.sub_process(cmd)
        return std_out.strip()


if __name__ == '__main__':
    class AESConfig(object):
        pd = '/APP/maum/cfg/.aes'
        ps_path = '/APP/maum/cfg/.heungkuk'
    
    # AESCipher 인스턴스 생성
    temp = AESCipher(AESConfig)

    # 사용자로부터 문자열 입력 받기
    test_str = input("Enter the string to encrypt: ")
    print(f"Original: {test_str}")
    
    # 암호화
    enc_str = temp.encrypt(test_str)
    print(f"Encrypted: {enc_str}")
    
    # 복호화
    dec_str = temp.decrypt(enc_str)
    print(f"Decrypted: {dec_str}")
    
    # 고정된 IV를 사용한 복호화 (예시)
    encoded_message = input("Enter the encoded message with fixed IV to decrypt (or press Enter to skip): ")
    if encoded_message:
        sample_str = temp.decrypt_hk(encoded_message)
        print(f"Decrypted with fixed IV: {sample_str}")

    # 추가 테스트
    test_str2 = input("\nEnter another string to encrypt: ")
    print(f"\nOriginal: {test_str2}")
    enc_str2 = temp.encrypt(test_str2)
    print(f"Encrypted: {enc_str2}")
    dec_str2 = temp.decrypt(enc_str2)
    print(f"Decrypted: {dec_str2}")
