"""Data models."""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Transaction:
    """Transaction data model."""

    transaction_code: str
    status: str
    timestamp: datetime
    amount_brl: float
    network: int
    category: str
    merchant_id: str

    def to_xml_dict(self) -> dict:
        """Convert to dictionary for XML generation."""
        return {
            'id': self.transaction_code,
            'status': self.status.lower(),
            'date': self.timestamp.strftime('%Y-%m-%d'),
            'amount': self.amount_brl,
            'type': self.category.upper(),
            'merchant_id': self.merchant_id,
            'network': str(self.network),
            'category': self.category.upper()
        }
