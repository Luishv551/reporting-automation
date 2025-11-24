"""Report generation (XML and JSON)."""

import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict
import xml.etree.ElementTree as ET
from xml.dom import minidom

from .models import Transaction


class XMLReporter:
    """Generates XML reports."""

    def generate(self, transactions: List[Transaction], month: str, output_path: str) -> str:
        """Generate XML report file."""
        root = ET.Element('TransactionsReport')
        root.set('month', month)
        root.set('generated_at', datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'))

        for trans in transactions:
            data = trans.to_xml_dict()
            trans_elem = ET.SubElement(root, 'Transaction')
            trans_elem.set('id', data['id'])

            ET.SubElement(trans_elem, 'Status').text = data['status']
            ET.SubElement(trans_elem, 'Date').text = data['date']

            amount_elem = ET.SubElement(trans_elem, 'Amount')
            amount_elem.set('currency', 'BRL')
            amount_elem.text = f"{data['amount']:.2f}"

            ET.SubElement(trans_elem, 'Type').text = data['type']
            ET.SubElement(trans_elem, 'MerchantId').text = data['merchant_id']
            ET.SubElement(trans_elem, 'Network').text = data['network']
            ET.SubElement(trans_elem, 'Category').text = data['category']

        # Pretty print
        rough_string = ET.tostring(root, encoding='utf-8')
        reparsed = minidom.parseString(rough_string)
        pretty_xml = reparsed.toprettyxml(indent='    ', encoding='utf-8').decode('utf-8')

        # Save
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(pretty_xml)

        return str(output_file)


class JSONReporter:
    """Generates JSON summary reports."""

    def generate(self, summary: Dict, month: str, output_path: str) -> str:
        """Generate JSON summary file."""
        report = {
            'month': month,
            'generated_at': datetime.utcnow().isoformat(),
            **summary
        }

        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)

        return str(output_file)
