"use strict";

const crypto = require('crypto');  // Importa o módulo crypto para operações criptográficas
const fs = require('fs');  // Importa o módulo fs para manipulação de arquivos
const CoinKey = require('coinkey');  // Importa o módulo coinkey para geração de chaves de criptomoeda
const { fork } = require('child_process');  // Importa a função fork do módulo child_process para criar processos filhos
const os = require('os');  // Importa o módulo os para interagir com o sistema operacional

const startTime = process.hrtime();  // Marca o início da execução do script

const criarPastasSeNaoExistirem = () => {
    const pastas = ['priv_hex', 'pub_key_com'];
    pastas.forEach(pasta => {
        if (!fs.existsSync(pasta)) {  // Verifica se a pasta já existe
            fs.mkdirSync(pasta);  // Cria a pasta se não existir
            console.log(`Pasta '${pasta}' criada.`);
        }
    });
};

const processarESalvarLote = (loteChavesPrivadas, loteEnderecosPublicos, loteNumero) => {
    return new Promise((resolve, reject) => {
        fs.writeFile(`priv_hex/chaves_privadas_${loteNumero}.txt`, loteChavesPrivadas.join('\n'), { flag: 'w' }, (err) => {
            if (err) {
                reject(`Erro ao salvar chaves privadas do lote ${loteNumero}: ${err}`);
            } else {
                console.log(`Chaves privadas geradas do lote ${loteNumero} salvas.`);
                resolve();
            }
        });
    }).then(() => {
        return new Promise((resolve, reject) => {
            fs.writeFile(`pub_key_com/pub_keys_compressed_${loteNumero}.txt`, loteEnderecosPublicos.join('\n'), { flag: 'w' }, (err) => {
                if (err) {
                    reject(`Erro ao salvar endereços públicos do lote ${loteNumero}: ${err}`);
                } else {
                    console.log(`Endereços públicos gerados do lote ${loteNumero} salvos.`);
                    resolve();
                }
            });
        });
    });
};

const numCarteiras = 1000000;  // Número total de carteiras a serem geradas
const tamanhoLote = 10000;  // Tamanho de cada lote de geração de carteiras

criarPastasSeNaoExistirem();  // Chama a função para criar pastas se não existirem

async function gerarLotes() {
    const numNucleos = os.cpus().length;  // Obtém o número de núcleos do processador
    const numLotesPorNucleo = Math.ceil(numCarteiras / (tamanhoLote * numNucleos));  // Calcula o número de lotes por núcleo

    const promises = [];

    for (let i = 0; i < numNucleos; i++) {
        const numInicio = i * numLotesPorNucleo * tamanhoLote;  // Calcula o número de início do lote para o núcleo atual
        const numFim = Math.min((i + 1) * numLotesPorNucleo * tamanhoLote, numCarteiras);  // Calcula o número de fim do lote para o núcleo atual

        const childProcess = fork(__filename);  // Cria um processo filho para cada núcleo
        const promise = new Promise((resolve, reject) => {
            childProcess.on('message', (message) => {
                if (message === 'success') {
                    resolve();
                } else {
                    reject(message);
                }
            });

            childProcess.send({ numInicio, numFim });  // Envia a mensagem para o processo filho com o número de início e fim do lote
        });

        promises.push(promise);
    }

    return Promise.all(promises);
}

if (process.send) {  // Verifica se o script está sendo executado como um processo filho
    process.on('message', async ({ numInicio, numFim }) => {  // Define um listener para mensagens do processo pai
        try {
            for (let i = numInicio; i < numFim; i += tamanhoLote) {  // Loop para gerar lotes de carteiras
                const loteChavesPrivadas = [];
                const loteEnderecosPublicos = [];

                for (let j = i; j < i + tamanhoLote && j < numCarteiras; j++) {  // Loop para gerar chaves privadas e públicas
                    const chavePrivadaHex = crypto.randomBytes(32).toString('hex');  // Gera uma chave privada aleatória
                    loteChavesPrivadas.push(chavePrivadaHex);  // Adiciona a chave privada ao lote

                    const ck = new CoinKey(Buffer.from(chavePrivadaHex, 'hex'));  // Cria uma instância de CoinKey a partir da chave privada
                    ck.compressed = true;  // Define a compressão da chave pública como verdadeira
                    loteEnderecosPublicos.push(ck.publicAddress);  // Adiciona o endereço público ao lote
                }

                await processarESalvarLote(loteChavesPrivadas, loteEnderecosPublicos, Math.ceil((i + 1) / tamanhoLote));  // Processa e salva o lote
            }

            process.send('success');  // Envia uma mensagem de sucesso para o processo pai
        } catch (error) {
            process.send(error);  // Envia uma mensagem de erro para o processo pai em caso de falha
        }
    });
} else {  // Se o script não estiver sendo executado como um processo filho (processo pai)
    gerarLotes().then(() => {  // Chama a função para gerar lotes de carteiras
        const endTime = process.hrtime(startTime);  // Marca o fim da execução do script
        const tempoExecucao = (endTime[0] + endTime[1] / 1e9).toFixed(2);  // Calcula o tempo de execução
        console.log(`Tempo total de execução: ${tempoExecucao} segundos`);  // Exibe o tempo total de execução
        process.exit(); // Encerra a execução do processo pai
    }).catch((error) => {
        console.error(error);  // Exibe erros na geração dos lotes de carteiras
    });
}
