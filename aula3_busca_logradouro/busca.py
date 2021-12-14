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
			data = [record[i].decode('latin1').strip() for i in range(len(record))]
			print("{:<32.32} {:<24.24} {:<24.24} {:<20.20} {:<4} {}".format(*data))
		line = f.read(registroCEP.size)
		counter += 1
	print ("Total de Registros Lidos: {}".format(counter))

