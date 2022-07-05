from distutils.log import error
import json
import secrets
import json
from argon2 import PasswordHasher
from Crypto.Cipher import AES


class Data():
    def __init__(self):
        self.ar=PasswordHasher() # create an object to manage hashes

    def load_data(self):
        try:
            with open("data",'r') as f:
                app_data=json.load(f)
        except:
            return False
        else:
            return app_data

    def argon_hash(self, string2hash):
        hash = self.ar.hash(string2hash)
        return hash

    def check_password(self,hash, password):
        try:
            validator=self.ar.verify(hash, password)
        except Exception:
            return False
        else:
            return validator
    
    def update_data(self,data):
        try:
            with open("data", "w") as json_file:
                json.dump(data, json_file)
        except:
            return False
        else:
            return True

    def create_api_key(self):
        return secrets.token_urlsafe(64)

    def valid_keys(self, keys):
        val_keys=[]
        for k in keys:
            val_keys.append(keys[k][0])

        return val_keys

    def encrypt(self,key, data):
        data=str(data).encode()
        cipher = AES.new(key, AES.MODE_EAX)
        nonce = cipher.nonce
        ciphertext, tag = cipher.encrypt_and_digest(data)
        return ciphertext, nonce


    def decrypt(self,key, ciphertext, nonce):
        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
        plaintext = cipher.decrypt(ciphertext)
        return plaintext


    def save_data(self,data, key):
        encrypt_data=self.encrypt(key, data)
        with open("data", "wb") as f:
            for d in encrypt_data:
                f.write(d)
                f.write(b'nanan')


    def get_data(self,key):
        try:
            with open("data", "rb") as f:
                data=f.read()
            c_param=data.split(b'nanan')[0:-1]
            ciphertext=c_param[0]
            nonce=c_param[1]
            des=self.decrypt(key, ciphertext, nonce).decode().replace("'",'"')
            data=json.loads(des)
        except:
            return False
        else:
            return data
    
