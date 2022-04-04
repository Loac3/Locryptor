from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import os, base64, hashlib
from getpass4 import getpass
import __main__ as main
curr_file_name = "LOCRYPTOR"
class console:
    error = lambda m: print(f"\033[91m[ERR]\033[0m\t{m}")
    input = lambda m: input(f"\033[94m[INPT]\033[0m\t{m}")
    info = lambda m: print(f"\033[92m[INFO]\033[0m\t{m}")
    warn = lambda m: print(f"\033[93m[WARN]\033[0m\t{m}")
    password = lambda m: getpass(f"\033[95m[PASS]\033[0m\t{m}")

PW_HASH = "REPLACE_WITH_HASH"

derive_from_hash = PBKDF2HMAC(
    algorithm=hashes.SHA512(),
    salt=b'2\x93\x1e\xe1\x01\x13\xf7O\xf9\xba\xa1c\xd0\xd3"\xdb',
    length=32,
    iterations=390000,
    backend=default_backend()

)

gen_key = lambda: base64.urlsafe_b64encode(derive_from_hash.derive(bytes(PW_HASH, "utf-8")))

def check_access():
    inputted_pw = console.password("Enter Encryption Password: ")
    if hashlib.sha512(inputted_pw.encode()).hexdigest() != PW_HASH:
        console.error("Incorrect Password")
        console.info("Closing Program.")
        input()
        exit()
        return "incorrect"
    
    if hashlib.sha512(inputted_pw.encode()).hexdigest() == PW_HASH:
        return "correct"

def walk_files():
    files = []
    file_names = list(os.walk(os.getcwd()))
    for dir in file_names:
        for file in dir[2]:
            files.append(dir[0] + "/" + file)

    return files

def encrypt_all():
        if check_access() == "correct":
            console.info("Password Correct")
            key = gen_key()
            console.info("Generated Key")
            for unenc_file in is_encrypted(walk_files(), key):
                if curr_file_name not in unenc_file:
                    try:
                        with open(unenc_file, "rb") as f:
                            data = f.read()
                            fernet = Fernet(key)
                            encrypted = fernet.encrypt(data)
                            with open(unenc_file, "wb") as f:
                                f.write(encrypted)
                                console.info(f"Encrypted {unenc_file}")
                    except:
                        console.error(f"Couldn't Encrypt {unenc_file}")
            
            console.info("Encryption Complete")

def decrypt_all():
    if check_access() == "correct":
        console.info("Password Correct")
        key = gen_key()
        console.info("Generated Key")
        for enc_file in is_unencrypted(walk_files(), key):
            if curr_file_name not in enc_file:
                try:
                    console.info(f"Decrypting {enc_file}")
                    with open(enc_file, "rb") as f:
                        data = f.read()
                        fernet = Fernet(key)
                        decrypted = fernet.decrypt(data)
                        with open(enc_file, "wb") as f:
                            f.write(decrypted)
                except:
                    console.error(f"Couldn't Decrypt {enc_file}")

        
        console.info("Decryption Complete")


def is_encrypted(lst, ke):
    unencrypted_files = []
    for file in lst:
        try:
            Fern = Fernet(ke)
            data = bytes(open(file, "rb").read())
            Fern.decrypt(data, None)
        except InvalidToken:
            unencrypted_files.append(file)

    return unencrypted_files

def is_unencrypted(lst, ke):
    encrypted_files = []
    for file in lst:
        try:
            Fern = Fernet(ke)
            data = bytes(open(file, "rb").read())
            Fern.decrypt(data, None)
            encrypted_files.append(file)
        except InvalidToken:
            pass

    return encrypted_files

choice = console.input("""
[1] Encrypt All Files
[2] Decrypt All Files


[>] """)

if choice == "1":
        encrypt_all()

if choice == "2":
        decrypt_all()
