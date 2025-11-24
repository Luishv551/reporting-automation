# Quickstart

## 1. Install Dependencies

```bash
uv venv
uv sync
```

## 2. Configure Email

Copy the example file:
```bash
cp .env.example .env
```

Edit `.env` with your recipient email:
```env
EMAIL_TO=recipient@example.com
```

**Important**: This system uses Outlook COM API for email sending. Ensure:
- Windows OS
- Outlook desktop application installed
- Outlook configured with an authenticated account

No SMTP credentials required.

## 3. Run

### CLI Mode

**Generate report** (no email):
```bash
python app.py --month=2023-08 --input=./data/data.csv --output=./outputs
```

**Generate and send email**:
```bash
python app.py --month=2023-08 --input=./data/data.csv --output=./outputs --send-email
```

### API Mode (REST)

**Start server**:
```bash
python run_api.py
```

Access: http://127.0.0.1:8000/docs (interactive documentation)

**Generate report via API**:
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

**Check job status**:
```bash
curl "http://127.0.0.1:8000/jobs/{job_id}"
```

## Outputs

Files are generated in `outputs/YYYYMM/`:
- `report.xml` - XML report with transactions
- `summary.json` - Summary with metrics

## Test Other Months

```bash
python app.py --month=2023-01 --input=./data/data.csv
python app.py --month=2023-12 --input=./data/data.csv
```
