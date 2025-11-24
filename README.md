# Transaction Reporting System

Sistema local que transforma dados de transações CSV em relatórios XML padronizados e envia notificações por email com resumos técnicos e alertas.

## Estrutura do Projeto

```
reporting-automation/
├── app.py                 # CLI principal
├── run_api.py            # Servidor REST API
├── .env.example          # Template de configuração
├── data/
│   └── data.csv          # Dados de entrada
├── outputs/              # Relatórios gerados
│   └── YYYYMM/
│       ├── report.xml
│       └── summary.json
└── src/
    ├── config.py         # Configurações
    ├── models.py         # Modelo de Transaction
    ├── processor.py      # Processamento CSV com pandas
    ├── reporters.py      # Geradores XML e JSON
    ├── email_sender.py   # Envio de email
    └── api.py           # API REST com FastAPI
```

## Instalação

```bash
uv add pandas python-dotenv fastapi uvicorn
```

## Configuração

1. Copie `.env.example` para `.env`
2. Configure suas credenciais de email:

```env
SMTP_USER=seu-email@outlook.com
SMTP_PASS=sua-senha
EMAIL_TO=destinatario@example.com
```

## Uso

### CLI

```bash
python app.py --month=2023-08 --input=./data/data.csv --output=./outputs
python app.py --month=2023-08 --input=./data/data.csv --send-email
```

### REST API

```bash
python run_api.py
```

Documentação interativa em: http://127.0.0.1:8000/docs

## Funcionalidades

- ✅ Leitura e processamento de CSV com pandas
- ✅ Normalização de datas (múltiplos formatos)
- ✅ Normalização de valores (vírgula/ponto decimal)
- ✅ Normalização de CNPJ (merchant_id)
- ✅ Validação e remoção de duplicatas
- ✅ Geração de XML padronizado
- ✅ Resumo JSON com métricas
- ✅ Notificação por email com anexo
- ✅ CLI e REST API
- ✅ Detecção de chargebacks e alertas

## Decisões de Design

**Organização**: Estrutura src/ com módulos separados por responsabilidade (config, models, processor, reporters, email, api)

**Simplicidade**: Uso de bibliotecas prontas (pandas para CSV, FastAPI para API) ao invés de implementações manuais

**Pandas**: Processamento de dados mais robusto e menos código

**FastAPI**: API REST moderna com documentação automática e validação

**Configuração**: Centralizada via .env para facilitar deploy
