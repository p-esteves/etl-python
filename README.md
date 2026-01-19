# Projeto Mandala - Custo Brasil (ETL Python)

## Sobre o Projeto
Este repositório contém o conjunto de scripts de ETL (Extração, Transformação e Carga) desenvolvidos para o projeto **Mandala**, uma iniciativa estratégica do **Observatório da Indústria da FIEC** em parceria com o **Ministério da Economia**.

O objetivo da Mandala é monitorar e propor ações para reduzir o **Custo Brasil**, estimado em **R$ 1,5 trilhão por ano** (aprox. 20,5% do PIB à época). Os indicadores são organizados em pilares como Capital Humano, Infraestrutura, Segurança Jurídica e Carga Tributária.

Estes scripts são responsáveis por coletar dados de diversas fontes públicas (nacionais e internacionais) para alimentar os painéis de monitoramento.

> [!NOTE]
> **Observação Importante**: Estes códigos fazem parte de um ecossistema maior de processamento de dados. Executá-los isoladamente pode resultar em erros de dependência ou falta de contexto.
>
> **Disponibilidade dos Dados**: Como este é um projeto legado (desenvolvido há alguns anos), algumas fontes de dados originais (URLs, APIs) podem ter mudado, estar indisponíveis ou não estarem completas neste repositório. O código serve principalmente como registro histórico da lógica de ETL utilizada.

## ⚠ Aviso de Segurança
Por razões de segurança, **nenhuma credencial de banco de dados é armazenada neste repositório**.
O código foi refatorado para utilizar **Variáveis de Ambiente**.

### Configuração do Ambiente
Para executar os scripts, você deve definir as seguintes variáveis de ambiente no seu sistema ou arquivo `.env`:

- `DB_SERVER`: Endereço do servidor SQL.
- `DB_USERNAME`: Usuário do banco de dados.
- `DB_PASSWORD`: Senha do banco de dados.
- `DB_DRIVER` (Opcional): Driver ODBC (padrão: `{ODBC Driver 17 for SQL Server}`).

## Estrutura do Projeto
O projeto está organizado em módulos por fonte de dados/tema. Cada diretório contém o script principal de ETL e uma pasta `functions` com utilitários de conexão segura.

### Módulos Principais

| Módulo | Descrição | Fonte |
| :--- | :--- | :--- |
| **aneel** | Tarifas médias de fornecimento de energia. | ANEEL |
| **anp** | Preços de combustíveis (revenda e distribuição). | ANP |
| **bcb** | Séries temporais (crédito, spread bancário). | Banco Central |
| **cambio** | Taxas de câmbio médias anuais. | Ipeadata |
| **cds** | Risco país (Credit Default Swap - 5 anos). | World Gov Bonds |
| **country ict** | Assinaturas de banda larga mundial. | ITU |
| **custo logistico** | Estimativas de custos logísticos. | Dados locais |
| **gas natural** | Consumo de gás natural. | ANP |
| **horas prep** | Horas gastas com pagamento de impostos. | Banco Mundial |
| **insolvency** | Taxa de recuperação em casos de insolvência. | Banco Mundial |
| **ocde / ocde 2** | Tarifas de energia/gás e indicadores PMR. | Eurostat / OCDE |
| **oecd wage** | Encargos trabalhistas e salários. | OCDE |
| **pib** | Produto Interno Bruto (R$ Correntes). | Fonte Local |
| **pilares** | Índice de Competitividade Global. | DataScope |
| **populacao** | Projeções populacionais. | IBGE |
| **transit** | Dados de tráfego e congestionamento (Inrix). | API Inrix |
| **tst** | Indicadores da Justiça do Trabalho. | TST |
| **worldbank** | Diversos indicadores econômicos (Doing Business). | Banco Mundial (API) |

## Requisitos
- Python 3.x
- Bibliotecas: `pandas`, `numpy`, `sqlalchemy`, `pyodbc`, `requests`, `openpyxl`, `eurostat`, `ipeadatapy`, `sgs`.

## Como Executar
1. Instale as dependências.
2. Configure as variáveis de ambiente.
3. Execute o script desejado, por exemplo:
   ```bash
   python mandala/aneel/aneel.py
   ```
