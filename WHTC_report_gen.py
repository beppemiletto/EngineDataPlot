import time
import os
import sys
import getopt
import pickle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm, mm
from reportlab.lib.colors import red, blue, green, black, gray, yellow, yellowgreen
# from reportlab.platypus.flowables import PageBreak, PageBreakIfNotEmpty

from PIL import Image as pil_img

# <class 'dict'>: {'h1': <ParagraphStyle 'Heading1'>,
# 'title': <ParagraphStyle 'Title'>,
# 'h2': <ParagraphStyle 'Heading2'>,
# 'h3': <ParagraphStyle 'Heading3'>,
# 'h4': <ParagraphStyle 'Heading4'>,
# 'h5': <ParagraphStyle 'Heading5'>,
# 'h6': <ParagraphStyle 'Heading6'>,
# 'bu': <ParagraphStyle 'Bullet'>,
# 'df': <ParagraphStyle 'Definition'>,
# 'ul': <ListStyle 'UnorderedList'>,
# 'ol': <ListStyle 'OrderedList'>}

class Test_Info():
    def __init__(self):
        self.elements = None
        self.type = None
        self.date = None
        self.number = None


def img_size(image_path=None):
    try:
        im = pil_img.open(image_path)
        width, height = im.size
    except:
        width= None
        height= None
    finally:
        return width,height

def txt_from_file(txt_file_path=None):
    try:
        with open(txt_file_path, "r") as txt_file:
            text_content = txt_file.read()
    except Exception:
        text_content= "Location of {}. Error occured: {}".format(txt_file_path, Exception)
    finally:
        return text_content

#----------------------------------------------------------------------
def addPageNumber(canvas, doc):
    """
    Add the page conf
    """
    page_num = canvas.getPageNumber()
    text = "page {}".format(page_num)
    canvas.drawRightString(207*mm, 3*mm, text)

