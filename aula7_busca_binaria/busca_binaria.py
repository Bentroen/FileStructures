import sys
import struct


TAMANHO_ENTRADA = 300

formato_entrada = struct.Struct("72s72s72s72s2s8s2s")


def busca_binaria(cep_buscado: str):

     with open('cep_ordenado.dat', 'rb') as f:
          
          # Verificar o tamanho do arquivo
          f.seek(0, 2)
          tamanho = f.tell()
          entradas = tamanho // TAMANHO_ENTRADA
          f.seek(0)

          cep_elemento = None
          inicio = 0
          fim = entradas - 1
          while True:
               if fim >= inicio:
                    meio = (inicio + fim) // 2
                    f.seek(meio * 300)
                    bytes_entrada = f.read(300)
                    dados_entrada = formato_entrada.unpack(bytes_entrada)
                    dados_str = tuple(i.decode('latin1').strip() for i in dados_entrada[:-1])
                    cep_elemento = dados_str[5]
                    print(f"Buscando CEP {cep_elemento} (entrada nº {meio + 1})")
                    if cep_elemento == cep_buscado:
                         return dados_str
                    elif cep_elemento > cep_buscado:
                         fim = meio - 1
                    else:
                         inicio = meio + 1
               else:
                    return None


if __name__ == "__main__":
     if len(sys.argv) != 2:
          print(f"Uso: python {sys.argv[0]} <cep>")
          exit()
     
     cep = sys.argv[1]
     resultado = busca_binaria(cep)

     print("\n=================================")
     if not resultado:
          print(f"O CEP {cep} não foi encontrado")
     else:
          print('\n'.join(resultado))
     print("=================================\n")
