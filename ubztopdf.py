#!/usr/bin/env python3

import zipfile
import argparse
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas
import os
import shutil

def main():
    parser = argparse.ArgumentParser(description='Convert .ubz files to pdf.')
    parser.add_argument('Path', metavar='path', type=str, help='Path to .ubz file')
    args = parser.parse_args()
    input_path = args.Path
    extracted_path = input_path[:-4]
    
    with zipfile.ZipFile(input_path, 'r') as archive:
        archive.extractall(extracted_path)

    filenames = sorted(os.listdir(extracted_path))
    svgfiles = [extracted_path + '/' + file for file in filenames if file[-4:] == '.svg']

    xL, yL, xH, yH = svg2rlg(open(svgfiles[0], 'r')).getBounds()
    pdf = canvas.Canvas(input_path[:-4] + '.pdf', pagesize = (xH - xL, yH - yL))

    for file in svgfiles:
        drawing = svg2rlg(file)
        #renderPDF.drawToFile(drawing, file)
        renderPDF.draw(drawing, pdf, 0, 0)
        pdf.showPage()

    pdf.save()

    shutil.rmtree(extracted_path)

if __name__ == "__main__":
    main()