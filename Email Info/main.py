from fpdf import FPDF
# from data import data
import datetime
import json
import os

f = open('./Email Info/data.json','r')
data = json.load(f)
# print(data['email']['PROFILE_CONTAINER'])
profile_data = data['email']['PROFILE_CONTAINER']['profile']

class PDF(FPDF):
    def header(self):
        # Left margin
        self.set_fill_color(0, 18, 95 )
        self.rect(0, 0, left_margin, self.h+1, 'F')

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

# Instantiation of inherited class
left_margin = 5
pdf = PDF()
pdf.alias_nb_pages()
pdf.add_page()

# defined Fonts 
pdf.add_font('DejaVu', '', './font/DejaVuSans.ttf', uni=True)
pdf.add_font('DejaVu-Bold', '', './font/dejavu-fonts-ttf-2.37/ttf/DejaVuSansCondensed-Bold.ttf', uni=True)
# Set the width for the image
# pdf.set_xy(0,0)
pdf.image('./img/logo1.png', left_margin, 7, h=30)
pdf.ln(30)

pdf.set_left_margin(left_margin+45)
pdf.set_y(10)
pdf.set_font('DejaVu-Bold', '', 22)
pdf.cell(50,10,"RUDRASTRA",0)
pdf.set_font('DejaVu', '', 22)
pdf.cell(30,10,"OSNIT",0,1)
pdf.cell(35,10,"REPORT",0)

pdf.set_font('times', '', 18)
pdf.cell(30,10,"for  {}".format(profile_data['emails']['PROFILE']['value']),0)



# Add confidential note
pdf.set_xy(0, 30 + 10)  # Adjust y-position after the image

pdf.set_font('Times', '', 12)
pdf.set_text_color(255, 255, 255)
pdf.set_fill_color(0, 18, 95 )
pdf.multi_cell(pdf.w, 10, "NOTE: This report is strictly confidential and only for Police officers. Don't share it with anyone else or post it on WhatsApp, Telegram, or anywhere else public.",0,fill=True,align='C')

line_gap = 10


pdf.ln(line_gap)

# Profile Section Started
pdf.set_left_margin(left_margin + 10)
pdf.set_text_color(0, 0, 0)

pdf.set_x(left_margin+10)
pdf.set_font('Times', 'B', 18)
pdf.image("./img/arrow.png",w=10)
line_gap = 70
pdf.set_xy(left_margin + 25, line_gap)
pdf.cell(0, 10, 'Profile Informationn', 0,ln=1)

pdf.ln(5)

pdf.set_font('Times', 'B', 16)
pdf.cell(40,10,"Full Name",0)
pdf.cell(40,10,f": {profile_data['names']['PROFILE']['fullname']}",0,1)
pdf.cell(40,10,"Email",0)
pdf.cell(40,10,f": {profile_data['emails']['PROFILE']['value']}",0,1)
pdf.cell(40,10,"User Types",0)
pdf.cell(40,10,f": {', '.join(profile_data['profileInfos']['PROFILE']['userTypes'])}",0,1)
# Profile Section Ended


pdf.ln(10)


# Apps Section Started
pdf.set_font('Times', 'B', 18)
pdf.image("./img/arrow.png",w=10)
line_gap += 55
pdf.set_xy(left_margin + 25, line_gap)
pdf.cell(0, 10, 'Apps Used: ', 0,ln=1)

pdf.ln(5)
line_gap += 15
pdf.set_font('Times', 'B', 16)
bullet = chr(149)
for i in profile_data['inAppReachability']['PROFILE']['apps']:
    
    pdf.set_font('Arial', 'B', 22)
    pdf.cell(20,10,bullet,align='C')
    pdf.set_font('Times', 'B', 16)
    pdf.cell(40,10,i,0,1)
    line_gap += 10

# Apps Section Ended

pdf.ln(10)

# Address Section Started
adress_data = data['email']['PROFILE_CONTAINER']['maps']['reviews'][0]['location']
pdf.set_font('Times', 'B', 18)
pdf.image("./img/arrow.png",w=10)
line_gap += 10
pdf.set_xy(left_margin + 25, line_gap)
pdf.cell(0, 10, 'Address Information', 0,ln=1)

pdf.ln(5)
types = ""
for index,i in enumerate(adress_data['types']):
    if index != len(adress_data['types']):
        types += str(i) + ","
    else:
        types += i
line_gap += 15
pdf.set_font('Times', 'B', 16)
# pdf.set_fill_color()
pdf.cell(0,10,f"{adress_data['name']} ({i})",0,1)
pdf.ln(5)
pdf.set_font('Times', 'B', 14)
pdf.cell(40,10,"Address")
pdf.multi_cell(0, 10, f":  {adress_data['address']} ",0,fill=0,align='L')

line_gap += 10
pdf.cell(40,10,"Longitude")
pdf.cell(0,10,f":  {adress_data['position']['longitude']} ",0,1)
line_gap += 10
pdf.cell(40,10,"Latitude")
pdf.cell(0,10,f":  {adress_data['position']['latitude']} ",0,1)
line_gap += 10
# Address Section Ended


# pdf.output("./Email info/Email Info.pdf")
pdf.output(os.path.join(os.getcwd(),f"Email info/{profile_data['emails']['PROFILE']['value']}_Email.pdf"), 'F')