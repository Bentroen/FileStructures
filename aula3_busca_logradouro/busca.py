import struct
import sys

if len(sys.argv) != 2:
	print ("Uso: python3 {} <logradouro>".format(sys.argv[0]))
	quit()


registroCEP = struct.Struct("72s72s72s72s2s8s2s")
addressColumn = 0
print ("Tamanho da Estrutura: {}".format(registroCEP.size))
with open("cep.dat","rb") as f:
	line = f.read(registroCEP.size)
	counter = 0
	while len(line) > 0:
		record = registroCEP.unpack(line)
		if sys.argv[1] in record[addressColumn].decode('latin1'):
			for i in range(0,len(record)-1):
				print (record[i].decode('latin1'))
		line = f.read(registroCEP.size)
		counter += 1
	print ("Total de Registros Lidos: {}".format(counter))

