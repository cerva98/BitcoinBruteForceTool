# Ferramenta de Brute Force para Bitcoin com Fins Acadêmicos

## Descrição

Esta ferramenta é uma solução abrangente para a realização de ataques de força bruta no Bitcoin, com foco em fins acadêmicos. Ela realiza a geração aleatória de chaves privadas hexadecimais do Bitcoin, utilizando a criptografia de curvas elípticas SECP256K1.

## Funcionalidades

### Geração da Chave Privada

- Gera chaves privadas aleatórias em formato hexadecimal.
- Utiliza a curva elíptica SECP256K1, padrão no protocolo Bitcoin, para assegurar a validade criptográfica dessas chaves.

### Derivação da Chave Pública

- Aplica processos criptográficos para derivar a chave pública correspondente.
- Converte a chave pública para o formato P2PKH (Pay-to-PubKey-Hash), amplamente utilizado para endereços de Bitcoin.

### Comparação de Endereços

- Utiliza a biblioteca `numpy` para comparação rápida e eficiente dos endereços P2PKH gerados com uma lista de endereços de carteiras com saldo.
- Verifica se algum dos endereços gerados colide com um endereço existente com saldo.

## Estrutura do Projeto

```plaintext
├── 0_main.py    # Script iniciar o processo automático em looping, até achar um valor positivo
├── 1_gen_priv_p2pkh.js    # Script para geração de chaves privadas
├── 2_check_balance.py     # Script para comparação de endereços utilizando numpy
├── y_download.py          # Script para baixar a lista de carteiras com saldo positivo.
├── z_manter_p2pkh.py       # Script para manter na lista apenas as carteiras no formato p2pkh
