import hashlib

path = r'/Users/lufftewaffle/Documents/basic-web/Screenshot 2024-10-26 at 8.27.10 PM.png'


# with open(path, 'rb') as open_file:
#     content = open_file.read()
#     md5 = hashlib.md5()
#     sha1 = hashlib.sha1()
#     sha224 = hashlib.sha224()
#     sha256 = hashlib.sha256()
#     sha384 = hashlib.sha384()
#     sha512 = hashlib.sha512()
    
#     md5.update(content)
#     sha1.update(content)
#     sha224.update(content)
#     sha256.update(content)
#     sha384.update(content)
#     sha512.update(content)
    
#     print(f"{md5.name} {md5.hexdigest()}")
#     print(f"{sha1.name} {sha1.hexdigest()}")
#     print(f"{sha224.name} {sha224.hexdigest()}")
#     print(f"{sha256.name} {sha256.hexdigest()}")
#     print(f"{sha384.name} {sha384.hexdigest()}")
#     print(f"{sha512.name} {sha512.hexdigest()}")

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
    