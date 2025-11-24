# Transaction Reporting System

Local system that transforms transaction CSV data into standardized XML reports and sends email notifications with technical summaries and alerts.

## Project Structure

```
reporting-automation/
├── app.py                 # Main CLI
├── run_api.py            # REST API server
├── .env.example          # Configuration template
├── data/
│   └── data.csv          # Input data
├── outputs/              # Generated reports
│   └── YYYYMM/
│       ├── report.xml
│       └── summary.json
└── src/
    ├── config.py         # Configuration
    ├── models.py         # Transaction model
    ├── processor.py      # CSV processing with pandas
    ├── reporters.py      # XML and JSON generators
    ├── email_sender.py   # Email sender (Outlook COM)
    └── api.py           # REST API with FastAPI
```
## Automated Email evidence

https://drive.google.com/drive/folders/1ec9g0T-R1QW_AKWCgHANoic1V067MxHG?usp=sharing

## Requirements

- **Python 3.12+**
- **Windows with Outlook installed** (for email functionality)

## Installation

### Option 1: Using uv (recommended)

```bash
uv venv
uv sync
```

### Option 2: Using pip

```bash
python -m venv venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Configuration

1. Copy `.env.example` to `.env`
2. Configure email recipient:

```env
EMAIL_TO=recipient@example.com
```

**Note**: Email sending uses Outlook COM API, requiring a local Outlook installation with an authenticated account. No SMTP credentials needed.

## Usage

### CLI

```bash
python app.py --month=2023-08 --input=./data/data.csv --output=./outputs
python app.py --month=2023-08 --input=./data/data.csv --send-email
```

### REST API

```bash
python run_api.py
```

Interactive documentation: http://127.0.0.1:8000/docs

## Features

- CSV reading and processing with pandas
- Date normalization (multiple formats)
- Value normalization (comma/dot decimal)
- CNPJ normalization (merchant_id)
- Duplicate validation and removal
- Standardized XML generation
- JSON summary with metrics
- Email notification with attachment
- CLI and REST API
- Chargeback detection and alerts

## Design Decisions

**Organization**: src/ structure with modules separated by responsibility (config, models, processor, reporters, email, api)

**Simplicity**: Use of production-ready libraries (pandas for CSV, FastAPI for API) instead of manual implementations

**Pandas**: More robust data processing with less code

**FastAPI**: Modern REST API with automatic documentation and validation

**Configuration**: Centralized via .env for easy deployment

**Email (Outlook COM)**: Uses Outlook COM API instead of SMTP to avoid authentication issues with modern security policies (MFA, OAuth2, disabled basic auth). Requires Windows with Outlook installed. This approach simplifies deployment by leveraging existing authenticated sessions.

## Key AI Prompts Used

This project was built with AI assistance. Key prompts included:

1. **Initial architecture**: "Build a local Python system that reads CSV transactions, analyzes and normalizes data, generates a single XML report with all reportable transactions, and sends email notifications with technical summaries and alerts. Include both CLI and REST API interfaces. Use pandas for CSV processing and FastAPI for the API layer."

2. **Data normalization**: "Implement robust CSV processing that handles: multiple date formats (DD/MM/YYYY, YYYY-MM-DD, timestamps), decimal separators (comma and dot), CNPJ normalization for merchant_id, duplicate detection and removal, and validation of required fields."

3. **XML generation**: "Create an XML reporter that generates a standardized structure with transaction_id, date, amount_brl, merchant_id, status, category, and payment_method. Filter transactions by month and handle chargebacks appropriately."

4. **Metrics and alerts**: "Generate a JSON summary with metrics including total transactions, total amount, chargebacks count, groupings by status and category, and a warnings list for potential inconsistencies like duplicate IDs, invalid categories, or suspicious chargebacks."

5. **REST API with async jobs**: "Implement a FastAPI endpoint that accepts month, input_file, output_dir, and send_email parameters. Process requests asynchronously, return a job_id immediately, and provide a status endpoint to check job completion and results."

6. **Email integration troubleshooting**: "The SMTP authentication is failing with error 535 (user locked by security defaults policy). I have another project using Outlook COM API (win32com.client) that works successfully. Can we migrate to this approach? Analyze the differences and implement email sending using Outlook COM to avoid MFA/OAuth2/basic auth restrictions."

7. **Code organization**: "Organize the codebase with clear separation of concerns: config.py for environment variables, models.py for data structures, processor.py for CSV logic, reporters.py for output generation, email_sender.py for notifications, and api.py for REST endpoints. Follow Python best practices."

8. **Documentation and deployment**: "Create comprehensive English documentation including installation with both uv and pip, clear explanation of the Outlook COM requirement and rationale, quickstart guide with CLI and API examples, and a requirements.txt for users without pyproject.toml."
