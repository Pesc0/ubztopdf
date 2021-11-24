#!/usr/bin/env python3

import argparse
import os
import zipfile
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas
import shutil



def ubz_to_pdf(filepath):
    file_name, file_extension = os.path.splitext(filepath)
    
    if file_extension != '.ubz':
        raise Exception('File ' + filepath + ' is not an ubz file. Skipping.')

    extract_dir = '/tmp/ubztopdf/' + os.path.basename(file_name)

    with zipfile.ZipFile(filepath, 'r') as archive:
        archive.extractall(extract_dir)

    allfiles = sorted(os.listdir(extract_dir))
    svgfiles = [extract_dir + '/' + file for file in allfiles if file[-4:] == '.svg']

    xL, yL, xH, yH = svg2rlg(svgfiles[0]).getBounds() 
    pdf = canvas.Canvas(file_name + '.pdf', pagesize = (xH - xL, yH - yL))

    for file in svgfiles:
        drawing = svg2rlg(file)
        #renderPDF.drawToFile(drawing, file) #Single image
        renderPDF.draw(drawing, pdf, 0, 0)
        pdf.showPage()

    pdf.save()
    shutil.rmtree(extract_dir)


def main():
    parser = argparse.ArgumentParser(description='Convert .ubz files to pdf.')
    parser.add_argument('files', nargs='+', type=str, help='One or more paths to .ubz files')
    args = parser.parse_args()

    for file in args.files:
        try:
            ubz_to_pdf(file)
        except Exception as e:
            print(str(e))


if __name__ == "__main__":
    main()
