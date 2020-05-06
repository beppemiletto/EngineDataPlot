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
    try:
        opts, args = getopt.getopt(argv, "hp:o:", ["path=", "ofile="])
    except getopt.GetoptError:
        print('report_gen.py  -p <\input path\..> -o <outputfile.pdf>')

        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('report_gen.py  -p <\input path\..> -o <outputfile.pdf>')
            sys.exit()
        elif opt in ("-p", "--path"):
            pwd = arg
        elif opt in ("-o", "--ofile"):
            docname = arg
    print ("Working path is '{}'".format(pwd))
    print ("Output PDF document is '{}'".format(docname))

    pickle_files = [f for f in os.listdir(pwd) if f.endswith('.pickle')]
    if len(pickle_files) == 0:
        print("No pickle file for segment definition.")
        sys.exit()
    elif len(pickle_files) > 1:
        print("Too many pickle files for segment definition: {}".format(pickle_files))
        sys.exit()
    else:
        pickle_file_path=os.path.join(pwd,pickle_files[0])

    with open(pickle_file_path, mode='rb') as pickle_file:
        esc_seq_dic = pickle.load(pickle_file)


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

    ptext = "Test Report: Fuel System methodology ESC test."
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
    ptext = "Tank emptying simulation at test bed using the ESC repeated profile."
    doc_story.append(Paragraph(ptext, styles["Heading2"]))
    doc_story.append(Spacer(1, 12))

    ptext = '<font size=12>Date of report: %s</font>' % formatted_time
    doc_story.append(Paragraph(ptext, styles["Heading3"]))
    doc_story.append(Spacer(1, 12))


    doc_story.append(PageBreak())

    # Summary page and notes
    ptext = 'Test methodology: the emptying simulation with ESC simplified repetition'
    doc_story.append(Paragraph(ptext, styles["Heading2"]))
    doc_story.append(Spacer(1, 12))

    txt_file = os.path.join(pwd,'the_ESC_method_preface.txt')
    ptext = txt_from_file(txt_file)
    doc_story.append(Paragraph(ptext, styles["Normal"]))
    doc_story.append(Spacer(1, 6))

    ptext= "ESC Test Modes table"
    doc_story.append(Paragraph(ptext, styles["Heading3"]))
    doc_story.append(Spacer(1, 6))

    data = [
        ["Mode"," Engine Speed", "Load, %", "Weight, %", "ESC Normal Duration", " ESC Simplified Duration"],
        ["1", "idle", "0", "15", "4 minutes", "1 minute"],
        ["2", "A", "100", "8", "2 minutes", "30 seconds"],
        ["3", "B", "50", "8", "2 minutes", "30 seconds"],
        ["4", "B", "75", "10", "2 minutes", "30 seconds"],
        ["5", "A", "50", "5", "2 minutes", "30 seconds"],
        ["6", "A", "75", "5", "2 minutes", "30 seconds"],
        ["7", "A", "25", "5", "2 minutes", "30 seconds"],
        ["8", "B", "100", "9", "2 minutes", "30 seconds"],
        ["9", "B", "25", "10", "2 minutes", "30 seconds"],
        ["10", "C", "100", "8", "2 minutes", "30 seconds"],
        ["11", "C", "25", "5", "2 minutes", "30 seconds"],
        ["12", "C", "75", "5", "2 minutes", "30 seconds"],
        ["13", "C", "50", "5", "2 minutes", "30 seconds"],
        ]
    t = Table(data)
    t.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
                           ('TEXTCOLOR', (0, 0), (-1, 0), red),
                           ('TEXTCOLOR', (0, 0), (-1, -1), blue),
                           ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
                           ('INNERGRID', (0, 0), (-1, -1), 0.25, black),
                           ('BOX', (0, 0), (-1, -1), 0.25, black),
                           ]))

    doc_story.append(t)
    doc_story.append(Spacer(1, 12))


    doc_story.append(PageBreak())



    # Total ESC Test Picture
    ptext = 'Picture of the total test main parameters'
    doc_story.append(Paragraph(ptext, styles["Heading2"]))
    doc_story.append(Spacer(1, 12))

    im_pict_png = esc_seq_dic['000']['gloabl_chart_png']
    width, height = img_size(im_pict_png)
    im = Image(im_pict_png, width / 300 * inch, height / 300 * inch)
    doc_story.append(im)

    doc_story.append(PageBreak())

    for esc_num in range(len(esc_seq_dic)):
        esc_completed = esc_seq_dic['{:03d}'.format(esc_num)]['esc_complete']
        figure_1 = True
        figure_2 = True

        if esc_completed:
            ptext = "Pictures of the completed simplified ESC conf {}.".format(esc_num+1)
            doc_story.append(Paragraph(ptext, styles["Heading2"]))
            doc_story.append(Spacer(1, 3))
            ptext = "The ESC completed means that no violations to the engine speeds and load percentages occured during the execution."
            doc_story.append(Paragraph(ptext, styles["Normal"]))
        else:
            ptext = "Pictures of the NOT completed simplified ESC conf {}.".format(esc_num + 1)
            doc_story.append(Paragraph(ptext, styles["Heading2"]))
            doc_story.append(Spacer(1, 3))
            ptext = """The ESC NOT completed means that one or more violations to the engine speeds and load 
            percentages occured during the execution.\n
            Tipically it happen when the fuel tank is almost empty or some other conditions 
            are affecting the capacity of the fuel system to provide the
            correct amount of required fuel at the right pressure and tenperature.\n
             """
            doc_story.append(Paragraph(ptext, styles["Normal"]))
        doc_story.append(Spacer(1, 3))

        im_pict_png = esc_seq_dic['{:03d}'.format(esc_num)]['chart1_segment_png']
        width, height = img_size(im_pict_png)
        im = Image(im_pict_png, width / 300 * inch * charts_scaling_factor, height / 300 * inch* charts_scaling_factor)
        doc_story.append(im)

        doc_story.append(Spacer(1, 3))

        im_pict_png = esc_seq_dic['{:03d}'.format(esc_num)]['chart2_segment_png']
        width, height = img_size(im_pict_png)
        im = Image(im_pict_png, width / 300 * inch* charts_scaling_factor, height / 300 * inch* charts_scaling_factor)
        doc_story.append(im)

        doc_story.append(PageBreak())



    doc.build(doc_story,onFirstPage=addPageNumber, onLaterPages=addPageNumber)

if __name__ == "__main__":
   main(sys.argv[1:])
