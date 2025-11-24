# Quickstart

## 1. Instalar Dependências

```bash
uv add pandas python-dotenv fastapi uvicorn
```

## 2. Configurar Email

Copie o arquivo de exemplo:
```bash
cp .env.example .env
```

Edite `.env` com suas credenciais do Outlook:
```env
SMTP_USER=seu-email@outlook.com
SMTP_PASS=sua-senha
EMAIL_TO=destinatario@example.com
```

## 3. Rodar

### Modo CLI

**Gerar relatório** (sem email):
```bash
python app.py --month=2023-08 --input=./data/data.csv --output=./outputs
```

**Gerar e enviar email**:
```bash
python app.py --month=2023-08 --input=./data/data.csv --output=./outputs --send-email
```

### Modo API (REST)

**Iniciar servidor**:
```bash
python run_api.py
```

Acesse: http://127.0.0.1:8000/docs (documentação interativa)

**Gerar relatório via API**:
```bash
curl -X POST "http://127.0.0.1:8000/reports/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "month": "2023-08",
    "input_file": "./data/data.csv",
    "output_dir": "./outputs",
    "send_email": false
  }'
```

**Consultar status do job**:
```bash
curl "http://127.0.0.1:8000/jobs/{job_id}"
```

## Outputs

Os arquivos são gerados em `outputs/YYYYMM/`:
- `report.xml` - Relatório XML com transações
- `summary.json` - Resumo com métricas

## Testar Outros Meses

```bash
python app.py --month=2023-01 --input=./data/data.csv
python app.py --month=2023-12 --input=./data/data.csv
```
