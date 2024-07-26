from fpdf import FPDF
import datetime
import json
import os

f = open('./Email Info/data.json', 'r')
data = json.load(f)
profile_data = data.get('email', {}).get('PROFILE_CONTAINER', {}).get('profile', {})

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
pdf.add_font('DejaVu', '', './font/DejaVuSans.ttf', uni=True)
pdf.add_font('DejaVu-Bold', '', './font/dejavu-fonts-ttf-2.37/ttf/DejaVuSansCondensed-Bold.ttf', uni=True)
# Set the width for the image
pdf.image('./img/logo1.png', left_margin, 7, h=30)
pdf.ln(30)

pdf.set_left_margin(left_margin + 45)
pdf.set_y(10)
pdf.set_font('DejaVu-Bold', '', 22)
pdf.cell(50, 10, "RUDRASTRA", 0)
pdf.set_font('DejaVu', '', 22)
pdf.cell(30, 10, "OSNIT", 0, 1)
pdf.cell(35, 10, "REPORT", 0)

pdf.set_font('times', '', 18)
email_value = profile_data.get('emails', {}).get('PROFILE', {}).get('value', 'N/A')
pdf.cell(30, 10, f"for  {email_value}", 0)

pdf.set_xy(0, 30 + 10)
pdf.set_font('Times', '', 12)
pdf.set_text_color(255, 255, 255)
pdf.set_fill_color(0, 18, 95)
pdf.multi_cell(pdf.w, 10, "NOTE: This report is strictly confidential and only for Police officers. Don't share it with anyone else or post it on WhatsApp, Telegram, or anywhere else public.", 0, fill=True, align='C')

line_gap = 10

# Profile Section Started
pdf.ln(line_gap)
pdf.set_left_margin(left_margin + 10)
pdf.set_text_color(0, 0, 0)

pdf.set_x(left_margin + 10)
pdf.set_font('Times', 'B', 18)
pdf.image("./img/arrow.png", w=10)
line_gap = 70
pdf.set_xy(left_margin + 25, line_gap)
pdf.cell(0, 10, 'Profile Information', 0, ln=1)

pdf.ln(5)

pdf.set_font('Times', 'B', 16)
pdf.cell(40, 10, "Full Name", 0)
fullname = profile_data.get('names', {}).get('PROFILE', {}).get('fullname', 'N/A')
pdf.cell(40, 10, f": {fullname}", 0, 1)

pdf.cell(40, 10, "Email", 0)
pdf.cell(40, 10, f": {email_value}", 0, 1)

pdf.cell(40, 10, "User Types", 0)
user_types = ', '.join(profile_data.get('profileInfos', {}).get('PROFILE', {}).get('userTypes', []))
pdf.cell(40, 10, f": {user_types}", 0, 1)
# Profile Section Ended

pdf.ln(10)

# Apps Section Started
pdf.set_font('Times', 'B', 18)
pdf.image("./img/arrow.png", w=10)
line_gap += 55
pdf.set_xy(left_margin + 25, line_gap)
pdf.cell(0, 10, 'Apps Used: ', 0, ln=1)

pdf.ln(5)
line_gap += 15
pdf.set_font('Times', 'B', 16)
bullet = chr(149)
apps = profile_data.get('inAppReachability', {}).get('PROFILE', {}).get('apps', [])
for app in apps:
    pdf.set_font('Arial', 'B', 22)
    pdf.cell(20, 10, bullet, align='C')
    pdf.set_font('Times', 'B', 16)
    pdf.cell(40, 10, app, 0, 1)
    line_gap += 10

# Apps Section Ended

pdf.ln(10)

# Address Section Started
address_data = data.get('email', {}).get('PROFILE_CONTAINER', {}).get('maps', {}).get('reviews', [{}])[0].get('location', {})
pdf.set_font('Times', 'B', 18)
pdf.image("./img/arrow.png", w=10)
line_gap += 10
pdf.set_xy(left_margin + 25, line_gap)
pdf.cell(0, 10, 'Address Information', 0, ln=1)

pdf.ln(5)
types = ", ".join(address_data.get('types', []))
line_gap += 15
pdf.set_font('Times', 'B', 16)
name = address_data.get('name', 'N/A')
pdf.cell(0, 10, f"{name} ({types})", 0, 1)

pdf.ln(5)
pdf.set_font('Times', 'B', 14)
pdf.cell(40, 10, "Address")
address = address_data.get('address', 'N/A')
pdf.multi_cell(0, 10, f":  {address}", 0, fill=0, align='L')

line_gap += 10
longitude = address_data.get('position', {}).get('longitude', 'N/A')
pdf.cell(40, 10, "Longitude")
pdf.cell(0, 10, f":  {longitude}", 0, 1)

line_gap += 10
latitude = address_data.get('position', {}).get('latitude', 'N/A')
pdf.cell(40, 10, "Latitude")
pdf.cell(0, 10, f":  {latitude}", 0, 1)
line_gap += 10
# Address Section Ended

pdf.output(os.path.join(os.getcwd(), f"Email info/{email_value}_Email.pdf"), 'F')
