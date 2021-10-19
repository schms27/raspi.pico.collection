from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import json
import os
import base64

class PasswordManager:
    def generate_encryption_key(self):
        return Fernet.generate_key()

    def encrypt_file(self, filepath, password):
        basepath = os.path.dirname(filepath)
        with open(filepath, "rb") as file:
            key, salt = self.get_key_from_password(password)
            f = Fernet(key)

            # read all file data
            file_data = file.read()
            file.close()
            # encrypt data
            encrypted_data = f.encrypt(file_data)

            # write the encrypted file
            with open(os.path.join(basepath,"passwords.encrypted"), "wb") as file:
                file.write(encrypted_data)
            # write the salt file
            with open(os.path.join(basepath,"salt"), "wb") as file:
                file.write(salt)
            
            os.remove(filepath)
            print(f"Encrypted File '{filepath}' using key '{key}'")

    def decrypt_file(self, filepath, password):
        basepath = os.path.dirname(filepath)
        with open(os.path.join(basepath, "salt"), "rb") as file:
            salt = file.read()
            key, salt = self.get_key_from_password(password, salt)
            f = Fernet(key)
            with open(filepath, "rb") as file:
                # read the encrypted data
                encrypted_data = file.read()
                # decrypt data
                self.decrypted_data = f.decrypt(encrypted_data)

    def get_password(self, name):
        if self.decrypted_data is not None:
            json_data = json.loads(self.decrypted_data.decode('utf-8'))
            return json_data[name]

    def get_key_from_password(self, password, salt=os.urandom(16)):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        return (base64.urlsafe_b64encode(kdf.derive(password.encode('ascii'))), salt)