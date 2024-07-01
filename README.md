# Ferramenta de Brute Force para Bitcoin 
Essa ferramenta destina-se para fins acadêmicos. Ela utiliza processamento por CPU para as conversões criptográficas.

## Descrição

Esta ferramenta é uma solução abrangente para a realização de ataques de força bruta no Bitcoin. Ela realiza a geração aleatória em massa de chaves privadas hexadecimais do Bitcoin, utilizando a criptografia de curvas elípticas SECP256K1.
Após gerar, a chave é convertida para endereço público no formato P2PKH e é feita uma comparação em massa, extremamente veloz, cerca de alguns milhões por segundo, comparando com a base de dados de milhões de carteiras com saldo, objetivando a colisão de alguma carteira.

## Funcionalidades

### Geração da Chave Privada

- Gera chaves privadas aleatórias em formato hexadecimal.
- Utiliza a curva elíptica SECP256K1, padrão no protocolo Bitcoin, para assegurar a validade criptográfica dessas chaves.

### Derivação da Chave Pública

- Aplica processos criptográficos para derivar a chave pública correspondente.
- Converte a chave pública para o formato P2PKH (Pay-to-PubKey-Hash), amplamente utilizado para endereços de Bitcoin.
- A geração e derivação das chaves utiliza multiprocessamento, portanto, utilizará todas os theads dispníveis da CPU.
- Já foram feitos testes com 20 núcleos e foi suportado pelo sistema.

### Comparação de Endereços

- Utiliza a biblioteca `numpy`e outras soluções, para comparação rápida e eficiente dos endereços P2PKH gerados com uma lista milhões de endereços de carteiras com saldo.
- Verifica se algum dos endereços gerados colide com um endereço existente com saldo.

## Estrutura do Projeto

```plaintext
├── 0_main.py              # Script iniciar o processo automático em looping, até achar um valor positivo
├── 1_gen_priv_p2pkh.js    # Script para geração de chaves privadas
├── 2_check_balance.py     # Script para comparação de endereços utilizando
├── y_download.py          # Script para baixar a lista mais recente de carteiras com saldo positivo
├── z_manter_p2pkh.py      # Script para manter na lista apenas as carteiras no formato p2pkh
