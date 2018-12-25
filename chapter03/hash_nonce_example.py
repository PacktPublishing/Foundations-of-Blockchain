# example of iterating a nonce in a hashing algorithm's input

from __future__ import print_function
from Crypto.Hash import SHA256

text = "I am Satoshi Nakamoto"

# iterate nonce from 0 to 19
for nonce in range(20):

    # add the nonce to the end of the text
    input_data = text + str(nonce)

    # calculate the SHA-256 hash of the input (text+nonce)
    hash_data = SHA256.new(input_data.encode()).hexdigest()

    # show the input and hash result
    print((input_data + '=>' + hash_data)[:64] + "...")
