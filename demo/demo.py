import os
from fpdf import FPDF

path = r'D:\TechnicalVPN_Projects\PDF_Design\fonts\Noto_Sans\static'

folder = os.listdir(path)
pdf = FPDF()
pdf.add_page()

for index, filename in enumerate(folder):
    if filename.endswith('.ttf'):
        font_path = os.path.join(path, filename)

        # Check if file is a .ttf font
        if filename.lower().endswith('.ttf'):
            try:
                print("Done")
                pdf.add_font(f"NotoColorEmoji{index}", '', font_path, uni=True)
                pdf.set_font(f"NotoColorEmoji{index}", size=16)
                # Add text with emojis
                pdf.cell(200, 10, txt="🙏🏻🚩जय श्रीराम📿🙏🏻🚩", ln=True, align='C')
            except Exception as e:
                pdf.cell(200, 10, txt=f"Error with font {filename}: {e}", ln=True, align='C')
        else:
            print(f"Skipping non-TTF file: {filename}")

# Output the PDF
pdf.output("./output.pdf",'F')
