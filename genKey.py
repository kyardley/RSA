#****Dependencies****
#Python3
#Python Module: pycrypto (pip3 install pycrypto)
from Crypto.PublicKey import RSA

#Generate a public/private key pair using 4096 bits key length (512 bytes)
new_key = RSA.generate(4096, e=65537)

#The private key in PEM format
private_key = new_key.exportKey("PEM")

#The private key in PEM formate
public_key = new_key.publickey().exportKey("PEM")

#create and save private_key.pem
fd = open("private_key.pem", "wb")
fd.write(private_key)
print("Saving Private Key in private_key.pem")
fd.close()

#create and save public_key.pem
fd = open("public_key.pem", "wb")
fd.write(public_key)
print("Saving Public Key in public_key.pem")
fd.close()

