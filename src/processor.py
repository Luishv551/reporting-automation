"""Data processing with pandas."""

import re
from typing import List, Dict
import pandas as pd
from .models import Transaction


class TransactionProcessor:
    """Processes transaction data from CSV."""

    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.df = None
        self.errors = []
        self.warnings = []

    def load_and_process(self, target_month: str) -> List[Transaction]:
        """
        Load CSV and process transactions for target month.

        Args:
            target_month: Month in YYYY-MM format

        Returns:
            List of Transaction objects
        """
        # Read CSV
        self.df = pd.read_csv(self.csv_path)
        self.df.columns = self.df.columns.str.strip()

        rows_in = len(self.df)

        # Parse dates
        self.df['timestamp'] = pd.to_datetime(
            self.df['timestamp'],
            format='mixed',
            dayfirst=True,
            errors='coerce'
        )

        # Remove invalid dates
        invalid_dates = self.df['timestamp'].isna().sum()
        if invalid_dates > 0:
            self.warnings.append(f"Removed {invalid_dates} rows with invalid dates")
        self.df = self.df[self.df['timestamp'].notna()]

        # Filter by month
        self.df['year_month'] = self.df['timestamp'].dt.strftime('%Y-%m')
        self.df = self.df[self.df['year_month'] == target_month]

        # Normalize amount
        self.df['amount_BRL'] = (
            self.df['amount_BRL']
            .astype(str)
            .str.replace('"', '')
            .str.replace(',', '.')
            .astype(float)
        )

        # Normalize category
        self.df['category'] = self.df['category'].str.strip().str.upper()

        # Normalize merchant ID
        self.df['merchant_id'] = self.df['merchant_id'].apply(self._normalize_merchant_id)

        # Clean status
        self.df['status'] = self.df['status'].str.strip().str.lower()

        # Remove duplicates
        duplicates = self.df.duplicated(subset=['transaction_code']).sum()
        if duplicates > 0:
            self.warnings.append(f"Removed {duplicates} duplicate transactions")
        self.df = self.df.drop_duplicates(subset=['transaction_code'])

        # Check for chargebacks
        chargebacks = (self.df['status'] == 'chargeback').sum()
        if chargebacks > 0:
            self.warnings.append(f"Found {chargebacks} chargeback(s)")

        # Convert to Transaction objects
        transactions = []
        for _, row in self.df.iterrows():
            transactions.append(Transaction(
                transaction_code=row['transaction_code'],
                status=row['status'],
                timestamp=row['timestamp'],
                amount_brl=row['amount_BRL'],
                network=int(row['network']),
                category=row['category'],
                merchant_id=row['merchant_id']
            ))

        return transactions

    def _normalize_merchant_id(self, merchant_id) -> str:
        """Normalize merchant ID by removing formatting."""
        if pd.isna(merchant_id):
            return ''

        numbers = re.sub(r'[^0-9]', '', str(merchant_id))

        # Pad partial CNPJ to 14 digits
        if 7 <= len(numbers) <= 9:
            numbers = numbers.ljust(8, '0') + '0001' + '00'
        elif len(numbers) == 11:
            numbers = numbers + '00'
        elif len(numbers) > 14:
            numbers = numbers[:14]

        return numbers

    def get_summary(self) -> Dict:
        """Get processing summary with metrics."""
        if self.df is None or len(self.df) == 0:
            return {}

        return {
            'total_transactions': len(self.df),
            'total_amount_brl': float(self.df['amount_BRL'].sum()),
            'by_status': self.df['status'].value_counts().to_dict(),
            'by_category': self.df['category'].value_counts().to_dict(),
            'by_network': self.df['network'].value_counts().to_dict(),
            'chargebacks': int((self.df['status'] == 'chargeback').sum()),
            'warnings': self.warnings
        }
