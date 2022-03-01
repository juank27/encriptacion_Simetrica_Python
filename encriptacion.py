from cryptography.fernet import Fernet

#generar clave
def generar_clave ():
   clave = Fernet.generate_key()
   with open("clave.key", "wb") as archivo_clave:
      archivo_clave.write(clave)
      #archivo_clave.close()

#cargar la clave
def cargar_clave():
   return open("clave.key", "rb").read()


def run():
   # generar clave
	generar_clave()
	# cargar una clave
	clave = cargar_clave()
	# encriptar un mensaje
	texto = input("Mensaje a encriptar : ")
	mensaje = texto.encode()
	f = Fernet(clave)
	# encriptar mensaje
	encriptado = f.encrypt(mensaje)
	print(encriptado)
	mensaje = desencriptado(f, encriptado)
	print(mensaje)

# desencriptado
def desencriptado (a,encript):
   salida = a.decrypt(encript)
   return salida

if __name__ == '__main__':
   run()