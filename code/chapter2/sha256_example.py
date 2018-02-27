from Crypto.Hash import SHA256

hash_object = SHA256.new(data=b'First')
print(hash_object.hexdigest())

hash_object.update(b'd')
print(hash_object.hexdigest())
