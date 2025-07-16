# utils/report_generator.py
from fpdf import FPDF
from datetime import datetime

class AccountStatementPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Bank Account Statement', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def generate_statement_pdf(account_number, transactions):
    pdf = AccountStatementPDF()
    pdf.add_page()
    pdf.set_font('Arial', '', 10)
    
    # Add account info
    pdf.cell(0, 10, f'Account Number: {account_number}', 0, 1)
    pdf.cell(0, 10, f'Statement Date: {datetime.now().strftime("%Y-%m-%d")}', 0, 1)
    pdf.ln(10)
    
    # Add transactions table
    pdf.set_fill_color(200, 220, 255)
    pdf.cell(30, 10, 'Date', 1, 0, 'C', 1)
    pdf.cell(40, 10, 'Type', 1, 0, 'C', 1)
    pdf.cell(40, 10, 'Amount', 1, 0, 'C', 1)
    pdf.cell(80, 10, 'Description', 1, 1, 'C', 1)
    
    pdf.set_fill_color(255, 255, 255)
    for t in transactions:
        pdf.cell(30, 10, t['timestamp'][:10], 1, 0)
        pdf.cell(40, 10, t['type'], 1, 0)
        amount = f"₹{t['amount']:.2f}"
        if t['type'] in ('Withdrawal', 'Transfer Out'):
            amount = f"-{amount}"
        pdf.cell(40, 10, amount, 1, 0, 'R')
        pdf.cell(80, 10, t.get('description', ''), 1, 1)
    
    return pdf.output(dest='S').encode('latin1')