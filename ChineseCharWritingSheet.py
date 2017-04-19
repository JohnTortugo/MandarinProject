#!/usr/bin/python3
# -*- coding: utf-8 -*-

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics;
from reportlab.pdfbase.cidfonts import UnicodeCIDFont;
from reportlab.lib.pagesizes import A4

import sys;
import math;

# These variables (actually only the first) are used to
# align some objects in the page, for instance, center
# the title horizontally.
pageWidth, pageHeight = A4;

# constants for identifying X and Y values across arrays
X = 0;
Y = 1;

# Width and height of the outer character box in each page
outerHeight = 40;
outerWidth = 40;

phraseOuterBoxHeight = 40;
phraseOuterBoxWidth = 489;

# Padding between the outer character box and the inner 
# matrix where the characters are drawn
innerPadding = 5;

# This is actually by how much the 2*innerPadding will 
# be decremented when drawing consecutive character in
# a phrase
phraseInnerPadding = 9;

# This is how much space will be inserted when there is
# a space in the correspondent mandarim character position
phraseBlankWidth = -20;

# Width and height of each of the cells in the inner matrix
# where the chinese characters are drawn
cellHeight = 10;
cellWidth = 10;

# Overall horizontal initial position to start drawing each
# character row
horPositionStart = 50;

# Vertical position to start drawing the first row in each
# page. The first page has a title and therefore the padding
# is larger.
firstPageVertPosStart = 170;
innerPagesVertPosStart = 70;

# Horizontal and vertical distance between top left corner
# of consecutive horizontal or vertical character boxes.
horIncrement = outerWidth + 5;
vertIncrement = outerHeight + 20;

# Maximum number of chinese character rows to be drawn on
# each page. The inner pages can have more rows since they
# don't have a page title.
MaxRowsFirstPage = 10;
MaxRowsInnerPages = 12;
currMaxRowPerPage = MaxRowsFirstPage;





# Prototype for commonly used functions:
#   lineTo(x, y) and moveTo(x, y)
def drawCharacterBox(canv, startPoint, pinText, charText):
    ###################################
    # Draw the pinyin outside the box
    canv.setFontSize(11);
    canv.drawCentredString(startPoint[X]+outerWidth/2, startPoint[Y]-3, pinText);

    ###################
    # Draw outer square
    p = canv.beginPath();
    canv.setDash(2);
    canv.setLineWidth(.3)

    p.moveTo(startPoint[X], startPoint[Y]);                             # start at top left
    p.lineTo(startPoint[X] + outerWidth, startPoint[Y]);                # to the right
    p.lineTo(startPoint[X] + outerWidth, startPoint[Y] + outerHeight);  # to the bottom right
    p.lineTo(startPoint[X], startPoint[Y] + outerHeight);               # to the bottom left
    p.lineTo(startPoint[X], startPoint[Y]);                             # to the top left

    canv.drawPath(p)

    ##########################
    # Draw inner small squares
    p2 = canv.beginPath();
    canv.setDash(1, 2);
    canv.setLineWidth(.3)

    p2.moveTo(startPoint[X] + innerPadding, startPoint[Y] + innerPadding);                             # start at top left
    p2.lineTo(startPoint[X] + outerWidth - innerPadding, startPoint[Y] + innerPadding);                # to the right
    p2.lineTo(startPoint[X] + outerWidth - innerPadding, startPoint[Y] + outerHeight - innerPadding);  # to the bottom right
    p2.lineTo(startPoint[X] + innerPadding, startPoint[Y] + outerHeight - innerPadding);               # to the bottom left
    p2.lineTo(startPoint[X] + innerPadding, startPoint[Y] + innerPadding);                             # to the top left

    p2.moveTo(startPoint[X] + innerPadding, startPoint[Y] + innerPadding + cellHeight);
    p2.lineTo(startPoint[X] + outerWidth - innerPadding, startPoint[Y] + innerPadding + cellHeight);

    p2.moveTo(startPoint[X] + innerPadding, startPoint[Y] + innerPadding + 2*cellHeight);
    p2.lineTo(startPoint[X] + outerWidth - innerPadding, startPoint[Y] + innerPadding + 2*cellHeight);

    p2.moveTo(startPoint[X] + innerPadding + cellWidth, startPoint[Y] + innerPadding);
    p2.lineTo(startPoint[X] + innerPadding + cellWidth, startPoint[Y] + outerHeight - innerPadding);

    p2.moveTo(startPoint[X] + innerPadding + 2*cellWidth, startPoint[Y] + innerPadding);
    p2.lineTo(startPoint[X] + innerPadding + 2*cellWidth, startPoint[Y] + outerHeight - innerPadding);

    canv.drawPath(p2);

    ###################################
    # Draw the character inside the box
    canv.setFont("STSong-Light", 25);
    canv.drawCentredString(startPoint[X] + innerPadding + 1.5*cellWidth, startPoint[Y] + innerPadding + 2.3*cellHeight, charText);



