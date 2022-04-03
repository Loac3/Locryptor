import hashlib, os
from getpass4 import getpass

password = getpass("Enter Encryption Password: ")
verify_password = getpass("Verify Password: ")
if password == verify_password:
    print("Password Matches")

    new_src = open('src.py', 'r').read().replace("REPLACE_WITH_HASH", hashlib.sha512(password.encode()).hexdigest())

    with open('LOCRYPTOR.py', 'w') as f:
        f.write(new_src)

    os.system('pyarmor pack --clean -e "--onefile " LOCRYPTOR.py')

    os.remove('LOCRYPTOR.py')
    print("Done")
else:
    print("Passwords do not match")
    input()
    
