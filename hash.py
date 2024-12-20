import hashlib

path = r'/Users/lufftewaffle/Documents/basic-web/Screenshot 2024-10-26 at 8.27.10 PM.png'


md5 = hashlib.md5()
sha1 = hashlib.sha1()
sha224 = hashlib.sha224()
sha256 = hashlib.sha256()
sha384 = hashlib.sha384()
sha512 = hashlib.sha512()

hash_list = [md5, sha1, sha224, sha256, sha384, sha512]

with open(path, 'rb') as open_file:
    print('hash file:')
    content = open_file.read()
    for hash in hash_list:
        hash.update(content)
        print(f"{hash.name} {hash.hexdigest()}")
    
    
    import os


really_secret_key = os.urandom(30)
print(f"Super key: {really_secret_key}")