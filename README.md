
# MiniGit - Estrutura de Dados

## Medição de leitura e escrita

| Commits | Passos do commitar | Passos do log |
|---|---:|---:|
| 10 | 2 | 10 |
| 100 | 2 | 100 |
| 1000 | 2 | 1000 |

## 1. Leitura x escrita

O commitar sempre gasta 2 passos porque precisa criar o commit e atualizar o ponteiro da branch. Já o log precisa percorrer os commits existentes, por isso seu custo aumenta conforme o histórico cresce.

## 2. Mensagem e buscar

O método mensagem gasta apenas 1 passo porque utiliza o dicionário para encontrar diretamente o commit pela chave. Já buscar precisa olhar as mensagens uma por uma, pois procura um texto dentro dos valores.

## 3. Merge e grafo

O merge possui dois pais porque junta o histórico de duas branches diferentes. Isso faz com que o histórico seja um grafo, pois um commit pode estar ligado a mais de um commit anterior, e não apenas ao anterior como em uma lista.

## 4. Tupla no método pais

O método pais devolve uma tupla para proteger os dados internos da classe. Assim, quem utiliza o método consegue consultar os pais, mas não consegue modificar diretamente a lista armazenada no dicionário.

## Como executar

O projeto foi desenvolvido em Python 3 e pode ser executado pelo terminal com o comando:

```bash
python3 minigit.py
