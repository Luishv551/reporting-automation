"""Email notification sender using Outlook COM API."""

import win32com.client
import pythoncom
from pathlib import Path
from typing import Dict

from .config import config


class EmailSender:
    """Sends email notifications via Outlook COM API."""

    def send_report(self, month: str, summary: Dict, xml_path: str):
        """
        Send transactional report via Outlook.

        Uses Outlook COM API to avoid authentication issues with
        modern security policies (MFA, OAuth2, disabled basic auth).

        Args:
            month: Report month (YYYY-MM)
            summary: Summary dictionary
            xml_path: Path to XML report
        """
        if not config.EMAIL_TO:
            raise ValueError("EMAIL_TO missing in .env")

        # Build email body
        body = self._build_body(month, summary)

        # Initialize COM
        pythoncom.CoInitialize()
        try:
            # Create Outlook instance
            outlook = win32com.client.Dispatch('outlook.application')
            mail = outlook.CreateItem(0)  # 0 = MailItem

            # Set properties
            mail.Subject = f'Transactional Report — {month}'
            mail.To = config.EMAIL_TO
            mail.Body = body

            # Attach XML
            xml_file = Path(xml_path)
            if xml_file.exists():
                mail.Attachments.Add(str(xml_file.absolute()))

            # Send
            mail.Send()
        finally:
            pythoncom.CoUninitialize()

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
