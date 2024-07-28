from fpdf import FPDF
import datetime
import os
from crypto_data import hash_data

d = os.getcwd()
bold_font = os.path.join(d,'fonts',"Noto_Sans\static",'NotoSans-Bold.ttf')
non_bold_font = os.path.join(d,'fonts','Noto_Sans\static','NotoSans-Regular.ttf')
print(bold_font)
print(non_bold_font)


def clean_text(text):
    if isinstance(text, (bool, int, float)):
        return str(text.encode('latin-1', 'replace').decode('latin-1'))
    return "".join(
        [char if len(char) == 1 and ord(char) < 128 else " " for char in text]
    )



class PDF(FPDF):
    def header(self):
        self.set_fill_color(0, 18, 95)
        self.rect(0, 0, left_margin, self.h + 1, 'F')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

left_margin = 5
pdf = PDF()
pdf.alias_nb_pages()
pdf.add_page()

# defined Fonts 
pdf.add_font("Noto",'',non_bold_font,uni=True)
pdf.add_font("Noto-Bold",'',bold_font,uni=True)

# Set the width for the image
pdf.image('./PDF/img/logo1.png', left_margin, 7, h=30)
pdf.ln(30)


pdf.set_left_margin(left_margin + 45)
pdf.set_y(10)
pdf.set_font('Noto-Bold', '', 22)
pdf.cell(50, 10, "RUDRASTRA", 0)
pdf.set_font('Noto-Bold', '', 22)
pdf.cell(30, 10, "OSNIT", 0, 1)
pdf.cell(35, 10, "REPORT", 0)

pdf.set_font('Noto', '', 18)
pdf.cell(30, 10, f"for  CRYPTO", 0)

pdf.set_xy(0, 30 + 10)
pdf.set_font('Noto', '', 12)
pdf.set_text_color(255, 255, 255)
pdf.set_fill_color(0, 18, 95)
pdf.multi_cell(pdf.w, 10, "NOTE: This report is strictly confidential and only for Police officers. Don't share it with anyone else or post it on WhatsApp, Telegram, or anywhere else public.", 0, fill=True, align='C')

line_gap = 10

# Crypto Section Started
pdf.ln(line_gap)
pdf.set_left_margin(left_margin + 10)
pdf.set_text_color(0, 0, 0)

pdf.set_font('Times', 'B', 18)
line_gap = 70
pdf.set_y(line_gap)
pdf.set_fill_color(51, 51, 255)

pdf.cell(0, 10, 'Cryptocurrency Transactions', 0, ln=1,align='C')
pdf.set_text_color(255, 255, 255)
pdf.set_font('Times', 'B', 22)
pdf.cell(0, 10, 'Account Balance: BTC, USD', 1, ln=1,align='C',fill=1)

pdf.ln(10)

pdf.set_text_color(0,0,0)

# Loop comes here
for index,obj in enumerate(hash_data.get('Transaction')):
    if pdf.get_y() >= pdf.h - 80:
        pdf.add_page()
        # print("page break")
    pdf.set_font('Noto-Bold', '', 20)
    pdf.cell(40, 10, f"Transaction {index+1}", 0,1)
    for k,v in obj.items():
        pdf.set_font('Noto', '', 18)
        pdf.cell(60, 10, f"{k}".capitalize(), 0) if k != "Transaction" else pdf.cell(60, 10, "Transaction ID", 0)
        pdf.cell(10, 10, ':', 0)
        pdf.multi_cell(0, 10, f"{v}", 0, 1)
    pdf.ln(10)
        
# Loop ends here

# Crypto Section Ended


pdf.add_page()
# pdf.set_left_margin(left_margin)

# //Legal Disclaimer for OSINT Report
pdf.set_text_color(0, 0, 0)
pdf.set_font('Noto-Bold', '', 18)
pdf.image("./PDF/img/arrow.png",w=10)
pdf.set_xy(left_margin + 25, 10)
pdf.cell(0, 10, "Legal Disclaimer for OSINT Report", 0,ln=1)

para = '''
The information in this Open Source Intelligence (OSINT) report is derived from
publicly available data and online sources as of its creation date. The accuracy,
completeness, and reliability of the information can vary and are not guaranteed.
This report is for informational purposes only and does not constitute legal,
professional, or expert advice.

The findings and conclusions in this report are based on publicly accessible
information and do not include any confidential or proprietary data. The recipient
acknowledges that the information may change over time, and any actions taken
based on this report are at their own risk. This report is not intended to infringe
upon any individual’s privacy rights or violate any laws or regulations. It is the
recipient’s responsibility to use the information responsibly and in compliance with
all applicable laws, regulations, and ethical standards.

The creators and providers of this report are not liable for any losses, damages, or
consequences arising from the use or reliance on the information in this report. The
recipient should independently verify any information before making decisions or
taking actions based on this report. By using this report, the recipient agrees to
release, indemnify, and hold harmless the creators and providers from any claims,
demands, actions, or liabilities arising from its use.

It is strongly recommended that the recipient seek legal, professional, or expert
advice before making decisions or taking actions based on the information in this
report.
'''
pdf.set_font('Noto', '', 12)
pdf.multi_cell(0,10,str(para))

# pdf.output(os.path.join(os.getcwd(), f"Email info/{email_value}_Email.pdf"), 'F')

pdf.output("Cypto_INFO.pdf", 'F')
