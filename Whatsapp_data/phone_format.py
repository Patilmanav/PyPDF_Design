from fpdf import FPDF
# from constants import report_disclamer
import os
import datetime
# from data import data
d = os.getcwd()
bold_font = os.path.join(d,'fonts',"Noto_Sans\static",'NotoSans-Bold.ttf')
non_bold_font = os.path.join(d,'fonts','Noto_Sans','NotoSans-VariableFont_wdth,wght.ttf')
print(bold_font)
print(non_bold_font)

def clean_text(text):
    if isinstance(text, (bool, int, float)):
        return str(text.encode('latin-1', 'replace').decode('latin-1'))
    return "".join(
        [char if len(char) == 1 and ord(char) < 128 else " " for char in text]
    )


def generate_phone_pdf(data):

    class PDF(FPDF):
        def header(self):
            # Left margin
            self.set_fill_color(0, 18, 95)
            self.rect(0, 0, left_margin, self.h, "F")

        # Page footer
        def footer(self):
            # Position at 1.5 cm from ottom
            self.set_y(-15)
            # Arial italic 8
            self.set_font("Noto", "", 8)
            # Page numer
            self.cell(0, 10, "Page " + str(self.page_no()) + "/{n}", 0, 0, "C")

    # Instantiation of inherited class
    left_margin = 5
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()

    # defined Fonts
    pdf.add_font("Noto", '', non_bold_font, uni=True)
    pdf.add_font("Noto-Bold", '', bold_font, uni=True)

    # Set the width for the image
    # pdf.set_xy(0,0)
    pdf.image("PDF/img/logo1.png", left_margin, 7, h=30)
    pdf.ln(30)

    pdf.set_left_margin(left_margin + 45)
    pdf.set_y(10)
    pdf.set_font("Noto-Bold", "", 22)
    pdf.cell(50, 10, "RUDRASTRA", 0)
    pdf.set_font("Noto", "", 22)
    pdf.cell(30, 10, "OSNIT", 0, 1)
    pdf.set_font("Noto-Bold", "", 22)
    pdf.cell(35, 10, "REPORT", 0)
    pdf.set_font("Noto", "", 22)
    truecaller_data = data.get("Truecaller_data", {}).get("data", {})[0]

    pdf.set_font("Noto", "", 18)
    pdf.cell(
        30,
        10,
        "for  {}".format(
            truecaller_data.get("phones", [{}])[0].get("e164Format", "N/A")
        ),
        0,
    )

    # Add confidential note
    pdf.set_xy(0, 30 + 10)  # Adjust y-position after the image

    pdf.set_font("Noto", "", 12)
    pdf.set_text_color(255, 255, 255)
    pdf.set_fill_color(0, 18, 95)
    pdf.multi_cell(
        pdf.w,
        10,
        "NOTE: This report is strictly confidential and only for Police officers. Don't share it with anyone else or post it on WhatsApp, Telegram, or anywhere else pulic.",
        0,
        fill=True,
        align="C",
    )

    pdf.ln(20)

    pdf.set_left_margin(left_margin + 10)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Noto-Bold", "", 18)
    pdf.set_x(left_margin + 10)
    pdf.image("PDF/img/arrow.png", w=10)
    pdf.set_xy(left_margin + 25, 80)
    pdf.cell(0, 10, "Suject Information", 0, ln=1)

    pdf.set_font("Noto-Bold", "", 16)
    pdf.cell(80, 10, "Phone Numer")
    pdf.set_font("Noto", "", 16)
    pdf.cell(10, 10, ":", 0)
    pdf.cell(
        80,
        10,
        f"{truecaller_data.get('phones', [{}])[0].get('e164Format', 'N/A')}",
        ln=1,
    )
    pdf.set_font("Noto-Bold", "", 16)
    pdf.cell(80, 10, "Date Of Report")
    pdf.set_font("Noto", "", 16)
    pdf.cell(10, 10, ":", 0)
    pdf.cell(80, 10, "{}".format(datetime.date.today()), ln=1)
    pdf.set_font("Noto-Bold", "", 16)
    pdf.cell(80, 10, "Report Generated y")
    pdf.set_font("Noto", "", 16)
    pdf.cell(10, 10, ":", 0)
    pdf.cell(80, 10, "+91 0123456789", ln=1)

    pdf.ln(20)

    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Noto-Bold", "", 18)
    pdf.image("PDF/img/arrow.png", w=10)
    pdf.set_xy(left_margin + 25, 80 + 60)
    pdf.cell(0, 10, "NAME's", 0, ln=1)

    names_len = None
    names = [data.get("eyecon_data", {}).get("data", {}).get("fullName", "N/A")]
    for i in data.get("eyecon_data", {}).get("data", {}).get("otherNames", []):
        names.append(i.get("name", "N/A"))

    for index, i in enumerate(names):
        pdf.set_font("Noto", "", 16)
        names_len = len(names)
        pdf.cell(0, 10, f"{index}.        {i}", 0, 1)

    pdf.ln(20)

    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Noto-Bold", "", 18)
    pdf.image("PDF/img/arrow.png", w=10)
    pdf.set_xy(left_margin + 25, 80 + 60 + (10 * names_len + 30))
    pdf.cell(0, 10, "CARRIER INFO", 0, ln=1)

    pdf.set_font("Noto-Bold", "", 16)
    pdf.cell(50, 10, "Moile")
    pdf.cell(10, 10, ":", 0)
    pdf.set_font("Noto", "", 16)
    pdf.cell(
        80,
        10,
        "{}".format(truecaller_data.get("phones", [{}])[0].get("e164Format", "N/A")),
        ln=1,
    )
    pdf.set_font("Noto-Bold", "", 16)
    pdf.cell(50, 10, "Carrier")
    pdf.set_font("Noto", "", 16)
    pdf.cell(10, 10, ":", 0)
    pdf.cell(
        80,
        10,
        "{}".format(truecaller_data.get("phones", [{}])[0].get("carrier", "N/A")),
        ln=1,
    )
    pdf.set_font("Noto-Bold", "", 16)
    pdf.cell(50, 10, "Type")
    pdf.cell(10, 10, ":", 0)
    pdf.set_font("Noto", "", 16)
    pdf.cell(
        80,
        10,
        "{}".format(truecaller_data.get("phones", [{}])[0].get("type", "N/A")),
        ln=1,
    )
    pdf.set_font("Noto-Bold", "", 16)
    pdf.cell(50, 10, "Addresss")
    pdf.cell(10, 10, ":", 0)
    pdf.set_font("Noto", "", 16)
    pdf.cell(
        80,
        10,
        "{}, {}".format(
            truecaller_data.get("addresses", [{}])[0].get("address", "N/A"),
            truecaller_data.get("addresses", [{}])[0].get("city", "N/A"),
        ),
        ln=1,
    )

    pdf.ln(20)
    pdf.add_page()
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Noto-Bold", "", 18)
    pdf.image("PDF/img/arrow.png", w=10)
    pdf.set_xy(left_margin + 25, 10)
    pdf.cell(0, 10, "PORTING INFORMATION", 0, ln=1)

    # TODO: Hardcoded, Fetch From API.
    pdf.set_font("Noto-Bold", "", 16)
    pdf.cell(50, 10, "Numer Ported")
    pdf.cell(10, 10, ":", 0)
    pdf.set_font("Noto", "", 16)
    pdf.cell(80, 10, "yes", ln=1)
    pdf.set_font("Noto-Bold", "", 16)
    pdf.cell(50, 10, "Present Provider")
    pdf.cell(10, 10, ":", 0)
    pdf.set_font("Noto", "", 16)
    pdf.cell(80, 10, "Jio", ln=1)
    pdf.set_font("Noto-Bold", "", 16)
    pdf.cell(50, 10, "Circle")
    pdf.cell(10, 10, ":", 0)
    pdf.set_font("Noto", "", 16)
    pdf.cell(80, 10, "Mumai", ln=1)
    pdf.set_font("Noto-Bold", "", 16)
    pdf.cell(50, 10, "Service Type")
    pdf.cell(10, 10, ":", 0)
    pdf.set_font("Noto", "", 16)
    pdf.cell(80, 10, "prepaid", ln=1)

    pdf.ln(20)

    sc_md_ac = (
        data.get("social_media_accounts", {}).get("data", {}).get("account_details", {})
    )
    wp_ac = data.get("whatsapp_data", {})
    social_media_acc = {}
    if data.get("social_media_accounts", {}).get("success"):
        social_media_acc.update({
            "WhatsApp": {
                "logo": "PDF/img/whatsapp.png",
                "Status": (
                    "Account Exist" if wp_ac.get("data").get("numer") else "Account Not Exist"
                ),
                "AboutStatus": wp_ac.get("data").get("about"),
                "LastUpdate": "19-11-2023 22:46",
            },
            "Flipkart": {
                "logo": "PDF/img/flipkart.png",
                "Status": (
                    "Account Exist"
                    if sc_md_ac.get("flipkart".lower()).get("registered")
                    else "Account Not Exist"
                ),
            },
            "ZEE5": {
                "logo": "PDF/img/zee5.png",
                "Status": (
                    "Account Exist"
                    if sc_md_ac.get("ZEE5".lower()).get("registered")
                    else "Account Not Exist"
                ),
            },
            "MakeMyTrip": {
                "logo": "PDF/img/makemytrip.png",
                "Status": (
                    "Account Exist"
                    if sc_md_ac.get("MakeMyTrip".lower()).get("registered")
                    else "Account Not Exist"
                ),
            },
            "Snapdeal": {
                "logo": "PDF/img/snapdeal.png",
                "Status": (
                    "Account Exist"
                    if sc_md_ac.get("Snapdeal".lower()).get("registered")
                    else "Account Not Exist"
                ),
            },
            "AltBalaji": {
                "logo": "PDF/img/alt_balaji.png",
                "Status": (
                    "Account Exist"
                    if sc_md_ac.get("AltBalaji".lower()).get("registered")
                    else "Account Not Exist"
                ),
            },
            "Shopclues": {
                "logo": "PDF/img/shopclus.jpg",
                "Status": (
                    "Account Exist"
                    if sc_md_ac.get("Shopclues".lower()).get("registered")
                    else "Account Not Exist"
                ),
            },
            "Ajio": {
                "logo": "PDF/img/alt_balaji.png",
                "Status": (
                    "Account Exist"
                    if sc_md_ac.get("Ajio".lower()).get("registered")
                    else "Account Not Exist"
                ),
            },
        })
    elif wp_ac.get("status",None) == 200:
        social_media_acc.update({"WhatsApp": {
                "logo": "PDF/img/whatsapp.png",
                "Status": (
                    "Account Exist" if wp_ac.get("data").get("number") else "Account Not Exist"
                ),
                "AboutStatus": str(wp_ac.get("data").get("about")),
                "LastUpdate": "19-11-2023 22:46",
            }}
        )
    else:
        social_media_acc = None

    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Noto-Bold", "", 18)
    pdf.image("PDF/img/arrow.png", w=10)
    pdf.set_xy(left_margin + 25, 80)
    pdf.cell(0, 10, "SOCIAL MEDIA ACCOUNTS", 0, ln=1)

    start = 80
    if social_media_acc:
        for index,(k, v) in enumerate(social_media_acc.items()):
            if wp_ac.get("data").get('isBusiness'):
                if index == 3:
                    pdf.add_page()
            else:
                if index == 5:
                    pdf.add_page()
            if start >= pdf.h+30:
                start = 30
            pdf.ln(10)
            pdf.set_x(left_margin + 10)
            pdf.image(str(v["logo"]),y = pdf.get_y() , w=20)
            pdf.set_font("Noto-Bold", "", 16)
            pdf.set_x(left_margin + 35)
            pdf.cell(50, 10, f"{str(k)}", 0, 1)
            start += 10
            
            pdf.set_font("Noto", "", 16)
            pdf.set_xy(left_margin + 35,pdf.get_y())
            pdf.cell(50, 10, "Status", 0)
            pdf.cell(10, 10, ":", 0)

            pdf.cell(50, 10, f"{str(v['Status'])}", 0, 1)
            start += 10
            
            if k == "WhatsApp":
                if wp_ac.get("data").get('isBusiness'):

                    businessProfile = wp_ac.get("data").get("businessProfile")
                    pdf.set_x(left_margin + 35)
                    pdf.cell(50, 10, "AboutStatus", 0)
                    pdf.cell(10, 10, ":", 0)
                    pdf.set_font("Noto", "", 16)
                    
                    pdf.cell(50, 10, f"{clean_text(v.get('AboutStatus','none'))}", 0, 1)
                    start += 10 
                    
                    pdf.set_x(left_margin + 35)
                    pdf.cell(50, 10, "LastUpdate", 0)
                    pdf.cell(10, 10, ":", 0)
                    pdf.cell(50, 10, f"{clean_text(v.get('LastUpdate','none'))}", 0, 1)
                    start += 10
                    
                    
                    pdf.set_x(left_margin + 35)
                    pdf.cell(50, 10, "Server", 0)
                    pdf.cell(10, 10, ":", 0)
                    pdf.cell(50, 10, f"{clean_text(businessProfile.get('id').get('server'))}", 0, 1)
                    start += 10

            
                    pdf.set_x(left_margin + 35)
                    pdf.cell(50, 10, "User", 0)
                    pdf.cell(10, 10, ":", 0)
                    pdf.cell(50, 10, f"{clean_text(businessProfile.get('id').get('user'))}", 0, 1)
                    start += 10

            
                    
                    pdf.set_x(left_margin + 35)
                    pdf.cell(50, 10, "Description", 0)
                    pdf.set_font("Noto","",14)
                    lines = businessProfile.get('description').replace(" ","")
                    cleaned_lines = [line for line in lines if line.strip() != ""]
                    pdf.cell(10, 10, ":", 0)
                    pdf.multi_cell(0, 10, f"{clean_text(cleaned_lines)}")
            
                    
                    pdf.set_font("Noto","",16)
                    pdf.set_x(left_margin + 35)
                    pdf.cell(50, 10, "Display Name", 0)
                    pdf.cell(10, 10, ":", 0)
                    pdf.cell(50, 10, f"{clean_text(businessProfile.get('categories')[0].get('localized_display_name'))}", 0, 1)
                    start += 10

            

                    bullet = chr(149)
                    
                    pdf.set_x(left_margin + 35)
                    pdf.cell(50, 10, "Profile Options", 0)
                    pdf.cell(10, 10, ":", 0)
                    start += 10

                    pdf.set_x(left_margin + 85)

                    pdf.set_font('Arial', 'B', 22)
                    pdf.cell(20, 10, bullet, align='C')
                    pdf.set_font('Noto', '', 16)
                    
                    pdf.cell(50, 10, f"{clean_text(businessProfile.get('profileOptions').get('commerceExperience'))}", 0, 1)
                    start += 10

                    pdf.set_x(left_margin + 85)
                    if businessProfile.get('profileOptions').get('cartEnabled'):
                        pdf.set_font('Arial', 'B', 22)
                        pdf.cell(20, 10, bullet, align='C')
                        pdf.set_font('Noto', '', 16)
                        
                        pdf.cell(50, 10, "Cart Enabled",0,1)
                        start += 10
                    
                    pdf.set_x(left_margin + 35)
                    pdf.cell(50, 10, "Email", 0)
                    pdf.cell(10, 10, ":", 0)
                    pdf.cell(50, 10, f"{clean_text(businessProfile.get('email'))}", 0, 1)
                    start += 10

            
                    pdf.set_x(left_margin + 35)
                    pdf.cell(50, 10, "Websites", 0)
                    pdf.cell(10, 10, ":", 0)
                    pdf.multi_cell(0, 10, f"{(businessProfile.get('website'))}", 0, 1)
                    start += 10
                    
                    pdf.set_x(left_margin + 35)
                    pdf.cell(50, 10, "Business Hours", 0)
                    start += 10
                    pdf.cell(10, 10, ":", 0)

                    shcedule = ""
                    for k,v in (businessProfile.get('businessHours').get('config').items()):
                        # pdf.cell(0, 10, f"{i}", 0)
                        shcedule += f"{k} : {v}\n"
                    pdf.multi_cell(0,10,shcedule)
                    
            
                    pdf.set_x(left_margin + 35)
                    pdf.cell(50, 10, "Address", 0)
                    pdf.cell(10, 10, ":", 0)
                    pdf.multi_cell(0, 10, f"{(businessProfile.get('address'))}", 0, 1)
                    start += 10

            
                    
                    pdf.set_x(left_margin + 35)
                    pdf.cell(50, 10, "Is Profile Linked", 0)
                    pdf.cell(10, 10, ":", 0)
                    pdf.cell(50, 10, f"{'Yes'if businessProfile.get('isProfileLinked') else 'No'}", 0, 1)
                    start += 10

            
                    pdf.set_x(left_margin + 35)
                    pdf.cell(50, 10, "Is Profile Locked", 0)
                    pdf.cell(10, 10, ":", 0)
                    pdf.cell(0, 10, f"{ 'Yes'if businessProfile.get('isProfileLocked') else 'No'}", 0, 1)
                    start += 10
            

                else:

                    pdf.set_x(left_margin + 35)
                    pdf.cell(50, 10, "AboutStatus", 0)
                    pdf.cell(10, 10, ":", 0)
                    pdf.cell(50, 10, f"{clean_text(v.get('AboutStatus','none'))}", 0, 1)
                    start += 10

                    pdf.set_x(left_margin + 35)
                    pdf.cell(50, 10, "LastUpdate", 0)
                    pdf.cell(10, 10, ":", 0)
                    pdf.cell(50, 10, f"{clean_text(v.get('LastUpdate','none'))}", 0, 1)
                    start += 10

                        

        pdf.add_page()
    else:
        pdf.set_font("Noto-Bold", "", 22)
        pdf.set_text_color(204, 0, 0)
        pdf.cell(0, 30, f"No Data Found", 0, 1, "C", 0)

    upi_status = data.get("Upi_Data", {}).get("status", {})

    # UPI Section
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Noto-Bold", "", 18)
    # pdf.set_top_margin(img_margin)
    pdf.image("PDF/img/arrow.png", w=10 )
    pdf.set_xy(left_margin + 25,10)
    pdf.cell(0, 10, "UPI Information", 0, ln=1)

    pdf.ln(20)
    pdf.set_font("Noto-Bold", "", 16)
    if upi_status:
        upi_data = data.get("Upi_Data", {}).get("data", {}).get("response2", {})

        # pdf.set_xy(left_margin + 35+20)
        pdf.cell(50, 10, "VPA Token", 0)
        pdf.cell(10, 10, ":", 0)
        pdf.set_font("Noto", "", 16)
        pdf.multi_cell(0, 10, f"{str(upi_data.get('vpa_token','none'))}", 0, "L")
        # pdf.set_xy(left_margin + 35+30)

        pdf.set_font("Noto-Bold", "", 16)
        pdf.cell(50, 10, "Masked VPA", 0)
        pdf.cell(10, 10, ":", 0)

        pdf.set_font("Noto", "", 16)
        pdf.cell(40, 10, f"{str(upi_data.get('masked_vpa','none'))}", 0, 1)

        pdf.set_font("Noto-Bold", "", 16)
        pdf.cell(50, 10, "Customer Name", 0)
        pdf.cell(10, 10, ":", 0)

        pdf.set_font("Noto", "", 16)
        pdf.cell(40, 10, f"{str(upi_data.get('customer_name','none'))}", 0, 1)
    else:
        pdf.set_font("Noto-Bold", "", 26)
        pdf.set_text_color(204, 0, 0)
        pdf.multi_cell(0, pdf.h - 100, f"No Data Found", 0, "C", 0)

    pdf.add_page()
    # //Source Images
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Noto-Bold", "", 18)
    pdf.image("PDF/img/arrow.png", w=10)
    pdf.set_xy(left_margin + 25, 10)
    pdf.cell(0, 10, "Source Images", 0, ln=1)

    pdf.add_page()
    # //E-MAIL REACHED
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Noto-Bold", "", 18)
    pdf.image("PDF/img/arrow.png", w=10)
    pdf.set_xy(left_margin + 25, 10)
    pdf.cell(0, 10, "E-MAIL REACHED", 0, ln=1)

    pdf.add_page()
    # //Legal Disclaimer for OSINT Report
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Noto-Bold", "", 18)
    pdf.image("PDF/img/arrow.png", w=10)
    pdf.set_xy(left_margin + 25, 10)
    pdf.cell(0, 10, "Legal Disclaimer for OSINT Report", 0, ln=1)

    # TODO: Add Actual Disclamer on last page in Production.
    para = "LONG Disclamer"
    pdf.set_font("Noto", "", 12)
    pdf.multi_cell(0, 10, str(para))

    # pdf.output(
    #     os.path.join(
    #         os.getcwd(),
    #         f"Phone Info/{truecaller_data.get('phones')[0].get('e164Format')}_phone.pdf",
    #     ),
    #     "F",)
    # pdf.output("Phone_OSINT.pdf")
    # Generate PDF content as inary
# Generate PDF content as inary

    filename = "Phone_OSINT.pdf"
    # pdf_content = pdf.output(dest="S").encode("latin-1")
    # with open(filename, "w") as f:
    #     f.write(pdf_content)

    
    pdf.output("filename.pdf", 'F')

from data import data
generate_phone_pdf(data)