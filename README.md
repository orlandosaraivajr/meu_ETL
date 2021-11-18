# Meu ETL

Projeto desenvolvido durante as sprints 7 e 8 - "NappAcademy - Fase 1"

### O que fazer ?

1. Clone o repositório
2. Crie um virtualenv 
3. Ative a virtualenv
4. Instale as dependências
5. Navegar em cada commit e observar os avanços

```console
git clone https://github.com/orlandosaraivajr/meu_ETL.git
virtualenv venv -p python3
source venv/bin/activate
cd meu_ETL/
pip install -r requirements.txt 
```
### Primeiro commit 

Neste commit, desenvolvido na live do dia 06 de novembro, desenvolvemos uma primeira versão do "Meu ETL".
O projeto:
1. Lista todos os Fundos Imobiliários (FIIs) disponíveis na B3
2. Para cada FII, pesquisar a cotação no momento da busca.
3. Registrar esta pesquisa do valor da cota em uma mídia não volátil.

```console
git checkout a92732d

 ```

### Segundo commit: 

Alteração na fonte da lista de fundos disponíveis na B3

Neste commit, foi alterado a fonte da lista de FIIs

```console
 git checkout  65c19c6
 ```

### Terceiro commit: 

Separando responsabilidades

Neste commit, foi criado uma classe para Extrair(E), uma classe para Transformação(T) e outra classe para Armazenar (L)

```console
 git checkout  db8eb06
 ```

### Quarto commit: 

Uso de padrões de projetos

Neste commit, foi criado uma classe base para Extrair(E), e uma classe base para Armazenar (L).
Futuras implementações para Extrair e Armazenar podem ser adicionadas sem quebrar o código existente.

```console
 git checkout  85a8dda
 ```

### Quinto commit: 

Onde estão os testes ?

Neste commit, foi adicionado testes.
Não foi uma implementação TDD ( Test Driven Developement), mas este commit tem como objetivo provocar você a refletir como criar testes com seu código legado.

```console
 git checkout  7eccf86
 ```

### Vamos executar: 

```console
 pytest --cov=.
 coverage html
 python meu_ETL.py

 ```