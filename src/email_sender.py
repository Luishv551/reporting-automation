"""Email notification sender."""

import smtplib
from pathlib import Path
from typing import Dict
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

from .config import config


class EmailSender:
    """Sends email notifications with attachments."""

    def send_report(self, month: str, summary: Dict, xml_path: str):
        """
        Send transactional report via email.

        Args:
            month: Report month (YYYY-MM)
            summary: Summary dictionary
            xml_path: Path to XML report
        """
        if not config.SMTP_USER or not config.EMAIL_TO:
            raise ValueError("Email configuration missing in .env")

        # Build email body
        body = self._build_body(month, summary)

        # Create message
        msg = MIMEMultipart()
        msg['Subject'] = f'Transactional Report — {month}'
        msg['From'] = config.EMAIL_FROM
        msg['To'] = config.EMAIL_TO

        msg.attach(MIMEText(body, 'plain'))

        # Attach XML
        xml_file = Path(xml_path)
        if xml_file.exists():
            with open(xml_file, 'rb') as f:
                attachment = MIMEApplication(f.read(), _subtype='xml')
                attachment.add_header('Content-Disposition', 'attachment', filename=xml_file.name)
                msg.attach(attachment)

        # Send
        with smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT) as server:
            server.starttls()
            server.login(config.SMTP_USER, config.SMTP_PASS)
            server.send_message(msg)

    def _build_body(self, month: str, summary: Dict) -> str:
        """Build email body text."""
        lines = [
            f"TRANSACTIONAL REPORT - {month}",
            "=" * 50,
            "",
            "SUMMARY:",
            f"  - Total transactions: {summary.get('total_transactions', 0)}",
            f"  - Total amount: R$ {summary.get('total_amount_brl', 0):,.2f}",
            f"  - Chargebacks: {summary.get('chargebacks', 0)}",
            ""
        ]

        # By status
        if 'by_status' in summary:
            lines.append("BY STATUS:")
            for status, count in summary['by_status'].items():
                lines.append(f"  - {status}: {count}")
            lines.append("")

        # By category
        if 'by_category' in summary:
            lines.append("BY CATEGORY:")
            for cat, count in summary['by_category'].items():
                lines.append(f"  - {cat}: {count}")
            lines.append("")

        # Warnings
        if summary.get('warnings'):
            lines.append("ALERTS:")
            for warning in summary['warnings']:
                lines.append(f"  ! {warning}")
            lines.append("")

        lines.extend([
            "=" * 50,
            "The complete XML report is attached.",
            "",
            "This is an automated notification."
        ])

        return "\n".join(lines)