# Prototype for commonly used functions:
#   lineTo(x, y) and moveTo(x, y)
def drawPhraseBox(canv, vertPositionStart, pinText, charText):
    ###################################
    # Draw the pinyin outside the box
    canv.setFont("STSong-Light", 11);
    canv.drawString(horPositionStart, vertPositionStart-3, pinText);

    ###################
    # Draw outer square
    p = canv.beginPath();
    canv.setDash(2);
    canv.setLineWidth(.3)

    p.moveTo(horPositionStart, vertPositionStart);                                                 # start at top left
    p.lineTo(horPositionStart + phraseOuterBoxWidth, vertPositionStart);                           # to the right
    p.lineTo(horPositionStart + phraseOuterBoxWidth, vertPositionStart + phraseOuterBoxHeight);    # to the bottom right
    p.lineTo(horPositionStart, vertPositionStart + phraseOuterBoxHeight);                          # to the bottom left
    p.lineTo(horPositionStart, vertPositionStart);                                                 # to the top left

    canv.drawPath(p)

    ##########################
    # Draw inner small square for each character. If the
    # character is a space just add some 'space'.
    startPoint = [horPositionStart, vertPositionStart];
    for charInd in range(0, 18):
        if (charText[charInd] != ' '):
            p2 = canv.beginPath();
            canv.setDash(1, 2);
            canv.setLineWidth(.3)

            p2.moveTo(startPoint[X] + innerPadding, startPoint[Y] + innerPadding);                             # start at top left
            p2.lineTo(startPoint[X] + outerWidth - innerPadding, startPoint[Y] + innerPadding);                # to the right
            p2.lineTo(startPoint[X] + outerWidth - innerPadding, startPoint[Y] + outerHeight - innerPadding);  # to the bottom right
            p2.lineTo(startPoint[X] + innerPadding, startPoint[Y] + outerHeight - innerPadding);               # to the bottom left
            p2.lineTo(startPoint[X] + innerPadding, startPoint[Y] + innerPadding);                             # to the top left

            p2.moveTo(startPoint[X] + innerPadding, startPoint[Y] + innerPadding + cellHeight);
            p2.lineTo(startPoint[X] + outerWidth - innerPadding, startPoint[Y] + innerPadding + cellHeight);

            p2.moveTo(startPoint[X] + innerPadding, startPoint[Y] + innerPadding + 2*cellHeight);
            p2.lineTo(startPoint[X] + outerWidth - innerPadding, startPoint[Y] + innerPadding + 2*cellHeight);

            p2.moveTo(startPoint[X] + innerPadding + cellWidth, startPoint[Y] + innerPadding);
            p2.lineTo(startPoint[X] + innerPadding + cellWidth, startPoint[Y] + outerHeight - innerPadding);

            p2.moveTo(startPoint[X] + innerPadding + 2*cellWidth, startPoint[Y] + innerPadding);
            p2.lineTo(startPoint[X] + innerPadding + 2*cellWidth, startPoint[Y] + outerHeight - innerPadding);

            canv.drawPath(p2);

            ###################################
            # Draw the character inside the box
            canv.setFont("STSong-Light", 25);
            canv.drawCentredString(startPoint[X] + innerPadding + 1.5*cellWidth, startPoint[Y] + innerPadding + 2.3*cellHeight, charText[charInd]);
        else:
            startPoint[X] += phraseBlankWidth;

        # Increment in horizontal offset for the next character 
        # box
        startPoint[X] += outerWidth - phraseInnerPadding;




def drawOpening(canv, english, chinese):
    canv.setFont("Helvetica", 15);
    canv.drawCentredString(pageWidth/2.0, 90, chinese);
    canv.drawCentredString(105, 130, "(Name): ");

    canv.setFont("STSong-Light", 15);
    canv.drawCentredString(pageWidth/2.0, 70, english);

    canv.setFont("STSong-Light", 12);
    canv.drawCentredString(62, 130, "姓名");

    p = canv.beginPath();
    canv.setLineWidth(.3)

    p.moveTo(135, 130);
    p.lineTo(540, 130);

    canv.drawPath(p);


def numPages(numRows):
    if (numRows < MaxRowsFirstPage):
        return 1;
    else:
        return 1 + math.ceil( (numRows - MaxRowsFirstPage) / MaxRowsInnerPages );


def drawFooter(canv, currentPage, maxPages):
    canv.setFont("Helvetica", 10);
    canv.drawString(482, 800, "(Page %d of %d)" % (currentPage, maxPages));

    canv.setFont("STSong-Light", 10);
    canv.drawString(425, 800, "汉字练习纸");

    p = canv.beginPath();
    canv.setLineWidth(.5)

    p.moveTo(50, 785);
    p.lineTo(540, 785);

    canv.drawPath(p);

# Function: getArgInt
# Description:
#	 pull out an integer argument from the command line
def getArgInt(name, args, min, max):
    try:
        arg = args.next();
    except:
        print(name + ": no argument supplied.");

    try:
        val = int(arg);
    except:
        print(name + ": non-integer value given.");

    if (val < min or val > max):
        print(name + ": value should be between %d and %d" % (min, max));

    return val;

