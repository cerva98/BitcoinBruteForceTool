import requests
import gzip
import shutil
import os
from tqdm import tqdm
import subprocess

def baixar_arquivo(url, nome_arquivo, callback=None):
    """
    Função para baixar um arquivo a partir de uma URL.

    Argumentos:
        url: URL do arquivo a ser baixado.
        nome_arquivo: Nome do arquivo para salvar localmente.
        callback: Função de retorno de chamada para monitorar o progresso do download (opcional).

    Retorno:
        None.
    """
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        tamanho_total = int(r.headers.get('content-length', 0))
        with open(nome_arquivo, 'wb') as f:
            with tqdm(total=tamanho_total, unit='B', unit_scale=True, unit_divisor=1024) as pbar:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        pbar.update(len(chunk))
                        if callback:
                            callback(len(chunk))


def extrair_arquivo_gz(nome_arquivo_gz, nome_arquivo_destino):
    """
    Função para extrair um arquivo .gz.

    Argumentos:
        nome_arquivo_gz: Nome do arquivo .gz a ser extraído.
        nome_arquivo_destino: Nome do arquivo para salvar o conteúdo extraído.

    Retorno:
        None.
    """
    with gzip.open(nome_arquivo_gz, 'rb') as f_in:
        with open(nome_arquivo_destino, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)


# Função para monitorar o progresso do download
def progresso_download(tamanho_atual):
    pbar.update(tamanho_atual)


# Baixar e extrair o arquivo
print("Baixando arquivo full_1.tsv.gz...")
baixar_arquivo("http://addresses.loyce.club/Bitcoin_addresses_LATEST.txt.gz", "full_1.tsv.gz")

print("Extraindo arquivo full_1.tsv...")
extrair_arquivo_gz("full_p2pkh.tsv.gz", "full_p2pkh.tsv")

print("O arquivo foi baixado e copiado com sucesso!")

