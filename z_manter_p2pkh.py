import os
import gzip

def editar_arquivo_tsv(nome_arquivo):
    """
    Função para editar um arquivo TSV e remover todas as linhas que não começam com o número 1,
    exceto a primeira linha.

    Argumentos:
        nome_arquivo: Nome do arquivo TSV.

    Retorno:
        None.
    """

    # Leitura do arquivo TSV em modo de leitura.
    with gzip.open(nome_arquivo + '.gz', "rt") as f:
        linhas = f.readlines()

    # Lista para armazenar as linhas que serão gravadas no arquivo.
    linhas_filtradas = []

    # Adicionando "address" na primeira linha
    linhas_filtradas.append("address\t" + linhas[0])

    # Loop para iterar sobre as linhas do arquivo, exceto a primeira.
    for linha in linhas[1:]:
        # Verificação se a linha começa com o número 1.
        if linha.startswith("1"):
            # Adição da linha à lista de linhas filtradas.
            linhas_filtradas.append(linha)

    # Escrita do arquivo TSV em modo de escrita.
    with open(nome_arquivo, "w") as f:
        f.writelines(linhas_filtradas)
        
    # Remover o arquivo original .gz
    os.remove(nome_arquivo + '.gz')


# Chamada da função para editar o arquivo especificado.
nome_arquivo = "full_p2pkh.tsv"
editar_arquivo_tsv(nome_arquivo)
