# Documentação: Projeção de Estoque e Reposição (projecao.ipynb)

Este documento descreve a estrutura e funcionalidade do notebook `projecao.ipynb`, desenvolvido para simular e calcular a necessidade de reposição de estoque por loja e SKU, baseado em previsões de vendas.

## Objetivo
O objetivo principal é calcular automaticamente a quantidade a ser reposta de cada produto (SKU) em cada filial (Loja), semana a semana, garantindo que o estoque cubra a demanda prevista para um determinado horizonte de tempo.

---

## Estrutura do Código e Blocos Funcionais

Abaixo está a explicação detalhada de cada bloco de código (célula) presente no notebook.

### 1. Importações e Configurações Iniciais
**Funcionalidade:**
- Importa as bibliotecas necessárias (`pandas`, `numpy`, `pathlib`).
- Define os caminhos dos arquivos de entrada (`data/`) e saída (`outputs/`).
- Define os parâmetros globais da simulação:
    - `SEMANA_INICIO`: Semana de partida da simulação (ex: "W42_25").
    - `HORIZONTE_SEMANAS`: Quantas semanas à frente serão simuladas (24 semanas).
    - `SEMANAS_ALVO`: Janela de cobertura de estoque desejada (12 semanas).
    - `FATOR_DEFALCACAO_ALVO`: Fator para ajuste do alvo (1.0 = 100%, sem deflação).

### 2. Função Auxiliar: `_ordenar_semana`
**Funcionalidade:**
- Função utilitária para permitir a ordenação correta das semanas.
- Converte strings no formato "W39_25" (Semana_Ano) para uma tupla `(Ano, Semana)`, permitindo ordenação cronológica correta (ex: ano 25 vem antes de 26).

### 3. Definição da Lista de Filiais (`lista_ra`)
**Funcionalidade:**
- Define uma lista explícita de códigos de filiais (IDs) que farão parte da análise. Apenas as lojas listadas aqui serão processadas.

### 4. Função: `carregar_vendas`
**Funcionalidade:**
- Carrega o arquivo de previsão de vendas (`forecast-vendas.xlsx`).
- **Tratamento de Dados:**
    - Filtra as filiais presentes na `lista_ra`.
    - Cria a chave única `SKU` concatenando `PRODUTO`, `COR` e `TAMANHO`.
    - Padroniza o `SKU` (maiúsculas, sem espaços).
- **Renomeação de Colunas:** Identifica colunas de data (ex: "2024_W39") e as padroniza para o formato "W39_24".
- **Agrupamento:** Consolida os valores de vendas por `FILIAL` e `SKU` para garantir unicidade.

### 5. Função Auxiliar: `_coluna_existente`
**Funcionalidade:**
- Verifica se alguma coluna de uma lista de candidatos existe no DataFrame. Útil para lidar com variações de nomes de colunas em arquivos Excel diferentes (ex: "Filial", "PontoVda", "Loja").

### 6. Função: `carregar_estoque`
**Funcionalidade:**
- Carrega o arquivo de estoque atual (`estoque-total.xlsx`).
- **Tratamento de Dados:**
    - Identifica automaticamente colunas de Artigo, Tamanho, Filial e Estoque Total.
    - Cria a chave `SKU` (Artigo + Tamanho).
    - Filtra por filiais válidas.
    - Trata valores nulos e converte tipos numéricos.
- **Saída:** Retorna um DataFrame com o estoque atual consolidado por `FILIAL` e `SKU`.

### 7. Função: `carregar_carteira`
**Funcionalidade:**
- Carrega a carteira de pedidos (`carteira.xlsx`).
- Segue lógica similar ao carregamento de estoque: padronização de colunas, criação de SKU e filtros.
- **Saída:** Retorna o total de peças em carteira (pedidos já feitos mas não entregues) por `FILIAL` e `SKU`.

### 8. Lógica de Cálculo de Alvos (Markdown)
**Documentação:**
- Explica o conceito de "Janela Deslizante". O alvo de uma semana `X` é a soma das vendas previstas para as próximas `SEMANAS_ALVO` semanas.

### 9. Função: `calcular_alvos`
**Funcionalidade:**
- Implementa a lógica da janela deslizante explicada acima.
- Para cada semana da simulação:
    1. Define o intervalo de cobertura (semana atual + `SEMANAS_ALVO`).
    2. Soma as vendas projetadas nesse intervalo.
    3. Aplica o `FATOR_DEFALCACAO_ALVO` (se houver).
    4. Armazena o resultado em uma nova coluna `ALVO_Wxx_yy`.

### 10. Lógica de Simulação (Markdown)
**Documentação:**
- Explica com exemplos numéricos como a reposição é calculada:
    - `Reposição = Alvo - (Estoque Atual - Vendas da Semana)`
    - O objetivo é cobrir o "buraco" deixado pelas vendas e atingir o nível alvo.

### 11. Função: `simular_reposicao`
**Funcionalidade:**
- Realiza a simulação semana a semana.
- **Cálculo da Reposição:**
    - Calcula o saldo projetado: `Estoque Atual - Vendas`.
    - Determina quanto falta para atingir o `Alvo`.
    - **Buffer de Segurança:** **Aplica um fator de 1.20 (20% extra)** sobre a necessidade de reposição.
    - Arredonda a reposição para cima (`np.ceil`).
- **Atualização do Estoque:**
    - Atualiza o `estoque_corrente` para a próxima semana: `Estoque Anterior - Vendas + Reposição Calculada`.
- Armazena os valores calculados de `REPOSICAO_` e `ESTOQUE_` para cada semana.

### 12. Função: `salvar_resultados`
**Funcionalidade:**
- Prepara o DataFrame final para exportação.
- Seleciona as colunas relevantes (Dados do Produto, Vendas, Alvos, Reposições, Estoques Simulados).
- Preenche valores ausentes com 0.
- Salva o arquivo em Excel: `outputs/projecao_sku_pdv.xlsx`.

### 13. Função Principal: `main`
**Funcionalidade:**
- Orquestra todo o fluxo de execução:
    1. Carrega Vendas, Estoque e Carteira.
    2. Faz o `merge` (junção) dos DataFrames (Vendas + Estoque + Carteira).
    3. Calcula o **Estoque Inicial Total** (`Estoque Atual` + `Carteira`).
    4. Executa o cálculo de alvos.
    5. Executa a simulação de reposição.
    6. Salva os resultados finais.
- Inclui tratamento de erros (`try-except`) para exibir mensagens claras em caso de falha.

---

## Como Executar
1. Certifique-se de que a pasta `data/` contenha os arquivos:
    - `forecast-vendas.xlsx`
    - `estoque-total.xlsx`
    - `carteira.xlsx`
2. Execute todas as células do notebook sequencialmente.
3. O resultado será gerado na pasta `outputs/`.
