from cryptography.fernet import Fernet


# key = Fernet.generate_key()

# with open('my_key.key', 'wb') as myKey:
#     myKey.write(key)
    
    
with open('my_key.key','rb') as myKey:
    key = myKey.read()
    
print(key)

f = Fernet(key)
with open('code.odt', 'rb') as og_file:
    original = og_file.read()
    
encrypted = f.encrypt(original)


with open('enc_doc.odt', 'wb') as enc_file:
    enc_file.write(encrypted)