def main(argv):
    pwd = ''
    docname = ''
    phases = {'cold':'Cold', 'hot':'Hot'}
    gen_pwd = 'D:\Application_data\yy_report_general_images'

    try:
        opts, args = getopt.getopt(argv, "hp:o:", ["path=", "ofile="])
    except getopt.GetoptError:
        print('WHTC_report_gen.py  -p <\input path\..> -o <outputfile.pdf>')

        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('WHTC_report_gen.py  -p <\input path\..> -o <outputfile.pdf>')
            sys.exit()
        elif opt in ("-p", "--path"):
            pwd = arg
        elif opt in ("-o", "--ofile"):
            docname = arg

    if pwd.strip() == '' or pwd.strip()[0] == '-':
        print('No working folder in options: -p <absolute path to folder>')
        exit(1)
    else:
        pwd_phases = {}

        phase: str
        for phase in phases.keys():
            pwd_phases[phase] = pwd + '_' + phases[phase]

    if docname.strip() == '':
        docname = pwd.split('\\')[-1] + '.pdf'

    print ("Base Working path is '{}'.".format(pwd))
    print ("     Cold phase is '{}'.".format(pwd_phases['cold']))
    print ("     Hot phase  is '{}'".format(pwd_phases['hot']))
    print ("Output PDF document is '{}'".format(docname))
    png_files = {}
    for phase in phases.keys():
        png_files[phase] = [f for f in os.listdir(pwd_phases[phase]) if f.endswith('.png')]

    for phase in phases.keys():
        if len(png_files[phase]) == 0:
            print("No .png image file for phase {}.".format(phases[phase]))

    test_info = Test_Info()
    test_info.elements = pwd.split('_')
    test_info.type = test_info.elements[2]
    test_info.date = test_info.elements[3]
    test_info.number = test_info.elements[4]

    pwd = gen_pwd

    # beginning of DOC construction
    doc = SimpleDocTemplate(os.path.join(pwd,docname), pagesize= A4,
                            rightMargin=36, leftMargin=36,
                            topMargin=9, bottomMargin=9,
                            author='Giuseppe Miletto')
    doc_story = []
    charts_scaling_factor = 0.95

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))


    formatted_time = time.ctime()

    # First Page
    im_logo = os.path.join(pwd,'logo.png')
    width,height = img_size(im_logo)
    im_logo_im = Image(im_logo, width /300 * inch, height / 300 * inch, hAlign='LEFT')

    ptext = "METATRON SPA - Local Unit Volvera - Turin"

    company_name = Paragraph(ptext, styles["Heading3"])

    im_cover = os.path.join(pwd,'head_left_image.png')
    width, height = img_size(im_cover)
    im_cover_im = Image(im_cover, width / 300 * inch, height / 300 * inch, hAlign='LEFT')

    ptext = "Test Report: World Harmonized Transient Cycle (WHTC)."
    title = (Paragraph(ptext, styles["Heading1"]))
    data = [[im_logo_im,company_name,'',''],[im_cover_im,title,'','']]

    table = Table(data)
    table.setStyle([("VALIGN", (0, 0), (0, 0), "TOP"),
                    ('SPAN',(-3, 0), (-1, 0)),
                    ('SPAN', (-3, 1), (-1, 1))
                    ])
    # table.wrapOn(self.c, self.width, self.height)
    # table.drawOn(self.c, *self.coord(18, 60, mm))
    doc_story.append(table)

    doc_story.append(Spacer(1, 12))
    ptext = "NGV OM 906 Single Point Injection."
    doc_story.append(Paragraph(ptext, styles["Heading2"]))
    doc_story.append(Spacer(1, 12))

    ptext = '<font size=12>Print date of report: %s</font>' % formatted_time
    doc_story.append(Paragraph(ptext, styles["Heading3"]))
    doc_story.append(Spacer(1, 12))

    ptext = '<font size=12>Test type: %s</font>' % test_info.type
    doc_story.append(Paragraph(ptext, styles["Heading3"]))
    doc_story.append(Spacer(1, 8))

    ptext = '<font size=12>Test date: %s</font>' % test_info.date
    doc_story.append(Paragraph(ptext, styles["Heading3"]))
    doc_story.append(Spacer(1, 8))

    ptext = '<font size=12>Test conf in date: %s</font>' % test_info.number
    doc_story.append(Paragraph(ptext, styles["Heading3"]))
    doc_story.append(Spacer(1, 8))

    doc_story.append(PageBreak())

    # Summary page and notes
    ptext = 'Test methodology: WHTC at Bosmal Test Bed '
    doc_story.append(Paragraph(ptext, styles["Heading2"]))
    doc_story.append(Spacer(1, 12))

    txt_file = os.path.join(pwd,'WHTC.txt')
    ptext = txt_from_file(txt_file)
    doc_story.append(Paragraph(ptext, styles["Normal"]))
    doc_story.append(Spacer(1, 6))

    ptext= "WHTC Test figure"
    doc_story.append(Paragraph(ptext, styles["Heading3"]))
    doc_story.append(Spacer(1, 6))

    im_pict_png =  os.path.join(pwd,'World-Harmonised-Transient-Cycle-WHTC.png')
    width, height = [850, 380]
    im = Image(im_pict_png, width / 300 * inch, height / 300 * inch)
    doc_story.append(im)

    doc_story.append(PageBreak())

    for phase in phases.keys():

        for png_file in png_files[phase]:
            print (png_file)
            ptext = "{} phase. Chart: {}".format(phases[phase], png_file.split('.')[0])
            doc_story.append(Paragraph(ptext, styles["Heading3"]))
            doc_story.append(Spacer(1, 6))

            im_pict_png = os.path.join(pwd_phases[phase], png_file)
            width, height = [2000, 1600]
            im = Image(im_pict_png, width / 300 * inch, height / 300 * inch)
            doc_story.append(im)

            doc_story.append(PageBreak())



    doc.build(doc_story,onFirstPage=addPageNumber, onLaterPages=addPageNumber)

if __name__ == "__main__":
   main(sys.argv[1:])
