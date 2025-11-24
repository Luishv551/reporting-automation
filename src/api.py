"""REST API with FastAPI."""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from pathlib import Path
from datetime import datetime
import uuid

from .processor import TransactionProcessor
from .reporters import XMLReporter, JSONReporter
from .email_sender import EmailSender

app = FastAPI(title="Transaction Reporting API")

# In-memory job storage
jobs = {}


class ReportRequest(BaseModel):
    """Report generation request."""
    month: str
    input_file: str
    output_dir: str = "./outputs"
    send_email: bool = False


class JobResponse(BaseModel):
    """Job creation response."""
    job_id: str
    status: str
    message: str


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "reporting-api",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post("/reports/generate", response_model=JobResponse)
def generate_report(request: ReportRequest, background_tasks: BackgroundTasks):
    """
    Generate transaction report.

    Starts report generation in background and returns job ID.
    """
    # Validate input file
    if not Path(request.input_file).exists():
        raise HTTPException(status_code=400, detail=f"Input file not found: {request.input_file}")

    # Create job
    job_id = str(uuid.uuid4())
    jobs[job_id] = {
        "job_id": job_id,
        "status": "pending",
        "created_at": datetime.utcnow().isoformat(),
        "month": request.month
    }

    # Start background processing
    background_tasks.add_task(
        process_report,
        job_id,
        request.month,
        request.input_file,
        request.output_dir,
        request.send_email
    )

    return JobResponse(
        job_id=job_id,
        status="pending",
        message="Report generation started"
    )


@app.get("/jobs/{job_id}")
def get_job_status(job_id: str):
    """Get job status by ID."""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")

    return jobs[job_id]


def process_report(job_id: str, month: str, input_file: str, output_dir: str, send_email: bool):
    """Process report in background."""
    job = jobs[job_id]
    job["status"] = "processing"

    try:
        # Process transactions
        processor = TransactionProcessor(input_file)
        transactions = processor.load_and_process(month)

        if not transactions:
            job["status"] = "failed"
            job["error"] = "No transactions found for the specified month"
            return

        summary = processor.get_summary()

        # Generate reports
        output_path = Path(output_dir) / month.replace('-', '')

        xml_reporter = XMLReporter()
        xml_path = xml_reporter.generate(transactions, month, str(output_path / 'report.xml'))

        json_reporter = JSONReporter()
        json_path = json_reporter.generate(summary, month, str(output_path / 'summary.json'))

        # Send email if requested
        if send_email:
            email_sender = EmailSender()
            email_sender.send_report(month, summary, xml_path)

        # Update job status
        job["status"] = "completed"
        job["result"] = {
            "transactions_count": len(transactions),
            "xml_path": xml_path,
            "json_path": json_path
        }

    except Exception as e:
        job["status"] = "failed"
        job["error"] = str(e)

    job["completed_at"] = datetime.utcnow().isoformat()
