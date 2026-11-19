import re
import io
import pymupdf
from contracts import Transaction, TransactionCategory
from dataclasses import dataclass

def extract_text_from_pdf(stream: io.BytesIO) -> str:
    doc = pymupdf.open(stream=stream, filetype="pdf")
    try:
        return "".join(page.get_text() for page in doc)
    finally:
        doc.close()

def parse_sber(text: str) -> [Transaction]:
    
    PATTERNS = {
        'transaction': 
        re.compile(r'\d{1,2}\.\d{2}\.\d{4}\n\d{1,2}:\d{2}\n',
        r'.+\n\+?\b\d{1,3}(?:[ \u00A0\u202F]\d{3})*,\d{2}\b\n',
        r'\b\d{1,3}(?:[ \u00A0\u202F]\d{3})*,\d{2}\b\n',
        r'\d{1,2}\.\d{2}\.\d{4}\n\d+\n.+\n'),
    } 

    def parse_transactions(text: str):
        tr = re.findall(PATTERNS['transaction'], text)
        transactions = []
        for t in tr:
            blocks = t.split('\n')
            try:
                curr_transaction = Transaction(
                datetime=datetime.strptime(f"{blocks[0]} {blocks[1]}", "%d.%m.%Y %H:%M"),
                category=blocks[2],
                amount=float(blocks[3].replace('\xa0', '').replace(',','.')),
                remaining=float(blocks[4].replace('\xa0', '').replace(',','.')),
                is_positive=blocks[3].startswith('+'),
                desc=blocks[7]
            )
            except:
                continue

            transactions.append(curr_transaction)
        return transactions
    


    



    