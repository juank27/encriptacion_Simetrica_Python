import cryptography
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

#Genera llave privada
private_key = rsa.generate_private_key(
   public_exponent=65537,
   key_size=2048,
   backend=default_backend()
)
public_key = private_key.public_key()

# private key
serial_private = private_key.private_bytes(
   encoding=serialization.Encoding.PEM,
   format=serialization.PrivateFormat.PKCS8,
   encryption_algorithm=serialization.NoEncryption()
)
with open('private_noshare.pem', 'wb') as f: f.write(serial_private)

# public key
serial_pub = public_key.public_bytes(
   encoding=serialization.Encoding.PEM,
   format=serialization.PublicFormat.SubjectPublicKeyInfo
)
with open('public_shared.pem', 'wb') as f: f.write(serial_pub)

#########      Private device only    ##########
def read_private (filename = "private_noshare.pem"):
   with open(filename, "rb") as key_file:
      private_key = serialization.load_pem_private_key(
         key_file.read(),
         password=None,
         backend=default_backend()
      )
   return private_key

######### Public (shared) device only ##########
def read_public (filename = "public_shared.pem"):
   with open("public_shared.pem", "rb") as key_file:
      public_key = serialization.load_pem_public_key(
         key_file.read(),
         backend=default_backend()
      )
   return public_key

# make sure the following are imported
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
######### Public (shared) device only #########
data = [b'My secret weight', b'My secret id']
public_key = read_public()
open('test.txt', "wb").close() # clear file
for encode in data:
   encrypted = public_key.encrypt(
      encode,
      padding.OAEP(
         mgf=padding.MGF1(algorithm=hashes.SHA256()),
         algorithm=hashes.SHA256(),
         label=None
      )
   )
   with open('test.txt', "ab") as f: f.write(encrypted)

#########      Private device only    ##########
read_data = []
private_key = read_private()
with open('test.txt', "rb") as f:
   for encrypted in f:
      read_data.append(
         private_key.decrypt(
            encrypted,
            padding.OAEP(
               mgf=padding.MGF1(algorithm=hashes.SHA256()),
               algorithm=hashes.SHA256(),
               label=None
            )
         )
      )
      print(read_data)
print(read_data)
read_data = [b'My secret weight', b'My secret id']