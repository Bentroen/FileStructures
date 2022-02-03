from enum import IntEnum
import struct


FORMATO_ENTRADA = struct.Struct("6s7s6s8s2s1s4s8s")

TAMANHO_ENTRADA = FORMATO_ENTRADA.size


class Sinasc(IntEnum):
    # fmt: off
    COD_MUN_NASC = 0    # Código do município de nascimento
    COD_ESTAB = 1       # Código do estabelecimento
    COD_MUN_RES = 2     # Código do município de residência
    DT_NASC = 3         # Data de nascimento (DDMMAAAA)
    SEMA_GEST = 4       # Número de semanas de gestação
    SEXO = 5            # Sexo (0=não informado, 1=masculino, 2=feminino)
    PESO = 6            # Peso (gramas)
    DT_NASC_MAE = 7     # Data de nascimento da mãe (DDMMAAAA)
    # fmt: on


def main():

    with open("sinasc-sp-2018.dat", "rb") as f:

        # 1) Verificar o tamanho do arquivo em bytes
        f.seek(0, 2)
        tamanho = f.tell()
        f.seek(0)
        print(f"1) O arquivo tem {tamanho} bytes")

        # 2) Verificar o tamanho de cada registro
        tamanho_registro = TAMANHO_ENTRADA
        print(f"2) Cada registro tem {tamanho_registro} bytes")

        # 3) Verificar o nº de entradas
        num_registros = tamanho // TAMANHO_ENTRADA
        print(f"3) O arquivo tem {num_registros} registros")

        # 4) Copiar registros ocorridos na capital
        registros_capital = []
        while True:
            bytes = f.read(TAMANHO_ENTRADA)
            if not bytes:  # EOF
                break
            dados = FORMATO_ENTRADA.unpack(bytes)
            dados_str = [valor.decode("latin-1") for valor in dados]
            if dados_str[Sinasc.COD_MUN_NASC] == "355030":
                registros_capital.append(dados)

        with open("sinasc-sp-capital-2018.dat", "wb") as fp:
            for registro in registros_capital:
                bytes = FORMATO_ENTRADA.pack(*registro)
                fp.write(bytes)
        print("4) Arquivo sinasc-sp-capital-2018.dat criado")
        f.seek(0)

        # 5) Verificar quantas meninas nasceram em Santos em 2018
        meninas_nasc_santos_2018 = 0
        while True:
            bytes = f.read(TAMANHO_ENTRADA)
            if not bytes:  # EOF
                break
            dados = FORMATO_ENTRADA.unpack(bytes)
            dados_str = [valor.decode("latin-1") for valor in dados]

            if (
                dados_str[Sinasc.COD_MUN_NASC] == "354850"
                and dados_str[Sinasc.SEXO] == "2"
                and dados_str[Sinasc.DT_NASC][4:] == "2018"
            ):
                meninas_nasc_santos_2018 += 1
        print(
            f"5) O número de meninas nascidas em Santos em 2018 é {meninas_nasc_santos_2018}"
        )
        f.seek(0)

        # 6) Verificar quantos bebês nasceram com baixo peso em Campinas em 2018
        nasc_baixopeso_campinas_2018 = 0
        while True:
            bytes = f.read(TAMANHO_ENTRADA)
            if not bytes:  # EOF
                break
            dados = FORMATO_ENTRADA.unpack(bytes)
            dados_str = [valor.decode("latin-1") for valor in dados]

            if (
                dados_str[Sinasc.COD_MUN_NASC] == "350950"
                and int(dados_str[Sinasc.PESO]) < 2500
                and dados_str[Sinasc.DT_NASC][4:] == "2018"
            ):
                nasc_baixopeso_campinas_2018 += 1
        print(
            f"6) O número de bebês nascidos em Campinas com baixo peso em 2018 é {nasc_baixopeso_campinas_2018}"
        )
        f.seek(0)

        # 7) Ordenar arquivo
        registros = []
        while True:
            bytes = f.read(TAMANHO_ENTRADA)
            if not bytes:  # EOF
                break
            dados = FORMATO_ENTRADA.unpack(bytes)
            registros.append(tuple(valor.decode("latin-1") for valor in dados))

        registros.sort(
            key=lambda x: int(x[Sinasc.COD_ESTAB]) if x[Sinasc.COD_ESTAB].strip() else 0
        )  # Registros vazios são tratados como 0 para fins de ordenação

        with open("sinasc-sp-2018-ordenado.dat", "wb") as fp:
            for registro in registros:
                dados_bytes = (valor.encode("latin-1") for valor in registro)
                bytes = FORMATO_ENTRADA.pack(*dados_bytes)
                fp.write(bytes)
        print("7) Arquivo sinasc-sp-2018-ordenado.dat criado")
        f.seek(0)

    with open("sinasc-sp-2018-ordenado.dat", "rb") as f:
        # 8) Contar número de nascimentos por estabelecimento
        estab_anterior = None
        nascimentos_por_estab = 0
        cont_estab = 0
        print("8) Número de nascimentos por estabelecimento:")
        while True:
            bytes = f.read(TAMANHO_ENTRADA)
            if not bytes:  # EOF
                break
            dados = FORMATO_ENTRADA.unpack(bytes)

            estab_atual = dados[Sinasc.COD_ESTAB].decode("latin-1")
            if estab_atual.strip() == "":
                estab_atual = "Não informado"

            if estab_anterior and estab_atual != estab_anterior:
                cont_estab += 1
                if cont_estab <= 10:  # Imprime apenas os 10 primeiros estabelecimentos
                    print(f"   | {estab_anterior}: {nascimentos_por_estab}")
                nascimentos_por_estab = 0

            nascimentos_por_estab += 1
            estab_anterior = estab_atual

        print("   | ...")

    # 9) Obter nº de estabelecimentos
    print(f"9) Nº de estabelecimentos: {cont_estab}")


if __name__ == "__main__":
    main()
