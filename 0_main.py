# Esse script gera um loop entre a geração de chaves privadas, conversão para chaves públicas e verificação de saldos
import subprocess
from termcolor import colored 

def main():
    scripts = [
        "1_gen_priv_p2pkh.js",  # Gera as chaves privadas em hexadecimal e converte em chave pública no formato p2pkh legacy
        "2_check_balance.py"  # Compara as chaves p2pkh com a lista atualizada de wallets com saldo
    ]

    total_loops = 0

    while True:
        total_loops += 1
        total_keys_checked = total_loops * 1000000
        print(colored(f"Chaves verificadas: {total_keys_checked}", "green"))

        for index, script in enumerate(scripts):
            print(f"Executando o script: {script}")

            # Execute o script Python ou JavaScript conforme necessário
            if script.endswith('.js'):
                process = subprocess.Popen(["node", script], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            else:
                process = subprocess.Popen(["python", script], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True) # Caso esteja em distro linux, altere para python3

            # Exiba a saída enquanto o script está em execução
            for line in process.stdout:
                print(line.strip())

            # Aguarde o término do script
            process.communicate()

            # Verifique a última linha da saída do último script
            if index == len(scripts) - 1:
                last_line = line.strip()  # Última linha capturada antes do término do script
                if last_line != "Total de endereços com saldo: 0":
                    print(colored("Condição de parada atingida. Encerrando o loop.", "red"))
                    return
                else:
                    print("Última linha indica que o script continua em execução. Continuando o loop.")
            else:
                print("Executando próximo script.")

if __name__ == "__main__":
    main()

    # Caso o loop seja interrompido, quer dizer que encontrou saldo. Se isso acontecer, basta verificar em qual arquivo a chave pública se encontra
    # Por exemplo, foi encontrado saldo, salvo no balance.txt, dentro da carteira 1xxx, que se encontra no arquivo pub_keys_compressed_50, portanto, a sua chave privada estará no arquivo e linhas correspondentes.
    # Para importar a carteira, basta inserir a chave privada em hexadecimal no script da conv_key_to_WIF.py
    # Todo script funciona Offline, a exceto o download das carteiras com saldo atualizada.
