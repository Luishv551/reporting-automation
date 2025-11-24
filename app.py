"""
CLI for transaction reporting system.

Usage:
    python app.py --month=2023-08 --input=./data/data.csv --output=./outputs
    python app.py --month=2023-08 --input=./data/data.csv --output=./outputs --send-email
"""

import argparse
import sys
from pathlib import Path

from src.processor import TransactionProcessor
from src.reporters import XMLReporter, JSONReporter
from src.email_sender import EmailSender


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Transaction Reporting System',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--month',
        required=True,
        help='Target month in YYYY-MM format (e.g., 2023-08)'
    )
    parser.add_argument(
        '--input',
        required=True,
        help='Path to input CSV file'
    )
    parser.add_argument(
        '--output',
        default='./outputs',
        help='Output directory for reports (default: ./outputs)'
    )
    parser.add_argument(
        '--send-email',
        action='store_true',
        help='Send email notification with report'
    )

    args = parser.parse_args()

    # Validate input file exists
    if not Path(args.input).exists():
        print(f"Error: Input file not found: {args.input}")
        sys.exit(1)

    print(f"\nGenerating report for {args.month}...")
    print(f"Input: {args.input}")
    print(f"Output: {args.output}\n")

    try:
        # Process transactions
        print("Step 1/4: Processing CSV data...")
        processor = TransactionProcessor(args.input)
        transactions = processor.load_and_process(args.month)
        print(f"  Found {len(transactions)} transactions for {args.month}")

        if len(transactions) == 0:
            print("\nNo transactions found for the specified month!")
            sys.exit(1)

        # Get summary
        summary = processor.get_summary()

        # Display warnings
        if summary.get('warnings'):
            print("\n  Warnings:")
            for warning in summary['warnings']:
                print(f"    - {warning}")

        # Generate reports
        output_dir = Path(args.output) / args.month.replace('-', '')

        print("\nStep 2/4: Generating XML report...")
        xml_reporter = XMLReporter()
        xml_path = xml_reporter.generate(transactions, args.month, str(output_dir / 'report.xml'))
        print(f"  {xml_path}")

        print("\nStep 3/4: Generating JSON summary...")
        json_reporter = JSONReporter()
        json_path = json_reporter.generate(summary, args.month, str(output_dir / 'summary.json'))
        print(f"  {json_path}")

        # Send email if requested
        if args.send_email:
            print("\nStep 4/4: Sending email...")
            try:
                email_sender = EmailSender()
                email_sender.send_report(args.month, summary, xml_path)
                print("  Email sent successfully")
            except Exception as e:
                print(f"  Email failed: {e}")
                sys.exit(1)
        else:
            print("\nStep 4/4: Skipping email (use --send-email to enable)")

        # Summary
        print(f"\n{'='*50}")
        print("REPORT GENERATED SUCCESSFULLY")
        print(f"{'='*50}")
        print(f"Transactions: {summary['total_transactions']}")
        print(f"Total amount: R$ {summary['total_amount_brl']:,.2f}")
        print(f"Chargebacks: {summary['chargebacks']}\n")

    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