# Function: getArgFloat
# Description:
#	 pull out a float argument from the command line
def getArgFloat(name, args, min, max):
    try:
        arg = args.next();
    except:
        print(name + ": no argument supplied.");

    try:
        val = float(arg);
    except:
        print(name + ": non-integer value given.");

    if (val < min or val > max):
        print(name + ": value should be between %d and %d" % (min, max));

    return val;

# Function: getArgStr
# Description:
#	 pull out a string argument from the command line
def getArgStr(name, args):
    try:
        return args.next();
    except:
        print(name + ": no argument supplied.");
        sys.exit(1);


#def characterSheet():
#    # Create a new canvas object to draw into
#    canvas = canvas.Canvas("worksheet.pdf", pagesize=A4, bottomup=0);
#
#    # Register STSong as a font. We'll use it for chinese writing 
#    pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
#
#    # Draw header information. Name and worksheet name
#    drawOpening(canvas);
#
#    # Where (y-coordinate) to start writing the rows and
#    # by how much each line should be spaced for among 
#    # themselves (vertically).
#    vertPosition = firstPageVertPosStart;
#
#    # Counter for the index of current page and number of rows
#    # in current page.
#    pageCounter = 1;
#    rowCounter = 0;
#
#    # Read all content of the file into a list
#    rows = tuple(open("input.txt"));
#
#    # Draw first page's footer  
#    drawFooter(canvas, pageCounter, numPages(len(rows)));
#
#    # Iterate over all lines from input file
#    for line in rows:
#        # Extract the pinyin and the character apart
#        parts = line.split();
#
#        # Where (x-coordinate) to start writing the rows and
#        # by how much each line should be spaced for among 
#        # themselves (horizontally).
#        horPosition = horPositionStart;
#
#        # Draw one entire row of characters. One at a time.
#        for ind in range(0, 11):
#            # Each column gets progressively opaque, the little
#            # math below is for linearly increasing the chracter
#            # opacity. Furthermore, opacity cannot be lower than
#            # zero, therefore we take care of that too.
#            alpha = 1.0 - ind/10;
#            canvas.setFillAlpha(alpha if (alpha >= 0) else 0);
#
#            # Draw one single characters
#            drawCharacterBox(canvas, (horPosition, vertPosition), parts[0], parts[1]);
#
#            # Increment in horizontal offset for the next character 
#            # box
#            horPosition += horIncrement;
#
#        # Increment in horizontal offset for the next character 
#        # box
#        vertPosition += vertIncrement;
#
#        # Account for the just written character row
#        rowCounter += 1;
#
#        # If the bottom of the page was reached, i.e., the maximum number of
#        # rows per page, we create a new page to draw into and reset vertical
#        # offsets.
#        if (rowCounter % currMaxRowPerPage == 0):
#            # Make the just filled page to show up and start a new one
#            canvas.showPage();
#
#            pageCounter += 1;
#            rowCounter = 0;
#            currMaxRowPerPage = MaxRowsInnerPages;
#            vertPosition = innerPagesVertPosStart;
#
#            # Draw a footer on the recently created page
#            drawFooter(canvas, pageCounter, numPages(len(rows)));
#
#    # Save PDF to file
#    canvas.save()



# Main entry point for the program when being executed from command line
if __name__ == '__main__':
    # Create a new canvas object to draw into
    canvas = canvas.Canvas("worksheet.pdf", pagesize=A4, bottomup=0);

    # Register STSong as a font. We'll use it for chinese writing 
    pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
    
    # Draw header information. Name and worksheet name
    drawOpening(canvas, "汉字练习纸", "Chinese Phrase Writing Sheet");

    # Where (y-coordinate) to start writing the rows and
    # by how much each line should be spaced for among 
    # themselves (vertically).
    vertPosition = firstPageVertPosStart;

    # Counter for the index of current page and number of rows
    # in current page.
    pageCounter = 1;
    rowCounter = 0;

    # Read all content of the file into a list
    fp = open("input2.txt");
    rows = tuple(fp);

    # Draw first page's footer  
    drawFooter(canvas, pageCounter, numPages(len(rows)));

    # Iterate over all lines of the input file.
    # lineIdx always should point to a valid verbatim phrase
    # logic inside the loop access the mandarin phrase
    for lineIdx in range(0, len(rows), 3):
        verbText = rows[lineIdx];
        mandText = rows[lineIdx + 1];

        # Draw one entire phrase. One at a time.
        for ind in range(0, 10):
            # Each column gets progressively opaque, the little
            # math below is for linearly increasing the chracter
            # opacity. Furthermore, opacity cannot be lower than
            # zero, therefore we take care of that too.
            alpha = 1.0 - ind/10;
            canvas.setFillAlpha(alpha if (alpha >= 0) else 0);

            # Draw one single phrase
            drawPhraseBox(canvas, vertPosition, verbText, mandText);

            # Increment in horizontal offset for the next character 
            # box
            vertPosition += vertIncrement;

    # Save PDF to file
    canvas.save()
