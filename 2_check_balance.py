import os  # Importa o módulo os para interagir com o sistema operacional
import pandas as pd  # Importa o módulo pandas para manipulação de dados
import numpy as np  # Importa o módulo numpy para operações numéricas
from tqdm import tqdm  # Importa o módulo tqdm para exibir barras de progresso

# Define os nomes dos arquivos
arquivo_pub_keys_com = "pub_key_com/pub_keys_compressed_"  # Arquivo contendo as chaves públicas
arquivo_wall_with_balance_com = "full_p2pkh.tsv"  # Arquivo contendo endereços com saldo
arquivo_balance = "balance.txt"  # Arquivo de saída para endereços com saldo

# Função para verificar se um endereço está em uma lista
def verificar_endereco(endereco, enderecos_set):
    return endereco in enderecos_set

# Ler os endereços do arquivo .tsv
def ler_enderecos(arquivo):
    with open(arquivo, "r") as f:
        enderecos_addr = pd.read_csv(f, delimiter="\t", chunksize=10000)
        # Concatenar os chunks em um único DataFrame
        enderecos_addr = pd.concat(enderecos_addr)
    return set(enderecos_addr["address"])

# Processar endereços com saldo
def processar_enderecos(arquivo_pub_keys, arquivo_addr_base):
    enderecos_set = ler_enderecos(arquivo_addr_base)  # Obtém os endereços do arquivo base
    enderecos_com_saldo = []  # Lista para armazenar endereços com saldo

    # Itera sobre os arquivos de chaves públicas
    for i in range(1, 101):
        arquivo_pub_keys_atual = arquivo_pub_keys + str(i) + ".txt"  # Nome do arquivo atual
        try:
            with open(arquivo_pub_keys_atual, "r") as f:
                enderecos_pub_keys = f.readlines()  # Lê as chaves públicas do arquivo
        except FileNotFoundError:
            print(f"Arquivo {arquivo_pub_keys_atual} não encontrado. Finalizando análise.")
            break

        # Processa os endereços com tqdm
        print(f"Comparando {arquivo_pub_keys_atual} com {arquivo_addr_base}")
        for endereco in tqdm(enderecos_pub_keys):
            endereco = endereco.strip()  # Remove o caractere de nova linha
            if verificar_endereco(endereco, enderecos_set):
                enderecos_com_saldo.append(endereco)  # Adiciona endereços com saldo à lista

    return enderecos_com_saldo

# Processar endereços pub_keys_com
enderecos_com_saldo_total = processar_enderecos(arquivo_pub_keys_com, arquivo_wall_with_balance_com)

# Salvar os endereços com saldo no arquivo balance.txt
with open(arquivo_balance, "w") as f:
    for endereco in enderecos_com_saldo_total:
        f.write(endereco + "\n")  # Escreve cada endereço com saldo no arquivo

# Mensagem de sucesso
print(f"\nEndereços com saldo salvos em {arquivo_balance}")
print(f"\nTotal de endereços com saldo: {len(enderecos_com_saldo_total)}")
