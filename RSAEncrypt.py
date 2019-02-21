# OVERVIEW: This script uses the TA's RSA public key to encrypt an image (by chunks); to grade the assignment, the TAs will use their private key and the decrypt script to decrypt the image
# THINGS TO CHANGE: modify the image passed into the function; see the ### CHANGE IMAGE HERE ### comment to know where to modify the script; verify the image is in the /Documents/RSA/ directory (in other words, the image needs to be in the same directory as this script)
# SRC: https://medium.com/@ismailakkila/black-hat-python-encrypt-and-decrypt-with-rsa-cryptography-bd6df84d65bc

# import needed libraries
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import zlib
import base64

# encryption function
def encrypt_blob(blob, public_key):
    # import the Public Key and use for encryption using PKCS1_OAEP
    rsa_key = RSA.importKey(public_key)
    rsa_key = PKCS1_OAEP.new(rsa_key)

    # compress the data (img) first
    blob = zlib.compress(blob)

    # the data will be in encrypted in chunks
    chunk_size = 470
    offset = 0
    end_loop = False
    encrypted =  bytes("".encode('utf-8'))

    while not end_loop:
        # the chunk
        chunk = blob[offset:offset + chunk_size]

        # if the data chunk is less then the chunk size, then we need to add
        # padding with " ". This indicates the we reached the end of the file
        # so we end loop here
        if len(chunk) % chunk_size != 0:
            end_loop = True
            chunk += bytes((" " * (chunk_size - len(chunk))).encode('utf-8'))

        # append the encrypted chunk to the overall encrypted file
        encrypted += rsa_key.encrypt(chunk)

        # increase the offset by chunk size
        offset += chunk_size

    # base 64 encode the encrypted file
    return base64.b64encode(encrypted)

# use the public key for encryption
### THE PUBLIC KEY PATH CAN BE MODIFIED TO YOUR PUBLIC KEY AFTER THE IMAGE ENCODED WITH THE TA's PUBLIC KEY HAS BEEN SUBMITTED ###
fd = open("TA_public_key.pem", "rb")
public_key = fd.read()
fd.close()

# image to be encrypted... the "rootbeer.jpg" should be changed to the filename of your image
### CHANGE IMAGE HERE ###
fd = open("rootbeer.jpg", "rb")
unencrypted_blob = fd.read()
fd.close()

# call function
encrypted_blob = encrypt_blob(unencrypted_blob, public_key)

# write the encrypted contents to a file (encrypted_img.jpg)
### VERIFY THE IMAGE SUBMITTED WITH YOUR HOMEWORK IS NAMED encrypted_img.jpg ###
fd = open("encrypted_img.jpg", "wb")
fd.write(encrypted_blob)

# write completion message to console
print('Stored encrypted image to ' + fd.name)
fd.close()