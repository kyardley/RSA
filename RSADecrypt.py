# OVERVIEW: This script uses the RSA private key to decrypt an image; this script won't work initially since the RSAEncrypt script references the TA's public key, so only their private key can decrypt the message. However, once you have generated the encrypted_img.jpg with the TA's public key, feel free to replace the key paths to reference your own public key in the RSAEncrypt.py script and play around with the scripts
# PLEASE BEWARE: if the scripts are run more than once, the encrypted_img.jpg and decrypted_img.jpg files will be overriden so please verify you submit the file that's been encrypted with the TA's public key before playing around with the scripts
# SRC: https://medium.com/@ismailakkila/black-hat-python-encrypt-and-decrypt-with-rsa-cryptography-bd6df84d65bc

# import needed libraries
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
import zlib

# decryption function
def decrypt_blob(encrypted_blob, private_key):

    # import the Private Key and use for decryption using PKCS1_OAEP
    rsakey = RSA.importKey(private_key)
    rsakey = PKCS1_OAEP.new(rsakey)

    # base 64 decode the data
    encrypted_blob = base64.b64decode(encrypted_blob)

    # in determining the chunk size, determine the private key length used in bytes.
    # the data will be in decrypted in chunks
    chunk_size = 512
    offset = 0
    decrypted = bytes("".encode('utf-8'))

    # keep loop going as long as we have chunks to decrypt
    while offset < len(encrypted_blob):
        # the chunk
        chunk = encrypted_blob[offset: offset + chunk_size]

        # append the decrypted chunk to the overall decrypted file
        decrypted += rsakey.decrypt(chunk)

        # increase the offset by chunk size
        offset += chunk_size

    # return the decompressed decrypted data
    return zlib.decompress(decrypted)

# use the private key for decryption
fd = open("private_key.pem", "rb")
private_key = fd.read()
fd.close()

# our candidate file to be decrypted
fd = open("encrypted_img.jpg", "rb")
encrypted_blob = fd.read()
fd.close()

# write the decrypted contents to a file
fd = open("decrypted_img.jpg", "wb")
fd.write(decrypt_blob(encrypted_blob, private_key))

# write completion message to console
print('Stored decrypted image to ' + fd.name)
fd.close()